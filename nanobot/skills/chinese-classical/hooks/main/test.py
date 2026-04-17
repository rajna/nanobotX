
#!/usr/bin/env python3
"""测试 Hook 发现"""

import sys
import re
from pathlib import Path

def test_hook_md(hook_md_path: str):
    """测试 HOOK.md 是否正确"""
    print(f"检查: {hook_md_path}")
    
    path = Path(hook_md_path)
    if not path.exists():
        print(f"❌ 文件不存在")
        return
    
    content = path.read_text(encoding="utf-8")
    print(f"文件内容:\n{content}")
    print()
    
    # 检查格式
    if not content.startswith("---"):
        print("❌ 不是以 --- 开头")
        return
    
    # 解析 frontmatter
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        print("❌ 没有匹配到 frontmatter")
        return
    
    frontmatter = {}
    current_key = None
    current_value = []
    
    for line in match.group(1).split("\n"):
        if line.startswith("  ") and current_key:
            current_value.append(line.strip())
        elif ":" in line:
            if current_key and current_value:
                frontmatter[current_key] = "\n".join(current_value) if len(current_value) > 1 else current_value[0]
                current_value = []
            key, value = line.split(":", 1)
            current_key = key.strip()
            current_value = [value.strip()] if value.strip() else []
    
    if current_key and current_value:
        frontmatter[current_key] = "\n".join(current_value) if len(current_value) > 1 else current_value[0]
    
    print(f"解析结果:")
    for k, v in frontmatter.items():
        print(f"  {k}: {v!r}")
    
    # 检查必要字段
    print()
    if "name" not in frontmatter:
        print("❌ 缺少 name 字段")
    else:
        print(f"✓ name: {frontmatter['name']}")
    
    if "trigger" not in frontmatter:
        print("❌ 缺少 trigger 字段")
    else:
        trigger = frontmatter['trigger']
        print(f"✓ trigger: {trigger!r}")
        
        # 解析 trigger
        for line in str(trigger).split("\n"):
            line = line.strip()
            if line.startswith("event:"):
                event = line.split(":", 1)[1].strip()
                print(f"  event: {event}")
            elif line.startswith("priority:"):
                priority = line.split(":", 1)[1].strip()
                print(f"  priority: {priority}")


def test_hook_py(hook_py_path: str):
    """测试 hook.py 是否正确"""
    print(f"\n检查: {hook_py_path}")
    
    path = Path(hook_py_path)
    if not path.exists():
        print(f"❌ 文件不存在")
        return
    
    content = path.read_text(encoding="utf-8")
    
    # 检查 execute 函数
    if "def execute" in content:
        print("✓ 找到 execute 函数")
        if "async def execute" in content:
            print("  是 async 函数")
        else:
            print("  是 sync 函数")
    else:
        print("❌ 没有 execute 函数")
    
    # 检查语法
    try:
        compile(content, hook_py_path, 'exec')
        print("✓ 语法正确")
    except SyntaxError as e:
        print(f"❌ 语法错误: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python test_hook_discovery.py /path/to/hook/directory")
        sys.exit(1)
    
    hook_dir = Path(sys.argv[1])
    print(f"Hook 目录: {hook_dir}")
    print("=" * 60)
    
    # 检查 HOOK.md
    hook_md = hook_dir / "HOOK.md"
    test_hook_md(str(hook_md))
    
    # 检查 hook.py
    hook_py = hook_dir / "hook.py"
    test_hook_py(str(hook_py))