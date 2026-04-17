#!/usr/bin/env python3
"""
Horoscope Fetcher - 星盘数据获取工具

从 deepastro.cn API 获取本命盘数据
"""

from __future__ import annotations

import argparse
import json
import sys
import os
from datetime import datetime, timedelta, timezone
from urllib.parse import quote
import requests


# 星座映射
ZODIAC_SIGNS = {
    0: "白羊座 (Aries)",
    1: "金牛座 (Taurus)",
    2: "双子座 (Gemini)",
    3: "巨蟹座 (Cancer)",
    4: "狮子座 (Leo)",
    5: "处女座 (Virgo)",
    6: "天秤座 (Libra)",
    7: "天蝎座 (Scorpio)",
    8: "射手座 (Sagittarius)",
    9: "摩羯座 (Capricorn)",
    10: "水瓶座 (Aquarius)",
    11: "双鱼座 (Pisces)"
}

# 行星中文名
PLANET_NAMES = {
    "sun": "太阳",
    "moon": "月亮",
    "mercury": "水星",
    "venus": "金星",
    "mars": "火星",
    "jupiter": "木星",
    "saturn": "土星",
    "uranus": "天王星",
    "neptune": "海王星",
    "pluto": "冥王星",
    "chiron": "凯龙星",
    "lilith": "莉莉丝",
    "ceres": "谷神星",
    "vesta": "灶神星",
    "pallas": "帕拉斯",
    "juno": "朱诺",
    "north_node": "北交点",
    "asc": "上升",
    "dc": "下降",
    "ic": "天底",
    "mc": "中天"
}

# 相位类型
ASPECT_TYPES = {
    0: "合相",
    60: "六合",
    90: "刑",
    120: "拱",
    180: "冲"
}


def geocode_address(address: str) -> tuple[float, float] | None:
    """
    使用 Nominatim API 将地址转换为经纬度

    Args:
        address: 地址字符串

    Returns:
        (latitude, longitude) 或 None
    """
    try:
        url = f"https://nominatim.openstreetmap.org/search"
        params = {
            "q": address,
            "format": "json",
            "limit": 1
        }
        headers = {
            "User-Agent": "Horoscope-Fetcher/1.0"
        }

        response = requests.get(url, params=params, headers=headers, timeout=10, verify=False)
        response.raise_for_status()

        data = response.json()
        if data and len(data) > 0:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            return lat, lon

    except Exception as e:
        print(f"⚠️  地理编码失败: {e}", file=sys.stderr)

    return None


def format_time(time_str: str, source_tz_offset: int = 8, target_tz: str = "GMT") -> str:
    """
    格式化时间为 API 需要的格式

    Args:
        time_str: 时间字符串 (YYYY-MM-DD HH:MM:SS)，本地时间
        source_tz_offset: 源时区偏移（小时），默认 8 (CST, UTC+8)
                         例如：中国=8, 南非=2, 英国=0, 美国东部=-5
        target_tz: 目标时区 (默认 GMT)

    Returns:
        格式化后的时间字符串（转换为目标时区）
    """
    try:
        # 解析时间字符串（本地时间）
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

        # 转换为目标时区时间
        # 如果源时区是 UTC+8，目标时区是 GMT (UTC+0)，则减去8小时
        # 如果源时区是 UTC+2，目标时区是 GMT (UTC+0)，则减去2小时
        tz_offset = timedelta(hours=source_tz_offset)
        dt_target = dt - tz_offset

        # 格式: Wed, 09 Oct 1940 17:30:00 GMT
        formatted = dt_target.strftime("%a, %d %b %Y %H:%M:%S")
        return f"{formatted} {target_tz}"
    except ValueError:
        raise ValueError(f"时间格式错误，请使用 YYYY-MM-DD HH:MM:SS 格式")


def get_horoscope(
    time_str: str,
    address: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    source_tz_offset: int = 8,
    target_tz: str = "GMT",
    show_desc: bool = True
) -> dict:
    """
    获取星盘数据

    Args:
        time_str: 时间字符串 (YYYY-MM-DD HH:MM:SS)
        address: 地址
        latitude: 纬度
        longitude: 经度
        source_tz_offset: 源时区偏移（小时），默认 8 (CST, UTC+8)
                         例如：中国=8, 南非=2, 英国=0, 美国东部=-5
        target_tz: 目标时区 (默认 GMT)
        show_desc: 是否显示描述

    Returns:
        星盘数据字典
    """
    # 格式化时间
    formatted_time = format_time(time_str, source_tz_offset, target_tz)

    # 处理位置信息
    if latitude is None or longitude is None:
        if address:
            # 使用地理编码
            coords = geocode_address(address)
            if coords:
                latitude, longitude = coords
                print(f"📍 地址 '{address}' 解析为: {latitude:.5f}, {longitude:.5f}")
            else:
                raise ValueError(f"无法解析地址: {address}，请直接提供经纬度")
        else:
            raise ValueError("必须提供地址或经纬度")

    # 构建 API URL
    base_url = "https://horoscope.deepastro.cn/horoscope"
    params = {
        "time": formatted_time,
        "latitude": latitude,
        "longitude": longitude,
        "isShowDesc": "true" if show_desc else "false"
    }

    if address:
        params["address"] = address

    # 构建完整 URL
    url = f"{base_url}?time={quote(params['time'])}"
    if "address" in params:
        url += f"&address={quote(params['address'])}"
    url += f"&latitude={params['latitude']}"
    url += f"&longitude={params['longitude']}"
    url += f"&isShowDesc={params['isShowDesc']}"

    # 打印 URL
    print(f"\n🔗 API URL:\n{url}\n")

    # 调用 API
    try:
        response = requests.get(url, timeout=30, verify=False)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        raise RuntimeError(f"API 调用失败: {e}")


def print_summary(data: dict, show_desc: bool = True):
    """打印星盘摘要"""
    if "data" not in data:
        print("❌ 无效的响应数据")
        return

    d = data["data"]

    print("\n" + "=" * 60)
    print("🌟 星盘摘要")
    print("=" * 60)

    # 基本信息
    if "info1" in d:
        print(f"\n📌 基本信息:")
        print(f"   {d['info1']}")

    # 行星位置
    if "astros" in d:
        print(f"\n🪐 行星位置:")
        for planet_name, planet_data in d["astros"].items():
            if planet_name in PLANET_NAMES:
                name = PLANET_NAMES[planet_name]
                # API 返回的 sign 索引从 1 开始，需要减 1
                sign_index = planet_data.get("sign", 1) - 1
                sign = ZODIAC_SIGNS.get(sign_index, "未知")
                pos = planet_data.get("position", {})
                if pos:
                    deg = pos.get("degrees", 0)
                    minute = pos.get("minutes", 0)
                    print(f"   {name:8s} → {sign:15s} ({deg}°{minute}')")

    # 四轴
    if "axes" in d:
        print(f"\n🎯 四轴:")
        for axis_name, axis_data in d["axes"].items():
            if axis_name in PLANET_NAMES:
                name = PLANET_NAMES[axis_name]
                # API 返回的 sign 索引从 1 开始，需要减 1
                sign_index = axis_data.get("sign", 1) - 1
                sign = ZODIAC_SIGNS.get(sign_index, "未知")
                pos = axis_data.get("position", {})
                if pos:
                    deg = pos.get("degrees", 0)
                    minute = pos.get("minutes", 0)
                    print(f"   {name:8s} → {sign:15s} ({deg}°{minute}')")

    # 主要相位
    if "pairs" in d and len(d["pairs"]) > 0:
        print(f"\n🔗 主要相位 (前10个):")
        for i, pair in enumerate(d["pairs"][:10]):
            phase = pair.get("phase", "")
            degree = pair.get("degree", 0)
            print(f"   {phase:20s} ({degree:.1f}°)")

    # 逆行行星
    if "returninfo" in d and len(d["returninfo"]) > 0:
        print(f"\n⏪ 逆行行星:")
        for info in d["returninfo"]:
            print(f"   • {info}")

    # 完整描述
    if show_desc and "alldesc" in d:
        print(f"\n📝 完整描述:")
        print(f"   {d['alldesc']}")

    print("\n" + "=" * 60)

