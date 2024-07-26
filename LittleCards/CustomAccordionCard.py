from importall import *
from LittleCards.LittleSettingCard import AttemptingToRemoveTheBorderFromTheSliderTab

# 自定义的手风琴设置卡，用于添加开关设置卡和范围设置卡
class PowerSettingCardCustom(ExpandGroupSettingCard):
    """
    自定义的手风琴设置卡，用于添加开关设置卡和范围设置卡
    """
    def __init__(self, icon, title, content, parent=None):
        super().__init__(icon, title, content, parent)
        
        # 存储开关设置卡和范围设置卡的列表
        self.switch_settings = []
        self.range_settings = []

        # 调整内部布局
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.viewLayout.setSpacing(0)

    def add_switch_setting(self, 开文本, 关文本, 描述文字, 绑定的类, 绑定的类对象, 调用的函数 = None):
        label = BodyLabel(描述文字)
        switch_button = SwitchButton(关文本, self, IndicatorPosition.RIGHT)
        switch_button.setOnText(开文本)
        initial_state = getattr(绑定的类, 绑定的类对象)
        switch_button.setChecked(initial_state)
        def update_state(checked):
            setattr(绑定的类, 绑定的类对象, checked)
            if 调用的函数!=None:
                调用的函数(checked)
        switch_button.checkedChanged.connect(update_state)
        self.add(label, switch_button)
        self.switch_settings.append((label, switch_button))

    def add_slider_setting(self, 标题, 正文, 配置类对象,关联的函数 = None):
        slider_card = AttemptingToRemoveTheBorderFromTheSliderTab(
            配置类对象,
            title=标题,
            content=正文,
        )
        def value_change(value):
            if 关联的函数!=None:
                关联的函数(value)
        slider_card.valueChanged.connect(value_change)
        self.addGroupWidget(slider_card)

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