from importall import *
class BaseMainWindow(FluentWindow):
    """
    主窗口基类，用来定义一些通用的方法，如切换主题、切换深色模式、切换图标、快捷键等。
    """
    def __init__(self):
        super().__init__()
        self.initializationfirst()

    def read_qrcpath(self,alias):
        resource_path = f":/{alias}"  # 资源路径前缀
        resource = QResource(resource_path)
        
        if resource.isValid():
            file = QFile(resource_path)
            if file.open(QIODevice.ReadOnly):
                content = file.readAll().data().decode()
                file.close()
                return content
            else:
                raise FileNotFoundError(f"无法打开资源文件 {resource_path}")
        else:
            raise FileNotFoundError(f"资源 {resource_path} 无效")

    def initializationfirst(self):
        # 创建一个字典，将中文天气名称与对应的英文文件名匹配
        self.WeatherIconDictionary = {
            '太阳': 'WeatherIconSun',
            '雪天': 'WeatherIconSnowy',
            '雷雨': 'WeatherIconThunderstorm',
            '月亮': 'WeatherIconMoon'
        }
        
        # 使用字典来简化资源读取过程
        for Chinese, alias in self.WeatherIconDictionary.items():
            setattr(self, alias, self.read_qrcpath(f"src/{alias}").strip("\n"))

    def keyPressEvent(self, event):
        # 检测是否同时按下Ctrl键
        if event.modifiers() & Qt.ControlModifier:
            # 检测是否按下特定的键
            if event.key() == 44:  # 使用Qt.Key枚举值代替直接的键码
                self.api.上一个文件()
            elif event.key() == 46:
                self.api.下一个文件()
            elif event.key() == Qt.Key_S:  # S键，save
                self.api.保存函数()
            elif event.key() == Qt.Key_R:  # R键，refresh，刷新遮罩
                self.api.显示遮罩流程()
            elif event.key() == Qt.Key_O:  # O键，output，显示原始参考图
                self.api.保存修改过后的数据函数()
            elif event.key() == Qt.Key_L:  # L键，隐藏遮罩对应的参考图
                self.api.根据遮罩数组显示参考图()
            elif event.key() == Qt.Key_P:  # P键，预处理
                self.api.预处理程序启动()
            elif event.key() == Qt.Key_X:  # Y键，清空遮罩
                self.api.消除遮罩函数()
            elif event.key() == Qt.Key_D:  # D键，显示原始数组参考图
                self.api.显示原始数组参考图()
            elif event.key() == Qt.Key_F:  # F键，一次性刷新遮罩
                self.api.刷新按钮()
            elif event.key() == Qt.Key_G:  # G键，加载上一次保存的文件
                self.api.加载上一个保存的文件()
            elif event.key() == Qt.Key_I:  # I键，校准参考十字位置
                self.api.绑定校准函数()
            elif event.key() == Qt.Key_T:  # T键，显示消除遮罩之后的参考图
                self.api.根据遮罩数组显示参考图()
            elif event.key() == Qt.Key_U:  # U键，显示遮罩对应的参考图
                self.api.显示消息框函数("warning", "即将进行边缘提取", "这个功能需要等待很长时间，计算量很大", "底部")
                QTimer.singleShot(100, self.api.边缘提取显示参考图)
        else:
            super().keyPressEvent(event)

    def SwitchDepthMode(self,chacked):
        WebContainer = self.api.webviewsall
        if chacked:
            setTheme(Theme.DARK)
            # 设置背景色为黑色
            self.setStyleSheet("background-color: #000000;")
            for i in WebContainer:
                try:
                    i.page().runJavaScript("try { toggleNightMode(true); } catch (error) { }")
                except:pass

        else:
            setTheme(Theme.LIGHT)
            # 删除背景颜色
            self.setStyleSheet("background-color: #ffffff;")
            for i in WebContainer:
                try:
                    i.page().runJavaScript("try { toggleNightMode(false); } catch (error) { }")
                except:pass
    def SwitchThemeColor(self,color):
        setThemeColor(color)

    def ToggleIcon(self,base64_str):
        """
        从 Base64 编码的字符串加载 QIcon。
        """
        # 获取对应的类属性值，还要转化一下
        base64_data = getattr(self,self.WeatherIconDictionary[base64_str])
        # 解码 Base64 数据
        image_data = base64.b64decode(base64_data)
        
        # 使用 QImage 加载图像数据
        image = QImage()
        image.loadFromData(image_data, "PNG")
        
        # 将 QImage 转换为 QPixmap
        pixmap = QPixmap.fromImage(image)
        
        # 创建 QIcon
        icon = QIcon(pixmap)
        
        self.setWindowIcon(icon)





