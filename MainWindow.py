from importall import *
from MainWidget.DataAnnotationWidget import DataAnnotation
from MainWidget.Functions import FunctionsAll
from MainWidget.SettingWidget import SettingWidget
from MainWidget.BaseMainWindow import BaseMainWindow

class MainWindow(BaseMainWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__()
        self.initialization()
        self.initWindow()
        self.SwitchDepthMode(self.api.是否开启夜间模式)
        self.SwitchThemeColor(self.api.软件主题色)
        self.show()

    def initialization(self):
        """ 初始化界面 """
        self.ui = DataAnnotation()
        self.ui.setupUi(self)

        self.api = FunctionsAll(self)
        self.api.Initialize_Connects(self)
        self.settingInterface = SettingWidget('设置界面', self)

        self.addSubInterface(self.ui.widget, FIF.HOME, '数据标注界面')
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置界面', NavigationItemPosition.BOTTOM)


    def initWindow(self):
        app = QCoreApplication.instance()

        # 获取屏幕的尺寸
        screen = app.primaryScreen().size()
        width = screen.width() * 0.9
        height = screen.height() * 0.9

        # 设置窗口大小
        self.resize(width, height)
        self.setWindowTitle('数组数据标注及后续处理小工具')
        self.ToggleIcon(self.api.软件图标)

        # 使窗口可以拖动改变大小
        self.setWindowFlags(self.windowFlags() | Qt.Window)

        # 计算屏幕中心位置并移动窗口
        screen = QApplication.primaryScreen().geometry()
        window_center_x = (screen.width() - self.width()) // 2
        window_center_y = (screen.height() - self.height()) // 2
        self.move(window_center_x, window_center_y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec()

