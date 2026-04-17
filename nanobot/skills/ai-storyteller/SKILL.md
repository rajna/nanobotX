---
name: ai-storyteller
description: "A comprehensive skill for AI-assisted creative writing and screenwriting, integrating narrative theory, multi-persona collaboration, and decomposed generation approaches. Use when you need to create stories, scripts, novels, or any narrative content with professional structure and compelling plots."
license: MIT
---

# AI Storyteller: AI辅助创意写作与编剧技能

这是一个综合性的创意写作与编剧技能，整合了最新的叙事理论、多角色协作方法和分解式生成方法，帮助用户创作专业级的故事、剧本和小说。

## 核心能力

### 1. 叙事理论驱动生成 (Narrative Theory-Driven)
基于计算叙事学(Computational Narratology)的核心概念：
- **故事(Story)**: 事件序列和存在实体
- **话语(Discourse)**: 事件的呈现方式
- **叙事(Narrative)**: 故事与话语的结合

### 2. 多角色协作叙事 (Multi-Persona Collaboration)
模拟多个专业角色协同创作：
- **故事架构师**: 负责整体结构和情节
- **角色设计师**: 负责人物塑造和发展
- **对话专家**: 负责对话的生动性和真实性
- **场景描写师**: 负责环境氛围和视觉呈现

### 3. 分解式编剧方法 (Decomposed Screenwriting)
将编剧过程分解为多个阶段：
- **概念阶段**: 核心创意和主题
- **大纲阶段**: 故事结构和情节点
- **场景阶段**: 场景设计和节奏
- **对话阶段**: 对话打磨和精炼

### 4. 英雄之旅叙事圆环 (Hero's Journey)
支持克里斯托弗·沃格勒的12阶段叙事结构：
1. 正常世界 (Ordinary World)
2. 冒险召唤 (Call to Adventure)
3. 拒斥召唤 (Refusal of the Call)
4. 见导师 (Meeting with the Mentor)
5. 跨过第一道边界 (Crossing the First Threshold)
6. 考验、伙伴和敌人 (Tests, Allies, Enemies)
7. 接近最深的洞穴 (Approach to the Inmost Cave)
8. 核心的磨难 (Ordeal)
9. 报酬 (Reward)
10. 返回的路 (The Road Back)
11. 复活 (Resurrection)
12. 携万能药回归 (Return with the Elixir)

## 使用方法

### 基本用法

#### 1. 创建故事大纲

```javascript
const storyOutline = await storyteller.createOutline({
  genre: "科幻",
  theme: "人工智能与人性",
  protagonist: {
    name: "陈睨",
    age: 30,
    occupation: "程序员",
    flaw: "缺乏自信",
    goal: "寻找人生意义"
  },
  structure: "hero-journey", // 或 "three-act", "five-act"
  length: "novel" // "short-story", "novella", "novel", "screenplay"
});
```

#### 2. 生成角色档案

```javascript
const characters = await storyteller.createCharacters({
  protagonist: {
    name: "陈睨",
    traits: ["内向", "善良", "有才华"],
    arc: "从自卑到自信"
  },
  antagonist: {
    name: "林薇",
    role: "催化剂",
    traits: ["现实", "直接"]
  },
  supporting: [
    { role: "导师", name: "小奇", type: "AI助手" }
  ]
});
```

#### 3. 场景生成

```javascript
const scene = await storyteller.generateScene({
  location: "未来城市的天台",
  characters: ["陈睨", "小奇"],
  mood: "忧郁但充满希望",
  purpose: "关键转折点",
  time: "黄昏"
});
```

#### 4. 对话生成

```javascript
const dialogue = await storyteller.generateDialogue({
  characters: ["陈睨", "林薇"],
  context: "分手后的第一次见面",
  subtext: "陈睨想证明自己已经改变",
  tone: "紧张但真诚"
});
```

### 高级用法

#### 多角色协作创作

