import json

with open("./standard/id-nm-sx.json", "r", encoding="utf-8") as f:
    result = json.load(f)


while line_ := input(">>>"):
    lls: list[str] = line_.strip().split("\t")

    if (idn := str(lls[0])) in result:
        result[idn][lls[2]] = lls[3]
    else:
        result[idn] = {"姓名": lls[1], "性别": "", lls[2]: lls[3]}


with open("FNL_RESULT.CSV", "w", encoding="gbk") as f:
    f.write(
        "学号,姓名,性别,总分,思想政治道德素质成绩,专业理论素质成绩,身心素质成绩,创造精神和实践精神成绩,备注\n"
    )
    for k, v in result.items():
        f.write(
            "{},{},{},{},{},{},{},{},\n".format(
                k,
                v["姓名"],
                v["性别"],
                sum(
                    (
                        float(i)
                        for i in (
                            v["思想政治道德素质"],
                            v["专业理论素质"],
                            v["身心素质"],
                            v["创造精神和实践能力"],
                        )
                    )
                ),
                v["思想政治道德素质"],
                v["专业理论素质"],
                v["身心素质"],
                v["创造精神和实践能力"],
            )
        )
