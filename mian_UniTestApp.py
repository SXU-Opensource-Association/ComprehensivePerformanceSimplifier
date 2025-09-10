# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
###########################################################################

import wx
import wx.xrc
import wx.richtext

import json
import random
import shutil
import gettext

from pathlib import Path

from utils.console import logger, object_constants, log__init__, TrimLog, Any
from utils.yanlun import yanlun_texts, yanlun_fg_colour, yanlun_bg_colour
from utils.charter import read_chart_data


_ = gettext.gettext


__appname__ = "综合评测计分工具"
__version__ = "0.0.1"


logger.info("注册变量并读取内容……")

osc = object_constants.ObjectStateConstant(
    logging_project_name=__appname__,
    logging_project_version=__version__,
    logging_exit_exec=lambda sth: wx.MessageDialog(
        None,
        sth + "\n问题不大吧？有问题拜托请报给开发者！谢谢！",
        "崩溃",
        wx.YES_DEFAULT | wx.ICON_STOP,
    ).ShowModal(),
    # is_this_a_release=True,
)
# print(osc.exit_execution)
osc.set_console(logger.console)

log__init__(osc, TrimLog.PipManage(True, True, 40), True)

logger.is_logging = True
logger.suffix = ".uta"
logger.is_tips = True
logger.printing = not osc.is_release


yanlun_length = len(yanlun_texts)


id_name_chart: dict[str, list[str]] = json.load(
    open("./standard/name_id.json", "r", encoding="utf-8"),
)

reference_levels: dict[str, dict[str, dict[str, Any]]] = json.load(
    open("./standard/referance.json", "r", encoding="utf-8"),
)
true_result_csv = Path("./results/got_result.csv")
if not true_result_csv.exists():
    true_result_csv.open("w", encoding="gbk").write(
        "学号,姓名,一级指标,二级指标,基础分,满分,描述,加分,证明备注,证明\n"
    )

error_result_csv = Path("./results/error_result.csv")
if not error_result_csv.exists():
    error_result_csv.open("w", encoding="gbk").write("学号,姓名,描述,图片\n")


class PersonStatus:
    OK = 0
    FINE_WITH_ID_ERROR = 1
    FINE_WITH_NAME_ERROR = 2
    ERROR = 3

    name: str
    id: str

    def __init__(self, name: str, id: Any):
        id = str(id)
        self.status = None
        if id in id_name_chart.keys():
            if name in id_name_chart[id]:
                self.status = PersonStatus.OK
            else:
                self.status = PersonStatus.FINE_WITH_NAME_ERROR
            self.id = id
            self.name = id_name_chart[id][0]
        else:
            for _id in id_name_chart.keys():
                if name in id_name_chart[_id]:
                    self.status = PersonStatus.FINE_WITH_ID_ERROR
                    self.id = _id
                    self.name = id_name_chart[_id][0]
                    break
            if not self.status:
                self.status = PersonStatus.ERROR
                self.id = id
                self.name = name

    def get_status_text(self) -> str:
        if self.status == PersonStatus.OK:
            return _("存在")
        elif self.status == PersonStatus.FINE_WITH_ID_ERROR:
            return _("姓名存在*学号错误")
        elif self.status == PersonStatus.FINE_WITH_NAME_ERROR:
            return _("学号存在*姓名错误")
        else:
            return _("查无此人")

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> str:
        return self.id

    def __str__(self) -> str:
        return f"{self.name} {self.id} {self.status}"

    def get_person_info(self) -> str:
        return f"姓名：{self.name}\t学号：{self.id}\t验证：{self.get_status_text()}"

    def get_store_path(self) -> Path:
        return (Path("./results/") / "{}_{}".format(self.id, self.name)).resolve()


logger.info("加载框架……")


class DrawingPanel(wx.Panel):
    def __init__(self, parent, id, pos, size, style, image_path):
        super(DrawingPanel, self).__init__(parent, id, pos, size, style)

        self.i_path = image_path

        self.image = wx.Image(image_path, wx.BITMAP_TYPE_ANY)

        self.original_image = self.image.Copy()
        self.drawing = False
        self.last_point = None
        self.scale_factor = 1.0

        # Bind events
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_MOTION, self.on_motion)
        self.Bind(wx.EVT_MOUSEWHEEL, self.on_mouse_wheel)

    def change_image(
        self,
        image_path,
        save_perivous_image: bool = True,
    ):
        if save_perivous_image:
            self.save_image(self.i_path)

        self.i_path = image_path

        self.image = wx.Image(image_path, wx.BITMAP_TYPE_ANY)
        self.original_image = self.image.Copy()
        self.scale_factor = 1.0
        self.Refresh()

    def on_paint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        # wx.Bitmap().Rescale
        scaled_image = self.image.Scale(
            int(self.original_image.GetWidth() * self.scale_factor),
            int(self.original_image.GetHeight() * self.scale_factor),
            quality=wx.IMAGE_QUALITY_HIGH,
        )
        dc.DrawBitmap(scaled_image.ConvertToBitmap(), 0, 0)
        # self.Refresh()

    def on_left_down(self, event):
        self.drawing = True
        self.last_point = event.GetPosition()

    def on_left_up(self, event):
        self.drawing = False
        self.last_point = None

    def on_motion(self, event):
        if not self.drawing:
            return
        dc = wx.ClientDC(self)
        dc.SetPen(wx.Pen("red", 3))
        dc.DrawLine(self.last_point, event.GetPosition())
        self.update_drawing(event.GetPosition())
        self.last_point = event.GetPosition()

    def update_drawing(self, position):
        # wx.Point() * 3
        mem_dc = wx.MemoryDC(self.image.ConvertToBitmap())
        mem_dc.SetPen(wx.Pen("red", 3))
        mem_dc.DrawLine(
            int(self.last_point.x / self.scale_factor),  # type: ignore
            int(self.last_point.y / self.scale_factor),  # type: ignore
            int(position.x / self.scale_factor),
            int(position.y / self.scale_factor),
        )
        self.image = mem_dc.GetAsBitmap().ConvertToImage()
        del mem_dc

    def on_mouse_wheel(self, event):
        rotation = event.GetWheelRotation()
        if rotation > 0:
            self.scale_factor *= 1.1
        elif rotation < 0:
            self.scale_factor /= 1.1
        self.Refresh()

    def save_image(self, path=None):
        if path is None:
            path = self.i_path
        self.image.SaveFile(path, wx.BITMAP_TYPE_PNG)


