#!/usr/bin/env python3
"""
Horoscope Fetcher 测试套件

用法:
    python3 test_horoscope.py              # 运行全部测试
    python3 test_horoscope.py -v           # 详细输出
    python3 test_horoscope.py TestTransitDesc  # 运行单个测试类
    python3 test_horoscope.py TestTransitDesc.test_transit_desc  # 运行单个测试方法
"""

import unittest
import math
import json
import sys
import os
from unittest.mock import patch, MagicMock
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from horoscope_fetcher import (
    format_time,
    _get_longitude_diff,
    _get_star_longitude,
    _handle_drawned,
    _star_in_house,
    _gen_star_props,
    star_point_comparison,
    transit_desc,
    ZODIAC_SIGNS,
    PLANET_NAMES,
    STAR_NAME_MAP,
    SIGN_NAMES,
    STAR_ARRAY,
    ASPECTS,
    TRANSIT_TYPE,
    STAR_ORDER,
    _ONE_DEGREE,
)


# ============================================================
# 工具函数测试
# ============================================================

class TestFormatTime(unittest.TestCase):
    """format_time 时间格式化测试"""

    def test_cst_to_gmt(self):
        """CST (UTC+8) 转 GMT"""
        result = format_time("2026-03-09 21:57:00", source_tz_offset=8, target_tz="GMT")
        self.assertTrue(result.endswith(" GMT"))
        # 21:57 CST - 8h = 13:57 GMT
        self.assertIn("13:57:00", result)

    def test_utc_to_gmt(self):
        """UTC (UTC+0) 转 GMT (不变)"""
        result = format_time("2026-03-09 13:57:00", source_tz_offset=0, target_tz="GMT")
        self.assertIn("13:57:00", result)

    def test_negative_offset(self):
        """负时区 (美国东部 UTC-5)"""
        result = format_time("2026-03-09 08:00:00", source_tz_offset=-5, target_tz="GMT")
        # 08:00 EST + 5h = 13:00 GMT
        self.assertIn("13:00:00", result)

    def test_invalid_format(self):
        """无效时间格式应抛出 ValueError"""
        with self.assertRaises(ValueError):
            format_time("not-a-date")

    def test_day_of_week(self):
        """验证星期几正确"""
        # 2026-03-09 是周一
        result = format_time("2026-03-09 21:57:00", source_tz_offset=8)
        self.assertIn("Mon", result)


class TestLongitudeDiff(unittest.TestCase):
    """_get_longitude_diff 经度差计算测试"""

    def test_same_position(self):
        """相同位置差为0"""
        self.assertAlmostEqual(_get_longitude_diff(100, 100), 0)

    def test_simple_diff(self):
        """简单差值"""
        self.assertAlmostEqual(_get_longitude_diff(10, 50), 40)

    def test_wrap_around(self):
        """跨0度"""
        self.assertAlmostEqual(_get_longitude_diff(350, 10), 20)

    def test_opposition(self):
        """对冲 (180度)"""
        self.assertAlmostEqual(_get_longitude_diff(0, 180), 180)
        self.assertAlmostEqual(_get_longitude_diff(90, 270), 180)

    def test_always_positive(self):
        """结果始终 <= 180"""
        for a in range(0, 360, 30):
            for b in range(0, 360, 30):
                diff = _get_longitude_diff(a, b)
                self.assertGreaterEqual(diff, 0)
                self.assertLessEqual(diff, 180)


class TestGetStarLongitude(unittest.TestCase):
    """_get_star_longitude 行星经度提取测试"""

    def test_normal(self):
        """正常行星数据"""
        star = {'position': {'degrees': 120, 'minutes': 30, 'seconds': 0}}
        self.assertAlmostEqual(_get_star_longitude(star), 120.5)

    def test_with_seconds(self):
        """带秒数"""
        star = {'position': {'degrees': 90, 'minutes': 0, 'seconds': 1800}}  # 30'
        self.assertAlmostEqual(_get_star_longitude(star), 90.5)

    def test_empty_star(self):
        """空数据返回0"""
        self.assertEqual(_get_star_longitude(None), 0)
        self.assertEqual(_get_star_longitude({}), 0)


# ============================================================
# 相位计算测试
# ============================================================

