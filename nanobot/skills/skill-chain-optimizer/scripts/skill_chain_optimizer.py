#!/usr/bin/env python3
"""
Skill Chain Optimizer: 技能调用链优化器（自动评估版）
支持对话开始推荐、对话结束保存优化
"""

import json
import os
import re
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from collections import defaultdict


class SkillCall:
    """单个技能调用记录"""
    def __init__(
        self,
        skill_name: str,
        timestamp: int,
        duration: int = 0,
        success: bool = True,
        input_data: Optional[Dict] = None,
        output_data: Optional[Dict] = None,
        error_message: Optional[str] = None
    ):
        self.skill_name = skill_name
        self.timestamp = timestamp
        self.duration = duration
        self.success = success
        self.input_data = input_data or {}
        self.output_data = output_data or {}
        self.error_message = error_message

    def to_dict(self) -> Dict[str, Any]:
        return {
            "skillName": self.skill_name,
            "timestamp": self.timestamp,
            "duration": self.duration,
            "success": self.success,
            "input": self.input_data,
            "output": self.output_data,
            "errorMessage": self.error_message
        }


class SkillChain:
    """技能调用链"""
    def __init__(
        self,
        id: str,
        chain: List[SkillCall],
        skill_name_chain: List[str],
        task_description: str,
        task_type: Optional[str] = None,
        tags: List[str] = None,
        created_at: int = None,
        updated_at: int = None
    ):
        self.id = id
        self.chain = chain
        self.skill_name_chain = skill_name_chain
        self.task_description = task_description
        self.task_type = task_type
        self.tags = tags or []
        self.created_at = created_at or int(datetime.now().timestamp() * 1000)
        self.updated_at = updated_at or self.created_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "chain": [call.to_dict() for call in self.chain],
            "skillNameChain": self.skill_name_chain,
            "taskDescription": self.task_description,
            "taskType": self.task_type,
            "tags": self.tags,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        }


class AutoEvaluation:
    """自动评估结果"""
    def __init__(
        self,
        chain_id: str,
        overall_score: float,
        dimensions: Dict[str, float],
        auto_evaluated_at: int,
        evaluation_details: Dict[str, Any]
    ):
        self.chain_id = chain_id
        self.overall_score = overall_score
        self.dimensions = dimensions
        self.auto_evaluated_at = auto_evaluated_at
        self.evaluation_details = evaluation_details

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chainId": self.chain_id,
            "overallScore": self.overall_score,
            "dimensions": self.dimensions,
            "autoEvaluatedAt": self.auto_evaluated_at,
            "evaluationDetails": self.evaluation_details
        }


class TaskRecord:
    """任务记录"""
    def __init__(
        self,
        id: str,
        description: str,
        task_type: Optional[str] = None,
        best_chain_id: Optional[str] = None,
        best_score: Optional[float] = None,
        all_chains: List[Dict[str, Any]] = None,
        created_at: int = None,
        updated_at: int = None
    ):
        self.id = id
        self.description = description
        self.task_type = task_type
        self.best_chain_id = best_chain_id
        self.best_score = best_score
        self.all_chains = all_chains or []
        self.created_at = created_at or int(datetime.now().timestamp() * 1000)
        self.updated_at = updated_at or self.created_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "description": self.description,
            "taskType": self.task_type,
            "bestChainId": self.best_chain_id,
            "bestScore": self.best_score,
            "allChains": [chain.to_dict() if hasattr(chain, 'to_dict') else chain for chain in self.all_chains],
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        }


