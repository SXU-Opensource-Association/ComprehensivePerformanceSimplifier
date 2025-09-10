# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.richtext

import gettext
_ = gettext.gettext

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"综测评价简化应用"), pos = wx.DefaultPosition, size = wx.Size( 1400,900 ), style = wx.CAPTION|wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL|wx.TRANSPARENT_WINDOW, name = u"untestapp_window" )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 240, 240, 240 ) )

        self.m_menubar1 = wx.MenuBar( 0 )
        self.m_file_menu1 = wx.Menu()
        self.m_open_menuItem1 = wx.MenuItem( self.m_file_menu1, wx.ID_ANY, _(u"打开"), _(u"打开导入的Excel文件所在位置"), wx.ITEM_NORMAL )
        self.m_file_menu1.Append( self.m_open_menuItem1 )

        self.m_exit_menuItem2 = wx.MenuItem( self.m_file_menu1, wx.ID_ANY, _(u"退出"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_file_menu1.Append( self.m_exit_menuItem2 )

        self.m_menubar1.Append( self.m_file_menu1, _(u"文件") )

        self.m_progress_menu3 = wx.Menu()
        self.m_progress_continue_menuItem5 = wx.MenuItem( self.m_progress_menu3, wx.ID_ANY, _(u"接续进度"), _(u"直接读取评分进度"), wx.ITEM_NORMAL )
        self.m_progress_menu3.Append( self.m_progress_continue_menuItem5 )

        self.m_progress_save_menuItem4 = wx.MenuItem( self.m_progress_menu3, wx.ID_ANY, _(u"进度暂存"), _(u"临时存储评分进度"), wx.ITEM_NORMAL )
        self.m_progress_menu3.Append( self.m_progress_save_menuItem4 )

        self.m_progress_menu3.AppendSeparator()

        self.m_progress_open_menuItem3 = wx.MenuItem( self.m_progress_menu3, wx.ID_ANY, _(u"打开进度"), _(u"打开存储的进度文件"), wx.ITEM_NORMAL )
        self.m_progress_menu3.Append( self.m_progress_open_menuItem3 )

        self.m_progress_save_as_menuItem6 = wx.MenuItem( self.m_progress_menu3, wx.ID_ANY, _(u"进度另存"), _(u"将进度文件存储在非默认位置"), wx.ITEM_NORMAL )
        self.m_progress_menu3.Append( self.m_progress_save_as_menuItem6 )

        self.m_menubar1.Append( self.m_progress_menu3, _(u"进度") )

        self.SetMenuBar( self.m_menubar1 )

        main_bSizer1 = wx.BoxSizer( wx.HORIZONTAL )

        left_bSizer2 = wx.BoxSizer( wx.VERTICAL )

        yanlun_sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"言·论") ), wx.VERTICAL )

        self.m_yanlun_staticText1 = wx.StaticText( yanlun_sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"综测评分简化系统"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_ELLIPSIZE_MIDDLE )
        self.m_yanlun_staticText1.Wrap( -1 )

        self.m_yanlun_staticText1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )
        self.m_yanlun_staticText1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

        yanlun_sbSizer2.Add( self.m_yanlun_staticText1, 0, wx.ALL|wx.EXPAND, 5 )


        left_bSizer2.Add( yanlun_sbSizer2, 0, wx.EXPAND, 5 )

        bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, _(u"完成进度"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )

        bSizer4.Add( self.m_staticText7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_progress_gauge1 = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL|wx.GA_SMOOTH )
        self.m_progress_gauge1.SetValue( 0 )
        bSizer4.Add( self.m_progress_gauge1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )

        self.m_progress_staticText8 = wx.StaticText( self, wx.ID_ANY, _(u"1/120"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_progress_staticText8.Wrap( -1 )

        bSizer4.Add( self.m_progress_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_progress_save_button5 = wx.Button( self, wx.ID_ANY, _(u"进度暂存"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer4.Add( self.m_progress_save_button5, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        left_bSizer2.Add( bSizer4, 0, wx.EXPAND, 5 )

        info_sbSizer5 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"信息展示区") ), wx.VERTICAL )

        self.m_staticText9 = wx.StaticText( info_sbSizer5.GetStaticBox(), wx.ID_ANY, _(u"姓名：祁元辉\t学号：202400101100\t验证：成功"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )

        info_sbSizer5.Add( self.m_staticText9, 0, wx.ALL|wx.EXPAND, 5 )

        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText10 = wx.StaticText( info_sbSizer5.GetStaticBox(), wx.ID_ANY, _(u"证明所属一级指标"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )

        bSizer5.Add( self.m_staticText10, 0, wx.ALL, 5 )

        m_the_first_lvquote_choice1Choices = [ _(u"思想政治道德素质"), _(u"身心素质"), _(u"创造精神和实践能力"), _(u"未知一级指标"), wx.EmptyString, wx.EmptyString ]
        self.m_the_first_lvquote_choice1 = wx.Choice( info_sbSizer5.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_the_first_lvquote_choice1Choices, 0 )
        self.m_the_first_lvquote_choice1.SetSelection( 0 )
        bSizer5.Add( self.m_the_first_lvquote_choice1, 1, wx.ALL, 5 )


        info_sbSizer5.Add( bSizer5, 0, wx.EXPAND, 5 )

        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText101 = wx.StaticText( info_sbSizer5.GetStaticBox(), wx.ID_ANY, _(u"证明所属二级指标"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText101.Wrap( -1 )

        bSizer6.Add( self.m_staticText101, 0, wx.ALL, 5 )

        m_the_second_lvquote_choice2Choices = [ _(u"思想政治道德素质"), _(u"身心素质"), _(u"创造精神和实践能力"), _(u"未知一级指标"), wx.EmptyString, wx.EmptyString ]
        self.m_the_second_lvquote_choice2 = wx.Choice( info_sbSizer5.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_the_second_lvquote_choice2Choices, 0 )
        self.m_the_second_lvquote_choice2.SetSelection( 0 )
        bSizer6.Add( self.m_the_second_lvquote_choice2, 1, wx.ALL, 5 )


        info_sbSizer5.Add( bSizer6, 0, wx.EXPAND, 5 )

        self.m_description_textCtrl1 = wx.TextCtrl( info_sbSizer5.GetStaticBox(), wx.ID_ANY, _(u"客观描述证明内容：\n - 奖级：校级\t奖次：参与奖\t任职：个人\n - 活动：北昌大学第零届“你好世界，一二三四”啊这什么大赛啥学院初赛\n主观描述证明内容：\n北昌大学第零届“你好世界，一二三四”啊这什么大赛啥学院初赛参与奖"), wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH )
        info_sbSizer5.Add( self.m_description_textCtrl1, 1, wx.ALL|wx.EXPAND, 5 )


        left_bSizer2.Add( info_sbSizer5, 0, wx.EXPAND, 5 )

        the_third_lvquote_sbSizer6 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"三级指标参考") ), wx.VERTICAL )

        self.m_richText1 = wx.richtext.RichTextCtrl( the_third_lvquote_sbSizer6.GetStaticBox(), wx.ID_ANY, _(u"请注意：以下各个职位若有兼任皆不累加，取最高分。\n班委成员中，班长、团支书、学委加1分；其他班委加0.5分；舍长加0.2分。\n校级组织中（校学生会、校报、广播站、电视台、社联），主席团加1分，部长加0.5分，副部长加0.4分，优秀干事加0.2分（取消，对于优秀干事/部门之星等表彰的加分移入【集体观念、合作意识（活动）】，即学期内可多次评选累加），干事0.1分。\n社团负责人加0.3，不累加。（这里加分的后面参加社团的0.1就不加了）\n辩论队：教练0.5、负责人0.4、最佳辩手0.2（取消，对于最佳辩手的加分移入【创造精神和创新能力】指标）、队员0.1\n足篮排等各类队伍：队长0.4，副队长0.3，其他负责（财务、副队长）0.2，队员0.1\n院级组织（院学生会、青协、青媒、足篮排队），加分标准同上。"), wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
        the_third_lvquote_sbSizer6.Add( self.m_richText1, 5, wx.ALL|wx.EXPAND, 5 )


        left_bSizer2.Add( the_third_lvquote_sbSizer6, 3, wx.EXPAND, 5 )


        main_bSizer1.Add( left_bSizer2, 1, wx.EXPAND, 5 )

        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        picprove_area_sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"图片证明区") ), wx.HORIZONTAL )

        self.m_left_prov_pic_staticText2 = wx.StaticText( picprove_area_sbSizer4.GetStaticBox(), wx.ID_ANY, _(u"<"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_left_prov_pic_staticText2.Wrap( -1 )

        self.m_left_prov_pic_staticText2.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )

        picprove_area_sbSizer4.Add( self.m_left_prov_pic_staticText2, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_prove_bitmap1 = wx.StaticBitmap( picprove_area_sbSizer4.GetStaticBox(), wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        picprove_area_sbSizer4.Add( self.m_prove_bitmap1, 5, wx.ALL|wx.EXPAND, 5 )

        self.m_right_prov_pic_staticText2 = wx.StaticText( picprove_area_sbSizer4.GetStaticBox(), wx.ID_ANY, _(u">"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_right_prov_pic_staticText2.Wrap( -1 )

        self.m_right_prov_pic_staticText2.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )

        picprove_area_sbSizer4.Add( self.m_right_prov_pic_staticText2, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer3.Add( picprove_area_sbSizer4, 8, wx.EXPAND, 5 )

        checker_area_sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"确认区") ), wx.HORIZONTAL )

        self.m_disagree_button1 = wx.Button( checker_area_sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"判错驳回"), wx.DefaultPosition, wx.DefaultSize, 0 )
        checker_area_sbSizer3.Add( self.m_disagree_button1, 1, wx.ALL, 5 )

        self.m_score_spinCtrlDouble1 = wx.SpinCtrlDouble( checker_area_sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL, 0, 100, 0.000000, 0.1 )
        self.m_score_spinCtrlDouble1.SetDigits( 3 )
        checker_area_sbSizer3.Add( self.m_score_spinCtrlDouble1, 2, wx.ALL, 5 )

        self.m_agree_button2 = wx.Button( checker_area_sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"确认"), wx.DefaultPosition, wx.DefaultSize, 0 )
        checker_area_sbSizer3.Add( self.m_agree_button2, 1, wx.ALL, 5 )


        bSizer3.Add( checker_area_sbSizer3, 1, wx.EXPAND, 5 )


        main_bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )


        self.SetSizer( main_bSizer1 )
        self.Layout()
        self.m_statusBar1 = self.CreateStatusBar( 1, wx.STB_ELLIPSIZE_MIDDLE|wx.STB_SHOW_TIPS|wx.STB_SIZEGRIP, wx.ID_ANY )

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_MENU, self.on_open_button_pressed, id = self.m_open_menuItem1.GetId() )
        self.Bind( wx.EVT_MENU, self.on_exit_button_pressed, id = self.m_exit_menuItem2.GetId() )
        self.Bind( wx.EVT_MENU, self.on_continue_progress_button_pressed, id = self.m_progress_continue_menuItem5.GetId() )
        self.Bind( wx.EVT_MENU, self.on_save_progress_button_pressed, id = self.m_progress_save_menuItem4.GetId() )
        self.Bind( wx.EVT_MENU, self.on_progress_open_button_pressed, id = self.m_progress_open_menuItem3.GetId() )
        self.Bind( wx.EVT_MENU, self.on_progress_saveas_button_pressed, id = self.m_progress_save_as_menuItem6.GetId() )
        self.m_yanlun_staticText1.Bind( wx.EVT_LEFT_DCLICK, self.on_random_yanlun )
        self.m_yanlun_staticText1.Bind( wx.EVT_MOUSEWHEEL, self.on_wheel_yanlun )
        self.m_progress_save_button5.Bind( wx.EVT_BUTTON, self.on_progress_save_button_pressed )
        self.m_the_first_lvquote_choice1.Bind( wx.EVT_CHOICE, self.on_first_lvquote_choice )
        self.m_the_second_lvquote_choice2.Bind( wx.EVT_CHOICE, self.on_second_lvquote_choice )
        self.m_left_prov_pic_staticText2.Bind( wx.EVT_LEFT_UP, self.on_prov_pic_left_button_pressed )
        self.m_prove_bitmap1.Bind( wx.EVT_CHAR, self.on_prove_pic_putchar )
        self.m_prove_bitmap1.Bind( wx.EVT_LEFT_DOWN, self.on_prove_pic_move_start )
        self.m_prove_bitmap1.Bind( wx.EVT_LEFT_UP, self.on_prove_pic_move_dropped )
        self.m_prove_bitmap1.Bind( wx.EVT_MOUSEWHEEL, self.on_prove_pic_wheel )
        self.m_right_prov_pic_staticText2.Bind( wx.EVT_LEFT_UP, self.on_prov_pic_right_button_pressed )
        self.m_disagree_button1.Bind( wx.EVT_BUTTON, self.on_disagree_button_pressed )
        self.m_score_spinCtrlDouble1.Bind( wx.EVT_TEXT_ENTER, self.on_text_entered )
        self.m_agree_button2.Bind( wx.EVT_BUTTON, self.on_agree_button_presswd )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def on_open_button_pressed( self, event ):
        event.Skip()

    def on_exit_button_pressed( self, event ):
        event.Skip()

    def on_continue_progress_button_pressed( self, event ):
        event.Skip()

    def on_save_progress_button_pressed( self, event ):
        event.Skip()

    def on_progress_open_button_pressed( self, event ):
        event.Skip()

    def on_progress_saveas_button_pressed( self, event ):
        event.Skip()

    def on_random_yanlun( self, event ):
        event.Skip()

    def on_wheel_yanlun( self, event ):
        event.Skip()

    def on_progress_save_button_pressed( self, event ):
        event.Skip()

    def on_first_lvquote_choice( self, event ):
        event.Skip()

    def on_second_lvquote_choice( self, event ):
        event.Skip()

    def on_prov_pic_left_button_pressed( self, event ):
        event.Skip()

    def on_prove_pic_putchar( self, event ):
        event.Skip()

    def on_prove_pic_move_start( self, event ):
        event.Skip()

    def on_prove_pic_move_dropped( self, event ):
        event.Skip()

    def on_prove_pic_wheel( self, event ):
        event.Skip()

    def on_prov_pic_right_button_pressed( self, event ):
        event.Skip()

    def on_disagree_button_pressed( self, event ):
        event.Skip()

    def on_text_entered( self, event ):
        event.Skip()

    def on_agree_button_presswd( self, event ):
        event.Skip()


