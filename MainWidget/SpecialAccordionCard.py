from importall import *
from LittleCards.DictionaryTable import DictTableWidget
from LittleCards.LittleSettingCard import AttemptingToRemoveTheBorderFromTheSliderTab

# 特殊设置的手风琴设置卡
class PowerSettingCard(ExpandGroupSettingCard):

    def __init__(self, parent=None):
        super().__init__(FIF.FILTER, "数据读取设置", "设置读取文件的前置条件，告诉软件要读取的npz里面有哪些键，每个键是什么意思，有多少种要进行标注的数据类型，每一种数据类型对应着什么遮罩数值和绘图颜色。", parent)

        # 创建可修改表格
        self.图像类型对应的源文件的key = DictTableWidget("图像类型对应的源文件的key", "图像类型对应的源文件的key：可编辑，值是要处理的npz文件转化成字典的key，值是那个键对应的意思，值将会显示在参考图上。\n【注意：“Musk”、“Musk_nan”、“Background”这三个键是保留键，有特殊的意义，不能出现在npz文件中。】\n使用预处理功能时，键将会以python变量名的形式出现，因此不能使用python关键字、空格、特殊符号和数字开头作为键，如果需要使用可以使用unicode形近符号作为替代。", self, parent.parentup.api)
        self.addGroupWidget(self.图像类型对应的源文件的key)
        self.图像类型对应的不同对象的选择数值 = DictTableWidget("图像类型对应的不同对象的选择数值", "图像类型对应的不同对象的选择数值：可编辑，键是要识别的类型，值是这个类型代表的数字，这个数字将会代表这个类型出现在生成的遮罩数组上。\n【注意，默认第一个类型是缺失值，对应0，第二个类型是待判断值，对应1，这两个键名字可以改，值和位置顺序不能更改！！！】\n【最后一个键也有特殊作用：一般绘图区不在表格内的颜色都会归到最后一个键对应的颜色，到遮罩数组里就是最后一个键对应的值】", self, parent.parentup.api)
        self.addGroupWidget(self.图像类型对应的不同对象的选择数值)
        self.图像类型对应的不同对象的选择颜色 = DictTableWidget("图像类型对应的不同对象的选择颜色", "图像类型对应的不同对象的选择颜色：可编辑，键是要识别的类型，这个表格里面键的数量和名字都必须和上一个表格里一样，值是在涂色时该类型对应的颜色（十六进制），将会被转化成对应的遮罩数字。\n【注意，默认第一个类型是缺失值，对应#000000纯黑色，第二个类型是待判断值，对应#ffffff纯白色，这两个键名字可以改，十六进制颜色值和位置顺序不能更改！！！】\n【最后一个键也有特殊作用：不在下表内的颜色都会归到最后一个键的颜色，这个键除了**顺序不能变**之外，名字和值和对应的颜色随便用。】", self, parent.parentup.api, colorselect=True)
        self.addGroupWidget(self.图像类型对应的不同对象的选择颜色)



        # 第一组
        self.lightnessLabel = BodyLabel("关闭的话以没有该键作为判断为极坐标的依据，打开的话以拥有该键作为判断为极坐标的依据")
        self.lightnessSwitchButton = SwitchButton("文件中没有以下键则判定为极坐标文件", self, IndicatorPosition.RIGHT)
        self.lightnessSwitchButton.setOnText("文件中拥有以下键则判定为极坐标文件")

        # 设置SwitchButton的初始状态
        self.lightnessSwitchButton.setChecked(parent.parentup.api.是否用拥有该键作为判断极坐标绘图的依据)
        # 定义槽函数以更新是否用拥有该键作为判断极坐标绘图的依据属性
        def updatePolarCoordDecision(checked):
            parent.parentup.api.是否用拥有该键作为判断极坐标绘图的依据 = checked

        # 连接checkedChanged信号到槽函数
        self.lightnessSwitchButton.checkedChanged.connect(updatePolarCoordDecision)





        # 第二组
        self.autoLabel_polar = BodyLabel("判定极坐标的键，必须出现在上面的表格中")
        self.autoComboBox_polar = LineEdit()
        self.autoComboBox_polar.setFixedWidth(135)

        # 在你的类的初始化方法中或者适当的地方设置LineEdit的初始值和连接信号
        self.autoComboBox_polar.setText(parent.parentup.api.用于判定是否使用极坐标绘图的的键)  # 设置初始值
        # 定义槽函数以更新属性
        def updateKey_polar(text):
            parent.parentup.api.用于判定是否使用极坐标绘图的的键 = text

        self.autoComboBox_polar.textChanged.connect(updateKey_polar)  # 连接信号到槽函数



        # 第三组
        self.autoLabel_painter = BodyLabel("用于绘制绘图区背景图的键，必须出现在上面的表格中。这个键对应的二维数组的灰度图像将加载为绘制的背景图，背景图会对填色工具的效果有影响。")
        self.autoComboBox_painter = LineEdit()
        self.autoComboBox_painter.setFixedWidth(135)

        # 在你的类的初始化方法中或者适当的地方设置LineEdit的初始值和连接信号
        self.autoComboBox_painter.setText(parent.parentup.api.用于绘制绘图区背景图的键)  # 设置初始值
        # 定义槽函数以更新属性
        def updateKey_painter():
            text = self.autoComboBox_painter.text()  # 直接从LineEdit获取当前文本
            if text not in list(parent.parentup.api.图像类型对应的源文件的key.values()):
                self.autoComboBox_painter.setText(parent.parentup.api.用于绘制绘图区背景图的键) 
                logger.warning(f"用于绘制绘图区背景图的键{text}不在图像类型对应的源文件的key里面，可能会导致绘图区背景图无法显示，所以不允许使用。")
                parent.parentup.api.显示消息框函数("warning", "数据读取设置填写不规范", f"用于绘制绘图区背景图的键【{text}】不在表格一的“值”里面，可能会导致绘图区背景图无法显示，请重新输入。", "底部")
            else:
                parent.parentup.api.用于绘制绘图区背景图的键 = text

        self.autoComboBox_painter.editingFinished.connect(updateKey_painter)  # 连接编辑完成信号到槽函数

        # 第四组
        ReferenceImage_Container_Slider = AttemptingToRemoveTheBorderFromTheSliderTab(
            parent.parentup.cfg.显示参考图的行数,
            title="显示多少行参考图",
            content="设置参考图容器的数量，滑动条设置的整数为n时，容器的数量为2n。如果表一的键的数量是2n-1，那么最后一个容器不显示。\n如果表一的键大于参考图容器的数量，会在日志中报错，但是实际使用不受影响，能显示多少显示多少。",
        )
        # ReferenceImage_Container_Slider.valueChanged.connect(要连接的函数) #啥时候要用到再说吧


        # 第五组
        self.modeButton = PushButton("立即应用修改")
        self.modeLabel = BodyLabel("点击刷新上面修改的内容到主程序中，然后立即再次加载文件使之生效，不想立刻重载文件的话不要点这个按钮（修改了参考图容器数量得点）。")
        self.modeButton.setFixedWidth(135)
        self.modeButton.clicked.connect(parent.parentup.api.更新初始自定义变量)




        # 调整内部布局
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.viewLayout.setSpacing(0)


        # 添加各组到设置卡中
        self.add(self.lightnessLabel, self.lightnessSwitchButton)
        self.add(self.autoLabel_polar, self.autoComboBox_polar)
        self.add(self.autoLabel_painter, self.autoComboBox_painter)
        self.addGroupWidget(ReferenceImage_Container_Slider)
        self.add(self.modeLabel, self.modeButton)



    def add(self, label, widget):
        w = QWidget()
        w.setFixedHeight(60)

        layout = QHBoxLayout(w)
        layout.setContentsMargins(48, 12, 48, 12)

        layout.addWidget(label)
        layout.addStretch(1)
        layout.addWidget(widget)

        # 添加组件到设置卡
        self.addGroupWidget(w)