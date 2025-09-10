import wx


class DrawingPanel(wx.Panel):
    def __init__(self, parent, image_path):
        super(DrawingPanel, self).__init__(parent)

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
        dc.SetPen(wx.Pen("red", 2))
        dc.DrawLine(self.last_point, event.GetPosition())
        self.update_drawing(event.GetPosition())
        self.last_point = event.GetPosition()

    def update_drawing(self, position):
        mem_dc = wx.MemoryDC(self.image.ConvertToBitmap())
        mem_dc.SetPen(wx.Pen("red", 2))
        mem_dc.DrawLine(self.last_point, position)
        self.image = mem_dc.GetAsBitmap().ConvertToImage()
        del mem_dc

    def on_mouse_wheel(self, event):
        rotation = event.GetWheelRotation()
        if rotation > 0:
            self.scale_factor *= 1.1
        elif rotation < 0:
            self.scale_factor /= 1.1
        self.Refresh()

    def save_image(self, path):
        self.image.SaveFile(path, wx.BITMAP_TYPE_PNG)


class MainFrame(wx.Frame):
    def __init__(self, title, image_path):
        super(MainFrame, self).__init__(None, title=title, size=(800, 600))

        panel = DrawingPanel(self, image_path)

        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        save_item = file_menu.Append(wx.ID_SAVE, "保存图片", "保存已编辑的图片")
        self.Bind(wx.EVT_MENU, self.on_save_image, save_item)
        menu_bar.Append(file_menu, "&File")

        self.SetMenuBar(menu_bar)

    def on_save_image(self, event):
        with wx.FileDialog(
            self,
            "保存",
            wildcard="PNG files (*.png)|*.png",
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        ) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = file_dialog.GetPath()
            panel = self.Children[0]
            panel.save_image(pathname)


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame("绘图测试", "path_to_your_image.png")
    frame.Show(True)
    app.MainLoop()
