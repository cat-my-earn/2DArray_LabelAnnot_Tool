from importall import *

class DataAnnotation(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1766, 1099)
        Dialog.setStyleSheet(u"background:white")
        self.widget = QWidget(Dialog)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(9, 9, 1811, 1081))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = ScrollArea(self.widget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"border: none;")
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 1776, 2350))
        self.scrollAreaWidgetContents_2.setMinimumSize(QSize(1600, 2350))
        self.scrollAreaWidgetContents_2.setMaximumSize(QSize(10000, 10000))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer_30 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_30, 9, 8, 2, 1)

        self.verticalSpacer_17 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_17, 1, 22, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_5, 9, 10, 2, 1)

        self.verticalSpacer_27 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_27, 5, 20, 1, 1)

        self.verticalSpacer_21 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_21, 11, 20, 1, 1)

        self.verticalSpacer_8 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_8, 11, 11, 1, 2)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_20, 9, 19, 2, 1)

        self.verticalSpacer_32 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_32, 1, 20, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 17, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_5, 8, 11, 1, 2)

        self.selectfiles = PrimaryPushButton(self.scrollAreaWidgetContents_2)
        self.selectfiles.setObjectName(u"selectfiles")
        self.selectfiles.setMinimumSize(QSize(130, 40))

        self.gridLayout.addWidget(self.selectfiles, 2, 11, 3, 2)

        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_22, 6, 21, 2, 1)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_18, 2, 19, 3, 1)

        self.outputclearpic = PushButton(self.scrollAreaWidgetContents_2)
        self.outputclearpic.setObjectName(u"outputclearpic")
        self.outputclearpic.setMinimumSize(QSize(0, 33))

        self.gridLayout.addWidget(self.outputclearpic, 6, 20, 2, 1)

        self.horizontalSpacer_28 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_28, 2, 8, 3, 1)

        self.horizontalSpacer_2 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 2, 5, 3, 1)

        self.showedge = PushButton(self.scrollAreaWidgetContents_2)
        self.showedge.setObjectName(u"showedge")
        self.showedge.setMinimumSize(QSize(0, 33))

        self.gridLayout.addWidget(self.showedge, 9, 22, 2, 1)

        self.savefileall = PushButton(self.scrollAreaWidgetContents_2)
        self.savefileall.setObjectName(u"savefileall")
        self.savefileall.setMinimumSize(QSize(0, 33))

        self.gridLayout.addWidget(self.savefileall, 6, 14, 2, 1)

        self.verticalSpacer_30 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_30, 1, 16, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_7, 11, 1, 1, 6)

        self.widget_3 = QWidget(self.scrollAreaWidgetContents_2)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(0, 40))

        self.gridLayout.addWidget(self.widget_3, 9, 9, 1, 1)

        self.widget_4 = QWidget(self.scrollAreaWidgetContents_2)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setMinimumSize(QSize(0, 40))

        self.gridLayout.addWidget(self.widget_4, 2, 9, 1, 1)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_19, 6, 19, 2, 1)

        self.verticalSpacer_15 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_15, 8, 14, 1, 1)

        self.showall = PushButton(self.scrollAreaWidgetContents_2)
        self.showall.setObjectName(u"showall")
        self.showall.setMinimumSize(QSize(0, 33))

        self.gridLayout.addWidget(self.showall, 9, 16, 2, 1)

        self.verticalSpacer_19 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_19, 8, 22, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 17, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_4, 5, 11, 1, 2)

        self.preprocessingall = PushButton(self.scrollAreaWidgetContents_2)
        self.preprocessingall.setObjectName(u"preprocessingall")
        self.preprocessingall.setMinimumSize(QSize(0, 33))

        self.gridLayout.addWidget(self.preprocessingall, 9, 14, 2, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_9, 2, 13, 3, 1)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_11, 2, 15, 3, 1)

        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_23, 9, 21, 2, 1)

        self.verticalSpacer_11 = QSpacerItem(20, 17, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_11, 1, 4, 1, 1)

        self.verticalSpacer_10 = QSpacerItem(20, 17, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_10, 1, 6, 1, 1)

        self.widget_2 = QWidget(self.scrollAreaWidgetContents_2)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(0, 40))

        self.gridLayout.addWidget(self.widget_2, 6, 9, 1, 1)

        self.verticalSpacer_29 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_29, 5, 16, 1, 1)

        self.refreshmask = PushButton(self.scrollAreaWidgetContents_2)
        self.refreshmask.setObjectName(u"refreshmask")
        self.refreshmask.setMinimumSize(QSize(140, 40))

        self.gridLayout.addWidget(self.refreshmask, 2, 22, 3, 1)

        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_21, 2, 21, 3, 1)

        self.verticalSpacer_16 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_16, 11, 14, 1, 1)

        self.verticalSpacer_14 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_14, 5, 14, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_7, 6, 0, 2, 1)

        self.verticalSpacer_18 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_18, 5, 22, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 17, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 5, 4, 1, 1)

        self.verticalSpacer_31 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_31, 1, 18, 1, 1)

        self.verticalSpacer_24 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_24, 8, 16, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 17, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_6, 8, 1, 1, 6)

        self.importpainter = PushButton(self.scrollAreaWidgetContents_2)
        self.importpainter.setObjectName(u"importpainter")
        self.importpainter.setMinimumSize(QSize(0, 33))

        self.gridLayout.addWidget(self.importpainter, 6, 22, 2, 1)

        self.horizontalSpacer_32 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_32, 9, 23, 1, 1)

        self.openfiles = PrimaryPushButton(self.scrollAreaWidgetContents_2)
        self.openfiles.setObjectName(u"openfiles")
        self.openfiles.setMinimumSize(QSize(130, 40))

        self.gridLayout.addWidget(self.openfiles, 2, 1, 3, 2)

        self.horizontalSpacer_31 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_31, 2, 23, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_8, 9, 0, 2, 1)

        self.verticalSpacer_28 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_28, 5, 18, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 17, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 5, 1, 1, 2)

        self.verticalSpacer_3 = QSpacerItem(20, 17, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_3, 5, 6, 1, 1)

        self.previousfile = PushButton(self.scrollAreaWidgetContents_2)
        self.previousfile.setObjectName(u"previousfile")
        self.previousfile.setMinimumSize(QSize(130, 40))

        self.gridLayout.addWidget(self.previousfile, 2, 14, 3, 1)

        self.refresh = PushButton(self.scrollAreaWidgetContents_2)
        self.refresh.setObjectName(u"refresh")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(140)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refresh.sizePolicy().hasHeightForWidth())
        self.refresh.setSizePolicy(sizePolicy)
        self.refresh.setMinimumSize(QSize(130, 40))

        self.gridLayout.addWidget(self.refresh, 2, 18, 3, 1)

        self.verticalSpacer_23 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_23, 11, 16, 1, 1)

        self.loadlastfile = PushButton(self.scrollAreaWidgetContents_2)
        self.loadlastfile.setObjectName(u"loadlastfile")
        self.loadlastfile.setMinimumSize(QSize(0, 33))

        self.gridLayout.addWidget(self.loadlastfile, 6, 16, 2, 1)

        self.verticalSpacer_9 = QSpacerItem(20, 17, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_9, 1, 11, 1, 2)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_12, 6, 15, 2, 1)

        self.horizontalSpacer = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 3, 3, 1)

        self.preprocessing = PushButton(self.scrollAreaWidgetContents_2)
        self.preprocessing.setObjectName(u"preprocessing")
        self.preprocessing.setMinimumSize(QSize(0, 33))

        self.gridLayout.addWidget(self.preprocessing, 9, 11, 2, 2)

        self.horizontalSpacer_3 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 2, 10, 3, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_10, 6, 13, 2, 1)

        self.showmask = PushButton(self.scrollAreaWidgetContents_2)
        self.showmask.setObjectName(u"showmask")
        self.showmask.setMinimumSize(QSize(140, 40))

        self.gridLayout.addWidget(self.showmask, 2, 20, 3, 1)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_15, 2, 17, 3, 1)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_16, 6, 17, 2, 1)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_14, 9, 13, 2, 1)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_17, 9, 17, 2, 1)

        self.correctingposition = PushButton(self.scrollAreaWidgetContents_2)
        self.correctingposition.setObjectName(u"correctingposition")
        self.correctingposition.setMinimumSize(QSize(0, 33))

        self.gridLayout.addWidget(self.correctingposition, 6, 18, 2, 1)

        self.showfiles = ComboBox(self.scrollAreaWidgetContents_2)
        self.showfiles.setObjectName(u"showfiles")
        self.showfiles.setMinimumSize(QSize(330, 40))

        self.gridLayout.addWidget(self.showfiles, 2, 6, 3, 1)

        self.verticalSpacer_13 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_13, 1, 14, 1, 1)

        self.savefile = PushButton(self.scrollAreaWidgetContents_2)
        self.savefile.setObjectName(u"savefile")
        self.savefile.setMinimumSize(QSize(0, 33))

        self.gridLayout.addWidget(self.savefile, 6, 11, 2, 2)

        self.horizontalSpacer_6 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_6, 2, 0, 3, 1)

        self.choosemaskselect = ComboBox(self.scrollAreaWidgetContents_2)
        self.choosemaskselect.setObjectName(u"choosemaskselect")
        self.choosemaskselect.setMinimumSize(QSize(0, 33))

        self.gridLayout.addWidget(self.choosemaskselect, 9, 18, 2, 1)

        self.page_selector = ComboBox(self.scrollAreaWidgetContents_2)
        self.page_selector.setObjectName(u"page_selector")
        self.page_selector.setMinimumSize(QSize(200, 40))

        self.gridLayout.addWidget(self.page_selector, 2, 4, 3, 1)

        self.verticalSpacer_22 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_22, 11, 18, 1, 1)

        self.verticalSpacer_25 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_25, 8, 18, 1, 1)

        self.verticalSpacer_26 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_26, 8, 20, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 6, 10, 2, 1)

        self.verticalSpacer_20 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_20, 11, 22, 1, 1)

        self.nextfile = PushButton(self.scrollAreaWidgetContents_2)
        self.nextfile.setObjectName(u"nextfile")
        self.nextfile.setMinimumSize(QSize(150, 40))

        self.gridLayout.addWidget(self.nextfile, 2, 16, 3, 1)

        self.verticalSpacer_12 = QSpacerItem(20, 17, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_12, 1, 1, 1, 2)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_13, 9, 15, 2, 1)

        self.horizontalSpacer_29 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_29, 6, 8, 2, 1)

        self.clearmask = PushButton(self.scrollAreaWidgetContents_2)
        self.clearmask.setObjectName(u"clearmask")
        self.clearmask.setMinimumSize(QSize(0, 33))

        self.gridLayout.addWidget(self.clearmask, 9, 20, 2, 1)

        self.widget_5 = QWidget(self.scrollAreaWidgetContents_2)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setMinimumSize(QSize(0, 40))

        self.gridLayout.addWidget(self.widget_5, 2, 7, 1, 1)

        self.savepath = SearchLineEdit(self.scrollAreaWidgetContents_2)
        self.savepath.setObjectName(u"savepath")
        self.savepath.setMinimumSize(QSize(630, 33))
        self.savepath.setMaximumSize(QSize(16777215, 33))

        self.gridLayout.addWidget(self.savepath, 6, 1, 2, 7)

        self.preprocessing_code = SearchLineEdit(self.scrollAreaWidgetContents_2)
        self.preprocessing_code.setObjectName(u"preprocessing_code")
        self.preprocessing_code.setMinimumSize(QSize(630, 33))
        self.preprocessing_code.setMaximumSize(QSize(16777215, 33))

        self.gridLayout.addWidget(self.preprocessing_code, 9, 1, 2, 7)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")

        # 添加基础的两个 WebEngineView 组件
        self.painter = QWebEngineView(self.scrollAreaWidgetContents_2)
        self.painter.setObjectName(u"painter")
        self.painter.setMinimumSize(QSize(790, 500))

        self.mask = QWebEngineView(self.scrollAreaWidgetContents_2)
        self.mask.setObjectName(u"mask")
        self.mask.setMinimumSize(QSize(790, 500))

        self.gridLayout_3.addWidget(self.painter, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.mask, 0, 2, 1, 1)

        self.verticalSpacer_first = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalSpacer_second = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.horizontalSpacer_first = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalSpacer_second = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.verticalSpacer_first, 1, 0, 1, 1)
        self.gridLayout_3.addItem(self.verticalSpacer_second, 1, 2, 1, 1)
        self.gridLayout_3.addItem(self.horizontalSpacer_first, 0, 1, 1, 1)
        self.gridLayout_3.addItem(self.horizontalSpacer_second, 0, 3, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_3)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", "Dialog", None))
        self.selectfiles.setText(QCoreApplication.translate("Dialog", "选择文件", None))
        self.outputclearpic.setText(QCoreApplication.translate("Dialog", "导出渲染参考", None))
        self.showedge.setText(QCoreApplication.translate("Dialog", "遮罩边缘提取", None))
        self.savefileall.setText(QCoreApplication.translate("Dialog", "批量保存图片", None))
        self.showall.setText(QCoreApplication.translate("Dialog", "显示原始参考图", None))
        self.preprocessingall.setText(QCoreApplication.translate("Dialog", "批量预处理", None))
        self.refreshmask.setText(QCoreApplication.translate("Dialog", "刷新遮罩预览", None))
        self.importpainter.setText(QCoreApplication.translate("Dialog", "导入绘图函数", None))
        self.openfiles.setText(QCoreApplication.translate("Dialog", "打开文件夹", None))
        self.previousfile.setText(QCoreApplication.translate("Dialog", "上一张", None))
        self.refresh.setText(QCoreApplication.translate("Dialog", "刷新绘图区", None))
        self.loadlastfile.setText(QCoreApplication.translate("Dialog", "加载保存文件", None))
        self.preprocessing.setText(QCoreApplication.translate("Dialog", "预处理", None))
        self.showmask.setText(QCoreApplication.translate("Dialog", "隐藏遮罩", None))
        self.correctingposition.setText(QCoreApplication.translate("Dialog", "校正光标位置", None))
        self.showfiles.setText(QCoreApplication.translate("Dialog", "显示可选择的文件", None))
        self.savefile.setText(QCoreApplication.translate("Dialog", "保存", None))
        self.choosemaskselect.setText(QCoreApplication.translate("Dialog", "遮罩可选项", None))
        self.page_selector.setText(QCoreApplication.translate("Dialog", "显示页码", None))
        self.nextfile.setText(QCoreApplication.translate("Dialog", "下一张", None))
        self.clearmask.setText(QCoreApplication.translate("Dialog", "消除遮罩部分", None))