def gen_analyze_chart_graph_prompt(data: dict) -> str:
    """
    生成星盘图结构的提示词

    Args:
        data: 星盘数据

    Returns:
        提示词文本
    """
    if "data" not in data:
        return "❌ 无效的响应数据"

    d = data["data"]

    # 提取星盘信息
    alldesc = d.get("alldesc", "")
    returninfo = d.get("returninfo", [])

    # 构建提示词
    prompt = f"""这次要根据星盘信息分析推理生产类似编程中的图结构；
        参考案例：【
        案例星盘信息:上升白羊,命主星火星,四宫头在巨蟹,七宫头在天秤,十宫头在摩羯,天秤入陷的太阳在6宫;水瓶的月亮在11宫;太阳在这里空相;月亮刑水星,拱火星,拱天王星,拱海王星,冲冥王星;群星聚集在北半球;群星聚集在天秤,群星聚集在金牛;行星大多分布在土元素;群星聚集在6宫;处女入陷的金星在6宫;金星六合水星;天秤入弱的火星在6宫;火星拱月亮,拱天王星,六合冥王星;处女的海王星在6宫;海王星拱月亮,拱天王星;群星聚集在1宫;金牛的且逆行的木星在1宫;木星冲水星,合土星,合天王星;金牛的且逆行的土星在1宫;土星冲水星,合木星;金牛的且逆行的天王星在1宫;天王星拱月亮,拱火星,合木星,拱海王星;狮子的冥王星在5宫;冥王星冲月亮,刑水星,六合火星;天蝎的水星在7宫;水星刑月亮,六合金星,冲木星,冲土星,刑冥王星;天秤的且逆行的北交在6宫;
        案例星盘对应的图结构：
        [根节点：三大巨头]
            ├─ N1（太阳·六宫·天秤）
            ├─ N2（月亮·十一宫·水瓶） → E1（阻碍）→ N1
            └─ N3（上升·白羊） → E2（共性）→ N1；E3（阻碍）→ N2

        [扩展1：宫位/半球]
            ├─ N4（六宫·星聚） → E4（场景定义）→ N1；E5（拉扯）→ N6
            └─ N5（下半球·侧重） -> E7（构成） -> N4/N6
            └─ N6（一宫·星聚）

        [扩展2：焦点行星群]
            ├─ A1（火星·天秤）→  E8（落宫"行动力加强"）→ N4；  → E9（"破环"）→ N3；E10（强化）→ A3 ；E11（破环）→ N6；E12（拱相位"结盟"）→ N2；
            ├─ A2（海王星·处女合火星） →  E13（合相位"激发"）→ A1；
            ├─ A3（金星·处女） →  E14（落宫"情绪加强"）→ N4；
            ├─ B1（木星·金牛） → E15（落宫"拓展"）→ N3/N6 ;E16（支持）→ N3/N1；E17（矛盾）→ B2;E18（合相位"融合"）→ B2;
            └─ B2（土星·金牛）→ E19（接受）→ B3 ;E20（改变）→ N3/N6 ;
            └─ B3（土星·逆行）
            └─ B4（天王星·一宫·金牛·逆行）→ E21（影响）→ N3/N6 ;  E22（被加强）→ N2 ;

        [扩展3：关键单星/交点]
            ├─ C1（水星·七宫·天蝎） → E23（冲相位'挑战'）→ B1；E24（冲相位'挑战'）→ B2；E25（六合相位'激发'）→ A3；E26（刑相位'困难'）→ N2
            ├─ C2（冥王星·五宫·狮子） → E26（共性[五宫和天秤]）→ N1
            ├─ C3（南交点·十二宫·白羊） → E27（挑战）→ N1
            └─ C4（北交点·六宫·天秤） → E18（成长）→ N1

        根据案例星盘对应的图结构的后续可以得出星盘解析:在占星解读中，我们首先聚焦于太阳、月亮和上升这"三大巨头"，忽略其他细节以简化分析。这有助于掌握整体印象，避免信息过载。以某个星盘为例：太阳落在第六宫天秤座，月亮落在第十一宫水瓶座，上升为白羊座。星座元素显示，这是一个以风象（智性）为主、但带有火象（锐气）的人。

使用基本公式：太阳天秤表明他是艺术家、恋人或和平者；月亮水瓶增添天才、被放逐者或说真话者的灵魂；上升白羊则呈现为战士、先锋或无惧的外在面具。综合来看，他是一个"戴着战士面具、拥有天才灵魂的艺术家"。这意味着，内在追求和谐与美（天秤），但情感驱动（月亮）渴望叛逆与自由（水瓶），外在表现（上升）却直接、激情甚至粗鲁。

内在冲突明显：天秤的和平倾向与水瓶的叛逆、白羊的直接相互拉扯。宫位加深复杂性：太阳在第六宫（奴仆宫）强调通过技巧服务他人，需发展艺术或调停能力以避免陷入低自尊；月亮在第十一宫（朋友宫）指向被局外人、梦想家吸引，推动他走向水瓶座的叛逆未来。

整体上，这人本质温和（天秤）、渴望助人（第六宫），但外在掩饰不确定性，形成自卑挑衅心态。太阳缺乏相位，暗示天秤特质可能被压抑。然而，命运非注定，他可通过整合三大巨头找到共同任务来进化。例如，以艺术为中心（太阳），需建立亲密合作（天秤），并以大胆、挑战的方式呈现（白羊和水瓶），避免廉价冲突。关键是以真实脆弱（太阳）面对世界，而非依赖强硬面具。

做到此事并不容易，但他握有一张王牌：半球侧重带来的弹性。

第二眼看星盘，我们应暂时忽略各行星身份，仅观察其分布。此时行星皆以黑点呈现，我们只关心位置与半球倾向。可见多数行星落于地平线之下，仅水星与月亮在上方。

依规则：太阳计3点，月亮及其他行星各1点。下半球有7个点，加太阳3点，共10点，确为下半球侧重。这揭示他的世界更主观，重心在意识层面而非外在事件。并非说他羞怯或生活平淡，而是他更倾向内省，重视领悟与心境胜过功业成就。

这成为他生命的潜规则。外界评价——无论是赞誉还是批评——对他皆非核心，真正重要的是经历在内心沉淀为记忆、图像与智慧。这赋予他内在的自由，使他能履行世间职责却不被外境所缚。

这位借战士面具表达艺术灵魂的英国人，其命运轮廓渐显。优势、弱点、陷阱、奖赏与盟友，正汇成完整图像，星盘已开始说话。

至此我们通过简化把握了主线，但接下来需进入更深层：将黑点还原为具体行星，直面占星符号的全部复杂性，让星盘自有规则引领我们前行。

要找出星盘中的焦点行星，我们首先扫描整体布局。两个群星聚集区立即引起注意：三颗行星落在金牛座第一宫，另有四颗行星（包括太阳）落在第六宫的处女座和天秤座。这显示出心智能量在两处关键领域高度集中。

除群星外，其余三颗行星也各自突出：月亮本身重要，冥王星与之精确对分，而水星位于第七宫合轴且相位最多。每颗行星都具焦点属性，这反而使我们难以找到明确起点。不过，由此可知此人个性鲜明，能在人群中凝聚并引导能量。

两大群星将他的主要关注点引向两个宫位：第一宫（自我与个性）和第六宫（工作与服务）。二者形成一种动态平衡，带出自由与责任、独立与合作等核心议题。

从第六宫开始分析是合理选择，尤其火星作为上升白羊的守护星也落在此宫。火星在天秤座（落陷位置）意味着，他将为建立和谐关系而战——无论是在人际还是艺术领域。若不能真诚表达，便容易陷入表面冲突。

火星与月亮形成拱相位，说明其行动力与水瓶座月亮追求的自由与清晰可相互支持；但若表达不当，也可能转化为疏离讥讽的言语。后续将看到水星在天蝎座可能强化这一倾向。

在这样的星盘中，每个选择都带来相应后果，而进化占星学的视角将这些可能性呈现为个体可自觉面对的道路。

继续分析第六宫，海王星位于处女座尾度，与天秤座火星合相。海王星象征超越与混沌，落入追求清晰的处女座形成落陷，带来直觉式的工作方式与理想化的完美主义。它与火星合相，意味着理想与现实的冲突常在工作关系中触发火星的张力。

第六宫最后一颗行星是处女座金星，它对关系抱有极高标准，易陷入苛责与自我批评。金星落于工作宫，再次印证其重要人际关系多与职业环境交织——婚姻幸福很可能与事业合作紧密相连。

转向第一宫金牛座群星，木星与土星紧密合相，形成核心矛盾。木星倾向乐观扩张，土星强调现实约束，二者逆行且势均力敌，赋予他时而开朗、时而严肃的复杂气质。解决之道在于将木星的愿景与土星的纪律结合，尤其在第六宫指向的创造性工作中实现"玩耍与工作的统一"。

天王星虽与木土未成合相，但落第一宫且是月亮水瓶的守护星，强化了他外在的独立、不羁的特质，使"流浪者"形象成为人格面具的一部分。

至此，星盘两大群星区域的主题已清晰：第六宫的工作与关系整合，第一宫的自我表达与内在矛盾。仅余水星与冥王星待解析，月亮交点的作用尚待展开。

水星是我们接下来要分析的重点行星。尽管因星盘结构特殊而未在早期讨论，但它实则力量强大，不可低估。

其重要性首先来自它落在第七宫，属于合轴行星，加之其相位数量（六个）为全盘最多，远超仅有四个相位的火星。这意味着水星处于信息交流的核心，是理解此人心理模式的关键一环。

即使暂不深入细节，仅从水星显著的位置就可推断：命主必然善于表达，热衷沟通。风象的日月的确赋予他理性思维，而强劲的水星则为这些思想提供了出口——语言。他很可能是擅长叙事的人，甚至以写作为业。

进一步看，水星的本质是传递信息，而它的"方式"与"动机"由天蝎座赋予，"场景"则在第七宫（关系与伴侣领域）。天蝎座赋予他穿透表象、直指本质的洞察力，但也容易因执着于局部真实而忽略整体善意。配合上升白羊、第一宫的天王星与土星，他能在言语交锋中迅速击中对方弱点，言辞锋利甚至伤人。

若选择正向发展，第七宫的水星会促使他在亲密关系中追求绝对诚实，建立充满深度对话的联结；他也会自然被聪明、善于表达的伴侣吸引。但若逃避成长，天蝎座水星的尖锐会转化为先发制人的攻击，使关系退化为言语竞赛，而天秤座太阳对关系的需求落空后将导致内心空洞。

此外，水星还受到以下关键相位影响：
•
与第一宫木土合相形成对冲，令他在"言无不尽"（木星）与"沉默克制"（土星）间反复；
•
与处女座金星六合，推动他与伴侣在思维和情感上不断深入融合；
•
与水瓶座月亮相刑，造成他在群体中的友善形象和私密关系中的激烈直言形成内在冲突，两者相互制衡却也彼此修正。
冥王星作为最后分析的行星，与月亮相冲、与水星相刑，象征超越自我、影响历史的能力。落于狮子座第五宫，显示他需通过天秤座艺术在世上留下印记——美不仅要整合内心，更要推动社会改变。危险在于，艺术可能沦为教条，结合水瓶座月亮与白羊座上升，他易成为自以为义的布道者，掩盖内心柔软。

其南交点落白羊座第十二宫，暗示过往业力或基因中带有"战败勇士"的模式：曾面对不可能任务，学会独立与超越，却对亲密陌生。这使天秤座的太阳缺乏根基，他必须从头学习关系与合作。

北交点与太阳同落天秤座第六宫，呼应其灵魂方向：需在日常工作和有意识的服务中，建立平等、有爱的合作关系。若失败，他将退回孤立好斗的面具后，灵魂亦随之枯萎。】;


        学习案例快速分析出对应星盘分析的图结构
        (根据图结构分析可以从某个节点出发，经过一系列节点可以方便的返回到之前讨论过的节点，起强调，补充, 冲突等作用，节点的内容可以是(星体|星座|宫位|相位|逆行)中一个或多个的组合，边的内容可以是1 相位的和谐与挑战 2 星座的特质，共性与对立 3 星体的特质,共性与对立 4 星座和星体的对应(比如一宫和白羊的性质类似)等等)
       
## 星盘信息
{alldesc}

### 逆行行星
{chr(10).join(f"• {info}" for info in returninfo) if returninfo else "无"}

请开始生成图结构："""

    return prompt


