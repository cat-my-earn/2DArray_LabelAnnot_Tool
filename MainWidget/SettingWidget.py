from importall import *
from LittleCards.LittleFlyoutView import CustomFlyoutView
from LittleCards.LittleSettingCard import ModifiedSwitchTab
from LittleCards.CustomAccordionCard import PowerSettingCardCustom
from MainWidget.SpecialAccordionCard import PowerSettingCard

class SettingWidget(QWidget):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        # 初始化 QVBoxLayout 作为主布局
        layout = QVBoxLayout(self)

        # 创建一个 QScrollArea
        scroll_area = ScrollArea()
        scroll_area.setWidgetResizable(True)

        # 创建一个 QWidget 作为 QScrollArea 的内容容器
        content = QWidget()
        content_layout = QVBoxLayout(content)  # 为内容容器设置布局
        self.parentup = parent

        def add_combobox_setting_card(icon, title, content, config_item, api_attr, texts,要添加到哪里,关联的函数 = None):
            combobox_card = ComboBoxSettingCard(
                configItem=config_item,
                icon=icon,
                title=title,
                content=content,
                texts=texts,
                parent=parent,
            )
            要添加到哪里.addSettingCard(combobox_card)

            def current_index_change(index):
                if 关联的函数!=None:
                    关联的函数(index)
            config_item.valueChanged.connect(current_index_change)





        def add_color_setting_card(icon, title, content, config_item, 初始颜色, 是否使用透明度通道, api_attr, 要添加到哪里,关联的函数 = None):
            color_card = ColorSettingCard(
                configItem=config_item,  # 配置项
                icon=icon,  # 图标
                title=title,  # 标题
                content=content,  # 内容（可选）
                parent=parent,  # 父窗口部件（可选）
                enableAlpha=是否使用透明度通道  # 是否启用 Alpha 通道（可选）
            )
            要添加到哪里.addSettingCard(color_card)

            def color_change(color):
                setattr(parent.api, api_attr, color)
                if 关联的函数!=None:
                    关联的函数(color)
            color_card.colorChanged.connect(color_change)

        
        # 定义添加滑动条设置项的函数
        def add_slider_setting_card(icon,title, content, config_item, api_attr,要添加到哪里,关联的函数 = None):
            slider_card = RangeSettingCard(
                config_item,
                FIF.PENCIL_INK,
                title=title,
                content=content,
            )
            要添加到哪里.addSettingCard(slider_card)

            def value_change(value):
                setattr(parent.api, api_attr, value)
                if 关联的函数!=None:
                    关联的函数(value)
            slider_card.valueChanged.connect(value_change)


        # 定义添加开关设置项的函数
        def add_switch_setting_card(icon, title, content, config_item, api_attr,要添加到哪里,关联的函数 = None):
            switch_card = ModifiedSwitchTab(
                icon=icon,
                title=title,
                content=content,
                configItem=config_item
            )
            要添加到哪里.addSettingCard(switch_card)

            def checked_change(checked):
                setattr(parent.api, api_attr, checked)
                if 关联的函数!=None:
                    关联的函数(checked)
            switch_card.checkedChanged.connect(checked_change)


        基础信息数据卡 = PrimaryPushSettingCard(
            text="浮出帮助",
            icon=FIF.HELP,
            title="基础信息和使用帮助",
            content="软件的使用教程、功能介绍、设计架构、自定义等等"
        )

        # 定义被召唤的函数
        def 基础信息按钮被点击函数():
            Flyout.make(CustomFlyoutView(parent), 基础信息数据卡, self, aniType=FlyoutAnimationType.DROP_DOWN)

        # 连接按钮的点击信号到函数
        基础信息数据卡.clicked.connect(基础信息按钮被点击函数)

        基础数据项 = SettingCardGroup("基础数据项",self)
        基础数据项.addSettingCard(基础信息数据卡)
        基础数据项.addSettingCard(PowerSettingCard(self))
        绘图区图像设定 = PowerSettingCardCustom(FIF.DEVELOPER_TOOLS, "绘图区底图设置", "设置绘图区底图的缺失值显示方式、颜色反转、图像上下、左右翻转和极坐标的旋转", self)
        绘图区图像设定.add_switch_setting("绘图区缺失值设置为白色", "绘图区缺失值设置为黑色", "打开之后绘图区缺失值设置为白色，关闭之后设置为黑色", parent.api, "绘图区缺失值是否设置为白色")
        绘图区图像设定.add_switch_setting("绘图区灰度图像颜色反转", "绘图区灰度图像颜色不反转", "打开之后绘图区灰度图像黑白反转，关闭之后不反转", parent.api, "绘图区灰度图像是否颜色反转")
        绘图区图像设定.add_switch_setting("绘图区图像转置", "绘图区图像不转置", "打开之后绘图区图像将会先将数据转置再绘制，关闭之后不转置", parent.api, "绘图区图像是否转置")
        绘图区图像设定.add_switch_setting("绘图区图像上下翻转", "绘图区图像不上下翻转", "打开之后绘图区图像将会上下翻转再绘制，关闭之后不上下翻转", parent.api, "绘图区图像是否上下翻转")
        绘图区图像设定.add_switch_setting("绘图区图像左右翻转", "绘图区图像不左右翻转", "打开之后绘图区图像将会左右翻转再绘制，关闭之后不左右翻转", parent.api, "绘图区图像是否左右翻转")
        绘图区图像设定.add_switch_setting("绘图区图像极坐标逆时针", "绘图区图像极坐标顺时针", "这个按钮不会直接改变图像，只会改变图像加减角度的方向，打开角度增加按照逆时针，关闭之后顺时针", parent.api, "绘图区图像极坐标是否是逆时针")
        绘图区图像设定.add_slider_setting("绘图区图像极坐标旋转角度", "绘图区图像极坐标旋转角度，-360~360度", parent.cfg.绘图区图像极坐标翻转角度)
        基础数据项.addSettingCard(绘图区图像设定)
        传递的遮罩设定 = PowerSettingCardCustom(FIF.LAYOUT, "传输遮罩数组设置", "大多数时候和绘图区底图设置一样，如果一样的设置里遮罩和底图还是无法重合，那就不用强求一样，目标是能重合。", self)
        传递的遮罩设定.add_switch_setting("遮罩数组转置", "遮罩数组不转置", "打开之后传输遮罩数组到绘图区时会先转置再传输，关闭之后不转置", parent.api, "传递的遮罩是否转置")
        传递的遮罩设定.add_switch_setting("遮罩数组上下翻转", "遮罩数组不上下翻转", "打开之后遮罩数组将会上下翻转再传输，关闭之后不上下翻转", parent.api, "传递的遮罩是否上下翻转")
        传递的遮罩设定.add_switch_setting("遮罩数组左右翻转", "遮罩数组不左右翻转", "打开之后遮罩数组将会左右翻转再传输，关闭之后不左右翻转", parent.api, "传递的遮罩是否左右翻转")
        传递的遮罩设定.add_switch_setting("遮罩数组极坐标逆时针", "遮罩数组极坐标顺时针", "这个按钮不会直接改变图像，只会改变图像加减角度的方向，打开角度增加按照逆时针，关闭之后顺时针", parent.api, "传递的遮罩极坐标是否是逆时针")
        传递的遮罩设定.add_slider_setting("遮罩数组极坐标旋转角度", "遮罩数组极坐标旋转角度，-360~360度", parent.cfg.传递的遮罩极坐标翻转角度)
        基础数据项.addSettingCard(传递的遮罩设定)



        通用设置项 = SettingCardGroup("基础功能设置项",self)
        add_switch_setting_card(FIF.BRIGHTNESS,"夜间模式", "打开之后会切换到黑暗模式", parent.cfg.是否开启夜间模式, "是否开启夜间模式",通用设置项,关联的函数=parent.SwitchDepthMode)
        add_color_setting_card(FIF.PALETTE,"软件主题色", "软件主题色，不同的主题色会影响软件的整体风格", parent.cfg.软件主题色, parent.api.软件主题色, False, "软件主题色",通用设置项,关联的函数=parent.SwitchThemeColor)
        add_combobox_setting_card(FIF.FONT_INCREASE,"软件图标", "软件图标，哪个看着顺眼用哪个", parent.cfg.软件图标, "软件图标", ["太阳", "雪天", "雷雨", "月亮"],通用设置项,关联的函数=parent.ToggleIcon)
        add_slider_setting_card(FIF.IOT,"绘制参考图的图片清晰度", "本质上是绘图时候的dpi数值，越大越清晰，当然绘图速度也越慢", parent.cfg.绘制图像dpi, "绘制图像dpi",通用设置项)
        add_switch_setting_card(FIF.CLEAR_SELECTION, "是否自动显示遮罩", "没有自动显示的话，点一下刷新也能显示，能节省3秒左右的时间", parent.cfg.是否自动显示遮罩, "是否自动显示遮罩",通用设置项)
        add_slider_setting_card(FIF.ALBUM, "自动显示遮罩延迟时间", "自动显示遮罩的延迟时间，单位是毫秒。目标是在绘图区刷新完成后第一时间显示遮罩，但是由于不同类型的数据加载时间不同，用绘图区HTML的加载完成作为信号常常会提前加载导致最后遮罩还是加载不出来。\n所以干脆将这个设置为选项，根据数据情况调整。", parent.cfg.自动显示遮罩延迟时间, "自动显示遮罩延迟时间",通用设置项)
        add_switch_setting_card(FIF.ROTATE, "是否每绘制一步都刷新遮罩", "关掉这个选项也可以点击按钮手动刷新第二幅图的遮罩。虽然是异步执行，但是绘制遮罩也需要时间，直角坐标勉强还算跟手，极坐标图像绘制遮罩需要额外的转换，最快也要10秒，延迟太高了，\n还非常占用计算资源，极坐标图像标注时强烈建议关闭！", parent.cfg.是否每绘制一步都刷新遮罩, "是否每绘制一步都刷新遮罩",通用设置项)
        add_switch_setting_card(FIF.TRANSPARENT, "是否默认预处理", "选择确定后每打开一个新的文件，在绘图之前会预处理，将符合条件的值提前设置为遮罩显示出来，减轻一部分工作量", parent.cfg.是否默认预处理, "是否默认预处理",通用设置项)
        add_switch_setting_card(FIF.UNPIN, "预处理函数只显示输出信息", "打开之后预处理操作只显示输出信息，不执行遮罩替换，速度会快很多，而且遮罩替换的时候太卡了，通知框有可能无法弹出", parent.cfg.预处理函数只显示输出信息, "预处理函数只显示输出信息",通用设置项)
        add_switch_setting_card(FIF.PRINT, "预处理函数代码print替换", "打开之后在预处理代码里面print出来的东西，最终会显示到主窗口的消息通知里面。", parent.cfg.预处理函数代码print替换, "预处理函数代码print替换",通用设置项)
        add_switch_setting_card(FIF.ASTERISK, "是否需要完整报错信息", "打开之后如果报错，下面会显示报错的目标行数", parent.cfg.是否需要完整报错信息, "是否需要完整报错信息",通用设置项)
        add_switch_setting_card(FIF.IMAGE_EXPORT, "批量输出图片时根据图片类型分类", "这个选项如果选否，输出结果是按照文件名分文件夹，如果选是，程序最后会自动转化为按照图片类型分文件夹", parent.cfg.批量输出图片时根据图片类型分类, "批量输出图片时根据图片类型分类",通用设置项)
        add_switch_setting_card(FIF.CALORIES, "批量预处理后是否保存当前文件", "打开之后批量预处理的时候会将遮罩和nan遮罩的修改保存到新的文件里，关闭之后不会保存，默认是开启的，关闭的话请确保批量预处理代码中存在保存文件相关的代码（虽然不建议在预处理代码中保存文件）。", parent.cfg.批量预处理后是否保存当前文件, "批量预处理后是否保存当前文件",通用设置项)
        add_switch_setting_card(FIF.REMOVE_FROM, "是否输出渲染图片同时保存当前修改", "在输出渲染的图像的时候，顺带保存下当前编辑内容，避免切换下一个文件的时候忘了保存（大误）", parent.cfg.是否输出渲染图片同时保存当前修改, "是否输出渲染图片同时保存当前修改",通用设置项)
        add_switch_setting_card(FIF.CHECKBOX, "是否输出渲染图片时输出对应的修改后npz文件", "不开这个选项，将参考图像输出出去的时候，就单纯新建个文件同名文件夹，然后往里面存图片，开了之后就会存按照当前选中内容筛选后的npz文件", parent.cfg.是否输出渲染图片时输出对应的修改后npz文件, "是否输出渲染图片时输出对应的修改后npz文件",通用设置项)
        add_switch_setting_card(FIF.TILES, "是否渲染导出时输出的npz文件按照图片类型分类", "不同类型的图片导出成不同的文件", parent.cfg.是否渲染导出时输出的npz文件按照图片类型分类, "是否渲染导出时输出的npz文件按照图片类型分类",通用设置项)
        add_switch_setting_card(FIF.SYNC, "是否显示参考图片", "如果不显示参考图片可以极大加快打开文件的速度，大概节省6秒左右", parent.cfg.是否加载参考图, "是否加载参考图",通用设置项)
        add_switch_setting_card(FIF.CAMERA, "是否只加载一张参考图片", "预处理好背景图之后再打开这个开关是理论上能够正常使用最快加载速度，一张图不要求特别严格的话其实也可以用来做标记了。", parent.cfg.是否只绘制一张参考图, "是否只加载一张参考图片",通用设置项)
        add_switch_setting_card(FIF.BOOK_SHELF, "有背景图时是否直接加载背景图", "打开之后，npz文件中有“Background”这个键的的时候，代表有缓存的背景图（base64格式），不会再重新计算背景图像，直接加载背景图，可以节省巨量的加载时间", parent.cfg.有背景图时是否直接加载背景图, "有背景图时是否直接加载背景图",通用设置项)
        add_switch_setting_card(FIF.LABEL, "是否使用自定义绘图函数", "自定义绘图函数我是直接exec运行的，还是希望使用者能够校验一下，不要出现安全漏洞", parent.cfg.自定义绘图函数能不能用, "自定义绘图函数能不能用",通用设置项)
        add_switch_setting_card(FIF.MINIMIZE, "是否需要规整数据", "规整数据的意思是将杂七杂八的颜色统一化为“不确定”的颜色，这个功能开不开只影响绘图的时候，因为杂七杂八的颜色保存到遮罩数组的时候都是默认为不确定的，重新加载文件也会是“不确定”的颜色。", parent.cfg.是否需要规整数据, "是否需要规整数据",通用设置项)
        add_switch_setting_card(FIF.CLOUD, "是否要渲染没有蒙版的文件", "这个选项适用于批量输出图片的时候，选择是否要跳过没有编辑过的文件", parent.cfg.是否要渲染没有蒙版的文件, "是否要渲染没有蒙版的文件",通用设置项)



        # # 创建 SwitchSettingCard 并添加到 content_layout
        # switch_card1 = SwitchSettingCard(
        #     icon=FIF.TRANSPARENT,
        #     title="是否默认预处理",
        #     content="选择确定后每打开一个新的文件，在绘图之前会预处理，将符合条件的值提前设置为遮罩显示出来，减轻一部分工作量",
        #     configItem=parent.cfg.是否默认预处理
        # )
        # content_layout.addWidget(switch_card1)

        # # 定义一个函数将收到的值传递给 configItem
        # def pre_checked_change(checked):
        #     parent.api.是否默认预处理 = checked
        # switch_card1.checkedChanged.connect(pre_checked_change)

        边缘参数设置卡集合 = SettingCardGroup("边缘提取效果调整参数",self)



        # 添加五个参数的滑动条设置项
        add_slider_setting_card(FIF.PENCIL_INK,"核大小", "Sobel 算子的核大小，控制边缘检测的精细程度。选择较大的值会使边缘检测结果更平滑。推荐取值范围为 3 或 5。", parent.cfg.边缘提取的核大小, "边缘提取的核大小",边缘参数设置卡集合)
        add_slider_setting_card(FIF.PENCIL_INK,"阈值", "用于二值化边缘检测结果的阈值。较高的值会导致仅检测到强边缘，较低的值会检测到更多的细节。推荐从 50 开始尝试，根据实际效果调整。", parent.cfg.边缘提取的阈值, "边缘提取的阈值",边缘参数设置卡集合)
        add_slider_setting_card(FIF.PENCIL_INK,"形态学核大小", "形态学操作的核大小，用于减少噪点和填补小孔。值越大，形态学操作越强。推荐取值范围为 3 至 7，一般情况下选择 3 或 5 即可。", parent.cfg.边缘提取的形态学核大小, "边缘提取的形态学核大小",边缘参数设置卡集合)
        add_slider_setting_card(FIF.PENCIL_INK,"描线宽度", "绘制轮廓的线条宽度。较大的值会使边缘线条变粗。推荐取值范围为 1 至 3，通常选择 1 或 2 即可得到较好的结果。", parent.cfg.边缘提取的描线宽度, "边缘提取的描线宽度",边缘参数设置卡集合)
        add_slider_setting_card(FIF.PENCIL_INK,"扩展像素", "扩展边缘的像素数量。较大的值会使边缘向外扩展更多像素，模拟 Photoshop 中的扩展效果。推荐取值范围为 0 至 5，大多数情况下选择 0 或 1 即可。", parent.cfg.边缘提取的扩展像素, "边缘提取的扩展像素",边缘参数设置卡集合)


        # 关键一步：将设置卡组添加到内容布局中
        content_layout.addWidget(基础数据项)
        content_layout.addWidget(通用设置项)
        content_layout.addWidget(边缘参数设置卡集合)






        
        # 创建并设置标签
        self.label = SubtitleLabel("苦逼大学狗搞数据标注时写的自己用的省事小脚本……Qt的多线程实在是没搞明白，多线程写的很烂，所以后台计算的时候UI会很卡……献丑了。", self)
        setFont(self.label, 14)
        self.label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.label)  # 将标签添加到内容布局中

        # 将内容容器设置为滚动区域的子窗口
        scroll_area.setWidget(content)

        # 将 QScrollArea 添加到主布局中
        layout.addWidget(scroll_area)

        # 设置样式表去掉滚动区域的边框
        scroll_area.setStyleSheet("QScrollArea { border: none; }")

        # 设置子界面对象名
        self.setObjectName(text.replace(' ', '-'))