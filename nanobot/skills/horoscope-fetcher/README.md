# Horoscope Fetcher

星盘数据获取工具 - 从 deepastro.cn API 获取本命盘数据

## 功能特性

- ✅ 获取完整的本命盘数据（行星位置、相位、宫位）
- ✅ 自动地理编码（地址 → 经纬度）
- ✅ 灵活的时间格式支持
- ✅ 详细的星盘解读
- ✅ 支持中文和英文输出

## 安装依赖

```bash
pip install requests
```

## 快速开始

### 基本用法

```bash
# 使用地址获取星盘
python3 scripts/horoscope_fetcher.py get_chart \
  --time "1940-10-09 17:30:00" \
  --address "利物浦"

# 使用经纬度获取星盘
python3 scripts/horoscope_fetcher.py get_chart \
  --time "1940-10-09 17:30:00" \
  --latitude 53.41666 \
  --longitude -3

# 输出 JSON 格式
python3 scripts/horoscope_fetcher.py get_chart \
  --time "1990-01-01 12:00:00" \
  --latitude 39.9042 \
  --longitude 116.4074 \
  --json
```

### 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--time` | string | 是 | 出生时间 (YYYY-MM-DD HH:MM:SS) |
| `--address` | string | 否* | 出生地点 |
| `--latitude` | float | 否* | 纬度 |
| `--longitude` | float | 否* | 经度 |
| `--timezone` | string | 否 | 时区 (默认: GMT) |
| `--show-desc` | bool | 否 | 显示详细描述 (默认: true) |
| `--json` | flag | 否 | 输出 JSON 格式 |

* 必须提供地址或经纬度之一

## 输出示例

### 摘要格式

```
============================================================
🌟 星盘摘要
============================================================

📌 基本信息:
   上升白羊,命主星火星,四宫头在巨蟹,七宫头在天秤,十宫头在摩羯,

🪐 行星位置:
   太阳       → 天蝎座 (Scorpio)   (16°16')
   月亮       → 双鱼座 (Pisces)    (3°32')
   水星       → 射手座 (Sagittarius) (8°33')
   ...

🎯 四轴:
   上升       → 金牛座 (Taurus)    (19°41')
   下降       → 天蝎座 (Scorpio)   (19°41')
   ...

🔗 主要相位:
   太阳冲上升                (176.6°)
   太阳合下降                (3.4°)
   ...

⏪ 逆行行星:
   • 木星逆行
   • 土星逆行
   ...
```

### JSON 格式

```json
{
  "data": {
    "astros": {
      "sun": {
        "name": "sun",
        "position": {
          "longitude": 196.2678938511275,
          "degrees": 16,
          "minutes": 16,
          "seconds": 4
        },
        "sign": 7
      },
      ...
    },
    "axes": {...},
    "houses": [...],
    "pairs": [...],
    "info1": "...",
    "info2": "...",
    "alldesc": "..."
  }
}
```

## 星座对照表

| 索引 | 星座 | 英文 |
|------|------|------|
| 0 | 白羊 | Aries |
| 1 | 金牛 | Taurus |
| 2 | 双子 | Gemini |
| 3 | 巨蟹 | Cancer |
| 4 | 狮子 | Leo |
| 5 | 处女 | Virgo |
| 6 | 天秤 | Libra |
| 7 | 天蝎 | Scorpio |
| 8 | 射手 | Sagittarius |
| 9 | 摩羯 | Capricorn |
| 10 | 水瓶 | Aquarius |
| 11 | 双鱼 | Pisces |

## 相位类型

| 类型 | 度数 | 名称 |
|------|------|------|
| 0 | 0° | 合相 (Conjunction) |
| 60 | 60° | 六合 (Sextile) |
| 90 | 90° | 刑 (Square) |
| 120 | 120° | 拱 (Trine) |
| 180 | 180° | 冲 (Opposition) |

## API 信息

- **API 地址**: https://horoscope.deepastro.cn/horoscope
- **方法**: GET
- **参数**:
  - `time`: 格式化时间 (如 "Wed, 09 Oct 1940 17:30:00 GMT")
  - `address`: 地址 (URL 编码)
  - `latitude`: 纬度
  - `longitude`: 经度
  - `isShowDesc`: 是否显示描述 (true/false)

## 注意事项

1. **时区**: API 默认使用 GMT 时区，如需其他时区请指定 `--timezone` 参数
2. **地理编码**: 使用 OpenStreetMap 的 Nominatim API，无需 API Key
3. **网络**: 需要稳定的网络连接访问 API
4. **精度**: 经纬度建议保留 5 位小数

## 示例场景

### 获取名人星盘

```bash
# 约翰·列侬
python3 scripts/horoscope_fetcher.py get_chart \
  --time "1940-10-09 17:30:00" \
  --latitude 53.41666 \
  --longitude -3

# 邓丽君
python3 scripts/horoscope_fetcher.py get_chart \
  --time "1953-01-29 08:00:00" \
  --address "台湾云林县"
```

### 批量分析

```bash
# 创建脚本批量处理
for person in "1990-01-01 12:00:00" "1985-06-15 08:30:00"; do
  python3 scripts/horoscope_fetcher.py get_chart \
    --time "$person" \
    --latitude 39.9042 \
    --longitude 116.4074
done
```

## 故障排除

### 地理编码失败

如果地址解析失败，请直接提供经纬度：

```bash
# ❌ 地址解析失败
python3 scripts/horoscope_fetcher.py get_chart \
  --time "1990-01-01 12:00:00" \
  --address "未知地址"

# ✅ 使用经纬度
python3 scripts/horoscope_fetcher.py get_chart \
  --time "1990-01-01 12:00:00" \
  --latitude 39.9042 \
  --longitude 116.4074
```

### API 调用失败

检查网络连接，或稍后重试。

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