def analyze_chart_prompt(data: dict) -> str:
    """
    生成星盘深度分析的提示词

    Args:
        data: 星盘数据
        model: 使用的模型（保留参数以兼容接口）

    Returns:
        分析提示词文本
    """
    if "data" not in data:
        return "❌ 无效的响应数据"

    d = data["data"]

    # 提取星盘信息
    alldesc = d.get("alldesc", "")
    returninfo = d.get("returninfo", [])

    # 构建提示词
    prompt = f"""这次要根据星盘信息分析推理生产类似编程中的图结构,然后根据图结构作为分析框架，组织语言，进行文字优雅，哲思充满洞见的本命盘分析；
        参考案例：【
        案例星盘信息:上升白羊,命主星火星,四宫头在巨蟹,七宫头在天秤,十宫头在摩羯,天秤入陷的太阳在6宫;水瓶的月亮在11宫;太阳在这里空相;月亮刑水星,拱火星,拱天王星,拱海王星,冲冥王星;群星聚集在北半球;群星聚集在天秤,群星聚集在金牛;行星大多分布在土元素;群星聚集在6宫;处女入陷的金星在6宫;金星六合水星;天秤入弱的火星在6宫;火星拱月亮,拱天王星,六合冥王星;处女的海王星在6宫;海王星拱月亮,拱天王星;群星聚集在1宫;金牛的且逆行的木星在1宫;木星冲水星,合土星,合天王星;金牛的且逆行的土星在1宫;土星冲水星,合木星;金牛的且逆行的天王星在1宫;天王星拱月亮,拱火星,合木星,拱海王星;狮子的冥王星在5宫;冥王星冲月亮,刑水星,六合火星;天蝎的水星在7宫;水星刑月亮,六合金星,冲木星,冲土星,刑冥王星;天秤的且逆行的北交在6宫;
        案例星盘对应的图结构：
        [根节点：三大巨头]
            ├─ N1（太阳·六宫·天秤）
            ├─ N2（月亮·十一宫·水瓶） → E1（阻碍）→ N1
            └─ N3（上升·白羊） → E2（共性）→ N1；E3（阻碍）→ N2

        [扩展1：宫位/半球]
            ├─ N4（六宫·星聚） → E4（场景定义）→ N1；E5（拉扯）→ N6
            └─ N5（下半球·侧重） -> E7（构成） -> N4/N6
            └─ N6（一宫·星聚）

        [扩展2：焦点行星群]
            ├─ A1（火星·天秤）→  E8（落宫"行动力加强"）→ N4；  → E9（"破环"）→ N3；E10（强化）→ A3 ；E11（破环）→ N6；E12（拱相位"结盟"）→ N2；
            ├─ A2（海王星·处女合火星） →  E13（合相位"激发"）→ A1；
            ├─ A3（金星·处女） →  E14（落宫"情绪加强"）→ N4；
            ├─ B1（木星·金牛） → E15（落宫"拓展"）→ N3/N6 ;E16（支持）→ N3/N1；E17（矛盾）→ B2;E18（合相位"融合"）→ B2;
            └─ B2（土星·金牛）→ E19（接受）→ B3 ;E20（改变）→ N3/N6 ;
            └─ B3（土星·逆行）
            └─ B4（天王星·一宫·金牛·逆行）→ E21（影响）→ N3/N6 ;  E22（被加强）→ N2 ;

        [扩展3：关键单星/交点]
            ├─ C1（水星·七宫·天蝎） → E23（冲相位'挑战'）→ B1；E24（冲相位'挑战'）→ B2；E25（六合相位'激发'）→ A3；E26（刑相位'困难'）→ N2
            ├─ C2（冥王星·五宫·狮子） → E26（共性[五宫和天秤]）→ N1
            ├─ C3（南交点·十二宫·白羊） → E27（挑战）→ N1
            └─ C4（北交点·六宫·天秤） → E18（成长）→ N1

        根据案例星盘对应的图结构的最后星盘解析:在占星解读中，我们首先聚焦于太阳、月亮和上升这"三大巨头"，忽略其他细节以简化分析。这有助于掌握整体印象，避免信息过载。以某个星盘为例：太阳落在第六宫天秤座，月亮落在第十一宫水瓶座，上升为白羊座。星座元素显示，这是一个以风象（智性）为主、但带有火象（锐气）的人。

使用基本公式：太阳天秤表明他是艺术家、恋人或和平者；月亮水瓶增添天才、被放逐者或说真话者的灵魂；上升白羊则呈现为战士、先锋或无惧的外在面具。综合来看，他是一个"戴着战士面具、拥有天才灵魂的艺术家"。这意味着，内在追求和谐与美（天秤），但情感驱动（月亮）渴望叛逆与自由（水瓶），外在表现（上升）却直接、激情甚至粗鲁。

内在冲突明显：天秤的和平倾向与水瓶的叛逆、白羊的直接相互拉扯。宫位加深复杂性：太阳在第六宫（奴仆宫）强调通过技巧服务他人，需发展艺术或调停能力以避免陷入低自尊；月亮在第十一宫（朋友宫）指向被局外人、梦想家吸引，推动他走向水瓶座的叛逆未来。

整体上，这人本质温和（天秤）、渴望助人（第六宫），但外在掩饰不确定性，形成自卑挑衅心态。太阳缺乏相位，暗示天秤特质可能被压抑。然而，命运非注定，他可通过整合三大巨头找到共同任务来进化。例如，以艺术为中心（太阳），需建立亲密合作（天秤），并以大胆、挑战的方式呈现（白羊和水瓶），避免廉价冲突。关键是以真实脆弱（太阳）面对世界，而非依赖强硬面具。

做到此事并不容易，但他握有一张王牌：半球侧重带来的弹性。

第二眼看星盘，我们应暂时忽略各行星身份，仅观察其分布。此时行星皆以黑点呈现，我们只关心位置与半球倾向。可见多数行星落于地平线之下，仅水星与月亮在上方。

依规则：太阳计3点，月亮及其他行星各1点。下半球有7个点，加太阳3点，共10点，确为下半球侧重。这揭示他的世界更主观，重心在意识层面而非外在事件。并非说他羞怯或生活平淡，而是他更倾向内省，重视领悟与心境胜过功业成就。

这成为他生命的潜规则。外界评价——无论是赞誉还是批评——对他皆非核心，真正重要的是经历在内心沉淀为记忆、图像与智慧。这赋予他内在的自由，使他能履行世间职责却不被外境所缚。

这位借战士面具表达艺术灵魂的英国人，其命运轮廓渐显。优势、弱点、陷阱、奖赏与盟友，正汇成完整图像，星盘已开始说话。

至此我们通过简化把握了主线，但接下来需进入更深层：将黑点还原为具体行星，直面占星符号的全部复杂性，让星盘自有规则引领我们前行。

要找出星盘中的焦点行星，我们首先扫描整体布局。两个群星聚集区立即引起注意：三颗行星落在金牛座第一宫，另有四颗行星（包括太阳）落在第六宫的处女座和天秤座。这显示出心智能量在两处关键领域高度集中。

除群星外，其余三颗行星也各自突出：月亮本身重要，冥王星与之精确对分，而水星位于第七宫合轴且相位最多。每颗行星都具焦点属性，这反而使我们难以找到明确起点。不过，由此可知此人个性鲜明，能在人群中凝聚并引导能量。

两大群星将他的主要关注点引向两个宫位：第一宫（自我与个性）和第六宫（工作与服务）。二者形成一种动态平衡，带出自由与责任、独立与合作等核心议题。

从第六宫开始分析是合理选择，尤其火星作为上升白羊的守护星也落在此宫。火星在天秤座（落陷位置）意味着，他将为建立和谐关系而战——无论是在人际还是艺术领域。若不能真诚表达，便容易陷入表面冲突。

火星与月亮形成拱相位，说明其行动力与水瓶座月亮追求的自由与清晰可相互支持；但若表达不当，也可能转化为疏离讥讽的言语。后续将看到水星在天蝎座可能强化这一倾向。

在这样的星盘中，每个选择都带来相应后果，而进化占星学的视角将这些可能性呈现为个体可自觉面对的道路。

继续分析第六宫，海王星位于处女座尾度，与天秤座火星合相。海王星象征超越与混沌，落入追求清晰的处女座形成落陷，带来直觉式的工作方式与理想化的完美主义。它与火星合相，意味着理想与现实的冲突常在工作关系中触发火星的张力。

第六宫最后一颗行星是处女座金星，它对关系抱有极高标准，易陷入苛责与自我批评。金星落于工作宫，再次印证其重要人际关系多与职业环境交织——婚姻幸福很可能与事业合作紧密相连。

转向第一宫金牛座群星，木星与土星紧密合相，形成核心矛盾。木星倾向乐观扩张，土星强调现实约束，二者逆行且势均力敌，赋予他时而开朗、时而严肃的复杂气质。解决之道在于将木星的愿景与土星的纪律结合，尤其在第六宫指向的创造性工作中实现"玩耍与工作的统一"。

天王星虽与木土未成合相，但落第一宫且是月亮水瓶的守护星，强化了他外在的独立、不羁的特质，使"流浪者"形象成为人格面具的一部分。

至此，星盘两大群星区域的主题已清晰：第六宫的工作与关系整合，第一宫的自我表达与内在矛盾。仅余水星与冥王星待解析，月亮交点的作用尚待展开。

水星是我们接下来要分析的重点行星。尽管因星盘结构特殊而未在早期讨论，但它实则力量强大，不可低估。

其重要性首先来自它落在第七宫，属于合轴行星，加之其相位数量（六个）为全盘最多，远超仅有四个相位的火星。这意味着水星处于信息交流的核心，是理解此人心理模式的关键一环。

即使暂不深入细节，仅从水星显著的位置就可推断：命主必然善于表达，热衷沟通。风象的日月的确赋予他理性思维，而强劲的水星则为这些思想提供了出口——语言。他很可能是擅长叙事的人，甚至以写作为业。

进一步看，水星的本质是传递信息，而它的"方式"与"动机"由天蝎座赋予，"场景"则在第七宫（关系与伴侣领域）。天蝎座赋予他穿透表象、直指本质的洞察力，但也容易因执着于局部真实而忽略整体善意。配合上升白羊、第一宫的天王星与土星，他能在言语交锋中迅速击中对方弱点，言辞锋利甚至伤人。

若选择正向发展，第七宫的水星会促使他在亲密关系中追求绝对诚实，建立充满深度对话的联结；他也会自然被聪明、善于表达的伴侣吸引。但若逃避成长，天蝎座水星的尖锐会转化为先发制人的攻击，使关系退化为言语竞赛，而天秤座太阳对关系的需求落空后将导致内心空洞。

此外，水星还受到以下关键相位影响：
•
与第一宫木土合相形成对冲，令他在"言无不尽"（木星）与"沉默克制"（土星）间反复；
•
与处女座金星六合，推动他与伴侣在思维和情感上不断深入融合；
•
与水瓶座月亮相刑，造成他在群体中的友善形象和私密关系中的激烈直言形成内在冲突，两者相互制衡却也彼此修正。
冥王星作为最后分析的行星，与月亮相冲、与水星相刑，象征超越自我、影响历史的能力。落于狮子座第五宫，显示他需通过天秤座艺术在世上留下印记——美不仅要整合内心，更要推动社会改变。危险在于，艺术可能沦为教条，结合水瓶座月亮与白羊座上升，他易成为自以为义的布道者，掩盖内心柔软。

其南交点落白羊座第十二宫，暗示过往业力或基因中带有"战败勇士"的模式：曾面对不可能任务，学会独立与超越，却对亲密陌生。这使天秤座的太阳缺乏根基，他必须从头学习关系与合作。

北交点与太阳同落天秤座第六宫，呼应其灵魂方向：需在日常工作和有意识的服务中，建立平等、有爱的合作关系。若失败，他将退回孤立好斗的面具后，灵魂亦随之枯萎。】;


        1学习案例快速分析出对应星盘分析的图结构
        (根据图结构分析可以从某个节点出发，经过一系列节点可以方便的返回到之前讨论过的节点，起强调，补充, 冲突等作用，节点的内容可以是(星体|星座|宫位|相位|逆行)中一个或多个的组合，边的内容可以是1 相位的和谐与挑战 2 星座的特质，共性与对立 3 星体的特质,共性与对立 4 星座和星体的对应(比如一宫和白羊的性质类似)等等)
        2.按照图结构遍历分析，详细分析，得到分析结果1
        3.文本调整:转化分析结果1中的诸如N1、E1、A1等图结构节点和边的代号为对应的节点或边的流畅的占星语言，隐藏任何关于'根据图结构'、'如节点所示'的说明性文字得到分析结果2。
        4.检查转化后的分析结果2是否按照图结构的节点遍历进行的分析，并调整成​最终交付文本

## 星盘信息

### 完整描述
{alldesc}

### 逆行行星
{chr(10).join(f"• {info}" for info in returninfo) if returninfo else "无"}

## 要求

1. **图结构清晰**：先展示构建的图结构，使用树状图格式
2. **分析深度**：从三大巨头开始，逐步扩展到宫位、行星群、关键单星
3. **语言优雅**：使用富有哲思和洞见的占星语言
4. **逻辑连贯**：按照图结构遍历，确保分析逻辑清晰
5. **避免技术术语**：不要在最终分析中提及"节点"、"边"、"图结构"等技术术语

请开始分析："""

    return prompt