class TestHandleDrawned(unittest.TestCase):
    """_handle_drawned 相位计算测试"""

    def _make_star(self, name, degrees, minutes=0, seconds=0, sign=1, isout=0):
        """创建模拟行星数据"""
        return {
            'rad': 0,
            'item': name,
            'isout': isout,
            'obj': {
                'position': {'degrees': degrees, 'minutes': minutes, 'seconds': seconds},
                'sign': sign
            }
        }

    def test_conjunction(self):
        """合相检测 (0度)"""
        drawned = {1: [self._make_star('sun', 0, 0, 0, 1, 0)]}
        drawned_b = {1: [self._make_star('sun', 2, 0, 0, 1, 1)]}  # 2° < 3° 容许度
        result = _handle_drawned(drawned, None, drawned_b, 4, 2)
        self.assertTrue(len(result) > 0)
        self.assertEqual(result[0]['aspectName'], '合')

    def test_no_aspect_same_isout(self):
        """同盘行星不计算相位"""
        drawned = {1: [self._make_star('sun', 0, 0, 0, 1, 0)]}
        drawned_b = {1: [self._make_star('moon', 5, 0, 0, 1, 0)]}
        result = _handle_drawned(drawned, None, drawned_b, 4, 2)
        self.assertEqual(len(result), 0)

    def test_trine(self):
        """拱相检测 (120度)"""
        drawned = {1: [self._make_star('sun', 0, 0, 0, 1, 0)]}
        drawned_b = {5: [self._make_star('jupiter', 120, 0, 0, 5, 1)]}
        result = _handle_drawned(drawned, None, drawned_b, 4, 2)
        trines = [r for r in result if r['aspectName'] == '拱']
        self.assertTrue(len(trines) > 0)

    def test_opposition(self):
        """冲相检测 (180度)"""
        drawned = {1: [self._make_star('sun', 0, 0, 0, 1, 0)]}
        drawned_b = {7: [self._make_star('moon', 180, 0, 0, 7, 1)]}
        result = _handle_drawned(drawned, None, drawned_b, 4, 2)
        oppositions = [r for r in result if r['aspectName'] == '冲']
        self.assertTrue(len(oppositions) > 0)

    def test_square(self):
        """刑相检测 (90度)"""
        drawned = {1: [self._make_star('sun', 0, 0, 0, 1, 0)]}
        drawned_b = {4: [self._make_star('mars', 90, 0, 0, 4, 1)]}
        result = _handle_drawned(drawned, None, drawned_b, 4, 2)
        squares = [r for r in result if r['aspectName'] == '刑']
        self.assertTrue(len(squares) > 0)

    def test_sextile(self):
        """六合检测 (60度)"""
        drawned = {1: [self._make_star('sun', 0, 0, 0, 1, 0)]}
        drawned_b = {3: [self._make_star('venus', 60, 0, 0, 3, 1)]}
        result = _handle_drawned(drawned, None, drawned_b, 4, 2)
        sextiles = [r for r in result if r['aspectName'] == '六合']
        self.assertTrue(len(sextiles) > 0)

    def test_no_aspect_outside_orb(self):
        """超出容许度不形成相位"""
        drawned = {1: [self._make_star('sun', 0, 0, 0, 1, 0)]}
        drawned_b = {1: [self._make_star('moon', 45, 0, 0, 2, 1)]}  # 45度不在任何相位容许度内
        result = _handle_drawned(drawned, None, drawned_b, 4, 2)
        self.assertEqual(len(result), 0)

    def test_result_structure(self):
        """验证返回结构"""
        drawned = {1: [self._make_star('sun', 0, 0, 0, 1, 0)]}
        drawned_b = {1: [self._make_star('moon', 3, 0, 0, 1, 1)]}
        result = _handle_drawned(drawned, None, drawned_b, 4, 2)
        self.assertTrue(len(result) > 0)
        r = result[0]
        self.assertIn('phase', r)
        self.assertIn('starA', r)
        self.assertIn('starB', r)
        self.assertIn('aspectName', r)
        self.assertIn('degree', r)


# ============================================================
# 落宫计算测试
# ============================================================

class TestStarInHouse(unittest.TestCase):
    """_star_in_house 行星落宫测试"""

    def _make_chart_data(self, house_longitudes):
        """创建模拟星盘数据

        Args:
            house_longitudes: 12个宫位的经度列表
        """
        houses = []
        for i, lon in enumerate(house_longitudes):
            houses.append({
                'position': {'longitude': lon}
            })

        astros = {}
        for item in STAR_ARRAY:
            astros[item] = {
                'position': {'degrees': 0, 'minutes': 0, 'seconds': 0},
                'sign': 1
            }

        axes = {
            'asc': {'position': {'degrees': 0, 'minutes': 0, 'seconds': 0}, 'sign': 1},
            'mc': {'position': {'degrees': 90, 'minutes': 0, 'seconds': 0}, 'sign': 4}
        }

        return {'houses': houses, 'astros': astros, 'axes': axes}

    def test_basic_house_assignment(self):
        """基本落宫分配"""
        # 12个宫位均匀分布
        house_lons = [i * 30 for i in range(12)]
        data_a = self._make_chart_data(house_lons)

        # 行星在45度 → 应落2宫 (30-60)
        data_b = self._make_chart_data(house_lons)
        data_b['astros']['sun']['position'] = {'degrees': 45, 'minutes': 0, 'seconds': 0}

        result = _star_in_house(data_a, data_b)
        sun_result = [r for r in result if r['star'] == '太阳']
        self.assertEqual(len(sun_result), 1)
        self.assertEqual(sun_result[0]['house'], 2)

    def test_all_planets_returned(self):
        """所有行星都有落宫结果"""
        house_lons = [i * 30 for i in range(12)]
        data_a = self._make_chart_data(house_lons)
        data_b = self._make_chart_data(house_lons)

        result = _star_in_house(data_a, data_b)
        # 11 行星 + 2 轴 = 13
        self.assertEqual(len(result), 13)

    def test_result_structure(self):
        """验证返回结构"""
        house_lons = [i * 30 for i in range(12)]
        data_a = self._make_chart_data(house_lons)
        data_b = self._make_chart_data(house_lons)

        result = _star_in_house(data_a, data_b)
        r = result[0]
        self.assertIn('desc', r)
        self.assertIn('type', r)
        self.assertIn('order', r)
        self.assertIn('star', r)
        self.assertIn('house', r)