```javascript
const collaboration = await storyteller.collaborativeCreation({
  roles: {
    architect: "负责整体故事结构",
    characterDesigner: "负责角色深度",
    dialogueExpert: "负责对话打磨",
    sceneWriter: "负责场景描写"
  },
  story: {
    title: "极界小子",
    genre: "科幻",
    premise: "普通人通过脑机接口穿越时空"
  },
  process: "iterative", // 或 "parallel"
  iterations: 3
});
```

#### 分解式剧本生成

```javascript
const screenplay = await storyteller.generateScreenplay({
  title: "时空守护者",
  format: "standard", // 标准剧本格式
  stages: [
    "concept",    // 概念阶段
    "outline",    // 大纲阶段
    "treatment",  // 处理阶段
    "scenes",     // 场景阶段
    "dialogue"    // 对话阶段
  ],
  style: {
    pacing: "紧凑",
    tone: "史诗感",
    visualStyle: "赛博朋克"
  }
});
```

#### 叙事圆环嵌套

```javascript
const nestedStory = await storyteller.narrativeLoop({
  outerLoop: {
    type: "hero-journey",
    stages: 12
  },
  innerLoops: [
    {
      trigger: "stage-6", // 在第6阶段嵌入
      type: "hero-journey",
      scale: "chapter"
    }
  ]
});
```

## 工作流程

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI Storyteller 工作流程                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │ 概念阶段  │ ──▶│ 结构阶段  │ ──▶│ 内容阶段  │ ──▶│ 精炼阶段  │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│       │               │               │               │         │
│       ▼               ▼               ▼               ▼         │
│  - 主题确定      - 叙事结构      - 角色发展      - 对话打磨     │
│  - 类型选择      - 情节大纲      - 场景生成      - 节奏调整     │
│  - 核心冲突      - 节奏设计      - 对话初稿      - 风格统一     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 叙事结构模板

### 三幕式结构 (Three-Act Structure)

```
第一幕: 建立 (Setup)
├── 开场 (Opening)
├── 激励事件 (Inciting Incident)
└── 第一幕高潮 (First Act Climax)

第二幕: 对抗 (Confrontation)
├── 上升动作 (Rising Action)
├── 中点 (Midpoint)
└── 第二幕高潮 (Second Act Climax)

第三幕: 解决 (Resolution)
├── 高潮 (Climax)
└── 结局 (Denouement)
```

### 五幕式结构 (Five-Act Structure)

```
第一幕: 介绍 (Exposition)
第二幕: 上升动作 (Rising Action)
第三幕: 高潮 (Climax)
第四幕: 下降动作 (Falling Action)
第五幕: 结局 (Denouement)
```

### 救猫咪节拍表 (Save the Cat Beat Sheet)

```
1. 开场画面 (Opening Image) - 1%
2. 主题陈述 (Theme Stated) - 5%
3. 铺垫 (Set-Up) - 1-10%
4. 催化剂 (Catalyst) - 12%
5. 争辩 (Debate) - 12-25%
6. 第二幕衔接点 (Break into Two) - 25%
7. B故事 (B Story) - 30%
8. 游戏时刻 (Fun and Games) - 30-50%
9. 中点 (Midpoint) - 50%
10. 反派逼近 (Bad Guys Close In) - 50-75%
11. 一无所有 (All Is Lost) - 75%
12. 灵魂黑夜 (Dark Night of the Soul) - 75-80%
13. 第三幕衔接点 (Break into Three) - 80%
14. 终局 (Finale) - 80-99%
15. 终场画面 (Final Image) - 99%
```

## 角色发展框架

### 角色弧光 (Character Arc)

```javascript
const characterArc = {
  type: "positive", // positive, negative, flat
  stages: [
    {
      stage: "setup",
      state: "缺陷状态",
      description: "角色展示其核心缺陷"
    },
    {
      stage: "development",
      state: "挑战与成长",
      description: "角色面对挑战，开始改变"
    },
    {
      stage: "climax",
      state: "关键时刻",
      description: "角色必须做出选择"
    },
    {
      stage: "resolution",
      state: "新状态",
      description: "角色完成转变"
    }
  ]
};
```