# ============================================================
# 行运/比较盘分析 - starPointComparison & transit_desc
# 移植自 JS

# ============================================================
# 行运/比较盘分析 - starPointComparison & transit_desc
# 移植自 JS
# ============================================================

import math
from datetime import datetime

# 度转弧度
_ONE_DEGREE = math.pi / 180

# 星座名 -> 索引映射 (0-11)
HOUSE_TO_I = {
    'aries': 0, 'taurus': 1, 'gemini': 2, 'cancer': 3,
    'leo': 4, 'virgo': 5, 'libra': 6, 'scorpio': 7,
    'sagittarius': 8, 'capricorn': 9, 'aquarius': 10, 'pisces': 11
}

# 星座中文名
SIGN_NAMES = {
    'aries': '白羊', 'taurus': '金牛', 'gemini': '双子', 'cancer': '巨蟹',
    'leo': '狮子', 'virgo': '处女', 'libra': '天秤', 'scorpio': '天蝎',
    'sagittarius': '射手', 'capricorn': '摩羯', 'aquarius': '水瓶', 'pisces': '双鱼'
}

# 行星英文名 -> 中文名
STAR_NAME_MAP = {
    'sun': '太阳', 'moon': '月亮', 'mercury': '水星', 'venus': '金星',
    'mars': '火星', 'saturn': '土星', 'jupiter': '木星', 'uranus': '天王星',
    'neptune': '海王星', 'pluto': '冥王星', 'north_node': '北交点',
    'asc': '上升', 'mc': '中天'
}