class SkillChainOptimizer:
    """技能调用链优化器"""

    def __init__(
        self,
        storage_path: str = "./data/skill-chains",
        similarity_threshold: float = 0.35,
        max_chains_per_task: int = 5,
        enable_auto_optimize: bool = True,
        evaluation_weights: Optional[Dict[str, float]] = None,
        efficiency_baseline: Optional[Dict[str, int]] = None
    ):
        self.storage_path = storage_path
        self.similarity_threshold = similarity_threshold
        self.max_chains_per_task = max_chains_per_task
        self.enable_auto_optimize = enable_auto_optimize

        # 默认评估权重
        self.evaluation_weights = evaluation_weights or {
            "successRate": 0.4,      # 40% 权重
            "efficiency": 0.25,      # 25% 权重
            "completeness": 0.2,     # 20% 权重
            "chainLength": 0.15      # 15% 权重
        }

        # 默认效率基准
        self.efficiency_baseline = efficiency_baseline or {
            "ideal_duration": 2000,   # 2秒理想
            "max_duration": 30000     # 30秒最大
        }

        # 数据存储
        self.tasks: Dict[str, TaskRecord] = {}
        self.chains: Dict[str, SkillChain] = {}
        self.evaluations: Dict[str, AutoEvaluation] = {}
        self.initialized = False

        # 当前对话上下文
        self.current_task_id: Optional[str] = None
        self.current_skill_calls: List[Dict[str, Any]] = []

        # 确保存储目录存在
        os.makedirs(storage_path, exist_ok=True)

    def initialize(self) -> None:
        """初始化优化器"""
        if self.initialized:
            return

        # 加载已有数据
        self._load_data()

        self.initialized = True
        print(f"✅ Skill Chain Optimizer initialized (Auto-Evaluation Mode)")

    def _load_data(self) -> None:
        """加载数据"""
        tasks_path = os.path.join(self.storage_path, "tasks.json")
        chains_path = os.path.join(self.storage_path, "chains.json")
        evaluations_path = os.path.join(self.storage_path, "evaluations.json")

        try:
            if os.path.exists(tasks_path):
                with open(tasks_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 转换字段名：驼峰命名 -> 蛇形命名
                    converted_data = {}
                    for k, v in data.items():
                        converted = {}
                        for field, value in v.items():
                            # 转换驼峰命名为蛇形命名
                            snake_field = field
                            if field == "taskType":
                                snake_field = "task_type"
                            elif field == "bestChainId":
                                snake_field = "best_chain_id"
                            elif field == "bestScore":
                                snake_field = "best_score"
                            elif field == "allChains":
                                snake_field = "all_chains"
                            elif field == "createdAt":
                                snake_field = "created_at"
                            elif field == "updatedAt":
                                snake_field = "updated_at"
                            elif field == "skillNameChain":
                                snake_field = "skill_name_chain"
                            elif field == "skillCalls":
                                snake_field = "skill_calls"
                            elif field == "taskDescription":
                                snake_field = "task_description"
                            converted[snake_field] = value
                        converted_data[k] = converted
                    self.tasks = {k: TaskRecord(**v) for k, v in converted_data.items()}

            if os.path.exists(chains_path):
                with open(chains_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 转换字段名：驼峰命名 -> 蛇形命名
                    converted_data = {}
                    for k, v in data.items():
                        converted = {}
                        for field, value in v.items():
                            snake_field = field
                            if field == "taskType":
                                snake_field = "task_type"
                            elif field == "bestChainId":
                                snake_field = "best_chain_id"
                            elif field == "bestScore":
                                snake_field = "best_score"
                            elif field == "allChains":
                                snake_field = "all_chains"
                            elif field == "createdAt":
                                snake_field = "created_at"
                            elif field == "updatedAt":
                                snake_field = "updated_at"
                            elif field == "skillNameChain":
                                snake_field = "skill_name_chain"
                            elif field == "skillCalls":
                                snake_field = "skill_calls"
                            elif field == "taskDescription":
                                snake_field = "task_description"
                            converted[snake_field] = value
                        converted_data[k] = converted
                    self.chains = {k: SkillChain(**v) for k, v in converted_data.items()}

            if os.path.exists(evaluations_path):
                with open(evaluations_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 转换字段名：驼峰命名 -> 蛇形命名
                    converted_data = {}
                    for k, v in data.items():
                        converted = {}
                        for field, value in v.items():
                            snake_field = field
                            if field == "chainId":
                                snake_field = "chain_id"
                            elif field == "overallScore":
                                snake_field = "overall_score"
                            elif field == "dimensions":
                                snake_field = "dimensions"
                            elif field == "autoEvaluatedAt":
                                snake_field = "auto_evaluated_at"
                            elif field == "evaluationDetails":
                                snake_field = "evaluation_details"
                            converted[snake_field] = value
                        converted_data[k] = converted
                    self.evaluations = {k: AutoEvaluation(**v) for k, v in converted_data.items()}

            print(f"📂 Loaded {len(self.tasks)} tasks, {len(self.chains)} chains")
        except Exception as e:
            print(f"Error loading data: {e}")

    def _save_data(self) -> None:
        """保存数据"""
        tasks_path = os.path.join(self.storage_path, "tasks.json")
        chains_path = os.path.join(self.storage_path, "chains.json")
        evaluations_path = os.path.join(self.storage_path, "evaluations.json")

        try:
            with open(tasks_path, 'w', encoding='utf-8') as f:
                tasks_data = {}
                for k, v in self.tasks.items():
                    if hasattr(v, 'to_dict'):
                        tasks_data[k] = v.to_dict()
                    else:
                        tasks_data[k] = v
                json.dump(tasks_data, f, ensure_ascii=False, indent=2)

            with open(chains_path, 'w', encoding='utf-8') as f:
                chains_data = {}
                for k, v in self.chains.items():
                    if hasattr(v, 'to_dict'):
                        chains_data[k] = v.to_dict()
                    else:
                        chains_data[k] = v
                json.dump(chains_data, f, ensure_ascii=False, indent=2)

            with open(evaluations_path, 'w', encoding='utf-8') as f:
                evaluations_data = {}
                for k, v in self.evaluations.items():
                    if hasattr(v, 'to_dict'):
                        evaluations_data[k] = v.to_dict()
                    else:
                        evaluations_data[k] = v
                json.dump(evaluations_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")

    def _generate_id(self, prefix: str) -> str:
        """生成唯一ID"""
        return f"{prefix}_{int(datetime.now().timestamp() * 1000)}_{os.urandom(4).hex()}"

    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 移除标点符号
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
        
        # 中文分词（简单实现：按字符分割）
        # 对于中文，我们提取2-4字的词组
        keywords = []
        
        # 提取中文词组
        chinese_chars = re.findall(r'[\u4e00-\u9fff]+', text)
        for phrase in chinese_chars:
            # 添加整个词组
            if len(phrase) >= 2:
                keywords.append(phrase)
            
            # 添加2-4字的子词组
            for i in range(len(phrase)):
                for length in [2, 3, 4]:
                    if i + length <= len(phrase):
                        keywords.append(phrase[i:i+length])
        
        # 提取英文单词
        english_words = re.findall(r'[a-zA-Z]+', text.lower())
        keywords.extend([w for w in english_words if len(w) > 1])
        
        # 过滤停用词
        stopwords = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '个', '什么', '怎么', '如何'}
        
        keywords = [w for w in keywords if w not in stopwords]
        
        return list(set(keywords))  # 去重

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度（改进版）"""
        # 提取关键词
        keywords1 = set(self._extract_keywords(text1))
        keywords2 = set(self._extract_keywords(text2))
        
        if not keywords1 or not keywords2:
            return 0.0
        
        # Jaccard相似度
        intersection = keywords1 & keywords2
        union = keywords1 | keywords2
        
        jaccard = len(intersection) / len(union) if union else 0
        
        # 考虑关键词重叠比例
        overlap1 = len(intersection) / len(keywords1) if keywords1 else 0
        overlap2 = len(intersection) / len(keywords2) if keywords2 else 0
        
        # 综合相似度
        similarity = jaccard * 0.5 + (overlap1 + overlap2) / 2 * 0.5
        
        return similarity

    def _find_or_create_task(self, description: str, task_type: Optional[str] = None) -> str:
        """查找或创建任务"""
        # 先查找相似任务
        similar = self._find_similar_tasks(description)

        if similar and similar[0]["similarity"] >= 0.95:
            return similar[0]["taskId"]

        # 创建新任务
        task_id = self._generate_id("task")
        task = TaskRecord(
            id=task_id,
            description=description,
            task_type=task_type,
            all_chains=[]
        )

        self.tasks[task_id] = task
        return task_id

    def _find_similar_tasks(self, description: str) -> List[Dict[str, Any]]:
        """查找相似任务"""
        results = []

        for task_id, task in self.tasks.items():
            similarity = self._calculate_similarity(description, task.description)

            if similarity >= self.similarity_threshold:
                results.append({
                    "taskId": task_id,
                    "similarity": similarity,
                    "description": task.description
                })

        # 按相似度排序
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results

    def _auto_evaluate(
        self,
        chain: SkillChain,
        task_completed: bool,
        task_output: Any = None
    ) -> AutoEvaluation:
        """自动评估调用链"""
        skill_calls = chain.chain
        weights = self.evaluation_weights
        baseline = self.efficiency_baseline

        # 计算评估详情
        total_skills = len(skill_calls)
        successful_skills = sum(1 for call in skill_calls if call.success)
        total_duration = sum(call.duration for call in skill_calls)
        average_duration = total_duration / total_skills if total_skills > 0 else 0
        has_errors = any(not call.success for call in skill_calls)

        # 1. 成功率评分 (0-100)
        success_rate = (successful_skills / total_skills) * 100 if total_skills > 0 else 0
        success_rate_score = task_completed * success_rate

        # 2. 效率评分 (0-100) - 基于执行时间
        efficiency_score = 100
        if total_duration > baseline["ideal_duration"]:
            over_ratio = (total_duration - baseline["ideal_duration"]) / (baseline["max_duration"] - baseline["ideal_duration"])
            efficiency_score = max(0, 100 - over_ratio * 100)

        # 3. 完整性评分 (0-100) - 基于任务完成和输出
        completeness_score = 100
        if not task_completed:
            completeness_score = 30
        elif has_errors:
            completeness_score = 70

        # 4. 链长度评分 (0-100) - 链越短越好（在完成任务的前提下）
        chain_length_score = 100
        if total_skills > 3:
            chain_length_score = max(50, 100 - (total_skills - 3) * 10)

        # 计算加权总分
        overall_score = round(
            success_rate_score * weights["successRate"] +
            efficiency_score * weights["efficiency"] +
            completeness_score * weights["completeness"] +
            chain_length_score * weights["chainLength"]
        )

        return AutoEvaluation(
            chain_id=chain.id,
            overall_score=overall_score,
            dimensions={
                "successRate": round(success_rate_score),
                "efficiency": round(efficiency_score),
                "completeness": round(completeness_score),
                "chainLength": round(chain_length_score)
            },
            auto_evaluated_at=int(datetime.now().timestamp() * 1000),
            evaluation_details={
                "totalSkills": total_skills,
                "successfulSkills": successful_skills,
                "totalDuration": total_duration,
                "averageDuration": round(average_duration, 2),
                "hasErrors": has_errors
            }
        )

    def _update_best_chain(self, task_id: str) -> bool:
        """更新最佳调用链"""
        task = self.tasks.get(task_id)
        if not task:
            return False

        # 找出评分最高的链
        sorted_chains = sorted(
            task.all_chains,
            key=lambda x: x["score"],
            reverse=True
        )

        if sorted_chains:
            new_best = sorted_chains[0]

            # 检查是否需要更新
            if task.best_chain_id != new_best["chainId"]:
                task.best_chain_id = new_best["chainId"]
                task.best_score = new_best["score"]
                return True

        # 如果超过最大保存数，移除评分最低的链
        if len(task.all_chains) > self.max_chains_per_task:
            task.all_chains.sort(key=lambda x: x["score"], reverse=True)
            removed = task.all_chains.pop(self.max_chains_per_task)

            # 从存储中移除
            if removed["chainId"] in self.chains:
                del self.chains[removed["chainId"]]
            if removed["chainId"] in self.evaluations:
                del self.evaluations[removed["chainId"]]

            # 保存到文件
            self._save_data()

        return False

    # ==================== 新增方法：对话开始推荐 ====================

    def recommend_chain_for_task(self, task_description: str) -> Dict[str, Any]:
        """
        对话开始时推荐最佳skill chain
        
        Args:
            task_description: 任务描述
            
        Returns:
            推荐结果，包含推荐的skill chain和置信度
        """
        if not self.initialized:
            self.initialize()

        # 查找相似任务
        similar_tasks = self._find_similar_tasks(task_description)

        if not similar_tasks:
            return {
                "recommended": False,
                "reason": "没有找到相似任务",
                "skillChain": [],
                "confidence": 0,
                "similarTasks": []
            }

        # 获取最相似任务的最佳链
        best_match = similar_tasks[0]
        task = self.tasks.get(best_match["taskId"])

        if not task or not task.best_chain_id:
            return {
                "recommended": False,
                "reason": "相似任务没有最佳链",
                "skillChain": [],
                "confidence": best_match["similarity"],
                "similarTasks": similar_tasks
            }

        chain = self.chains.get(task.best_chain_id)
        evaluation = self.evaluations.get(task.best_chain_id)

        # 设置当前任务上下文
        self.current_task_id = task.id
        self.current_skill_calls = []

        return {
            "recommended": True,
            "reason": f"找到相似任务（相似度: {best_match['similarity']:.1%}）",
            "skillChain": chain.skill_name_chain if chain else [],
            "confidence": best_match["similarity"],
            "historicalScore": evaluation.overall_score if evaluation else 0,
            "similarTasks": similar_tasks[:3],  # 只返回前3个
            "taskId": task.id
        }

    # ==================== 新增方法：记录skill调用 ====================

    def record_skill_call(
        self,
        skill_name: str,
        duration: int = 0,
        success: bool = True,
        input_data: Optional[Dict] = None,
        output_data: Optional[Dict] = None,
        error_message: Optional[str] = None
    ) -> None:
        """
        记录单个skill调用（在执行过程中调用）
        
        Args:
            skill_name: skill名称
            duration: 执行时长（毫秒）
            success: 是否成功
            input_data: 输入数据
            output_data: 输出数据
            error_message: 错误信息
        """
        call = {
            "skill_name": skill_name,
            "timestamp": int(datetime.now().timestamp() * 1000),
            "duration": duration,
            "success": success,
            "input_data": input_data or {},
            "output_data": output_data or {},
            "error_message": error_message
        }
        
        self.current_skill_calls.append(call)

    # ==================== 新增方法：对话结束保存优化 ====================

    def save_and_optimize_chain(
        self,
        task_description: str,
        task_completed: bool = True,
        task_output: Any = None,
        task_type: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        对话结束时保存并优化skill chain
        
        Args:
            task_description: 任务描述
            task_completed: 任务是否完成
            task_output: 任务输出
            task_type: 任务类型
            tags: 标签
            
        Returns:
            保存结果，包含评分和是否替换了旧链
        """
        if not self.initialized:
            self.initialize()

        # 如果没有记录任何skill调用，返回空结果
        if not self.current_skill_calls:
            return {
                "saved": False,
                "reason": "没有记录到skill调用",
                "skillChain": [],
                "score": 0
            }

        # 使用record_and_evaluate保存
        result = self.record_and_evaluate(
            task_description=task_description,
            skill_calls=self.current_skill_calls,
            task_type=task_type,
            tags=tags,
            task_completed=task_completed,
            task_output=task_output
        )

        # 清空当前上下文
        self.current_task_id = None
        self.current_skill_calls = []

        return {
            "saved": True,
            "taskId": result["taskId"],
            "chainId": result["chainId"],
            "skillChain": result["skillNameChain"],
            "score": result["evaluation"]["overallScore"],
            "isBestChain": result["isBestChain"],
            "previousBestScore": result["previousBestScore"],
            "evaluation": result["evaluation"]
        }

    # ==================== 原有方法保持不变 ====================

    def record_and_evaluate(
        self,
        task_description: str,
        skill_calls: List[Dict[str, Any]],
        task_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        task_completed: bool = True,
        task_output: Any = None
    ) -> Dict[str, Any]:
        """
        记录技能调用链并自动评估

        Args:
            task_description: 任务描述
            skill_calls: 技能调用列表
            task_type: 任务类型
            tags: 标签
            task_completed: 任务是否完成
            task_output: 任务输出

        Returns:
            任务完成结果
        """
        if not self.initialized:
            self.initialize()

        # 生成ID
        chain_id = self._generate_id("chain")
        now = int(datetime.now().timestamp() * 1000)

        # 提取技能名称链（支持skillName和skill_name两种键名）
        skill_name_chain = [call.get("skillName") or call.get("skill_name", "unknown") for call in skill_calls]

        # 创建调用链记录 - 转换字典键名以匹配SkillCall构造函数
        converted_calls = []
        for call in skill_calls:
            converted = {}
            for key, value in call.items():
                # 转换键名
                if key == "skillName":
                    converted["skill_name"] = value
                elif key == "input":
                    converted["input_data"] = value
                elif key == "output":
                    converted["output_data"] = value
                elif key == "errorMessage":
                    converted["error_message"] = value
                else:
                    converted[key] = value
            converted_calls.append(converted)
        
        chain = SkillChain(
            id=chain_id,
            chain=[SkillCall(**call) for call in converted_calls],
            skill_name_chain=skill_name_chain,
            task_description=task_description,
            task_type=task_type,
            tags=tags or [],
            created_at=now,
            updated_at=now
        )

        # 自动评估
        evaluation = self._auto_evaluate(chain, task_completed, task_output)

        # 查找或创建任务记录
        task_id = self._find_or_create_task(task_description, task_type)

        # 保存调用链和评估
        self.chains[chain_id] = chain
        self.evaluations[chain_id] = evaluation

        # 更新任务记录
        task = self.tasks[task_id]
        previous_best_score = task.best_score

        task.all_chains.append({
            "chainId": chain_id,
            "score": evaluation.overall_score,
            "skillNameChain": skill_name_chain,
            "usedAt": now
        })
        task.updated_at = now

        # 自动优化：更新最佳调用链
        is_best_chain = False
        if self.enable_auto_optimize:
            is_best_chain = self._update_best_chain(task_id)

        self.tasks[task_id] = task

        # 持久化
        self._save_data()

        return {
            "taskId": task_id,
            "chainId": chain_id,
            "skillNameChain": skill_name_chain,
            "evaluation": evaluation.to_dict(),
            "isBestChain": is_best_chain,
            "previousBestScore": previous_best_score
        }

    def get_best_chain(self, task_description: str) -> Dict[str, Any]:
        """
        获取推荐的最佳调用链

        Args:
            task_description: 任务描述

        Returns:
            推荐结果
        """
        if not self.initialized:
            self.initialize()

        # 查找相似任务
        similar_tasks = self._find_similar_tasks(task_description)

        if not similar_tasks:
            return {
                "chain": None,
                "evaluation": None,
                "skillNameChain": [],
                "confidence": 0,
                "similarTasks": []
            }

        # 获取最相似任务的最佳链
        best_match = similar_tasks[0]
        task = self.tasks.get(best_match["taskId"])

        if not task or not task.best_chain_id:
            return {
                "chain": None,
                "evaluation": None,
                "skillNameChain": [],
                "confidence": best_match["similarity"],
                "similarTasks": similar_tasks
            }

        chain = self.chains.get(task.best_chain_id)
        evaluation = self.evaluations.get(task.best_chain_id)

        return {
            "chain": chain,
            "evaluation": evaluation,
            "skillNameChain": chain.skill_name_chain if chain else [],
            "confidence": best_match["similarity"],
            "similarTasks": similar_tasks
        }

    def get_task_chain_history(self, task_id: str) -> Dict[str, Any]:
        """
        获取任务的技能名称链历史

        Args:
            task_id: 任务ID

        Returns:
            历史记录
        """
        task = self.tasks.get(task_id)
        if not task:
            return {"skillNameChains": [], "scores": [], "bestChain": []}

        skill_name_chains = [record["skillNameChain"] for record in task.all_chains]
        scores = [record["score"] for record in task.all_chains]

        return {
            "skillNameChains": skill_name_chains,
            "scores": scores,
            "bestChain": task.best_chain_id and self.chains.get(task.best_chain_id).skill_name_chain if task.best_chain_id else []
        }

    def get_stats(self) -> Dict[str, Any]:
        """
        获取统计信息

        Returns:
            统计信息
        """
        total_score = 0
        evaluated_count = 0
        skill_stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"count": 0, "totalScore": 0})
        task_type_distribution: Dict[str, int] = defaultdict(int)

        # 统计评分和技能使用
        for chain_id, evaluation in self.evaluations.items():
            total_score += evaluation.overall_score
            evaluated_count += 1

            chain = self.chains.get(chain_id)
            if chain:
                # 处理chain.chain可能是字典列表或SkillCall对象列表
                for call in chain.chain:
                    if isinstance(call, dict):
                        skill_name = call.get("skillName") or call.get("skill_name", "unknown")
                    else:
                        skill_name = call.skill_name
                    skill_stats[skill_name]["count"] += 1
                    skill_stats[skill_name]["totalScore"] += evaluation.overall_score

        # 统计任务类型分布
        for task in self.tasks.values():
            task_type = task.task_type or "unknown"
            task_type_distribution[task_type] += 1

        # 排序热门技能
        top_skills = [
            {
                "skillName": skill_name,
                "usageCount": stats["count"],
                "avgScore": round(stats["totalScore"] / stats["count"])
            }
            for skill_name, stats in skill_stats.items()
        ]
        top_skills.sort(key=lambda x: x["usageCount"], reverse=True)
        top_skills = top_skills[:10]

        # 获取最佳链列表
        best_chains = []
        for task in self.tasks.values():
            if task.best_chain_id and task.best_score:
                chain = self.chains.get(task.best_chain_id)
                if chain:
                    # 处理skill_name_chain可能是字典列表或字符串列表
                    skill_name_chain = []
                    for item in chain.skill_name_chain:
                        if isinstance(item, dict):
                            skill_name_chain.append(item.get("skillName") or item.get("skill_name", "unknown"))
                        else:
                            skill_name_chain.append(item)

                    best_chains.append({
                        "taskDescription": task.description,
                        "skillNameChain": skill_name_chain,
                        "score": task.best_score
                    })

        best_chains.sort(key=lambda x: x["score"], reverse=True)
        best_chains = best_chains[:10]

        return {
            "totalTasks": len(self.tasks),
            "totalChains": len(self.chains),
            "averageScore": round(total_score / evaluated_count) if evaluated_count > 0 else 0,
            "topSkills": top_skills,
            "taskTypeDistribution": dict(task_type_distribution),
            "bestChains": best_chains
        }

    def export_data(self) -> Dict[str, Any]:
        """
        导出数据

        Returns:
            导出的数据
        """
        return {
            "tasks": [task.to_dict() for task in self.tasks.values()],
            "chains": [chain.to_dict() for chain in self.chains.values()],
            "evaluations": [eval.to_dict() for eval in self.evaluations.values()]
        }


# ==================== 使用示例 ====================

def demo():
    """演示技能调用链优化器"""
    print("\n🎯 Skill Chain Optimizer Demo (Auto-Evaluation)")
    print("=" * 55)

    optimizer = SkillChainOptimizer(
        storage_path="./data/skill-chains",
        max_chains_per_task=5,
        enable_auto_optimize=True
    )

    optimizer.initialize()

    # ==================== 场景1：对话开始推荐 ====================
    print("\n📌 场景1：对话开始推荐")
    print("-" * 55)
    
    recommendation = optimizer.recommend_chain_for_task("今日股市行情分析")
    
    if recommendation["recommended"]:
        print(f"✅ 推荐skill chain: {' → '.join(recommendation['skillChain'])}")
        print(f"   置信度: {recommendation['confidence']:.1%}")
        print(f"   历史评分: {recommendation['historicalScore']}/100")
    else:
        print(f"❌ {recommendation['reason']}")

    # ==================== 场景2：执行过程中记录 ====================
    print("\n📌 场景2：执行过程中记录skill调用")
    print("-" * 55)
    
    # 记录第一个skill调用
    optimizer.record_skill_call(
        skill_name="stock-query",
        duration=1500,
        success=True,
        input_data={"query": "A股行情"},
        output_data={"stocks": 5489}
    )
    print("   ✅ 记录: stock-query (1500ms)")
    
    # 记录第二个skill调用
    optimizer.record_skill_call(
        skill_name="web-search",
        duration=2000,
        success=True,
        input_data={"query": "今日行情"},
        output_data={"results": 5}
    )
    print("   ✅ 记录: web-search (2000ms)")
    
    # 记录第三个skill调用
    optimizer.record_skill_call(
        skill_name="LLM",
        duration=3000,
        success=True,
        input_data={"prompt": "分析行情"},
        output_data={"analysis": "..."}
    )
    print("   ✅ 记录: LLM (3000ms)")

    # ==================== 场景3：对话结束保存优化 ====================
    print("\n📌 场景3：对话结束保存优化")
    print("-" * 55)
    
    result = optimizer.save_and_optimize_chain(
        task_description="今日股市行情分析",
        task_completed=True,
        task_type="stock-analysis"
    )
    
    if result["saved"]:
        print(f"✅ 已保存skill chain: {' → '.join(result['skillChain'])}")
        print(f"   自动评分: {result['score']}/100")
        
        if result["isBestChain"]:
            print(f"   🏆 这是目前最佳方案！")
            if result["previousBestScore"]:
                print(f"   替换了旧方案（评分: {result['previousBestScore']}/100）")
        
        print(f"\n   评分详情:")
        eval = result["evaluation"]
        print(f"     - 成功率: {eval['dimensions']['successRate']}/100")
        print(f"     - 效率: {eval['dimensions']['efficiency']}/100")
        print(f"     - 完整性: {eval['dimensions']['completeness']}/100")
        print(f"     - 链长度: {eval['dimensions']['chainLength']}/100")

    # ==================== 场景4：再次推荐（应该找到历史记录） ====================
    print("\n📌 场景4：再次推荐相同任务")
    print("-" * 55)
    
    recommendation2 = optimizer.recommend_chain_for_task("分析今日股市")
    
    if recommendation2["recommended"]:
        print(f"✅ 推荐skill chain: {' → '.join(recommendation2['skillChain'])}")
        print(f"   置信度: {recommendation2['confidence']:.1%}")
        print(f"   历史评分: {recommendation2['historicalScore']}/100")

    # ==================== 统计信息 ====================
    print("\n📌 统计信息")
    print("-" * 55)
    
    stats = optimizer.get_stats()
    print(f"   总任务数: {stats['totalTasks']}")
    print(f"   总调用链数: {stats['totalChains']}")
    print(f"   平均评分: {stats['averageScore']}/100")

    print("\n✅ Demo completed!")


if __name__ == "__main__":
    demo()
