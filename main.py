import os
import re
import pandas as pd
from typing import List, Dict, Tuple
from openpyxl.styles import Alignment, Font


# 定义函数用来从文件夹中读取所有的xlsx文件
def read_checkin_files(folder_path: str) -> List[str]:
    """读取文件夹中的所有xlsx文件路径"""
    file_list: List[str] = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".xlsx"):
            file_path = os.path.join(folder_path, file_name)
            file_list.append(file_path)
    return file_list


# 定义函数读取每个签到表
def read_checkin_data(file_path: str) -> pd.DataFrame:
    """从文件路径读取Excel签到表并返回DataFrame"""
    data: pd.DataFrame = pd.read_excel(file_path)
    # 将学号列转换为字符串，避免科学计数法
    if "学号" in data.columns:
        data["学号"] = data["学号"].astype(str)
    return data


# 定义函数从文件名中提取课程名称
def extract_course_name(file_name: str) -> str:
    """使用正则表达式从文件名中提取汉字部分作为课程名称"""
    match = re.search(r"[\u4e00-\u9fff]+", file_name)
    if match:
        return match.group(0)
    return "未知课程"


# 定义函数从签到数据中提取时间信息
def extract_checkin_time(checkin_data: pd.DataFrame) -> str:
    """从签到数据中提取签到日期和时间，并格式化为'MM月DD日-[上午/下午]'"""
    if "签到日期" not in checkin_data.columns:
        return "未知时间"
    # 提取签到日期
    checkin_date = checkin_data["签到日期"].iloc[0]
    if not isinstance(checkin_date, str):
        checkin_date = checkin_date.strftime("%Y-%m-%d")
    # 提取签到时间（如果存在）
    if "签到时间" in checkin_data.columns:
        checkin_time = checkin_data["签到时间"].iloc[0]
        if isinstance(checkin_time, str):
            hour = int(checkin_time.split(":")[0])
        else:
            hour = checkin_time.hour
    else:
        hour = 12  # 默认中午12点
    period = "上午" if hour < 13 else ("下午" if hour < 19 else "晚上")
    # 格式化日期
    month = checkin_date.split("-")[1]
    day = checkin_date.split("-")[2]
    return f"{month}月{day}日-{period}"


# 定义函数来解析签到数据
def analyze_checkins(
    checkin_data_list: List[pd.DataFrame],
    file_names: List[str],
    class_student_list: List[Tuple[str, str]],
) -> Tuple[Dict[str, pd.DataFrame], List[Dict[str, str]]]:
    """根据签到数据列表和班级学生名单进行分析，按课程名称和时间分组统计签到情况"""
    course_results: Dict[str, pd.DataFrame] = {}  # 按课程名称和时间存储结果
    anomalies: List[Dict[str, str]] = []  # 存储异常数据

    id_name_dict = dict(class_student_list)

    for file_data, file_name in zip(checkin_data_list, file_names):
        # 检查数据结构
        if (
            "学号" in file_data.columns
            and "姓名" in file_data.columns
            and "签到日期" in file_data.columns
        ):
            checkin_record: pd.DataFrame = file_data
            checked_in_ids: List[str] = checkin_record["学号"].tolist()
            checked_in_names: List[str] = checkin_record["姓名"].tolist()
            course_name = extract_course_name(file_name)  # 提取课程名称
            time_label = extract_checkin_time(checkin_record)  # 提取签到时间
            column_header = f"{time_label}\n{course_name}"  # 生成表头
            student_results: List[dict] = []

            for student_id, student_name in class_student_list:
                status: str = (
                    "已签到"
                    if student_id in checked_in_ids
                    else (
                        "已签到*学号错误"
                        if student_name in checked_in_names
                        else "未签到"
                    )
                )
                student_results.append(
                    {
                        "学号": student_id,
                        "姓名": student_name,
                        column_header: status,  # 动态生成列名
                    }
                )

            for checkined_student_id, checkined_student_name in zip(
                checked_in_ids, checked_in_names
            ):
                if (
                    checkined_student_id in id_name_dict.keys()
                    and checkined_student_name != id_name_dict[checkined_student_id]
                ):
                    print(
                        f"姓名与学号不匹配\n\t学号：`{checkined_student_id}`，姓名：`{checkined_student_name}`，登表名：`{id_name_dict[checkined_student_id]}`\n"
                    )
                    anomalies.append(
                        {
                            "学号": checkined_student_id,
                            "姓名": checkined_student_name,
                            "异常原因": "姓名与学号不匹配",
                        }
                    )
                if checkined_student_id not in id_name_dict.keys():
                    if checkined_student_name not in id_name_dict.values():
                        print(
                            f"学号及姓名皆错误，查无此人\n\t学号：`{checkined_student_id}`，姓名：`{checkined_student_name}`\n"
                        )
                        anomalies.append(
                            {
                                "学号": checkined_student_id,
                                "姓名": checkined_student_name,
                                "异常原因": "学号及姓名皆错误，查无此人",
                            }
                        )
                    else:
                        print(
                            f"学号错误\n\t学号：`{checkined_student_id}`，姓名：`{checkined_student_name}`\n"
                        )
                        anomalies.append(
                            {
                                "学号": checkined_student_id,
                                "姓名": checkined_student_name,
                                "异常原因": "学号错误",
                            }
                        )

            # 将当前课程的签到结果存储到字典中
            course_results[column_header] = pd.DataFrame(student_results)
        else:
            print(f"文件 {file_name} 格式有误，无法处理")
    return course_results, anomalies