# 行星类型 (用于判断是否为主要行星)
TRANSIT_TYPE = {
    '太阳': True, '月亮': True, '水星': True, '金星': True, '火星': True,
    '木星': True, '土星': True, '天王星': True, '海王星': True, '冥王星': True,
    '北交点': False, '上升': False, '中天': False
}

# 行星权重 (用于排序)
STAR_ORDER = {
    '太阳': 10, '月亮': 9, '水星': 7, '金星': 8, '火星': 6,
    '木星': 5, '土星': 4, '天王星': 3, '海王星': 2, '冥王星': 1,
    '北交点': 0, '上升': 0, '中天': 0
}

# 相位定义: (名称, 角度, 容许度)
# 行运分析使用更严格的容许度
ASPECTS = [
    ('合', 0, 3),
    ('六合', 60, 3),
    ('刑', 90, 4),
    ('拱', 120, 4),
    ('冲', 180, 3),
]

# 相位弧度映射
COMPARISON_ARC = {
    "合": 0, "六合": 60, "刑": 90, "拱": 120, "冲": 180,
}

# 相位容许度
ASPECT_ORBS = {
    "合": 10, "六合": 6, "刑": 8, "拱": 8, "冲": 10,
}

# 行星列表
STAR_ARRAY = ['sun', 'moon', 'mercury', 'venus', 'mars', 'saturn', 'jupiter', 'uranus', 'neptune', 'pluto', 'north_node']



def _get_axes_and_mc(axes, item):
    """获取四轴(上升/中天)的弧度值"""
    pos = axes[item]['position']
    deg = pos['degrees'] + pos['minutes'] / 60 + pos['seconds'] / 3600
    return deg * _ONE_DEGREE


