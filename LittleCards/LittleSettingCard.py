from importall import *
class AttemptingToRemoveTheBorderFromTheSliderTab(RangeSettingCard):
    """
    试图去除边框但是失败的滑块选项卡
    """
    def __init__(self, configItem, title = "", content=None, parent=None):
        super().__init__(configItem, QIcon(), title, content, parent)
        
        # 去除边框
        self.setStyleSheet("border: none;")
        # 移除图标相关部分，设置self.iconLabel 为纯透明QICON
        # self.iconLabel.setIcon(QIcon())



class ModifiedSwitchTab(SwitchSettingCard):
    """ 将按钮文字改造成 '开' 和 '关' """

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None,
                 configItem: ConfigItem = None, parent=None):
        super().__init__(icon, title, content, configItem, parent)

    def setValue(self, isChecked: bool):
        if self.configItem:
            qconfig.set(self.configItem, isChecked)

        self.switchButton.setChecked(isChecked)
        self.switchButton.setText(
            self.tr('开') if isChecked else self.tr('关'))