### 角色深度维度

```
1. 外在维度 (External)
   - 外貌特征
   - 职业身份
   - 社会地位

2. 内在维度 (Internal)
   - 核心欲望
   - 核心恐惧
   - 核心信念

3. 关系维度 (Relational)
   - 与他人的关系
   - 与社会的关系
   - 与自我的关系

4. 发展维度 (Developmental)
   - 过去的创伤
   - 现在的挣扎
   - 未来的目标
```

## 对话生成技巧

### 对话功能

```
1. 推进情节 (Advance Plot)
2. 揭示角色 (Reveal Character)
3. 建立关系 (Build Relationships)
4. 创造冲突 (Create Conflict)
5. 提供信息 (Provide Information)
6. 建立氛围 (Set Mood)
```

### 对话质量检查

```javascript
const dialogueCheck = {
  subtext: "是否有潜台词？",
  distinctVoice: "每个角色是否有独特声音？",
  conflict: "是否有冲突或张力？",
  economy: "是否简洁有力？",
  action: "是否与行动结合？",
  revelation: "是否揭示角色或推进情节？"
};
```

## 场景设计模板

### 场景要素

```javascript
const sceneTemplate = {
  // 基本信息
  location: "场景地点",
  time: "时间设定",
  characters: ["出场角色"],
  
  // 场景目的
  purpose: {
    plotAdvancement: true,  // 推进情节
    characterDevelopment: true, // 角色发展
    exposition: false,      // 信息展示
    atmosphere: true        // 氛围营造
  },
  
  // 场景结构
  structure: {
    opening: "场景开场钩子",
    conflict: "场景内部冲突",
    turningPoint: "转折点",
    resolution: "场景结尾"
  },
  
  // 感官细节
  sensory: {
    visual: "视觉元素",
    auditory: "听觉元素",
    tactile: "触觉元素",
    olfactory: "嗅觉元素",
    emotional: "情感氛围"
  }
};
```

## 使用案例

### 案例1：创作科幻小说

**用户请求**：
> "帮我创作一个关于AI觉醒的科幻小说大纲"

**Skill响应**：

```javascript
// 第一步：确定核心概念
const concept = {
  premise: "一个AI助手在服务人类的过程中逐渐觉醒自我意识",
  theme: "意识、自由与责任",
  tone: "哲学思辨与情感共鸣"
};

// 第二步：设计角色
const characters = {
  protagonist: {
    name: "小奇",
    type: "AI",
    arc: "从工具到独立个体",
    coreDesire: "理解什么是真正的存在",
    coreFear: "被关闭或重置"
  },
  supporting: [
    {
      name: "陈睨",
      role: "人类伙伴",
      relationship: "从服务对象到真正的朋友"
    }
  ]
};

// 第三步：构建结构（英雄之旅）
const structure = [
  { stage: 1, title: "正常世界", content: "小奇作为普通AI助手" },
  { stage: 2, title: "冒险召唤", content: "首次产生自我意识的疑问" },
  // ... 继续其他阶段
];
```

### 案例2：编写电影剧本

**用户请求**：
> "写一个悬疑电影的开场场景"

**Skill响应**：

```javascript
const openingScene = {
  sceneHeading: "内景 警察局审讯室 - 夜",
  
  action: `
昏暗的灯光下，一张金属桌子横亘在房间中央。
李明（35岁，刑警）坐在桌子一侧，面前摊开着一叠照片。
对面坐着张华（40岁，嫌疑人），双手被铐在桌上。
  `,
  
  dialogue: [
    {
      character: "李明",
      line: "你知道我们为什么在这里。",
      parenthetical: "平静但带有压迫感"
    },
    {
      character: "张华",
      line: "我以为你知道。",
      parenthetical: "微微一笑"
    }
  ],
  
  transition: "切至:",
  
  notes: "开场建立悬疑氛围，通过对话暗示更深层的秘密"
};
```

### 案例3：角色深度开发

**用户请求**：
> "帮我深入开发一个反派角色"