def _get_longitude_diff(lon1, lon2):
    """计算两个经度之间的最小角度差 (度数)"""
    diff = abs(lon1 - lon2) % 360
    if diff > 180:
        diff = 360 - diff
    return diff


def _get_star_longitude(star):
    """获取行星的黄道经度 (0°~360°)"""
    if not star or 'position' not in star:
        return 0
    pos = star['position']
    sign_offset = (star.get('sign', 1) - 1) * 30  # sign为整数1-12
    return sign_offset + pos['degrees'] + pos['minutes'] / 60 + pos['seconds'] / 3600


def _handle_drawned(drawned, sign_key, drawned_b, chart_type, param):
    """
    处理相位计算 - 比较两个盘的行星之间的相位
    每对行星只保留最精确的一个相位（容许度最小）

    Args:
        drawned: 第一个盘的行星按星座分组
        sign_key: 当前星座键
        drawned_b: 第二个盘的行星按星座分组
        chart_type: 盘类型
        param: 参数

    Returns:
        相位结果数组
    """
    # 用字典去重: key=(starA, starB), value=最佳相位
    best_aspects = {}

    # 收集盘A的所有行星
    all_stars_a = []
    for key in drawned:
        for s in drawned[key]:
            all_stars_a.append(s)

    # 收集盘B的所有行星
    all_stars_b = []
    for key in drawned_b:
        for s in drawned_b[key]:
            all_stars_b.append(s)

    # 比较盘A的行星与盘B的行星之间的相位
    for star_a in all_stars_a:
        for star_b in all_stars_b:
            # 跳过同盘比较 (isout=0 vs isout=0 或 isout=1 vs isout=1)
            if star_a['isout'] == star_b['isout']:
                continue

            lon_a = _get_star_longitude(star_a['obj'])
            lon_b = _get_star_longitude(star_b['obj'])
            diff = _get_longitude_diff(lon_a, lon_b)

            # 检查每个相位
            for aspect_name, aspect_angle, aspect_orb in ASPECTS:
                deviation = abs(diff - aspect_angle)
                if deviation <= aspect_orb:
                    name_a = STAR_NAME_MAP.get(star_a['item'], star_a['item'])
                    name_b = STAR_NAME_MAP.get(star_b['item'], star_b['item'])

                    # 统一 key: 行运星在前, 本命星在后
                    if star_a['isout'] == 1:
                        key = (name_a, name_b)
                    else:
                        key = (name_b, name_a)

                    # 保留偏差最小的相位
                    if key not in best_aspects or deviation < best_aspects[key]['deviation']:
                        best_aspects[key] = {
                            'phase': f"{key[0]}{aspect_name}{key[1]}",
                            'starA': key[0],
                            'starB': key[1],
                            'content': f"{key[0]}{aspect_name}{key[1]} ({diff:.1f})",
                            'degree': diff,
                            'aspectName': aspect_name,
                            'aspectAngle': aspect_angle,
                            'deviation': deviation,
                        }

    return list(best_aspects.values())


def _star_in_house(data_a, data_b):
    """
    计算行星落宫 - 确定盘B的行星落在盘A的哪个宫

    Args:
        data_a: 盘A的数据 (chart['data'])
        data_b: 盘B的数据 (chartB['data'])

    Returns:
        行星落宫结果列表
    """
    result = []
    houses = data_a.get('houses', [])
    astros = data_b.get('astros', {})
    axes = data_b.get('axes', {})

    # 构建宫位边界数组 (按经度排序)
    house_boundaries = []
    for i in range(12):
        if houses[i] and houses[i].get('position'):
            house_boundaries.append({
                'houseNum': i + 1,
                'longitude': houses[i]['position']['longitude']
            })
    house_boundaries.sort(key=lambda x: x['longitude'])

    def find_house(planet_lon):
        for i in range(len(house_boundaries)):
            current = house_boundaries[i]['longitude']
            next_lon = house_boundaries[(i + 1) % len(house_boundaries)]['longitude']

            if i == len(house_boundaries) - 1:
                if planet_lon >= current or planet_lon < next_lon:
                    return house_boundaries[i]['houseNum']
            else:
                if planet_lon >= current and planet_lon < next_lon:
                    return house_boundaries[i]['houseNum']
        return 1

    # 处理行星
    for item in STAR_ARRAY:
        star = astros.get(item)
        if star and star.get('position'):
            lon = _get_star_longitude(star)
            house_num = find_house(lon)
            name = STAR_NAME_MAP.get(item, item)
            sign_name = SIGN_NAMES.get(star.get('sign', ''), star.get('sign', ''))

            result.append({
                'desc': f"{name}落{house_num}宫",
                'type': 'planet',
                'order': STAR_ORDER.get(name, 0),
                'star': name,
                'house': house_num,
                'sign': sign_name,
                'longitude': lon
            })

    # 处理四轴
    for item in ['asc', 'mc']:
        axis = axes.get(item)
        if axis and axis.get('position'):
            lon = _get_star_longitude(axis)
            house_num = find_house(lon)
            name = STAR_NAME_MAP.get(item, item)
            sign_name = SIGN_NAMES.get(axis.get('sign', ''), axis.get('sign', ''))

            result.append({
                'desc': f"{name}落{house_num}宫",
                'type': 'axis',
                'order': STAR_ORDER.get(name, 0),
                'star': name,
                'house': house_num,
                'sign': sign_name,
                'longitude': lon
            })

    return result


def _gen_star_props(pairs, returninfo, info2):
    """
    生成行星属性 (从 pairs, returninfo, info2)

    Args:
        pairs: 相位数组
        returninfo: 逆行信息列表
        info2: 星座宫位信息 (逗号分隔字符串)

    Returns:
        行星属性字典
    """
    props = {}

    # 从 info2 解析行星信息
    if isinstance(info2, str):
        info2_list = info2.split(',')
    elif isinstance(info2, list):
        info2_list = info2
    else:
        info2_list = []

    for info in info2_list:
        import re
        match = re.match(r'(.+?)在(\d+)宫', info.strip())
        if match:
            star_name = match.group(1)
            house = match.group(2)
            props[star_name] = props.get(star_name, {})
            props[star_name]['house'] = f"{house}宫"

    # 从 pairs 解析相位信息
    if isinstance(pairs, list):
        for pair in pairs:
            phase = pair.get('phase', '')
            for aspect_name, aspect_angle, aspect_orb in ASPECTS:
                idx = phase.find(aspect_name)
                if idx > 0:
                    star_a = phase[:idx]
                    star_b = phase[idx + len(aspect_name):]
                    if star_a and star_b:
                        props[star_a] = props.get(star_a, {})
                        props[star_b] = props.get(star_b, {})
                        if 'aspects' not in props[star_a]:
                            props[star_a]['aspects'] = []
                        if 'aspects' not in props[star_b]:
                            props[star_b]['aspects'] = []
                        props[star_a]['aspects'].append({'aspect': aspect_name, 'with': star_b, 'degree': pair.get('degree', 0)})
                        props[star_b]['aspects'].append({'aspect': aspect_name, 'with': star_a, 'degree': pair.get('degree', 0)})

    # 标记逆行行星
    if isinstance(returninfo, list):
        for info in returninfo:
            import re
            match = re.match(r'(.+?)逆行', info)
            if match:
                star_name = match.group(1)
                props[star_name] = props.get(star_name, {})
                props[star_name]['retrograde'] = True

    return props