###########################################################################
## Class MainFrame
###########################################################################


class MainFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title=_("综测评价简化应用"),
            pos=wx.DefaultPosition,
            size=wx.Size(1400, 900),
            style=wx.CAPTION
            | wx.DEFAULT_FRAME_STYLE
            | wx.TAB_TRAVERSAL
            | wx.TRANSPARENT_WINDOW,
            name="untestapp_window",
        )

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.Colour(240, 240, 240))

        self.now_person = PersonStatus(
            list(id_name_chart.keys())[0], list(id_name_chart.values())[0][0]
        )
        self.now_picture_index = 0

        self.m_menubar1 = wx.MenuBar(0)
        self.m_file_menu1 = wx.Menu()
        self.m_open_menuItem1 = wx.MenuItem(
            self.m_file_menu1,
            wx.ID_ANY,
            _("打开"),
            _("打开导入的Excel文件所在位置"),
            wx.ITEM_NORMAL,
        )
        self.m_file_menu1.Append(self.m_open_menuItem1)

        self.m_exit_menuItem2 = wx.MenuItem(
            self.m_file_menu1,
            wx.ID_ANY,
            _("退出"),
            _("你猜这个键用来干嘛"),
            wx.ITEM_NORMAL,
        )
        self.m_file_menu1.Append(self.m_exit_menuItem2)

        self.m_menubar1.Append(self.m_file_menu1, _("文件"))

        self.m_progress_menu3 = wx.Menu()
        self.m_progress_continue_menuItem5 = wx.MenuItem(
            self.m_progress_menu3,
            wx.ID_ANY,
            _("接续进度"),
            _("直接读取评分进度"),
            wx.ITEM_NORMAL,
        )
        self.m_progress_menu3.Append(self.m_progress_continue_menuItem5)

        self.m_progress_save_menuItem4 = wx.MenuItem(
            self.m_progress_menu3,
            wx.ID_ANY,
            _("进度暂存"),
            _("临时存储评分进度"),
            wx.ITEM_NORMAL,
        )
        self.m_progress_menu3.Append(self.m_progress_save_menuItem4)

        self.m_progress_menu3.AppendSeparator()

        self.m_progress_open_menuItem3 = wx.MenuItem(
            self.m_progress_menu3,
            wx.ID_ANY,
            _("打开进度"),
            _("打开存储的进度文件"),
            wx.ITEM_NORMAL,
        )
        self.m_progress_menu3.Append(self.m_progress_open_menuItem3)

        self.m_progress_save_as_menuItem6 = wx.MenuItem(
            self.m_progress_menu3,
            wx.ID_ANY,
            _("进度另存"),
            _("将进度文件存储在非默认位置"),
            wx.ITEM_NORMAL,
        )
        self.m_progress_menu3.Append(self.m_progress_save_as_menuItem6)

        self.m_menubar1.Append(self.m_progress_menu3, _("进度"))

        self.SetMenuBar(self.m_menubar1)

        main_bSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        left_bSizer2 = wx.BoxSizer(wx.VERTICAL)

        yanlun_sbSizer2 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("言·论")), wx.VERTICAL
        )

        self.m_yanlun_staticText1 = wx.StaticText(
            yanlun_sbSizer2.GetStaticBox(),
            wx.ID_ANY,
            _("综测评分简化系统"),
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.ALIGN_CENTER_HORIZONTAL | wx.ST_ELLIPSIZE_MIDDLE | wx.ST_NO_AUTORESIZE,
        )
        self.yanlun_now = random.randrange(0, yanlun_length)
        self.m_yanlun_staticText1.Wrap(-1)

        self.m_yanlun_staticText1.SetForegroundColour(yanlun_fg_colour)
        self.m_yanlun_staticText1.SetBackgroundColour(yanlun_bg_colour)

        yanlun_sbSizer2.Add(self.m_yanlun_staticText1, 0, wx.ALL | wx.EXPAND, 5)

        left_bSizer2.Add(yanlun_sbSizer2, 0, wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText7 = wx.StaticText(
            self, wx.ID_ANY, _("完成进度"), wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText7.Wrap(-1)

        bSizer4.Add(self.m_staticText7, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_progress_gauge1 = wx.Gauge(
            self,
            wx.ID_ANY,
            100,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.GA_HORIZONTAL | wx.GA_SMOOTH,
        )
        self.m_progress_gauge1.SetValue(25)
        bSizer4.Add(
            self.m_progress_gauge1,
            0,
            wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.RESERVE_SPACE_EVEN_IF_HIDDEN,
            5,
        )

        self.m_progress_staticText8 = wx.StaticText(
            self,
            wx.ID_ANY,
            _("000/000"),
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.ST_NO_AUTORESIZE,
        )
        self.m_progress_staticText8.Wrap(-1)

        bSizer4.Add(
            self.m_progress_staticText8,
            0,
            wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.RESERVE_SPACE_EVEN_IF_HIDDEN,
            5,
        )

        self.m_progress_save_button5 = wx.Button(
            self, wx.ID_ANY, _("进度暂存"), wx.DefaultPosition, wx.DefaultSize, 0
        )
        bSizer4.Add(
            self.m_progress_save_button5, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5
        )

        self.m_progress_save_status_staticText81 = wx.StaticText(
            self,
            wx.ID_ANY,
            _("❌未存储"),
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.ST_NO_AUTORESIZE,
        )
        self.m_progress_save_status_staticText81.Wrap(-1)

        bSizer4.Add(
            self.m_progress_save_status_staticText81,
            0,
            wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.RESERVE_SPACE_EVEN_IF_HIDDEN,
            5,
        )

        left_bSizer2.Add(bSizer4, 0, wx.EXPAND, 5)

        info_sbSizer5 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("信息展示区")), wx.VERTICAL
        )

        self.m_person_info_staticText9 = wx.StaticText(
            info_sbSizer5.GetStaticBox(),
            wx.ID_ANY,
            _("姓名：祁元辉\t学号：202400101100\t验证：成功"),
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.ST_NO_AUTORESIZE,
        )
        self.m_person_info_staticText9.Wrap(-1)

        info_sbSizer5.Add(
            self.m_person_info_staticText9,
            0,
            wx.ALL | wx.EXPAND | wx.RESERVE_SPACE_EVEN_IF_HIDDEN,
            5,
        )

        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText10 = wx.StaticText(
            info_sbSizer5.GetStaticBox(),
            wx.ID_ANY,
            _("证明所属一级指标"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText10.Wrap(-1)

        bSizer5.Add(self.m_staticText10, 0, wx.ALL, 5)

        self.m_the_first_lvquote_choice1Choices = [
            _("思想政治道德素质"),
            _("身心素质"),
            _("创造精神和实践能力"),
            _("未知一级指标"),
        ]
        self.m_the_first_lvquote_choice1 = wx.Choice(
            info_sbSizer5.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            self.m_the_first_lvquote_choice1Choices,
            0,
        )
        self.m_the_first_lvquote_choice1.SetSelection(0)
        bSizer5.Add(self.m_the_first_lvquote_choice1, 1, wx.ALL, 5)

        info_sbSizer5.Add(bSizer5, 0, wx.EXPAND, 5)

        bSizer6 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText101 = wx.StaticText(
            info_sbSizer5.GetStaticBox(),
            wx.ID_ANY,
            _("证明所属二级指标"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText101.Wrap(-1)

        bSizer6.Add(self.m_staticText101, 0, wx.ALL, 5)

        m_the_second_lvquote_choice2Choices = [
            _("集体观念、合作意识（成员）"),
        ]
        self.m_the_second_lvquote_choice2 = wx.Choice(
            info_sbSizer5.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            m_the_second_lvquote_choice2Choices,
            0,
        )
        self.m_the_second_lvquote_choice2.SetSelection(0)
        bSizer6.Add(self.m_the_second_lvquote_choice2, 1, wx.ALL, 5)

        info_sbSizer5.Add(bSizer6, 0, wx.EXPAND, 5)

        self.m_description_textCtrl1 = wx.TextCtrl(
            info_sbSizer5.GetStaticBox(),
            wx.ID_ANY,
            _(
                "客观描述证明内容：\n - 奖级：校级\t奖次：参与奖\t任职：个人\n - 活动：北昌大学第零届“你好世界，一二三四”啊这什么大赛啥学院初赛\n主观描述证明内容：\n\t北昌大学第零届“你好世界，一二三四”啊这什么大赛啥学院初赛参与奖"
            ),
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_MULTILINE | wx.TE_PROCESS_TAB | wx.TE_RICH | wx.HSCROLL,
        )
        info_sbSizer5.Add(self.m_description_textCtrl1, 2, wx.ALL | wx.EXPAND, 5)

        self.m_basic_max_staticText10 = wx.StaticText(
            info_sbSizer5.GetStaticBox(),
            wx.ID_ANY,
            _("基础分：1\t满分：2.5\t共用：创造精神和创新能力（项目）"),
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.ST_NO_AUTORESIZE,
        )
        self.m_basic_max_staticText10.Wrap(-1)

        info_sbSizer5.Add(
            self.m_basic_max_staticText10,
            0,
            wx.ALL | wx.EXPAND | wx.RESERVE_SPACE_EVEN_IF_HIDDEN,
            5,
        )

        left_bSizer2.Add(info_sbSizer5, 0, wx.EXPAND, 5)

        the_third_lvquote_sbSizer6 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("三级指标参考")), wx.VERTICAL
        )

        self.m_the_third_lvquote_richText1 = wx.TextCtrl(
            the_third_lvquote_sbSizer6.GetStaticBox(),
            wx.ID_ANY,
            _(
                "请注意：以下各个职位若有兼任皆不累加，取最高分。\n班委成员中，班长、团支书、学委加1分；其他班委加0.5分；舍长加0.2分。\n校级组织中（校学生会、校报、广播站、电视台、社联），主席团加1分，部长加0.5分，副部长加0.4分，干事0.1分。\n辩论队：教练0.5、负责人0.4、队员0.1\n足篮排等各类队伍：队长0.4，副队长0.3，其他负责（财务、副队长）0.2，队员0.1\n院级组织（院学生会、青协、青媒、足篮排队），加分标准同校级。"
            ),
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_READONLY | wx.TE_RICH | wx.TE_MULTILINE,
        )
        the_third_lvquote_sbSizer6.Add(
            self.m_the_third_lvquote_richText1, 4, wx.ALL | wx.EXPAND, 5
        )

        left_bSizer2.Add(the_third_lvquote_sbSizer6, 3, wx.EXPAND, 5)

        main_bSizer1.Add(left_bSizer2, 1, wx.EXPAND, 5)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        picprove_area_sbSizer4 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("图片证明区")), wx.HORIZONTAL
        )

        self.m_left_prov_pic_staticText2 = wx.StaticText(
            picprove_area_sbSizer4.GetStaticBox(),
            wx.ID_ANY,
            _("<"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_left_prov_pic_staticText2.Wrap(-1)

        self.m_left_prov_pic_staticText2.SetBackgroundColour(wx.Colour(255, 255, 255))

        picprove_area_sbSizer4.Add(
            self.m_left_prov_pic_staticText2, 0, wx.ALL | wx.EXPAND, 5
        )

        # self.prove_original_image: wx.Bitmap = wx.NullBitmap
        # self.prove_drawing: bool = False
        # self.prove_last_point = None
        # self.prove_scale_factor: float = 1.0

        self.m_prov_picture_panel1 = DrawingPanel(
            picprove_area_sbSizer4.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
            "path_to_your_image.png",
        )
        picprove_area_sbSizer4.Add(self.m_prov_picture_panel1, 1, wx.EXPAND | wx.ALL, 5)

        self.m_right_prov_pic_staticText2 = wx.StaticText(
            picprove_area_sbSizer4.GetStaticBox(),
            wx.ID_ANY,
            _(">"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_right_prov_pic_staticText2.Wrap(-1)

        self.m_right_prov_pic_staticText2.SetBackgroundColour(wx.Colour(255, 255, 255))

        picprove_area_sbSizer4.Add(
            self.m_right_prov_pic_staticText2, 0, wx.ALL | wx.EXPAND, 5
        )

        bSizer3.Add(picprove_area_sbSizer4, 8, wx.EXPAND, 5)

        checker_area_sbSizer3 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("确认区")), wx.VERTICAL
        )

        bSizer7 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_disagree_button1 = wx.Button(
            checker_area_sbSizer3.GetStaticBox(),
            wx.ID_ANY,
            _("判错驳回"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        bSizer7.Add(self.m_disagree_button1, 0, wx.ALL, 5)

        self.m_score_spinCtrlDouble1 = wx.SpinCtrlDouble(
            checker_area_sbSizer3.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.ALIGN_CENTER_HORIZONTAL,
            0,
            100,
            0.000000,
            0.1,
        )
        self.m_score_spinCtrlDouble1.SetDigits(3)
        bSizer7.Add(self.m_score_spinCtrlDouble1, 1, wx.ALL | wx.EXPAND, 5)

        self.m_agree_button2 = wx.Button(
            checker_area_sbSizer3.GetStaticBox(),
            wx.ID_ANY,
            _("确认加分"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        bSizer7.Add(self.m_agree_button2, 0, wx.ALL, 5)

        checker_area_sbSizer3.Add(bSizer7, 1, wx.EXPAND, 5)

        bSizer8 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_only_select_checkBox1 = wx.CheckBox(
            checker_area_sbSizer3.GetStaticBox(),
            wx.ID_ANY,
            _("分选此图"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        bSizer8.Add(
            self.m_only_select_checkBox1,
            0,
            wx.ALL | wx.EXPAND,
            5,
        )

        self.m_need_more_checkBox2 = wx.CheckBox(
            checker_area_sbSizer3.GetStaticBox(),
            wx.ID_ANY,
            _("索求更多证明"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        bSizer8.Add(
            self.m_need_more_checkBox2,
            0,
            wx.ALL | wx.EXPAND,
            5,
        )

        self.m_has_used_staticText3 = wx.StaticText(
            checker_area_sbSizer3.GetStaticBox(),
            wx.ID_ANY,
            _("————"),
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.ST_NO_AUTORESIZE,
        )
        self.m_has_used_staticText3.Wrap(-1)
        bSizer8.Add(
            self.m_has_used_staticText3,
            0,
            wx.ALL | wx.EXPAND | wx.RESERVE_SPACE_EVEN_IF_HIDDEN,
            5,
        )

        bSizer9 = wx.BoxSizer(wx.VERTICAL)

        self.m_only_select_button4 = wx.Button(
            checker_area_sbSizer3.GetStaticBox(),
            wx.ID_ANY,
            _("分选确认"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        bSizer9.Add(self.m_only_select_button4, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        bSizer8.Add(bSizer9, 1, wx.ALL | wx.EXPAND, 0)

        checker_area_sbSizer3.Add(bSizer8, 1, wx.EXPAND, 5)

        bSizer3.Add(checker_area_sbSizer3, 1, wx.EXPAND, 5)

        main_bSizer1.Add(bSizer3, 1, wx.EXPAND, 5)

        self.SetSizer(main_bSizer1)
        self.Layout()
        self.m_statusBar1 = self.CreateStatusBar(
            1, wx.STB_ELLIPSIZE_MIDDLE | wx.STB_SHOW_TIPS | wx.STB_SIZEGRIP, wx.ID_ANY
        )

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(
            wx.EVT_MENU, self.on_open_button_pressed, id=self.m_open_menuItem1.GetId()
        )
        self.Bind(
            wx.EVT_MENU, self.on_exit_button_pressed, id=self.m_exit_menuItem2.GetId()
        )
        self.Bind(
            wx.EVT_MENU,
            self.on_continue_progress_button_pressed,
            id=self.m_progress_continue_menuItem5.GetId(),
        )
        self.Bind(
            wx.EVT_MENU,
            self.on_save_progress_button_pressed,
            id=self.m_progress_save_menuItem4.GetId(),
        )
        self.Bind(
            wx.EVT_MENU,
            self.on_progress_open_button_pressed,
            id=self.m_progress_open_menuItem3.GetId(),
        )
        self.Bind(
            wx.EVT_MENU,
            self.on_progress_saveas_button_pressed,
            id=self.m_progress_save_as_menuItem6.GetId(),
        )
        self.m_yanlun_staticText1.Bind(wx.EVT_LEFT_DCLICK, self.on_random_yanlun)
        self.m_yanlun_staticText1.Bind(wx.EVT_MOUSEWHEEL, self.on_wheel_yanlun)
        self.m_progress_save_button5.Bind(
            wx.EVT_BUTTON, self.on_save_progress_button_pressed
        )
        self.m_the_first_lvquote_choice1.Bind(
            wx.EVT_CHOICE, self.on_first_lvquote_choice
        )
        self.m_the_second_lvquote_choice2.Bind(
            wx.EVT_CHOICE, self.on_second_lvquote_choice
        )
        self.m_left_prov_pic_staticText2.Bind(
            wx.EVT_LEFT_UP, self.on_prov_pic_left_button_pressed
        )
        # self.m_prove_bitmap1.Bind(wx.EVT_CHAR, self.on_prove_pic_putchar)
        # self.m_prove_bitmap1.Bind(wx.EVT_MOTION, self.on_prove_pic_move_motion)
        # self.m_prove_bitmap1.Bind(wx.EVT_PAINT, self.on_prove_pic_paint)
        # self.m_prove_bitmap1.Bind(wx.EVT_LEFT_DOWN, self.on_prove_pic_move_start)
        # self.m_prove_bitmap1.Bind(wx.EVT_LEFT_UP, self.on_prove_pic_move_dropped)
        # self.m_prove_bitmap1.Bind(wx.EVT_MOUSEWHEEL, self.on_prove_pic_wheel)
        self.m_prov_picture_panel1.Bind(
            wx.EVT_RIGHT_DCLICK, self.on_prov_pic_right_button_pressed
        )
        self.m_right_prov_pic_staticText2.Bind(
            wx.EVT_LEFT_UP, self.on_prov_pic_right_button_pressed
        )
        self.m_disagree_button1.Bind(wx.EVT_BUTTON, self.on_disagree_button_pressed)
        self.m_score_spinCtrlDouble1.Bind(wx.EVT_MOUSEWHEEL, self.on_wheel_scores)
        self.m_score_spinCtrlDouble1.Bind(wx.EVT_TEXT_ENTER, self.on_text_entered)
        self.m_agree_button2.Bind(wx.EVT_BUTTON, self.on_agree_button_presswd)
        self.m_only_select_checkBox1.Bind(
            wx.EVT_CHECKBOX, self.on_only_select_pic_checked
        )
        self.m_need_more_checkBox2.Bind(wx.EVT_CHECKBOX, self.on_need_more_pic_checked)
        self.m_only_select_button4.Bind(
            wx.EVT_BUTTON, self.on_only_select_button_selected
        )

    def __del__(self):
        pass

    def refresh_data(
        self,
    ):
        self.m_progress_gauge1.SetRange(self.length_progress)
        self.m_progress_gauge1.SetValue(self.progress + 1)
        self.m_progress_staticText8.SetLabel(
            "{:0>3d}/{:0>3d}".format(self.progress + 1, self.length_progress)
        )

        self.m_progress_save_status_staticText81.SetLabel("✔已保存")

        self.now_person = PersonStatus(
            self.chart_zongce_data[self.progress][3],
            self.chart_zongce_data[self.progress][2],
        )
        self.m_person_info_staticText9.SetLabel(self.now_person.get_person_info())

        self.m_description_textCtrl1.SetValue(
            "客观描述证明内容：\n- 奖级：{2}\t奖次：{3}\t任职：{0}\n- 活动：{1}\n主观描述证明内容：\n\t{4}".format(
                *self.chart_zongce_data[self.progress][8:13]
            )
        )

        now_picture_list = [
            (
                self.image_path
                / (
                    _n
                    if (
                        (
                            _n := Path(
                                (
                                    i
                                    if i.startswith(
                                        self.chart_zongce_data[self.progress][0]
                                    )
                                    else self.chart_zongce_data[self.progress][0] + i
                                ).strip()
                            )
                        ).suffix.lower()
                        in (".jpg", ".png", ".jpeg")
                    )
                    else _n.with_suffix(".png")
                )
            )
            for i in self.chart_zongce_data[self.progress][13].split(
                self.chart_zongce_data[self.progress][0]
            )[1:]
        ]

        self.now_picture_list: list[tuple[Path, bool, bool]] = []
        """
        列表：
        [
            (图片路径, 是否分选, 是否已使用过),
            ...
        ]
        """
        for i in range(len(now_picture_list)):
            picture_path = now_picture_list[i]
            if (_k := now_picture_list.count(picture_path)) > 1:
                now_picture_list[i] = picture_path.with_stem(
                    picture_path.stem + "（{}）".format(_k - 1)
                )
            self.now_picture_list.append((now_picture_list[i], False, False))
        self.now_picture_list.sort(key=lambda x: x[0].name)

        logger.info("当前图片列：{}".format(self.now_picture_list))

        self.now_picture_index = 0

        self.m_prov_picture_panel1.change_image(
            str(self.now_picture_list[self.now_picture_index][0].resolve())
        )

        self.m_has_used_staticText3.SetLabel(
            "已使用" if self.now_picture_list[self.now_picture_index][2] else "————"
        )
        self.m_only_select_checkBox1.SetValue(
            self.now_picture_list[self.now_picture_index][1]
        )
        self.m_need_more_checkBox2.SetValue(False)

        if (
            self.chart_zongce_data[self.progress][4]
            in self.m_the_first_lvquote_choice1Choices
        ):
            self.m_the_first_lvquote_choice1.SetSelection(
                _n := self.m_the_first_lvquote_choice1Choices.index(
                    self.chart_zongce_data[self.progress][4]
                )
            )
            choices2 = reference_levels[self.chart_zongce_data[self.progress][4]]
            self.m_the_second_lvquote_choice2.SetItems(list(choices2.keys()))

            if self.chart_zongce_data[self.progress][5 + _n] in choices2:
                self.m_the_second_lvquote_choice2.SetSelection(
                    list(choices2.keys()).index(
                        self.chart_zongce_data[self.progress][5 + _n]
                    )
                )
            else:
                raise ValueError(
                    "未找到对应的二级指标，这写的是啥？？：\n{}".format(
                        self.chart_zongce_data[self.progress][5 + _n]
                    )
                )

            self.m_basic_max_staticText10.SetLabel(
                "基础分：{:.3f}\t满分：{:.3f}\t共用：{}".format(
                    *list(
                        choices2[self.chart_zongce_data[self.progress][5 + _n]].values()
                    )[1:]
                )
            )

            self.m_the_third_lvquote_richText1.SetValue(
                choices2[self.chart_zongce_data[self.progress][5 + _n]]["三级指标"]
            )

        else:
            self.m_the_first_lvquote_choice1.SetSelection(3)
            self.m_the_second_lvquote_choice2.SetItems(["未知二级指标"])
            self.m_basic_max_staticText10.SetLabel(
                "基础分：*.***\t满分：*.***\t共用：***"
            )
            self.m_the_third_lvquote_richText1.SetValue("请选择一级二级指标")

    # Virtual event handlers, override them in your derived class
    def on_open_button_pressed(self, event):
        fileDialog = wx.FileDialog(
            None,
            message="选择表格文件",
            defaultDir="./",
            wildcard="Excel表格文档 (*.xls;*.xlsx)|*.xls;*.xlsx",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        )
        dialogResult = fileDialog.ShowModal()
        if dialogResult == wx.ID_OK:
            logger.info("选择表格文件：{}".format(fileDialog.GetPath()))
            self.total_data = read_chart_data(fileDialog.GetPath())
            self.chart_zongce_data: list[list[str]] = self.total_data.values.tolist()  # type: ignore
            self.length_progress = len(self.chart_zongce_data)
            self.progress: int = 0
            self.image_path: Path = Path(fileDialog.GetPath()).parent / "图片"
            self.refresh_data()
        else:
            logger.info("未选择表格文件")
            wx.MessageBox("未选择文件", "取消", wx.OK | wx.ICON_WARNING)

        fileDialog.Destroy()

    def on_exit_button_pressed(self, event):
        self.Destroy()

    def on_continue_progress_button_pressed(self, event):
        self.progress = int(open("PGS.UTA", "r", encoding="utf-8").read())
        self.refresh_data()

    def on_save_progress_button_pressed(self, event):
        if self.m_progress_save_status_staticText81.GetLabel() == "✔已保存":
            open("PGS.UTA", "w", encoding="utf-8").write("{}".format(self.progress))
            wx.MessageBox("已暂存", "保存", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox(
                "当前状态下不可暂存，请确保当前页信息处理完毕",
                "取消",
                wx.OK | wx.ICON_WARNING,
            )

    def on_progress_open_button_pressed(self, event):
        event.Skip()

    def on_progress_saveas_button_pressed(self, event):
        event.Skip()

    def on_random_yanlun(self, event):
        self.yanlun_now = random.randrange(0, yanlun_length)
        self.m_yanlun_staticText1.SetLabelText(yanlun_texts[self.yanlun_now] + "\r")

    def on_wheel_yanlun(self, event):
        if event.GetWheelRotation() < 0:
            self.yanlun_now += 1
        else:
            self.yanlun_now -= 1
        self.yanlun_now += (
            -yanlun_length
            if self.yanlun_now >= yanlun_length
            else (yanlun_length if self.yanlun_now < 0 else 0)
        )
        self.m_yanlun_staticText1.SetLabelText(yanlun_texts[self.yanlun_now] + "\r")
    def on_first_lvquote_choice(self, event):

        self.m_progress_save_status_staticText81.SetLabel("❌未存储")

        if self.m_the_first_lvquote_choice1.GetSelection() == 3:
            self.m_the_first_lvquote_choice1.SetSelection(0)
            # return
            # self.m_the_second_lvquote_choice2.SetItems(["未知二级指标"])
            # self.m_basic_max_staticText10.SetLabel(
            #     "基础分：*.***\t满分：*.***\t共用：***"
            # )
            # self.m_the_third_lvquote_richText1.SetValue("请选择一级二级指标")

        choices2 = reference_levels[
            self.m_the_first_lvquote_choice1.GetStringSelection()
        ]
        self.m_the_second_lvquote_choice2.SetItems(list(choices2.keys()))
        self.m_the_second_lvquote_choice2.SetSelection(0)

        self.m_basic_max_staticText10.SetLabel(
            "基础分：{:.3f}\t满分：{:.3f}\t共用：{}".format(
                *list((_l := list(choices2.values())[0]).values())[1:]
            )
        )

        self.m_the_third_lvquote_richText1.SetValue(_l["三级指标"])

    def on_second_lvquote_choice(self, event):

        self.m_progress_save_status_staticText81.SetLabel("❌未存储")

        choice = reference_levels[
            self.m_the_first_lvquote_choice1.GetStringSelection()
        ][self.m_the_second_lvquote_choice2.GetStringSelection()]

        self.m_basic_max_staticText10.SetLabel(
            "基础分：{:.3f}\t满分：{:.3f}\t共用：{}".format(*list(choice.values())[1:])
        )

        self.m_the_third_lvquote_richText1.SetValue(choice["三级指标"])

    def on_prov_pic_left_button_pressed(self, event):
        self.now_picture_index = (self.now_picture_index - 1) % len(
            self.now_picture_list
        )
        logger.info(
            "图片切换：{}\n\t{}".format(
                self.now_picture_index, self.now_picture_list[self.now_picture_index]
            )
        )
        self.m_prov_picture_panel1.change_image(
            str(self.now_picture_list[self.now_picture_index][0].resolve()),
        )
        self.m_only_select_checkBox1.SetValue(
            self.now_picture_list[self.now_picture_index][1]
        )
        self.m_has_used_staticText3.SetLabel(
            "已使用" if self.now_picture_list[self.now_picture_index][2] else "————"
        )

    def on_prove_pic_putchar(self, event):
        event.Skip()

    # def on_prove_pic_move_motion(self, event):
    #     if not self.prove_drawing:
    #         return
    #     dc = wx.ClientDC(self.m_prove_bitmap1)
    #     dc.SetPen(wx.Pen("red", 2))
    #     dc.DrawLine(self.prove_last_point, event.GetPosition())
    #     self.update_drawing(event.GetPosition())
    #     self.prove_last_point = event.GetPosition()

    # def update_drawing(self, position):
    #     mem_dc = wx.MemoryDC(self.m_prove_bitmap1.GetBitmap())
    #     mem_dc.SetPen(wx.Pen("red", 2))
    #     mem_dc.DrawLine(self.prove_last_point, position)
    #     self.m_prove_bitmap1.SetBitmap(mem_dc.GetAsBitmap())
    #     del mem_dc

    # def on_prove_pic_paint(self, event):
    #     dc = wx.BufferedPaintDC(self.m_prove_bitmap1)
    #     dc.Clear()
    #     # wx.Bitmap().Rescale
    #     scaled_image = (
    #         self.m_prove_bitmap1.GetBitmap()
    #         .ConvertToImage()
    #         .Scale(
    #             int(self.prove_original_image.GetWidth() * self.prove_scale_factor),
    #             int(self.prove_original_image.GetHeight() * self.prove_scale_factor),
    #             quality=wx.IMAGE_QUALITY_HIGH,
    #         )
    #     )
    #     dc.DrawBitmap(scaled_image.ConvertToBitmap(), 0, 0)

    def on_prove_pic_move_start(self, event):
        event.Skip()
        # self.prove_drawing = True
        # self.prove_last_point = event.GetPosition()

    def on_prove_pic_move_dropped(self, event):
        event.Skip()
        # self.prove_drawing = False
        # self.prove_last_point = None

    def on_prove_pic_wheel(self, event):
        event.Skip()
        # rotation = event.GetWheelRotation()
        # if rotation > 0:
        #     self.scale_factor *= 1.1
        # elif rotation < 0:
        #     self.scale_factor /= 1.1
        # self.Refresh()

    def on_prov_pic_right_button_pressed(self, event):
        self.now_picture_index = (self.now_picture_index + 1) % len(
            self.now_picture_list
        )
        logger.info(
            "图片切换：{}\n\t{}".format(
                self.now_picture_index, self.now_picture_list[self.now_picture_index]
            )
        )
        self.m_prov_picture_panel1.change_image(
            str(self.now_picture_list[self.now_picture_index][0].resolve()),
        )
        self.m_only_select_checkBox1.SetValue(
            self.now_picture_list[self.now_picture_index][1]
        )
        self.m_has_used_staticText3.SetLabel(
            "已使用" if self.now_picture_list[self.now_picture_index][2] else "————"
        )

        # event.Skip()

    def get_description_rec(
        self,
    ) -> str:
        return (
            self.m_description_textCtrl1.GetValue()
            .split("\n\t")[1]
            .replace("\n", "=")
            .replace('"', "=")
            .replace("+", "=")
            .replace("\\", "=")
            .replace("/", "=")
            .replace(":", "=")
            .replace("*", "=")
            .replace("?", "=")
            .replace("<", "=")
            .replace(">", "=")
            .replace("|", "=")
        )

    def move_picture_to(
        self,
        destination_folder_path: Path,
        get_choice: bool = True,
        all_picture: bool = True,
    ):
        if not destination_folder_path.exists():
            destination_folder_path.mkdir(parents=True, exist_ok=True)

        self.m_prov_picture_panel1.save_image()

        rec_name = Path(self.get_description_rec())

        # pic_need_to_move = [i for i in self.now_picture_list if all_picture or i[1]]

        # if len(pic_need_to_move) == len(self.now_picture_list):
        #     all_picture = True
        used_count = 0

        for i in range(len(self.now_picture_list)):
            # picture_path.rename(destination_folder_path / picture_path.name)
            if all_picture or self.now_picture_list[i][1]:
                shutil.copy(
                    self.now_picture_list[i][0],
                    destination_folder_path
                    / (
                        _m := "{}_{}_{}-{}.png".format(
                            (
                                self.m_the_first_lvquote_choice1.GetStringSelection()
                                if get_choice
                                else self.now_person.get_name()
                            ),
                            (
                                self.m_the_second_lvquote_choice2.GetStringSelection()
                                if get_choice
                                else self.now_picture_list[i][0].stem
                            ),
                            rec_name,
                            i,
                        )
                    ),
                )
                self.now_picture_list[i] = (
                    self.now_picture_list[i][0],
                    False,
                    True,
                )

                logger.info("图片移动至：{}".format(_m))
                # if not all_picture:
                #     self.now_picture_list.remove(pic_need_to_move[i])

                yield _m

            if self.now_picture_list[i][2]:
                used_count += 1

        if used_count == len(self.now_picture_list):
            self.progress += 1
            self.refresh_data()

        # if not all_picture:
        #     self.now_picture_index = 0
        #     self.m_prov_picture_panel1.change_image(
        #         str(self.now_picture_list[self.now_picture_index][0].resolve()),
        #     )

    def on_disagree_button_pressed(self, event):

        # "|".join(self.move_picture_to(self.now_person.get_store_path() / "#错误"))

        error_result_csv.open("a", encoding="gbk").write(
            "{id}, {name}, {desc}, {pics}\n".format(
                id=self.now_person.get_id(),
                name=self.now_person.get_name(),
                desc=self.get_description_rec(),
                pics="|".join(
                    self.move_picture_to(
                        self.now_person.get_store_path() / "#错误", False, True
                    )
                ),
            )
        )
        # self.progress += 1
        # self.refresh_data()

    def on_wheel_scores(self, event):
        self.m_progress_save_status_staticText81.SetLabel("❌未存储")
        if event.GetWheelRotation() < 0:
            self.m_score_spinCtrlDouble1.SetValue(
                self.m_score_spinCtrlDouble1.GetValue() - 0.01
            )
        else:
            self.m_score_spinCtrlDouble1.SetValue(
                self.m_score_spinCtrlDouble1.GetValue() + 0.01
            )

    def on_text_entered(self, event):
        self.m_progress_save_status_staticText81.SetLabel("❌未存储")
        event.Skip()

    def on_agree_button_presswd(self, event):
        # 学号,姓名,一级指标,二级指标,基础分,满分,描述,加分,证明备注,证明
        true_result_csv.open("a", encoding="gbk").write(
            "{id}, {name}, {lv1}, {lv2}, {base}, {max_s}, {desc}, {add_s}, {req_m}, {pics}\n".format(
                id=self.now_person.get_id(),
                name=self.now_person.get_name(),
                lv1=self.m_the_first_lvquote_choice1.GetStringSelection(),
                lv2=self.m_the_second_lvquote_choice2.GetStringSelection(),
                base=reference_levels[
                    self.m_the_first_lvquote_choice1.GetStringSelection()
                ][self.m_the_second_lvquote_choice2.GetStringSelection()]["基础分"],
                max_s=reference_levels[
                    self.m_the_first_lvquote_choice1.GetStringSelection()
                ][self.m_the_second_lvquote_choice2.GetStringSelection()]["满分"],
                desc=self.get_description_rec(),
                add_s=self.m_score_spinCtrlDouble1.GetValue(),
                req_m="需要更多证明" if self.m_need_more_checkBox2.GetValue() else "",
                pics="|".join(
                    self.move_picture_to(self.now_person.get_store_path(), True, True)
                ),
            )
        )

        # self.progress += 1
        # self.refresh_data()
        # event.Skip()

    def on_only_select_pic_checked(self, event):
        self.m_progress_save_status_staticText81.SetLabel("❌未存储")
        self.now_picture_list[self.now_picture_index] = (
            self.now_picture_list[self.now_picture_index][0],
            self.m_only_select_checkBox1.GetValue(),
            self.now_picture_list[self.now_picture_index][2],
        )
        logger.info(
            "修改图片分选属性：{}".format(self.now_picture_list[self.now_picture_index])
        )

    def on_need_more_pic_checked(self, event):
        self.m_progress_save_status_staticText81.SetLabel("❌未存储")
        event.Skip()

    def on_only_select_button_selected(self, event):
        if _m := "|".join(
            self.move_picture_to(self.now_person.get_store_path(), True, False)
        ):
            self.m_progress_save_status_staticText81.SetLabel("❌未存储")
            true_result_csv.open("a", encoding="gbk").write(
                "{id}, {name}, {lv1}, {lv2}, {base}, {max_s}, {desc}, {add_s}, {req_m}, {pics}\n".format(
                    id=self.now_person.get_id(),
                    name=self.now_person.get_name(),
                    lv1=self.m_the_first_lvquote_choice1.GetStringSelection(),
                    lv2=self.m_the_second_lvquote_choice2.GetStringSelection(),
                    base=reference_levels[
                        self.m_the_first_lvquote_choice1.GetStringSelection()
                    ][self.m_the_second_lvquote_choice2.GetStringSelection()]["基础分"],
                    max_s=reference_levels[
                        self.m_the_first_lvquote_choice1.GetStringSelection()
                    ][self.m_the_second_lvquote_choice2.GetStringSelection()]["满分"],
                    desc=self.get_description_rec(),
                    add_s=self.m_score_spinCtrlDouble1.GetValue(),
                    req_m=(
                        "需要更多证明" if self.m_need_more_checkBox2.GetValue() else ""
                    ),
                    pics=_m,
                )
            )
        else:
            wx.MessageDialog(
                self,
                "未选择证明图片",
                "警告",
                wx.OK | wx.ICON_QUESTION,
            ).ShowModal()
        self.m_has_used_staticText3.SetLabel(
            "已使用" if self.now_picture_list[self.now_picture_index][2] else "————"
        )
        self.m_only_select_checkBox1.SetValue(
            self.now_picture_list[self.now_picture_index][1]
        )


logger.info("加载应用界面……")


# 创建应用程序类
class UniTestApp(wx.App):
    def OnInit(self):
        # 创建主窗口
        self.SetAppName(__appname__)
        self.frame = MainFrame(
            None,
        )
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


# 启动应用程序
if __name__ == "__main__":

    logger.info("开启窗口")

    app = UniTestApp()

    app.MainLoop()