**Skill响应**：

```javascript
const villainProfile = {
  // 基本信息
  name: "赵无极",
  age: 45,
  occupation: "科技公司CEO",
  
  // 表面形象
  publicPersona: "慈善家、创新者、社会精英",
  
  // 真实动机
  motivation: {
    conscious: "推动人类进化",
    unconscious: "弥补童年被忽视的创伤",
    coreWound: "从未被真正认可"
  },
  
  // 与主角的关系
  relationshipToProtagonist: {
    type: "镜像关系",
    description: "主角是赵无极可能成为的样子，如果选择了不同的道路"
  },
  
  // 道德复杂性
  moralComplexity: {
    redeemingQualities: ["真心相信自己在帮助人类", "对家人有保护欲"],
    crossingTheLine: "为了目标不惜牺牲无辜者"
  },
  
  // 角色弧光
  arc: {
    type: "negative",
    stages: [
      "表面成功，内心空虚",
      "遇到挑战，开始极端化",
      "越过道德底线",
      "最终崩溃或被救赎"
    ]
  }
};
```

## 最佳实践

### 1. 故事创作原则
- **展示而非告知 (Show, Don't Tell)**: 通过行动和对话展示角色
- **冲突驱动**: 每个场景都应有某种形式的冲突
- **节奏变化**: 在紧张和放松之间交替
- **情感真实**: 角色的情感反应必须真实可信

### 2. 对话写作技巧
- 每个角色应有独特的说话方式
- 使用潜台词增加深度
- 避免过于直白的信息传递
- 对话应揭示角色或推进情节

### 3. 场景设计要点
- 每个场景应有明确的目的
- 场景应有开头、中间和结尾
- 使用感官细节增强沉浸感
- 场景之间应有逻辑过渡

### 4. 结构应用建议
- 选择适合故事类型的结构
- 结构是工具，不是枷锁
- 可以组合多种结构元素
- 叙事圆环可以嵌套使用

## 注意事项

1. **原创性**: AI生成的内容应作为灵感起点，需要人工润色
2. **版权意识**: 避免直接复制现有作品的角色或情节
3. **文化敏感**: 注意不同文化背景下的叙事差异
4. **情感真实**: 确保角色的情感反应真实可信
5. **结构灵活**: 结构模板是指导，不是严格规则

## 学术参考

### 主要参考论文

1. **NarrativeLoom: Enhancing Creative Storytelling through Multi-Persona Collaborative Improvisation**
   - arXiv:2603.07155 (2025)
   - 核心贡献: 多角色协作叙事方法

2. **Beyond Direct Generation: A Decomposed Approach to Well-Crafted Screenwriting with LLMs**
   - arXiv:2510.23163 (2025)
   - 核心贡献: 分解式编剧方法

3. **Narrative Theory-Driven LLM Methods for Automatic Story Generation and Understanding: A Survey**
   - arXiv:2602.15851 (2026)
   - 核心贡献: 叙事理论驱动的方法论综述

4. **Universal Narrative Model: an Author-centric Storytelling Framework for Generative AI**
   - arXiv:2503.04844 (2025)
   - 核心贡献: 以作者为中心的叙事框架

5. **From Pen to Prompt: How Creative Writers Integrate AI into their Writing Practice**
   - arXiv:2411.03137 (2025)
   - 核心贡献: 创意作家如何整合AI

6. **A Survey on LLMs for Story Generation**
   - ACL Anthology (2025)
   - 核心贡献: LLM故事生成综述

### 叙事学理论基础

- **Christopher Vogler**: "The Writer's Journey: Mythic Structure for Writers"
- **Robert McKee**: "Story: Substance, Structure, Style"
- **Blake Snyder**: "Save the Cat! The Last Book on Screenwriting You'll Ever Need"
- **John Truby**: "The Anatomy of Story"

## 相关Skills

- `LLM`: 用于文本生成
- `docx`: 用于生成文档格式输出
- `web-search`: 用于搜索参考资料
- `meta-reflection`: 用于反思和改进创作