# ============================================================
# 行星属性测试
# ============================================================

class TestGenStarProps(unittest.TestCase):
    """_gen_star_props 行星属性生成测试"""

    def test_info2_parsing(self):
        """info2 字符串解析"""
        info2 = "太阳在5宫,月亮在1宫"
        props = _gen_star_props([], [], info2)
        self.assertEqual(props['太阳']['house'], '5宫')
        self.assertEqual(props['月亮']['house'], '1宫')

    def test_info2_list(self):
        """info2 列表格式"""
        info2 = ["太阳在5宫", "月亮在1宫"]
        props = _gen_star_props([], [], info2)
        self.assertEqual(props['太阳']['house'], '5宫')

    def test_retrograde_detection(self):
        """逆行检测"""
        returninfo = ["水星逆行", "火星逆行"]
        props = _gen_star_props([], returninfo, "")
        self.assertTrue(props['水星']['retrograde'])
        self.assertTrue(props['火星']['retrograde'])
        self.assertNotIn('金星', props)

    def test_aspect_parsing(self):
        """相位解析"""
        pairs = [
            {'phase': '太阳合月亮', 'degree': 2.5},
            {'phase': '水星刑火星', 'degree': 89.3}
        ]
        props = _gen_star_props(pairs, [], "")
        self.assertEqual(len(props['太阳']['aspects']), 1)
        self.assertEqual(props['太阳']['aspects'][0]['aspect'], '合')
        self.assertEqual(props['太阳']['aspects'][0]['with'], '月亮')

    def test_empty_input(self):
        """空输入"""
        props = _gen_star_props([], [], "")
        self.assertEqual(props, {})


# ============================================================
# star_point_comparison 集成测试 (使用 mock)
# ============================================================

class TestStarPointComparison(unittest.TestCase):
    """star_point_comparison 集成测试"""

    def _make_mock_chart(self, sign_offsets=None):
        """创建模拟星盘数据

        Args:
            sign_offsets: 行星名 -> (sign, degrees, minutes) 的映射
        """
        if sign_offsets is None:
            sign_offsets = {}

        astros = {}
        for item in STAR_ARRAY:
            sign, deg, mins = sign_offsets.get(item, (1, 0, 0))
            astros[item] = {
                'position': {'degrees': deg, 'minutes': mins, 'seconds': 0},
                'sign': sign
            }

        axes = {
            'asc': {'position': {'degrees': 0, 'minutes': 0, 'seconds': 0}, 'sign': 8},
            'mc': {'position': {'degrees': 90, 'minutes': 0, 'seconds': 0}, 'sign': 1}
        }

        houses = []
        for i in range(12):
            houses.append({'position': {'longitude': i * 30}})

        return {
            'data': {
                'astros': astros,
                'axes': axes,
                'houses': houses,
                'pairs': [],
                'returninfo': [],
                'info2': ''
            }
        }

    def test_returns_dict_with_desc(self):
        """返回包含 desc 的字典"""
        chart = self._make_mock_chart()
        chart_b = self._make_mock_chart()
        result = star_point_comparison(chart, chart_b, 4)
        self.assertIsInstance(result, dict)
        self.assertIn('desc', result)
        self.assertIsInstance(result['desc'], str)

    def test_transit_desc_starts_with_keyword(self):
        """行运盘描述以 '行运信息:' 开头"""
        chart = self._make_mock_chart()
        chart_b = self._make_mock_chart()
        result = star_point_comparison(chart, chart_b, 4)
        self.assertTrue(result['desc'].startswith('行运信息:'))

    def test_comparison_chart_type_3(self):
        """比较盘 (chart_type=3) 返回逗号分隔的相位"""
        chart = self._make_mock_chart()
        chart_b = self._make_mock_chart()
        result = star_point_comparison(chart, chart_b, 3)
        # 比较盘不包含 "行运信息:" 前缀
        self.assertFalse(result['desc'].startswith('行运信息:'))

    def test_conjunction_detected(self):
        """合相被正确检测"""
        # 盘A: 太阳在白羊座 0度
        # 盘B: 太阳在白羊座 2度 → 合相 (自合在 step_prompt 中被排除，但 update 中存在)
        # 改用不同行星: 盘A太阳0°, 盘B月亮2° → 合相
        offsets_a = {'sun': (1, 0, 0)}
        offsets_b = {'moon': (1, 2, 0)}
        chart = self._make_mock_chart(offsets_a)
        chart_b = self._make_mock_chart(offsets_b)
        result = star_point_comparison(chart, chart_b, 4)
        self.assertIn('合', result['desc'])

    def test_trine_detected(self):
        """拱相被正确检测"""
        # 盘A: 太阳在 0度
        # 盘B: 木星在 120度 → 拱相 (经度由 degrees 决定，非 sign)
        offsets_a = {'sun': (1, 0, 0)}
        offsets_b = {'jupiter': (5, 120, 0)}
        chart = self._make_mock_chart(offsets_a)
        chart_b = self._make_mock_chart(offsets_b)
        result = star_point_comparison(chart, chart_b, 4)
        self.assertIn('拱', result['desc'])