# 定义主函数
def process_checkins(folder_path: str, class_list_file: str) -> None:
    """主函数：分析签到情况并输出结果为Excel文件"""
    # 读取数据
    file_list: List[str] = read_checkin_files(folder_path)
    checkin_data_list: List[pd.DataFrame] = []
    for file in file_list:
        data: pd.DataFrame = read_checkin_data(file)
        checkin_data_list.append(data)

    # 读取全班学生名单（仅读取前两列）
    class_list_df: pd.DataFrame = pd.read_excel(class_list_file, usecols=[0, 1])
    # 将学号列转换为字符串，避免科学计数法
    class_list_df["学号"] = class_list_df["学号"].astype(str)
    class_student_list: List[Tuple[str, str]] = class_list_df[
        ["学号", "姓名"]
    ].values.tolist()

    # 分析签到情况
    course_results, anomalies = analyze_checkins(
        checkin_data_list,
        [os.path.basename(file) for file in file_list],
        class_student_list,
    )

    # 将所有课程的签到结果合并到一个DataFrame中
    final_results: pd.DataFrame = class_list_df.copy()  # 以班级名单为基础
    for column_header, course_data in sorted(
        course_results.items(),
        key=lambda x: x[0]
        .replace("上午", "00")
        .replace("下午", "12")
        .replace("晚上", "18"),
    ):
        # 将每门课程的签到状态合并到最终结果中
        final_results = final_results.merge(
            course_data[["学号", column_header]], on="学号", how="left"
        )

    # 将结果保存为Excel文件
    output_file_path: str = "Checkin_Results.xlsx"
    with pd.ExcelWriter(output_file_path, engine="openpyxl") as writer:
        final_results.to_excel(writer, sheet_name="签到统计", index=False)
        # 将异常数据保存到另一个工作表中
        anomalies_df = pd.DataFrame(anomalies)
        anomalies_df.to_excel(writer, sheet_name="异常数据", index=False)
        # 设置单元格样式
        workbook = writer.book
        worksheet = writer.sheets["签到统计"]
        # 设置表头自动换行
        for col in worksheet.columns:
            col_letter = col[0].column_letter
            worksheet.column_dimensions[col_letter].width = 15  # 设置列宽
            for cell in col:
                if cell.row == 1:  # 表头行
                    cell.alignment = Alignment(wrap_text=True, horizontal="center")
                else:
                    if "已签到" in cell.value:
                        cell.alignment = Alignment(horizontal="left")
                    elif "未签到" in cell.value:
                        cell.font = Font(bold=True)
                        cell.alignment = Alignment(horizontal="right")

    print(f"分析结束，结果在 {output_file_path}")


# 调用主函数
if __name__ == "__main__":
    folder_path: str = input("请输入签到表所在的文件夹路径：")
    class_list_file: str = input("请输入全班学生名单文件路径（xlsx格式）：")
    process_checkins(folder_path, class_list_file)
