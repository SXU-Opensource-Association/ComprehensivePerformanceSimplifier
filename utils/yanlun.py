# -*- coding: utf-8 -*-

"""
綜測計算軟體 言论版组件
Linglun Converter Yan Lun Component

版权所有 © 2026 金羿
Copyright © 2026 Eilles

本文件選摘自“伶倫轉換器”專案，原專案地址：
https://gitee.com/TriM-Organization/Linglun-Converter
該項目以 汉钰律许可协议，第一版 授權。
本文件繼承該協議，獨立授權，授權文本如下：

伶伦转换器WXGUI版本（“原项目”）的协议颁发者为 金羿
The Licensor of _Linglun Converter WxPython GUI_ is Eilles Wan.

原项目根据 汉钰律许可协议，第一版（“本协议”）授权。
任何人皆可从以下地址获得本协议副本：https://gitee.com/EillesWan/YulvLicenses。
若非因法律要求或经过了特殊准许，此作品在根据本协议“原样”提供的基础上，不予提供任何形式的担保、任何明示、任何暗示或类似承诺。也就是说，用户将自行承担因此作品的质量或性能问题而产生的全部风险。
详细的准许和限制条款请见原协议文本。

"""

import zhDateTime

from .console import logger  # , prt

STANDARD_WHITE = (242, 244, 246)
STANDART_BLACK = (18, 17, 16)

yanlun_fg_colour = STANDARD_WHITE
yanlun_bg_colour = STANDART_BLACK

logger.info("获取 言·论 信息……")

solar_datetime = zhDateTime.DateTime.now()
lunar_datetime = solar_datetime.to_chinese_format()
solar_date = (solar_datetime.month, solar_datetime.day)
lunar_date = (
    lunar_datetime.chinese_calendar_month,
    lunar_datetime.chinese_calendar_day,
)

logger.info(
    "當前日期：{} 西洋曆{}月{}日".format(lunar_datetime.date_hanzify(), *solar_date)
)

if solar_date == (4, 3):
    yanlun_texts = ["金羿ELS 生日快乐~！", "Happy Birthday, Eilles!"]

else:
    yanlun_texts = [
        "綜測計算簡化軟體 版權所有 © 2026 金羿",
        "Comprehensive Performance Calculation Simplifying Software, Copyright © 2026 Eilles",
    ]
