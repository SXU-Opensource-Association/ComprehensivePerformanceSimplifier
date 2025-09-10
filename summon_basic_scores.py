from pathlib import Path

import json
from typing import Any

basic_score_csv = Path("./results/basic_score.csv")


id_name_chart: dict[str, list[str]] = json.load(
    open("./standard/name_id.json", "r", encoding="utf-8"),
)

reference_levels: dict[str, dict[str, dict[str, Any]]] = json.load(
    open("./standard/referance.json", "r", encoding="utf-8"),
)

if not basic_score_csv.exists():
    basic_score_csv.open("w", encoding="gbk").write(
        "学号,姓名,一级指标,二级指标,基础分,满分,描述,加分\n"
    )

donelist = []

for id, name in id_name_chart.items():
    for lv1 in reference_levels.keys():
        for lv2 in reference_levels[lv1].keys():
            if lv2 in donelist:
                continue
            if reference_levels[lv1][lv2]["共用"]:
                donelist.append(reference_levels[lv1][lv2]["共用"])
            if reference_levels[lv1][lv2]["基础分"] > 0:
                basic_score_csv.open("a", encoding="gbk").write(
                    f"\"{id}\",{name[0]},{lv1},{lv2},{reference_levels[lv1][lv2]['基础分']},{reference_levels[lv1][lv2]['满分']},基础分加分占位,{reference_levels[lv1][lv2]['默认加分']}\n"
                    if ("默认加分" in reference_levels[lv1][lv2])
                    else f"\"{id}\",{name[0]},{lv1},{lv2},{reference_levels[lv1][lv2]['基础分']},{reference_levels[lv1][lv2]['满分']},基础分加分占位,0\n"
                )