# ============================================================
# transit_desc 集成测试 (真实 API)
# ============================================================

class TestTransitDesc(unittest.TestCase):
    """transit_desc 真实 API 集成测试

    注意: 这些测试需要网络连接，会调用真实 API
    """

    def test_basic_call(self):
        """基本调用测试 (使用经纬度避免地理编码偶发失败)"""
        result = transit_desc(
            time="2026-03-09 21:57:00",
            latitude=31.57766,
            longitude=120.29528,
            source_tz_offset=8
        )
        print(result)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith('行运信息:'))

    def test_with_coordinates(self):
        """使用经纬度调用"""
        result = transit_desc(
            time="2026-03-09 21:57:00",
            latitude=31.57766,
            longitude=120.29528,
            source_tz_offset=8
        )
        self.assertIsNotNone(result)
        self.assertTrue(result.startswith('行运信息:'))

    def test_output_format(self):
        """验证输出格式: 行运信息:...落X宫;..."""
        result = transit_desc(
            time="2026-03-09 21:57:00",
            address="无锡",
            source_tz_offset=8
        )
        # 应包含 "落X宫" 格式
        self.assertRegex(result, r'落\d+宫')
        # 应包含分号分隔
        self.assertIn(';', result)

    def test_different_timezone(self):
        """不同时区测试"""
        result = transit_desc(
            time="1990-06-15 14:30:00",
            address="北京",
            source_tz_offset=8
        )
        self.assertIsNotNone(result)
        self.assertTrue(result.startswith('行运信息:'))


# ============================================================
# 常量完整性测试
# ============================================================

class TestConstants(unittest.TestCase):
    """常量完整性检查"""

    def test_star_array_completeness(self):
        """STAR_ARRAY 包含所有主要行星"""
        expected = ['sun', 'moon', 'mercury', 'venus', 'mars',
                    'saturn', 'jupiter', 'uranus', 'neptune', 'pluto', 'north_node']
        self.assertEqual(STAR_ARRAY, expected)

    def test_star_name_map_covers_star_array(self):
        """STAR_NAME_MAP 覆盖 STAR_ARRAY 中所有行星"""
        for item in STAR_ARRAY:
            self.assertIn(item, STAR_NAME_MAP, f"STAR_NAME_MAP 缺少 {item}")

    def test_transit_type_covers_all(self):
        """TRANSIT_TYPE 覆盖 STAR_NAME_MAP 中所有行星"""
        for name in STAR_NAME_MAP.values():
            self.assertIn(name, TRANSIT_TYPE, f"TRANSIT_TYPE 缺少 {name}")

    def test_star_order_covers_all(self):
        """STAR_ORDER 覆盖 STAR_NAME_MAP 中所有行星"""
        for name in STAR_NAME_MAP.values():
            self.assertIn(name, STAR_ORDER, f"STAR_ORDER 缺少 {name}")

    def test_zodiac_signs_count(self):
        """ZODIAC_SIGNS 有12个星座"""
        self.assertEqual(len(ZODIAC_SIGNS), 12)

    def test_aspects_definition(self):
        """ASPECTS 定义正确"""
        aspect_names = [a[0] for a in ASPECTS]
        self.assertIn('合', aspect_names)
        self.assertIn('六合', aspect_names)
        self.assertIn('刑', aspect_names)
        self.assertIn('拱', aspect_names)
        self.assertIn('冲', aspect_names)


if __name__ == '__main__':
    unittest.main()
