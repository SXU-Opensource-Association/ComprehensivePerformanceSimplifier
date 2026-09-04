import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import numpy as np
import os


from utils.console import logger, object_constants, log__init__
from utils.yanlun import yanlun_texts

__appname__ = "主修课加权平均计算工具"
__version__ = "0.0.1"


logger.info("注册变量并读取内容……")

osc = object_constants.ObjectStateConstant(
    logging_project_name=__appname__,
    logging_project_version=__version__,
    logging_exit_exec=lambda sth: messagebox.showinfo(
        "崩溃",
        sth + "\n问题不大吧？有问题拜托请报给开发者！谢谢！",
        icon="error",
    ),
    # is_this_a_release=True,
)
osc.set_console(logger.console)

log__init__(osc, True)

logger.is_logging = True
logger.suffix = ".gct"
logger.is_tips = True
logger.printing = not osc.is_release


class GradeCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("学院综合测评主修课加权分计算器")
        self.root.geometry("600x400")

        self.file_path = None
        self.df_raw = None
        self.course_credits = {}  # {课程名: 学分}
        self.student_data = []  # [{学号, 姓名, scores: {课程: 分数}}, ...]

        # 界面布局
        self.create_widgets()

    def create_widgets(self):
        # 1. 文件选择区域
        frame_file = tk.Frame(self.root, pady=10)
        frame_file.pack(fill=tk.X, padx=20)

        tk.Label(
            frame_file,
            text="步骤 1: 选择成绩单 Excel 文件",
            font=("MiSans", 12, "bold"),
        ).pack(anchor=tk.W)
        self.btn_load = tk.Button(
            frame_file, text="打开 Excel 文件", command=self.load_file, width=20
        )
        self.btn_load.pack(side=tk.LEFT, padx=5)
        self.lbl_file = tk.Label(frame_file, text="未选择文件", fg="gray")
        self.lbl_file.pack(side=tk.LEFT, padx=10)

        # 2. 课程选择区域 (初始隐藏)
        self.frame_courses = tk.Frame(self.root, pady=10)
        # 不立即 pack，等加载文件后显示

        tk.Label(
            self.frame_courses,
            text="步骤 2: 勾选主修科目 （未勾选则不参与计算）",
            font=("MiSans", 12, "bold"),
        ).pack(anchor=tk.W)

        # 创建带滚动条的 Canvas 来放置复选框
        self.canvas = tk.Canvas(self.frame_courses)
        self.scrollbar = ttk.Scrollbar(
            self.frame_courses, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.course_vars = {}  # {课程名: BooleanVar}

        # 3. 操作按钮区域
        frame_action = tk.Frame(self.root, pady=20)
        frame_action.pack(fill=tk.X, padx=20)

        self.btn_calc = tk.Button(
            frame_action,
            text="步骤 3: 计算并导出结果",
            command=self.calculate_and_export,
            state=tk.DISABLED,
            bg="#4CAF50",
            fg="white",
            font=("MiSans", 10, "bold"),
        )
        self.btn_calc.pack(fill=tk.X)

        self.status_label = tk.Label(self.root, text="", fg="blue")
        self.status_label.pack(pady=10)

    def load_file(self):
        self.file_path = filedialog.askopenfilename(
            filetypes=[("Excel 表格文件", "*.xlsx *.xls")]
        )
        if not self.file_path:
            return

        self.lbl_file.config(text=os.path.basename(self.file_path), fg="black")
        self.status_label.config(text="正在读取数据...")
        self.root.update()

        try:
            # 读取 Excel，header=None 表示没有默认表头，我们需要手动处理
            # 根据描述：
            # Row 0-3: 标题信息
            # Row 4 (index 4): 课程名称 (对应图中的第5行)
            # Row 5 (index 5): 学时 (对应图中的第6行，虽然计算不用，但占位)
            # Row 6 (index 6): 学分 (对应图中的第7行)
            # Row 7+ (index 7+): 学生数据

            # 使用 openpyxl 引擎读取以保留更多信息，或者直接用 pandas skiprows
            # 这里为了稳健，先读入所有数据

            df = pd.read_excel(self.file_path, header=None)

            # 定位关键行索引 (基于0的索引)
            # 用户说：5行为课程名称 -> index 4
            # 7行为学分 -> index 6
            # 8行开始为学生 -> index 7

            idx_course_name = 4
            idx_credit = 6
            idx_student_start = 7

            # 提取课程名和学分
            # 注意：表格前几列可能是 学号、姓名、性别 等，需要跳过
            # 假设前3列是固定信息 (学号, 姓名, 性别/学时占位)，从第4列(index 3)开始是课程
            # 根据提供的文本数据：
            # Col 0: 学号, Col 1: 姓名, Col 2: 性别/学时标签?
            # 让我们动态检测：找到 "课程名称" 所在的行，然后看哪一列开始有具体课程名

            row_courses = df.iloc[idx_course_name]
            row_credits = df.iloc[idx_credit]

            # 找到课程开始的列索引 (跳过前面的 '课程名称', '学号', '姓名' 等)
            # 简单策略：从第3列开始尝试，或者找到第一个非空且不是元数据的列
            start_col = 3  # 假设前3列是元数据

            self.course_credits = {}
            valid_courses = []

            for col in range(start_col, len(row_courses)):
                course_name = row_courses[col]
                credit_val = row_credits[col]

                # 清洗数据
                if pd.notna(course_name) and str(course_name).strip() not in [
                    "算术平均分",
                    "名次",
                    "总学分绩点",
                    "公选课获得学分",
                    "加权平均分",
                    "班级排名",
                ]:
                    # 尝试转换学分
                    try:
                        credit = float(credit_val)
                        self.course_credits[str(course_name).strip()] = credit
                        valid_courses.append(str(course_name).strip())
                    except (ValueError, TypeError):
                        logger.info(
                            "无法转换为学分的列 `{}`:`{}`".format(
                                course_name, credit_val
                            )
                        )
                        continue

            if not valid_courses:
                messagebox.showerror(
                    "错误",
                    "未能识别出有效的课程和学分，请检查表格格式是否符合要求（第5行课程名，第7行学分）。",
                )
                return

            # 提取学生数据
            self.student_data = []
            for row_idx in range(idx_student_start, len(df)):
                row = df.iloc[row_idx]
                sid = row[0]
                name = row[1]

                if pd.isna(sid) or str(sid).strip() == "":
                    logger.info("学号 `{}` 是空的，直接跳过".format(sid))
                    continue

                try:
                    float(sid)
                except ValueError:
                    logger.info("学号 `{}` 看上去不像是学号，直接跳过".format(sid))
                    continue

                scores = {}
                for col in range(start_col, len(row)):
                    course_name = row_courses[col]
                    if pd.notna(course_name):
                        c_name_str = str(course_name).strip()
                        if c_name_str in self.course_credits:
                            score_val = row[col]
                            # 处理缺考、空值等
                            if pd.notna(score_val):
                                try:
                                    s = float(score_val)
                                    scores[c_name_str] = s
                                except ValueError:
                                    # 可能是 "缺考$" 之类的字符串，视为0分或不计入？
                                    # 题目说：如果格子是空的，就没有修习。
                                    # 如果有字但不是数字（如缺考），通常算0分或者不计入。
                                    # 这里为了安全，如果是非数字，暂不计入该科（相当于没修），或者记为0。
                                    # 根据常规综测，缺考通常算0分。但题目强调“空格子=没修”。
                                    # 我们假设非数字且非空 = 0分 (参与计算但拉低平均分) 或者 忽略。
                                    # 只计入数字。如果是非数字，如“缺考”，用户可能需要手动在Excel改成0。
                                    # 这里我们只处理纯数字。

                                    # 别看上面人工智能瞎说
                                    # 下面已经处理了补考和缓考的情况
                                    if str(score_val).endswith(("*", "$")):
                                        if float(str(score_val)[:-1]) >= 60:
                                            scores[c_name_str] = float(
                                                str(score_val)[:-1]
                                            )
                                        else:
                                            scores[c_name_str] = 0

                self.student_data.append(
                    {
                        "sid": str(sid).strip(),
                        "name": str(name).strip() if pd.notna(name) else "",
                        "scores": scores,
                    }
                )
                logger.info("读取到 `{}`:`{}` 的成绩数据".format(sid, name))

            # 显示课程选择界面
            self.populate_course_selection(valid_courses)
            self.frame_courses.pack(fill=tk.BOTH, expand=True, padx=20)
            self.btn_calc.config(state=tk.NORMAL)
            self.status_label.config(
                text=f"成功加载 {len(self.student_data)} 名学生，{len(valid_courses)} 门课程。请勾选主修课。"
            )

        except Exception as e:
            messagebox.showerror("读取错误", f"发生错误: {str(e)}")

    def populate_course_selection(self, courses):
        # 清空旧控件
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.course_vars = {}

        # 每行放2个复选框以节省空间
        for i, course in enumerate(courses):
            var = tk.BooleanVar(value=False)  # 默认不选，让用户主动选主修
            self.course_vars[course] = var

            cb = tk.Checkbutton(
                self.scrollable_frame,
                text=f"{course} ({self.course_credits[course]}学分)",
                variable=var,
            )
            cb.grid(row=i // 2, column=i % 2, sticky=tk.W, padx=5, pady=2)

        # 添加全选/反选按钮
        btn_frame = tk.Frame(self.scrollable_frame)
        btn_frame.grid(row=len(courses) // 2 + 1, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="全选", command=lambda: self.toggle_all(True)).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(
            btn_frame, text="全不选", command=lambda: self.toggle_all(False)
        ).pack(side=tk.LEFT, padx=5)

    def toggle_all(self, select):
        for var in self.course_vars.values():
            var.set(select)

    def calculate_and_export(self):
        # 1. 获取选中的主修课
        selected_courses = [c for c, var in self.course_vars.items() if var.get()]

        if not selected_courses:
            messagebox.showwarning("提示", "请至少选择一门主修课程！")
            return

        # 2. 计算加权平均分
        results = []

        for student in self.student_data:
            total_weighted_score = 0.0
            total_credits = 0.0

            for course in selected_courses:
                if course in student["scores"]:
                    score = student["scores"][course]
                    credit = self.course_credits[course]
                    total_weighted_score += score * credit
                    total_credits += credit

            # 计算平均分
            if total_credits > 0:
                weighted_avg = total_weighted_score / total_credits
            else:
                weighted_avg = 0.0

            results.append(
                {
                    "学号": student["sid"],
                    "姓名": student["name"],
                    "主修加权平均分": round(weighted_avg, 2),
                    "计入主修总学分": total_credits,
                }
            )

        # 3. 排名
        # 按加权平均分降序排序
        results.sort(key=lambda x: x["主修加权平均分"], reverse=True)

        # 添加排名 (处理并列排名：如果分数相同，排名相同)
        current_rank = 1
        for i, res in enumerate(results):
            if i > 0 and res["主修加权平均分"] < results[i - 1]["主修加权平均分"]:
                current_rank = i + 1
            res["班级排名"] = current_rank

        # 4. 导出
        save_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel 文件", "*.xlsx")],
            initialfile="主修课加权平均分排名.xlsx",
        )

        if save_path:
            df_result = pd.DataFrame(results)
            # 调整列顺序
            df_result = df_result[
                ["学号", "姓名", "主修加权平均分", "班级排名", "计入主修总学分"]
            ]
            df_result.to_excel(save_path, index=False)
            messagebox.showinfo("完成", f"计算完成！结果已保存至:\n{save_path}")
            self.status_label.config(text="导出成功！")
        else:
            self.status_label.config(text="取消保存。")


if __name__ == "__main__":
    root = tk.Tk()
    app = GradeCalculatorApp(root)
    root.mainloop()