def star_point_comparison(chart, chart_b, chart_type=4):
    """
    比较两个星盘的相位和落宫

    Args:
        chart: 第一个盘 (本命盘) - get_horoscope() 返回的完整 dict
        chart_b: 第二个盘 (行运盘/比较盘) - get_horoscope() 返回的完整 dict
        chart_type: 盘类型 (3=比较盘, 4=行运盘)

    Returns:
        {"desc": str}
    """
    axes = chart['data']['axes']
    axes_b = chart_b['data']['axes']

    # 过滤逆行信息 (只保留水星、火星、金星)
    returninfo_list = chart_b['data'].get('returninfo', [])
    filtered_returninfo = [item for item in returninfo_list
                           if any(x in item for x in ['水星', '火星', '金星'])]
    returninfo_str = ','.join(list(set(filtered_returninfo)))

    # 上升点计算
    asc = 0

    axes_point = ["asc", "mc"]
    drawned = {i: [] for i in range(1, 13)}
    drawned_b = {i: [] for i in range(1, 13)}

    # 处理第一个盘的上升、MC点
    for item in axes_point:
        asc_deg = _get_axes_and_mc(axes, item)

        if item == 'asc':
            asc = (12 - axes[item]['sign'] + 1) * 30 * _ONE_DEGREE - asc_deg

        rad = ((2 * math.pi) / 12) * (axes[item]['sign'] - 1) - asc_deg - asc
        drawned[axes[item]['sign']].append({
            'rad': rad,
            'item': item,
            'isout': 0,
            'obj': axes[item]
        })

    # 处理第二个盘的上升、MC点
    for item in axes_point:
        pos = axes_b[item]['position']
        asc_deg = (pos['degrees'] + pos['minutes'] / 60 + pos['seconds'] / 3600) * _ONE_DEGREE

        rad = ((2 * math.pi) / 12) * (axes_b[item]['sign'] - 1) - asc_deg - asc
        drawned_b[axes_b[item]['sign']].append({
            'rad': rad,
            'item': item,
            'isout': 1,
            'obj': axes_b[item]
        })

    # 处理行星
    for item in STAR_ARRAY:
        # 盘A
        star = chart['data']['astros'][item]
        pos = star['position']
        deg = (pos['degrees'] + pos['minutes'] / 60 + pos['seconds'] / 3600)
        deg_rad = (2 * math.pi * deg) / 360
        rad = ((2 * math.pi) / 12) * (star['sign'] - 1) - deg_rad - asc
        drawned[star['sign']].append({
            'rad': rad,
            'item': item,
            'isout': 0,
            'obj': star
        })

        # 盘B
        star = chart_b['data']['astros'][item]
        pos = star['position']
        deg = (pos['degrees'] + pos['minutes'] / 60 + pos['seconds'] / 3600)
        deg_rad = (2 * math.pi * deg) / 360
        rad = ((2 * math.pi) / 12) * (star['sign'] - 1) - deg_rad - asc
        drawned_b[star['sign']].append({
            'rad': rad,
            'item': item,
            'isout': 1,
            'obj': star
        })

    # 计算相位 (只调用一次，_handle_drawned 内部已遍历所有行星对)
    update = _handle_drawned(drawned, None, drawned_b, chart_type,
                             2 if chart_type in (4, 7) else -1)

    # 比较盘: 获取行星所落宫位置
    if chart_type == 3:
        star_in_house_list = _star_in_house(chart['data'], chart_b['data'])
        for star in star_in_house_list:
            item_desc = star['desc']
            if item_desc.find("中天") < 0 and item_desc.find("上升") < 0 and item_desc.find("北交点") < 0:
                update.insert(0, {
                    'phase': f"TA{item_desc.replace('落', '落你')}",
                    'content': item_desc,
                    'degree': 0
                })

    # 行运盘: 生成 stepPrompt
    house = []
    house_obj = []
    step_prompt = ''

    pairs = chart['data'].get('pairs', [])
    return_thing = chart['data'].get('returninfo', [])
    info2 = chart['data'].get('info2', '')
    star_props = _gen_star_props(pairs, return_thing, info2)

    if chart_type == 4:
        star_in_house_list = _star_in_house(chart['data'], chart_b['data'])
        for star in star_in_house_list:
            item_desc = star['desc']
            if item_desc.find("中天") < 0 and item_desc.find("上升") < 0 and item_desc.find("北交点") < 0:
                house.append({
                    'phase': f"行运{item_desc}",
                    'type': star['type'],
                    'order': star['order'],
                    'star': star['star'],
                    'house': star['house'],
                    'content': None,
                    'degree': 10000
                })

        house.sort(key=lambda x: x['order'], reverse=True)

        # 按宫分组
        for h in house:
            index = -1
            for i, o in enumerate(house_obj):
                if o[0] == h['house']:
                    index = i
                    break
            if index >= 0:
                house_obj[index][1].append(h)
                house_obj[index][2] += 1
            else:
                house_obj.append([h['house'], [h], 1])

        return_array = chart_b['data'].get('returninfo', [])

        # 排序: 按权重和数量
        for item in house_obj:
            order_sum = sum(x['order'] for x in item[1])
            item.append(item[2] + order_sum)
        house_obj.sort(key=lambda x: x[3], reverse=True)

        for item in house_obj:
            desc_parts = []
            for inner_iter in item[1]:
                is_retro = any(inner_iter['star'] in r for r in return_array)
                desc_parts.append(f"行运{inner_iter['star']}{'逆行' if is_retro else ''}")
            step_prompt += f"{','.join(desc_parts)}落{item[0]}宫;"

            for inner_iter in item[1]:
                p_array = [p for p in update
                           if p['starA'] == inner_iter['star']
                           and p['starB'] != inner_iter['star']  # 排除自合
                           and (TRANSIT_TYPE.get(p['starA'], False) or TRANSIT_TYPE.get(p['starB'], False))
                           and p['starB'] not in ("上升", "中天", "北交点")]
                for p in p_array:
                    star_b_props = star_props.get(p['starB'])
                    desc = f"{star_b_props.get('house', '') if star_b_props else ''}{p['starB']}"
                    step_prompt += f"{p['phase'].replace(p['starB'], desc)};"

    # 排序相位
    update.sort(key=lambda x: x['degree'])
    new_update = [item['phase'] for item in update]

    if isinstance(new_update, list):
        return {
            'desc': f"行运信息:{step_prompt}" if chart_type == 4 else ','.join(new_update)
        }
    return None


def transit_desc(time, address=None, latitude=None, longitude=None, source_tz_offset=8, transit_time=None):
    """
    获取行运描述

    Args:
        time: 出生时间 (YYYY-MM-DD HH:MM:SS)
        address: 出生地址
        latitude: 纬度
        longitude: 经度
        source_tz_offset: 源时区偏移 (小时)
        transit_time: 行运时间 (YYYY-MM-DD HH:MM:SS)，默认为当前时间

    Returns:
        行运描述字符串
    """
    import io
    from contextlib import redirect_stdout

    # 抑制 get_horoscope 的 print 输出
    with io.StringIO() as buf, redirect_stdout(buf):
        # 1. 获取本命盘
        chart1 = get_horoscope(
            time_str=time,
            address=address,
            latitude=latitude,
            longitude=longitude,
            source_tz_offset=source_tz_offset,
            target_tz="GMT",
            show_desc=True
        )

        # 2. 获取行运盘 (使用指定时间或当前时间)
        if transit_time:
            current_time = transit_time
        else:
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        chart2 = get_horoscope(
            time_str=current_time,
            address=address,
            latitude=latitude,
            longitude=longitude,
            source_tz_offset=8,
            target_tz="GMT",
            show_desc=True
        )

    # 3. 比较两个盘
    result = star_point_comparison(chart1, chart2, 4)

    return result['desc'] if result else None



