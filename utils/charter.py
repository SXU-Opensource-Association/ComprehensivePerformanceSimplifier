
import pandas as pd
# import openpyxl as opxl

# xlsheet = opxl.load_workbook("",keep_vba=True,data_only=True,keep_links=True,rich_text=True)
# xlsheet.sheetnames
# [j.value for j in [i for i in xlsheet[""].rows][0]]
# xlsheet[""]._images
# xlsheet._images
# 定义函数读取证明表
def read_chart_data(file_path: str) -> pd.DataFrame:
    """从文件路径读取Excel签到表并返回DataFrame"""
    data: pd.DataFrame = pd.read_excel(file_path)
    # 将学号列转换为字符串，避免科学计数法
    if "学号（必填）" in data.columns:
        data["学号（必填）"] = data["学号（必填）"].astype(str)
    return data

