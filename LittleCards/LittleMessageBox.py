from importall import *
class CustomMessageBox(MessageBoxBase):
    """ 自定义对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.绘图函数对话框标头 = SubtitleLabel('加载自定义绘图函数')
        self.绘图函数对话框警告正文 = TextEdit()

        self.绘图函数对话框警告正文.setPlaceholderText('等待修改')

        # 将组件添加到布局中
        self.viewLayout.addWidget(self.绘图函数对话框标头)
        self.viewLayout.addWidget(self.绘图函数对话框警告正文)

        # 设置对话框的最小宽度
        self.widget.setMinimumWidth(900)
        self.widget.setMinimumHeight(600)

        # 在子类中将按钮文本改为中文
        self.yesButton.setText(self.tr('确定'))
        self.cancelButton.setText(self.tr('取消'))