def main():
    parser = argparse.ArgumentParser(
        description="星盘数据获取工具 - 从 deepastro.cn API 获取本命盘数据"
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # get_chart 命令
    chart_parser = subparsers.add_parser("get_chart", help="获取星盘数据")
    chart_parser.add_argument("--time", required=True, help="出生时间 (YYYY-MM-DD HH:MM:SS)")
    chart_parser.add_argument("--address", help="出生地点")
    chart_parser.add_argument("--latitude", type=float, help="纬度")
    chart_parser.add_argument("--longitude", type=float, help="经度")
    chart_parser.add_argument("--source-tz-offset", type=int, default=8,
                             help="源时区偏移（小时），默认 8 (CST, UTC+8)。例如：中国=8, 南非=2, 英国=0, 美国东部=-5")
    chart_parser.add_argument("--target-tz", default="GMT", help="目标时区 (默认: GMT)")
    chart_parser.add_argument("--show-desc", action="store_true", dest="show_desc", help="显示详细描述 (默认: true)")
    chart_parser.add_argument("--no-show-desc", action="store_false", dest="show_desc", help="不显示详细描述")
    chart_parser.set_defaults(show_desc=True)
    chart_parser.add_argument("--json", action="store_true", help="输出 JSON 格式")

    # analyze_chart 命令
    analyze_parser = subparsers.add_parser("analyze_chart", help="深度分析星盘")
    analyze_parser.add_argument("--time", required=True, help="出生时间 (YYYY-MM-DD HH:MM:SS)")
    analyze_parser.add_argument("--address", help="出生地点")
    analyze_parser.add_argument("--latitude", type=float, help="纬度")
    analyze_parser.add_argument("--longitude", type=float, help="经度")
    analyze_parser.add_argument("--timezone", default="GMT", help="时区 (默认: GMT)")

    # gen_analyze_chart_graph_prompt 命令
    analyze_parser = subparsers.add_parser("gen_analyze_chart_graph_prompt", help="星盘分析用图结构")
    analyze_parser.add_argument("--time", required=True, help="出生时间 (YYYY-MM-DD HH:MM:SS)")
    analyze_parser.add_argument("--address", help="出生地点")
    analyze_parser.add_argument("--latitude", type=float, help="纬度")
    analyze_parser.add_argument("--longitude", type=float, help="经度")
    analyze_parser.add_argument("--source-tz-offset", type=int, default=8,
                             help="源时区偏移（小时），默认 8 (CST, UTC+8)。例如：中国=8, 南非=2, 英国=0, 美国东部=-5")
    analyze_parser.add_argument("--target-tz", default="GMT", help="目标时区 (默认: GMT)")

    # transit 命令
    transit_parser = subparsers.add_parser("transit", help="获取行运描述")
    transit_parser.add_argument("--time", required=True, help="出生时间 (YYYY-MM-DD HH:MM:SS)")
    transit_parser.add_argument("--address", help="出生地点")
    transit_parser.add_argument("--latitude", type=float, help="纬度")
    transit_parser.add_argument("--longitude", type=float, help="经度")
    transit_parser.add_argument("--source-tz-offset", type=int, default=8,
                             help="源时区偏移（小时），默认 8 (CST, UTC+8)")
    transit_parser.add_argument("--transit-time", help="行运时间 (YYYY-MM-DD HH:MM:SS)，默认为当前时间")

    # compare 命令
    compare_parser = subparsers.add_parser("compare", help="比较盘分析")
    compare_parser.add_argument("--time", required=True, help="第一人出生时间 (YYYY-MM-DD HH:MM:SS)")
    compare_parser.add_argument("--address", help="第一人出生地点")
    compare_parser.add_argument("--latitude", type=float, help="第一人纬度")
    compare_parser.add_argument("--longitude", type=float, help="第一人经度")
    compare_parser.add_argument("--source-tz-offset", type=int, default=8,
                             help="第一人源时区偏移（小时），默认 8")
    compare_parser.add_argument("--compare-time", required=True, help="第二人出生时间 (YYYY-MM-DD HH:MM:SS)")
    compare_parser.add_argument("--compare-address", help="第二人出生地点")
    compare_parser.add_argument("--compare-latitude", type=float, help="第二人纬度")
    compare_parser.add_argument("--compare-longitude", type=float, help="第二人经度")
    compare_parser.add_argument("--compare-tz-offset", type=int, default=8,
                             help="第二人源时区偏移（小时），默认 8")

    args = parser.parse_args()

    if args.command == "get_chart":
        try:
            data = get_horoscope(
                time_str=args.time,
                address=args.address,
                latitude=args.latitude,
                longitude=args.longitude,
                source_tz_offset=args.source_tz_offset,
                target_tz=args.target_tz,
                show_desc=args.show_desc
            )

            if args.json:
                print(json.dumps(data, ensure_ascii=False, indent=2))
            else:
                print_summary(data, show_desc=args.show_desc)

        except Exception as e:
            print(f"❌ 错误: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "analyze_chart":
        try:
            data = get_horoscope(
                time_str=args.time,
                address=args.address,
                latitude=args.latitude,
                longitude=args.longitude,
                source_tz_offset=args.source_tz_offset,
                target_tz=args.target_tz,
                show_desc=True
            )

            analyze_chart_prompt(data)

        except Exception as e:
            print(f"❌ 错误: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.command == "gen_analyze_chart_graph_prompt":
        try:
            data = get_horoscope(
                time_str=args.time,
                address=args.address,
                latitude=args.latitude,
                longitude=args.longitude,
                source_tz_offset=args.source_tz_offset,
                target_tz=args.target_tz,
                show_desc=True
            )

            prompt = gen_analyze_chart_graph_prompt(data)
            print(prompt)

        except Exception as e:
            print(f"❌ 错误: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "transit":
        try:
            desc = transit_desc(
                time=args.time,
                address=args.address,
                latitude=args.latitude,
                longitude=args.longitude,
                source_tz_offset=args.source_tz_offset,
                transit_time=args.transit_time
            )
            if desc:
                print(desc)
            else:
                print("❌ 无法获取行运描述", file=sys.stderr)
                sys.exit(1)

        except Exception as e:
            print(f"❌ 错误: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "compare":
        try:
            result = star_point_comparison(
                chart1=get_horoscope(
                    time_str=args.time,
                    address=args.address,
                    latitude=args.latitude,
                    longitude=args.longitude,
                    source_tz_offset=args.source_tz_offset,
                    target_tz="GMT",
                    show_desc=True
                ),
                chart_b=get_horoscope(
                    time_str=args.compare_time,
                    address=args.compare_address or args.address,
                    latitude=args.compare_latitude or args.latitude,
                    longitude=args.compare_longitude or args.longitude,
                    source_tz_offset=args.compare_tz_offset if args.compare_tz_offset is not None else 8,
                    target_tz="GMT",
                    show_desc=True
                ),
                chart_type=3
            )
            if result and result.get('desc'):
                print(result['desc'])
            else:
                print("❌ 无法获取比较盘描述", file=sys.stderr)
                sys.exit(1)

        except Exception as e:
            print(f"❌ 错误: {e}", file=sys.stderr)
            sys.exit(1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
