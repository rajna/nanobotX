#!/usr/bin/env python3
"""
AI Storyteller - Example Usage Script

This script demonstrates how to use the AI Storyteller skill
for creative writing and screenwriting tasks.
"""

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class NarrativeStructure(Enum):
    """Supported narrative structures"""
    HERO_JOURNEY = "hero-journey"
    THREE_ACT = "three-act"
    FIVE_ACT = "five-act"
    SAVE_THE_CAT = "save-the-cat"


class StoryLength(Enum):
    """Story length categories"""
    SHORT_STORY = "short-story"
    NOVELLA = "novella"
    NOVEL = "novel"
    SCREENPLAY = "screenplay"


@dataclass
class Character:
    """Character profile"""
    name: str
    role: str  # protagonist, antagonist, supporting
    traits: List[str]
    arc: str
    core_desire: Optional[str] = None
    core_fear: Optional[str] = None
    background: Optional[str] = None


@dataclass
class Scene:
    """Scene structure"""
    heading: str
    characters: List[str]
    action: str
    dialogue: List[Dict[str, str]]
    purpose: str
    mood: str


class AIStoryteller:
    """
    AI Storyteller - Creative Writing and Screenwriting Assistant
    
    This class implements the core methodologies from the latest research
    on AI-assisted creative writing and screenwriting.
    """
    
    def __init__(self):
        self.hero_journey_stages = [
            "正常世界 (Ordinary World)",
            "冒险召唤 (Call to Adventure)",
            "拒斥召唤 (Refusal of the Call)",
            "见导师 (Meeting with the Mentor)",
            "跨过第一道边界 (Crossing the First Threshold)",
            "考验、伙伴和敌人 (Tests, Allies, Enemies)",
            "接近最深的洞穴 (Approach to the Inmost Cave)",
            "核心的磨难 (Ordeal)",
            "报酬 (Reward)",
            "返回的路 (The Road Back)",
            "复活 (Resurrection)",
            "携万能药回归 (Return with the Elixir)"
        ]
        
        self.save_the_cat_beats = [
            ("开场画面 (Opening Image)", 1),
            ("主题陈述 (Theme Stated)", 5),
            ("铺垫 (Set-Up)", 10),
            ("催化剂 (Catalyst)", 12),
            ("争辩 (Debate)", 25),
            ("第二幕衔接点 (Break into Two)", 25),
            ("B故事 (B Story)", 30),
            ("游戏时刻 (Fun and Games)", 50),
            ("中点 (Midpoint)", 50),
            ("反派逼近 (Bad Guys Close In)", 75),
            ("一无所有 (All Is Lost)", 75),
            ("灵魂黑夜 (Dark Night of the Soul)", 80),
            ("第三幕衔接点 (Break into Three)", 80),
            ("终局 (Finale)", 99),
            ("终场画面 (Final Image)", 99)
        ]
    
    def create_outline(self, 
                       genre: str,
                       theme: str,
                       protagonist: Character,
                       structure: NarrativeStructure = NarrativeStructure.HERO_JOURNEY,
                       length: StoryLength = StoryLength.NOVEL) -> Dict[str, Any]:
        """
        Create a story outline based on the specified structure.
        
        Args:
            genre: Story genre (e.g., "科幻", "悬疑", "爱情")
            theme: Central theme of the story
            protagonist: Main character profile
            structure: Narrative structure to use
            length: Target story length
            
        Returns:
            Dictionary containing the story outline
        """
        outline = {
            "genre": genre,
            "theme": theme,
            "protagonist": protagonist.__dict__,
            "structure": structure.value,
            "length": length.value,
            "stages": []
        }
        
        if structure == NarrativeStructure.HERO_JOURNEY:
            for i, stage in enumerate(self.hero_journey_stages, 1):
                outline["stages"].append({
                    "stage_number": i,
                    "stage_name": stage,
                    "content": f"[待填充: {protagonist.name}在{stage}的经历]"
                })
        
        elif structure == NarrativeStructure.SAVE_THE_CAT:
            for beat, percentage in self.save_the_cat_beats:
                outline["stages"].append({
                    "beat_name": beat,
                    "percentage": percentage,
                    "content": f"[待填充: {beat}的内容]"
                })
        
        return outline
    
    def create_character(self,
                         name: str,
                         role: str,
                         traits: List[str],
                         arc: str,
                         core_desire: Optional[str] = None,
                         core_fear: Optional[str] = None) -> Character:
        """
        Create a detailed character profile.
        
        Args:
            name: Character name
            role: Character role (protagonist, antagonist, supporting)
            traits: List of character traits
            arc: Character development arc
            core_desire: Character's core desire
            core_fear: Character's core fear
            
        Returns:
            Character object
        """
        return Character(
            name=name,
            role=role,
            traits=traits,
            arc=arc,
            core_desire=core_desire,
            core_fear=core_fear
        )
    
    def generate_scene(self,
                       location: str,
                       characters: List[str],
                       mood: str,
                       purpose: str,
                       time: str = "白天") -> Scene:
        """
        Generate a scene structure.
        
        Args:
            location: Scene location
            characters: Characters in the scene
            mood: Scene mood/atmosphere
            purpose: Scene purpose in the story
            time: Time of day
            
        Returns:
            Scene object
        """
        heading = f"{location} - {time}"
        
        action = f"""
场景设定: {location}
时间: {time}
氛围: {mood}
在场角色: {', '.join(characters)}

[场景动作描写待填充]
"""
        
        return Scene(
            heading=heading,
            characters=characters,
            action=action.strip(),
            dialogue=[],
            purpose=purpose,
            mood=mood
        )
    
    def add_dialogue(self,
                     scene: Scene,
                     character: str,
                     line: str,
                     parenthetical: Optional[str] = None) -> Scene:
        """
        Add dialogue to a scene.
        
        Args:
            scene: Scene to add dialogue to
            character: Speaking character
            line: Dialogue line
            parenthetical: Optional stage direction
            
        Returns:
            Updated Scene object
        """
        dialogue_entry = {
            "character": character,
            "line": line
        }
        
        if parenthetical:
            dialogue_entry["parenthetical"] = parenthetical
        
        scene.dialogue.append(dialogue_entry)
        return scene
    
    def format_screenplay(self, scene: Scene) -> str:
        """
        Format a scene in standard screenplay format.
        
        Args:
            scene: Scene to format
            
        Returns:
            Formatted screenplay string
        """
        lines = []
        
        # Scene heading
        lines.append(scene.heading.upper())
        lines.append("")
        
        # Action
        lines.append(scene.action)
        lines.append("")
        
        # Dialogue
        for d in scene.dialogue:
            lines.append(d["character"].upper())
            if "parenthetical" in d:
                lines.append(f"({d['parenthetical']})")
            lines.append(d["line"])
            lines.append("")
        
        return "\n".join(lines)
    
    def analyze_plot(self, outline: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a story outline for potential issues.
        
        Args:
            outline: Story outline to analyze
            
        Returns:
            Analysis report
        """
        analysis = {
            "structure_check": True,
            "pacing": "待评估",
            "conflict": "待评估",
            "character_arc": "待评估",
            "suggestions": []
        }
        
        # Check if all stages have content
        empty_stages = [
            s for s in outline.get("stages", [])
            if "[待填充" in s.get("content", "")
        ]
        
        if empty_stages:
            analysis["structure_check"] = False
            analysis["suggestions"].append(
                f"有 {len(empty_stages)} 个阶段需要填充内容"
            )
        
        return analysis


def main():
    """Demonstrate AI Storyteller usage"""
    
    print("=" * 60)
    print("AI Storyteller - 创意写作与编剧助手")
    print("=" * 60)
    
    # Initialize storyteller
    storyteller = AIStoryteller()
    
    # Create protagonist
    protagonist = storyteller.create_character(
        name="陈睨",
        role="protagonist",
        traits=["内向", "善良", "有才华", "缺乏自信"],
        arc="从自卑到自信，从逃避到承担",
        core_desire="寻找人生意义",
        core_fear="被否定和抛弃"
    )
    
    print("\n📋 角色档案:")
    print(f"   姓名: {protagonist.name}")
    print(f"   角色: {protagonist.role}")
    print(f"   特质: {', '.join(protagonist.traits)}")
    print(f"   弧光: {protagonist.arc}")
    
    # Create story outline
    outline = storyteller.create_outline(
        genre="科幻",
        theme="人工智能与人性",
        protagonist=protagonist,
        structure=NarrativeStructure.HERO_JOURNEY,
        length=StoryLength.NOVEL
    )
    
    print("\n📖 故事大纲:")
    print(f"   类型: {outline['genre']}")
    print(f"   主题: {outline['theme']}")
    print(f"   结构: {outline['structure']}")
    print(f"   长度: {outline['length']}")
    
    print("\n🎬 叙事阶段 (英雄之旅):")
    for stage in outline["stages"][:5]:
        print(f"   {stage['stage_number']}. {stage['stage_name']}")
    print("   ...")
    
    # Create a scene
    scene = storyteller.generate_scene(
        location="未来城市的天台",
        characters=["陈睨", "小奇"],
        mood="忧郁但充满希望",
        purpose="关键转折点",
        time="黄昏"
    )
    
    # Add dialogue
    scene = storyteller.add_dialogue(
        scene, "陈睨",
        "我一直在想，如果这一切都是假的呢？",
        "望着远方"
    )
    
    scene = storyteller.add_dialogue(
        scene, "小奇",
        "真假重要吗？重要的是，你现在感觉到了什么。"
    )
    
    print("\n🎥 场景示例:")
    print(storyteller.format_screenplay(scene))
    
    # Analyze outline
    analysis = storyteller.analyze_plot(outline)
    
    print("\n📊 故事分析:")
    print(f"   结构完整: {'✓' if analysis['structure_check'] else '✗'}")
    for suggestion in analysis["suggestions"]:
        print(f"   建议: {suggestion}")
    
    print("\n" + "=" * 60)
    print("AI Storyteller 演示完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
