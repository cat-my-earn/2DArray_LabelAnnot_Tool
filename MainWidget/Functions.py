

#%%

from importall import *
from LittleCards.ProgressBar import ProgressFlyoutView
from MainWidget.BredgeToWebView import Bridge,CustomWebEnginePage
from MainWidget.ConfigClass import MyConfig
from LittleCards.LittleMessageBox import CustomMessageBox
from LittleCards.Basic_Matpainter import matpainter

class FunctionsAll:
    """
    实打实的屎山代码，数据处理相关的方法全定义在这了。
    """
    def __init__(self, ui):
        self.Main = ui
        self.ui = ui.ui

        # 设置全局配置文件项
        self.Main.cfg = MyConfig()
        # 是否存在配置文件，如果不存在则创建
        qconfig.load(r'配置文件.json', self.Main.cfg)

        properties = {
            '文件夹路径': self.Main.cfg.文件夹路径,
            '正在使用的文件名字': self.Main.cfg.正在使用的文件名字,
            '当前使用的文件路径': self.Main.cfg.当前使用的文件路径,
            '正在使用的文件索引': self.Main.cfg.正在使用的文件索引,
            '正在使用的页数': self.Main.cfg.正在使用的页数,
            '是否需要完整报错信息': self.Main.cfg.是否需要完整报错信息,
            '是否需要规整数据': self.Main.cfg.是否需要规整数据,
            '是否默认预处理': self.Main.cfg.是否默认预处理,
            '图像类型对应的源文件的key': self.Main.cfg.图像类型对应的源文件的key,
            '图像类型对应自定义色标': self.Main.cfg.图像类型对应自定义色标,
            '文件保存路径': self.Main.cfg.文件保存路径,
            '预处理代码': self.Main.cfg.预处理代码,
            '上一个处理的文件路径': self.Main.cfg.上一个处理的文件路径,
            '是否加载参考图': self.Main.cfg.是否加载参考图,
            '是否自动显示遮罩': self.Main.cfg.是否自动显示遮罩,
            '图像类型对应的不同对象的选择数值': self.Main.cfg.图像类型对应的不同对象的选择数值,
            '图像类型对应的不同对象的选择颜色': self.Main.cfg.图像类型对应的不同对象的选择颜色,
            'X坐标基础值': self.Main.cfg.X坐标基础值,
            'Y坐标基础值': self.Main.cfg.Y坐标基础值,
            'X坐标偏移倍率': self.Main.cfg.X坐标偏移倍率,
            'Y坐标偏移倍率': self.Main.cfg.Y坐标偏移倍率,
            '圆心基础X坐标': self.Main.cfg.圆心基础X坐标,
            '圆心基础Y坐标': self.Main.cfg.圆心基础Y坐标,
            '半径偏移倍率': self.Main.cfg.半径偏移倍率,
            '直角坐标基础宽度': self.Main.cfg.直角坐标基础宽度,
            '直角坐标基础高度': self.Main.cfg.直角坐标基础高度,
            '极坐标基础半径': self.Main.cfg.极坐标基础半径,
            '圆心偏移X坐标': self.Main.cfg.圆心偏移X坐标,
            '圆心偏移Y坐标': self.Main.cfg.圆心偏移Y坐标,
            '是否每绘制一步都刷新遮罩': self.Main.cfg.是否每绘制一步都刷新遮罩,
            '自定义绘图函数': self.Main.cfg.自定义绘图函数,
            '自定义绘图函数能不能用': self.Main.cfg.自定义绘图函数能不能用,
            '边缘提取的核大小': self.Main.cfg.边缘提取的核大小,
            '边缘提取的阈值': self.Main.cfg.边缘提取的阈值,
            '边缘提取的形态学核大小': self.Main.cfg.边缘提取的形态学核大小,
            '边缘提取的描线宽度': self.Main.cfg.边缘提取的描线宽度,
            '边缘提取的扩展像素': self.Main.cfg.边缘提取的扩展像素,
            '批量输出图片时根据图片类型分类': self.Main.cfg.批量输出图片时根据图片类型分类,
            '是否要渲染没有蒙版的文件': self.Main.cfg.是否要渲染没有蒙版的文件,
            '上一个文件的文件路径': self.Main.cfg.上一个文件的文件路径,
            '预处理函数只显示输出信息': self.Main.cfg.预处理函数只显示输出信息,
            '预处理函数代码print替换': self.Main.cfg.预处理函数代码print替换,
            '绘制图像dpi': self.Main.cfg.绘制图像dpi,
            '是否输出渲染图片同时保存当前修改': self.Main.cfg.是否输出渲染图片同时保存当前修改,
            '是否输出渲染图片时输出对应的修改后npz文件': self.Main.cfg.是否输出渲染图片时输出对应的修改后npz文件,
            '是否渲染导出时输出的npz文件按照图片类型分类': self.Main.cfg.是否渲染导出时输出的npz文件按照图片类型分类,
            '缓存遮罩保存位置': self.Main.cfg.缓存遮罩保存位置,
            '是否只绘制一张参考图': self.Main.cfg.是否只绘制一张参考图,
            '用于判定是否使用极坐标绘图的的键': self.Main.cfg.用于判定是否使用极坐标绘图的的键,
            '是否用拥有该键作为判断极坐标绘图的依据': self.Main.cfg.是否用拥有该键作为判断极坐标绘图的依据,
            '用于绘制绘图区背景图的键': self.Main.cfg.用于绘制绘图区背景图的键,
            '有背景图时是否直接加载背景图': self.Main.cfg.有背景图时是否直接加载背景图,
            '是否开启夜间模式': self.Main.cfg.是否开启夜间模式,
            '软件主题色': self.Main.cfg.软件主题色,
            '软件图标': self.Main.cfg.软件图标,
            '绘图区图像是否转置': self.Main.cfg.绘图区图像是否转置,
            '绘图区图像是否上下翻转': self.Main.cfg.绘图区图像是否上下翻转,
            '绘图区图像是否左右翻转': self.Main.cfg.绘图区图像是否左右翻转,
            '绘图区图像极坐标是否是逆时针': self.Main.cfg.绘图区图像极坐标是否是逆时针,
            '绘图区图像极坐标翻转角度': self.Main.cfg.绘图区图像极坐标翻转角度,
            '传递的遮罩是否转置': self.Main.cfg.传递的遮罩是否转置,
            '传递的遮罩是否上下翻转': self.Main.cfg.传递的遮罩是否上下翻转,
            '传递的遮罩是否左右翻转': self.Main.cfg.传递的遮罩是否左右翻转,
            '传递的遮罩极坐标是否是逆时针': self.Main.cfg.传递的遮罩极坐标是否是逆时针,
            '传递的遮罩极坐标翻转角度': self.Main.cfg.传递的遮罩极坐标翻转角度,
            '绘图区缺失值是否设置为白色': self.Main.cfg.绘图区缺失值是否设置为白色,
            '绘图区灰度图像是否颜色反转': self.Main.cfg.绘图区灰度图像是否颜色反转,
            '批量预处理后是否保存当前文件': self.Main.cfg.批量预处理后是否保存当前文件,
            '自动显示遮罩延迟时间': self.Main.cfg.自动显示遮罩延迟时间,
            '显示参考图的行数': self.Main.cfg.显示参考图的行数,


        }

        # 使用 setattr 动态创建属性和对应的 property，tmd这是我写到现在最高级的东西了，动态创建全局属性
        for i in range(len(properties)):
            prop_name, cfg_item = list(properties.keys())[i], list(properties.values())[i]

            # 定义 getter 和 setter 函数
            def create_getter_setter(prop_name, cfg_item):# 额外多建立一个函数的意义是：提前将想要的字符串传递给内层函数，避免因为闭包的原因导致内层函数无法获取到想要的字符串（因为闭包的原因，内层函数只能获取到最后一次循环的字符串）
                def getter(self):
                    #logger.info(f"获取全局属性：{prop_name}")
                    return self.Main.cfg.get(cfg_item)

                def setter(self, value):
                    #logger.info(f"设置全局属性：{prop_name}，值为：{value}")
                    self.Main.cfg.set(cfg_item, value)

                return getter, setter

            getter, setter = create_getter_setter(prop_name, cfg_item)

            # 使用 property 函数创建属性
            setattr(self.__class__, prop_name, property(getter, setter))

    
        

        self.自定义变量值(ui)
        # 解码base64图片
        image_data = base64.b64decode(ui.base64pictemp.replace("data:image/png;base64,", ""))
        image = Image.open(BytesIO(image_data))

        # 获取图片尺寸
        width, height = image.size

        # 创建线程池
        ui.executor = ThreadPoolExecutor(max_workers=20)

        # 创建四个二维数组
        # 使用列表推导式创建并直接转换为NumPy数组
        ui.数值遮罩数组 = np.array([[1 for _ in range(width)] for _ in range(height)])
        ui.nan遮罩数组 = np.array([[1 for _ in range(width)] for _ in range(height)])
        ui.颜色遮罩数组 = np.array([["#ffffff" for _ in range(width)] for _ in range(height)])
        ui.nan颜色数组 = np.array([["#ffffff" for _ in range(width)] for _ in range(height)])

        # 创建 QWebChannel 和 Bridge 对象
        ui.channel = QWebChannel()
        ui.bridge = Bridge(ui)

        ui.校准函数是否开启 = False
        ui.是否使用极坐标 = False
        ui.当前使用numpy数组 = None


        for i in range(1, 6):  # 从1到5
            setattr(self, f'缓存遮罩{i}', np.zeros((500, 500)))

        # 如果之前保存过缓存遮罩，就直接加载已经存在的缓存遮罩
        if self.缓存遮罩保存位置!="" and os.path.exists(self.缓存遮罩保存位置):
            self.读取缓存遮罩(self.缓存遮罩保存位置)

        # 初始化为 None
        ui.雷达缩写对应名字 = {v:k for k,v in self.图像类型对应的源文件的key.items()}
        for name in ui.雷达缩写对应名字:
            setattr(self.ui, f"当前使用的{name}数组", [name,"当前没有值",[]])


        # 注册对象
        ui.channel.registerObject('bridge', ui.bridge)

        # 创建 WebEngineView 组件
        self.webview_base ,self.webviews = self.添加网页容器(num_groups=self.显示参考图的行数, parent=ui.ui, parent2=ui)
        self.webviewsall = self.webview_base + self.webviews

        for i in range(0, len(self.webview_base), 2):
            for view in self.webview_base[i:i+2]:
                page = CustomWebEnginePage(view, object1=view.objectName())
                view.setPage(page)
                page.setWebChannel(ui.channel)
        
        self.预启动加载()

        # 加载上一次的数据
        if self.展示文件函数(self.文件夹路径, self.正在使用的页数, 是否第一次启动=True) != 0:
            self.更新文件按钮状态()
            self.页码选择变化(self.正在使用的页数)
            self.选择文件(self.正在使用的文件索引)


        


    def 添加网页容器(self, num_groups=1, parent=None, parent2=None):
        """
        添加指定数量的 WebEngineView 组件和弹簧到 gridLayout_3 中。

        参数:
        num_groups (int): 需要添加的 WebEngineView 组数。
        """
        if parent is None:
            return

        logger.debug(f"添加网页容器：{num_groups}，目前的组件数量：{parent.gridLayout_3.count()}，分别有：{[parent.gridLayout_3.itemAt(i).widget() for i in range(parent.gridLayout_3.count())]}")

        webview_base = [parent.painter, parent.mask]

        # 存储基础的弹簧以便不删除它们
        self.base_spacers = [
            parent.verticalSpacer_first,
            parent.verticalSpacer_second,
            parent.horizontalSpacer_first,
            parent.horizontalSpacer_second
        ]
        
        # 清除现有的组件和弹簧
        for i in range(parent.gridLayout_3.count() - 1, -1, -1):
            item = parent.gridLayout_3.itemAt(i)
            if item is not None:
                widget_to_remove = item.widget()
                if widget_to_remove is not None:
                    # 跳过基础的 WebEngineView 组件和它们的弹簧
                    if widget_to_remove in [parent.painter, parent.mask]:
                        continue
                    
                    # 移除并删除不需要的组件
                    parent.gridLayout_3.removeWidget(widget_to_remove)
                    widget_to_remove.setParent(None)
                else:
                    # 如果是弹簧项目，移除并删除，跳过基础弹簧
                    if item in self.base_spacers:
                        continue
                    parent.gridLayout_3.removeItem(item)

        logger.debug(f"删除结束之后的组件数量：{parent.gridLayout_3.count()}，分别有：{[parent.gridLayout_3.itemAt(i).widget() for i in range(parent.gridLayout_3.count())]}")

        # 用于存储动态创建的 webview 实例
        webviews = []
        if num_groups != 0:
            # 遍历添加每组的 WebEngineView 组件
            for i in range(num_groups):
                # 创建两个 WebEngineView 组件
                webview1 = QWebEngineView(parent.scrollAreaWidgetContents_2)
                webview2 = QWebEngineView(parent.scrollAreaWidgetContents_2)
                webview1.setObjectName(f"webview_{i*2 + 1}")
                webview2.setObjectName(f"webview_{i*2 + 2}")
                
                # 使用 setattr 设置组件的名称
                setattr(self, f"webview_{i*2 + 1}", webview1)
                setattr(self, f"webview_{i*2 + 2}", webview2)
                
                # 设置组件的最小尺寸
                webview1.setMinimumSize(QSize(790, 500))
                webview2.setMinimumSize(QSize(790, 500))

                # 添加到 gridLayout_3 中
                parent.gridLayout_3.addWidget(webview1, i*2 + 2, 0, 1, 1)
                parent.gridLayout_3.addWidget(webview2, i*2 + 2, 2, 1, 1)

                # 创建并添加弹簧
                vertical_spacer1 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
                vertical_spacer2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
                horizontal_spacer1 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
                horizontal_spacer2 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

                parent.gridLayout_3.addItem(vertical_spacer1, i*2 + 3, 0, 1, 1)
                parent.gridLayout_3.addItem(vertical_spacer2, i*2 + 3, 2, 1, 1)
                parent.gridLayout_3.addItem(horizontal_spacer1, i*2 + 2, 1, 1, 1)
                parent.gridLayout_3.addItem(horizontal_spacer2, i*2 + 2, 3, 1, 1)

            # 从 self 中获取所有动态创建的 webview 实例并添加到列表
            for i in range(num_groups * 2):
                webview = getattr(self, f"webview_{i + 1}")
                webviews.append(webview)

        for i in range(0, len(webviews), 2):
            for view in webviews[i:i+2]:
                page = CustomWebEnginePage(view, object1=view.objectName())
                view.setPage(page)
                page.setWebChannel(parent2.channel)

        # 更新内层滑动区域的高度，保证滑动条正常出现和消失
        parent.scrollAreaWidgetContents_2.setMinimumSize(QSize(1600, 760 + 520 * num_groups))
        
        return webview_base, webviews


    def 预启动加载(self):
        ui = self.Main

        # 动态生成画笔的html代码
        html_painter_template = '<div class="color-button" id="{id}" title="{title}" style="background-color: {color};"></div>'

        html_painter_output = ""
        for key in self.Main.图像判别类型转换成数字.keys():
            id = key
            title = key
            color = self.Main.图像判别类型转换成颜色[key]
            html_painter_output += html_painter_template.format(id=id, title=title, color=color) + "\n"

        self.加载函数运行标志位 = True

        # 先加载一个皮卡丘先
        self.ui.painter.setHtml(self.Main.path_painter_html.replace("画笔种类颜色替换位置", html_painter_output).replace("var Nightmode = false;", f"var Nightmode = {str(self.是否开启夜间模式).lower()};"))
        self.painterbase64picdata = ui.base64pictemp
        self.ui.painter.loadFinished.connect(self.executeJavaScript)
        self.ui.whitepic = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAMAAAADCAYAAABWKLW/AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAAYSURBVBhXY/z//+9/BihggtJggMRhYAAAkcIEACsOnEUAAAAASUVORK5CYII="
        self.ui.mask.setHtml(self.Main.path_other_html.replace("base64数据替换占位符", ui.base64pictemp).replace("遮罩图标志位", "已开启遮罩图").replace("crosshairPosition = { x: positionArray[0], y: positionArray[1] };", "crosshairPosition = { x: positionArray[2], y: positionArray[3] };").replace("var Nightmode = false;", f"var Nightmode = {str(self.是否开启夜间模式).lower()};"))



        for webview in self.webviews:
            webview.setHtml(self.Main.path_other_html.replace("base64数据替换占位符", ui.base64pictemp).replace("var Nightmode = false;", f"var Nightmode = {str(self.是否开启夜间模式).lower()};"))

    def 自定义变量值(self, ui):
        ui.图像判别类型转换成数字 = {k: (int(v) if isinstance(v, str) and v.isdigit() else v) for k, v in self.图像类型对应的不同对象的选择数值.items()}
        ui.图像判别类型转换成颜色 = self.图像类型对应的不同对象的选择颜色
        # 不论大小写统一变小写，为了和html配合，html里面的黑白判定不绘制遮罩判定的是小写的
        for 类型, 颜色 in ui.图像判别类型转换成颜色.items():
            ui.图像判别类型转换成颜色[类型] = 颜色.lower()
        ui.图像判别数字转换成颜色 = {value: ui.图像判别类型转换成颜色[key] for key, value in ui.图像判别类型转换成数字.items()}
        ui.图像判别颜色转换成数字 = {value: ui.图像判别类型转换成数字[key] for key, value in ui.图像判别类型转换成颜色.items()}

        ui.图像判别数字转换成类型 = {value: key for key, value in ui.图像判别类型转换成数字.items()}
        ui.图像判别颜色转换成类型 = {value: key for key, value in ui.图像判别类型转换成颜色.items()}
        def 读取qrc路径(alias):
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

        # 使用示例
        ui.path_painter_html = 读取qrc路径("temple/painter")
        ui.path_other_html = 读取qrc路径("temple/mask")
        ui.base64pictemp = 读取qrc路径("src/base64pictemp").strip("\n")

        #############——————————————————————————————————————################
        

        ## 下面是绑定按钮要用到的一些变量
        ui.按钮状态 = QObject()
        ui.按钮状态.是否显示遮罩 = True
        self.Main.上一个文件 = self.文件夹路径
        self.page_size = 150 # 每页显示的文件数量
        self.total_pages = 1 # 总页数
        self.matched_files = [] # 匹配的文件列表
        self.stateTooltip = None
        self.全局遮罩选择菜单状态 = {key: {"选择状态": 0, "代表的数值": value} for key, value in self.Main.图像判别类型转换成数字.items()}
        self.判断参考图是否经过预处理标志位 = False
        self.判断参考图是否经过边缘提取标志位 = False
        self.当前文件存在遮罩 = False


    def 计时装饰器(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()  # 开始时间
            result = func(*args, **kwargs)  # 调用原始函数
            end_time = time.time()  # 结束时间
            logger.info(f"{func.__name__} 函数运行时间：{end_time - start_time} 秒。")
            return result
        return wrapper


    # 全局错误处理，输出报错信息：
    @staticmethod
    def 报错装饰器(func, context="程序运行出错了！错误信息："):
        def wrapper(*args, **kwargs):
            res = None
            try:
                res = func(*args, **kwargs)
            except Exception as e:
                self = args[0]  # 由于func是方法的引用，args[0]将是self
                # 判断是否需要完整报错信息
                if self.是否需要完整报错信息:
                    # 获取完整的错误堆栈信息
                    error_info = traceback.format_exc()
                    content = context + str(e) + "\n详细错误信息：" + error_info
                else:
                    content = context + str(e)
                if "IndexError: list index out of range" in content and "ori_array = self.Main.当前使用numpy数组和内部数据字典[0][2]" in content:
                    content = "当前使用的文件中键的范围与设置里表格一中键的范围不对应，文件中键的范围应该包含表格一中键的范围，请检查文件是否正确！"
                elif all(keyword in content for keyword in ["MainWindow", "has no attribute", "当前使用numpy数组和内部数据字典"]):
                    content = "还没有加载文件，请先加载文件后再进行操作！"
                
                logger.error(content)
                
                w = InfoBar(
                    icon=InfoBarIcon.ERROR,
                    title='报错！',
                    content=content,
                    isClosable=True,
                    position=InfoBarPosition.BOTTOM,
                    duration=15000,
                    parent=self.Main)
                w.show()
            return res
        return wrapper
            
    def 显示消息框函数(self, icon, title, content ,position="右上", duration=4000):
        """
        position可选项：
        """
            
        位置字典 = {
            "顶部": InfoBarPosition.TOP,
            "底部": InfoBarPosition.BOTTOM,
            "左上": InfoBarPosition.TOP_LEFT,
            "右上": InfoBarPosition.TOP_RIGHT,
            "左下": InfoBarPosition.BOTTOM_LEFT,
            "右下": InfoBarPosition.BOTTOM_RIGHT,
            "无": InfoBarPosition.NONE
        }
        w = InfoBar(
        icon=getattr(InfoBarIcon, icon.upper(), None),
        title=title,
        content=content,
        isClosable=True,
        position=位置字典[position],
        duration=duration,
        parent=self.Main)
        w.show()
    
    @报错装饰器
    def 显示进度条(self,是否显示 = True):
        if not 是否显示:# 之前用 if self.stateTooltip判断是否在显示
            logger.info("隐藏进度条")
            try:
                self.stateTooltip.setContent('文件加载完成啦 😆')
                self.stateTooltip.setState(True)
            except:pass
        else:
            logger.info("显示进度条")
            self.stateTooltip = StateToolTip('正在加载文件', '请耐心等待哦~~', self.ui.widget)
            # 获取父窗口的尺寸
            parentWidth = self.Main.width()
            parentHeight = self.Main.height()

            # 假设提示框的尺寸为150x200
            tooltipWidth = 340# 470
            tooltipHeight = 120# 0

            # 计算提示框的位置，使其位于右下角
            x = parentWidth - tooltipWidth  # 20为右边距
            y = parentHeight - tooltipHeight  # 20为下边距

            # 移动提示框到计算出的位置
            self.stateTooltip.move(x, y)
            self.stateTooltip.show()


    @报错装饰器
    def 更新初始自定义变量(self):
        self.Main.雷达缩写对应名字 = {v: k for k, v in self.图像类型对应的源文件的key.items()}
        for name in self.Main.雷达缩写对应名字:
            setattr(self.ui, f"当前使用的{name}数组", [name, "当前没有值", []])

        self.Main.图像判别类型转换成数字 = {k: (int(v) if isinstance(v, str) and v.isdigit() else v) for k, v in self.图像类型对应的不同对象的选择数值.items()}
        self.Main.图像判别类型转换成颜色 = self.图像类型对应的不同对象的选择颜色
        # 不论大小写统一变小写，为了和html配合，html里面的黑白判定不绘制遮罩判定的是小写的
        for 类型, 颜色 in self.Main.图像判别类型转换成颜色.items():
            self.Main.图像判别类型转换成颜色[类型] = 颜色.lower()
        self.Main.图像判别数字转换成颜色 = {value: self.Main.图像判别类型转换成颜色[key] for key, value in self.Main.图像判别类型转换成数字.items()}
        self.Main.图像判别颜色转换成数字 = {value: self.Main.图像判别类型转换成数字[key] for key, value in self.Main.图像判别类型转换成颜色.items()}

        self.Main.图像判别数字转换成类型 = {value: key for key, value in self.Main.图像判别类型转换成数字.items()}
        self.Main.图像判别颜色转换成类型 = {value: key for key, value in self.Main.图像判别类型转换成颜色.items()}

        # 字典的更新就是很慢，用刷新其他参数的方式敦促配置类将没加载到位置文件的量加载进去
        self.是否需要规整数据 = not self.是否需要规整数据
        self.是否需要规整数据 = not self.是否需要规整数据

        self.webview_base ,self.webviews = self.添加网页容器(num_groups=self.显示参考图的行数, parent=self.Main.ui, parent2=self.Main)
        self.预启动加载()
        self.选择文件函数()
        self.显示原始数组参考图()


    @报错装饰器
    def 初始化参考图像函数(self, 是否保存文件=False):

        images = self.webviews
        if self.是否只绘制一张参考图:
            self.更新参考图片(0, 是否保存文件)
        else:
            for i, image in enumerate(images):
                # 假设 lst 是你要检查的列表
                lst = self.Main.当前使用numpy数组和内部数据字典
                # 检查索引 i 是否在 lst 的索引范围内
                if 0 <= i < len(lst):
                    # 如果 i 是有效的索引
                    self.更新参考图片(i, 是否保存文件)
                    QCoreApplication.processEvents()
                else:pass

    
    @报错装饰器
    def 更新参考图片(self, 索引, 是否保存文件=False):
        global 绘制图像
        if globals().get('绘制图像')!=None:
            del 绘制图像
        if self.自定义绘图函数能不能用:
            exec(self.自定义绘图函数,globals())
        else:
            绘制图像 = globals().get('matpainter')
        if 索引 >= len(self.webviews):
            logger.error(f"绘制参考图的时候，npz文件数组的键索引超出参考图容器数量范围，当前索引为{索引}，最大索引为{len(self.webviews)-1}，当前键为{self.Main.当前使用numpy数组和内部数据字典[索引][0]}")
            return
        images = self.webviews
        绘图使用的文件名 = re.sub(r"(_Mask|_预处理|_已修改)", "", os.path.basename(self.正在使用的文件名字).split(".")[0])
        
        if 是否保存文件:
            
            def 校验文件路径(路径):
                # 检查路径是否存在
                if os.path.exists(路径):
                    # 检查路径是否可写
                    if os.access(路径, os.W_OK):
                        return True
                    else:
                        logger.error("保存图片时路径不可写")
                        return False
                else:
                    logger.error("保存图片时路径不存在")
                    return False
            if self.判断参考图是否经过预处理标志位 == True:
                需要处理的数字 = []
                for key in self.全局遮罩选择菜单状态:
                    if self.全局遮罩选择菜单状态[key]["选择状态"] == 1:
                        需要处理的数字.append(self.全局遮罩选择菜单状态[key]["代表的数值"])
                需要处理的内容 = "-".join([self.Main.图像判别数字转换成类型[int(i)] for i in 需要处理的数字])
                绘图使用的文件名 = 绘图使用的文件名+f"┃消去【{需要处理的内容}】"        
            logger.info(f"开始绘制{self.Main.当前使用numpy数组和内部数据字典[索引][0]}-{绘图使用的文件名}图像")
            if self.文件保存路径!="" and 校验文件路径(self.文件保存路径):
                保存到哪里 = self.文件保存路径
            elif self.文件保存路径 == "":
                self.显示消息框函数("warning", "保存路径为空", f"将存入来源文件路径，但会放在同名文件夹下面，保存路径为{os.path.dirname(self.当前使用的文件路径)}")
                保存到哪里 = os.path.dirname(self.当前使用的文件路径)
            elif 校验文件路径(self.文件保存路径) == False:
                self.显示消息框函数("error", "保存路径不可用", "请重新输入，单击右边的搜索框可以唤起文件选择对话框。")
                return
            if self.判断参考图是否经过预处理标志位:
                if self.判断参考图是否经过边缘提取标志位:
                    # 处理保存文件，预处理和边缘提取都为True的情况
                    logger.info("处理保存文件，预处理和边缘提取都为True的情况")
                    picbase64data = 绘制图像(self.根据遮罩数组处理原始图像(self.Main.当前使用numpy数组和内部数据字典[索引][2].copy()), self.Main.当前使用numpy数组和内部数据字典[索引][0], self.Main.是否使用极坐标, file_name = 绘图使用的文件名, dpi=self.绘制图像dpi,save_path = 保存到哪里,edgedict = self.最终传递的边缘数组字典)
                else:
                    # 处理保存文件和预处理为True，边缘提取为False的情况
                    logger.info("处理保存文件和预处理为True，边缘提取为False的情况")
                    picbase64data = 绘制图像(self.根据遮罩数组处理原始图像(self.Main.当前使用numpy数组和内部数据字典[索引][2].copy()), self.Main.当前使用numpy数组和内部数据字典[索引][0], self.Main.是否使用极坐标, file_name = 绘图使用的文件名, dpi=self.绘制图像dpi,save_path = 保存到哪里)
            else:
                if self.判断参考图是否经过边缘提取标志位:
                    # 处理保存文件和边缘提取为True，预处理为False的情况
                    logger.info("处理保存文件和边缘提取为True，预处理为False的情况")
                    picbase64data = 绘制图像(self.Main.当前使用numpy数组和内部数据字典[索引][2].copy(), self.Main.当前使用numpy数组和内部数据字典[索引][0], self.Main.是否使用极坐标, file_name = 绘图使用的文件名, dpi=self.绘制图像dpi,save_path = 保存到哪里,edgedict = self.最终传递的边缘数组字典)
                else:
                    # 处理只有保存文件为True，其它都为False的情况
                    logger.info("处理只有保存文件为True，其它都为False的情况")
                    picbase64data = 绘制图像(self.Main.当前使用numpy数组和内部数据字典[索引][2].copy(), self.Main.当前使用numpy数组和内部数据字典[索引][0], self.Main.是否使用极坐标, file_name = 绘图使用的文件名, dpi=self.绘制图像dpi,save_path = 保存到哪里)
        else:
            logger.info(f"开始绘制{self.Main.当前使用numpy数组和内部数据字典[索引][0]}-{绘图使用的文件名}图像")
            if self.判断参考图是否经过预处理标志位:
                if self.判断参考图是否经过边缘提取标志位:
                    # 处理保存文件为False，预处理和边缘提取都为True的情况
                    logger.info("处理保存文件为False，预处理和边缘提取都为True的情况")
                    picbase64data = 绘制图像(self.根据遮罩数组处理原始图像(self.Main.当前使用numpy数组和内部数据字典[索引][2].copy()), self.Main.当前使用numpy数组和内部数据字典[索引][0], self.Main.是否使用极坐标, file_name = 绘图使用的文件名, dpi=self.绘制图像dpi,edgedict = self.最终传递的边缘数组字典)
                    images[索引].setHtml(self.Main.path_other_html.replace("base64数据替换占位符", picbase64data).replace("var Nightmode = false;", f"var Nightmode = {str(self.是否开启夜间模式).lower()};"))
                else:
                    # 处理保存文件为False，预处理为True，边缘提取为False的情况
                    logger.info("处理保存文件为False，预处理为True，边缘提取为False的情况")
                    picbase64data = 绘制图像(self.根据遮罩数组处理原始图像(self.Main.当前使用numpy数组和内部数据字典[索引][2].copy()), self.Main.当前使用numpy数组和内部数据字典[索引][0], self.Main.是否使用极坐标, file_name = 绘图使用的文件名, dpi=self.绘制图像dpi)
                    images[索引].setHtml(self.Main.path_other_html.replace("base64数据替换占位符", picbase64data).replace("var Nightmode = false;", f"var Nightmode = {str(self.是否开启夜间模式).lower()};"))
            else:
                if self.判断参考图是否经过边缘提取标志位:
                    # 处理保存文件为False，边缘提取为True，预处理为False的情况
                    logger.info("处理保存文件为False，边缘提取为True，预处理为False的情况")
                    picbase64data = 绘制图像(self.Main.当前使用numpy数组和内部数据字典[索引][2].copy(), self.Main.当前使用numpy数组和内部数据字典[索引][0], self.Main.是否使用极坐标, file_name = 绘图使用的文件名, dpi=self.绘制图像dpi,edgedict = self.最终传递的边缘数组字典)
                    images[索引].setHtml(self.Main.path_other_html.replace("base64数据替换占位符", picbase64data).replace("var Nightmode = false;", f"var Nightmode = {str(self.是否开启夜间模式).lower()};"))
                else:
                    # 处理保存文件，预处理和边缘提取都为False的情况
                    logger.info("处理保存文件，预处理和边缘提取都为False的情况")
                    picbase64data = 绘制图像(self.Main.当前使用numpy数组和内部数据字典[索引][2].copy(), self.Main.当前使用numpy数组和内部数据字典[索引][0], self.Main.是否使用极坐标, file_name = 绘图使用的文件名, dpi=self.绘制图像dpi)
                    images[索引].setHtml(self.Main.path_other_html.replace("base64数据替换占位符", picbase64data).replace("var Nightmode = false;", f"var Nightmode = {str(self.是否开启夜间模式).lower()};"))
    
    def 确保有效的保存路径(self):
        # 检查并更新文件保存路径
        if self.文件保存路径 == "":
            if self.文件夹路径 == "":
                self.显示消息框函数("error", "保存文件夹路径不存在", "请先选择文件夹路径", "底部")
                return
            else:
                self.文件保存路径 = self.文件夹路径


    @报错装饰器
    def 数组绘图之前的预处理(self, array_all):
        """
        array_all: numpy数组
        为了保证和matplotlib的默认显示方式一致，极坐标显示得时候翻转角度默认 + 90
        """
        # 确保numpy数组不为空
        if array_all.size == 0:
            raise ValueError("传递的数组为空")
        array_all = np.array(array_all.copy())

        try:
            # 根据配置进行处理
            if self.绘图区图像是否转置:
                array_all = np.transpose(array_all)

            if self.绘图区图像是否上下翻转:
                array_all = np.flip(array_all, axis=1)  # 上下翻转

            if self.绘图区图像是否左右翻转:
                array_all = np.flip(array_all, axis=0)  # 左右翻转

            if self.Main.是否使用极坐标:
                angle_flip = self.绘图区图像极坐标翻转角度 + 90
                angle_flip = angle_flip % 360  # 确保angle_flip在0-360之间
            else:
                angle_flip = self.绘图区图像极坐标翻转角度 

            if angle_flip != 0:
                每个角度对应的元素数 = len(array_all) / 360
                # 更新angle_flip的值
                angle_flip = round(angle_flip * 每个角度对应的元素数)  # 确保angle_flip是整数
                if self.绘图区图像极坐标是否是逆时针:
                    array_all = np.concatenate((array_all[-angle_flip:], array_all[:-angle_flip]), axis=0)
                else:
                    array_all = np.concatenate((array_all[angle_flip:], array_all[:angle_flip]), axis=0)

            logger.info("原始数组预处理完成")
            # 获取基础数值要放在预处理后面，不然根据位置参数来获取肯定会和实际不符
            if self.Main.是否使用极坐标:
                self.极坐标基础半径 = array_all.shape[1]
                self.圆心基础X坐标 = array_all.shape[1]
                self.圆心基础Y坐标 = array_all.shape[1]
            else:
                self.直角坐标基础宽度 = array_all.shape[1]
                self.直角坐标基础高度 = array_all.shape[0]

            return array_all

        except Exception as e:
            track = traceback.format_exc()
            logger.error(f"预处理失败: {e}\n{track}")
            raise e


    @报错装饰器
    def executeJavaScript(self, 用不到 = ""):
        # 加载背景图
        if hasattr(self.Main.bridge, 'requestBase64ImageFromPython'):
            self.Main.bridge.requestBase64ImageFromPython(self.painterbase64picdata)
        else:
            return 
        
        if self.加载函数运行标志位:
            self.加载函数运行标志位 = False
        else: return
        # 修改后的代码
        if (self.是否自动显示遮罩 and self.当前文件存在遮罩) or self.是否默认预处理:
            def execute_js():
                js_code = """
                console.log('开始自动绘图');
                drawColorArrayOnCanvas(maskArray_color);
                """
                self.ui.painter.page().runJavaScript(js_code)
            
            QTimer.singleShot(self.自动显示遮罩延迟时间, execute_js)  # 2秒后执行execute_js函数



    @报错装饰器
    def 将新的文件加载到webview中(self,key = None):
        # 例如，如果你有特定的 HTML 文件要加载到某个 view 中，可以使用 setHtml 或 load 方法
        # ui.painter.setHtml("<html>...</html>")
        # ui.mask.load(QUrl("path/to/html"))
        if key == "空文件夹路径":
            self.显示消息框函数("error", "打开文件夹失败了", "上次编辑的记录找不到了QAQ，请重新选择文件","底部")
            return

        for keyname, name in self.Main.雷达缩写对应名字.items():
            if keyname != "Musk" and keyname != "Musk_nan" and keyname != "Background":
                self.Main.当前文件存在的图像列表 = f"当前使用的{name}数组"

        if self.有背景图时是否直接加载背景图 and "Background" in self.Main.当前使用numpy数组.keys():
            # 这个有个超级巨坑：直接从npz加载的str类型的数据不能直接当str用，它本质上不是str，而是一个np的对象
            self.Background图片 = str(self.Main.当前使用numpy数组["Background"])
            self.painterbase64picdata = self.Background图片
        else:
            for item in self.Main.当前使用numpy数组和内部数据字典:
                if item[3] == self.用于绘制绘图区背景图的键:
                    self.painterbase64picdata = self.从原始numpy数组绘制坐标图(item[2], self.Main.是否使用极坐标)
                    break

        极坐标标识符 = "polar" if self.Main.是否使用极坐标 else "rect"

        logger.info(f"极坐标标识符为{极坐标标识符}")
        QApplication.processEvents()

        # 动态生成画笔的html代码
        html_painter_template = '<div class="color-button" id="{id}" data-title="{title}" style="background-color: {color};"></div>'

        self.html_painter_output = ""
        for key in self.Main.图像判别类型转换成数字.keys():
            id = key
            title = key
            color = self.Main.图像判别类型转换成颜色[key]
            self.html_painter_output += html_painter_template.format(id=id, title=title, color=color) + "\n"

        self.加载函数运行标志位 = True

        self.ui.painter.setHtml(
            self.Main.path_painter_html.replace('var coordinateFlag = "rect"', f'var coordinateFlag = "{极坐标标识符}"')
            .replace("画笔种类颜色替换位置", self.html_painter_output)
            .replace("var Nightmode = false;", f"var Nightmode = {str(self.是否开启夜间模式).lower()};")
            )
        QCoreApplication.processEvents()

        if self.是否加载参考图:
            self.初始化参考图像函数()
            self.显示消息框函数("success", "加载图像", f"将要加载{len(self.Main.当前使用numpy数组和内部数据字典)}个图像","底部")
        QCoreApplication.processEvents()
        self.ui.mask.setHtml(self.Main.path_other_html.replace("base64数据替换占位符", self.ui.whitepic).replace("遮罩图标志位", "已开启遮罩图").replace("crosshairPosition = { x: positionArray[0], y: positionArray[1] };", "crosshairPosition = { x: positionArray[2], y: positionArray[3] };").replace("var Nightmode = false;", f"var Nightmode = {str(self.是否开启夜间模式).lower()};"))
    # 这个暂时不用
    
    @报错装饰器
    def 从原始numpy数组绘制坐标图(self, all_array,是否使用极坐标=False):
        logger.info("开始绘制原始图像")
        all_array = self.数组绘图之前的预处理(all_array)
        try:
            if 是否使用极坐标: 

                max_val = np.nanmax(all_array)
                min_val = np.nanmin(all_array)

                if self.绘图区缺失值是否设置为白色:
                    # 缺失值设置为白色，替换值应为最大值
                    replacement_val = max_val + (max_val - min_val) / 255
                else:
                    # 缺失值设置为黑色，替换值应为最小值减去最大值和最小值的差的 1/255
                    replacement_val = min_val - (max_val - min_val) / 255

                # 替换 all_array 中的 nan 值
                all_array = np.where(np.isnan(all_array), replacement_val, all_array)
                ori_array = np.array(self.完整极坐标数组到画布数组(all_array,"数组"))


            # 假设 all_array 已经定义并且可能包含 nan 值
            # 计算 all_array 中非 nan 值的最大值和最小值
            else:
                max_val = np.nanmax(all_array)
                min_val = np.nanmin(all_array)

                if self.绘图区缺失值是否设置为白色:
                    # 缺失值设置为白色，替换值应为最大值
                    replacement_val = max_val + (max_val - min_val) / 255
                else:
                    # 缺失值设置为黑色，替换值应为最小值减去最大值和最小值的差的 1/255
                    replacement_val = min_val - (max_val - min_val) / 255

                # 替换 all_array 中的 nan 值
                all_array = np.where(np.isnan(all_array), replacement_val, all_array)

                # 接下来的操作
                ori_array = all_array.copy()
            
            # 步骤3: 使用线性变换将数组的值归一化到0到255区间
            normalized_array = (ori_array - np.min(ori_array)) / (np.max(ori_array) - np.min(ori_array)) * 255
            
            if self.绘图区灰度图像是否颜色反转:
                # 反转颜色，使黑色变为白色，白色变为黑色
                inverted_array = 255 - normalized_array
            else:
                inverted_array = normalized_array

            # 步骤4: 将归一化后的数组转换为np.uint8类型
            image_array = inverted_array.astype(np.uint8)


            # 创建图像
            img = Image.fromarray(image_array, 'L')
            # 转换为base64编码
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()  # 画完之后还要转换成base64编码，返回值应该是一个base64编码的字符串
            return img_str
        except Exception as e:
            track = traceback.format_exc()
            logger.error(f"绘制原始图像失败: {e}\n{track}")
            logger.error(f"当前使用的数组：{all_array}")
            return self.Main.base64pictemp


    def 输入原始数据返回要不要使用极坐标(self, all_array):
        key_present_check = (self.用于判定是否使用极坐标绘图的的键 in all_array.keys())
        if (self.是否用拥有该键作为判断极坐标绘图的依据 and key_present_check) or (not self.是否用拥有该键作为判断极坐标绘图的依据 and not key_present_check):
            return True
        else:
            return False

    @报错装饰器
    def 从文件得到全局数组(self, filepath):
        '''
        传入文件路径，生成全局数值数组和遮罩数组（包含完整遮罩数组和缺失值遮罩数组）
        '''
        if filepath == "":
            return "空文件夹路径"
        try:
            data_dict = np.load(filepath)
            # 将NpzFile对象中的所有数组提取到一个新的字典中
            array_dict = {key: data_dict[key] for key in data_dict.keys() if key != 'allow_pickle'}
        except Exception as e:
            logger.error(f"读取文件失败，错误信息：{e}")
            logger.error(f"文件路径：{filepath}")
            raise ValueError("文件格式不一致，当前源文件只能是npz字典格式，要处理其他文件格式请改动源代码的'从文件得到全局数组'函数以及配置文件的色标，要能够从源文件生成数据二位数组，绘图函数只需要传入二维数组和自定义色标即可")

        if not isinstance(array_dict, dict):
            raise ValueError("文件格式不一致，当前源文件只能是npz字典格式，键为字符串，值为图片二位数组，请改动源代码的'从文件得到全局数组'函数以及配置文件的色标，绘图函数只需要传入二维数组和自定义色标即可")
    
        # 检查列表是否为空
        if not self.上一个文件的文件路径:
            self.上一个文件的文件路径 = [filepath]
        else:
            # 如果列表不为空，先添加新的文件路径
            self.上一个文件的文件路径.append(filepath)
            # 如果列表长度超过5，移除最早的文件路径
            if len(self.上一个文件的文件路径) > 6:
                self.上一个文件的文件路径 = self.上一个文件的文件路径[1:]
        


        QApplication.processEvents()
        self.Main.是否使用极坐标 = self.输入原始数据返回要不要使用极坐标(array_dict)


        self.Main.当前使用numpy数组 = array_dict
        self.Main.当前使用numpy数组和内部数据字典 = []

        for key, name in self.Main.雷达缩写对应名字.items():
            try:
                if key != "Musk" and key != "Musk_nan" and key != "Background":
                    setattr(self.Main, f"当前使用的{name}数组", [name, "当前存在值", array_dict[key], key])  # 从 array_dict 中取值并赋值
                    self.Main.当前使用numpy数组和内部数据字典.append(getattr(self.Main, f"当前使用的{name}数组"))
            except:
                pass
        # 找到键的差集并遍历
        for key in set(self.Main.雷达缩写对应名字) - set(array_dict):
            if key != "Musk" and key != "Musk_nan" and key != "Background":
                # 构建属性名称
                attr_name = f"当前使用的{self.Main.雷达缩写对应名字[key]}数组"
                # 直接给类属性赋新值
                setattr(self.Main, attr_name, [self.Main.雷达缩写对应名字[key], "当前没有值", []])
        
        # 以第一个数据作为参考
        ori_array = self.Main.当前使用numpy数组[self.用于绘制绘图区背景图的键]

        # 初始化空数组与ori_array同尺寸
        self.Main.数值遮罩数组 = np.empty_like(ori_array)
        self.Main.nan遮罩数组 = np.empty_like(ori_array)
        self.Main.颜色遮罩数组 = np.empty_like(ori_array, dtype=object)  # 假设颜色值是字符串
        self.Main.nan颜色数组 = np.empty_like(ori_array, dtype=object)  # 假设颜色值是字符串

        第一个值 = list(self.Main.图像判别类型转换成数字.values())[0] # 一般第一个值默认为nan值
        第二个值 = list(self.Main.图像判别类型转换成数字.values())[1] # 第二个值默认为待判断值
    
        # 从如果源文件包含了遮罩数组，就直接加载遮罩数组给全局变量
        if "Musk" in list(array_dict.keys()):
            self.Main.数值遮罩数组 = array_dict["Musk"]
        else:
            self.Main.数值遮罩数组 = np.where(np.isnan(ori_array), 第一个值, 第二个值)
        if "Musk_nan" in list(array_dict.keys()):
            self.Main.nan遮罩数组 = array_dict["Musk_nan"]
        else:
            self.Main.nan遮罩数组 = np.where(np.isnan(ori_array), 第一个值, 第二个值)

        QApplication.processEvents()
        logger.info(f"开始转换数值数组到颜色数组")
        self.Main.颜色遮罩数组 = self.将数值遮罩数组转换为颜色遮罩数组(self.Main.数值遮罩数组)
        self.Main.nan颜色数组 = self.将数值遮罩数组转换为颜色遮罩数组(self.Main.nan遮罩数组)

        if "Musk" in list(array_dict.keys()) and "Musk_nan" in list(array_dict.keys()):
            self.当前文件存在遮罩 = True
            self.Main.颜色遮罩数组 = self.将数值遮罩数组转换为颜色遮罩数组(self.Main.数值遮罩数组)
            self.Main.nan颜色数组 = self.将数值遮罩数组转换为颜色遮罩数组(self.Main.nan遮罩数组)
        else:
            self.当前文件存在遮罩 = False
            if self.是否默认预处理 == True and self.当前文件存在遮罩 != True:
                self.预处理程序启动(True)
        logger.success(f"处理文件数据已完成，成功读取文件：{filepath}")
        
        return None
    
    @报错装饰器
    def 将数值遮罩数组转换为颜色遮罩数组(self, 数值遮罩数组):
        '''
        输入数值遮罩数组，输出颜色遮罩数组
        '''
        颜色遮罩数组 = np.empty(数值遮罩数组.shape, dtype=object)
        for 数值, 颜色 in self.Main.图像判别数字转换成颜色.items():
            颜色遮罩数组[np.where(数值遮罩数组 == 数值)] = 颜色
        return 颜色遮罩数组
        

    @报错装饰器
    def 将颜色遮罩数组转换成图片(self, mask_array):
        try:
            logger.info("查看输入painter数组尺寸")
            logger.info(f"{len(mask_array)},{len(mask_array[0])}")
            mask_array = self.数组绘图之前的预处理(mask_array)

            if self.Main.是否使用极坐标:
                mask_array = self.完整极坐标数组到画布数组(mask_array, "图片")
                mask_array = mask_array.astype(np.int32)

            if not self.Main.是否使用极坐标:
                # 找出所有唯一颜色
                unique_colors = np.unique(mask_array)

                # 创建颜色到整数的映射表
                color_to_int = {}
                for color in unique_colors:
                    if color.startswith('#') and len(color) == 7:
                        color_to_int[color] = int(color[1:], 16)
                    else:
                        color_to_int[color] = 16777215  # 默认颜色

                # 将所有颜色转换为整数
                # 先创建一个与 mask_array 形状相同的数组，初始值为默认颜色
                int_mask_array = np.full(mask_array.shape, 16777215, dtype=np.int32)

                # 对每种颜色进行批量替换
                for color, int_color in color_to_int.items():
                    int_mask_array[np.where(mask_array == color)] = int_color

                mask_array = int_mask_array

            # 将整数颜色值转换为RGBA格式
            image_data = np.stack(
                [
                    (mask_array >> 16) & 0xFF,
                    (mask_array >> 8) & 0xFF,
                    mask_array & 0xFF,
                    np.full(mask_array.shape, 255)
                ],
                axis=-1
            )

            # 将Numpy数组转换为PIL图像
            image = Image.fromarray(image_data.astype('uint8'), 'RGBA')

            # 将图片转换为PNG格式的字节数据
            with io.BytesIO() as output:
                image.save(output, format="PNG")
                png_data = output.getvalue()
            
            # 将PNG字节数据编码为base64
            base64data = "data:image/png;base64," + base64.b64encode(png_data).decode('utf-8')
            return base64data

        except Exception as e:
            logger.error(f"转换遮罩数组到图片失败，错误信息：{e}\n详细信息：{traceback.format_exc()}")
            return self.Main.base64pictemp
    
    @报错装饰器
    def 从webengineview的遮罩更新本地数据(self, mask_color_array, 是否需要规整数据=True):
        # 将 mask_color_array 转换为 numpy 数组
        mask_color_array = np.array(mask_color_array)
        self.Main.颜色遮罩数组 = mask_color_array
        
        # 提取第一个值和最后一个值
        图像判别类型转换成数字 = self.Main.图像判别类型转换成数字
        第一个值 = list(图像判别类型转换成数字.values())[0]
        最后一个值 = list(图像判别类型转换成数字.values())[-1]

        # 确保 nan_mask 与 self.Main.颜色遮罩数组维度匹配
        if self.Main.nan遮罩数组.shape != self.Main.颜色遮罩数组.shape:
            logger.info(f"nan遮罩数组的维度：{self.Main.nan遮罩数组.shape}")
            logger.info(f"颜色遮罩数组的维度：{self.Main.颜色遮罩数组.shape}")
            logger.error("nan遮罩数组和颜色遮罩数组的维度不匹配")
            return
        
        # 将颜色遮罩数组去掉 nan 值
        nan_mask = self.Main.nan遮罩数组 == 第一个值
        if nan_mask.shape != self.Main.颜色遮罩数组.shape:
            logger.info(f"布尔掩码的维度：{nan_mask.shape}")
            logger.info(f"颜色遮罩数组的维度：{self.Main.颜色遮罩数组.shape}")
            logger.error("布尔掩码的维度与颜色遮罩数组维度不一致")
            return
        
        self.Main.颜色遮罩数组[nan_mask] = self.Main.图像判别数字转换成颜色[第一个值]

        # 将颜色遮罩数组转换为数值遮罩数组
        图像判别颜色转换成数字 = self.Main.图像判别颜色转换成数字
        数值遮罩数组 = self.Main.数值遮罩数组.copy()

        # 记录已处理的位置
        processed_mask = np.zeros_like(self.Main.颜色遮罩数组, dtype=bool)

        for color, number in 图像判别颜色转换成数字.items():
            mask = self.Main.颜色遮罩数组 == color
            if mask.shape != self.Main.数值遮罩数组.shape:
                logger.error("布尔掩码的维度与数值遮罩数组维度不一致")
                continue
            
            # 更新数值遮罩数组
            数值遮罩数组[mask] = number

            # 记录处理过的位置
            processed_mask = processed_mask | mask

        # 没有被处理的位置，设置为最后一个值
        数值遮罩数组[~processed_mask] = 最后一个值

        self.Main.数值遮罩数组 = 数值遮罩数组

        if 是否需要规整数据:
            # 将数值遮罩数组重新转换成颜色遮罩数组
            图像判别数字转换成颜色 = self.Main.图像判别数字转换成颜色
            self.Main.颜色遮罩数组 = np.vectorize(图像判别数字转换成颜色.get)(self.Main.数值遮罩数组)
    
    @报错装饰器
    def 显示遮罩流程(self):
        # 显示遮罩流程
        # 1. js将遮罩传递回python主程序
        # 2. 更新数值遮罩数组
        # 3. 更新颜色遮罩数组
        # 4. 从颜色遮罩数组转换成图片，再转换成base64编码
        # 5. 将base64图片传递给js
        time.sleep(0.1)  # 等待一下，等待本地数组更新完毕

        # 定义回调函数
        def on_base64_ready(base64data):
            self.Main.bridge.requestbase64picture(base64data, '十字标注线')

        # 使用线程来处理耗时的操作
        def 处理并获取base64(颜色遮罩数组):
            strtt_time = time.time()
            base64data = self.将颜色遮罩数组转换成图片(颜色遮罩数组)  # 假设这是一个独立的函数，不依赖于self
            logger.info(f"计算完成遮罩图片的base64编码耗时：{time.time() - strtt_time:.4f} 秒")
            return base64data

        # # 线程任务函数
        # def 线程任务():
        base64data = 处理并获取base64(self.Main.颜色遮罩数组.copy())
        # 执行回调函数
        on_base64_ready(base64data)



    # 控件名称	控件类型	中文意思
    # Dialog	QDialog	对话框
    # widget	QWidget	小部件
    # verticalLayout	QVBoxLayout	垂直布局
    # scrollArea	QScrollArea	滚动区域
    # scrollAreaWidgetContents_2	QWidget	滚动区域内容容器
    # painter	QWebEngineView	绘图器
    # mask	QWebEngineView	遮罩图层
    # ZDRphoto	QWebEngineView	ZDR照片
    # Vphoto	QWebEngineView	V照片
    # Wphoto	QWebEngineView	W照片
    # SNRphoto	QWebEngineView	SNR照片
    # LDRphoto	QWebEngineView	LDR照片
    # widget_8	QWebEngineView	小部件8
    # openfiles	PrimaryPushButton	打开文件按钮
    # previousfile	QPushButton	上一个文件按钮
    # nextfile	QPushButton	下一个文件按钮
    # clearmask	QPushButton	清除遮罩按钮
    # showall	QPushButton	显示全部按钮
    # outputclearpic	QPushButton	输出清晰图片按钮
    # showmask	QPushButton	显示遮罩按钮
    # selectfiles	PrimaryPushButton	选择文件按钮
    # savepath	SearchLineEdit	保存路径输入框
    # savefile	QPushButton	保存文件按钮
    # refresh	QPushButton	刷新按钮
    # page_selector	QComboBox	页面选择器
    # preprocessing_code	SearchLineEdit	预处理代码输入框
    # preprocessing	QPushButton	预处理按钮
    # correctingposition	QPushButton	校正位置按钮
    # showfiles	QComboBox	显示文件选择器
    # loadlastfile	QPushButton	加载最后一个文件按钮
    # refreshmask    QPushButton	刷新遮罩按钮
    # choosemaskselect    QPushButton	选择遮罩下拉菜单
    # importpainter    QPushButton	导入自定义绘图函数按钮
    # savefileall    QPushButton	保存文件夹下所有渲染的参考图像按钮
    # showedge   QPushButton	显示边缘提取图像按钮
    # preprocessingall    QPushButton	批量预处理按钮


    # 用来给按钮绑定函数的
    def Initialize_Connects(self,ui):
        # 为控件添加工具提示
        tooltips = {
            self.ui.showmask: "点击以显示或隐藏遮罩，点击切换状态，如果有遮罩的文件但是没显示出遮罩，也可以点击这里刷新一下。\n隐藏遮罩的快捷键为【Ctrl + Y】,显示遮罩的快捷键为【Ctrl + L】",
            self.ui.refresh: "刷新当前视图，工作原理是根据绘制的遮罩替换主函数的颜色数组，再将遮罩传递给绘图.\n绘图区域出bug可以用这个抢救下。\n快捷键为【Ctrl + F】",
            self.ui.page_selector: "下拉菜单切换分页：如果一个下拉菜单放太多文件，会很卡",
            self.ui.openfiles: "打开文件夹，选择好后还要在右边的下拉菜单选择具体文件，然后点击选择文件，等待加载即可。\n文件夹内的内容有更新的时候，目录不会自动更新，需要先打开另一个文件夹，再打开要使用的文件夹，才会成功更新——因为打开和上次相同的路径时不会重新执行加载操作。",
            self.Main.ui.previousfile: "查看上一个文件，可以在设置界面根据自己的需求调整，以找到合适的加载时间。\n快捷键为【Ctrl + <】",
            self.Main.ui.nextfile: "查看下一个文件，这两个按钮会自动加载文件，不需要额外点击加载文件按钮。\n快捷键为【Ctrl + >】",
            self.Main.ui.showfiles: "展示文件的下拉框",
            self.Main.ui.selectfiles: "选择要处理的文件，文件加载好后在绘图区域绘制蒙版。\n按住shift键可以画直线和展示参考文件定位。\n点击ctrl可以将所有参考图像缩放平移到绘图窗口位置。\n按住alt可以拖动画布。\n滚动鼠标放大缩小。",
            self.ui.savepath: "保存文件夹路径，不一定要手输入，点击右边的搜索按钮可以弹出选择文件夹框\n（得先在输入框输点东西，点击才有用）",
            self.ui.preprocessing_code: "预处理代码必须是一个Python代码片段！详情点击右边的搜索按钮查看\n（不过必须先在输入框里输入一点文字，之后点击搜索按钮才有用）",
            self.ui.savefile: "将当前处理的文件保存成新的npz文件，遮罩数组会压在npz文件里面，再次用该软件打开即可加载遮罩。\n快捷键为【Ctrl + S】",
            self.ui.loadlastfile: "加载上一次保存的文件（如果你画完不满意想修改的话）\n快捷键为【Ctrl + G】",
            self.ui.correctingposition: "不同绘图函数绘制出来的图像位置都不一样，需要矫正才能让参考线足够标准。\n快捷键为【Ctrl + I】",
            self.ui.refreshmask: "刷新当前显示的遮罩（极坐标计算时间长），这东西主要是用来更新右边的参考遮罩\n如果你关了每一步绘图都自动显示遮罩的话，这个功能就非常有用。\n快捷键为【Ctrl + R】",
            self.ui.choosemaskselect: "筛选对应的遮罩类型，然后进行处理",
            self.ui.outputclearpic: "保存当前显示的参考图像（比如去掉了某些目标物的），注意，此时会创建一个名字为文件名的文件夹，储存在保存路径下面。\n后来这个功能被拓展成可以保存修改过后的npz或者npy文件。\n快捷键为【Ctrl + O】",
            self.ui.preprocessing: "点击执行预处理程序。\n快捷键为【Ctrl + P】",
            self.ui.importpainter: "导入自定义绘图函数，很重要的功能.\n毕竟每个人看习惯的图不一样，这个函数可以让用户使用自己的绘图函数作为参考图和输出图",
            self.ui.showall: "显示完整的原图。\n快捷键为【Ctrl + D】",
            self.ui.clearmask: "根据遮罩隐去原图的某些部分。\n快捷键为【Ctrl + T】",
            self.ui.savefileall: "渲染所有文件的图像（没有mask的npz文件则跳过），需要的时间非常长，没事别轻易点。\n我现在搞不定QT多线程，所以在跑图的时候软件必会卡住，建议挂着，跑的时候不要关闭软件。\n此时如果有命令行后台，则可以在命令行后台上看到进度条，前台弹窗也会有进度条，点掉之后如果程序还在跑，再点回来也能看到进度条。\n默认只渲染有蒙版的文件，不会渲染没有经过处理的文件，如果想要渲染所有文件，需要去设置里将对应的开关打开。",
            self.ui.showedge: "显示边缘提取的结果，这个按钮主要是用来画圈用的，有些模型训练的标记需要画圈。\n使用的是sobel算子进行边缘提取，计算量比较大，需要等很久。边缘提取的参数在设置界面调整。\n快捷键为【Ctrl + U】",
            self.ui.preprocessingall: "批量预处理所有文件，这个功能和批量渲染图片一样，因为没搞好多线程会导致窗口巨卡，没事不建议用，但是批量生成背景图之后可以加快加载速度（其实最初写这个功能就是这个目的）\n批量为npz文件生成背景图（生成一个源文件上附加键为“Background”的base64码的新npz文件）的预处理代码是：背景图片=生成背景图(雷达反射率)，先点击打开文件夹，选择要预处理的文件存放的文件夹。\n此时如果有命令行后台，则可以在命令行后台上看到进度条。\n前台也能看到弹窗进度条，如果批处理正在跑，点掉了再点回来也能看到进度条。"
        }

        for widget, tooltip in tooltips.items():
            widget.setToolTip(tooltip)
            widget.installEventFilter(ToolTipFilter(widget, showDelay=300, position=ToolTipPosition.TOP))

        # 原有的连接代码
        self.ui.showmask.clicked.connect(self.显示和消除遮罩按钮)
        self.ui.refresh.clicked.connect(self.刷新按钮)
        self.ui.page_selector.currentIndexChanged.connect(self.页码选择变化)
        self.ui.openfiles.clicked.connect(self.打开文件夹函数)
        self.Main.ui.previousfile.clicked.connect(self.上一个文件)
        self.Main.ui.nextfile.clicked.connect(self.下一个文件)
        self.Main.ui.showfiles.currentIndexChanged.connect(self.文件选择变化)
        self.Main.ui.selectfiles.clicked.connect(self.选择文件函数)
        self.ui.savepath.textChanged.connect(self.更新文件保存路径)
        self.ui.preprocessing_code.textChanged.connect(self.更新预处理代码)
        self.ui.savepath.setPlaceholderText("请输入文件保存路径")
        self.ui.savepath.searchSignal.connect(self.保存文件时打开文件浏览器)
        self.ui.preprocessing_code.setPlaceholderText("请输入预处理代码")
        self.ui.preprocessing_code.searchSignal.connect(self.打开预处理代码详细解释)
        self.ui.savefile.clicked.connect(self.保存函数)
        self.ui.loadlastfile.clicked.connect(self.加载上一个保存的文件)
        self.ui.correctingposition.clicked.connect(self.绑定校准函数)
        self.ui.refreshmask.clicked.connect(self.显示遮罩流程)
        self.ui.choosemaskselect.currentIndexChanged.connect(self.处理选择遮罩变化)
        self.ui.outputclearpic.clicked.connect(self.保存正在显示的预览图函数)
        self.ui.preprocessing.clicked.connect(self.预处理程序启动)
        self.ui.importpainter.clicked.connect(self.导入绘图函数按钮)
        self.ui.showedge.clicked.connect(lambda: (self.显示消息框函数("warning", "即将进行边缘提取", "这个功能需要等待很长时间，计算量很大", "底部"), QTimer.singleShot(100,self.边缘提取显示参考图)))
        self.ui.savefileall.clicked.connect(self.浮出批量保存图片进度条)
        self.ui.preprocessingall.clicked.connect(self.浮出批量预处理文件进度条)

        self.下拉框正在被占用 = False
        self.处理选择遮罩变化(1)
        self.ui.showall.clicked.connect(self.显示原始数组参考图)
        self.ui.clearmask.clicked.connect(self.根据遮罩数组显示参考图)

        if self.文件保存路径 != "":
            self.ui.savepath.setText(self.文件保存路径)
        if self.预处理代码 != "":
            self.ui.preprocessing_code.setText(self.预处理代码)


    ## 以下是一堆用来绑定按钮的函数，难倒是不难，就是又多又烦

    
    def 打开文件夹函数(self):
        if not QApplication.instance():
            app = QApplication([])  # 如果没有QApplication实例，则创建一个
        文件夹路径 = QFileDialog.getExistingDirectory(caption="选择要处理的文件所在文件夹的路径", dir = self.文件夹路径)  # 打开系统的文件夹选择对话框
        
        if 文件夹路径:  # 检查用户是否选择了文件夹
            self.文件夹路径 = 文件夹路径
            self.展示文件函数(文件夹路径)  # 调用展示文件函数
    

    @报错装饰器
    def 展示文件函数(self, folder_path, page=1, 需要文件解释=True, 是否第一次启动=False):
        if folder_path == "":
            logger.warning("没有缓存路径！")
            return 0
        # 如果是第一次调用或文件夹路径改变，重新扫描文件
        if self.Main.上一个文件 != folder_path or 是否第一次启动:
            需要页码解释 = True
            self.matched_files = []
            # 遍历folder_path目录及其所有子目录
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    # 检查文件名是否以'Z1_'开头并且以'.npz'结尾
                    if file.endswith('.npz'):
                        # 构建完整的文件路径并添加到列表中
                        self.matched_files.append(os.path.join(root, file).replace("/", "\\").replace(r"\\\\", "\\").replace(r"\\", "\\\\"))
            self.Main.上一个文件 = folder_path
            self.total_pages = (len(self.matched_files) + self.page_size - 1) // self.page_size
            self.Main.matched_files_dict = {os.path.basename(file): file for file in self.matched_files}
            if not 是否第一次启动:
                self.正在使用的文件索引 = -1  # 重置当前文件索引

        else:
            需要页码解释 = False

        # 如果没有找到匹配的文件，显示一个消息框
        if self.matched_files == []:
            self.显示消息框函数("warning", "没有找到匹配的文件", "请检查文件夹路径是否正确！")
            return

        # 确保页码在有效范围内
        self.正在使用的页数  = max(1, min(page, self.total_pages))

        # 计算当前页应显示的文件
        start_index = (self.正在使用的页数  - 1) * self.page_size
        end_index = start_index + self.page_size
        current_page_files = self.matched_files[start_index:end_index]

        # 更新文件名和索引的字典
        self.Main.filesnames = {os.path.basename(file): file for file in current_page_files}
        logger.info("已经定义了文件名字典")
        self.Main.filenames_to_index = {os.path.basename(file): index for index, file in enumerate(current_page_files)}
        self.Main.index_to_filenames = {index: os.path.basename(file) for index, file in enumerate(current_page_files)}

        # 更新文件相关按钮
        self.更新文件相关按钮(需要文件解释,需要页码解释)

    def 更新文件相关按钮(self,需要文件解释=True,需要页码解释=True):
        # 更新文件名选择框
        self.Main.ui.showfiles.clear()
        if 需要文件解释:
            self.Main.ui.showfiles.addItems(["选择要打开的文件"] + list(self.Main.filesnames.keys()))
        else:
            self.Main.ui.showfiles.addItems(list(self.Main.filesnames.keys()))

        # 更新页码下拉框
        self.Main.ui.page_selector.blockSignals(True)
        self.Main.ui.page_selector.clear()
        if 需要页码解释:
            self.Main.ui.page_selector.addItems(["选择页码"]+[f"第{i}页" for i in range(1, self.total_pages + 1)])
            self.Main.ui.page_selector.setCurrentIndex(self.正在使用的页数  - 1)
        else:
            self.Main.ui.page_selector.addItems([f"第{i}页" for i in range(1, self.total_pages + 1)])
            self.Main.ui.page_selector.setCurrentIndex(self.正在使用的页数  - 1)
        self.Main.ui.page_selector.blockSignals(False)

        # 更新上一个文件和下一个文件按钮的状态
        self.更新文件按钮状态()

    def 更新文件按钮状态(self):
        # 禁用或启用上一个文件和下一个文件按钮
        self.Main.ui.previousfile.setEnabled(self.正在使用的页数  > 1 or self.正在使用的文件索引 > 0)
        self.Main.ui.nextfile.setEnabled(self.正在使用的页数  < self.total_pages or self.正在使用的文件索引 < len(self.Main.filesnames) - 1)

    def 更新文件相关配置项(self, num, 是否直接赋值=False):
        
        #logger.info("更新文件相关配置项")
        if 是否直接赋值:
            self.正在使用的文件索引 = num
        else:
            self.正在使用的文件索引 += num
        self.正在使用的文件名字 = self.Main.index_to_filenames[self.正在使用的文件索引]
        #logger.info(f"正在使用的文件名字为：{self.正在使用的文件名字}")
        self.当前使用的文件路径 = self.Main.matched_files_dict[self.正在使用的文件名字]
        #logger.info(f"当前使用的文件路径为：{self.当前使用的文件路径}")


    def 上一个文件(self):
        if self.正在使用的文件索引 > 0:
            self.更新文件相关配置项(-1)
        else:
            if self.正在使用的页数  > 1:
                # 设置选中最后一个文件
                self.更新文件相关配置项(self.page_size - 1, True)
                self.展示文件函数(self.文件夹路径, self.正在使用的页数  - 1, False)
        self.选择文件(self.正在使用的文件索引)

    def 下一个文件(self):
        if self.正在使用的文件索引 < len(self.Main.filesnames) - 1:
            self.更新文件相关配置项(1)
            
        else:
            if self.正在使用的页数  < self.total_pages:
                # 设置选中第一个文件
                self.更新文件相关配置项(0, True)
                self.展示文件函数(self.文件夹路径, self.正在使用的页数  + 1, False)
        self.选择文件(self.正在使用的文件索引)

    def 选择文件(self, index):
        if 0 <= index < len(self.Main.filesnames):
            self.更新文件相关配置项(index, True)
            if self.page_size == self.Main.ui.showfiles.count():
                self.Main.ui.showfiles.setCurrentIndex(index)
            else:
                self.Main.ui.showfiles.setCurrentIndex(index + 1)  # +1 因为第一项是 "选择要打开的文件"
            self.更新文件按钮状态()
            # 这里可以添加处理选中文件的逻辑，比如打开文件等
            self.选择文件函数(self.当前使用的文件路径)

    def 页码选择变化(self, index):
        if self.Main.ui.page_selector.count() == self.total_pages:
            selected_page = index + 1
            self.展示文件函数(self.文件夹路径, selected_page)
        else:
            selected_page = index
            self.展示文件函数(self.文件夹路径, selected_page)

    def 文件选择变化(self, index):
        if index == 0 and self.Main.ui.showfiles.count()!= self.page_size:
            return
        self.更新文件按钮状态()
        self.更新文件相关配置项(index - 1, True)
        # 这里可以添加处理选中文件的逻辑



    
    @报错装饰器
    def 选择文件函数(self, path=None):
        self.判断参考图是否经过预处理标志位 = False
        self.判断参考图是否经过边缘提取标志位 = False
        logger.info("触发选择文件函数")
        if path == None:
            path = self.当前使用的文件路径  # 假设 self.当前文件路径 是存储当前文件路径的属性
        self.显示进度条(True)
        QApplication.processEvents()
        self.将新的文件加载到webview中(self.从文件得到全局数组(path))
        QTimer.singleShot(8000, lambda: self.显示进度条(False))





    # 这个按钮主要是图像出问题了再使用的
    def 刷新按钮(self):
        logger.info("开始刷新遮罩")
        self.消除遮罩函数()
        self.显示遮罩函数()



    def 显示和消除遮罩按钮(self):
        # 更新按钮文本来反映当前状态
        if self.Main.按钮状态.是否显示遮罩:
            self.消除遮罩函数()
            self.ui.showmask.setText("显示遮罩")
        else:
            self.显示遮罩函数()
            self.ui.showmask.setText("隐藏遮罩")

        # 切换遮罩的显示状态
        self.Main.按钮状态.是否显示遮罩 = not self.Main.按钮状态.是否显示遮罩
        
    
    def 显示遮罩函数(self):
        # 让网页清空遮罩，然后将colormask数组传递给js，让js重新绘制遮罩，直接对painter对象跑js代码
        self.ui.painter.page().runJavaScript("clearCanvasCompletely(canvas);")# 清空遮罩
        logger.info("显示遮罩时候的发送")
        self.Main.bridge.requestMuskArrayFromPython()#向js发送颜色数组
        time.sleep(0.1)
        self.ui.painter.page().runJavaScript("drawColorArrayOnCanvas(maskArray_color);")# 重新绘制遮罩
    
    def 消除遮罩函数(self):
        # 先将遮罩数据传递回主函数，再让网页清空遮罩，直接对painter对象跑js代码
        self.ui.painter.page().runJavaScript("sendMuskArrayToPython();")# 让js发送遮罩数组回主函数
        self.ui.painter.page().runJavaScript("clearCanvasCompletely(canvas);")# 清空遮罩

    def 更新文件保存路径(self):
        # 读取SearchLineEdit的文本作为保存路径
        保存路径 = self.ui.savepath.text()
        # 保存路径
        self.文件保存路径 = 保存路径

    def 更新预处理代码(self):
        # 读取SearchLineEdit的文本作为预处理代码
        预处理代码 = self.ui.preprocessing_code.text()
        # 保存预处理代码
        self.预处理代码 = 预处理代码

    @报错装饰器
    def 保存函数(self):
        self.ui.painter.page().runJavaScript("sendMuskArrayToPython();")  # 让js发送遮罩数组回主函数
        save_dict = dict()
        time.sleep(0.1)
        for i in self.Main.当前使用numpy数组和内部数据字典:
            save_dict[i[3]] = i[2]
        save_dict["Musk"] = self.Main.数值遮罩数组
        save_dict["Musk_nan"] = self.Main.nan遮罩数组
        if "Background" in self.Main.当前使用numpy数组:
            save_dict["Background"] = self.Background图片

        def 校验文件路径(路径):
            # 检查路径是否存在
            if os.path.exists(路径):
                # 检查路径是否可写
                if os.access(路径, os.W_OK):
                    return True
                else:
                    logger.error("保存文件时路径不可写")
                    return False
            else:
                logger.error("保存文件时路径不存在")
                return False

        if self.文件保存路径!="" and 校验文件路径(self.文件保存路径):
            save_path = os.path.join(self.文件保存路径, re.sub(r"(\.npz|_Mask|_预处理)", "", self.正在使用的文件名字) + "_Mask.npz")
        elif self.文件保存路径 == "":
            self.显示消息框函数("warning", "保存路径为空", "将存入来源文件路径，但文件名会有所不同。")
            save_path = os.path.join(os.path.dirname(self.当前使用的文件路径), re.sub(r"(\.npz|_Mask|_预处理)", "", self.正在使用的文件名字) + "_Mask.npz")
        elif 校验文件路径(self.文件保存路径) == False:
            self.显示消息框函数("error", "保存路径不可用", "请重新输入，单击右边的搜索框可以唤起文件选择对话框。")
            return
        # 使用获取的保存路径保存npz文件
        np.savez(save_path, **save_dict)
        self.上一个处理的文件路径 = save_path

    @报错装饰器
    def 保存修改过后的数据函数(self, 使用的保存数组 = dict(), 正在使用的文件名字 = "", 文件保存路径 = "" , 当前使用的文件路径 = "", 雷达缩写对应名字 = ""):
        需要处理的数字 = []
        for key in self.全局遮罩选择菜单状态:
            if self.全局遮罩选择菜单状态[key]["选择状态"] == 1:
                需要处理的数字.append(self.全局遮罩选择菜单状态[key]["代表的数值"])
        需要处理的内容 = "-".join([self.Main.图像判别数字转换成类型[int(i)] for i in 需要处理的数字])
        def 校验文件路径(路径):
            # 检查路径是否存在
            if os.path.exists(路径):
                # 检查路径是否可写
                if os.access(路径, os.W_OK):
                    return True
                else:
                    logger.error("保存图像同时保存修改过后的数据时路径不可写")
                    return False
            else:
                logger.error("保存图像同时保存修改过后的数据时路径不存在")
                return False

        文件名基础 = re.sub(r"(\.npz|_Mask|_已修改|_预处理)", "", 正在使用的文件名字)
        if 文件保存路径 != "" and 校验文件路径(文件保存路径):
            save_path = os.path.join(文件保存路径, 文件名基础, 文件名基础 + "_已修改").replace("/", "\\")
        elif 文件保存路径 == "":
            self.显示消息框函数("warning", "保存路径为空", f"将存入来源文件路径，但会放在同名文件夹下面，保存路径为{os.path.dirname(当前使用的文件路径)}")
            save_path = os.path.join(os.path.dirname(当前使用的文件路径), 文件名基础, 文件名基础 + "_已修改").replace("/", "\\")
        elif not 校验文件路径(文件保存路径):
            self.显示消息框函数("error", "保存路径不可用", "请重新输入，单击右边的搜索框可以唤起文件选择对话框。")
            return
        # 使用获取的保存路径保存npz文件
        if self.是否渲染导出时输出的npz文件按照图片类型分类:
            for 类型, 数组 in 使用的保存数组.items():
                if self.判断参考图是否经过预处理标志位 == True:
                    文件名 = os.path.dirname(save_path) + f"\\{雷达缩写对应名字[类型]}-{文件名基础}┃消去【{需要处理的内容}】"
                else:
                    文件名 = os.path.dirname(save_path) + f"\\{雷达缩写对应名字[类型]}-{文件名基础}"
                目录名 = os.path.dirname(文件名)
                if not os.path.exists(目录名):
                    os.makedirs(目录名)
                np.save(文件名, 数组)
            self.显示消息框函数("seccess", "保存成功", f"已经将处理后的数据保存在【{os.path.dirname(save_path)}】目录下")
        else:
            目录名 = os.path.dirname(save_path)
            if not os.path.exists(目录名):
                os.makedirs(目录名)
            if self.判断参考图是否经过预处理标志位 == True:
                np.savez(save_path.replace("_已修改", f"┃消去【{需要处理的内容}】_已修改"), **使用的保存数组)
            else:
                np.savez(save_path, **使用的保存数组)
            self.显示消息框函数("seccess", "保存成功", f"已经将处理后的数据保存在【{os.path.dirname(save_path)}】目录下")



    @报错装饰器
    def 加载上一个保存的文件(self):
        if self.上一个处理的文件路径 != "":
            self.将新的文件加载到webview中(self.从文件得到全局数组(self.上一个处理的文件路径))
        else:
            self.显示消息框函数("error", "没有文件路径", "请先保存文件再加载")


    def 绑定校准函数(self):
        self.Main.校准函数是否开启 = True
        for i in self.webviews:
            i.page().runJavaScript("CalibrationFlagPosition = true;")
        if self.Main.是否使用极坐标:
            self.显示消息框函数("success", "即将开始极坐标图例位置校准", "点击某一张图以启动，需要在同一个参考图里获取两次鼠标位置，鼠标移动过去，按下空格获取位置，第一次获取到极坐标最中心，第二次获取到极坐标半径", "底部",30000)
        else:
            self.显示消息框函数("success", "即将开始直角坐标图例位置校准", "点击某一张图以启动，需要在同一个参考图里点击两次，鼠标移动过去，按下空格获取位置，第一次获取到直角坐标最左上角，第二次获取到直角坐标最右下角", "底部",30000)


    @报错装饰器
    def 处理选择遮罩变化(self,参数=None):
        if self.下拉框正在被占用 == True:
            return
        self.下拉框正在被占用 = True
        # 获取当前选中项的索引和文本
        currentIndex = self.ui.choosemaskselect.currentIndex()
        currentText = self.ui.choosemaskselect.currentText().replace(" √","")
        
        if currentText != "请选择遮罩类型" and currentText != "" or 参数 != None:
            if currentText != "请选择遮罩类型" and currentText:
                if self.全局遮罩选择菜单状态[currentText]["选择状态"] == 0:
                    self.全局遮罩选择菜单状态[currentText]["选择状态"] = 1
                else:
                    self.全局遮罩选择菜单状态[currentText]["选择状态"] = 0

            itemlist = []
            # 添加新项
            for key in self.全局遮罩选择菜单状态:
                itemstr = key
                if self.全局遮罩选择菜单状态[key]["选择状态"] == 1:
                    logger.success(f"添加√  {key}")
                    itemstr = itemstr + " √"
                itemlist.append(itemstr)
            # 刷新所有向
            self.ui.choosemaskselect.clear()
            self.ui.choosemaskselect.addItems(["请选择遮罩类型"]+itemlist)
            
        if 参数!=None:
            # 设置选中状态为当前项
            if currentIndex == -1:
                currentIndex = 0
            self.ui.choosemaskselect.setCurrentIndex(currentIndex)
        time.sleep(0.1)
        self.下拉框正在被占用 = False

    def 显示原始数组参考图(self):
        self.判断参考图是否经过预处理标志位 = False
        self.判断参考图是否经过边缘提取标志位 = False
        self.初始化参考图像函数()
        self.显示消息框函数("success", "加载图像", f"将要加载{len(self.Main.当前使用numpy数组和内部数据字典)}个图像","底部")

    def 根据遮罩数组显示参考图(self):
        self.判断参考图是否经过预处理标志位 = True
        self.初始化参考图像函数()
        self.显示消息框函数("success", "加载遮罩隐去图像", f"将要加载{len(self.Main.当前使用numpy数组和内部数据字典)}个图像","底部")

    def 边缘提取显示参考图(self):
        self.判断参考图是否经过边缘提取标志位 = True
        self.显示消息框函数("warning", "即将进行边缘提取", "这个功能需要等待很长时间，计算量很大", "底部")
        self.生成边缘坐标字典()
        self.初始化参考图像函数()
        self.显示消息框函数("success", "加载边缘提取图像", f"将要加载{len(self.Main.当前使用numpy数组和内部数据字典)}个图像","底部")
    
    @报错装饰器
    def 根据遮罩数组处理原始图像(self, ori_array,数值遮罩数组=None):
        需要处理的数字 = []
        if 数值遮罩数组 is None:
            判定用的数组 = self.Main.数值遮罩数组.copy()
        else:
            判定用的数组 = 数值遮罩数组
        # 遍历全局遮罩选择菜单状态，如果选择状态为1，则将代表的数值添加到需要处理的数字列表中
        for key in self.全局遮罩选择菜单状态:
            if self.全局遮罩选择菜单状态[key]["选择状态"] == 1:
                需要处理的数字.append(self.全局遮罩选择菜单状态[key]["代表的数值"])
        logger.info(f"需要处理的数字为：{需要处理的数字}")
        # 将ori_array里面和self.Main.数值遮罩数组 里面的值都在需要处理的数字的位置，对应位置的值改为np.nan
        for i in range(ori_array.shape[0]):
            for j in range(ori_array.shape[1]):
                if 判定用的数组[i, j] in 需要处理的数字:
                    ori_array[i, j] = np.nan
        return ori_array
    

    @报错装饰器
    def 生成边缘坐标字典(self):
        """
        不需要输入任何参数
        1. 先根据选择的天气类型，将对应的边缘坐标提取出来，成为字典
        2. 返回值是字典，这个字典会传递给绘图函数
        """
        logger.info("开始生成边缘坐标字典")
        self.最终传递的边缘数组字典 = dict()
        需要处理的数字 = []
        for key in self.全局遮罩选择菜单状态:
            if self.全局遮罩选择菜单状态[key]["选择状态"] == 1:
                需要处理的数字.append(self.全局遮罩选择菜单状态[key]["代表的数值"])
        ### 遍历这些数字，从数值遮罩数组中创建用于边缘提取的数组（只有黑白两色，等于数字的是白色，不等于数字的是黑色）
        for i in 需要处理的数字:
            边缘提取数组 = np.where(self.Main.数值遮罩数组 == i, self.Main.图像判别数字转换成颜色[i], "#000000")
            # 检查边缘提取数组中的唯一值
            唯一值 = np.unique(边缘提取数组)
            # 如果唯一值只包含"#000000"，则跳过后续部分
            if 唯一值.size == 1 and 唯一值[0] == "#000000":
                self.显示消息框函数("error", "边缘提取数组全为黑色", f"没有{self.Main.图像判别数字转换成类型[i]}的数据")
                logger.error(f"没有{self.Main.图像判别数字转换成类型[i]}的数据")
                logger.info(f"{self.Main.数值遮罩数组}")
            else:
                # 后续代码部分 
                绘图坐标列表 = self.边缘提取中间函数(边缘提取数组,self.Main.是否使用极坐标)
                self.最终传递的边缘数组字典[self.Main.图像判别数字转换成颜色[i]] = 绘图坐标列表
        

    @报错装饰器
    def 保存正在显示的预览图函数(self):
        self.初始化参考图像函数(是否保存文件=True)
        if self.是否输出渲染图片同时保存当前修改:
            self.保存函数()
        if self.是否输出渲染图片时输出对应的修改后npz文件:
            使用的保存数组 = dict()
            for i in self.Main.当前使用numpy数组和内部数据字典:
                使用的保存数组[i[3]] = self.根据遮罩数组处理原始图像(i[2].copy())
            self.保存修改过后的数据函数(使用的保存数组, self.正在使用的文件名字, self.文件保存路径, self.当前使用的文件路径, self.Main.雷达缩写对应名字)
        self.显示消息框函数("success", "加载图像", f"将要加载{len(self.Main.当前使用numpy数组和内部数据字典)}个图像","底部")


    @报错装饰器
    def 预处理函数(self,是否第一次启动=True,主窗口类的当前使用的numpy数组=None,主窗口类的雷达缩写对应名字=None,类的数值遮罩数组=None,类的缺失值遮罩数组=None,是否使用极坐标=None, 当前使用的文件名字=None):
        global 展示,保存,载入,缓存遮罩1,缓存遮罩2,缓存遮罩3,缓存遮罩4,缓存遮罩5,遮罩,缺失值数组,生成背景图,背景图片,当前文件名,Mainobject,apiobject,uiobject
        # 预处理代码
        if 主窗口类的当前使用的numpy数组 == None:
            logger.error("没有输入参数")
            return
        if type(主窗口类的当前使用的numpy数组) != dict:
            logger.error(f"输入参数类型错误：{type(主窗口类的当前使用的numpy数组)},{主窗口类的当前使用的numpy数组}")
            return
        logger.info(f"接收到的输入参数为：{主窗口类的当前使用的numpy数组.keys()}")
        预处理代码 = self.ui.preprocessing_code.text()
        for key, value in self.图像类型对应的源文件的key.items():
            QCoreApplication.processEvents()
            try:
                globals()[key] = pd.DataFrame(主窗口类的当前使用的numpy数组[value])
            except:
                if 是否第一次启动:
                    logger.info(f"没有当前使用文件中key：{key}的数据")
        # 如果预处理代码中使用到上n个文件
        if re.search(r"上\d个", 预处理代码):
            for i in range(len(self.上一个文件的文件路径[:-1])):
                QCoreApplication.processEvents()
                try:
                    datapre = np.load(self.上一个文件的文件路径[i])
                except:
                    logger.error(f"上{len(self.上一个文件的文件路径[:-1])-i}个文件的路径不正确，本次预处理无法使用上一个文件数据")
                    continue
                for key, value in datapre.items():
                    QCoreApplication.processEvents()
                    try:
                        globals()[f"上{len(self.上一个文件的文件路径[:-1])-i}个"+主窗口类的雷达缩写对应名字[key]] = pd.DataFrame(value)
                    except:
                        if 是否第一次启动:
                            logger.info(f"没有前{len(self.上一个文件的文件路径[:-1])-i}个文件中key：{key}的数据")
        
        if 类的数值遮罩数组 is not None:
            遮罩 = pd.DataFrame(类的数值遮罩数组)
        else:
            遮罩 = None
        if 类的缺失值遮罩数组 is not None:
            缺失值数组 = pd.DataFrame(类的缺失值遮罩数组)
        else:
            缺失值数组 = None

        缓存遮罩1 = self.缓存遮罩1.copy()
        缓存遮罩2 = self.缓存遮罩2.copy()
        缓存遮罩3 = self.缓存遮罩3.copy()
        缓存遮罩4 = self.缓存遮罩4.copy()
        缓存遮罩5 = self.缓存遮罩5.copy()

        Mainobject = self.Main
        apiobject = self
        uiobject = self.ui

        当前文件名 = 当前使用的文件名字
        

        # 映射函数名字
        展示 = self.用于预处理将数值遮罩数组转换并显示图片
        保存 = self.储存缓存遮罩
        载入 = self.读取缓存遮罩
        def 生成背景图(array):
            base64data = self.从原始numpy数组绘制坐标图(array,是否使用极坐标)
            return base64data

        
        def 转化为分钟数(时间字符串):
            分割的时间 = 时间字符串.split("时")
            小时 = 分割的时间[0]
            分钟 = 分割的时间[1].replace("分", "")
            小时数 = int(小时)
            分钟数 = int(分钟)
            总分钟数 = 小时数 * 60 + 分钟数
            return 总分钟数

        def 替换时间为分钟数(原文本):
            # 正则表达式匹配格式为“\d\d时\d\d分”的字符串
            时间模式 = r'\d\d时\d\d分'
            
            # 使用正则表达式找到所有匹配项
            所有匹配项 = re.findall(时间模式, 原文本)
            
            # 对于每一个匹配项，计算分钟数并替换原字符串
            for 时间字符串 in 所有匹配项:
                分钟数 = 转化为分钟数(时间字符串)
                原文本 = 原文本.replace(时间字符串, str(分钟数))
            
            return 原文本

        # 新增：替换图像类型对应的不同对象的选择数值字典的键为对应的值
        for key, value in self.Main.图像判别类型转换成数字.items():
            预处理代码 = re.sub(r'\b' + re.escape(key) + r'\b', str(value), 预处理代码)
        
        预处理代码 = 预处理代码.replace("（","(").replace("）",")").replace("【","[").replace("】","]").replace("；",";").replace("，",",").replace("：",":").replace("。",".").replace("“",'"').replace("”",'"').replace("‘","'").replace("’","'").replace("？","?").replace("！", "!").replace("、", ",").replace("…", "...").replace("—", "-").replace("～", "~").replace("·", ".").replace("《", "<").replace("》", ">").replace("「", "{").replace("」", "}").replace("【", "[").replace("】", "]").replace("￥", "$").replace("％", "%").replace("＃", "#").replace("＆", "&").replace("＊", "*").replace("＋", "+").replace("－", "-").replace("／", "/").replace("＝", "=").replace("＠", "@").replace("＾", "^").replace("｜", "|").replace("＼", "\\").replace("＂", '"').replace("＇", "'").replace("＿", "_").replace("｀", "`").replace("＂", '"').replace("＇", "'").replace("＿", "_").replace("｀", "`")

        预处理代码 = 替换时间为分钟数(预处理代码)

        if not 是否第一次启动:
            class RemovePrintAndShowTransformer(ast.NodeTransformer):
                def visit_Call(self, node):
                    if (isinstance(node.func, ast.Name) and node.func.id in ('print', '展示')):
                        # 返回一个空的pass语句节点
                        return ast.Pass()
                    return self.generic_visit(node)

            # 解析Python代码为AST
            tree = ast.parse(预处理代码)

            # 使用RemovePrintAndShowTransformer转换AST
            transformer = RemovePrintAndShowTransformer()
            new_tree = transformer.visit(tree)

            # 将修改后的AST转换回代码
            预处理代码 = astor.to_source(new_tree)

        if self.预处理函数代码print替换 == True:
            class PrintTransformer(ast.NodeTransformer):
                def visit_Call(self, node):
                    if isinstance(node.func, ast.Name) and node.func.id == 'print':
                        # 构造FormattedValue节点列表
                        formatted_values = [ast.FormattedValue(value=arg, conversion=-1, format_spec=None) for arg in node.args]
                        
                        # 构造JoinedStr节点
                        joined_str = ast.JoinedStr(values=formatted_values)
                        
                        # 构造新的函数调用
                        new_node = ast.Call(
                            func=ast.Attribute(
                                value=ast.Name(id='self', ctx=ast.Load()),
                                attr='显示消息框函数',
                                ctx=ast.Load()
                            ),
                            args=[
                                ast.Str(s='info'),
                                ast.Str(s='输出信息'),
                                joined_str,  # 将所有参数组合成一个f-string
                                ast.Str(s='底部'),
                                ast.Num(n=40000)
                            ],
                            keywords=[]
                        )
                        return ast.copy_location(new_node, node)
                    return self.generic_visit(node)
                
            # 解析Python代码为AST
            tree = ast.parse(预处理代码)

            # 转换AST
            transformer = PrintTransformer()
            new_tree = transformer.visit(tree)

            # 将修改后的AST转换回代码
            预处理代码 = astor.to_source(new_tree)

        # 将预处理代码中的类属性指向全局属性
        预处理代码 = 预处理代码.replace("self.Main", "Mainobject").replace("self.ui", "uiobject").replace("self", "apiobject")

        logger.info(f"预处理代码：{预处理代码}")



        # 执行对应的预处理代码
        try:
            exec(预处理代码, globals())
        except Exception as e:
            if self.是否需要完整报错信息:
                error_info = traceback.format_exc()
                self.显示消息框函数("error", "预处理代码格式不规范", f"错误信息:{e}\n\n{error_info}", "底部",60000)
                logger.error(f"错误信息:{e}\n\n{error_info}")
            else:
                self.显示消息框函数("error", "预处理代码格式不规范", f"错误信息:{e}", "底部",60000)
                logger.error(f"错误信息:{e}")

        self.专门整一个函数用来保存数据看看(遮罩,缺失值数组)
        # 从exec_namespace的缓存变量字典中提取更新后的值
        self.保存缓存遮罩("缓存遮罩1", 缓存遮罩1)
        self.保存缓存遮罩("缓存遮罩2", 缓存遮罩2)
        self.保存缓存遮罩("缓存遮罩3", 缓存遮罩3)
        self.保存缓存遮罩("缓存遮罩4", 缓存遮罩4)
        self.保存缓存遮罩("缓存遮罩5", 缓存遮罩5)

        # self.用于预处理将数值遮罩数组转换并显示图片(遮罩)

    @报错装饰器
    def 专门整一个函数用来保存数据看看(self,array,array2):
        if array is not None:
            self.Main.数值遮罩数组 = np.array(array)
        if array2 is not None:
            self.Main.nan遮罩数组 = np.array(array2)
        # 将nan值遮罩数组为0的地方也让数值遮罩数组为0
        try:
            if array is not None:
                self.Main.数值遮罩数组 = np.where(self.Main.nan遮罩数组 == 0, 0, self.Main.数值遮罩数组)
                self.Main.颜色遮罩数组 = np.array(self.将数值遮罩数组转换为颜色遮罩数组(self.Main.数值遮罩数组))
            if array2 is not None and array is None:
                self.Main.数值遮罩数组 = np.where(self.Main.nan遮罩数组 == 0, 0, self.Main.数值遮罩数组)
            if array2 is not None:
                self.Main.nan颜色数组 = np.array(self.将数值遮罩数组转换为颜色遮罩数组(self.Main.nan遮罩数组))
        except:
            pass
    
    @报错装饰器
    def 保存缓存遮罩(self, 缓存遮罩名称, 缓存遮罩数组):
        setattr(self, 缓存遮罩名称, 缓存遮罩数组.copy())
    
    @报错装饰器
    def 储存缓存遮罩(self):
        # 创建一个字典，用于存储缓存遮罩1~5及其对应的值
        缓存数据 = {}
        for i in range(1, 6):
            缓存键 = f'缓存遮罩{i}'
            缓存值 = getattr(self, 缓存键)
            # 判断缓存值的类型
            if isinstance(缓存值, pd.DataFrame):
                缓存值 = 缓存值.values  # 如果是DataFrame，则取其.values
            缓存数据[缓存键] = 缓存值
        
        # 获取当前时间，并格式化为指定的字符串格式
        当前时间 = datetime.now().strftime('%Y年%m月%d日%H时%M分%S秒')
        文件名 = f'{当前时间}缓存遮罩数据'
    
        # 使用numpy的savez函数创建npz文件，文件名为指定的格式
        np.savez(os.path.join(self.文件保存路径,文件名), **缓存数据)

    @报错装饰器
    def 读取缓存遮罩(self, 文件序号=1, path=None):
        if path == None:
        # 获取当前目录下所有的npzz文件
            文件列表 = [os.path.join(self.文件保存路径, 文件) for 文件 in os.listdir(self.文件保存路径) if 文件.split(".")[0].endswith('缓存遮罩数据')]
            # 按照时间从新到旧排序文件
            文件列表.sort(key=lambda x: datetime.strptime(x.split('缓存遮罩数据')[0], '%Y年%m月%d日%H时%M分%S秒'), reverse=True)
            # 根据输入参数选择文件
            if 文件序号 <= len(文件列表) and 文件序号 > 0:
                文件名 = 文件列表[文件序号 - 1]
            else:
                logger.error("输入的文件序号超出范围")
                return
        
        else:
            文件名 = path
        # 读取npzz文件
        数据 = np.load(文件名, allow_pickle=True)
        
        # 将读取的数据赋值给self的属性
        for i in range(1, 6):
            缓存键 = f'缓存遮罩{i}'
            setattr(self, 缓存键, 数据[缓存键])  
    
    @报错装饰器
    def 用于预处理将数值遮罩数组转换并显示图片(self, 数值遮罩数组):
        '''
        输入数值遮罩数组，输出颜色遮罩数组并显示图片
        '''

        数值遮罩数组 = np.array(数值遮罩数组)
        if 数值遮罩数组.dtype == bool:
            数值遮罩数组 = 数值遮罩数组.astype(int)
        数值遮罩数组 = np.nan_to_num(数值遮罩数组)
        # 检查输入是否为布尔数组，如果是则转换为数值数组
        if 数值遮罩数组.dtype == bool:
            数值遮罩数组 = 数值遮罩数组.astype(int)
        try:
            # 将数值遮罩数组转换为颜色遮罩数组
            颜色遮罩数组 = np.empty_like(数值遮罩数组, dtype=object)
            for i in range(数值遮罩数组.shape[0]):
                for j in range(数值遮罩数组.shape[1]):
                    颜色遮罩数组[i, j] = self.Main.图像判别数字转换成颜色[数值遮罩数组[i, j]]

            logger.info(f"查看输入painter数组尺寸：{len(颜色遮罩数组)},{len(颜色遮罩数组[0])}")

            if self.Main.是否使用极坐标:
                # 颜色遮罩数组的预处理
                    hex_colors = np.array(颜色遮罩数组).flatten()
                    hex_colors = np.flip(hex_colors, 0)
                    hex_colors = np.concatenate((hex_colors[179:], hex_colors[:179]), axis=0)

                    # 直接从十六进制颜色到RGBA数组的转换
                    hex_to_rgba = np.vectorize(lambda x: [int(x[1:3], 16), int(x[3:5], 16), int(x[5:7], 16), 255] if x.startswith('#') and len(x) == 7 else [255, 255, 255, 255])

                    rgba_array = np.array(hex_to_rgba(hex_colors)).reshape(hex_colors.shape[0], hex_colors.shape[1], 4)
                    rgba_array = rgba_array / 255.0  # 正常化到 [0, 1]

                    # 转换为极坐标
                    theta = np.linspace(0, 2 * np.pi, rgba_array.shape[1])
                    r = np.linspace(0, 1, rgba_array.shape[0])
                    theta, r = np.meshgrid(theta, r)

                    # 创建极坐标图
                    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
                    ax.set_aspect('auto')

                    # 绘制数据
                    for i in range(rgba_array.shape[0]):
                        ax.pcolormesh(theta[i:i+2], r[:,i:i+2], np.zeros((2, 2)), color=rgba_array[i])

                    # 隐藏坐标轴
                    ax.axis('off')

                    # 显示图像
                    plt.show()
            else:
                # 将遮罩数组左右颠倒和转置
                颜色遮罩数组 = 颜色遮罩数组.T
                颜色遮罩数组 = np.flipud(颜色遮罩数组)
            
                # 直接从十六进制颜色到RGBA数组的转换
                颜色遮罩数组 = np.vectorize(lambda x: int(x[1:], 16) if x.startswith('#') and len(x) == 7 else 16777215)(颜色遮罩数组)
                
                r = (颜色遮罩数组 >> 16) & 0xFF
                g = (颜色遮罩数组 >> 8) & 0xFF
                b = 颜色遮罩数组 & 0xFF
                a = np.full(颜色遮罩数组.shape, 255)

                rgba_array = np.stack((r, g, b, a), axis=-1)

                # 用matplotlib显示图像
                plt.imshow(rgba_array.astype('uint8'))
                plt.axis('off')  # 隐藏坐标轴
                plt.show()
        except:
            if self.Main.是否使用极坐标:
                数值遮罩数组 = np.flip(数值遮罩数组,0)

                数值遮罩数组 = np.concatenate((数值遮罩数组[-90:], 数值遮罩数组[:-90]), axis=0)# 逆时针旋转90度
                # 获取数组的尺寸
                num_angles, num_radii = 数值遮罩数组.shape

                # 创建角度和半径的网格
                angles = np.linspace(0, 2 * np.pi, num_angles, endpoint=False)  # 将角度转换为弧度
                radii = np.linspace(0, 1, num_radii)

                # 创建极坐标网格
                angles, radii = np.meshgrid(angles, radii)

                # 创建极坐标图
                fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

                # 显示数据
                c = ax.pcolormesh(angles, radii, 数值遮罩数组.T, shading='auto')

                # 隐藏坐标轴
                ax.axis('off')

                # 显示图像
                plt.show()

            else:
                # 用matplotlib显示图像
                plt.imshow(数值遮罩数组)
                plt.axis('off')  # 隐藏坐标轴
                plt.show()


    @报错装饰器
    def 预处理程序启动(self,是否在打开文件时调用=False):
        if 是否在打开文件时调用:
            临时变量 = False
        else:
            临时变量 = True
        self.预处理函数(False, self.Main.当前使用numpy数组, self.Main.雷达缩写对应名字, self.Main.数值遮罩数组, self.Main.nan遮罩数组, self.Main.是否使用极坐标, self.正在使用的文件名字)
        self.预处理函数(临时变量, self.Main.当前使用numpy数组, self.Main.雷达缩写对应名字, self.Main.数值遮罩数组, self.Main.nan遮罩数组, self.Main.是否使用极坐标, self.正在使用的文件名字)
        if not self.预处理函数只显示输出信息:
            self.显示遮罩函数()
            self.显示遮罩流程()

    @报错装饰器
    def 保存文件时打开文件浏览器(self, 用不到的 =  ""):

        # 打开文件浏览器
        logger.info("打开文件浏览器")
        文件保存路径 = QFileDialog.getExistingDirectory(caption="选择文件保存路径", dir = self.文件保存路径)
        if 文件保存路径:  # 检查用户是否选择了文件夹
            self.文件保存路径 = 文件保存路径
        # 更新SearchLineEdit的文本
        self.ui.savepath.setText(self.文件保存路径)

    @报错装饰器
    def 打开预处理代码详细解释(self, 用不到的 =  ""):
        logger.info("打开预处理代码详细解释")
        Flyout.create(
            icon=InfoBarIcon.SUCCESS,
            title='预处理代码使用说明',
            content="""输入的必须是正经python代码，但是为了方便，会默认将各种中文字符全部替换为对应的英文字符，然后执行。\n
已经事先定义好了名字为【设置中数据读取设置里表格一的键】的那些变量，变量类型是pandas的DataFrame，其中的数据就是对应的图像数据，还有一个名字为“遮罩”的变量，代表着数值遮罩数组，以及一个叫做“缺失值数组”的变量，代表着nan值遮罩数组，前者代表着当前绘制的标注，后者代表着允许标注的区域。\n
但是注意：为了提高效率，nan值遮罩数组只有在加载文件的时候才会传输给绘图区，所以如果修改nan值遮罩数组（缺失值数组），需要保存文件后再打开这个文件才会有效。\n
标注类型实际上是数字，但是我有安排替换，直接写【鼠标放在画布颜色圆圈上能够看到的字符】也是可以生效的，类型是pandas的DataFrame，数据就是遮罩数组，你可以直接对遮罩进行操作，遮罩数组会被直接修改。同时还定义了“当前文件名”这个变量，就是当前使用的文件名字。\n
我还额外定义了之前5个个文件的相应的对象，只需要在变量名前面加上”上n个“即可访问，用于对比时间变化之下数据的变化，同时还定义了五个缓存遮罩变量，分别是从缓存遮罩1~缓存遮罩5，这些缓存遮罩实现可以跨文件交流信息。\n
然后是函数的部分，我定义了保存和载入两个函数，用来将缓存遮罩保存到文件夹里，以及将文件夹里的缓存遮罩加载到软件中。加载函数可以输入参数，为整数数字，效果是加载离当前时间第几近的文件。\n
除此之外还定义了一个通用函数——展示（），输入参数为单个二维数组，无论什么样的数据都可以用展示函数将其展示出来，但是数据量较大的时候需要等待几秒钟。如果想获得数据的确定的值，可以用print，已经将print替换成在窗口以消息形式显示了。 \n
DataFrame的操作方法有很多，比如\n
遮罩[(雷达反射率 <35)&(多普勒速度==0)]=判断为杂波 \n
这样一条语句就可以将所有雷达反射率小且速度平行于雷达的点赋值为杂波。\n
DataFrame也支持数字索引，但是考虑到有些图的横坐标是时间，时间的部分写aa时bb分也是可以生效的，但是格式必须要有两个连续数字才能被识别。只支持横坐标有1440个数值且正好在一天内，说白了就是专门给THi图像用的功能。\n
在和一些比较复杂的条件数组交互时，DAtaFrame中二维布尔数组必须用np.array转换成numpy布尔数组才能参与运算，否则只能直接使用，比如下面的例子：\n
遮罩.loc[np.array(pd.DataFrame(np.outer(速度谱宽.index.isin(range(00时18分, 18时20分)), 速度谱宽.columns.isin(range(90, 180))), index=速度谱宽.index, columns=速度谱宽.columns))&(np.array(雷达反射率<10))] = 3\n
这一段代码可以将THI图像中时间范围内且雷达反射率要求内的点判断为杂波\n
遮罩.values[np.where(np.array((雷达反射率.notna()) & (上1个雷达反射率.notna()) & (上2个雷达反射率.notna()) &(上3个雷达反射率.notna()) & (上4个雷达反射率.notna())))] = 3\n
这一段代码可以检验前四个时间和当前雷达图的重复之处，可以用来判断地物回波（但是雷达回波随时间变化太小的话意义不大）\n
【缓存遮罩1 = 雷达反射率】这个代码可以将当前的雷达反射率数据存到缓存遮罩1上，不论文件变化，缓存遮罩的数据都是不变的，除非重启软件。\n
【缓存遮罩1 = np.array(雷达反射率>10) 】这个代码可以将一个np形式的布尔数组储存到缓存遮罩1里，然后在某一张图用【遮罩[缓存遮罩1]=判断为杂波】即可将缓存遮罩直接作为判断依据。\n
更多用法请参考pandas语法。""",
            target=self.Main.ui.widget,
            parent=self.Main.ui.widget,
            isClosable=True,
            aniType=FlyoutAnimationType.PULL_UP
        )

    @报错装饰器
    def 导入绘图函数按钮(self):
        w = CustomMessageBox(self.Main.ui.widget)
        w.绘图函数对话框警告正文.setMarkdown("""
## 请注意\n\n\n \n\n\n
导入的文件必须是一个Python文件，文件中除了必须的库之外必须只有一个函数（甚至没有库也不是不可以，但是无论如何要保证用到的库主程序里都有导入），同时不能有除了函数之外的其他全局变量，所有要用到的变量比如自定义色标等，都要定义在函数内部。\n\n\n \n\n\n
函数名可以是“绘制图像”四个汉字，或者“matpainter”，函数名不能换！！也最好不要写子函数！！！\n\n\n \n\n\n
## 这个函数的标准声明方式如：\n\n\n \n\n\n 
def matpainter(TwoDimensionalArray, DataType, DrawPolarOrNot, file_name ='', dpi=100, save_path=None,edgedict=None)\n\n\n \n\n\n
* 所有参数位置必须是这样，前三个参数的名字可以自定义，后四个参数必须是规定的参数名。这些参数的意思按照顺序为：要绘制的二维数组、绘制图形的类型（在npz中的键的意思）、是否使用极坐标、当前处理到的文件名字。\n\n\n \n\n\n
更后面的三个参数分别是清晰度（这个参数可以用，但是软件设置界面提供了调整方式，不建议写死在函数里）、文件保存路径（这个参数不要用，软件会自动传入）、遮罩边缘数组（这个参数也不要用，软件会自动传入）\n\n传入的时候是按照这样参数位置传入的，所以顺序绝不能变，最后四个参数名字和位置都不能动！！！这四个参数有其他的作用，但是在绘制图像标题的时候可以利用到文件名这个参数。\n\n\n \n\n\n 
“save_path=None”和另一个是一个固定格式，一定要有，一定要放在输入参数的最后面。多次强调，主要是一旦格式出错，函数运行就会报错，程序会直接假死，再次打开也会假死，只能去【配置文件.json】里面把启动自定义函数的选项改成false，然后再启动才能正常启动。\n\n\n \n\n\n
## 函数体内容\n\n\n \n\n\n
用户要完成的任务主要是根据数据数组（二维的，顺序和原始数组一样，代码过程全完别改动原始数据，不然边缘用散点图绘制的时候无法和真实数据重合。如果极坐标或者直角坐标发现绘制出来的图和绘图区的底图不一样，一方面可以在设置界面调整绘图区和传输遮罩的数组设置，另一方面建议在matplotlib中调整坐标轴，参考代码如下：\n\n\n \n\n\n
ax.set_theta_offset(np.pi / 2)  # 起始角度顺时针旋转90度\n\n
ax.set_theta_direction(-1)  # 角度方向逆时针\n\n\n \n\n\n
直角坐标图也有可能出现类似问题，同样在设置界面中改变选项或者matplotlib里改变坐标轴就行，可以通过调用 ax.invert_xaxis() 和 ax.invert_yaxis() 方法来翻转 x 轴和 y 轴，千万别动在绘图函数里修改绘图数据（原始数据）。\n\n\n \n\n\n
主要还是绘图区的背景图像和遮罩绘图的算法太复杂了很难做成高度自定义（就像导入自定义绘图函数这种），所以只能麻烦用户迁就一下了。\n\n\n \n\n\n
还有如果一张图文件绘制多个图，在代码最后将要画圈的ax用plt.gca(ax)标注出来）和数据类型和是否要绘制极坐标图像，以及文件名，借助这些信息去完成绘图，最后以plt.show()输出！！！\n\n\n \n\n\n
plt.show()很重要，而且不要有其他输出方式，程序实际上不会用show去输出，但是show是定位和替换成标准输出的标志位！！\n\n\n \n\n\n
如果加载函数之后还是运行失败了，那就是你的函数需要用到的库和对象在主程序文件里面没有被定义，你在你的程序文件里面定义了不会起作用的，还是要打开主文件复制粘贴一下。如果用的是exe那就没办法了，所以最好载入环境运行源代码。\n\n\n \n\n\n
精力有限没有做太多校验相关的事情，所以代码安全性全靠用户了！！！
                                  """)
        if w.exec():
            # 打开文件浏览器
            path1 = QFileDialog.getOpenFileName(self.Main.ui.widget, "选择绘图函数文件", "", "Python文件 (*.py)")[0]
            if path1:
                # 读取文件内容
                with open(path1, 'r', encoding='utf-8') as file:
                    # 读取文件内容
                    file_content = file.read().replace("matpainter(","绘制图像(")
                # 使用正则表达式找到plt.show()及其前面的空白字符
                pattern = r"(\n\s*)plt.show\(\)"
                边缘函数返回替换文本 = """
if save_path != None:
    save_filename_dir = file_name+"┃"
    save_filename_dir = save_filename_dir.split("┃")[0]
    if edgedict != None:
        for key in edgedict.keys():
            current_ax = plt.gca()
            current_ax.scatter(edgedict[key][0], edgedict[key][1], c=key, s=1)
    if not os.path.exists(os.path.join(save_path,save_filename_dir)):
            os.makedirs(os.path.join(save_path,save_filename_dir))
    plt.savefig(os.path.join(save_path,save_filename_dir , f"{data_type} - {file_name}"+ '.png'), dpi=dpi)
    plt.close()
else:
    if edgedict != None:
        for key in edgedict.keys():
            current_ax = plt.gca()
            current_ax.scatter(edgedict[key][0], edgedict[key][1], c=key, s=1)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=dpi)
    plt.clf()
    plt.close()
    buf.seek(0)
    time.sleep(0.1)
    img_base64 = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return img_base64"""
                # 替换文本中的换行符后面添加与plt.show()相同的空白字符
                match = re.search(pattern, file_content)
                if match:
                    indent = match.group(1)  # 获取与plt.show()相同的缩进
                    # 为替换文本的每一行添加相同的缩进
                    indented_replacement_text = indent.join(边缘函数返回替换文本.splitlines(True))
                    # 替换原文中的plt.show()及其前面的空白字符
                    modified_content = re.sub(pattern, indented_replacement_text, file_content)
                # 将文件内容传递给js
                self.自定义绘图函数 = modified_content
                # 设置自定义绘图函数能用
                self.自定义绘图函数能不能用 = True
                # 输出提示信息
                self.显示消息框函数("success", "导入绘图函数成功", "已成功导入绘图函数，重新加载文件以使用自定义绘图函数。")

    @报错装饰器
    def 浮出批量保存图片进度条(self):
        # 检查self.picture_output_progressflyout是否存在
        
        if hasattr(self, 'picture_output_progressflyout'):
            # 如果存在，检查其内部值是否为False
            # logger.info(f"进度条是否已存在标识符：{self.picture_output_progressflyout.progress_exist}")
            if not self.picture_output_progressflyout.progress_exist:
                # 如果是False，重新创建对象
                self.picture_output_progressflyout = ProgressFlyoutView(self.Main, self.开始批量渲染图片操作, self.暂停批量渲染图片操作, self.终止批量渲染图片操作)
                self.picture_output_progressflyout.keynote = "进行批量渲染图片的时候界面会很卡，请耐心等待完成。"
                self.picture_output_progressflyout.Oprah = "正在批量渲染文件夹内所有文件的参考图"
            # 如果内部值是True，则保持现有对象不变
        else:
            # 如果self.picture_output_progressflyout不存在，重新创建对象
            self.picture_output_progressflyout = ProgressFlyoutView(self.Main, self.开始批量渲染图片操作, self.暂停批量渲染图片操作, self.终止批量渲染图片操作)
            self.picture_output_progressflyout.keynote = "进行批量渲染图片的时候界面会很卡，请耐心等待完成。"
            self.picture_output_progressflyout.Oprah = "正在批量渲染文件夹内所有文件的参考图"
        Flyout.make(self.picture_output_progressflyout, self.ui.savefileall, self.Main, aniType=FlyoutAnimationType.DROP_DOWN,isDeleteOnClose=False)

    def 开始批量渲染图片操作(self):
        self.批量渲染图片中断标志位 = True
        self.批量渲染图片结束标志位 = True
        self.批量保存文件夹下所有渲染的参考图像()


    def 暂停批量渲染图片操作(self,bool1):
        self.批量渲染图片中断标志位 = bool1

    def 终止批量渲染图片操作(self):
        self.批量渲染图片结束标志位 = False

    @报错装饰器
    def 批量保存文件夹下所有渲染的参考图像(self):
        global 绘制图像
        是否经过预处理标志位 = self.判断参考图是否经过预处理标志位
        是否经过边缘提取标志位 = self.判断参考图是否经过边缘提取标志位
        数值遮罩数组 = self.Main.数值遮罩数组
        nan遮罩数组 = self.Main.nan遮罩数组
        图像判别数字转换成颜色 = self.Main.图像判别数字转换成颜色
        图像判别数字转换成类型 = self.Main.图像判别数字转换成类型
        边缘提取中间函数 = self.边缘提取中间函数
        自定义绘图函数 = self.自定义绘图函数
        根据遮罩数组处理原始图像 = self.根据遮罩数组处理原始图像
        自定义绘图函数能不能用 = self.自定义绘图函数能不能用
        边缘坐标字典 = {}
        # 读取当前文件夹路径
        文件夹路径 = self.文件夹路径

        雷达缩写对应名字 = self.Main.雷达缩写对应名字
        全局遮罩选择菜单状态 = self.全局遮罩选择菜单状态
        批量输出图片时根据图片类型分类 = self.批量输出图片时根据图片类型分类
        allkeylist = []
        绘制图像dpi = self.绘制图像dpi

        def 校验文件路径(路径):
            # 检查路径是否存在
            if os.path.exists(路径):
                # 检查路径是否可写
                if os.access(路径, os.W_OK):
                    return True
                else:
                    logger.error("批量保存参考图像路径不可写")
                    return False
            else:
                logger.error("批量保存参考图像路径不存在")
                return False


        if self.文件保存路径!="" and 校验文件路径(self.文件保存路径):
            文件保存路径 = self.文件保存路径
        elif self.文件保存路径 == "":
            self.显示消息框函数("warning", "保存路径为空", "将存入来源文件路径，但文件名会有所不同。")
            文件保存路径 = self.文件夹路径
        elif 校验文件路径(self.文件保存路径) == False:
            self.显示消息框函数("error", "保存路径不可用", "请重新输入，单击右边的搜索框可以唤起文件选择对话框。")
            return
        


        def 生成边缘坐标字典(全局遮罩选择菜单状态, 数值遮罩数组, 图像判别数字转换成颜色, 图像判别数字转换成类型, 是否使用极坐标, 边缘提取中间函数):
            最终传递的边缘数组字典 = dict()
            需要处理的数字 = []
            logger.info("批量保存文件夹函数下，生成边缘坐标字典被调用")
            for key in 全局遮罩选择菜单状态:
                if 全局遮罩选择菜单状态[key]["选择状态"] == 1:
                    需要处理的数字.append(全局遮罩选择菜单状态[key]["代表的数值"])

            for i in 需要处理的数字:
                边缘提取数组 = np.where(数值遮罩数组 == i, 图像判别数字转换成颜色[i], "#000000")
                唯一值 = np.unique(边缘提取数组)

                if 唯一值.size == 1 and 唯一值[0] == "#000000":
                    logger.error(f"没有{图像判别数字转换成类型[i]}的数据")
                    logger.error(f"{数值遮罩数组}")
                else:
                    绘图坐标列表 = 边缘提取中间函数(边缘提取数组, 是否使用极坐标)
                    最终传递的边缘数组字典[图像判别数字转换成颜色[i]] = 绘图坐标列表

            return 最终传递的边缘数组字典

        # 遍历这个路径下所有后缀为.npz的文件
        filepathlist = []
        for file in os.listdir(文件夹路径):
            if file.endswith(".npz"):
                filepathlist.append(os.path.join(文件夹路径, file))

        self.picture_output_progressflyout.totle_files = len(filepathlist)
        filecount = 0

        # 真是傻逼屎山代码，因为alive_bar在打包成exe的时候会报错，所以只能用这种傻逼方法（主要是懒得专门为打包exe定制一个）
        try:
            with alive_bar(len(filepathlist), title='正在处理文件') as bar:
                # 遍历这些文件，读取数据，渲染图像，保存图像
                for path in filepathlist:
                    # 下面两个是和进度条交互用的标志位
                    while not self.批量渲染图片中断标志位:
                        time.sleep(0.01)
                        QCoreApplication.processEvents()
                    if not self.批量渲染图片结束标志位:
                        break
                    # 读取文件
                    data = np.load(path)
                    if self.是否要渲染没有蒙版的文件 == False:
                        if "Musk" not in list(data.keys()):
                            filecount += 1
                            if self.picture_output_progressflyout.progress_exist:
                                self.picture_output_progressflyout.set_files_processed(filecount,os.path.basename(path))
                            bar()
                            continue
                    是否使用极坐标 = self.输入原始数据返回要不要使用极坐标(data)
                    data_dict = dict()
                    # 读取数据
                    for key in data.keys():
                        if key not in allkeylist and key != "Musk" and key != "Musk_nan" and key != "Background" and key != "allow_pickle":
                            allkeylist.append(雷达缩写对应名字[key])
                        if key == "Musk":
                            数值遮罩数组 = data[key]
                        elif key == "Musk_nan":
                            nan遮罩数组 = data[key]
                        else:
                            data_dict[key] = data[key]
                    # 保存文件
                    if 是否经过边缘提取标志位 == True:
                        边缘坐标字典 = 生成边缘坐标字典(全局遮罩选择菜单状态, 数值遮罩数组, 图像判别数字转换成颜色, 图像判别数字转换成类型, 是否使用极坐标, 边缘提取中间函数)
                    for key in data_dict.keys():
                        # 特定键不进行绘制
                        if key == "Musk" or key == "Musk_nan" or key == "Background" or key == "allow_pickle":
                            continue
                        QCoreApplication.processEvents()
                        # 保存文件
                        if 自定义绘图函数能不能用:
                            exec(自定义绘图函数,globals())
                        else:
                            绘制图像 = globals().get('matpainter')
                        绘图使用的文件名 = re.sub(r"(_Mask|_预处理|_已修改)", "", os.path.basename(path).split(".")[0])
                        if self.判断参考图是否经过预处理标志位 == True:
                            需要处理的数字 = []
                            for key1 in self.全局遮罩选择菜单状态:
                                if self.全局遮罩选择菜单状态[key1]["选择状态"] == 1:
                                    需要处理的数字.append(self.全局遮罩选择菜单状态[key1]["代表的数值"])
                            需要处理的内容 = "-".join([self.Main.图像判别数字转换成类型[int(i)] for i in 需要处理的数字])
                            绘图使用的文件名 = 绘图使用的文件名+f"┃消去【{需要处理的内容}】"       
                        logger.info(f"开始绘制{雷达缩写对应名字[key]}-{绘图使用的文件名}图像")
                        if 是否经过预处理标志位:
                            if 是否经过边缘提取标志位:
                                logger.info("处理保存文件，预处理和边缘提取都为True的情况")
                                绘制图像(根据遮罩数组处理原始图像(data_dict[key].copy(),数值遮罩数组=数值遮罩数组), 雷达缩写对应名字[key], 是否使用极坐标, file_name = 绘图使用的文件名, dpi = 绘制图像dpi, save_path=文件保存路径, edgedict=边缘坐标字典)
                            else:
                                logger.info("处理保存文件和预处理为True，边缘提取为False的情况")
                                绘制图像(根据遮罩数组处理原始图像(data_dict[key].copy(),数值遮罩数组=数值遮罩数组), 雷达缩写对应名字[key], 是否使用极坐标, file_name = 绘图使用的文件名, dpi = 绘制图像dpi, save_path=文件保存路径)
                        else:
                            if 是否经过边缘提取标志位:
                                logger.info("处理保存文件和边缘提取为True，预处理为False的情况")
                                绘制图像(data_dict[key].copy(), 雷达缩写对应名字[key], 是否使用极坐标, file_name = 绘图使用的文件名, dpi = 绘制图像dpi, save_path=文件保存路径, edgedict=边缘坐标字典)
                            else:
                                logger.info("处理只有保存文件为True，其它都为False的情况")
                                绘制图像(data_dict[key].copy(), 雷达缩写对应名字[key], 是否使用极坐标, file_name = 绘图使用的文件名, dpi = 绘制图像dpi, save_path=文件保存路径)

                    if self.是否输出渲染图片时输出对应的修改后npz文件:
                        使用的保存数组 = dict()
                        for i in data.keys():
                            if i != "Musk" and i != "Musk_nan" and i != "Background" and i != "allow_pickle":
                                使用的保存数组[i] = data[i]
                        self.保存修改过后的数据函数(使用的保存数组,绘图使用的文件名,文件保存路径,path,雷达缩写对应名字)
                        
                    filecount += 1
                    if self.picture_output_progressflyout.progress_exist:
                        self.picture_output_progressflyout.set_files_processed(filecount,os.path.basename(path))
                    bar()

        except Exception as e:
                # 遍历这些文件，读取数据，渲染图像，保存图像
                for path in filepathlist:
                    # 下面两个是和进度条交互用的标志位
                    while not self.批量渲染图片中断标志位:
                        time.sleep(0.01)
                        QCoreApplication.processEvents()
                    if not self.批量渲染图片结束标志位:
                        break
                    # 读取文件
                    data = np.load(path)
                    if self.是否要渲染没有蒙版的文件 == False:
                        if "Musk" not in list(data.keys()):
                            filecount += 1
                            if self.picture_output_progressflyout.progress_exist:
                                self.picture_output_progressflyout.set_files_processed(filecount,os.path.basename(path))
                            continue
                    是否使用极坐标 = self.输入原始数据返回要不要使用极坐标(data)
                    data_dict = dict()
                    # 读取数据
                    for key in data.keys():
                        if key not in allkeylist and key != "Musk" and key != "Musk_nan" and key != "Background" and key != "allow_pickle":
                            allkeylist.append(雷达缩写对应名字[key])
                        if key == "Musk":
                            数值遮罩数组 = data[key]
                        elif key == "Musk_nan":
                            nan遮罩数组 = data[key]
                        else:
                            data_dict[key] = data[key]
                    # 保存文件
                    if 是否经过边缘提取标志位 == True:
                        边缘坐标字典 = 生成边缘坐标字典(全局遮罩选择菜单状态, 数值遮罩数组, 图像判别数字转换成颜色, 图像判别数字转换成类型, 是否使用极坐标, 边缘提取中间函数)
                    for key in data_dict.keys():
                        # 特定键不进行绘制
                        if key == "Musk" or key == "Musk_nan" or key == "Background" or key == "allow_pickle":
                            continue
                        QCoreApplication.processEvents()
                        # 保存文件
                        if 自定义绘图函数能不能用:
                            exec(自定义绘图函数,globals())
                        else:
                            绘制图像 = globals().get('matpainter')
                        绘图使用的文件名 = re.sub(r"(_Mask|_预处理|_已修改)", "", os.path.basename(path).split(".")[0])
                        if self.判断参考图是否经过预处理标志位 == True:
                            需要处理的数字 = []
                            for key1 in self.全局遮罩选择菜单状态:
                                if self.全局遮罩选择菜单状态[key1]["选择状态"] == 1:
                                    需要处理的数字.append(self.全局遮罩选择菜单状态[key1]["代表的数值"])
                            需要处理的内容 = "-".join([self.Main.图像判别数字转换成类型[int(i)] for i in 需要处理的数字])
                            绘图使用的文件名 = 绘图使用的文件名+f"┃消去【{需要处理的内容}】"               
                        logger.info(f"开始绘制{雷达缩写对应名字[key]}-{绘图使用的文件名}图像")
                        if 是否经过预处理标志位:
                            if 是否经过边缘提取标志位:
                                logger.info("处理保存文件，预处理和边缘提取都为True的情况")
                                绘制图像(根据遮罩数组处理原始图像(data_dict[key].copy(),数值遮罩数组=数值遮罩数组), 雷达缩写对应名字[key], 是否使用极坐标, file_name = 绘图使用的文件名, dpi = 绘制图像dpi, save_path=文件保存路径, edgedict=边缘坐标字典)
                            else:
                                logger.info("处理保存文件和预处理为True，边缘提取为False的情况")
                                绘制图像(根据遮罩数组处理原始图像(data_dict[key].copy(),数值遮罩数组=数值遮罩数组), 雷达缩写对应名字[key], 是否使用极坐标, file_name = 绘图使用的文件名, dpi = 绘制图像dpi, save_path=文件保存路径)
                        else:
                            if 是否经过边缘提取标志位:
                                logger.info("处理保存文件和边缘提取为True，预处理为False的情况")
                                绘制图像(data_dict[key].copy(), 雷达缩写对应名字[key], 是否使用极坐标, file_name = 绘图使用的文件名, dpi = 绘制图像dpi, save_path=文件保存路径, edgedict=边缘坐标字典)
                            else:
                                logger.info("处理只有保存文件为True，其它都为False的情况")
                                绘制图像(data_dict[key].copy(), 雷达缩写对应名字[key], 是否使用极坐标, file_name = 绘图使用的文件名, dpi = 绘制图像dpi, save_path=文件保存路径)

                    if self.是否输出渲染图片时输出对应的修改后npz文件:
                        使用的保存数组 = dict()
                        for i in data.keys():
                            if i != "Musk" and i != "Musk_nan" and i != "Background" and i != "allow_pickle":
                                使用的保存数组[i] = data[i]
                        self.保存修改过后的数据函数(使用的保存数组,绘图使用的文件名,文件保存路径,path,雷达缩写对应名字)

                    filecount += 1
                    if self.picture_output_progressflyout.progress_exist:
                        self.picture_output_progressflyout.set_files_processed(filecount,os.path.basename(path))

        if 批量输出图片时根据图片类型分类 == True:
            # 遍历包括所有子文件夹的所有文件，将文件名和完整文件路径对应成字典
            文件名和完整文件路径对应字典 = dict()
            for root, dirs, files in os.walk(文件保存路径):
                for file in files:
                    文件名和完整文件路径对应字典[file] = os.path.join(root, file)
            # 遍历这个字典，将文件名和文件路径对应的文件移动到对应的文件夹下
            # 你现有的代码
            for key in 文件名和完整文件路径对应字典.keys():
                for i in allkeylist:
                    if i in key:
                        if not os.path.exists(os.path.join(文件保存路径, i)):
                            os.makedirs(os.path.join(文件保存路径, i))
                        try:
                            shutil.move(os.path.join(文件名和完整文件路径对应字典[key]).replace("/", "\\").replace("\\", "/"), os.path.join(文件保存路径, i, key).replace("/", "\\").replace("\\", "/"))
                        except:
                            pass

            # 删除多余的文件夹
            for folder in os.listdir(文件保存路径):
                folder_path = os.path.join(文件保存路径, folder)
                if os.path.isdir(folder_path):
                    # 检查文件夹是否为空
                    if not os.listdir(folder_path):
                        # 如果文件夹为空，则删除
                        os.rmdir(folder_path)
                


    @报错装饰器
    def 浮出批量预处理文件进度条(self):
        # 检查self.preprocessing_progressflyout是否存在
        
        if hasattr(self, 'preprocessing_progressflyout'):
            # 如果存在，检查其内部值是否为False
            # logger.info(f"批量预处理进度条是否存在标识符为：{self.preprocessing_progressflyout.progress_exist}")
            if not self.preprocessing_progressflyout.progress_exist:
                # 如果是False，重新创建对象
                self.preprocessing_progressflyout = ProgressFlyoutView(self.Main, self.开始批量预处理文件操作, self.暂停批量预处理文件操作, self.终止批量预处理文件操作)
                self.preprocessing_progressflyout.keynote = "进行批量预处理文件的时候界面会很卡，请耐心等待完成。"
                self.preprocessing_progressflyout.Oprah = "正在批量预处理文件夹内所有文件"
            # 如果内部值是True，则保持现有对象不变
        else:
            # 如果self.preprocessing_progressflyout不存在，重新创建对象
            self.preprocessing_progressflyout = ProgressFlyoutView(self.Main, self.开始批量预处理文件操作, self.暂停批量预处理文件操作, self.终止批量预处理文件操作)
            self.preprocessing_progressflyout.keynote = "进行批量预处理文件的时候界面会很卡，请耐心等待完成。"
            self.preprocessing_progressflyout.Oprah = "正在批量预处理文件夹内所有文件"
        Flyout.make(self.preprocessing_progressflyout, self.ui.preprocessingall, self.Main, aniType=FlyoutAnimationType.DROP_DOWN,isDeleteOnClose=False)

    def 开始批量预处理文件操作(self):
        self.批量预处理文件中断标志位 = True
        self.批量预处理文件结束标志位 = True
        self.批量预处理函数()


    def 暂停批量预处理文件操作(self,bool1):
        self.批量预处理文件中断标志位 = bool1

    def 终止批量预处理文件操作(self):
        self.批量预处理文件结束标志位 = False






    #批量生成背景图的预处理代码是：背景图片=生成背景图(雷达反射率)
    @报错装饰器
    def 批量预处理函数(self):
        global 背景图片
        是否经过预处理标志位 = self.判断参考图是否经过预处理标志位
        是否经过边缘提取标志位 = self.判断参考图是否经过边缘提取标志位
        数值遮罩数组 = None
        nan遮罩数组 = None
        图像判别数字转换成颜色 = self.Main.图像判别数字转换成颜色
        图像判别数字转换成类型 = self.Main.图像判别数字转换成类型
        边缘提取中间函数 = self.边缘提取中间函数
        自定义绘图函数 = self.自定义绘图函数
        根据遮罩数组处理原始图像 = self.根据遮罩数组处理原始图像
        自定义绘图函数能不能用 = self.自定义绘图函数能不能用
        边缘坐标字典 = {}
        # 读取当前文件夹路径
        文件夹路径 = self.文件夹路径
        批量预处理后是否保存当前文件 = self.批量预处理后是否保存当前文件
        雷达缩写对应名字 = self.Main.雷达缩写对应名字
        全局遮罩选择菜单状态 = self.全局遮罩选择菜单状态
        批量输出图片时根据图片类型分类 = self.批量输出图片时根据图片类型分类
        是否要渲染没有蒙版的文件 = self.是否要渲染没有蒙版的文件
        allkeylist = []
        绘制图像dpi = self.绘制图像dpi
        背景图片 = "预处理函数初始值"


        def 校验文件路径(路径):
            # 检查路径是否存在
            if os.path.exists(路径):
                # 检查路径是否可写
                if os.access(路径, os.W_OK):
                    return True
                else:
                    logger.error("批量预处理时路径不可写")
                    return False
            else:
                logger.error("批量预处理时路径不存在")
                return False


        if self.文件保存路径!="" and 校验文件路径(self.文件保存路径):
            文件保存路径 = self.文件保存路径
        elif self.文件保存路径 == "":
            self.显示消息框函数("warning", "保存路径为空", "将存入来源文件路径，但文件名会有所不同。")
            文件保存路径 = self.文件夹路径
        elif 校验文件路径(self.文件保存路径) == False:
            self.显示消息框函数("error", "保存路径不可用", "请重新输入，单击右边的搜索框可以唤起文件选择对话框。")
            return
        

        # 遍历这个路径下所有后缀为.npz的文件
        filepathlist = []
        for file in os.listdir(文件夹路径):
            if file.endswith(".npz"):
                filepathlist.append(os.path.join(文件夹路径, file))


        self.preprocessing_progressflyout.totle_files = len(filepathlist)
        filecount = 0

        # 真是傻逼屎山代码，因为alive_bar在打包成exe之后会报错，不知道为什么，然后exec因为作用域问题又不能丢到函数里面，这样丑归丑起码能用……
        try:
            with alive_bar(len(filepathlist), title='正在处理文件') as bar:
                # 遍历这些文件，读取数据，渲染图像，保存图像
                for path in filepathlist:
                    # 下面两个是和进度条交互用的标志位
                    while not self.批量预处理文件中断标志位:
                        time.sleep(0.01)
                        QCoreApplication.processEvents()
                    if not self.批量预处理文件结束标志位:
                        break
                    # 读取文件
                    data = dict(np.load(path))
                    是否使用极坐标 = self.输入原始数据返回要不要使用极坐标(data)
                    data_dict = dict()
                    # 读取数据
                    for key in data.keys():
                        QCoreApplication.processEvents()
                        if key not in allkeylist and key != "Musk" and key != "Musk_nan" and key != "Background" and key != "allow_pickle":
                            allkeylist.append(key)
                        if key == "Musk":
                            数值遮罩数组 = data[key]
                        else:
                            数值遮罩数组 = None
                        if key == "Musk_nan":
                            nan遮罩数组 = data[key]
                        else:
                            nan遮罩数组 = None
                        if key == "Background":
                            背景图片 = data[key]
                        else:
                            背景图片 = "预处理函数初始值"
                        if key not in ["Musk", "Musk_nan", "Background", "allow_pickle"]:
                            data_dict[key] = data[key]
                    # 运行预处理函数
                    # logger.info(f"当前文件存在的key为：{data_dict.keys()}")
                    self.预处理函数(True, data_dict, 雷达缩写对应名字, 数值遮罩数组, nan遮罩数组, 是否使用极坐标, os.path.basename(path).replace(".npz", ""))
                    QCoreApplication.processEvents()
                    self.预处理函数(False, data_dict, 雷达缩写对应名字, 数值遮罩数组, nan遮罩数组, 是否使用极坐标, os.path.basename(path).replace(".npz", ""))
                    QCoreApplication.processEvents()
                    # 将处理完成的数据保存到一个字典变量
                    if 批量预处理后是否保存当前文件:
                        data_output = dict()
                        for key in data_dict.keys():
                            QCoreApplication.processEvents()
                            data_output[key] = data_dict[key]
                        if 遮罩 is not None:
                            data_output["Musk"] = 遮罩
                        if 缺失值数组 is not None:
                            data_output["Musk_nan"] = 缺失值数组
                        if 背景图片 != "" and 背景图片 is not None and 背景图片 != "预处理函数初始值":
                            logger.info("背景图片已经生成")
                            data_output["Background"] = 背景图片
                        # 用numpy保存文件
                        np.savez(os.path.join(文件保存路径, os.path.basename(path)).replace(".npz", "_预处理.npz"), **data_output)
                        
                    filecount += 1
                    if self.preprocessing_progressflyout.progress_exist:
                        self.preprocessing_progressflyout.set_files_processed(filecount,os.path.basename(path))
                    bar()
        except:
                # 遍历这些文件，读取数据，渲染图像，保存图像
                for path in filepathlist:
                    # 下面两个是和进度条交互用的标志位
                    while not self.批量预处理文件中断标志位:
                        time.sleep(0.01)
                        QCoreApplication.processEvents()
                    if not self.批量预处理文件结束标志位:
                        break
                    # 读取文件
                    data = dict(np.load(path))
                    是否使用极坐标 = self.输入原始数据返回要不要使用极坐标(data)
                    data_dict = dict()
                    # 读取数据
                    for key in data.keys():
                        QCoreApplication.processEvents()
                        if key not in allkeylist and key != "Musk" and key != "Musk_nan" and key != "Background" and key != "allow_pickle":
                            allkeylist.append(key)
                        if key == "Musk":
                            数值遮罩数组 = data[key]
                        else:
                            数值遮罩数组 = None
                        if key == "Musk_nan":
                            nan遮罩数组 = data[key]
                        else:
                            nan遮罩数组 = None
                        if key == "Background":
                            背景图片 = data[key]
                        else:
                            背景图片 = "预处理函数初始值"
                        if key not in ["Musk", "Musk_nan", "Background", "allow_pickle"]:
                            data_dict[key] = data[key]
                    # 运行预处理函数
                    # logger.info(f"当前文件存在的key为：{data_dict.keys()}")
                    self.预处理函数(True, data_dict, 雷达缩写对应名字, 数值遮罩数组, nan遮罩数组, 是否使用极坐标, os.path.basename(path).replace(".npz", ""))
                    QCoreApplication.processEvents()
                    self.预处理函数(False, data_dict, 雷达缩写对应名字, 数值遮罩数组, nan遮罩数组, 是否使用极坐标, os.path.basename(path).replace(".npz", ""))
                    QCoreApplication.processEvents()
                    # 将处理完成的数据保存到一个字典变量
                    if 批量预处理后是否保存当前文件:
                        data_output = dict()
                        for key in data_dict.keys():
                            QCoreApplication.processEvents()
                            data_output[key] = data_dict[key]
                        if 遮罩 is not None:
                            data_output["Musk"] = 遮罩
                        if 缺失值数组 is not None:
                            data_output["Musk_nan"] = 缺失值数组
                        if 背景图片 != "" and 背景图片 is not None and 背景图片 != "预处理函数初始值":
                            logger.info("背景图片已经生成")
                            data_output["Background"] = 背景图片
                        # 用numpy保存文件
                        np.savez(os.path.join(文件保存路径, os.path.basename(path)).replace(".npz", "_预处理.npz"), **data_output)
                        
                    filecount += 1
                    if self.preprocessing_progressflyout.progress_exist:
                        self.preprocessing_progressflyout.set_files_processed(filecount,os.path.basename(path))


    # 这函数换现在我也看不懂了，算法每一步的东西全部都融在一个函数里面了，主要是为了提高效率。
    # 这个东西我折腾了整整一天啊，唉，太难了，自己画极坐标，还得和html同步，太难了
    
    def 完整极坐标数组到画布数组(self, polar_array, array_or_image):
        """
        将极坐标数组转换为画布数组。
        
        参数:
        polar_array (numpy.ndarray): 极坐标数组。第一维是角度，第二维是半径。
        array_or_image (str): 指定输入的类型，可以是“数组”或“图片”。
        
        返回:
        numpy.ndarray: 生成的画布数组。
        """

        start_time = time.time()# 计时有关参数
        last_estimate_time = start_time  # 上一次估算时间
        estimate_interval = 20  # 每20秒钟估算一次


        if array_or_image == "数组":
            # 如果输入类型是数组，计算最小非 NaN 值的绝对值
            minnan = np.abs(np.nanmin(polar_array))
        else:
            # 找出所有唯一的颜色代码
            unique_colors = np.unique(polar_array)

            # 遍历每个唯一的颜色代码
            for color in unique_colors:
                # 检查颜色代码是否符合条件
                if isinstance(color, str) and color.startswith('#') and len(color) == 7:
                    # 将符合条件的颜色代码转换为整数
                    int_color = int(color[1:], 16)
                else:
                    # 不符合条件的颜色代码使用默认颜色
                    int_color = 16777215
    
                # 使用np.where替换颜色代码为对应的整数值
                polar_array = np.where(polar_array == color, int_color, polar_array)
        # 画布的尺寸为极坐标数组半径的两倍
        canvassize = polar_array.shape[1] * 2
        
        # 初始化画布数组
        canvas = np.zeros((canvassize, canvassize))
        dimension = polar_array.shape[0]

        total_elements = len(polar_array) * len(polar_array[0]) # 计时有关参数
        processed_elements = 0# 计时有关参数
        
        for theta in range(len(polar_array)):
            if time.time() - start_time > 0.1:
                QCoreApplication.processEvents()
            for r in range(len(polar_array[theta])):
                theta_use = theta*360/len(polar_array)
                # 将角度转换为弧度
                theta_rad = math.radians(theta_use)
                # 计算极坐标对应的画布中心坐标
                x_center = r * math.cos(theta_rad)
                y_center = r * math.sin(theta_rad)
                # 计算半径在画布上的投影长度
                b = r * math.sin(math.pi / dimension)
                
                if b < 0.3:
                    # 投影长度小于0.3时，只考虑中心点
                    pointlist = [(round(x_center), round(y_center))]
                elif b < 1.2:
                    # 投影长度小于1.2时，考虑中心点和周围的8个点
                    pointlist = [(round(x_center), round(y_center))]
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            x = round(x_center) + dx
                            y = round(y_center) + dy
                            pointlist.append((x, y))
                else:
                    # 投影长度大于等于1.2时，考虑中心点及其周围的所有点
                    x_min, x_max = round(x_center - b), round(x_center + b)
                    y_min, y_max = round(y_center - b), round(y_center + b)
                    pointlist = []
                    
                    for x in range(x_min, x_max + 1):
                        for y in range(y_min, y_max + 1):
                            r1 = math.sqrt(x**2 + y**2)
                            theta1 = math.degrees(math.atan2(y, x))
                            if theta1 < 0:
                                theta1 += 360
                            if abs(r1 - r) <= 1 and abs(theta1 - theta_use) <= 360/len(polar_array)/2:
                                pointlist.append((x, y))
                
                # 将点坐标转换为画布坐标
                for x, y in pointlist:
                    x_canvas = round(x + canvassize/2)
                    y_canvas = round(y + canvassize/2)
                    if 0 <= x_canvas < canvassize and 0 <= y_canvas < canvassize:
                        if array_or_image == "数组":
                            if not np.isnan(polar_array[theta, r]):
                                canvas[x_canvas, y_canvas] = polar_array[theta, r] + minnan
                            else:
                                canvas[x_canvas, y_canvas] = 0
                        elif array_or_image == "图片":
                            canvas[x_canvas, y_canvas] = polar_array[theta, r]


                processed_elements += 1
                current_time = time.time()
                elapsed_time = current_time - start_time
                # 计算时间并输出预计剩余时间
                if current_time - last_estimate_time > estimate_interval:
                    remaining_elements = total_elements - processed_elements
                    estimated_total_time = elapsed_time / processed_elements * total_elements
                    remaining_time = estimated_total_time - elapsed_time
                    logger.info(f"转换极坐标预计剩余时间: {remaining_time//60:.0f}分钟{remaining_time%60:.0f}秒，已耗费时间: {elapsed_time//60:.0f}分钟{elapsed_time%60:.0f}秒")
                    self.显示消息框函数("info", f"转换极坐标预计剩余时间：{remaining_time//60:.0f}分钟{remaining_time%60:.0f}秒", f"已耗费时间: {elapsed_time//60:.0f}分钟{elapsed_time%60:.0f}秒","底部")
                    last_estimate_time = current_time
                    QCoreApplication.processEvents()

        end_time = time.time()
        total_processing_time = end_time - start_time
        if total_processing_time > 30:
            logger.info(f"转换极坐标总耗时: {total_processing_time//60:.0f}分钟{total_processing_time%60}秒, 速度: {total_elements/total_processing_time:.2f}个像素/秒")
        return canvas

    @报错装饰器
    def 零散画布位置列表到极坐标(self,canvas_list, canvas_size=1000 ,a=360):
        """
        输入参数是一系列像素坐标点的列表，每个元素是一个(x, y)坐标的元组。
        返回一堆极坐标点的集合。
        """
        # 初始化极坐标数组，这里假设极坐标的范围和精度，可能需要根据实际情况调整
        polar_coords = []

        for x, y in canvas_list:
            QCoreApplication.processEvents()
            # 将直角坐标 (x, y) 转换为极坐标 (r, theta)
            r = math.sqrt((x - canvas_size // 2)**2 + (y - canvas_size // 2)**2)  # 计算半径 r
            theta = math.degrees(math.atan2(y - canvas_size // 2, x - canvas_size // 2))  # 计算角度 theta，并将其转换为度数
            if theta < 0:
                theta += 360  # 确保角度在 0 到 360 度之间
            b = r * math.sin(math.pi / a)  # 计算 b 值
            
            # 初始化列表，包含原始极坐标，先r后theta
            possible_polar_coords = [(round(theta/360*a), round(r))]
                
            # 根据 b 值循环判定并添加额外的极坐标
            i = 1
            while b < (1 / (2 ** i)):  # 例如 b < 0.5, b < 0.25, b < 0.125, ...
                possible_polar_coords.append((round((theta - i)/360*a) % 360, round(r)))
                possible_polar_coords.append((round((theta + i)/360*a) % 360, round(r)))
                i += 1
            
            polar_coords += possible_polar_coords

        return list(set(polar_coords))

    

    # 图像边缘提取的第二层函数，输入二维数组和判断是不是极坐标的标志位，输出用于绘图的第一个和第二个列表
    @报错装饰器
    def 边缘提取中间函数(self,二维数组,是否使用极坐标):
        """
        输入参数是二维数组和是否使用极坐标的标志位，输出用于绘图的第一个和第二个列表
        """
        原始二维数组 = 二维数组.copy()
    ####### 这是直角坐标
        if 是否使用极坐标 == False:
            logger.info("开始使用直角坐标进行边缘提取")

            # 将二维数组中的白色替换成黑色
            二维数组 = np.where(二维数组 == '#ffffff', '#000000', 二维数组 )
            # timestart = time.time()
            # 计算边缘并输出坐标
            edges1 = 图像边缘提取(二维数组,核大小=self.边缘提取的核大小, 阈值=self.边缘提取的阈值, 形态学核大小=self.边缘提取的形态学核大小, 描线宽度=self.边缘提取的描线宽度, 扩展像素=self.边缘提取的扩展像素)
            # logger.info(f"图像提取的边缘点数{len(edges1)}")
            # timemiddle = time.time()
            # logger.info(f"图像提取耗费时间{timemiddle-timestart }")
            # timeend = time.time()
            # logger.info(f"像素点替换耗费时间{timeend - timemiddle }")
            x_coords, y_coords = zip(*edges1)
            

        ###### 这是极坐标
        else:
            logger.info("开始使用极坐标进行边缘提取")
            # timestart = time.time()
            # 将二维数组中的白色替换成黑色
            二维数组 = np.where(二维数组 == '#ffffff', '#000000', 二维数组 )
            canvassize = 二维数组.shape[1]
            #二维数组 = np.flip(二维数组,1)

            # 将二维数组的值转换成整数
            二维数组 = self.完整极坐标数组到画布数组(二维数组,"图片").astype(int)

            # 将二维数组中的数字转换为十六进制颜色字符串
            # 假设二维数组中的数字已经是0-255之间的整数，代表颜色的RGB分量
            def 数字到十六进制颜色(num):
                return "#{:02x}{:02x}{:02x}".format(num, num, num)

            # 应用转换函数
            二维数组 = np.vectorize(数字到十六进制颜色)(二维数组)

            edges1 = 图像边缘提取(二维数组,核大小=self.边缘提取的核大小, 阈值=self.边缘提取的阈值, 形态学核大小=self.边缘提取的形态学核大小, 描线宽度=self.边缘提取的描线宽度, 扩展像素=self.边缘提取的扩展像素)

            

            edges1 = self.零散画布位置列表到极坐标(edges1,len(原始二维数组[0])*2,len(原始二维数组))

            # timemiddle = time.time()
            # logger.info(f"图像提取耗费时间{timemiddle-timestart }")
            logger.info(f"图像提取的边缘点数{len(edges1)}")

            x_coords, y_coords = zip(*edges1)
            x_coords = np.deg2rad(x_coords)# 将角度转换为弧度。这一步可不能省

        return [x_coords, y_coords]


# 图像边缘提取函数，我居然真把这东西写出来了，我真是牛逼
def 图像边缘提取(二维数组, 核大小=3, 阈值=50, 形态学核大小=3, 描线宽度=1, 扩展像素=0):
        """
        参数:
        二维数组: 二维数组，包含图像的十六进制颜色值。
        核大小 (核大小): Sobel 算子的核大小，控制边缘检测的精细程度。值越大，边缘检测越平滑。
        阈值 (阈值): 用于二值化边缘检测结果的阈值。较高的值会导致仅检测到强边缘，较低的值会检测到更多的细节。
        形态学核大小 (形态学核大小): 形态学操作的核大小，用于减少噪点和填补小孔。值越大，形态学操作越强。
        描线宽度 (描线宽度): 绘制轮廓的线条宽度。值越大，边缘线条越粗。
        扩展像素 (扩展像素): 扩展边缘的像素数量。值越大，边缘会向外扩展更多像素，模拟Photoshop中的扩展效果。
        """
        logger.info("进入图像边缘提取函数")
        # 将十六进制颜色转换为RGB
        def 十六进制转换成RGB(十六进制颜色字符串):
            try:
                十六进制颜色字符串 = 十六进制颜色字符串.lstrip('#')
            except:
                logger.error(f"报错的十六进制字符串为：{十六进制颜色字符串}")
                raise EOFError
            return tuple(int(十六进制颜色字符串[i:i+2], 16) for i in (0, 2, 4))

        # 将二维数组中的十六进制颜色值转换为图像
        def 十六进制转换成图像(二维数组):
            height = len(二维数组)
            width = len(二维数组[0])
            过程中创建的临时画布 = np.zeros((height, width, 3), dtype=np.uint8)
            
            for i in range(height):
                QCoreApplication.processEvents()
                for j in range(width):
                    try:
                        过程中创建的临时画布[i, j] = 十六进制转换成RGB(二维数组[i][j])
                    except:
                        logger.error(f"报错的输入数组位置和数组值分别为：{i},{j},{二维数组[i][j]}")
            
            return 过程中创建的临时画布

        # 计算Sobel边缘并返回边缘布尔数组
        def 计算边缘坐标(过程中创建的临时画布, 核大小, 阈值, 形态学核大小, 扩展像素):
            过程中创建的临时灰度图像 = cv2.cvtColor(过程中创建的临时画布, cv2.COLOR_RGB2GRAY)
            
            sobelx = cv2.Sobel(过程中创建的临时灰度图像, cv2.CV_64F, 1, 0, ksize=核大小)
            sobely = cv2.Sobel(过程中创建的临时灰度图像, cv2.CV_64F, 0, 1, ksize=核大小)
            
            sobel幅度 = np.sqrt(sobelx**2 + sobely**2)
            sobel幅度 = np.uint8(np.absolute(sobel幅度))
            
            # 阈值化以获得二值边缘图像
            _, 边缘坐标画布 = cv2.threshold(sobel幅度, 阈值, 255, cv2.THRESH_BINARY)
            
            # 应用形态学操作以减少噪点
            形态学的核 = np.ones((形态学核大小, 形态学核大小), np.uint8)
            边缘坐标画布 = cv2.morphologyEx(边缘坐标画布, cv2.MORPH_CLOSE, 形态学的核)
            
            # 扩展边缘
            if 扩展像素 > 0:
                形态学的核 = np.ones((扩展像素, 扩展像素), np.uint8)
                边缘坐标画布 = cv2.dilate(边缘坐标画布, 形态学的核, iterations=1)
            
            # 查找轮廓以提取边缘
            轮廓点, _ = cv2.findContours(边缘坐标画布, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            
            # 创建一个空白图像来绘制边缘
            空白的边缘坐标画布 = np.zeros_like(边缘坐标画布)
            
            # 仅绘制轮廓边缘
            cv2.drawContours(空白的边缘坐标画布, 轮廓点, -1, (255), 描线宽度)
            
            # 获取边缘的布尔数组
            边缘布尔数组 = 空白的边缘坐标画布 > 0
            
            return 边缘布尔数组

        # 将十六进制颜色数组转换为RGB图像
        过程中创建的临时画布 = 十六进制转换成图像(二维数组)
        
        # 计算边缘
        边缘布尔数组 = 计算边缘坐标(过程中创建的临时画布, 核大小, 阈值, 形态学核大小, 扩展像素)
        
        # 获取边缘的坐标
        边缘坐标 = np.column_stack(np.where(边缘布尔数组))
        
        return 边缘坐标
# %%
