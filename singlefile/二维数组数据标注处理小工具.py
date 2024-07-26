# 我原来只是写着自己用的，所以全写的中文变量名，我知道我写的全是答辩，QAQ

import sys
import math
import shutil
import traceback
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
import base64
import time
import numpy as np
import pandas as pd
import cv2
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib as mpl
from matplotlib.cm import ScalarMappable
import matplotlib.style as mplstyle
from PIL import Image
import io
import re
import ast
import astor
import os
import random
from alive_progress import alive_bar
from datetime import datetime, timedelta
from typing import Union
import gzip
import json
import threading

# PySide6 导入
from PySide6.QtCore import (QCoreApplication,QMetaObject, QObject,
                             QRect, QSize, Qt, Slot, Signal,  QThread,QTimer)
from PySide6.QtGui import ( QIcon,QKeyEvent,Qt, QColor,QImage,QPixmap)
from PySide6.QtWidgets import (QApplication,  QFileDialog, QVBoxLayout, QWidget,QHBoxLayout,QGridLayout,
                            QSpacerItem, QSizePolicy, QVBoxLayout, QTableWidget, QTableWidgetItem)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebChannel import QWebChannel

# qfluentwidgets 导入
from qfluentwidgets import (ComboBox, PrimaryPushButton, PushButton, ScrollArea,
                            SearchLineEdit, NavigationItemPosition, FluentWindow,
                            SubtitleLabel, setFont, InfoBar, InfoBarPosition,
                            InfoBarIcon, SwitchSettingCard, StateToolTip, Theme, setTheme,setThemeColor,
                            FluentIcon as FIF,
                            ScrollArea, RangeSettingCard, SettingCardGroup, ConfigItem,
                            RangeConfigItem, RangeValidator, BoolValidator, MessageBoxBase,
                            TextEdit, qconfig,QConfig, Flyout, FlyoutAnimationType, FlyoutViewBase,
                            SwitchButton, IndicatorPosition,ExpandGroupSettingCard,PrimaryPushSettingCard,
                            ToolTipFilter,ToolTipPosition,BodyLabel,TransparentPushButton,TableWidget,
                            LineEdit,ColorPickerButton,ColorConfigItem,OptionsConfigItem,OptionsValidator,
                            FluentIconBase,ComboBoxSettingCard,ColorSettingCard,ProgressBar)

from loguru import logger
logger.remove()#删去import logger之后自动产生的handler，不删除的话会出现重复输出的现象
logger.add("日志.log", rotation="500 MB", retention="60 days", level="INFO",enqueue=True)#日志记录
try:
    logger.add(sys.stderr, level="DEBUG")  # 同时输出到控制台
except:pass
logger.info("日志记录已开启")


mplstyle.use('fast')
matplotlib.use('QtAgg')# 绘图后台使用Qt

# 中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

Documentation = """
###   功能介绍

 

该软件主要作用是对格式规整的二维数组进行像素级数据标注，输入文件必须是包含各种二位数组的npz格式文件，并对其进行像素级的数据标注，然后将标注的内容以一个和原始数据二维数组尺寸一样的遮罩数组的形式叠加在原始npz文件里。处理后可以方便地将遮罩提取出来，用以进行神经网络训练等各种操作。

 

该软件的建议使用范围为百万像素（数组一二维相乘）左右的数组，同时采用直角坐标绘图，基本跟手。极限大概在千万像素，这个时候绘图就会有3~4秒的延迟了——千万像素级的运算量有点太大了，超出我当前优化能力范围。不是特别在意延迟的话，很大很大的数组也不是不可以用……

 

该软件支持极坐标二维数组，但是极坐标运算量较大，毕竟转化成图像之后是R²的像素量。绘图时延迟和同量级的直角坐标数组类似，但加载背景图像和遮罩图像的时候，极坐标转化到画布上运算量较大，在预处理计算好背景图像且不加载遮罩图像的情况下，使用效率和直角坐标近似。

 

由于多线程没写好，在大量运算时界面会卡顿——不过加了很多手动刷新，大多数时候不会完全卡死不动，由此带来的糟糕使用体验深感抱歉。

 

###   使用步骤

 

* 第一步

 

将需要进行标注的二维数组储存到一个npz文件中，一个npz文件可以有不同的二维数组，它们具备关联性，但是每个二维数组的尺寸都必须相同，例如一个卫星传感器的不同通道，而且值必须是纯数字，否则无法绘图。值不是纯数字的数组需要先将所有的值转化为纯数字，才能正常加载。不同的二维数组将作为参考图辅助进行数据标注——可以用中文或者英文的键在npz文件中标明其意义，但是这个键必须符合python变量名命名规则。

 

* 第二步

 

将已经存在的配置文件.json删除（假如有的话），重新打开软件，在设置界面的“数据读取设置”一栏，单击右边小箭头打开，查看填注说明，在第一个表格的“值”部分填写需要进行标注的npz文件的键，第一个表格的“键”部分填写其对应的意义（这个将会出现在参考图的标题部分，可以写得详细一些以方便辨别）。实际使用的npz的键必须能全部包含第一个表格的“值”（除了保留的三个和npz的序列化键之外），可以多余，但是不能少于，少于会报错。

 

接下来的两个表格键的部分必须相同。键的部分代表需要对二维数组的数据标注出多少种类型，注意表格第一行第二行和最后一行为保留位置，具体参照填写说明。第二个表格填写内容为出现在二维数组遮罩层上的对应标注类型的数字。第三个表格填写内容为对应标注类型在绘图过程中代表的颜色。

 

* 第三步

 

选择绘图类型为极坐标还是直角坐标，程序的判断依据为npz文件中包含或者不包含某个键，可以在数据读取设置界面自定义设置。同时还要选择作为绘图背景的数据键，程序会根据这个键计算出对应的灰度图，作为绘图区域的背景。然后点击“导入自定义绘图函数按钮”来导入自定义的绘图函数，并且在“绘图区底图设置”和“传输遮罩数组设置”中修改绘图区背景图像（比如转置、上下翻转、左右翻转、极坐标的旋转等，使绘图区背景的灰度图像和参考图像对应上），使参考图、遮罩、绘图区底图三者位置一致。

 

注意，如果没有自定义绘图函数的话，就不要去修改绘图区底图。修改底图的功能是搭配自定义绘图函数使用的，用来处理底图和绘制的参考图方向不一或者产生镜像问题的情况。自带的基础绘图函数在处理直角坐标的时候是直接显示，也就是(0,0)的定位是在左上角。整体程序处理极坐标的时候默认data[x][y]中的x为角度，y为半径，如果没有提前预处理数据的话，也可以使用设置界面绘图区底图里的的转置功能。

 

然后是选择显示参考图的数量。程序可以动态加载参考图容器，一行两个，可以自定义行数。参考图容器数量大于可显示的键的数量，则会有一部分容器什么都不显示。反之小于的话，则显示前2n个键对应的参考图（同时会在日志里报错，但是不影响使用）。

 

使用过程中也可以修改这些数据读取参数，点击立即应用修改按钮即可重新加载文件生效。

 

* 第四步

 

确定生成了配置文件.json后关闭软件，重新打开软件，如果在主界面能够看到生成的图片，就表明已经可以进行数据标注了。左边一列第一个容器是绘图区容器，右边一列第第一个容器是显示遮罩的容器。除此之外其他都是参考图容器。

 

如果参考图过于模糊，可以在设置界面的“绘制参考图的图片清晰度”里进行调整，到其和绘图区背景图的清晰度一致即可。这个选项开的太大会导致参考图计算太久或者生成的图片太大加载不出来。

 

如果要使用参考线和Ctrl键附带的功能，需要先点击“矫正光标位置”按钮，而后有详细的操作步骤浮现——不使用自定义函数也需要矫正光标位置，因为不同的数据绘制成参考图后缩放比例和坐标轴起点都不一样，这是matplotlib的性质决定的。

 

 

###   标注方式

 

* 加载速度

 

如果涉及到绘制极坐标，每加载一次文件，都要计算绘图区域的极坐标灰度图，计算时间为10s上下，如果是直角坐标则为2s上下，建议将所有的npz文件都进行预处理，提前计算好背景图，可以极大提升加载速度。

 

但是注意，如果在绘图区右侧显示遮罩数组图像的话，这个计算时间是避免不了的，直角坐标图像有传输数据压缩优化，还算跟手，极坐标非常慢，建议需要的时候再显示遮罩图像，关闭设置界面里“是否每绘制一步都刷新遮罩”选项。

 

* 计算背景图的方式

 

先打开到所有npz文件所在目录，再填写文件保存路径，然后在预处理框中输入代码【背景图片=生成背景图(雷达反射率)】，然后点击批量预处理按钮，点击开始，然后等到进度条结束，就会在文件保存路径下生成预处理好的文件，用那些文件进行加载标注可以提升加载速度。

 

可以在设置界面指定用于计算背景图像的数组在npz文件中的键，这个计算的本质是在npz文件中创建了一个新的键“Background”，用于储存背景图像的Base64码，因此如果有自定义背景图像的需求，可以用同样的思路预处理npz文件。

 

想要更换参考图片容器里显示的参考图，无论是顺序，还是显示不在加载范围内的参考图，只需要在“数据读取设置”里面的表一修改对应的键值顺序和内容，再刷新应用即可。

 

* 计算标注区域的方式

 

标注区域将会以“Musk_nan”为键，以二维数组的形式储存在npz文件中，其尺寸和原始数据相同，值为0（不可被标注区域）和1（可被标注区域）。

 

没有“Musk_nan”键的文件载入的时候会自动以背景图像中的缺失值设置不可标注区域，其他区域设置为可标注区域。如果需要自定义可标注区域的，也可以使用同样的思路——将需要标注和不需要标注的区域以尺寸相同的缺失值数组存入npz文件之中，加载处理后的文件即可。

 

* 标注结果

 

结果会以“Musk”为键储存在标注好保存后的npz文件中，将npz文件load成为python字典后，提取对应的值，就是尺寸等于被标注的二维数组的一个二维数组，其值为“数据读取设置”里表格二代表着标注类型的各个数字。代表着对应位置的原始数据点被标注为对应的类型。

 

储存的npz文件中也会有键为“Musk_nan”的数组，代表缺失值数组，由0和1组成。

 

为什么是Musk而不是Mask，是写代码的时候输错了，一路将错就错，到后面改不过来了……正好Musk这个词不常用，而Mask是个常用词，不将其占用掉。

 

* 标注工具

 

目前能够使用的标注工具主要有画笔（笔刷为圆形，画笔宽度可调节）、多边形、圆形、矩形、填充（可以调节颜色容差和遇到边界时候的跳跃像素点数量）。画笔一般用来进行像素级标注，圆形和矩形用来大面积标注，多边形用来标注边缘明确的区域，填充工具可以通过背景图的色差批量标注一个区域。

 

主要的操作过程就是利用这些工具选择不同颜色在绘图区域上绘制，绘制的过程就是标注的过程，不同的标注值回以不同颜色显示，绘制完成后点击保存按钮，在填写的保存路径上就会生成标注后的对应文件（没有保存路径就会在原始路径生成，但是文件名不一样）。用该程序打开标注后的npz文件，可以看到之前标注的遮罩，如果没有看到，请点击刷新绘图区并且等待一会儿。

 

按住Alt可以拖动画布，鼠标滚轮可以放大缩小画布，按下Shift键拖动鼠标可以在参考图上用十字标注线标注出对应的鼠标位置。按下Ctrl键可以将参考图都移动到绘制区域所在位置，但是注意，Ctrl键的缩放受到参考图里坐标区域占据整体的百分比的影响，如果参考图总面积和坐标区域面积相差太大，缩放效果会很差。

 

 

###   常用功能

 

* 快捷键

 

长按shift键可以让参考图的十字参考线出现在绘图区域的鼠标位置，点击ctrl键可以将参考图缩放移动到绘图区域所在位置。每个按钮都有对应的快捷键，具体可以将鼠标放在按钮上查看详细信息，ctrl加上其他按键可以组成组合快捷键。

 

* 切换文件

 

打开文件夹到对应的目录后，选择页码，再选择对应的文件，然后点击选择文件，即可开始加载文件。点击上一张和下一张可以直接加载文件顺序位于其前后的npz文件，而无需多次点击选择文件按钮。使用ctrl+键盘上<>两个键可以快速触发上一张和下一张的切换。

 

* 绘图区域和遮罩预览相关

 

软件的运行逻辑是：绘制实际上是与webview容器交互，每交互一次，webview就会更新一次主程序里储存的遮罩数组变量和颜色数组变量。但是主程序与容器交互的时候传递的都是颜色数组而非数值数组，数值数组一般只会在加载文件时转化更新颜色数组。因此在绘图区域内实际操作的并非真正会被储存到文件中的遮罩。

 

在Qt中运行webview容器有可能会出现一些bug，出bug了先重新加载文件，再不行就删除配置文件重新启动。

 

查看实际储存的遮罩数组变量有两个方式，一个是刷新绘图区按钮，一个是刷新遮罩预览按钮。刷新遮罩预览会将实际上的遮罩数组以图片的形式显示在右边——绘图区为了方便绘图，并不完全“所见即所得”。刷新绘图区按钮会将主程序内的遮罩数组传递给绘图webview，用于“实际上存在遮罩但是主绘图区域显示不出来”的情况，主要是由于Qt和webview的交互问题。

 

* 文件相关

 

因为保存文件的路径和实际打开文件的路径不一致，所以专门有一个按钮加载上一个保存的文件，方便突然想修改，而不用专门切换到文件保存路径。

 

修改后的文件要专门点击保存按钮才会被保存到保存路径中——但是在设置面板中开启相应的开关后，导出渲染图片的时候也可以顺便保存文件。

 

* 矫正光标

 

绘图区是只有数据图像，而参考图通过matplotlib进行绘制，往往还有坐标轴和色标，其像素点和比例不一定对应，因此需要校准光标位置才能保证十字参考线能够在参考图上，标出在绘图区域鼠标的位置。ctrl键的使用也需要矫正光标。点击对应的按钮，按照提示操作即可。

 

* 绘图相关功能区

 

1. 在数据标注时，参考图是必不可少的，但是不同的图像需要不同的绘制方式，也有不同的色标，因此软件支持导入自定义绘图函数。

 

2. 主程序通过调用导入的绘图函数进行绘图，如果没有导入或者没有开启使用绘图函数的功能，则使用默认的绘图函数进行绘制。自定义绘图函数能够获取的参数包括：需要进行绘制的二维数组、该数据的类型（在第一个表格中“键”部分填写的东西）、是否绘制极坐标图、当前使用的npz文件文件名。用户需要在函数体内根据这些参数完成绘图，同时将绘图结果用plt.show()表示出来。实际的程序定义在点击导入自定义函数按钮的时候会有详细说明。
   【一定要仔细看说明！！定义色标等各种量的时候定义成函数域内变量，不要定义成全局变量！！！全局变量只能有一个函数名！！需要用到matplotlib、numpy、pandas、PIL、cv2之外的库，需要去源代码的主程序里import，在】

 

3. 如果自定义绘图函数执行出错，程序一般会假死崩溃，这个时候去【配置文件.json】内将是否使用自定义绘图函数改成false，即可重新正常启动程序。修正自定义绘图函数后再次导入即可。

 

4. 程序还提供了导出参考图的功能，如果有大量npz文件等待绘制，也可以点击“批量保存图片”一键一次性导出成图像……当然并不建议这么做，程序内绘图肯定没有自己写代码批量绘图效率高。但是如果有一张图需要立刻得到png版本，有这个按钮也可以省却写代码的工作量。

 

5. 遮罩也可以和参考图相结合，可以在选择遮罩类型处勾选需要的遮罩类型（选中之后，想要取消，需要先选中其他的，然后再点回想要取消的那一个，即可取消，推荐用“请选择遮罩类型"进行中转，不会误操作其他的）然后点击消去遮罩部分即可得到将对应的遮罩消除的参考图像。

 

6. 如果点击遮罩边缘提取，则是使用sobel算子进行边缘提取，然后将边缘在参考图上以散点图绘制出来。本质上就是将涂色的地方圈出来，适用于需要画圈的场合。消除遮罩区域和画圈可以结合起来，两个先后点就可以了。点击消除遮罩区域后，想要获得包含遮罩区域的画圈图，则需要先点击“显示原始参考图”以消除标志位（程序是根据标志位判定要不要画特殊的图）。

 

7. 当然这些特殊的图也可以导出，如果有绘制这些图片的需求的话，也相当于节省了很大一部分代码。

 

8. 导出图片时候也支持导出【按照当前显示的参考图修改后的npz原始数据】或者【按照当前显示的参考图修改后的npy单个原始数据数组】，可以在设置界面打开相关按钮——但是这个功能不符合程序设计理念——应该不修改原始数据的，只是在原始数据里叠了一层遮罩，有需要的根据遮罩提取数据即可。

 

* 预处理相关功能区

 

这个功能适用于需要进行数值判定去绘制遮罩的时候，比如某张雷达图，将反射率小于10的都判定为杂波，使用预处理明显比手动绘制效率高，实际上更推荐的流程是先对文件进行预处理，再进行手动纠正，效率高而且工作量也少得多。

 

预处理功能本质上是利用exec运行用户写的代码，只是预先将可能用到的二维数组都转化成了Dataframe形式，便于进行批量筛选、对比、计算甚至导出——是的，因为是运行实体python代码，所以你在预处理框写一个将当前处理的数据导出成excel的代码，这也可以被运行——我知道有巨大的安全隐患，但反正都是本地自己用不是？实际上自定义绘图函数也是通过exec直接运行用户的代码，只是涉及到标准化输出稍微麻烦了些，也正是因为exec，如果自定义绘图函数出错了，不会报错，而是直接整个程序假死。

 

预处理功能预先将所有在表1里标注的二维数组都定义成了名字叫表1里对应的键的变量——理解起来有点困难，大概意思就是假如在npz文件中我有一个Z1的键代表着雷达反射率，那么在预处理环境下，就有一个叫“雷达反射率”的df变量可以使用。不仅定义了当前文件的变量，还包括之前使用的5个文件的变量也会被加载进来，方便跨时间比对。

 

同时也定义了特殊变量——代表当前遮罩的“遮罩”变量，是一个DataFrame，修改它就可以直接修改遮罩，同理还有“缺失值数组”变量。还有缓存遮罩1~5，能够跨文件保存数据。还有三个特殊的函数——展示【可以将任何二维数组plt.show()出来】、载入、保存，后两个函数用来操作缓存遮罩的。预处理代码中的print可以以消息的形式显示在软件窗口内。

 

在预处理代码输入框稍微输入一点东西，然后点击右边的搜索按钮，可以看到更详细的使用说明和示例代码。

 

* 批量处理相关功能

 

就两个：批量导出图片和批量预处理。批量预处理提供了批量生成背景图的功能，具体可以将鼠标放在按钮上进行查看。批量预处理还可以根据不同的图批量生成“Musk_nan”标注区域遮罩层，使用代码为【缺失值数组 = np.array(自定义的条件)】然后点击批量预处理，开始即可。

 

因为我的Qt多线程实在写的太烂了，所以任何批量操作程序都会导致页面很卡，即使我假如了手动刷新，也很难在批处理的是偶进行操作。进行批处理的时候会命令行和软件弹窗上都会显示一个进度条，通过查看进度条知道程序执行的进度，如果软件弹窗上的进度条一直是未知而且没刷新，就说明批处理操作出错了。先将其终止，修正代码再重启。

 

因为是手动刷新，一般处理完一个文件才会刷新一次，单个文件处理比较久的话就显得很像卡死了……其实还是在跑的，可以去日志里看看进度。同理因为是手动刷新，点击暂停和终止的时候，也要等到处理完当前文件刷新页面之后才会处理这个请求——所以请不要多点，点一次然后等待就好了。

 

* 夜间模式

 

本软件还支持夜间模式，不仅软件本身进入暗黑模式，webview容器内的html文件也进行了适配。除此之外软件也支持自定义主题色，甚至修改软件图标！！！

 

###   注意

 

* 一些tips

 

本软件的按钮众多、再加上参考图，需要占据的面积比较大，宽度为1920像素的屏幕应该差不多比需求多一点点。程序打开的时候默认是90%当前屏幕的宽度高度，然后可以使用最大化将其全屏展示。如果屏幕实在是比较小。只能通过滑动条进行操作，操作手感会相对一般。

 

比较推荐的操作方式是记住对应功能的快捷键，然后向下滑动屏幕，到整个屏幕正好能放下绘图区、遮罩区和第一、第二张参考图，就可以全心全意进行枯燥无味的数据标注工作了。不然按钮要占据很大一部分屏幕，第一、第二张参考图只能显示一半。

 

参考图容器设定最大值为30行，也就是60个参考图，应该无论如何都够用了，实在不够用的话在源代码里改一下上限即可。

 

已经尽量让所有报错都以消息提醒的形式输出在窗口中，可以在设置界面打开“是否需要完整报错信息”来查看traceback的内容。本软件虽然将所有的功能都做到 UI 上了，但出于精力有限，不可能完全照顾所有可能性（说白了就是可能有隐藏bug，需要懂代码去源代码里调整）。

 

多线程写的很烂，仅有的多线程也不是用QTread写的，而是treading……但是依然解决不了阻塞问题。界面很卡的话其实后台也在跑，会有对应的输出信息。

 

大多数绘图区域bug可以通过删除配置文件后重启软件来解决。

"""












MainDrawingAreaContainer = """
<!DOCTYPE html>
<html>
<head>
    <title>绘制图像</title>
    <script src="https://cdn.bootcdn.net/ajax/libs/fabric.js/5.3.1/fabric.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pako/2.0.4/pako.min.js"></script>
    <script type="text/javascript" src="qrc:///qtwebchannel/qwebchannel.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <script>
    /**
     * 
     * 一个javascript填色小工具
     * 以h5的canvas为载体
     * 该代码由其作者applelee公开
     * 任何人或机构可以随意使用，但任何使用该代码产生的后果，作者不负任何责任
     * 
     * 版本2020-08-24
     * 
     * 后来者又浅浅改了以下大佬的源代码
     * 版本20224-07-17
    */
    
    (function (win, doc) {
        const w = win || window
        const d = doc || document
        
        // 可配置属性
        let options = {
            // 画布尺寸
            canvasSize: [600, 800],
            // 填充色
            fillColor: [100, 100, 100, 255],
            // 被填充色
            coverFillColor: [255, 255, 255, 255],
            // 禁止填充色
            boundaryColor: [0, 0, 0, 255],
            // 颜色匹配容差值 1-200
            tolerance: 100,
            // 遇到边界时候的跳跃像素，大片不密实的填色区域适用，默认为1，就是检测周围1像素的像素点内有没有符合条件的，有的话加入填充栈，注意太大的话会导致计算时间太长
            skipDistance: 1,
            // 是否禁止填充边界色
            isBanBoundaryColor: true,
            // 是否自动更新被填充色
            isAutoChangeCoverFillColor: true,
            // 不显示离屏画布，不能直接用点击触发事件，需要手动调用函数，然后返回对应的点击坐标
            offscreenCanvasVisible: true,
            // 是否使用fabric画布对象，fabric画布的操作逻辑和正常的canvas不大一样，需要特殊处理
            isFabricCanvas: false,
            // 传递fabric画布对象
            fabricCanvas: null,
        }
        
        // 开关
        let isTurnOn = false
        
        // 构造函数
        const FastFill = function (opt = {}) {
            options = {
            ...options,
            ...opt,
            };
        
            if (!options.elementId) error('指向主 canvas 的 options 的 elementId 不能为空！！')

            // 根据传入的 canvasId 获取主 Canvas 元素
            const mainCanvas = document.getElementById(options.elementId);
            const domRect = mainCanvas.getBoundingClientRect();

            // 创建离屏容器 div
            const offscreenContainer = document.createElement('div');
            offscreenContainer.id = 'offscreenCanvasContainer';
            offscreenContainer.style.position = 'absolute';
            offscreenContainer.style.width = `${domRect.width}px`;
            offscreenContainer.style.height = `${domRect.height}px`;
            offscreenContainer.style.left = `${domRect.left}px`;
            offscreenContainer.style.top = `${domRect.top}px`;
            document.body.appendChild(offscreenContainer);

            // 创建离屏 Canvas
            const offscreenCanvas = document.createElement('canvas');
            offscreenCanvas.setAttribute('willReadFrequently', 'true');
            offscreenCanvas.width = domRect.width;
            offscreenCanvas.height = domRect.height;
            offscreenCanvas.style.display = 'none';
            offscreenCanvas.id = 'offscreenCanvas';
            offscreenContainer.appendChild(offscreenCanvas);

            // 初始化 FastFill 实例
            //this.elementId = 'offscreenCanvasContainer'; // 使用离屏容器的 ID
            this.canvasSize = [domRect.width, domRect.height]; // 使用离屏 Canvas 的尺寸
            this.imageURL = options.imageURL; // 图片的 URL

            init(this); // 初始化 FastFill 实例
        }
        
        // 工厂函数
        FastFill.create = (opt = {}) => {
            return new FastFill(opt)
        }
        
        // 更改配置
        FastFill.prototype.reset = function (opt = {}) {
            this.imgData = null
            this.elementId = opt.elementId || this.elementId
            this.imageURL = opt.imageURL || this.imageURL
            this.canvasSize = opt.canvasSize || this.canvasSize
            this.fillColor = opt.fillColor || this.fillColor
            this.coverFillColor = opt.coverFillColor || this.coverFillColor
            this.boundaryColor = opt.boundaryColor || this.boundaryColor
            this.isBanBoundaryColor = opt.isBanBoundaryColor || this.isBanBoundaryColor
            this.offscreenCanvasVisible = opt.offscreenCanvasVisible || this.offscreenCanvasVisible
            this.isFabricCanvas = opt.isFabricCanvas || this.isFabricCanvas
            this.fabricCanvas = opt.fabricCanvas || this.fabricCanvas
            this.tolerance = opt.tolerance && (opt.tolerance > 200 ? 200 : opt.tolerance) || this.tolerance
            this.skipDistance = opt.skipDistance && (opt.skipDistance > 200 ? 200 : opt.skipDistance) || this.skipDistance
        
            if (opt.imageURL) {
            const [x, y] = this.canvasSize
            this.ctx.clearRect(0, 0, x, y)
            imageHandle('图片重新加载完毕', this)
            }
        }
        
        // 重置画布
        FastFill.prototype.resetCanvas = function () {
            imageHandle('图片重新加载完毕', this)
        }
        
        // 注册开始，如果不显示画布就不进行注册
        FastFill.prototype.turnOn = function (cb = () => {}) {
            if (this.isEvent) return
            if (this.offscreenCanvasVisible) {
            run(this)}
        }
        
        // 监听填色开始
        FastFill.prototype.startFill = function (cb = () => {}) {
            this.startFillCB = cb
        }
        
        // 关闭填色，注销事件，如果不显示画布就不进行注销
        FastFill.prototype.turnOff = function (cb = () => {}) {
            if (this.offscreenCanvasVisible) {
            this.cvs.removeEventListener('click', this.clickEventHandle)}
            this.isEvent = false
            cb()
        }
        
        // 资源加载完成
        FastFill.prototype.loaded = function (cb = () => {}) {
            this.loadedCB = res => cb(res)
        }
        
        // 填色结果
        FastFill.prototype.fillDone = function (success = () => {}, error = () => {}) {
            this.successCB = () => success()
            this.errorCB = err => error(err)
        }

        // 手动触发填色
        FastFill.prototype.manualFill = function (x, y) {
            console.log('手动触发填色')
            this.fillStack = [[x, y]];
            const bool = invalidFillDetecion([x, y], this);
            if (!bool) return;
            startFill(this);
            console.log('手动填色完成')
            ////console.log(this.filledPoints)
            return this.filledPoints
        }

        // FastFill 类方法定义
        FastFill.prototype.updateOffscreenCanvas = function() {
            // 如果isFabricCanvas为true，则不执行以下操作
            if (this.isFabricCanvas === true) {

                // 创建一个虚拟 Canvas，宽高设置为主 Canvas 的宽高
                var virtualCanvas = document.createElement('canvas');
                virtualCanvas.width = this.canvasSize[0];
                virtualCanvas.height = this.canvasSize[1];

                // 构建一个新的 fabric.Canvas 对象，绑定虚拟 Canvas
                var virtualFabricCanvas = new fabric.Canvas(virtualCanvas);

                // 克隆背景图
                let cloneBackgroundPromise = new Promise((resolve, reject) => {
                    if (this.fabricCanvas.backgroundImage) {
                        this.fabricCanvas.backgroundImage.clone(function(clonedBackground) {
                            virtualFabricCanvas.setBackgroundImage(clonedBackground, () => {
                                virtualFabricCanvas.renderAll();
                                resolve();
                            });
                        });
                    } else {
                        resolve(); // 如果没有背景图，直接解决Promise
                    }
                });

                // 克隆其他所有对象
                let cloneObjectsPromise = Promise.all(this.fabricCanvas.getObjects().map(object => {
                    return new Promise((resolve) => {
                        object.clone(function(cloned) {
                            virtualFabricCanvas.add(cloned);
                            resolve();
                        });
                    });
                }));

                // 等待所有克隆操作完成
                Promise.all([cloneBackgroundPromise, cloneObjectsPromise]).then(() => {
                    // 调整虚拟画布的缩放比例和位置
                    virtualFabricCanvas.setZoom(1);
                    virtualFabricCanvas.absolutePan(new fabric.Point(0, 0));

                    // 导出虚拟画布内容
                    var dataURL = virtualFabricCanvas.toDataURL({
                        format: 'png',
                        quality: 1 // 设置导出质量为最高
                    });

                    // 重置 FastFill 实例
                    this.reset({ imageURL: dataURL });
                });

                
            } else{
                // 清空离屏 canvas
                this.offscreenCtx.clearRect(0, 0, this.offscreenCanvas.width, this.offscreenCanvas.height);

                // 获取主 Canvas 元素
                const fabricCanvasEl = this.mainCanvas;
                const canvasWidth = fabricCanvasEl.width;
                const canvasHeight = fabricCanvasEl.height;

                // 将主 Canvas 上的内容绘制到离屏 canvas 上
                this.offscreenCtx.drawImage(fabricCanvasEl, 0, 0, canvasWidth, canvasHeight);

                // 生成离屏 canvas 的图像 URL
                const offscreenDataURL = this.offscreenCanvas.toDataURL();

                // 更新 FastFill 实例的 imageURL 属性
                this.reset({ imageURL: offscreenDataURL });
            }
        }

        FastFill.prototype.close = function() {
            // 尝试获取离屏容器
            const offscreenContainer = document.getElementById('offscreenCanvasContainer');
            console.log('关闭函数被调用', offscreenContainer);
            // 如果容器存在，则移除
            if (offscreenContainer) {
                offscreenContainer.remove();
            } else {
                console.log('未找到离屏div元素，应该已经比删除');
            }
        }


        
        const init = self => {
            // 填充类型
            const type = 0
            // 是否绑定点击事件
            self.isEvent = false
            // 绘制数据
            self.imgData = null
            // 已经检测集合
            self.solvedSet = new Set()
            // 未检测集合
            self.stackedSet = new Set()
            // 可以填充的栈
            self.fillStack = []
            // 图片在画布中的位置与实际尺寸
            self.imgStartX = 0
            self.imgStartY = 0
            self.imgDisplayWidth = 0
            self.imgDisplayHeight = 0

            self.mainCanvas = d.getElementById(options.elementId)
            self.offscreenCanvas = d.getElementById('offscreenCanvas')
            self.offscreenContainer = d.getElementById('offscreenCanvasContainer')
            self.offscreenCtx = self.offscreenCanvas.getContext('2d', { willReadFrequently: true })
        
            // 检测方向枚举
            self.directions = [[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]]
            // 画布
            self.cvs = d.createElement('canvas');
            ////console.log(self.cvs);
            // canvas上下文
            self.ctx = self.cvs.getContext('2d', { willReadFrequently: true }); // 设置 willReadFrequently 为 true
            // 递归计数器
            self.count = 0
            // 最大计数值(防止内存溢出)
            self.maxCount = 2000
        
            // 点击事件回调
            self.clickEventHandle = () => {}
            // 开始填充回调
            self.startFillCB = () => {}
            // 资源加载回调
            self.loadedCB = () => {}
            // 填充完成回调
            self.successCB = () => {}
            // 填充异常回调
            self.errorCB = () => {}
        
            self.elementId = options.elementId
            self.imageURL = options.imageURL
            self.canvasSize = options.canvasSize
            self.fillColor = options.fillColor
            self.coverFillColor = options.coverFillColor
            self.boundaryColor = options.boundaryColor
            self.isBanBoundaryColor = options.isBanBoundaryColor
            self.isAutoChangeCoverFillColor = options.isAutoChangeCoverFillColor
            self.offscreenCanvasVisible = options.offscreenCanvasVisible
            self.isFabricCanvas = options.isFabricCanvas
            self.fabricCanvas = options.fabricCanvas
            self.tolerance = options.tolerance > 200 ? 200 : options.tolerance
            self.skipDistance = options.skipDistance > 200 ? 200 : options.skipDistance

            if (!self.offscreenCanvasVisible) {
                console.log('不显示离屏画布')
                self.offscreenContainer.style.display = 'none';
                self.cvs.style.display = 'none';
            }
        
            createScreen(self)
            ////imageHandle(self)
            self.updateOffscreenCanvas();
            ////console.log(self.imageURL)
            ////imageHandle('图片重新加载完毕', self);
            
        }
        
        const createScreen = self => {
            const [width, height] = self.canvasSize
            
            if (!self.offscreenContainer) error('画布容器不存在！！')
        
            self.cvs.width = width
            self.cvs.height = height
            self.offscreenContainer.append(self.cvs)
            }
        // 图片加载
        const imageHandle = function () {
            console.log("图片加载函数被调用")
            const len = arguments.length
            const msg = typeof arguments[0] !== 'string' ? '' : arguments[0]
            const self = arguments[len - 1]
            const image = new Image()
            // 设置跨域属性
            image.crossOrigin = 'anonymous'
    
            image.src = self.imageURL
    
            image.onerror = function (e) {
                error('图片加载异常', e.type)
            }
    
            // 定义图片加载成功时的回调函数
            image.onload = function (e) {
                // 从self对象中获取画布的宽度和高度
                const [width, height] = self.canvasSize
                // 打印日志信息，表示图片已经加载完毕
                console.log('图片加载完毕')
                // 从事件对象的path属性中获取图片的实际宽度和高度
                // 注意：这里的e.path可能在某些浏览器中不可用，建议使用this.width和this.height作为替代
                const imgWidth = this.width
                const imgHeight = this.height
                console.log('图片的实际宽度和高度分别为', imgWidth, imgHeight)
    
                // 将画布的宽高设置为图片的宽高
                self.ctx.canvas.width = imgWidth
                self.ctx.canvas.height = imgHeight
    
                // 计算画布的宽高比
                const cvsProportion = width / height
                // 计算图片的宽高比
                const imgProportion = imgWidth / imgHeight

                console.log('画布的宽高比为', cvsProportion)
                console.log('图片的宽高比为', imgProportion)
    
                // 根据宽高比调整图片的显示宽度和高度，以适应画布大小
                self.imgDisplayWidth = cvsProportion >= imgProportion ? imgWidth * height / imgHeight : width
                self.imgDisplayHeight = cvsProportion >= imgProportion ? height : width * imgHeight / imgWidth
                // 计算图片在画布上的起始x坐标
                self.imgStartX = cvsProportion >= imgProportion ? (width / 2) - (self.imgDisplayWidth / 2) : 0
                // 计算图片在画布上的起始y坐标
                self.imgStartY = cvsProportion >= imgProportion ? 0 : (height / 2) - (self.imgDisplayHeight / 2)
                console.log('图片在画布上的起始坐标分别为', self.imgStartX, self.imgStartY)
                console.log('图片在画布上的显示宽度和高度分别为', self.imgDisplayWidth, self.imgDisplayHeight)

                
                // 在画布上绘制图片
                self.ctx.drawImage(this, 0, 0, imgWidth, imgHeight, self.imgStartX, self.imgStartY, self.imgDisplayWidth, self.imgDisplayHeight)
    
                // 调用加载完成后的回调函数，传入消息对象
                self.loadedCB({ msg })
            }
            // console.log("图片链接为：",self.imageURL);
        }

        
        const run = self => {
        console.log('开始注册点击事件')
            self.isEvent = true
            self.clickEventHandle = clickEventHandle.bind(self)
            self.cvs.addEventListener('click', self.clickEventHandle)
        }
        
        // 点击事件处理
        function clickEventHandle (e) {
            console.log('点击事件触发')
            // 填充起点矢量
            const [x, y] = getEventPosition(e)
        
            // 填充起点入栈
            this.fillStack = [[x, y]]
        
            const bool = invalidFillDetecion([x, y], this)
            if (!bool) return
            startFill(this)
        }



        // 无效填充检测函数定义
        // 参数：坐标点 [x, y] 和 self 对象（通常指向当前的工作对象）
        const invalidFillDetecion = ([x, y], self) => {
            // 使用 canvas 的 getImageData 方法获取指定坐标点的像素颜色数据
            const colorData = self.ctx.getImageData(x, y, 1, 1).data;
            console.log(`坐标 (${x}, ${y}) 的颜色数据为 ${colorData}`);
    
            // 如果设置了自动更改覆盖填充颜色的标志，则更新 coverFillColor 属性为当前点的颜色
            if (self.isAutoChangeCoverFillColor) {
                self.coverFillColor = colorData;
            }
    
            // 检查坐标点是否在有效的图片显示区域内
            // 如果点的坐标超出了图片的开始坐标加上其显示宽度或高度，则认为是无效填充区域
            if (x < self.imgStartX || y < self.imgStartY || x >= self.imgStartX + self.imgDisplayWidth || y >= self.imgStartY + self.imgDisplayHeight) {
                console.error(`坐标 (${x}, ${y}) 超出有效填充区域。有效区域为 x: [${self.imgStartX}, ${self.imgStartX + self.imgDisplayWidth})，y: [${self.imgStartY}, ${self.imgStartY + self.imgDisplayHeight})`);
                // 调用错误回调函数，传递错误信息
                self.errorCB({
                    msg: '无效填充区域',
                });
                return false; // 返回 false 表示检测到无效填充
            }
    
            // 如果设置了禁止填充边界颜色，并且当前点的颜色与边界颜色相同，则认为是禁止填充的颜色
            if (self.isBanBoundaryColor && isSameColor(colorData, self.boundaryColor)) {
                console.error(`坐标 (${x}, ${y}) 的颜色与禁止填充的边界颜色相同。`);
                // 调用错误回调函数，传递错误信息
                self.errorCB({
                    msg: '选中颜色为禁止填充色',
                });
                return false; // 返回 false 表示检测到禁止填充的颜色
            }
    
            // 如果当前点的颜色不是预期的被填充颜色，则认为是错误的填充颜色
            if (!isSameColor(colorData, self.coverFillColor)) {
                console.error(`坐标 (${x}, ${y}) 的颜色不是预期的被填充颜色。预期颜色为 ${self.coverFillColor}，实际颜色为 ${colorData}`);
                // 调用错误回调函数，传递错误信息
                self.errorCB({
                    msg: '选中颜色不是被填充的颜色',
                });
                return false; // 返回 false 表示检测到错误的填充颜色
            }
    
            // 如果所有检查都通过，则返回 true 表示填充检测有效
            return true;
        }
        
        // 开始
        const startFill = (self) => { // 设置默认色彩容差为 200，默认跳跃距离为 5（在方向检测是否入栈函数里使用的条约距离，完全不跳跃的话，遇到密集均匀离散的点，填色效果很差）
        self.filledPoints = []; // 初始化存储填色点坐标的列表
        self.startFillCB(); // 调用开始填充的回调函数
        let counter = 0; // 初始化计数器
        while (self.fillStack.length > 0 && counter < 1000) { // 循环，直到填充栈为空，或者计数器达到 1000 个循环，避免无限循环
            if (counter % 10 === 0) { // 每循环十次才执行一次 console.log
                console.log('开始循环第', counter + 1, '次');
            }
            drippingRecursion(self); // 调用递归填色函数
            counter++; // 每次循环后递增计数器
        }
        console.log(`循环执行了 ${counter} 次。`);

        ////console.log(self.stackedSet);
        endFill(self); // 调用结束填充的函数
        }

        // 核心逻辑
        const drippingRecursion = (self) => {
        const [x, y] = self.fillStack.shift(); // 从填色栈中取出一个坐标点

        // 入栈与出栈
        self.solvedSet.add(`${x};${y}`); // 将当前点标记为已解决
        self.stackedSet.delete(`${x};${y}`); // 从待处理集合中删除当前点

        // 填色
        fill([x, y], self); // 调用填色函数

        // 方向检测
        directionDetection([x, y], self); // 调用方向检测函数，检测周围点是否需要填色
        }

        // 填色
        const fill = ([x, y], self) => {
        const [r, g, b, a] = self.fillColor; // 获取填色的 RGBA 值

        // 在填色前将坐标添加到列表中
        self.filledPoints.push({ x: x, y: y }); // 将坐标对象加入列表

        if (self.offscreenCanvasVisible) {
        if (!self.imgData) {
            self.ctx.rect(x, y, 1, 1); // 绘制一个 1x1 的矩形
            self.ctx.fillStyle = `rgba(${r}, ${g}, ${b}, ${a})`; // 设置填色
            self.ctx.fill(); // 执行填色
            self.imgData = self.ctx.getImageData(x, y, 1, 1); // 获取该点的图像数据
        } else {
            self.ctx.putImageData(self.imgData, x, y); // 将图像数据放回到该点
        }
        }
        }

        // 方向检测
        const directionDetection = ([x, y], self) => {
        self.directions.forEach(([dirX, dirY]) => { // 遍历所有方向
            let foundValidPoint = false;
            for (let i = 1; i <= self.skipDistance; i++) {
            const dirCoord = [x + dirX * i, y + dirY * i]; // 计算当前点在该方向上的新坐标
            if (pushTesting(dirCoord, self)) { // 如果新坐标通过检测
                self.fillStack.push(dirCoord); // 将新坐标入栈

                if (!self.solvedSet.has(`${dirCoord[0]};${dirCoord[1]}`)) { // 如果新坐标不在已解决集合中
                self.stackedSet.add(`${dirCoord[0]};${dirCoord[1]}`); // 将新坐标添加到待处理集合中
                }
                foundValidPoint = true;
                break; // 找到一个有效点后跳出循环
            }
            }
            if (!foundValidPoint) { // 如果在 skipDistance 范围内没有找到有效点
            const dirCoord = [x + dirX * self.skipDistance, y + dirY * self.skipDistance];
            if (pushTesting(dirCoord, self)) {
                self.fillStack.push(dirCoord);
                if (!self.solvedSet.has(`${dirCoord[0]};${dirCoord[1]}`)) {
                self.stackedSet.add(`${dirCoord[0]};${dirCoord[1]}`);
                }
            }
            }
        });

        if (self.fillStack.length > 0) { // 如果填色栈不为空
            if (self.count >= self.maxCount) { // 如果递归深度达到最大值
            self.count = 0; // 重置递归计数
            return;
            }

            self.count += 1; // 递增递归计数

            try {
            drippingRecursion(self); // 递归调用自身
            } catch (e) {
            self.count = 0; // 捕获异常并重置递归计数
            return;
            }
        }
        }

        // 入栈检测
        const pushTesting = ([x, y], self) => {
        const data = self.ctx.getImageData(x, y, 1, 1).data; // 获取指定点的图像数据

        // 已经填充
        if (self.solvedSet.has(`${x};${y}`)) {
            return false;
        }

        // 已经入栈
        if (self.stackedSet.has(`${x};${y}`)) {
            return false;
        }

        // 色彩偏移检测
        if ((self.coverFillColor[0] - data[0] < -self.tolerance || self.coverFillColor[0] - data[0] > self.tolerance)
            || (self.coverFillColor[1] - data[1] < -self.tolerance || self.coverFillColor[1] - data[1] > self.tolerance)
            || (self.coverFillColor[2] - data[2] < -self.tolerance || self.coverFillColor[2] - data[2] > self.tolerance)
            || (self.coverFillColor[3] - data[3] < -self.tolerance || self.coverFillColor[3] - data[3] > self.tolerance)) {
            return false;
        }

        // 纯白色和纯黑色检测，遇到这两种颜色直接当作边界颜色
        if ((data[0] === 255 && data[1] === 255 && data[2] === 255 && data[3] === 255) // 纯白色
            || (data[0] === 0 && data[1] === 0 && data[2] === 0 && data[3] === 255)) { // 纯黑色
            return false;
        }

        return true; // 如果通过所有检测，返回 true
        }


        
        const endFill = self => {
            self.count = 0
            self.solvedSet.clear()
            self.stackedSet.clear()
            self.fillStack = []
            self.successCB()
        }
        
        // 抛出错误
        const error = msg => {
            throw msg
        }
        
        // 获取填充起点
        const getEventPosition = e => {
            let x, y;
        
            if (e.layerX || e.layerX === 0) {
            console.log("使用了 layerX 和 layerY 属性")
            x = e.layerX
            y = e.layerY
            } else if (e.offsetX || e.offsetX === 0) { // Opera
            console.log("使用了 offsetX 和 offsetY 属性")
            x = e.offsetX
            y = e.offsetY
            }
        
            return [x, y]
        }

        // function getEventPosition(e) {
        //     const canvas = document.getElementById(this.elementId); // 假设 this.elementId 是画布元素的 ID
        //     const rect = canvas.getBoundingClientRect(); // 获取画布元素的边界矩形
        //     const x = e.clientX - rect.left; // 计算相对于画布的 X 坐标
        //     const y = e.clientY - rect.top; // 计算相对于画布的 Y 坐标
        //     return [x, y];
        // }
        
        // 是否是等色
        const isSameColor = (s, b) => {
            if (s[0] === b[0] && s[1] === b[1] && s[2] === b[2] && s[3] === b[3]) {
            return true
            }
            return false
        }


        
        w.FastFill = FastFill
        })(window, document)
        
    </script>
    <script type="text/javascript">
        var maskArray_color = Array(500).fill(Array(500).fill("#000000")); // 定义一个500*500的数组，每个元素都是"#000000"
        var maskArray_nan = Array(500).fill(Array(500).fill("#ffffff")); // 定义一个500*500的数组，每个元素都是"nan"
        
        // 全局变量，用于存储背景图像素数据
        var pixelDataArray = [];

        // 这个函数的作用是每次改动maskArray_color的时候，都要保证maskArray_nan中对应的位置也是"#000000"（缺失值始终是缺失值）
        function updateColorArray() {
            for (let i = 0; i < maskArray_nan.length; i++) {
                for (let j = 0; j < maskArray_nan[i].length; j++) {
                    if (maskArray_nan[i][j] === '#000000') {
                        maskArray_color[i][j] = '#000000';
                    }
                }
            }
        }
                
        // 这个函数用于向python发送列表，这是用来发送鼠标位置的
        function sendListToPython(listdata) {
            if (window.bridge) {
                var jsList = listdata;
                window.bridge.receiveListFromJS(jsList);
            } else {
                console.log("桥接对象未初始化");
            }
        }

        // 这个函数用于向python发送画布位置
        function sendCanvasPositionToPython(listdata) {
            if (window.bridge) {
                window.bridge.receivePositionFromJs(listdata);
            } else {
                console.log("桥接对象未初始化");
            }
        }

        // 发送遮罩数组给Python
        function sendMuskArrayToPython() {
            console.log("发送maskArray_color到Python");

            if (window.bridge) {
                try {
                    let startTime, endTime;

                    // 将数组转换为JSON字符串
                    console.log("开始将数组转换为JSON字符串");
                    startTime = performance.now();
                    var jsonString = JSON.stringify(maskArray_color);
                    endTime = performance.now();
                    console.log(`JSON字符串转换完成，长度: ${jsonString.length}，耗时: ${endTime - startTime}ms`);

                    // 压缩JSON字符串
                    console.log("开始压缩JSON字符串");
                    startTime = performance.now();
                    var compressedData = pako.gzip(jsonString);
                    endTime = performance.now();
                    console.log(`压缩完成，压缩后数据长度: ${compressedData.length}，耗时: ${endTime - startTime}ms`);

                    // 将压缩数据转换为Base64字符串
                    console.log("开始将压缩数据转换为Base64字符串");
                    startTime = performance.now();
                    var binary = '';
                    var bytes = new Uint8Array(compressedData);
                    var len = bytes.byteLength;
                    for (var i = 0; i < len; i++) {
                        binary += String.fromCharCode(bytes[i]);
                    }
                    var base64Data = btoa(binary);
                    endTime = performance.now();
                    console.log(`Base64字符串转换完成，长度: ${base64Data.length}，耗时: ${endTime - startTime}ms`);

                    // 发送数据到Python
                    console.log("开始发送数据到Python");
                    startTime = performance.now();
                    window.bridge.receiveMuskArrayFromJS(base64Data)
                        .then(() => {
                            endTime = performance.now();
                            console.log(`数据已成功发送到Python，耗时: ${endTime - startTime}ms`);
                        })
                        .catch(err => console.error("发送数据到Python时出错:", err));
                } catch (error) {
                    console.error("处理数据时发生错误:", error);
                }
            } else {
                console.log("桥接对象未初始化");
            }
        }



        

        document.addEventListener("DOMContentLoaded", function() {
            // 创建 QWebChannel 实例
            new QWebChannel(qt.webChannelTransport, function(channel) {
                // 将 QWebChannel 的 bridge 对象保存为全局变量
                window.bridge = channel.objects.bridge;

                // 处理分块数据接收
                var receivedChunks = [];
                var totalChunks = 0;
                var expectedChunks = 0;

                window.bridge.sendChunkToJS.connect(function(chunk, index, total) {
                    console.log("接收到从python发来的数据块，块索引为:", index, "总块数为:", total);
                    if (expectedChunks === 0) {
                        expectedChunks = total;
                    }
                    // console.log("数据块内容:", chunk);
                    console.log("数据块类型:", typeof chunk);
                    console.log("数据块大小 (字符数):", chunk.length);

                    receivedChunks[index] = chunk;
                    totalChunks++;

                    if (totalChunks === expectedChunks) {
                        console.log("接收到从python发来的所有数据块，数据块总数为:", totalChunks);
                        // console.log("所有数据块内容:", receivedChunks);

                        var combinedChunks = receivedChunks.join('');
                        var decodedData = atob(combinedChunks);  // 解码base64字符串
                        var byteArray = new Uint8Array(decodedData.length);
                        for (var i = 0; i < decodedData.length; i++) {
                            byteArray[i] = decodedData.charCodeAt(i);
                        }
                        // console.log("合并后的压缩数据:", byteArray);
                        
                        try {
                            var decompressedData = pako.ungzip(byteArray, { to: 'string' });
                            if (!decompressedData) {
                                console.error("解压缩数据失败或结果为空");
                                return;
                            }
                            // console.log("解压缩后的数据:", decompressedData);
                            var data = JSON.parse(decompressedData);
                            // console.log("解析后的数据:", data);

                            if (Array.isArray(data[0])) {
                                console.log("接收到从python发来的数组，数组元素数量为:", data.length);
                                console.log("两个子数组的形状分别是:", data[0].length, data[0][0].length, data[1].length, data[1][0].length);
                                maskArray_color = data[0];
                                maskArray_nan = data[1];
                                console.log("更新maskArray_color和maskArray_nan成功");
                            }
                        } catch (error) {
                            console.error("处理接收数据时发生错误:", error);
                        }
                    }
                });

                // 处理背景图像接收
                window.bridge.sendBase64ToJS.connect(function(base64Data) {
                    console.log("接收到python发来的背景图像");
                    console.log("背景图像数据长度:", base64Data.length);
                    handleBase64Image(base64Data);
                });
            });
        });


        // 下面是处理极坐标用到的函数
        // 下面是处理极坐标用到的函数
        // 将直角坐标 (x, y) 转换为极坐标 (r, theta)
        function rectToPolar(item) {
            const r = Math.sqrt(item.x ** 2 + item.y ** 2); // 计算半径 r
            let theta = Math.atan2(item.y, item.x) * (180 / Math.PI); // 计算角度 theta，并将其转换为度数
            if (theta < 0) {
                theta += 360; // 确保角度在 0 到 360 度之间
            }
            return {r:r, theta:theta};
        }

        // 判定一个点可能对应的所有极坐标
        function pixelToPolar(item_o, a = 360) {
            const item = rectToPolar(item_o); // 将直角坐标转换为极坐标
            const b = item.r * Math.sin(Math.PI / a); // 计算 b 值
            
            // 初始化列表，包含原始极坐标，要转化成数组坐标，而不是完整的极坐标
            const possiblePolarCoords = [{r:Math.round(item.r), theta:Math.round(item.theta*a/360)}];
            
            let i = 1;
            while (b < (1 / (2 ** i))) { // 例如 b < 0.5, b < 0.25, b < 0.125, ...
                possiblePolarCoords.push({r:Math.round(item.r), theta:Math.round((item.theta + i)*a/360 % 360)});
                possiblePolarCoords.push({r:Math.round(item.r), theta:Math.round((item.theta - i)*a/360 % 360)});
                i += 1;
            }
            
            // 去除重复的极坐标
            const uniquePolarCoords = Array.from(new Set(possiblePolarCoords.map(JSON.stringify))).map(JSON.parse);
            return uniquePolarCoords;
        }


        // 将极坐标 (r, theta) 转换为直角坐标 (x, y)
        function polarToRect(item) {
            const thetaRad = item.theta * (Math.PI / 180); // 将角度从度数转换为弧度
            const x = item.r * Math.cos(thetaRad);
            const y = item.r * Math.sin(thetaRad);
            return {x:x, y:y};
        }

        // 将极坐标转换为像素坐标
        function polarToPixels(item1, a = 360) {
            const thetaRad = item1.theta * (Math.PI / 180); // 将角度从度数转换为弧度
            const item2 = polarToRect(item1); // 将极坐标转换为直角坐标
            const b = item1.r * Math.sin(Math.PI / a); // 计算弦长b值

            // 如果 b 值较小，则获取相邻点
            if (b < 0.3) { // 例如，b < 0.5, b < 0.25, b < 0.125, ...
                return [[Math.round(item2.x), Math.round(item2.y)]];
            } else if (b < 1.2) {
                const minPoints = getAdjacentPoints(item2, item1, 3);
                return [{x: Math.round(item2.x), y: Math.round(item2.y)}, ...minPoints];
            }
            
            const xMin = Math.round(item2.x - b);
            const xMax = Math.round(item2.x + b);
            const yMin = Math.round(item2.y - b);
            const yMax = Math.round(item2.y + b);
            
            const pixels = []; // 用于存储满足条件的像素点
            
            // 遍历 (xMin, xMax) 和 (yMin, yMax) 范围内的所有点
            for (let x = xMin; x <= xMax; x++) {
                for (let y = yMin; y <= yMax; y++) {
                    const {r:r1, theta:theta1} = rectToPolar({x:x, y:y}); // 将直角坐标转换为极坐标
                    if (Math.abs(r1 - item1.r) <= 1) {
                        if (Math.abs(theta1 - item1.theta) <= 360/a/2) {
                            pixels.push({x:x, y:y}); // 满足条件的像素点加入列表
                        }
                    }
                }
            }
            
            // 去除重复的像素点
            return Array.from(new Set(pixels.map(JSON.stringify)), JSON.parse);
        }

        // 计算和一个点最接近的相邻点
        function getAdjacentPoints(item2, item1, num = 1) {
            const differences = [];
            // 遍历周围的八个点
            for (let dx = -1; dx <= 1; dx++) {
                for (let dy = -1; dy <= 1; dy++) {
                    if (dx === 0 && dy === 0) continue; // 跳过中心点本身
                    const x = Math.round(item2.x) + dx;
                    const y = Math.round(item2.y) + dy;
                    const item3 = rectToPolar({x: x, y: y}); // 计算极坐标
                    const diff = Math.abs(item1.r - item3.r) + Math.abs(item1.theta - item3.theta); // 计算差异
                    differences.push([{x: x, y: y}, diff]); // 添加到列表
                }
            }
            
            differences.sort((a, b) => a[1] - b[1]); // 根据差异排序
            return differences.slice(0, num).map(item => item[0]); // 返回差异最小的点的对象
        }

        // ——————————将极坐标数据映射到画布数组
        function polarArrayToCanvasArray(polarArray) {
            const canvasSize = picwidth; // 画布大小
            const canvas1 = Array.from({ length: canvasSize }, () => Array(canvasSize).fill("#000000")); // 创建一个空白二维数组（默认黑色）
            const dimension = polarArray.length; // 获取极坐标数组的维度

            for (let theta = 0; theta < polarArray.length; theta++) {
                for (let r = 0; r < polarArray[theta].length; r++) {
                    theta_use = theta*360/dimension;
                    let pointlistFinal = [];
                    const pointlist = polarToPixels({ r: r, theta: theta_use }, dimension); // 使用极坐标映射到像素坐标计算笛卡尔坐标

                    for (const { x: x, y: y } of pointlist) {
                        const xCanvas = Math.round(x + canvasSize / 2);
                        const yCanvas = Math.round(y + canvasSize / 2);
                        pointlistFinal.push([xCanvas, yCanvas]);
                    }

                    for (const [xCanvas, yCanvas] of pointlistFinal) {
                        if (0 <= xCanvas && xCanvas < canvasSize && 0 <= yCanvas && yCanvas < canvasSize) { // 确保坐标在画布范围内
                            const hexColor = polarArray[theta][r];
                            if (/^#[0-9A-F]{6}$/i.test(hexColor)) { // 检查是否为有效的十六进制颜色代码
                                canvas1[xCanvas][yCanvas] = hexColor; // 在画布上标记点
                            }
                        }
                    }
                }
            }
            return canvas1;
        }


        // ————————————将零散画布位置列表转换为极坐标
        function scatterCanvasToPolar(canvasList, canvasSize = 1000 ,a = 360) {
            const polarCoords = [];

            for (const point of canvasList) {
                const x = point.x - canvasSize / 2;
                const y = point.y - canvasSize / 2;
                const pointlist = pixelToPolar({x:x, y:y},a);
                polarCoords.push(...pointlist);
            }

            return Array.from(new Set(polarCoords.map(JSON.stringify)), JSON.parse);
        }

        // ————————————零散极坐标位置到画布
        function scatterPolarToCanvas(polarCoords, canvasSize = 1000 , a = 360) {
            const canvasCoords = [];

            for (const item of polarCoords) {
                const pointlist = polarToPixels({theta:item.theta/a*360, r:item.r},a);
                const adjustedPointlist = pointlist.map(({x, y}) => ({x: x + canvasSize / 2, y: y + canvasSize / 2}));
                canvasCoords.push(...adjustedPointlist);
            }


            return Array.from(new Set(canvasCoords.map(JSON.stringify)), JSON.parse);
        }






    </script>
    <style>
        body, html {
            max-width: 100%;
            max-height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
            padding: 0;
        }
        #brush-tools {
            position: fixed;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            z-index: 999;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 5px;
            padding: 5px;
            background-color: #f8f8f8;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 15px;
        }
        .tool-row {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 5px;
            width: calc(100% + 10px);
        }
        #brush-tools button {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 33px;
            height: 33px;
            border: none;
            border-radius: 50%;
            background-color: #fff;
            cursor: pointer;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s, transform 0.3s;
        }
        #brush-tools button:hover {
            background-color: #e0e0e0;
            transform: scale(1.1);
        }
        #brush-tools button:active {
            transform: scale(0.9);
            background-color: #d0d0d0;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
        }
        #brush-tools button i {
            font-size: 15px;
            color: #333;
        }
        #controls {
            border: 0px solid #000;
        }
        #canvas-container {
            display: flex;
            justify-content: center;
            width: 100%;
        }
        .color-button {
            display: inline-block;
            width: 15px;
            height: 15px;
            margin: 3px;
            border-radius: 50%;
            border: 1px solid #000;
            cursor: pointer;
        }
        .center-align label {
            font-size: 14px; /* 设置标签字体大小 */
            font-family: "YouYuan"
        }
        .label-slide{
            margin-top: 3px;
        }
        .center-align {
            display: flex;
            align-items: center;
            margin-left: 5px;
            margin-right: 5px;
            gap: 3px;
        }
        input[type="range"] {
            width: 70px;
            height: 10px;
            -webkit-appearance: none;
            appearance: none;
            background-color: #ccc;
            border-radius: 5px;
            outline: none;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        input[type="range"]:hover {
            background-color: #cb8181;
        }
        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background-color: #666;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        input[type="range"]::-webkit-slider-thumb:hover {
            background-color: #3870b9;
        }
        input[type="range"]:active::-webkit-slider-thumb {
            background-color: #1d6541;
        }
        /* 工具提示框样式 */
        [data-title]:hover {
            position: relative;
        }

        [data-title]:after {
            content: attr(data-title);
            position: absolute;
            top: 35px; /* 将此值增加以将提示显示得更下面 */
            left: 10px;
            color: #666;
            font-size: 12px;
            border: 1px solid #ffffff;
            background-color: #fff;
            z-index: 20;
            line-height: 1.5;
            font-style: normal; 
            white-space: nowrap;
            padding: 0 5px;
            border-radius: 4px; /* 添加圆角 */
            box-shadow: 0 4px 8px rgba(0,0,0,0.2); /* 添加阴影 */
            opacity: 0; /* 初始透明度 */
            transition: opacity 0.5s ease; /* 过渡持续时间 */
            transition-delay: 0s; /* 移除延迟 */
        }

        [data-title]:hover:after {
            opacity: 1; /* 悬停时的透明度 */
            transition-delay: 1s; /* 悬停时的延迟，一成功显示立刻修改，让它能够立刻延迟出现动画，鼠标一移开，延迟效果消失，控件立刻开始动画消失，天知道我改了多久 */
        }


        /* Night mode styles */
        body.night-mode, html.night-mode {
            background-color: #000000;
            color: #e0e0e0;
        }
        #brush-tools.night-mode {
            background-color: #333;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
        }
        #brush-tools.night-mode button {
            background-color: #444;
        }
        #brush-tools.night-mode button:hover {
            background-color: #555;
        }
        #brush-tools.night-mode button:active {
            background-color: #666;
        }
        #brush-tools.night-mode button i {
            color: #e0e0e0;
        }
        .color-button.night-mode {
            border: 1px solid #e0e0e0;
        }
        .center-align.night-mode label {
            color: #e0e0e0;
        }
        input[type="range"].night-mode {
            background-color: #666;
        }
        input[type="range"].night-mode:hover {
            background-color: #888;
        }
        input[type="range"].night-mode::-webkit-slider-thumb {
            background-color: #ccc;
        }
        input[type="range"].night-mode::-webkit-slider-thumb:hover {
            background-color: #fff;
        }

        /* 夜间模式下的工具栏浮现样式 */
        .night-mode [data-title]:after {
            color: #e0e0e0;
            background-color: #333;
            border: 1px solid #444;
            box-shadow: 0 4px 8px rgba(0,0,0,0.5);
        }
    </style>
</head>
<body>
    <div id="controls">
        <div id="brush-tools">
            <div class="tool-row">
                <button id="toggle-night-mode" data-title="切换夜间模式" style="display: none;"><i class="fas fa-moon"></i></button>
                <button id="draw-polygon" data-title="绘制多边形，左键绘制，右键结束绘制"><i class="fas fa-draw-polygon"></i></button>
                <button id="draw-rectangle" data-title="绘制矩形，左键绘制，右键结束绘制"><i class="fa-regular fa-square"></i></button>
                <button id="draw-circle" data-title="绘制圆形，左键绘制，右键结束绘制"><i class="fa-regular fa-circle"></i></button>
                <button id="draw-filltool" data-title="填色工具，单击左键填色，等待完成，区域大或者跳跃像素开大会等很久，正常现象。"><i class="fas fa-fill-drip"></i></button>
                <button id="draw-brush" data-title="直接进行绘制"><i class="fas fa-paint-brush"></i></button>
                <div class="center-align">
                    <label for="brush-color">自定颜色&nbsp;</label>
                    <input type="color" id="brush-color" value="#ff0000" data-title="设置自定义颜色，但是非预定义颜色存入遮罩的时候会统一数值">
                </div>
                画笔种类颜色替换位置
            </div>
            <div class="tool-row">
                <div class="center-align">
                    <label for="brush-size" data-title="调整画笔绘制宽度，数值为半径" class="label-slide">画笔宽度：</label>
                    <input type="range" id="brush-size" min="1" max="200" value="100">
                </div>
                <div class="center-align">
                    <label for="fill-tolerance" data-title="调整填色工具检测颜色的容差" class="label-slide">填色容差：</label>
                    <input type="range" id="fill-tolerance" min="1" max="200" value="100">
                </div>
                <div class="center-align">
                    <label for="skip-pixels" data-title="调整填色工具遇到边界时跳跃几个像素进行检测" class="label-slide">跳跃像素：</label>
                    <input type="range" id="skip-pixels" min="1" max="20" value="1">
                </div>
            </div>
        </div>
        <div id="canvas-container">
            <canvas id="c"></canvas>
        </div>
    </div>
    <script>
        // 初始化设置 //
        var canvasElement = document.getElementById('canvas-container');
        var brushToolsHeight = document.getElementById('brush-tools').offsetHeight;
        canvasElement.style.position = 'relative';
        canvasElement.style.top = brushToolsHeight + 'px';

        var picwidth = 500;
        var picheight = 500;

        // 初始化fabric画布
        var canvas = new fabric.Canvas('c', {
            imageSmoothingEnabled: false // 将像素点平滑关掉
            });
        canvas.isDrawingMode = true; // 启用绘制模式
        canvas.freeDrawingBrush.color = "#000000"; // 默认画笔颜色设置为黑色
        var isDrawing = false;
        var lastPoint = null;
        var pixelSize = 1; // 定义每个像素点的大小
        const canvasWidth = canvas.width;
        const canvasHeight = canvas.height;
        const centerX = canvasWidth / 2;
        const centerY = canvasHeight / 2;
        var coordinateFlag = "rect"; // 定义全局标志位，默认为"rect"
        var Nightmode = false; // 默认不是夜间模式
        

        // 按照画布上的点和缩放参数移动画布的函数
        function adjustCanvas(zoom, canvasCenterX, canvasCenterY) {

            // 设置画布的缩放级别
            canvas.setZoom(1);

            canvas.absolutePan(new fabric.Point(0, 0));

            //实际偏移的位置
            const viewportWidth2 = parseInt(document.getElementById('c').style.width);//这个才是实际显示的画布大小，非style是当初设定的直接属性值
            const viewportHeight2 = parseInt(document.getElementById('c').style.height);//这个才是实际显示的画布大小
            console.log(viewportWidth2/2,viewportHeight2/2,canvasCenterX, canvasCenterY)

            // 计算视窗中心点相对于画布原点的偏移量
            const offsetX = canvasCenterX - viewportWidth2 / 2;
            const offsetY = canvasCenterY - viewportHeight2 / 2;
            console.log(offsetX,offsetY)

            // 使用absolutePan方法来移动画布到指定的中心位置
            canvas.absolutePan(new fabric.Point(offsetX, offsetY));


            // 使用zoomToPoint方法，以移动后的视窗中心作为缩放的中心，tmd这个方法的参数是相对于视窗的位置的点，而不是画布位置的点……
            canvas.zoomToPoint(new fabric.Point(viewportWidth2 / 2, viewportHeight2 / 2), zoom);

            // 请求画布重新渲染
            canvas.requestRenderAll();
        }











        // 设置夜间模式的函数
        function toggleNightMode(forceNightMode = null) {
            console.log("切换白天夜间模式");
            const isNightMode = document.body.classList.contains('night-mode');
            if (forceNightMode !== null) {
                if (forceNightMode && !isNightMode) {
                    document.body.classList.add('night-mode');
                    document.getElementById('brush-tools').classList.add('night-mode');
                    document.querySelectorAll('.color-button, .center-align label, input[type="range"]').forEach(function(el) {
                        el.classList.add('night-mode');
                    });
                } else if (!forceNightMode && isNightMode) {
                    document.body.classList.remove('night-mode');
                    document.getElementById('brush-tools').classList.remove('night-mode');
                    document.querySelectorAll('.color-button, .center-align label, input[type="range"]').forEach(function(el) {
                        el.classList.remove('night-mode');
                    });
                }
            } else {
                document.body.classList.toggle('night-mode');
                document.getElementById('brush-tools').classList.toggle('night-mode');
                document.querySelectorAll('.color-button, .center-align label, input[type="range"]').forEach(function(el) {
                    el.classList.toggle('night-mode');
                });
            }
        }

        document.getElementById('toggle-night-mode').onclick = function() {
            toggleNightMode();
        };

        toggleNightMode(Nightmode);














        window.onload = function() {
            setTimeout(function() {
                sendMuskArrayToPython();
            }, 500);
        };





        // 工具栏相关设置 //

        {//这个代码块是设置工具栏的宽度适中
            const brushTools = document.getElementById('brush-tools');
            const toolRows = brushTools.getElementsByClassName('tool-row');

            let maxWidth = 0;

            Array.from(toolRows).forEach(row => {
                let rowWidth = 0;
                Array.from(row.children).forEach(child => {
                    const style = window.getComputedStyle(child);
                    const margin = parseFloat(style.marginLeft) + parseFloat(style.marginRight);
                    rowWidth += child.offsetWidth + margin;
                });
                // 更新最大宽度
                if (rowWidth > maxWidth) {
                    maxWidth = rowWidth;
                }
            });

            // 设置brush-tools的宽度为最大子元素行宽度加上30px
            brushTools.style.width = `${maxWidth + 50}px`;
        }

        {// 设定滑块元素和对应的监视器
            var brushColorInput = document.getElementById('brush-color');
            var brushSizeInput = document.getElementById('brush-size');
            var fillToleranceInput = document.getElementById('fill-tolerance');
            var skipPixelsInput = document.getElementById('skip-pixels');

            // 监听画笔颜色选择器的变化
            brushColorInput.addEventListener('change', function() {
                // 设置画笔颜色
                canvas.freeDrawingBrush.color = this.value;
            });

            // 监听画笔宽度选择器的变化
            brushSizeInput.addEventListener('change', function() {
                // 设置画笔宽度
                canvas.freeDrawingBrush.width = parseInt(this.value, 10);
            });

            var fillToleranceValue = 100;
            var skipPixelsValue = 1;

            // 监听填色容差滑动条的变化
            fillToleranceInput.addEventListener('change', function() {
                // 创建一个新的变量来存储填色容差的值
                fillToleranceValue = parseInt(this.value, 10);
            });

            // 监听跳跃像素滑动条的变化
            skipPixelsInput.addEventListener('change', function() {
                // 创建一个新的变量来存储跳跃像素的值
                skipPixelsValue = parseInt(this.value, 10);
            });
        }

        // 初始化画笔颜色和宽度
        canvas.freeDrawingBrush.color = brushColorInput.value;
        canvas.freeDrawingBrush.width = parseInt(brushSizeInput.value, 10);
        //设置填色对象
        var FF = null;
        var filltoolflag = false;

        // 预设颜色按钮，点击按钮可以更改画笔颜色成为标准颜色
        var colorButtons = document.querySelectorAll('.color-button');
        colorButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                console.log("点击了颜色按钮");
                var color = window.getComputedStyle(this).backgroundColor;
                canvas.freeDrawingBrush.color = rgbToHex(color);
                brushColorInput.value = canvas.freeDrawingBrush.color;
            });
        });

        // 当前绘制的图形类型
        let currentShape = 'brush';
        // 临时点数组，用于存储绘制多边形时的点
        let tempPoints = [];
        // 当前绘制的对象（多边形、矩形或圆形）
        let currentObject = null;
        // 是否按下了 alt 键
        let altKeyDown = false;
        // 存储画笔轨迹的点数组
        let brushPoints = [];


        // 工具栏按钮点击事件
        document.getElementById('draw-polygon').onclick = () => setCurrentShape('polygon');
        document.getElementById('draw-rectangle').onclick = () => setCurrentShape('rectangle');
        document.getElementById('draw-circle').onclick = () => setCurrentShape('circle');
        document.getElementById('draw-brush').onclick = () => setCurrentShape('brush');
        document.getElementById('draw-filltool').onclick = () => setCurrentShape('filltool');


        // 设置当前绘制的图形类型
        function setCurrentShape(shape) {
            console.log('setCurrentShape', shape);
            console.log('currentShape', currentShape);
            // 如果当前工具是填色工具，则在切换前调用fillToolClose()
            if (currentShape === 'filltool') {
                fillToolclose();
            }

            if (shape === 'brush') {
                canvas.isDrawingMode = true;
            }else{
                canvas.isDrawingMode = false;
            }

            currentShape = shape;
            tempPoints = [];
            brushPoints = [];
            if (currentObject) {
                canvas.remove(currentObject);
                currentObject = null;
            }
        }










        




        


        // 绘图完成后进行点对象列表处理的统一入口
        function ProcessDrawingPointSetList(uniquePixels){
            // 过滤掉不在画布范围内的点
            uniquePixels = uniquePixels.filter(function(point) {
                return point.x >= 0 && point.x < picwidth && point.y >= 0 && point.y < picheight;
            });
            if (coordinateFlag === "polar") {
                console.log("正在绘制极坐标图");
                //现将零散画布坐标映射到极坐标
                let polarCoordinates = scatterCanvasToPolar(uniquePixels, picwidth ,maskArray_color.length);
                // 然后删掉多余的坐标点（映射之后应该是根据极坐标去删除，删除的原理一样）
                uniquePixels2 = deletepoints(polarCoordinates, maskArray_nan);
                // 删除完之后即将绘制的点保存到数组里
                uniquePixels2.forEach(pixel => {
                    maskArray_color[maskArray_color.length - 1 - pixel.theta][maskArray_color[0].length - 1 - pixel.r] = canvas.freeDrawingBrush.color; // 将maskArray_color中的对应位置的颜色值改为画笔颜色，并左右颠倒
                });
                //然后将极坐标映射到画布坐标
                uniquePixels2 = scatterPolarToCanvas(uniquePixels2, picwidth ,maskArray_color.length);
                //最后绘制
                drawPixelsOnCanvas(canvas, uniquePixels2);

            } else if (coordinateFlag === "rect") {
                console.log("可绘制的范围是:", maskArray_color.length, maskArray_color[0].length);
                uniquePixels = deletepoints(uniquePixels, maskArray_nan);
                uniquePixels.forEach(pixel => {
                    maskArray_color[maskArray_color.length - 1 - pixel.x][maskArray_color[0].length - 1 - pixel.y] = canvas.freeDrawingBrush.color; // 将maskArray_color中的对应位置的颜色值改为画笔颜色，并左右颠倒
                });
                drawPixelsOnCanvas(canvas, uniquePixels);
            }
        }


        // 这个函数的作用是获取两点之间的所有像素点，输入参数为两个点的坐标，返回值为这两点之间的所有像素点的坐标数组
        function getLinePixels(start, end) {
            var dx = end.x - start.x;
            var dy = end.y - start.y;
            var distance = Math.sqrt(dx * dx + dy * dy);
            var stepX = dx / distance;
            var stepY = dy / distance;
            var linePixels = [];
        
            for (var i = 0; i <= distance; i++) {
                var x = start.x + stepX * i;
                var y = start.y + stepY * i;
                linePixels.push({x: Math.round(x), y: Math.round(y)});
            }
        
            return linePixels;
        }
        
        // 这个函数的作用是获取以输入点为圆心，指定半径的圆内的所有像素点，输入参数为圆心坐标和半径，返回值为圆内的所有像素点的坐标数组
        function getCircleCoveredPixels(inputPoint, diameter) {
            var pixels = [];
            // 将直径转换为半径
            var radius = diameter / 2;
            var radiusSquared = Math.pow(radius, 2);
            var centerX = inputPoint.x;
            var centerY = inputPoint.y;
        
            // 遍历圆的边界框内的每个点
            for (var x = centerX - radius; x <= centerX + radius; x++) {
                for (var y = centerY - radius; y <= centerY + radius; y++) {
                    // 检查点是否在圆内
                    if (Math.pow(x - centerX, 2) + Math.pow(y - centerY, 2) <= radiusSquared) {
                        pixels.push({x: x, y: y});
                    }
                }
            }
        
            return pixels;
        }

        // 这个函数用来删掉不符合条件的点，这个b函数的内部顺序全tm是乱的，我根本看不懂，一点点尝试了三四小时尝试出来的
        function deletepoints(uniquePixels, maskarray_delete){
            // 假设maskarray_delete的尺寸是已知的
            const width = maskarray_delete[0].length;
            const height = maskarray_delete.length;

            // 初始化二维布尔数组
            const isBlackPoint = Array.from({ length: height }, () => new Array(width).fill(false));

            // 填充布尔数组
            for (let i = 0; i < height; i++) {
                for (let j = 0; j < width; j++) {
                    if (maskarray_delete[i][j] === "#000000") {
                        isBlackPoint[i][j] = true;
                    }
                }
            }

            // 构造好的二维布尔数组：isBlackPoint
            // 左右翻转
            for (let i = 0; i < height; i++) {
                isBlackPoint[i].reverse();
            }

            // 上下翻转
            isBlackPoint.reverse();

            if (coordinateFlag === "rect"){

                uniquePixels = uniquePixels.filter(function(pixel) {
                    return pixel.x >= 0 && pixel.x < height && pixel.y >= 0 && pixel.y < width;
                });

                // 过滤uniquePixels
                uniquePixels = uniquePixels.filter(pixel => !isBlackPoint[pixel.x][pixel.y]);
            }else{

                uniquePixels = uniquePixels.filter(function(pixel) {
                    return pixel.theta >= 0 && pixel.theta < height && pixel.r >= 0 && pixel.r < width;
                });

                // 过滤uniquePixels
                uniquePixels = uniquePixels.filter(pixel => !isBlackPoint[pixel.theta][pixel.r]);

            }

            return uniquePixels

        }

        // 这个函数的作用是将不重复的像素点数组绘制到 canvas 上
        function drawPixelsOnCanvas(canvas, uniquePixels) {
            // 创建一个临时 canvas，用于绘制临时图像，出现很整齐的绘制不到画布上，一定是画布范围没有设置好
            var tempCanvas = document.createElement('canvas');
            tempCanvas.width = picwidth; // 设置临时 canvas 的宽度与主 canvas 一致
            tempCanvas.height = picheight; // 设置临时 canvas 的高度与主 canvas 一致
            var tempCtx = tempCanvas.getContext('2d'); // 获取临时 canvas 的 2D 绘图上下文

            // 设置临时 canvas 的绘图填充颜色为主 canvas 的自由绘制笔刷颜色
            tempCtx.fillStyle = canvas.freeDrawingBrush.color;

            // 过滤掉 x 或 y 为 null 的点坐标对象
            uniquePixels = uniquePixels.filter(function(pixel) {
                return pixel.x !== null && pixel.y !== null;
            });


            // 遍历 uniquePixels 数组，绘制每一个像素点
            uniquePixels.forEach(function(pixel) {
                    // 检查画笔颜色是否为白色
                    if (canvas.freeDrawingBrush.color === "#ffffff") {
                        // 如果画笔颜色为白色，尝试从 pixelDataArray 中获取对应像素点的颜色
                        var pixelColor = pixelDataArray[pixel.y][pixel.x].color;

                        // 使用获取到的颜色值填充该像素点
                        tempCtx.fillStyle = pixelColor;
                    } else {
                        // 如果画笔颜色不是白色，使用笔刷颜色绘制像素点
                        tempCtx.fillStyle = canvas.freeDrawingBrush.color;
                    }
                    // 在临时 canvas 上填充该像素点
                    tempCtx.fillRect(pixel.x, pixel.y, 1, 1);
            });

            // 将临时 canvas 转换为 fabric.Image，并添加到主 canvas 上
            var imgElement = new Image();
            imgElement.onload = function() {
                var imgInstance = new fabric.Image(imgElement, {
                    left: 0,
                    top: 0,
                    selectable: false,
                    evented: false,
                    objectCaching: false,
                    imageSmoothing: false
                });
                canvas.add(imgInstance);
                canvas.renderAll();
            };
            imgElement.src = tempCanvas.toDataURL();


            setTimeout(function() {
                sendMuskArrayToPython();
            }, 10);


            // 合并图像到主 canvas 上
            //mergeImagesOnCanvas(canvas);
        }


        
        // 十六进制颜色转换为RGBA函数
        function hexToRgba(hex, alpha = 1) {
            var r = parseInt(hex.slice(1, 3), 16),
                g = parseInt(hex.slice(3, 5), 16),
                b = parseInt(hex.slice(5, 7), 16);
        
            return `rgba(${r}, ${g}, ${b}, ${alpha})`;
        }

        // RGB颜色转换为十六进制颜色函数
        function rgbToHex(rgb) {
            // 正则匹配rgb中的数字
            let matches = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
            if (!matches) {
                return rgb; // 如果输入不是有效的rgb格式，直接返回原字符串
            }

            // 将rgb值转换为十六进制，并返回
            return "#" + matches.slice(1, 4).map(x => {
                return ("0" + parseInt(x).toString(16)).slice(-2);
            }).join('');
        }

        // 定义一个函数，用于将xy坐标转换为极坐标（半径和度数）————主要用于向Qt传递坐标的时候使用
        function convertXYToPolarCoordinates(x, y) {
            // 假设图像的宽度和高度已知，这里使用全局变量picwidth和picheight
            const canvasWidth = picwidth;
            const canvasHeight = picheight;
            // 计算圆心坐标
            const centerX = canvasWidth / 2;
            const centerY = canvasHeight / 2;
            // 使用圆心坐标和输入的xy坐标计算dx和dy
            const dx = x - centerX;
            const dy = y - centerY;
            // 计算半径
            const radius = Math.sqrt(dx * dx + dy * dy);
            // 计算从正X轴开始的弧度
            let radian = Math.atan2(dy, dx);
            // 如果弧度为负，加上2π转换为正弧度
            if (radian < 0) {
                radian += 2 * Math.PI;
            }
            // 将弧度转换为角度
            const degree = radian * (180 / Math.PI);

            // 返回半径和度数
            return { radius, degree: Math.round(degree) };
        }


        // 长得很类似的绘制像素点的函数，不过这个函数主要用来画刷新的遮罩层，功能单一
        function drawColorArrayOnCanvas(colorArray) {

            colorArray_temp = JSON.parse(JSON.stringify(colorArray));
            // 上下翻转 colorArray
            colorArray_temp.reverse();

            // 左右翻转 colorArray 的每一行
            colorArray_temp.forEach(row => row.reverse());

            if (coordinateFlag === "polar"){
                colorArray_temp = polarArrayToCanvasArray(colorArray_temp);
            }

            // 更新 colorArray
            console.log("开始绘制遮罩层");

            // 获取二维数组的尺寸
            var rows = colorArray_temp.length;
            var cols = rows > 0 ? colorArray_temp[0].length : 0;

            // 创建一个临时 canvas，用于绘制临时图像
            var tempCanvas2 = document.createElement('canvas');
            tempCanvas2.width = colorArray_temp.length  ; // 设置临时 canvas 的宽度与主 canvas 一致
            console.log("tempCanvas2.width", tempCanvas2.width);
            tempCanvas2.height = colorArray_temp[0].length ; // 设置临时 canvas 的高度与主 canvas 一致
            console.log("tempCanvas2.height", tempCanvas2.height);
            var tempCtx2 = tempCanvas2.getContext('2d'); // 获取临时 canvas 的 2D 绘图上下文

            // 遍历 colorArray 二维数组，绘制每一个像素点
            for (var x = 0; x < rows; x++) {
                for (var y = 0; y < cols; y++) {
                    var color = colorArray_temp[x][y];
                    if (color && color !== '#ffffff' && color !== '#000000') {
                        tempCtx2.fillStyle = color;
                        tempCtx2.fillRect(x, y, 1, 1); // 绘制一个 1x1 的矩形
                    }
                }
            }

            // 将临时 canvas 转换为 fabric.Image，并添加到主 canvas 上
            var imgElement2 = new Image();
            imgElement2.onload = function() {
                var imgInstance = new fabric.Image(imgElement2, {
                    left: 0,
                    top: 0,
                    selectable: false,
                    evented: false,
                    objectCaching: false,
                    imageSmoothing: false
                });
                canvas.add(imgInstance);
                canvas.width = colorArray_temp.length;
                console.log("canvas.width", canvas.width);
                canvas.height = colorArray_temp[0].length;
                console.log("canvas.height", canvas.height);
                canvas.renderAll();
            };
            imgElement2.src = tempCanvas2.toDataURL();
            console.log("绘制遮罩层成功");
        }

        // 在适当的时候调用initializeGlobalImage来初始化全局Image对象
        // 例如，在canvas初始化后

        // 这个函数的作用是将不重复的极坐标点转换为不重复的直角坐标点，返回值为直角坐标点数组
        function calculateUniqueSquares(targetCanvas, totalRadius, segments, radiusDegreeColorPairs) {
            const centerX = targetCanvas.width / 2;
            const centerY = targetCanvas.height / 2;

            const segmentAngle = 2 * Math.PI / segments;

            let uniqueSquares = [];

            radiusDegreeColorPairs.forEach(item => {
                let {radius: actualRadius, degree: degreePosition, color: fillColor} = item;
                actualRadius = Math.min(actualRadius, totalRadius);
                const actualAngle = (degreePosition + 90) * Math.PI / 180;
                const startAngle = actualAngle - segmentAngle / 2;
                const endAngle = actualAngle + segmentAngle / 2;

                for (let angle = startAngle; angle <= endAngle; angle += Math.PI / 1800) {
                    const x = Math.round(centerX + actualRadius * Math.cos(angle));
                    const y = Math.round(centerY + actualRadius * Math.sin(angle));

                    if (!uniqueSquares.some(square => square.left === x && square.top === y)) {
                        uniqueSquares.push({
                            x:x,
                            y:y
                        });
                    }
                }
            });

            return uniqueSquares;
        }

        // 这个函数的作用是移除画布上除了背景对象之外的所有对象，然后将画布导出为图片URL，再将图片URL转换为fabric.Image对象添加到画布上
        function mergeImagesOnCanvas(canvas) {
            // 临时保存背景对象
            var originalBackground = canvas.backgroundImage;
            // 临时移除背景对象
            canvas.backgroundImage = null;
            // 重新渲染画布以应用背景对象的移除
            canvas.renderAll();

            // 导出当前画布的内容为图片URL（此时不包括背景对象）
            var canvasURL = canvas.toDataURL({
                format: 'png',
                quality: 1
            });

            // 恢复背景对象
            canvas.backgroundImage = originalBackground;
            // 重新渲染画布以显示背景对象
            canvas.renderAll();

            // 清除画布上的所有对象（除了背景对象）
            canvas.getObjects().forEach(function(obj) {
                if (obj !== canvas.backgroundImage) {
                    canvas.remove(obj);
                }
            });

            // 使用导出的图片URL创建一个新的fabric.Image对象
            fabric.Image.fromURL(canvasURL, function(newImage) {
                // 将新的图像对象添加到画布上
                canvas.add(newImage);
                // 确保新图像对象在画布上的所有其他对象之下
                newImage.moveTo(0);
                // 渲染画布以显示更改
                canvas.renderAll();
            });
        }

        // 这个函数的作用是将canvas上的坐标转换为极坐标的半径和角度
        function calculateRadiusAndDegreeFromCanvas(x, y) {
            const canvasWidth = canvas.width;
            const canvasHeight = canvas.height;
            const centerX = picwidth / 2;
            const centerY = picheight / 2;

            const dx = x - centerX;
            const dy = y - centerY;

            // 计算半径并取整
            const radius = Math.sqrt(dx * dx + dy * dy);

            // 计算从正X轴开始的弧度
            let radian = Math.atan2(dy, dx);

            // 调整弧度使其从正Y轴开始
            // radian -= Math.PI / 2;

            // 如果弧度为负，加上2π转换为正弧度
            if (radian < 0) {
                radian += 2 * Math.PI;
            }

            // 将弧度转换为角度并取整
            const degree = radian * (180 / Math.PI);

            return { radius, degree };
        }

        // 这个函数的作用是将坐标数组集合转化为极坐标数组集合，并且去除重复项
        function uniquePixelsToUniquePolarCoordinates(uniquePixels, canvas) {
            const uniquePolarSet = new Set();
        
            uniquePixels.forEach(pixel => {
                const { radius, degree } = calculateRadiusAndDegreeFromCanvas(pixel.x, pixel.y, canvas);
                const polarStr = `${radius},${degree}`;
                uniquePolarSet.add(polarStr);
            });
        
            const uniquePolarCoordinates = Array.from(uniquePolarSet).map(str => {
                const [radius, degree] = str.split(',').map(Number);
                return { radius:radius, degree:degree }; // 为每个极坐标对象添加颜色值
            });
        
            return uniquePolarCoordinates;
        }
        
        // 这个函数的作用是为极坐标数组集合添加颜色值
        function addColorToPolarCoordinates(polarCoordinates, brushColor) {
            return polarCoordinates.map(coordinate => {
                return { ...coordinate, color: brushColor }; // 为每个极坐标对象添加颜色值
            });
        }

        // 定义一个函数来分割数组
        function chunkArray(array, chunkSize) {
        const chunks = [];
        for (let i = 0; i < array.length; i += chunkSize) {
            chunks.push(array.slice(i, i + chunkSize));
        }
        return chunks;
        }

        // 这个函数的作用是将多个元素压缩成一个元素——但是有问题……压缩完之后再刷新重新渲染容易出现不可预知的bug
        function mergeImagesOnCanvas(canvas) {
            // 临时保存背景对象
            var originalBackground = canvas.backgroundImage;
            // 临时移除背景对象
            canvas.backgroundImage = null;
            // 重新渲染画布以应用背景对象的移除
            canvas.renderAll();

            // 导出当前画布的内容为图片URL（此时不包括背景对象）
            var canvasURL = canvas.toDataURL({
                format: 'png',
                quality: 1
            });

            // 恢复背景对象
            canvas.backgroundImage = originalBackground;
            // 重新渲染画布以显示背景对象
            canvas.renderAll();

            // 清除画布上的所有对象（除了背景对象）
            canvas.getObjects().forEach(function(obj) {
                if (obj !== canvas.backgroundImage) {
                    canvas.remove(obj);
                }
            });

            // 使用导出的图片URL创建一个新的fabric.Image对象
            fabric.Image.fromURL(canvasURL, function(newImage) {
                // 将新的图像对象添加到画布上
                canvas.add(newImage);
                // 确保新图像对象在画布上的所有其他对象之下
                newImage.moveTo(0);
                // 渲染画布以显示更改
                canvas.renderAll();
            });
        }

        // 这个函数的作用是清除画布上所有内容并回到初始状态
        function clearCanvasCompletely(canvas) {
            // 清除画布上的所有对象
            objexts = canvas.getObjects();
            console.log(objexts);
            
            objexts.forEach(function(obj) {
                canvas.remove(obj);
            });

            // 清除画布背景图
            //canvas.setBackgroundImage(null, canvas.renderAll.bind(canvas));

            // 清除画布背景色
            canvas.setBackgroundColor(null, canvas.renderAll.bind(canvas));

            // 重新渲染画布
            canvas.renderAll();
        }




        
        // 你的图片的Base64编码
        function handleBase64Image(base64Image) {
            console.log("准备开始绘制图片");
            // 从 URL 加载图像，并处理图像数据
            fabric.Image.fromURL(base64Image, function(oImg) {
                // 创建临时 canvas 用于处理图像
                var tempCanvas = document.createElement('canvas');
                tempCanvas.width = oImg.width; // 设置临时 canvas 的宽度为图像宽度
                tempCanvas.height = oImg.height; // 设置临时 canvas 的高度为图像高度
                picwidth = oImg.width;//设置全局变量为图片的宽度
                picheight = oImg.height;//设置全局变量为图片的高度
                var ctx = tempCanvas.getContext('2d'); // 获取临时 canvas 的 2D 绘图上下文
                console.log("图片的宽度是", oImg.width, "准备开始绘制图片");
                // 绘制图像到临时 canvas 上
                ctx.drawImage(oImg.getElement(), 0, 0, oImg.width, oImg.height);

                // 获取图像的像素数据
                var imageData = ctx.getImageData(0, 0, tempCanvas.width, tempCanvas.height);
                var data = imageData.data; // 像素数据数组

                // 遍历图像的像素数据
                for (var y = 0; y < tempCanvas.height; y++) {
                    var row = [];
                    for (var x = 0; x < tempCanvas.width; x++) {
                        var index = (y * tempCanvas.width + x) * 4; // 计算像素索引
                        var r = data[index]; // 获取红色通道值
                        var g = data[index + 1]; // 获取绿色通道值
                        var b = data[index + 2]; // 获取蓝色通道值

                        // 将 RGB 转换为十六进制颜色值
                        var hex = "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);

                        // 将像素点的信息（坐标和颜色）存储到行数组中
                        row.push({x: x, y: y, color: hex});
                    }
                    // 将行数组添加到全局像素数据数组中
                    pixelDataArray.push(row);
                }

                // 此时，pixelDataArray 已经包含了图像的像素数据

                // 假设oImg是已加载的图像对象
                // 首先，获取页面的宽度和高度，减去200
                var pageWidth = window.innerWidth-50;
                var pageHeight = window.innerHeight-50;

                // 检查图像的宽度和高度是否小于页面的宽度和高度（都减去了200）
                if (oImg.width < pageWidth && oImg.height < pageHeight) {
                    // 如果图像的宽度和高度都小于页面的宽度和高度，直接使用图像的尺寸
                    canvas.setWidth(oImg.width);
                    canvas.setHeight(oImg.height);
                } else {
                    // 如果图像的任一尺寸大于页面的对应尺寸，使用页面的尺寸
                    canvas.setWidth(pageWidth);
                    canvas.setHeight(pageHeight - brushToolsHeight);
                    // 计算缩放比例，使得画布适合窗口大小
                    var scaleX = pageWidth / oImg.width;
                    var scaleY = (pageHeight - brushToolsHeight) / oImg.height;
                    var scale = Math.min(scaleX, scaleY);

                    // 应用缩放到画布
                    canvas.setZoom(scale);

                    // 调整视口，使画布居中
                    var viewport = canvas.viewportTransform;
                    viewport[4] = (pageWidth - oImg.width * scale) / 2;
                    viewport[5] = (pageHeight - brushToolsHeight - oImg.height * scale) / 2;

                    // 应用视口变换
                    canvas.setViewportTransform(viewport);
                }

                oImg.imageSmoothing = false;
            
                // 设置背景图片并调整其大小以适应画布
                canvas.setBackgroundImage(oImg, canvas.renderAll.bind(canvas), {
                    scaleX: 1,//不调整
                    scaleY: 1,
                    // 在这里也可以设置imageSmoothingEnabled为false，但主要是通过oImg.imageSmoothing来控制
                    imageSmoothingEnabled: false
                });
                console.log("视窗大小为",window.innerWidth,window.innerHeight,"画布大小为",document.getElementById('c').width,document.getElementById('c').height,"画布样式大小为",document.getElementById('c').style.width,document.getElementById('c').style.height,"视窗位于",document.getElementById('c').getBoundingClientRect().left,document.getElementById('c').getBoundingClientRect().top);
                // 输出大哥前视窗中心位于画布的坐标
                console.log("视窗中心位于",canvas.getVpCenter().x,canvas.getVpCenter().y);
            });
        }






















        // 图形功能的的代码主要都写在这里 //


        // 绘制的时候处理画笔路径点坐标
        function brushpath(options){
            var path = options.path; // 获取绘制的路径
            canvas.remove(path); // 移除原始路径

            // 使用Map来存储已处理的像素点，以便快速去重
            const processedPixels = new Map();

            path.path.forEach(function(point, index) {
                if (index > 0) {
                    var prevPoint = path.path[index - 1];
                    var linePixels = getLinePixels({x: prevPoint[1], y: prevPoint[2]}, {x: point[1], y: point[2]});
                    linePixels.forEach(function(pixel) {
                        var pixelKey = pixel.x + "," + pixel.y;
                        if (!processedPixels.has(pixelKey)) {
                            var allCirclePixels = getCircleCoveredPixels(pixel, canvas.freeDrawingBrush.width);
                            allCirclePixels.forEach(function(point) {
                                var circlePixelKey = point.x + "," + point.y;
                                processedPixels.set(circlePixelKey, true);
                            });
                        }
                    });
                } else {
                    getCircleCoveredPixels({x: point[1], y: point[2]}, canvas.freeDrawingBrush.width).forEach(function(point) {
                        var circlePixelKey = point.x + "," + point.y;
                        processedPixels.set(circlePixelKey, true);
                    });
                }
            });

            // 优化：直接在forEach中构造对象，避免后续的map操作
            var uniquePixels = [];
            processedPixels.forEach((value, key) => {
                var parts = key.split(",");
                uniquePixels.push({ x: parseInt(parts[0], 10), y: parseInt(parts[1], 10) });
            });
            ProcessDrawingPointSetList(uniquePixels);
        };



        // 添加折线到画布
        function addPolyline(points) {
            currentObject = new fabric.Polyline(points, {
                stroke: canvas.freeDrawingBrush.color,
                strokeWidth: 1,
                fill: hexToRgba(canvas.freeDrawingBrush.color, 0.3),//"transparent"是透明
                selectable: false,
                evented: false,
                objectCaching: false
            });
            canvas.add(currentObject);
        }

        // 更新折线的点
        function updatePolyline(points) {
            if (currentObject) {
                currentObject.set({ points: points });
                canvas.requestRenderAll();
            }
        }

        // 完成多边形的绘制
        function finishPolygon() {
            if (tempPoints.length < 3) return;
            const polygon = new fabric.Polygon(tempPoints, {
                stroke: canvas.freeDrawingBrush.color,
                strokeWidth: 1,
                fill: hexToRgba(canvas.freeDrawingBrush.color, 0.3),//之前写的时候都没想过这个函数还能在其他地方派上用场！！
                selectable: true,
                evented: true,
            });
            canvas.add(polygon);
            canvas.remove(currentObject);
            tempPoints = [];
            currentObject = null;
            consoleWrappedPoints(polygon);
        }

        // 添加矩形到画布
        function addRectangle(startPoint) {
            currentObject = new fabric.Rect({
                left: startPoint.x,
                top: startPoint.y,
                width: 0,
                height: 0,
                stroke: canvas.freeDrawingBrush.color,
                strokeWidth: 1,
                fill: hexToRgba(canvas.freeDrawingBrush.color, 0.3),
                selectable: true,
                evented: true,
            });
            canvas.add(currentObject);
        }

        // 更新矩形的尺寸
        function updateRectangle(endPoint) {
            if (currentObject) {
                currentObject.set({
                    width: Math.abs(endPoint.x - tempPoints[0].x),
                    height: Math.abs(endPoint.y - tempPoints[0].y),
                    // 这两必须禁掉，不然重新渲染的时候会出现边框很丑
                    hasControls: false, // 禁用控制点
                    hasBorders: false // 禁用边界
                });
                if (endPoint.x < tempPoints[0].x) {
                    currentObject.set({ left: endPoint.x });
                }
                if (endPoint.y < tempPoints[0].y) {
                    currentObject.set({ top: endPoint.y });
                }
                canvas.requestRenderAll();
            }
        }

        // 完成矩形的绘制
        function finishRectangle() {
            if (tempPoints.length !== 1) return;

            // 移除当前的矩形对象
            canvas.remove(currentObject);

            // 创建并添加新的矩形对象
            const newRectangle = new fabric.Rect({
                left: currentObject.left,
                top: currentObject.top,
                width: currentObject.width,
                height: currentObject.height,
                stroke: canvas.freeDrawingBrush.color,
                strokeWidth: 1,
                fill: hexToRgba(canvas.freeDrawingBrush.color, 0.3),
                selectable: true,
                evented: true,
                originX: 'left',
                originY: 'top'
            });
            canvas.add(newRectangle);

            // 清空临时点数组和当前对象
            tempPoints = [];
            currentObject = null;

            // 传入新创建的矩形对象
            consoleWrappedPoints(newRectangle);
        }

        // 添加圆形到画布
        function addCircle(startPoint) {
            currentObject = new fabric.Circle({
                left: startPoint.x,
                top: startPoint.y,
                radius: 0,
                stroke: canvas.freeDrawingBrush.color,
                strokeWidth: 1,
                fill: hexToRgba(canvas.freeDrawingBrush.color, 0.3),
                selectable: true,
                evented: true,
                originX: 'center',
                originY: 'center'
            });
            canvas.add(currentObject);
        }

        // 更新圆形的半径
        function updateCircle(endPoint) {
            if (currentObject) {
                // 计算起点和终点之间的距离，作为直径
                const diameter = Math.sqrt(Math.pow(endPoint.x - tempPoints[0].x, 2) + Math.pow(endPoint.y - tempPoints[0].y, 2));
                const radius = diameter / 2; // 半径是直径的一半

                // 设置圆形的半径
                currentObject.set({ radius: radius });

                // 计算并设置圆形的中心点位置
                currentObject.set({
                    left: (tempPoints[0].x + endPoint.x) / 2, // 圆心的X坐标
                    top: (tempPoints[0].y + endPoint.y) / 2, // 圆心的Y坐标
                    hasControls: false, // 禁用控制点
                    hasBorders: false // 禁用边界
                });

                // 请求画布重新渲染
                canvas.requestRenderAll();
            }
        }

        // 完成圆形的绘制
        function finishCircle() {
            if (tempPoints.length !== 1) return;

            // 移除当前的圆形对象
            canvas.remove(currentObject);

            // 创建并添加新的圆形对象
            const newCircle = new fabric.Circle({
                left: currentObject.left,
                top: currentObject.top,
                radius: currentObject.radius,
                stroke: canvas.freeDrawingBrush.color,
                strokeWidth: 1,
                fill: hexToRgba(canvas.freeDrawingBrush.color, 0.3),
                selectable: true,
                evented: true,
                originX: 'center',
                originY: 'center'
            });
            canvas.add(newCircle);

            // 清空临时点数组和当前对象
            tempPoints = [];
            currentObject = null;

            // 传入新创建的圆形对象
            consoleWrappedPoints(newCircle);
        }


        // 函数用于获取多边形内部所有点的集合（使用射线法，说句实话我还是理解不能这个代码到底和书上的射线法有什么关系）
        function getPointsInsidePolygon(polygon) {
            const points = polygon.get('points'); // 获取多边形的顶点
            const boundingRect = polygon.getBoundingRect(true, true); // 获取多边形的包围盒，第一个参数为true表示是相对于画布的位置坐标
            console.log(boundingRect.left,boundingRect.top,boundingRect.width,boundingRect.height);
            const polygonPoints = points
            points.forEach(element => {
                console.log("X的坐标为：",element.x,"Y的坐标为：",element.y)
            });

            const pointsInside = [];

            function pointInPolygon(point, polygonPoints) {
                let inside = false;
                const n = polygonPoints.length

                function isPointOnSegment(p, p1, p2) {
                    const onSegment = (p[0] === p1[0] && p[1] === p1[1]) || (p[0] === p2[0] && p[1] === p2[1]);
                    return onSegment;
                }

                for (let i = 0, j = n - 1; i < n; j = i++) {
                    const xi = polygonPoints[i].x, yi = polygonPoints[i].y;
                    const xj = polygonPoints[j].x, yj = polygonPoints[j].y;

                    if (isPointOnSegment([point.x, point.y], [xi, yi], [xj, yj])) {
                        return true;
                    }

                    const intersect = (yi > point.y) !== (yj > point.y) &&
                                    point.x < ((xj - xi) * (point.y - yi)) / (yj - yi) + xi;

                    if (intersect) inside = !inside;
                }
                return inside;
            }

            // 遍历包围盒内所有点，判断是否在多边形内部
            for (let x = boundingRect.left; x <= boundingRect.left + boundingRect.width; x++) {
                for (let y = boundingRect.top; y <= boundingRect.top + boundingRect.height; y++) {
                    if (pointInPolygon({ x, y }, polygonPoints)) {
                        pointsInside.push({ x:x, y:y }); // 将在多边形内部的点加入集合
                    }
                }
            }
            console.log("包裹的坐标点数量为",pointsInside.length);
            return pointsInside;
        }



        // 计算并输出图形包裹的点的集合
        function consoleWrappedPoints(object) {
            let pointsCollection = [];

            // 根据对象类型获取不同的边界和点集合
            if (object.type === 'rect') {
                // 矩形
                const minX = Math.floor(object.left);
                const minY = Math.floor(object.top);
                const maxX = Math.ceil(object.left + object.width);
                const maxY = Math.ceil(object.top + object.height);

                for (let x = minX; x <= maxX; x++) {
                    for (let y = minY; y <= maxY; y++) {
                        pointsCollection.push({ x, y });
                    }
                }
            } else if (object.type === 'circle') {
                // 圆形
                const centerX = object.left;
                const centerY = object.top;
                console.log(centerX, centerY);
                const radius = object.radius;

                for (let x = Math.floor(centerX - radius); x <= Math.ceil(centerX + radius); x++) {
                    for (let y = Math.floor(centerY - radius); y <= Math.ceil(centerY + radius); y++) {
                        if (Math.sqrt(Math.pow(x - centerX, 2) + Math.pow(y - centerY, 2)) <= radius) {
                            pointsCollection.push({ x, y });
                        }
                    }
                }
            } else if (object.type === 'polygon') {
                // 多边形
                const polygonPoints = getPointsInsidePolygon(object);

                polygonPoints.forEach(point => {
                    pointsCollection.push({ x: Math.round(point.x), y: Math.round(point.y) });
                });
            }


            // 将点坐标对象列表传入 drawPixelsOnCanvas 函数
            ProcessDrawingPointSetList(pointsCollection);

            // 删除这个对象
            canvas.remove(object);

            // 禁用画布的默认右键菜单行为，以免与完成绘制的操作冲突
            canvas.upperCanvasEl.addEventListener('contextmenu', function(e) {
                e.preventDefault();
            });
        }


        function fillTool(pointer) {
            filltoolflag = true
            var fillToolBottom = document.getElementById('draw-filltool');
            fillToolBottom.innerHTML = ""
            fillToolBottom.innerText = "正在填色"; // 设置文本为“填色中”
            fillToolBottom.style.fontSize = '10px'; // 设置文本大小为12px

            if (FF) {
                console.log('FF已经存在，更新画布');
                FF.updateOffscreenCanvas();
            } else {
                console.log('FF不存在，创建新实例');
                FF = FastFill.create({
                    elementId: 'c',
                    canvasSize: [picwidth, picheight],
                    fillColor: [170, 0, 0, 255],//这个暂时用不到，设置成画笔颜色的话，还得转换一下，想想就让它默认得了
                    tolerance: fillToleranceValue,
                    skipDistance: skipPixelsValue,
                    offscreenCanvasVisible: false,
                    isFabricCanvas: true,
                    fabricCanvas: canvas
                });
            }
            FF.loaded(res => {
                // 直接在当前位置处理和转换点坐标，一获取到结果立刻转化成整数
                returnpoints = FF.manualFill(pointer.x, pointer.y).map(point => ({
                    x: Math.round(point.x),
                    y: Math.round(point.y)
                }));
                // 过滤掉不在画布范围内的点坐标对象
                ProcessDrawingPointSetList(returnpoints);
                fillToolBottom.innerHTML = '<i class="fas fa-fill-drip"></i>'; // 填色完成后还原文本
                filltoolflag = false
            });
        }

        function fillToolclose() {
            FF.close();
            FF = null;
        }



        // 监听函数和监听过程主要放这里 //


        var isDragging = false; // 定义一个标志，用于判断用户是否正在拖动画布
        var isMouseDown = false; // 定义一个标志，用于判断鼠标是否按下
        var lastPosX = 0; // 记录上一次鼠标的X位置
        var lastPosY = 0; // 记录上一次鼠标的Y位置


        function  enableZoom(opt) {
            var delta = opt.e.deltaY; // 获取鼠标滚轮的滚动值，向上滚动为负值，向下滚动为正值

            var zoom = canvas.getZoom(); // 获取当前画布的缩放比例
            zoom *= 0.999 ** delta; // 根据滚动值调整缩放比例，滚轮每滚动一单位，缩放比例变化0.1%

            if (zoom > 20) zoom = 20; // 限制最大缩放比例为20倍，防止过度放大
            if (zoom < 0.01) zoom = 0.01; // 限制最小缩放比例为0.01倍，防止过度缩小

            // 应用新的缩放比例，以鼠标当前位置为中心进行缩放
            canvas.zoomToPoint({ x: opt.e.offsetX, y: opt.e.offsetY }, zoom);

            // 禁用图像平滑处理，保持像素点清晰
            canvas.imageSmoothingEnabled = false;

            opt.e.preventDefault(); // 阻止默认的滚轮滚动行为，避免滚动画布时页面也跟着滚动
            opt.e.stopPropagation(); // 阻止事件冒泡，避免滚轮事件影响到其他元素
        }



        // 处理鼠标右键点击事件
        function handleRightClick(e) {
            if (e.button === 2) { // 右键点击
                if (isDragging) return; // 如果按下 alt 键，进入拖动模式，不执行结束绘制操作
                e.preventDefault();
                if (currentShape === 'polygon' && tempPoints.length >= 3) {
                    finishPolygon();
                } else if (currentShape === 'rectangle' && tempPoints.length === 1) {
                    finishRectangle();
                } else if (currentShape === 'circle' && tempPoints.length === 1) {
                    finishCircle();
                } 
            }
        }

        // 处理鼠标按下事件
        function handleMousedown(options) {
            var e = options.e;
            isMouseDown = true; // 设置鼠标按下标志为true
            lastPosX = e.clientX;
            lastPosY = e.clientY;
            console.log("进入鼠标按下事件")
            // 直接检测alt键是否按下
            if (e.altKey) {
                isDragging = true; // 如果按下 alt 键，设置拖动标志为true
                canvas.isDrawingMode = false; // 如果按下 alt 键，设置拖动标志为true
                return; // 并返回，不执行绘制操作
            } else {
                isDragging = false; // 如果没有按下 alt 键，设置拖动标志为false
            }
            const pointer = canvas.getPointer(options.e);
            if (currentShape === 'polygon') {
                tempPoints.push(pointer);
                if (tempPoints.length === 1) {
                    addPolyline([pointer]);
                } else {
                    updatePolyline(tempPoints);
                }
            } else if (currentShape === 'rectangle' && tempPoints.length === 0) {
                tempPoints.push(pointer);
                addRectangle(pointer);
            } else if (currentShape === 'circle' && tempPoints.length === 0) {
                tempPoints.push(pointer);
                addCircle(pointer);
            } else if (currentShape === 'filltool' && filltoolflag === false) {
                console.log('触发filltool');
                fillTool(pointer);
            }
        }


        // 处理鼠标移动事件
        function handleMouseMove(options) {
            if (isDragging && isMouseDown) { // 只有当处于拖动模式并且鼠标按下时才处理拖动
                    var e = options.e;
                    var vpt = canvas.viewportTransform;
                    vpt[4] += e.clientX - lastPosX;
                    vpt[5] += e.clientY - lastPosY;
                    canvas.requestRenderAll();
                    lastPosX = e.clientX;
                    lastPosY = e.clientY;
                }
            if (isDragging) return; // 如果按下 alt 键，不执行绘制操作
            const pointer = canvas.getPointer(options.e);
            if (currentShape === 'polygon' && tempPoints.length > 0 && options.target === null) {
                const tempPointsWithCurrent = [...tempPoints, pointer];
                updatePolyline(tempPointsWithCurrent);
            } else if (currentShape === 'rectangle' && tempPoints.length === 1) {
                updateRectangle(pointer);
            } else if (currentShape === 'circle' && tempPoints.length === 1) {
                updateCircle(pointer);
            } 
        }

        //监听鼠标移动事件，回传信息给Qt端
        function handleMouseMovetoQt(event) {
            if (document.hasFocus() === false) {//鼠标在网页上移动的时候。如果窗口没有焦点，则聚焦窗口
                window.focus();}
            if (event.e.shiftKey) { // 检查是否按下了Shift键
                var pointer = canvas.getPointer(event.e);
                const mouseX = pointer.x;
                const mouseY = pointer.y;

                // 将画布上的坐标转换为极坐标
                const { radius, degree } = calculateRadiusAndDegreeFromCanvas(mouseX, mouseY, canvas);
                console.log(`半径: ${radius}, 角度: ${degree}, 鼠标坐标: (${mouseX}, ${mouseY})`);

                if (coordinateFlag === "polar") {
                    sendListToPython([radius, degree]);
                } else if (coordinateFlag === "rect") {
                    sendListToPython([mouseX, mouseY]);
                }
            }
        }

        // 监听鼠标释放事件函数定义
        function handleMouseUp(options) {
            isMouseDown = false; // 设置鼠标按下标志为false
        }

        // 键盘抬起事件函数定义
        function handleAltKeyUp(e) {
            if (e.key === 'Alt') { // 如果松开的是Alt键
                if (currentShape === 'brush'){
                    canvas.isDrawingMode = true; // 恢复画布的绘制模式
                }
                isDragging = false; // 结束拖动模式
            }
        }

        // 键盘按下事件函数定义
        function handleKeyDown(e) {
            if (e.key === 'Alt') { // 如果按下的是Alt键
                e.preventDefault(); // 防止默认行为
                if (currentShape === 'brush'){
                    canvas.isDrawingMode = false; // 禁用画布的绘制模式
                }
                isDragging = true; // 启动拖动模式
            }
            if (e.key === 'Control') { // 如果按下的是Ctrl键
                e.preventDefault(); // 防止默认行为
                const zoom = canvas.getZoom(); // 获取当前画布的缩放值
                const viewportCenter = canvas.getVpCenter(); // 获取当前视窗中心点
                var polarpoint = convertXYToPolarCoordinates(viewportCenter.x, viewportCenter.y);
                console.log(`当前画布缩放值: ${zoom}`);
                console.log(`当前视窗中心对应于画布的坐标: (${viewportCenter.x}, ${viewportCenter.y})`);
                console.log(`当前视窗中心对应的极坐标: 半径 ${polarpoint.radius}, 角度 ${polarpoint.degree}`);
                console.log(`当前极坐标标识符: ${coordinateFlag}`);
                if (coordinateFlag === "polar") {
                    sendCanvasPositionToPython([zoom, polarpoint.radius, polarpoint.degree]);
                } else if (coordinateFlag === "rect") {
                    sendCanvasPositionToPython([zoom, viewportCenter.x, viewportCenter.y]);
                }
            }
        }







        {// 启动监听事件
            // 画布相关——监听画笔路径，将其传入画笔路径处理函数
            canvas.on('path:created', brushpath)

            // 监听鼠标抬起事件
            canvas.on('mouse:down', handleMousedown);
            // 监听鼠标移动事件（拖动操作和传递信息给Qt）
            canvas.on('mouse:move', handleMouseMove);
            canvas.on('mouse:move', handleMouseMovetoQt)
            // 监听鼠标滚轮事件
            canvas.on('mouse:wheel',enableZoom);
            // 监听鼠标释放事件
            canvas.on('mouse:up', handleMouseUp);
            // 监听鼠标右键点击事件
            document.addEventListener('pointerdown', handleRightClick)
            // 监听键盘松开事件
            document.addEventListener('keyup', handleAltKeyUp);
            // 监听键盘按下事件
            document.addEventListener('keydown', handleKeyDown);
        }

    </script>
</body>
</html>

"""



ReferenceImageContainer = """
<!DOCTYPE html>
<html>
<head>
    <title>绘制图像</title>
    <script src="https://cdn.bootcdn.net/ajax/libs/fabric.js/4.5.0/fabric.min.js"></script>
    <script type="text/javascript" src="qrc:///qtwebchannel/qwebchannel.js"></script>
    <script type="text/javascript">
        var bridge;
        var flag = 2; // 画布绘制标志位，如果=1说明是第一次绘制，否则是更新绘制
        var CalibrationFlagPosition = false;

        
        // 设置全局变量表示十字线的初始位置
        var crosshairPosition = { x:100, y:100 };

        var flagss = "遮罩图标志位";
        document.addEventListener("DOMContentLoaded", function() {
            new QWebChannel(qt.webChannelTransport, function(channel) {
                bridge = channel.objects.bridge;
    
                // 监听从Python发送的列表
                bridge.sendListToJS.connect(function(list) {
                    //console.log("接收python的数组:", list);
                    if (typeof list[0] === 'number' ) {
                        updateCrosshairPosition(list);
                    }
                    if (typeof list[0] === 'string' && list[0].startsWith('十字标注线' )&& flagss === "已开启遮罩图") {
                        setBackgroundImage(list[1], canvas);
                    }
                    // 处理接收到的列表...
                });

                // 监听从Python发送的画布位置列表
                bridge.sendCanvasPositionToJS.connect(function(list) {
                    console.log("接收python的画布位置数组:", list);
                    //console.log("接收python的画布位置数组:", list);
                    if (flagss === "已开启遮罩图") {
                        console.log("mask容器位置调整参数:", list[0], list[5], list[6]);
                        adjustCanvas(list[0], list[5], list[6]);
                    }else{
                        zoomnumber = list[0] * ((list[1] / picwidth) + (list[2] / picwidth) / 2);
                        console.log("参考图容器位置调整参数:", zoomnumber, list[3], list[4]);
                        adjustCanvas(zoomnumber, list[3], list[4]);
                    }
                    
                });



                // 请求Python发送列表
                // bridge.requestListFromPython();
            });
        });
        function sendCorrectionCoordinatesToPython(x, y) {
            if (bridge) {
                // 将坐标封装成列表
                var coordinates = [x, y];
                // 使用bridge对象发送坐标到Python
                bridge.sendCoordinatesToPython(coordinates);
            } else {
                console.error("Bridge is not initialized.");
            }
        }


    </script>
    <style>
        html, body {
            height: 100%;
            width: 100%;
            margin: 0;
            padding: 0;
            overflow: hidden; /* 防止滚动条出现 */
            display: flex; /* 使用Flexbox布局 */
            justify-content: center; /* 水平居中 */
            align-items: center; /* 垂直居中 */
            position: relative; /* 设置为相对定位，作为后代绝对定位元素的参考 */
        }
        
        #crosshair-all {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none; /* 允许鼠标事件穿透，以便可以与下面的canvas互动 */
        }
        
        #crosshair-h, #crosshair-v {
            position: absolute;
            background-color: black;
        }
        
        #crosshair-h {
            left: 0;
            right: 0;
            height: 1px; /* 十字线的粗细 */
            top: 50%; /* 水平线位于垂直中间 */
        }
        
        #crosshair-v {
            top: 0;
            bottom: 0;
            width: 1px; /* 十字线的粗细 */
            left: 50%; /* 垂直线位于水平中间 */
        }

        .night-mode {
            background-color: #000000;
            color: #e0e0e0;
        }
    </style>
    </head>
    <body>
        <canvas id="c"></canvas>
        <div id="crosshair-all">
            <div id="crosshair-h"></div>
            <div id="crosshair-v"></div>
        </div>
    </body>
    <script>
        var Nightmode = false; // 默认不是夜间模式

        // 初始化fabric画布
        var canvas = new fabric.Canvas('c', {
            imageSmoothingEnabled: false // 将像素点平滑关掉
            });

        // 全局变量，用于存储鼠标的最后位置
        var lastMouseX = 0;
        var lastMouseY = 0;
        var picwidth = 0;
        var picheight = 0;


        // 按照画布上的点和缩放参数移动画布的函数
        function adjustCanvas(zoom, canvasCenterX, canvasCenterY) {

            // 设置画布的缩放级别
            canvas.setZoom(1);

            canvas.absolutePan(new fabric.Point(0, 0));

            //实际偏移的位置
            const viewportWidth2 = parseInt(document.getElementById('c').style.width);//这个才是实际显示的画布大小，非style是当初设定的直接属性值
            const viewportHeight2 = parseInt(document.getElementById('c').style.height);//这个才是实际显示的画布大小
            console.log(viewportWidth2/2,viewportHeight2/2,canvasCenterX, canvasCenterY)

            // 计算视窗中心点相对于画布原点的偏移量
            const offsetX = canvasCenterX - viewportWidth2 / 2;
            const offsetY = canvasCenterY - viewportHeight2 / 2;
            console.log(offsetX,offsetY)

            // 使用absolutePan方法来移动画布到指定的中心位置
            canvas.absolutePan(new fabric.Point(offsetX, offsetY));


            // 使用zoomToPoint方法，以移动后的视窗中心作为缩放的中心，tmd这个方法的参数是相对于视窗的位置的点，而不是画布位置的点……
            canvas.zoomToPoint(new fabric.Point(viewportWidth2 / 2, viewportHeight2 / 2), zoom);

            // 请求画布重新渲染
            canvas.requestRenderAll();
        }



        // 你的图片的Base64编码
        var base64Image = 'base64数据替换占位符';

        function setBackgroundImage(base64Image, canvas) {
            fabric.Image.fromURL(base64Image, function(oImg) {
                // 根据加载的图片大小调整画布大小
                canvas.setWidth(oImg.width);
                canvas.setHeight(oImg.height);

                // 设置全局变量——图像宽高
                picwidth = oImg.width;//设置全局变量为图片的宽度
                picheight = oImg.height;//设置全局变量为图片的高度

                crosshairPosition.x = oImg.width / 2;
                crosshairPosition.y = oImg.height / 2;

                var pageWidth = window.innerWidth-50;
                var pageHeight = window.innerHeight-50;

                if (flag !== 0){ 
                    // 检查图像的宽度和高度是否小于页面的宽度和高度（都减去了200）
                    if (oImg.width < pageWidth && oImg.height < pageHeight) {
                        // 如果图像的宽度和高度都小于页面的宽度和高度，直接使用图像的尺寸
                        canvas.setWidth(oImg.width);
                        canvas.setHeight(oImg.height);
                    } else {
                        // 如果图像的任一尺寸大于页面的对应尺寸，使用页面的尺寸
                        canvas.setWidth(pageWidth);
                        canvas.setHeight(pageHeight);
                        // 计算缩放比例，使得画布适合窗口大小
                        var scaleX = pageWidth / oImg.width;
                        var scaleY = pageHeight / oImg.height;
                        var scale = Math.min(scaleX, scaleY);

                        // 应用缩放到画布
                        canvas.setZoom(scale);

                        // 调整视口，使画布居中
                        var viewport = canvas.viewportTransform;
                        viewport[4] = (pageWidth - oImg.width * scale) / 2;
                        viewport[5] = (pageHeight - oImg.height * scale) / 2;

                        // 应用视口变换
                        canvas.setViewportTransform(viewport);
                    }
                    flag = flag - 1;
                }




                // 关闭图片的抗锯齿
                oImg.imageSmoothing = false;

                // 设置背景图片并调整其大小以适应画布
                canvas.setBackgroundImage(oImg, canvas.renderAll.bind(canvas), {
                    scaleX: 1,
                    scaleY: 1,
                    imageSmoothingEnabled: false
                });
                console.log("视窗大小为",window.innerWidth,window.innerHeight,"画布大小为",document.getElementById('c').width,document.getElementById('c').height,"画布样式大小为",document.getElementById('c').style.width,document.getElementById('c').style.height);
            });
        }

        function drawCrosshair(position) {
            //console.log("开始绘制十字线", position);
            var canvasElement = document.getElementById('c');
            var rect = canvasElement.getBoundingClientRect(); // 获取画布相对于视口的位置

            // 假设canvas是你的fabric.Canvas实例
            var zoom = canvas.getZoom();
            var viewportTransform = canvas.viewportTransform;
            var offsetX = viewportTransform[4];
            var offsetY = viewportTransform[5];

            // 调整position以考虑缩放和偏移
            var adjustedX = (position.x * zoom) + offsetX;
            var adjustedY = (position.y * zoom) + offsetY;

            // 计算画布上的点在网页上的绝对位置
            var absoluteX = rect.left + adjustedX;
            var absoluteY = rect.top + adjustedY;

            var crosshairH = document.getElementById('crosshair-h');
            var crosshairV = document.getElementById('crosshair-v');
            crosshairH.style.backgroundColor = 'black';
            crosshairV.style.backgroundColor = 'black';

            // 设置十字线的位置，使其以画布上的点为中心
            crosshairH.style.top = absoluteY + 'px';
            crosshairH.style.left = 0;
            crosshairH.style.width = '100%';
            crosshairH.style.height = '1px';

            crosshairV.style.left = absoluteX + 'px';
            crosshairV.style.top = 0;
            crosshairV.style.width = '1px';
            crosshairV.style.height = '100%';
        }

        // 示例：在画布的(100, 100)位置绘制十字线
        // 注意：实际使用时，应根据需要调用此函数
        function updateCrosshairPosition(positionArray) {
            // 更新全局变量crosshairPosition的值
            crosshairPosition = { x: positionArray[0], y: positionArray[1] };
            //console.log("更新的crosshairPosition:", crosshairPosition);

            // 使用更新后的crosshairPosition调用drawCrosshair函数
            drawCrosshair(crosshairPosition);
        }

        // updateCrosshairPosition([100, 100]);

        // 这个函数的作用是启用画布的放大缩小功能
        function enableZoom() {
            // 监听画布上的鼠标滚轮事件
            canvas.on('mouse:wheel', function(opt) {
            var delta = opt.e.deltaY; // 获取鼠标滚轮的滚动值，向上滚动为负值，向下滚动为正值

            var zoom = canvas.getZoom(); // 获取当前画布的缩放比例
            zoom *= 0.999 ** delta; // 根据滚动值调整缩放比例，滚轮每滚动一单位，缩放比例变化0.1%

            if (zoom > 20) zoom = 20; // 限制最大缩放比例为20倍，防止过度放大
            if (zoom < 0.01) zoom = 0.01; // 限制最小缩放比例为0.01倍，防止过度缩小

            // 应用新的缩放比例，以鼠标当前位置为中心进行缩放
            canvas.zoomToPoint({ x: opt.e.offsetX, y: opt.e.offsetY }, zoom);

            // 禁用图像平滑处理，保持像素点清晰
            canvas.imageSmoothingEnabled = false;

            opt.e.preventDefault(); // 阻止默认的滚轮滚动行为，避免滚动画布时页面也跟着滚动
            opt.e.stopPropagation(); // 阻止事件冒泡，避免滚轮事件影响到其他元素
            drawCrosshair(crosshairPosition); // 重新绘制十字线
            });
        }










        // 这个函数的作用是启用画布的拖动功能并在拖动时禁用绘制功能
        function enableDraggingAndDisableDrawing() {
            var isDragging = false; // 定义一个标志，用于判断用户是否正在拖动画布
            var isMouseDown = false; // 定义一个标志，用于判断鼠标是否按下
            var lastPosX = 0; // 记录上一次鼠标的X位置
            var lastPosY = 0; // 记录上一次鼠标的Y位置

            // 监听键盘按下事件
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Alt') { // 如果按下的是Alt键
                    e.preventDefault(); // 防止默认行为
                    canvas.isDrawingMode = false; // 禁用画布的绘制模式
                    isDragging = true; // 启动拖动模式
                }
            });

            // 监听鼠标按下事件
            canvas.on('mouse:down', function(opt) {
                var e = opt.e;
                isMouseDown = true; // 设置鼠标按下标志为true
                lastPosX = e.clientX;
                lastPosY = e.clientY;
            });

            // 监听鼠标移动事件
            canvas.on('mouse:move', function(opt) {
                if (document.hasFocus() === false) {//鼠标在网页上移动的时候。如果窗口没有焦点，则聚焦窗口
                    window.focus();}
                var pointer = canvas.getPointer(opt.e);
                lastMouseX = pointer.x;
                lastMouseY = pointer.y;
                if (isDragging && isMouseDown) { // 只有当处于拖动模式并且鼠标按下时才处理拖动
                    var e = opt.e;
                    var vpt = canvas.viewportTransform;
                    vpt[4] += e.clientX - lastPosX;
                    vpt[5] += e.clientY - lastPosY;
                    canvas.requestRenderAll();
                    lastPosX = e.clientX;
                    lastPosY = e.clientY;
                }
            });

            // 监听鼠标释放事件
            canvas.on('mouse:up', function(opt) {
                isMouseDown = false; // 设置鼠标按下标志为false
            });

            // 监听键盘松开事件
            document.addEventListener('keyup', function(e) {
                if (e.key === 'Alt') { // 如果松开的是Alt键
                    canvas.isDrawingMode = false; // 恢复画布的绘制模式
                    isDragging = false; // 结束拖动模式
                    drawCrosshair(crosshairPosition); // 重新绘制十字线
                }
            });
        }


        // 监听键盘按下事件
        document.addEventListener('keydown', function(event) {
            if (event.keyCode === 32 && CalibrationFlagPosition === true) { // 检查是否按下了空格键
                event.preventDefault(); // 防止空格键的默认行为（例如滚动页面）
                // 使用鼠标的最后位置调用函数
                sendCorrectionCoordinatesToPython(lastMouseX, lastMouseY);
            }
        });


        function toggleNightMode(forceNightMode = null) {
            const isNightMode = document.body.classList.contains('night-mode');
            if (forceNightMode !== null) {
                if (forceNightMode && !isNightMode) {
                    document.documentElement.classList.add('night-mode');
                    document.body.classList.add('night-mode');
                } else if (!forceNightMode && isNightMode) {
                    document.documentElement.classList.remove('night-mode');
                    document.body.classList.remove('night-mode');
                }
            } else {
                document.documentElement.classList.toggle('night-mode');
                document.body.classList.toggle('night-mode');
            }
        }
            
        
        toggleNightMode(Nightmode);
        

        enableDraggingAndDisableDrawing();
        enableZoom();
        setBackgroundImage(base64Image, canvas)
    </script>
</html>
"""


base64pictempdata = """
data:image/png;base64,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
"""

WeatherIconMoon = """
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Uk0AAHomAACAhAAA+gAAAIDoAAB1MAAA6mAAADqYAAAXcJy6UTwAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAXJaVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/PiA8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJBZG9iZSBYTVAgQ29yZSA5LjEtYzAwMiA3OS5hNmE2Mzk2LCAyMDI0LzAzLzEyLTA3OjQ4OjIzICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjUuOSAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDI0LTA3LTE5VDE2OjM0OjI2KzA4OjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyNC0wNy0xOVQxNjozOTowOCswODowMCIgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyNC0wNy0xOVQxNjozOTowOCswODowMCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6Njk2ZGU3M2MtOGRmZS1kYzRhLWIxMWYtMTZkZTNjNThlZmI3IiB4bXBNTTpEb2N1bWVu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
"""

WeatherIconSnowy = """
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Uk0AAHomAACAhAAA+gAAAIDoAAB1MAAA6mAAADqYAAAXcJy6UTwAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAXJaVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/PiA8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJBZG9iZSBYTVAgQ29yZSA5LjEtYzAwMiA3OS5hNmE2Mzk2LCAyMDI0LzAzLzEyLTA3OjQ4OjIzICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjUuOSAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDI0LTA3LTE5VDE2OjM0OjI2KzA4OjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyNC0wNy0xOVQxNjo0MTozMCswODowMCIgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyNC0wNy0xOVQxNjo0MTozMCswODowMCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6ZDBkYWEyZmMtYjE5Mi0yNzRjLWIyODktNTQ4MWNhYzM0OTE4IiB4bXBNTTpEb2N1bWVu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
"""

WeatherIconSun = """
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Uk0AAHomAACAhAAA+gAAAIDoAAB1MAAA6mAAADqYAAAXcJy6UTwAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAXJaVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/PiA8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJBZG9iZSBYTVAgQ29yZSA5LjEtYzAwMiA3OS5hNmE2Mzk2LCAyMDI0LzAzLzEyLTA3OjQ4OjIzICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjUuOSAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDI0LTA3LTE5VDE2OjM0OjI2KzA4OjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyNC0wNy0xOVQxNjozODozMiswODowMCIgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyNC0wNy0xOVQxNjozODozMiswODowMCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6ZTc0ZjcwZmYtYjJhNy1jZDQwLTg4ZjMtY2YxYWNhODQ2NDE5IiB4bXBNTTpEb2N1bWVu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
"""

WeatherIconThunderstorm = """
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Uk0AAHomAACAhAAA+gAAAIDoAAB1MAAA6mAAADqYAAAXcJy6UTwAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAXJaVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/PiA8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJBZG9iZSBYTVAgQ29yZSA5LjEtYzAwMiA3OS5hNmE2Mzk2LCAyMDI0LzAzLzEyLTA3OjQ4OjIzICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjUuOSAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDI0LTA3LTE5VDE2OjM0OjI2KzA4OjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyNC0wNy0xOVQxNjo0MDoyMCswODowMCIgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyNC0wNy0xOVQxNjo0MDoyMCswODowMCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6OGNjMWRhMWMtNjkxMC1lZjQ5LTkwNTYtN2ViZWE2YmQ1OWExIiB4bXBNTTpEb2N1bWVu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
"""

class CustomFlyoutView(FlyoutViewBase):
    """
    浮出帮助的自定义视图
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.TextEdit = TextEdit()
        # 检查当前目录下是否存在readme.md文件
        if os.path.exists('README.md'):
            # 如果存在，读取并使用readme.md的内容
            with open('README.md', 'r', encoding='utf-8') as file:
                软件说明 = file.read()
        else:
            软件说明 = Documentation
        self.TextEdit.setMarkdown(软件说明)
        self.TextEdit.setFixedSize(900, 600)
        颜文字 = ["(⁎⁍̴̛ᴗ⁍̴̛⁎)", "╰(✿´⌣`✿)╯♡", "(๑•́ ₃ •̀๑)ｴｰ", "(๑ơ ₃ ơ)♥", "(๑¯ω¯๑)", "(ง •̀_•́)ง‼", "٩(๑`^´๑)۶", "٩(๑òωó๑)۶", "(⌒ω⌒)", "( ◠‿◠ )", "٩(๑˃̵ᴗ˂̵๑)۶", "ʕ•̀ω•́ʔ✧", "(•ө•)♡", "( つ•̀ω•́)つ", "( ๑॔˃̶◡ ˂̶๑॓)◞♡", "( ó × ò)", "( ๑͒･(ｴ)･๑͒)", "꒰ ๑͒ ･౪･๑͒꒱", "꒰ ๑͒ óｪò๑͒꒱", "σ(o’ω’o)", "(๑•́ ₃ •̀๑)/", "(･’ω’･)", "(｡◕ ∀ ◕｡)", "╲(｡◕‿◕｡)╱", "(´｡✪ω✪｡｀)", "(✿╹◡╹)", "(* Ŏ∀Ŏ)", "(๑◔‿◔๑)", "(<em>δωδ</em>)」", "(･◡ु‹ )", "٩(๑òωó๑)۶", "(灬╹ω╹灬)", "•ू(ᵒ̴̶̷ωᵒ̴̶̷*•ू)", "( ๑˃̶ ॣꇴ ॣ˂̶)♪⁺", "(๑˃̵ᴗ˂̵)و ﾖｼ!", "(<em>´◒`</em>)", "(๑･㉨･๑)", "(｡╹ω╹｡)", "(<em>｀益´</em>)がう", "٩( ╹▿╹ )۶", "(◍´ಲ`◍)", "(●´ϖ`●)", "(◍<em>3</em>◍)", "(●♡ᴗ♡●)", "(◍╹ｘ╹◍)", "(●☌◡☌●)", "(●･̆⍛･̆●)", "(◕̻͠◸◕̻͠)", "ฅ ̳͒•ˑ̫• ̳͒ฅ♡", "චᆽච", "༶ඬ༝ඬ༶", "ოර⌄රო", "⁙ὸ‿ό⁙", "(,,◕ ⋏ ◕,,)", "(..＞◡＜..)", "(,,Ծ‸Ծ,, )", "(❍ᴥ❍ʋ)", "( ͡° ᴥ ͡° ʋ)", "V●ω●V", "V✪ω✪V", "V✪⋏✪V", "∪ ̿–⋏ ̿–∪", "∪･ω･∪", "໒( ●ܫฺ ●)ʋ", "໒( = ᴥ =)ʋ", "໒( ̿･ ᴥ ̿･ )ʋ", "໒( ̿❍ ᴥ ̿❍)ʋ", "▽･ｪ･▽ﾉ”", "ଘ(∪・ﻌ・∪)ଓ", "∪◕ฺᴥ◕ฺ∪", "໒(＾ᴥ＾)७", "ฅU=ﻌ =Uฅ", "ᐡ ・ ﻌ ・ ᐡ", "ᐡ ᐧ ﻌ ᐧ ᐡ", "(*´_ゝ｀)", "(<em>´∀`</em>)", "(<em>´ｪ｀</em>)", "｡(<em>^▽^</em>)ゞ", "(‘-’*)", "(<em>´∀`</em>)", "(<em>^^</em>)", "(*ﾟｰﾟ)ゞ", "(ノ<em>゜▽゜</em>)", "ฅ(<em>°ω°</em>ฅ)", "(<em>ﾟ∀ﾟ</em>)", "(<em>´ω｀</em>)", "(´ω｀*)", "(⁎❝᷀ົ ˙̫ ❝᷀ົ⁎)", "ε=ε=ε=ε=ε” “(/<em>’-‘</em>)/", "ヽ(＊&gt;∇&lt;)ﾉ", "(<em>´-｀</em>)", "( <em>’ω’</em> )", "( <em>∵</em> )", "<em>:ﾟ</em>｡⋆ฺ(*´◡`)", "(#^.^#)", "(#｀ε´# )ゞ", "(＃⌒∇⌒＃)ゞ", "꒰⌗´͈ ᵕ ॣ`͈⌗꒱৩", "(#ﾟﾛﾟ#)", "꒰#’ω`#꒱੭", "(#^^#)ゞ", "(๑•́ ω •̀๑)", "⁝(๑⑈௰⑈)◞⁝˚º꒰꒱", "(๑•́ ₃ •̀๑)", "(๑ˊ▵ॢˋ̥๑)", "(๑´ㅂ`๑)", "(๑ゝω╹๑)", "(´๑•_•๑)", "(๑•́ω•̀๑)", "(๑⃙⃘·́ω·̀๑⃙⃘)੨", "(◞ ๑⑈௰⑈)", "(๑´ω`๑)", "(๑癶ω癶๑)", "(´•ω•`๑)", "(๑´•ω • `๑)", "(_๑˘ㅂ˘๑)", "(๑´⍢`๑)", "(๑′°︿°๑)", "(๑́•∀•๑̀)ฅ", "(๑ּగ⌄ּగ๑)", "(⁶ੌ௰⁶ੌ๑)", "(๑꒪̇⌄꒪̇๑)", "(๑꒪⍘꒪๑)", "(๑⁍᷄౪⁍᷅๑)", "Σ(๑꒪⃙⃚᷄ꑣ꒪⃚⃙᷅๑۶)۶", "(๑￫‿￩๑)", "(๑•́‧̫•̀๑)", "(๑･▱･๑)", "(͡o‿O͡)", "( ͡°³ ͡°)", "( ͡°⊖ ͡°)", "( ͡°Ɛ ͡°)", "( ͡°з ͡°)", "( ͡°- ͡°)", "( ͡°⊱ ͡°)", "( ͡°❥ ͡°)", "( ͡°ω ͡°)", "(ง⌐□ل͜□)ง", "( ͡°〓 ͡°)", "( ͡°👅 ͡°)", "(͡• ͜ʖ ͡•)", "( ͡° ͜ ͡°)", "( ͡° ᴥ ͡°)", "(͡• ͜໒ ͡• )", "( ͡◉ ͜ʖ ͡◉)", "( ͡° ͜V ͡°)", "( ͡• ͜ʖ ͡• )", "ヽ(͡◕ ͜ʖ ͡◕)ﾉ", "(◕ᴗ◕✿)", "(◕◡◕✿)", "(◔◡◔✿)", "(｡◕‿◕｡✿)", "(◡‿◡✿)", "(◠‿◠✿)", "(◕ܫ◕✿)", "(◕▿◕✿)", "(◕ ワ ◕✿)"]
        # 从列表中随机选择一个颜文字
        选中的颜文字 = random.choice(颜文字)
        self.button = PrimaryPushButton(选中的颜文字)
        def change_button_text():
            # 从颜文字列表中随机选择一个并设置为按钮的文字
            self.button.setText(random.choice(颜文字))
        self.button.clicked.connect(change_button_text)

        self.button.setFixedWidth(140)
        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.setContentsMargins(20, 16, 20, 16)
        self.vBoxLayout.addWidget(self.TextEdit)

        # 创建水平布局用于按钮
        hBoxLayout = QHBoxLayout()
        hBoxLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        hBoxLayout.addWidget(self.button)
        hBoxLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # 将水平布局添加到垂直布局中
        self.vBoxLayout.addLayout(hBoxLayout)

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

class DictTableWidget(QWidget):
    """
    自定义控件，用于展示和编辑原始字典数据。
    
    参数:
    original_dict: 原始字典，用于初始化数据。如果是字符串，将从父控件中获取对应属性。如果不是字符串，直接使用。
    contextstr: 控件的上下文说明字符串。
    parent: 父控件，默认为None。
    parentup: 搜寻原始字典储存的父=控件类，用于更新原始字典，默认为None。
    colorselect: 是否启用颜色选择器，默认为False。使用颜色选择器的话，表格里值的部分将会是颜色选择器按钮，效果一样。
    """
    
    def __init__(self, original_dict, contextstr, parent=None ,parentup=None, colorselect = False):
        super().__init__(parent)
        
        self.parentup = parentup
        self.original_dict_notuse = original_dict
        self.colorselect = colorselect

        if isinstance(original_dict, str) and not hasattr(parentup, original_dict):
            logger.error(f'父控件中没有属性 {original_dict}，肯定哪里输错了，建议重输。')
        
        # 初始化原始字典和数据字典
        # 从parent类里面获取cfgobjextstr名字的属性
        self.objectflag = False
        if parent:
            if isinstance(original_dict, str) and hasattr(parentup, original_dict):
                logger.info(f'从父控件中获取了属性 {original_dict}')
                self.original_dict = getattr(parentup, original_dict)
                logger.info(f'从父控件中获取了属性 {original_dict}，值为 {self.original_dict}')
                self.objectflag = True
            else:
                self.original_dict = original_dict
        else:
            self.original_dict = {}
        self.data_dict = {}  # 初始化空字典，稍后将转换
        # 转换原始数据到字典格式
        self.convert_original_to_dict()
        # 初始化表格项变更的槽函数
        self.item_changed_slot = None  # 保存 itemChanged 信号连接的槽函数对象
        
        # 初始化表格
        self.table = TableWidget()
        self.table.setColumnCount(4)  # 设置列数为4
        self.table.verticalHeader().setVisible(False)  # 不显示垂直表头
        self.table.setHorizontalHeaderLabels(['序号', '键', '值', '操作'])  # 设置表头标签
        self.update_table(self.data_dict)  # 初始化表格数据
        
        # 初始化说明标签
        self.label = BodyLabel(contextstr)
        self.label.setAlignment(Qt.AlignCenter)  # 设置文字居中
        
        # 初始化添加行按钮，并连接点击事件
        button_layout = QHBoxLayout()
        self.add_row_button = PrimaryPushButton('添加行')
        self.add_row_button.clicked.connect(self.add_new_row)
        button_layout.addWidget(self.add_row_button)
        
        # 组合布局
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(button_layout)
        self.main_layout.addWidget(self.table)
        
        # 设置控件布局
        self.setLayout(self.main_layout)

        # 调整窗口高度
        self.adjust_height()

    def adjust_height(self):
        total_height = self.calculate_total_height() + 15 # 不知道为什么，获取的高度不足以显示完整，所以加了60
        self.setFixedHeight(total_height)

    def calculate_total_height(self):
        total_height = 0
        # 遍历布局中的所有控件
        for i in range(self.main_layout.count()):
            item = self.main_layout.itemAt(i)
            widget = item.widget() if item else None
            if widget:  # 确保是控件
                # 检查控件是否为表格
                if isinstance(widget, QTableWidget):
                    # 计算表格的总高度，包括所有行和表头
                    table_height = widget.horizontalHeader().height()  # 表头高度
                    for row in range(widget.rowCount()):
                        table_height += widget.rowHeight(row)  # 累加每一行的高度
                    if widget.horizontalScrollBar().isVisible():  # 如果水平滚动条可见
                        table_height += widget.horizontalScrollBar().height()  # 添加滚动条的高度
                    total_height += table_height
                else:
                    total_height += widget.sizeHint().height() + 20
        
        # 获取布局的间距和边距
        spacing = self.main_layout.spacing()
        margins = self.main_layout.contentsMargins()
        # 计算总高度，包括间距和上下边距
        total_height += (self.main_layout.count() - 1) * spacing  # 控件间的间距
        total_height += margins.top() + margins.bottom()  # 上下边距
        
        return total_height
    
    def convert_original_to_dict(self):
        # 将self.original_dict 转换为 self.data_dict 的形式
        self.data_dict.clear()  # 清空 self.data_dict
        for idx, (key, value) in enumerate(self.original_dict.items(), start=1):
            self.data_dict[idx] = {'key': key, 'value': value}
    
    
    def update_table(self, data_dict):
        self.table.clearContents()
        self.table.setRowCount(len(data_dict))  # 设置行数为字典长度
        
        # 断开之前的信号连接
        if self.item_changed_slot:
            self.table.itemChanged.disconnect(self.item_changed_slot)
        
        for row, (index, item) in enumerate(sorted(data_dict.items())):
            index_item = QTableWidgetItem(str(index))
            index_item.setTextAlignment(Qt.AlignCenter)  # 第一列居中对齐
            self.table.setItem(row, 0, index_item)  # 第一列是序号
            
            key_item = QTableWidgetItem(item['key'])
            key_item.setTextAlignment(Qt.AlignCenter)  # 第二列居中对齐
            self.table.setItem(row, 1, key_item)  # 第二列是键
            
            if self.colorselect:
                # 在for循环中，创建ColorPickerButton后
                color_button = ColorPickerButton(QColor(item['value']), item['value'], self, enableAlpha=False)
                color_button.colorChanged.connect(lambda color, idx=index: self.update_color(idx, color))

                # 创建一个QWidget作为容器
                widget = QWidget()
                # 创建一个水平布局
                layout = QHBoxLayout()
                # 将布局的对齐方式设置为居中
                layout.setAlignment(Qt.AlignCenter)
                # 将按钮添加到布局中
                layout.addWidget(color_button)
                # 将布局设置到QWidget容器中
                widget.setLayout(layout)

                # 将QWidget容器（现在包含按钮）设置为单元格的小部件
                self.table.setCellWidget(row, 2, widget)
            else:
                value_item = QTableWidgetItem(item['value'])
                value_item.setTextAlignment(Qt.AlignCenter)  # 第三列居中对齐
                self.table.setItem(row, 2, value_item)  # 第三列是值
            
            # 添加删除按钮到最后一列
            delete_button = TransparentPushButton(FIF.DELETE,"删除")
            delete_button.clicked.connect(lambda _, idx=index: self.delete_row(idx))
            self.table.setCellWidget(row, 3, delete_button)

        # 清除表格选中状态
        self.table.clearSelection()
        # 连接信号
        self.item_changed_slot = self.table.itemChanged.connect(self.update_dict_from_table)
    
    

    # 处理颜色改变信号
    def update_color(self, index, color):
        key = self.data_dict[index]['key']
        new_value = color.name()

        # 检查是否有重复的颜色
        for idx, item in self.data_dict.items():
            if idx != index and item['value'] == new_value:
                self.parentup.显示消息框函数("error", "警告", "已存在相同的颜色，请修改后再保存。", "右下", 5000)
                # 恢复原来的颜色
                current_color = QColor(item['value'])
                self.table.cellWidget(idx - 1, 2).setColor(current_color)
                return

        # 更新self.data_dict中的值
        self.data_dict[index]['value'] = new_value

        # 更新self.original_dict中对应的值
        self.original_dict[key] = new_value
        if self.objectflag:
            setattr(self.parentup, self.original_dict_notuse, self.original_dict)

        logger.info(f'更新原始字典中键 {key} 的颜色值为 {new_value}')
        logger.info(f'当前字典内容：{self.original_dict}')


    # 删除特定行
    def delete_row(self, index):
        if index not in self.data_dict:
            logger.error(f'试图删除无效索引 {index}')
            return
        logger.info(f'删除序号为 {index} 的行')
        del_key = self.data_dict[index]['key']
        logger.info(f'删除的键为 {del_key}')
        logger.info(f'删除的对象为 {self.data_dict[index]}')
        del_value = self.data_dict[index]['value']
        
        del self.data_dict[index]
        
        # 更新self.original_dict中对应的键值对
        del self.original_dict[del_key]
        logger.debug(f"更新标志位：{self.objectflag}，更新属性名：{self.original_dict_notuse}")
        if self.objectflag:
            setattr(self.parentup, self.original_dict_notuse, self.original_dict)
        
        # 更新表格显示
        self.update_table(self.data_dict.copy())
        self.update_row_indices()  # 更新所有行的序号
        self.update_table(self.data_dict.copy())
        
        
        logger.info(f'从字典中删除了序号为 {index} 的行')
        logger.info(f'当前字典内容：{self.original_dict}')
        logger.info(f'当前表格内容：{self.data_dict}')
    
    # 添加新行，默认内容
    def add_new_row(self):
        """
        向表格中添加新行，并在字典中记录相应的键值对。
        新行的键和值基于已有最大键值加一生成，确保唯一性。
        如果生成的键或值与已有项重复，将提示用户并取消添加。
        """
        self.table.itemChanged.disconnect(self.item_changed_slot)
        # 收集现有行中键的数字部分以确定新行的键值
        existing_indexes = []
        for row in range(self.table.rowCount()):
            # 假设键存储在第一列
            key = self.table.item(row, 1).text()
            # 提取键名中的数字部分
            try:
                index = int(''.join(filter(str.isdigit, key)))
            except ValueError:
                continue
            existing_indexes.append(index)

        logger.info(f'现有键的数字部分：{existing_indexes}')
        
        # 查找不存在于现有键中的最小整数键值
        # 从1开始查找不在existing_indexes中的最小数字
        default_index = 1
        while default_index in existing_indexes:
            default_index += 1
        
        # 根据默认索引生成新的键和值
        default_key = f'key{default_index}'
        default_value = f'value{default_index}'
        if self.colorselect:
            default_value = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)).name()
        
        # 检查新生成的键或值是否已存在于字典中
        # 检查新增的键和值是否已存在
        if any(item['key'] == default_key or item['value'] == default_value for item in self.data_dict.values()):
            self.parentup.显示消息框函数("error","警告","新行的键或值已存在，请将原来的键对应的值修改完再添加。","右下",5000)
            return
        
        # 在字典中添加新的键值对
        self.data_dict[default_index] = {'key': default_key, 'value': default_value}
        
        # 更新self.original_dict中的对应值
        self.original_dict[default_key] = default_value
        logger.debug(f"更新标志位：{self.objectflag}，更新属性名：{self.original_dict_notuse}")
        if self.objectflag:
            setattr(self.parentup, self.original_dict_notuse, self.original_dict)
        
        # 在表格中插入新行并设置相应单元格的值
        self.table.insertRow(self.table.rowCount())
        
        index_item = QTableWidgetItem(str(default_index))
        index_item.setTextAlignment(Qt.AlignCenter)  # 设置序号居中
        self.table.setItem(self.table.rowCount() - 1, 0, index_item)
        
        key_item = QTableWidgetItem(default_key)
        key_item.setTextAlignment(Qt.AlignCenter)  # 设置键居中
        self.table.setItem(self.table.rowCount() - 1, 1, key_item)
        
        # 替换为随机颜色的按钮
        if self.colorselect:
            # 生成随机颜色按钮
            color_button = ColorPickerButton(default_value, default_value, self, enableAlpha=False)
            color_button.colorChanged.connect(lambda color, idx=index: self.update_color(idx, color))

            # 创建一个QWidget作为容器
            widget = QWidget()
            # 创建一个水平布局
            layout = QHBoxLayout()
            # 将布局的对齐方式设置为居中
            layout.setAlignment(Qt.AlignCenter)
            # 将按钮添加到布局中
            layout.addWidget(color_button)
            # 将布局设置到QWidget容器中
            widget.setLayout(layout)

            # 将QWidget容器（现在包含按钮）设置为单元格的小部件
            self.table.setCellWidget(self.table.rowCount() - 1, 2, widget)
        else:
            value_item = QTableWidgetItem(default_value)
            value_item.setTextAlignment(Qt.AlignCenter)  # 设置值居中
            self.table.setItem(self.table.rowCount() - 1, 2, value_item)
        
        # 在新行的最后列添加删除按钮
        delete_button = TransparentPushButton(FIF.DELETE,"删除")
        delete_button.clicked.connect(lambda _, idx=index: self.delete_row(idx))
        self.table.setCellWidget(self.table.rowCount() - 1, 3, delete_button)

        self.item_changed_slot = self.table.itemChanged.connect(self.update_dict_from_table)

        # 输出添加的新行信息
        logger.info(f'向字典中添加了新行，序号为 {default_index}')
        logger.info(f'当前字典内容：{self.original_dict}')
        
        # 更新表格显示
        self.update_row_indices()  # 更新所有行的序号
        self.update_table(self.data_dict.copy())
        
    # 更新所有行的序号
    def update_row_indices(self):
        self.data_dict.clear()  # 清空原有字典
        for row in range(self.table.rowCount()):
            new_index = row + 1  # 从1开始的序号
            item = QTableWidgetItem(str(new_index))
            item.setTextAlignment(Qt.AlignCenter)  # 设置文本居中
            self.table.setItem(row, 0, item)
            key = self.table.item(row, 1).text()
            # 检查单元格是否有小部件，并且该小部件是否包含布局
            if isinstance(self.table.cellWidget(row, 2), QWidget) and self.table.cellWidget(row, 2).layout() is not None:
                widget = self.table.cellWidget(row, 2)
                layout = widget.layout()
                # 假设ColorPickerButton是布局中的第一个（也可能是唯一一个）小部件
                color_button = layout.itemAt(0).widget()
                if isinstance(color_button, ColorPickerButton):
                    # 从颜色选择按钮获取颜色值
                    color = color_button.color  # 直接对按钮对象.color可以获得对应的pyside6 QColor 对象
                    value = color.name()  # 获取颜色的十六进制字符串
            else:
                value = self.table.item(row, 2).text()
            self.data_dict[new_index] = {'key': key, 'value': value}
        
        logger.info(f'更新所有行的序号，当前字典内容：{self.data_dict}')
    
    # 从表格更新字典内容
    def update_dict_from_table(self, item):
        if item.column() == 1:  # 第二列是键
            row = item.row()
            if row >= len(self.data_dict):
                return
            
            index = int(self.table.item(row, 0).text())
            new_key = item.text()
            
            old_key = self.data_dict[index]['key']
            
            # 检查是否有重复的键
            for key, value in self.data_dict.items():
                if key != index and value['key'] == new_key:
                    self.parentup.显示消息框函数("error","警告","已存在相同的键，请修改后再保存。","右下",5000)
                    item.setText(old_key)  # 恢复原来的值
                    return
            
            # 更新self.data_dict中的键
            self.data_dict[index]['key'] = new_key
            
            # 更新self.original_dict中对应的键值
            del self.original_dict[old_key]
            self.original_dict[new_key] = self.data_dict[index]['value']
            if self.objectflag:
                setattr(self.parentup, self.original_dict_notuse, self.original_dict)
            
            logger.info(f'更新原始字典中键 {old_key} 为 {new_key}，当前内容：{self.original_dict}')
            logger.info(f'更新字典中序号为 {index} 的键为 {new_key}')
        
        elif item.column() == 2:  # 第三列是值
            row = item.row()
            if row >= len(self.data_dict):
                return
            
            index = int(self.table.item(row, 0).text())
            new_value = item.text()
            
            # 检查是否有重复的值
            for key, value in self.data_dict.items():
                if key != index and value['value'] == new_value:
                    self.parentup.显示消息框函数("error","警告","已存在相同的值，请修改后再保存。","右下",5000)
                    item.setText(self.data_dict[index]['value'])  # 恢复原来的值
                    return
            
            # 更新self.data_dict中的值
            self.data_dict[index]['value'] = new_value
            
            # 更新self.original_dict中对应的值
            self.original_dict[self.data_dict[index]['key']] = new_value
            if self.objectflag:
                setattr(self.parentup, self.original_dict_notuse, self.original_dict)
            
            logger.info(f'更新原始字典中键 {self.data_dict[index]["key"]} 的值为 {new_value}，当前内容：{self.original_dict}')
            logger.info(f'更新字典中序号为 {index} 的值为 {new_value}')


    def resizeEvent(self, event):
        # 重写resizeEvent方法以调整列宽
        total_width = self.width() - 20  # 获取QWidget的当前宽度（全满居然会出现滑动条……所以要减掉一点）
        column_width = total_width // 4   # 计算前三列的宽度
        last_column_width = total_width - (column_width * 3)  # 计算最后一列的宽度，以吸收可能的余数

        # 设置前三列的宽度
        for i in range(3):
            self.table.setColumnWidth(i, column_width)
        # 设置最后一列的宽度
        self.table.setColumnWidth(3, last_column_width)

        super().resizeEvent(event)  # 调用父类的resizeEvent方法


# 大佬的ui没法实现进度条类，我只能自己写一个，哎，写了好多
class ProgressFlyoutView(FlyoutViewBase):
    def __init__(self, parent=None, startfunc=None, pausefunc=None, finishfunc=None):
        super().__init__(parent)
        self.startfunc = startfunc  # 开始按钮的回调函数
        self.pausefunc = pausefunc  # 暂停按钮的回调函数
        self.finishfunc = finishfunc  # 结束按钮的回调函数
        self.start_time = None  # 记录开始时间
        self.elapsed_time = timedelta()  # 记录已消耗时间
        self.timer = QTimer()  # 定时器用于更新时间
        self.timer.timeout.connect(self.update_time)  # 连接定时器的超时信号到更新时间的槽函数
        self.files_processed = 0  # 已处理文件数
        self.start_processing_time = None  # 记录处理开始时间
        self.totle_files = 100  # 总文件数
        self.now_filename = "待加载"  # 当前文件名
        self.progress_exist = True  # 进度条是否存在
        self.keynote = ""
        self.Oprah = ""
        self.labelstart = "批处理开始"
        self.labelpaus_stop = "批处理暂停"
        self.labelpaus_restart = "批处理继续"
        self.labelfinish = "批处理已结束"
        self.beforestart = "这里将会显示进度信息"

        # 垂直布局
        self.vBoxLayout = QVBoxLayout(self)

        # 文字信息标签
        self.label = BodyLabel(self.beforestart)
        self.label.setAlignment(Qt.AlignCenter)  # 设置文本居中
        self.vBoxLayout.addWidget(self.label)

        # 进度条
        self.progressBar = ProgressBar()
        self.progressBar.setRange(0, self.totle_files)
        self.vBoxLayout.addWidget(self.progressBar)

        # 横向布局用于按钮
        hBoxLayout = QHBoxLayout()

        # 添加按钮
        self.startButton = PushButton("开始")
        self.pauseButton = PushButton("暂停")
        self.resetButton = PushButton("终止")

        # 在按钮两侧添加弹性空间
        hBoxLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        hBoxLayout.addWidget(self.startButton)
        hBoxLayout.addWidget(self.pauseButton)
        hBoxLayout.addWidget(self.resetButton)
        hBoxLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # 将按钮布局添加到垂直布局
        self.vBoxLayout.addLayout(hBoxLayout)

        # 设置默认大小
        self.setFixedSize(500, 250)

        # 连接按钮信号到槽函数
        self.startButton.clicked.connect(self.start_progress)
        self.pauseButton.clicked.connect(self.pause_or_resume_progress)
        self.resetButton.clicked.connect(self.reset_progress)

    def start_progress(self):
        # 处理开始进度
        self.progress_exist = True  # 进度条是否存在
        self.progressBar.setValue(0)  # 设置进度条初始值为0
        self.label.setText(self.labelstart)  # 更新标签文本
        self.start_time = datetime.now()  # 记录开始时间
        self.start_processing_time = self.start_time  # 记录处理开始时间
        self.timer.start(1000)  # 每秒更新一次
        self.startButton.hide()  # 隐藏开始按钮
        if self.startfunc:
            logger.info("开始调用批处理函数")
            self.startfunc()  # 调用开始回调函数

    def pause_or_resume_progress(self):
        if self.timer.isActive():
            # 暂停进度
            self.label.setText(self.labelpaus_stop)  # 更新标签文本
            self.elapsed_time += datetime.now() - self.start_time  # 更新已消耗时间
            self.timer.stop()  # 停止定时器
            self.pauseButton.setText("继续")  # 更新按钮文本
            if self.pausefunc:
                self.pausefunc(False)  # 调用暂停回调函数
        else:
            # 恢复进度
            self.label.setText(self.labelpaus_restart)  # 更新标签文本
            self.start_time = datetime.now()  # 重新记录开始时间
            self.timer.start(1000)  # 重新启动定时器
            self.pauseButton.setText("暂停")  # 更新按钮文本
            if self.pausefunc:
                self.pausefunc(True)  # 调用暂停回调函数

    def reset_progress(self):
        # 处理重置进度
        self.progressBar.setValue(0)  # 重置进度条
        self.label.setText(self.labelfinish)  # 更新标签文本
        self.timer.stop()  # 停止定时器
        self.start_time = None  # 重置开始时间
        self.elapsed_time = timedelta()  # 重置已消耗时间
        self.pauseButton.setText("暂停")  # 恢复暂停按钮文本
        self.progress_exist = False  # 进度条不存在
        self.startButton.show()
        if self.finishfunc:
            self.finishfunc()  # 调用结束回调函数

    def update_time(self):
        if self.start_time:
            current_time = datetime.now()  # 获取当前时间
            self.elapsed_time += current_time - self.start_time  # 更新已消耗时间
            self.start_time = current_time  # 重新记录开始时间
            self.update_label_info()  # 更新标签信息

    def update_label_info(self):
        if self.totle_files  <= self.files_processed:
            self.progress_exist = False
            self.timer.stop()
            self.label.setText("批处理已结束")  # 更新标签文本
            self.reset_progress()

        if self.files_processed > 0 and self.start_processing_time:
            # 计算平均每个文件处理时间
            total_processing_time = datetime.now() - self.start_processing_time
            avg_time_per_file = total_processing_time.total_seconds() / self.files_processed
        else:
            avg_time_per_file = 0

        self.progressBar.setValue(self.files_processed)
        remaining_files = self.totle_files - self.files_processed  # 计算剩余文件数量

        if avg_time_per_file > 0:
            remaining_time = remaining_files * avg_time_per_file  # 计算剩余时间
            estimated_completion_time = datetime.now() + timedelta(seconds=remaining_time)  # 计算预计完成时间
            estimated_completion_time_str = estimated_completion_time.strftime("%Y-%m-%d %H:%M:%S")  # 将预计完成时间格式化为字符串
        else:
            remaining_time = 0
            estimated_completion_time_str = "未知"

        def format_time(days, hours, minutes, seconds):
            """格式化时间，忽略值为0的部分"""
            parts = []
            if days > 0:
                parts.append(f"{days}天")
            if hours > 0:
                parts.append(f"{hours}小时")
            if minutes > 0:
                parts.append(f"{minutes}分钟")
            if seconds > 0:
                parts.append(f"{seconds}秒")
            return " ".join(parts) if parts else "0秒"

        # 假设remaining_time是剩余时间的秒数
        remaining_time_seconds = remaining_time  # 从你的代码或计算中获取剩余秒数

        # 创建timedelta对象
        td = timedelta(seconds=remaining_time_seconds)

        # 获取天数、小时数、分钟数、秒数
        days = td.days
        hours = td.seconds // 3600
        minutes = (td.seconds % 3600) // 60
        seconds = (td.seconds % 3600) % 60

        # 格式化预计剩余时间
        formatted_remaining_time = format_time(days, hours, minutes, seconds)

        # 假设elapsed_time和avg_time_per_file是已经计算好的值
        # 例如:
        # elapsed_time = 12345  # 已消耗时间的秒数
        # avg_time_per_file = 123  # 平均每个文件消耗时间的秒数

        # 格式化已消耗时间和平均每个文件消耗时间
        elapsed_td = self.elapsed_time
        avg_td = timedelta(seconds=avg_time_per_file)

        formatted_elapsed_time = format_time(elapsed_td.days, elapsed_td.seconds // 3600, (elapsed_td.seconds % 3600) // 60, (elapsed_td.seconds % 3600) % 60)
        formatted_avg_time_per_file = format_time(avg_td.days, avg_td.seconds // 3600, (avg_td.seconds % 3600) // 60, (avg_td.seconds % 3600) % 60)

        self.label.setText(
            f"{self.keynote}\n"
            f"当前运行的操作：{self.Oprah}\n"
            f"总共文件数：{self.totle_files}\n"  # 显示总文件数
            f"当前操作的文件名：{self.now_filename}\n"  # 当前文件名
            f"已处理文件数：{self.files_processed}\n"  # 已处理文件数
            f"已消耗时间：{formatted_elapsed_time}\n"  # 已消耗时间
            f"平均每个文件消耗时间：{formatted_avg_time_per_file}\n"  # 平均每个文件消耗时间
            f"预计还需要处理多久：{formatted_remaining_time}\n"  # 预计剩余时间
            f"预计完成时间：{estimated_completion_time_str}"  # 预计完成时间
        )

    def set_files_processed(self, files_processed, now_filename):
        # 设置已处理文件数
        self.progressBar.setRange(0, self.totle_files)
        self.files_processed = files_processed
        self.now_filename = now_filename
        self.update_label_info()  # 更新进度信息


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
        self.clearmask.setText(QCoreApplication.translate("Dialog", "取消遮罩部分", None))


class CustomWebEnginePage(QWebEnginePage):
    """
    自定义的WebEnginePage类，用于处理JavaScript的输出
    """
    def __init__(self, parent = None, object1 = ""):
        super().__init__(parent)
        self.object1 = object1
    
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        logger.info(f"{self.object1}Console: {message} 【line: {lineNumber}】")



class Bridge(QObject):
    """
    定义一个Bridge类，用于处理Python和JavaScript之间的通信
    """
    # 定义一个信号，用于向JavaScript发送数据
    sendListToJS = Signal(list)
    sendCanvasPositionToJS = Signal(list)
    sendChunkToJS = Signal(str, int, int)  # 发送数据块信号
    sendBase64ToJS = Signal(str)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui  # 把主函数窗口传过来，方便调用主循环函数类里面的函数和变量
        self.校准变量 = 0

    def 鼠标坐标转换函数(self, x, y):
        if self.ui.是否使用极坐标:
            # 输入参数r是半径，theta是角度（从负Y轴开始计算，顺时针方向，单位为度）
            r = x*self.ui.api.半径偏移倍率
            theta = y

            # 将角度转换为弧度
            theta_radians = math.radians(theta)

            # 设置x1, y1为极坐标
            x1 = r*math.cos(theta_radians) + self.ui.api.圆心基础X坐标 + self.ui.api.圆心偏移X坐标 # 这里的x1是半径
            y1 = r*math.sin(theta_radians) + self.ui.api.圆心基础Y坐标 + self.ui.api.圆心偏移Y坐标 # 这里的y1是角度

            logger.info(f"极坐标转换后的坐标为：({x}, {y})，半径偏移倍率为：{self.ui.api.半径偏移倍率}，圆心偏移X坐标为：{self.ui.api.圆心偏移X坐标}，圆心偏移Y坐标为：{self.ui.api.圆心偏移Y坐标}")
            return x1, y1
        else:
            x = int(x*self.ui.api.X坐标偏移倍率 + self.ui.api.X坐标基础值)
            y = int(y*self.ui.api.Y坐标偏移倍率 + self.ui.api.Y坐标基础值)
            return x, y


    # 接收来自painter的鼠标位置列表
    @Slot(list)
    def receiveListFromJS(self, jsList):
        #logger.info(f"Received list from JS: {jsList}")
        if jsList and isinstance(jsList[0], (int, float)):
            x2,y2 = self.鼠标坐标转换函数(jsList[0], jsList[1])
            if self.ui.是否使用极坐标:
                # 假设jsList[0]是半径，jsList[1]是角度（从负Y轴向左边开始计算，顺时针）-我也不知道为什么实际给出的值是顺时针的
                r = jsList[0]
                theta = jsList[1]

                # 将角度转换为弧度
                theta_radians = math.radians(theta)

                # 设置x1, y1为极坐标
                x1 = r*math.cos(theta_radians) + self.ui.api.圆心基础X坐标 # 这里的x1是半径
                y1 = r*math.sin(theta_radians) + self.ui.api.圆心基础Y坐标 # 这里的y1是角度
                logger.info(f"遮罩极坐标转换后的坐标为：({x1}, {y1})")
            else:
                x1 = jsList[0]
                y1 = jsList[1]
            self.requestListFromPython([x2, y2,x1, y1])
        else:
            pass
        # 处理接收到的列表...

    # 接收来自painter的画布位置列表
    @Slot(list)
    def receivePositionFromJs(self, jsList):
        logger.info(f"接收到来自js的画布位置列表为{jsList}")
        x2,y2 = self.鼠标坐标转换函数(jsList[1], jsList[2])
        zoom = jsList[0] # 缩放比例
        # 下面这个if else是给遮罩准备的
        if self.ui.是否使用极坐标:
            # 假设jsList[0]是半径，jsList[1]是角度（从负Y轴向左边开始计算，顺时针）-我也不知道为什么实际给出的值是顺时针的
            r = jsList[1]
            theta = jsList[2]
            # 将角度转换为弧度
            theta_radians = math.radians(theta)
            # 设置x1, y1为极坐标
            x1 = round(r*math.cos(theta_radians) + self.ui.api.圆心基础X坐标) # 这里的x1是半径
            y1 = round(r*math.sin(theta_radians) + self.ui.api.圆心基础Y坐标) # 这里的y1是角度
            logger.info(f"遮罩极坐标转换后的坐标为：({x1}, {y1})")
            # 发送给painter的是半径和角度
            self.requestCanvasPositionFromPython([zoom, self.ui.api.极坐标基础半径* 2 ,self.ui.api.极坐标基础半径* 2, x2, y2,x1, y1])
        else:
            x1 = round(float(jsList[1]))
            y1 = round(float(jsList[2]))
            self.requestCanvasPositionFromPython([zoom, self.ui.api.直角坐标基础宽度 ,self.ui.api.直角坐标基础高度, x2, y2,x1, y1])

    # 接收来自painter的遮罩数组
    @Slot(str)
    def receiveMuskArrayFromJS(self, base64Data):
        logger.info("接收到来自js的遮罩数组")

        # def process_data(apiobject, data):
        try:
                
            # 解码 Base64 数据
            compressed_data = base64.b64decode(base64Data)

            # 解压缩数据
            decompressed_data = gzip.decompress(compressed_data)

            # 将解压后的数据转换为 numpy 数组
            numpy_array = np.array(json.loads(decompressed_data.decode('utf-8')))

            # 检查 numpy 数组的形状
            if numpy_array.shape[0] == 500 and numpy_array.shape[1] == 500:
                logger.info("接收到来自js的遮罩数组然后发送给painter")
                self.requestMuskArrayFromPython()
                return

            logger.info(f"接收到来自js的遮罩数组，数组的形状为：{numpy_array.shape}")

            # 预处理 numpy 数组
            numpy_array = self.数组输入输出之前的预处理(numpy_array, False)

            # 更新本地数据
            self.ui.api.从webengineview的遮罩更新本地数据(numpy_array, self.ui.api.是否需要规整数据)

            # 显示遮罩流程
            if self.ui.api.是否每绘制一步都刷新遮罩:
                logger.info("开始显示遮罩流程")
                self.ui.api.显示遮罩流程()

        except Exception as e:
            if self.ui.api.是否需要完整报错信息:
                logger.error(f"处理接收数据时发生错误: {e}")
                logger.error(traceback.format_exc())
            else:
                logger.error(f"处理接收数据时发生错误: {e}")

        # # 启动新线程来处理数据
        # thread = threading.Thread(target=process_data, args=(self.ui.api,base64Data))
        # thread.start()

    # 鼠标位置用着函数发送给其他图
    @Slot()
    def requestListFromPython(self, pythonList):
        # 假设这是要发送给JavaScript的列表
        self.sendListToJS.emit(pythonList)

    # 鼠标位置用着函数发送给其他图
    @Slot()
    def requestCanvasPositionFromPython(self, pythonList):
        # 假设这是要发送给JavaScript的列表
        self.sendCanvasPositionToJS.emit(pythonList)

    # 接收十字线传递回来的校准坐标的函数
    @Slot(list)
    def sendCoordinatesToPython(self, coordinates):
        if self.ui.校准函数是否开启:
            if self.校准变量 == 0:
                logger.info(f"第1次点击的校准坐标:", coordinates)
                if self.ui.是否使用极坐标:
                    self.ui.api.圆心偏移X坐标 = coordinates[0]-self.ui.api.圆心基础X坐标
                    self.ui.api.圆心偏移Y坐标 = coordinates[1]-self.ui.api.圆心基础Y坐标
                    self.ui.api.显示消息框函数("success", f"成功定位圆心坐标为：{coordinates}", "接下来请获取圆的半径，鼠标移动到圆的半径，然后按下空格","底部",10000)
                else:
                    self.ui.api.X坐标基础值 = coordinates[0]
                    self.ui.api.Y坐标基础值 = coordinates[1]
                    self.ui.api.显示消息框函数("success", f"成功定位左上角坐标为：{coordinates}", "接下来请获取右下角坐标，，鼠标移动到最右下角，然后按下空格","底部",10000)
                self.校准变量 += 1
            elif self.校准变量 == 1:
                logger.info(f"第2次点击的校准坐标:", coordinates)
                if self.ui.是否使用极坐标:
                    self.ui.api.半径偏移倍率 = math.sqrt((coordinates[0] - (self.ui.api.圆心偏移X坐标+self.ui.api.圆心基础X坐标))**2 + (coordinates[1] - (self.ui.api.圆心偏移Y坐标+self.ui.api.圆心基础Y坐标))**2)/self.ui.api.极坐标基础半径
                    self.ui.api.显示消息框函数("success", f"成功定位圆的半径为：{math.sqrt((coordinates[0] - self.ui.api.圆心基础X坐标)**2 + (coordinates[1] - self.ui.api.圆心基础Y坐标)**2)}", f"相比于基础半径的倍率为：{self.ui.api.半径偏移倍率}","底部",10000)
                else:
                    self.ui.api.X坐标偏移倍率 = (coordinates[0] - self.ui.api.X坐标基础值)/self.ui.api.直角坐标基础宽度
                    self.ui.api.Y坐标偏移倍率 = (coordinates[1] - self.ui.api.Y坐标基础值)/self.ui.api.直角坐标基础高度
                    self.ui.api.显示消息框函数("success", f"成功定位右下角坐标为：{coordinates}", f"图像宽度为：{coordinates[0] - self.ui.api.X坐标基础值}，图像高度为：{coordinates[1] - self.ui.api.Y坐标基础值}，相比于基本宽度的X坐标偏移倍率为：{self.ui.api.X坐标偏移倍率}，相比于基本高度的Y坐标偏移倍率为：{self.ui.api.Y坐标偏移倍率}","底部",10000)
                self.校准变量 = 0
                self.ui.校准函数是否开启 = False
                self.ui.api.显示消息框函数("success", "校准成功", "参考图坐标校准已完成","底部")
                for i in self.ui.api.webviews:
                    i.page().runJavaScript("CalibrationFlagPosition = true;")# 让js发送遮罩数组回主函数

    # 向主painter传递背景图片
    @Slot()
    def requestBase64ImageFromPython(self, base64_image_data):
        logger.debug(f"向painter发送背景图片")
        # 向 JavaScript 发送 base64 编码的图像数据
        self.sendBase64ToJS.emit(base64_image_data)


    # 绘制的遮罩图像也用这个函数传递
    @Slot()
    def requestbase64picture(self,base64str, keystr):
        # 假设这是要发送给JavaScript的列表
        self.sendListToJS.emit([keystr, base64str])
    
    # 发送给painter的遮罩数组
    @Slot()
    def requestMuskArrayFromPython(self):
        logger.info("向painter发送遮罩数组")  
    
        颜色遮罩数组 = self.数组输入输出之前的预处理(self.ui.颜色遮罩数组).tolist()
        nan颜色数组 = self.数组输入输出之前的预处理(self.ui.nan颜色数组).tolist()

        data = [颜色遮罩数组, nan颜色数组]
        data_str = json.dumps(data)
        compressed_data = gzip.compress(data_str.encode('utf-8'))
        
        chunk_size = 1024 * 8192  # 8 MB
        total_chunks = (len(compressed_data) + chunk_size - 1) // chunk_size
        logger.info(f"数据压缩后大小为 {len(compressed_data)} 字节")

        def send_chunk(i, chunk):
            encoded_chunk = base64.b64encode(chunk).decode('utf-8')  # 将字节数据转换为base64字符串
            logger.info(f"正在发送 {i + 1} 个数据块，总数据块为 {total_chunks}")
            self.sendChunkToJS.emit(encoded_chunk, i, total_chunks)  # 发送base64字符串数据块

        threads = []
        for i in range(total_chunks):
            chunk = compressed_data[i * chunk_size:(i + 1) * chunk_size]
            thread = threading.Thread(target=send_chunk, args=(i, chunk))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def 数组输入输出之前的预处理(self, ori_array, 是否发送=True):
        """
        ori_array: numpy 数组
        是否发送: bool, 默认为 True
            如果为 True，则表示数据是要发送给 JavaScript 的，需要进行预处理
            如果为 False，则表示数据是从 JavaScript 接收的，需要逆序处理
        这个函数有一个额外的点，首先canvas和matplotlib的绘制方式本身有差别，matplotlib坐标原点默认就是0,0位于画面中心（实际上是画面左下角，因为不会出现负值），而canvas默认是左上角
        然后因为一些屎山问题，我已经不记得在html哪个地方进行的对应操作了，最后的结果就是输入的遮罩数组同时要完成转置→上下翻转→左右翻转之后才能和canvas对应上
        按理来说不需要那么多的，应该只需要一个操作就可以了……
        因为没有额外操作下都要转置翻转，然后又是布尔数组，所以在前面加上not，由于不知名原因，canvas绘制的极坐标必须+90度和一个单位数据才能和绘图区重合，明明算法是一样的啊。
        为了保证和matplotlib显示方式一样，极坐标最基础要默认+90度逆时针旋转，然后再根据用户的设置进行调整
        """
        # 先做一个深拷贝
        numpy_array = ori_array.copy()

        try:
            if 是否发送:
                # 发送处理步骤（顺序处理）
                if not self.ui.api.传递的遮罩是否转置:
                    numpy_array = np.transpose(numpy_array)

                if not self.ui.api.传递的遮罩是否上下翻转:
                    numpy_array = np.flip(numpy_array, axis=1)  # 上下翻转

                if not self.ui.api.传递的遮罩是否左右翻转:
                    numpy_array = np.flip(numpy_array, axis=0)  # 左右翻转

                if self.ui.是否使用极坐标:
                    # 矫正极坐标遮罩和底图的位置区别
                    numpy_array = np.transpose(numpy_array)
                    numpy_array = np.flip(numpy_array, axis=0)
                    numpy_array = np.concatenate((numpy_array[1:], numpy_array[:1]), axis=0)

                angle_flip = self.ui.api.传递的遮罩极坐标翻转角度
                if angle_flip != 0:
                    # 计算每个角度对应的元素数量
                    每个角度对应的元素数 = len(numpy_array) / 360
                    # 更新angle_flip的值
                    angle_flip = round(angle_flip * 每个角度对应的元素数)  # 确保angle_flip是整数
                    if self.ui.api.传递的遮罩极坐标是否是逆时针:
                        numpy_array = np.concatenate((numpy_array[-angle_flip:], numpy_array[:-angle_flip]), axis=0)
                    else:
                        numpy_array = np.concatenate((numpy_array[angle_flip:], numpy_array[:angle_flip]), axis=0)

            else:
                angle_flip = self.ui.api.传递的遮罩极坐标翻转角度
                if angle_flip != 0:
                    # 计算每个角度对应的元素数量
                    每个角度对应的元素数 = len(numpy_array) / 360
                    # 更新angle_flip的值
                    angle_flip = int(angle_flip * 每个角度对应的元素数)  # 确保angle_flip是整数
                    if self.ui.api.传递的遮罩极坐标是否是逆时针:
                        numpy_array = np.concatenate((numpy_array[angle_flip:], numpy_array[:angle_flip]), axis=0)
                    else:
                        numpy_array = np.concatenate((numpy_array[-angle_flip:], numpy_array[:-angle_flip]), axis=0)

                if self.ui.是否使用极坐标:
                    numpy_array = np.concatenate((numpy_array[-1:], numpy_array[:-1]), axis=0)
                    numpy_array = np.flip(numpy_array, axis=0)
                    numpy_array = np.transpose(numpy_array)

                if not self.ui.api.传递的遮罩是否左右翻转:
                    numpy_array = np.flip(numpy_array, axis=0)  # 左右翻转

                if not self.ui.api.传递的遮罩是否上下翻转:
                    numpy_array = np.flip(numpy_array, axis=1)  # 上下翻转

                if not self.ui.api.传递的遮罩是否转置:
                    numpy_array = np.transpose(numpy_array)

            return numpy_array

        except Exception as e:
            track = traceback.format_exc()
            logger.error(f"预处理失败: {e}\n{track}")
            raise e
        

class MyConfig(QConfig):
    """ Config of application """
    X坐标基础值 = ConfigItem("坐标换算组", "X坐标基础值", 0)
    Y坐标基础值 = ConfigItem("坐标换算组", "Y坐标基础值", 0)
    X坐标偏移倍率 = ConfigItem("坐标换算组", "X坐标偏移倍率", 1)
    Y坐标偏移倍率 = ConfigItem("坐标换算组", "Y坐标偏移倍率", 1)
    直角坐标基础宽度 = ConfigItem("坐标换算组", "直角坐标基础宽度", 1440)
    直角坐标基础高度 = ConfigItem("坐标换算组", "直角坐标基础高度", 500)
    圆心基础X坐标 = ConfigItem("坐标换算组", "圆心基础X坐标", 400)
    圆心基础Y坐标 = ConfigItem("坐标换算组", "圆心基础Y坐标", 400)
    圆心偏移X坐标 = ConfigItem("坐标换算组", "圆心偏移X坐标", 0)
    圆心偏移Y坐标 = ConfigItem("坐标换算组", "圆心偏移Y坐标", 0)
    半径偏移倍率 = ConfigItem("坐标换算组", "半径偏移倍率", 1)# 原再怎么画也不会变扁，总比方形图少一个参数
    极坐标基础半径 = ConfigItem("坐标换算组", "极坐标基础半径", 400)

    边缘提取的核大小 = RangeConfigItem("函数参数缓存组", "边缘提取的核大小", 3, RangeValidator(0, 10))
    边缘提取的阈值 = RangeConfigItem("函数参数缓存组", "边缘提取的阈值", 50, RangeValidator(0, 100))
    边缘提取的形态学核大小 = RangeConfigItem("函数参数缓存组", "边缘提取的形态学核大小", 3, RangeValidator(0, 10))
    边缘提取的描线宽度 = RangeConfigItem("函数参数缓存组", "边缘提取的描线宽度", 1, RangeValidator(0, 20))
    边缘提取的扩展像素 = RangeConfigItem("函数参数缓存组", "边缘提取的扩展像素", 0, RangeValidator(0, 20))




    文件夹路径 = ConfigItem("数据清理窗口组", "文件夹路径", "")
    正在使用的文件索引 = ConfigItem("数据清理窗口组", "正在使用的文件索引", 1)
    正在使用的文件名字 = ConfigItem("数据清理窗口组", "正在使用的文件名字", "")
    当前使用的文件路径 = ConfigItem("数据清理窗口组", "当前使用的文件路径", "")
    正在使用的页数 = ConfigItem("数据清理窗口组", "正在使用的页数", 1)
    是否需要完整报错信息 = ConfigItem("数据清理窗口组", "是否需要完整报错信息", False)
    是否需要规整数据 = ConfigItem("数据清理窗口组", "是否需要规整数据", False)
    是否默认预处理 = ConfigItem("数据清理窗口组", "是否默认预处理", False, BoolValidator())
    文件保存路径 = ConfigItem("数据清理窗口组", "文件保存路径", "")
    预处理代码 = ConfigItem("数据清理窗口组", "预处理代码", "")
    上一个处理的文件路径 = ConfigItem("数据清理窗口组", "上一个处理的文件路径", "")
    是否加载参考图 = ConfigItem("数据清理窗口组", "是否加载参考图", True)
    是否自动显示遮罩 = ConfigItem("数据清理窗口组", "是否自动显示遮罩", False)
    是否每绘制一步都刷新遮罩 = ConfigItem("数据清理窗口组", "是否每绘制一步都刷新遮罩", False)
    批量输出图片时根据图片类型分类 = ConfigItem("数据清理窗口组", "批量输出图片时根据图片类型分类", False)
    批量预处理后是否保存当前文件 = ConfigItem("数据清理窗口组", "批量预处理后是否保存当前文件", True)
    是否要渲染没有蒙版的文件 = ConfigItem("数据清理窗口组", "是否要渲染没有蒙版的文件", False)
    上一个文件的文件路径 = ConfigItem("数据清理窗口组", "上一个文件的文件路径", [])
    预处理函数只显示输出信息 = ConfigItem("数据清理窗口组", "预处理函数只显示输出信息", False)
    预处理函数代码print替换 = ConfigItem("数据清理窗口组", "预处理函数代码print替换", False)
    绘制图像dpi = RangeConfigItem("函数参数缓存组", "绘制图像dpi", 100, RangeValidator(0, 2000))
    是否输出渲染图片同时保存当前修改 = ConfigItem("数据清理窗口组", "是否输出渲染图片同时保存当前修改", False)
    是否输出渲染图片时输出对应的修改后npz文件 = ConfigItem("数据清理窗口组", "是否输出渲染图片时输出对应的修改后npz文件", False)
    是否渲染导出时输出的npz文件按照图片类型分类 = ConfigItem("数据清理窗口组", "是否渲染导出时输出的npz文件按照图片类型分类", False)
    缓存遮罩保存位置 = ConfigItem("数据清理窗口组", "缓存遮罩保存位置", "")
    是否只绘制一张参考图 = ConfigItem("数据清理窗口组", "是否只绘制一张参考图", False)
    有背景图时是否直接加载背景图 = ConfigItem("数据清理窗口组", "有背景图时是否直接加载背景图", True)
    是否开启夜间模式 = ConfigItem("数据清理窗口组", "是否开启夜间模式", False)
    软件主题色 = ColorConfigItem("数据清理窗口组", "软件主题色", "#009faa")
    软件图标 = OptionsConfigItem("数据清理窗口组", "软件图标","太阳", OptionsValidator(["太阳", "雪天", "雷雨", "月亮"]), restart=True)
    自动显示遮罩延迟时间 = RangeConfigItem("数据清理窗口组", "自动显示遮罩延迟时间", 1500, RangeValidator(0, 15000))
    


    自定义绘图函数 = ConfigItem("自定义组", "自定义绘图函数", "")
    自定义绘图函数能不能用 = ConfigItem("自定义组", "自定义绘图函数能不能用", False)


    用于判定是否使用极坐标绘图的的键 = ConfigItem("绘图数据组", "用于判定是否使用极坐标绘图的的键", "LDR")
    用于绘制绘图区背景图的键 = ConfigItem("绘图数据组", "用于绘制绘图区背景图的键", "Z1")
    是否用拥有该键作为判断极坐标绘图的依据 = ConfigItem("绘图数据组", "是否用拥有该键作为判断极坐标绘图的依据", False)
    显示参考图的行数 = RangeConfigItem("绘图数据组", "显示参考图的行数", 1, RangeValidator(0, 30))

    绘图区缺失值是否设置为白色 = ConfigItem("绘图数据组", "绘图区缺失值是否设置为白色", False)
    绘图区灰度图像是否颜色反转 = ConfigItem("绘图数据组", "绘图区灰度图像是否颜色反转", False)
    绘图区图像是否转置 = ConfigItem("绘图数据组", "绘图区图像是否转置", False)
    绘图区图像是否上下翻转 = ConfigItem("绘图数据组", "绘图区图像是否上下翻转", False)
    绘图区图像是否左右翻转 = ConfigItem("绘图数据组", "绘图区图像是否左右翻转", False)
    绘图区图像极坐标是否是逆时针 = ConfigItem("绘图数据组", "绘图区图线极坐标是否是逆时针", True)
    绘图区图像极坐标翻转角度 = RangeConfigItem("绘图数据组", "绘图区图像极坐标翻转角度", 0, RangeValidator(-360, 360))
    传递的遮罩是否转置 = ConfigItem("绘图数据组", "传递的遮罩是否转置", False)
    传递的遮罩是否上下翻转 = ConfigItem("绘图数据组", "传递的遮罩是否上下翻转", False)
    传递的遮罩是否左右翻转 = ConfigItem("绘图数据组", "传递的遮罩是否左右翻转", False)
    传递的遮罩极坐标是否是逆时针 = ConfigItem("绘图数据组", "传递的遮罩极坐标是否是逆时针", True)
    传递的遮罩极坐标翻转角度 = RangeConfigItem("绘图数据组", "传递的遮罩极坐标翻转角度", 0, RangeValidator(-360, 360))

    图像类型对应的源文件的key = ConfigItem("绘图数据组", "图像类型对应的源文件的key", {
                                                                                    "雷达反射率": "Z1",
                                                                                    "多普勒速度": "V1",
                                                                                    "速度谱宽": "W1",
                                                                                    "雷达信噪比": "SNR1",
                                                                                    "线性退偏振比": "LDR"
                                                                                })
    
    图像类型对应的不同对象的选择数值 = ConfigItem("绘图数据组", "图像类型对应的不同对象的选择数值", {"nan值":"0",
                                                                                            "待判断值":"1",
                                                                                            "判断为云":"2",
                                                                                            "地物杂波":"3",  # 新增
                                                                                            "非地物杂波":"4",  # 新增
                                                                                            "判断为气象目标物但不是云":"5",  # 原来是4，现在顺延为5
                                                                                            "不确定":"6",})  # 原来是5，现在顺延为6
    图像类型对应的不同对象的选择颜色 = ConfigItem("绘图数据组", "图像类型对应的不同对象的选择颜色", {"nan值":"#000000",# 黑色
                                                                                        "待判断值":"#FFFFFF",# 白色
                                                                                        "判断为云":"#FF0000",# 红色
                                                                                        "地物杂波":"#FF00FF",  # 正洋红色
                                                                                        "非地物杂波":"#00FF00",  # 绿色
                                                                                        "判断为气象目标物但不是云":"#0000FF",# 蓝色
                                                                                        "不确定":"#FFFF00",})# 黄色
    图像类型对应自定义色标 = ConfigItem("绘图数据组", "图像类型对应自定义色标（可以十六进制也可以rgb）", {})

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
        ui.path_painter_html = MainDrawingAreaContainer
        ui.path_other_html = ReferenceImageContainer
        ui.base64pictemp = base64pictempdata.strip("\n")

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
    
    def 显示进度条(self,是否显示 = True):
        if not 是否显示:# 之前用 if self.stateTooltip判断是否在显示
            logger.info("隐藏进度条")
            self.stateTooltip.setContent('文件加载完成啦 😆')
            self.stateTooltip.setState(True)
            
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

        # # 启动线程
        # thread = threading.Thread(target=线程任务)
        # thread.start()





    # 用来给按钮绑定函数的
    def Initialize_Connects(self,ui):
        # 为控件添加工具提示
        tooltips = {
            self.ui.showmask: "点击以显示或隐藏遮罩，点击切换状态，如果有遮罩的文件但是没显示出遮罩，也可以点击这里刷新一下。\n隐藏遮罩的快捷键为【Ctrl + X】,显示遮罩的快捷键为【Ctrl + L】",
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



            


        #ui.ui.widget.load(QUrl.fromLocalFile(path1))
        #ui.ui.widget.load(QUrl("https://cdn.bootcdn.net/ajax/libs/fabric.js/5.3.1/fabric.js"))


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


    # 这函数换现在我也看不懂了，算法每一步的东西全部都融在一个函数里面了，主要是为了提高效率，真要理解算法去看我最初写的七八个函数的文件
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


def matpainter(data, data_type, use_polar, file_name="",dpi=100, save_path=None,edgedict=None):
    """
    基础绘图函数，用于绘制单通道图像或极坐标图像。
    """
    if use_polar:
        # 创建一个极坐标图的画布
        r = np.linspace(0, data.shape[1], data.shape[1])
        theta = np.linspace(0, 2 * np.pi, data.shape[0])
        R, Theta = np.meshgrid(r, theta)

        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, dpi=dpi)
        ax.set_title(f"{data_type}-{file_name}")  # 设置图表标题

        # 绘制等高线填充图
        ax.contourf(Theta, R, data)
        ax.grid(False)  # 关闭网格显示
        ax.axis('off')  # 关闭坐标轴显示

    else:
        # 假设data是你的numpy数组
        # max_value_except_65535 = data[data != 65535].max()
        data[data == 65535] = np.nan  # 将65535的值替换为np.nan

        # 使用numpy的nan_to_num方法处理nan值，将nan替换为一个特定的值，这里选择最大值+1以便后续处理
        max_value = np.nanmax(data)
        data = np.nan_to_num(data, nan=max_value + 1)

        # 确保数据在0到255范围内
        data_normalized = (data - np.nanmin(data)) / (np.nanmax(data) - np.nanmin(data)) * 255
        data_normalized = data_normalized.astype(np.uint8)

        # 将单通道图像转换为彩色黑白图像（即RGB通道相同）
        data_rgb = np.stack([data_normalized]*3, axis=-1)

        # 处理nan值，将其绘制为白色
        data_rgb[data_normalized > 255] = [255, 255, 255]  # 将超出范围的值（即原nan位置）设置为白色

        # 绘制彩色黑白图像
        fig = plt.figure(figsize=(8, 6))
        plt.imshow(data_rgb, cmap='gray')  # 使用灰度色图以保持黑白效果
        plt.title(f"{data_type}-{file_name}")
        plt.axis('off')

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
        return img_base64


class BaseMainWindow(FluentWindow):
    """
    主窗口基类，用来定义一些通用的方法，如切换主题、切换深色模式、切换图标、快捷键等。
    """
    def __init__(self):
        super().__init__()
        self.initializationfirst()

    def initializationfirst(self):
        # 创建一个字典，将中文天气名称与对应的英文文件名匹配
        self.WeatherIconDictionary = {
            '太阳': ['WeatherIconSun.txt','WeatherIconSun'],
            '雪天': ['WeatherIconSnowy.txt','WeatherIconSnowy'],
            '雷雨': ['WeatherIconThunderstorm.txt','WeatherIconThunderstorm'],
            '月亮': ['WeatherIconMoon.txt','WeatherIconMoon']
        }
        
        # 使用字典来简化文件读取过程
        for Chinese, English in self.WeatherIconDictionary .items():
            setattr(self, English[1], globals()[English[1]].strip("\n"))

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
            elif event.key() == Qt.Key_X:  # X键，清空遮罩
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
                    i.page().runJavaScript("toggleNightMode(true);")
                except:pass

        else:
            setTheme(Theme.LIGHT)
            # 删除背景颜色
            self.setStyleSheet("background-color: #ffffff;")
            for i in WebContainer:
                try:
                    i.page().runJavaScript("toggleNightMode(false);")
                except:pass
    def SwitchThemeColor(self,color):
        setThemeColor(color)

    def ToggleIcon(self,base64_str):
        """
        从 Base64 编码的字符串加载 QIcon。
        """
        # 获取对应的类属性值，还要转化一下
        base64_data = getattr(self,self.WeatherIconDictionary[base64_str][1])
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
        add_switch_setting_card(FIF.CALORIES, "批量预处理后是否保存当前文件", "打开之后批量预处理的时候会将遮罩和nan遮罩的修改保存到新的文件里，关闭之后不会保存，默认是开启的，关闭的话请确保批量预处理代码中存在保存文件相关的代码（虽然不建议在预处理代码中保存文件）。", parent.cfg.批量预处理后是否保存当前文件, "批量预处理后是否保存当前文件",通用设置项)
        add_switch_setting_card(FIF.REMOVE_FROM, "是否输出渲染图片同时保存当前修改", "在输出渲染的图像的时候，顺带保存下当前编辑内容，避免切换下一个文件的时候忘了保存（大误）", parent.cfg.是否输出渲染图片同时保存当前修改, "是否输出渲染图片同时保存当前修改",通用设置项)
        add_switch_setting_card(FIF.CHECKBOX, "是否输出渲染图片时输出对应的修改后npz文件", "不开这个选项，将参考图像输出出去的时候，就单纯新建个文件同名文件夹，然后往里面存图片，开了之后就会存按照当前选中内容筛选后的npz文件", parent.cfg.是否输出渲染图片时输出对应的修改后npz文件, "是否输出渲染图片时输出对应的修改后npz文件",通用设置项)
        add_switch_setting_card(FIF.TILES, "是否渲染导出时输出的npz文件按照图片类型分类", "不同类型的图片导出成不同的文件", parent.cfg.是否渲染导出时输出的npz文件按照图片类型分类, "是否渲染导出时输出的npz文件按照图片类型分类",通用设置项)
        add_switch_setting_card(FIF.SYNC, "是否显示参考图片", "如果不显示参考图片可以极大加快打开文件的速度，大概节省6秒左右", parent.cfg.是否加载参考图, "是否加载参考图",通用设置项)
        add_switch_setting_card(FIF.CAMERA, "是否只加载一张参考图片", "预处理好背景图之后再打开这个开关是理论上能够正常使用最快加载速度，一张图不要求特别严格的话其实也可以用来做标记了。", parent.cfg.是否只绘制一张参考图, "是否只加载一张参考图片",通用设置项)
        add_switch_setting_card(FIF.BOOK_SHELF, "有背景图时是否直接加载背景图", "打开之后，npz文件中有“Background”这个键的的时候，代表有缓存的背景图（base64格式），不会再重新计算背景图像，直接加载背景图，可以节省巨量的加载时间", parent.cfg.有背景图时是否直接加载背景图, "有背景图时是否直接加载背景图",通用设置项)
        add_switch_setting_card(FIF.LABEL, "是否使用自定义绘图函数", "自定义绘图函数我是直接exec运行的，还是希望使用者能够校验一下，不要出现安全漏洞", parent.cfg.自定义绘图函数能不能用, "自定义绘图函数能不能用",通用设置项)
        add_switch_setting_card(FIF.MINIMIZE, "是否需要规整数据", "规整数据的意思是将杂七杂八的颜色统一化为“不确定”的颜色，这个功能开不开只影响绘图的时候，因为杂七杂八的颜色保存到遮罩数组的时候都是默认为不确定的，重新加载文件也会是“不确定”的颜色。", parent.cfg.是否需要规整数据, "是否需要规整数据",通用设置项)
        add_switch_setting_card(FIF.IMAGE_EXPORT, "批量输出图片时根据图片类型分类", "这个选项如果选否，输出结果是按照文件名分文件夹，如果选是，程序最后会自动转化为按照图片类型分文件夹", parent.cfg.批量输出图片时根据图片类型分类, "批量输出图片时根据图片类型分类",通用设置项)
        add_switch_setting_card(FIF.CLOUD, "是否要渲染没有蒙版的文件", "这个选项适用于批量输出图片的时候，选择是否要跳过没有编辑过的文件", parent.cfg.是否要渲染没有蒙版的文件, "是否要渲染没有蒙版的文件",通用设置项)

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


class MainWindow(BaseMainWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__()
        self.initialization()
        self.initWindow()# 初始化放在后面，因为需要先创建窗口对象，再初始化窗口，这样窗口名字就不会被覆盖
        self.SwitchDepthMode(self.api.是否开启夜间模式)
        self.SwitchThemeColor(self.api.软件主题色)
        self.show()

    def initialization(self):
        # 创建子界面
        self.ui = DataAnnotation()
        self.ui.setupUi(self)

        self.api = FunctionsAll(self)
        self.api.Initialize_Connects(self)
        self.settingInterface = SettingWidget('设置界面', self)

        self.addSubInterface(self.ui.widget, FIF.HOME, '数据标注界面')
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置界面', NavigationItemPosition.BOTTOM)


    def initWindow(self):
        # 获取应用程序实例
        app = QCoreApplication.instance()
        # 获取屏幕的尺寸
        screen = app.primaryScreen().size()
        # 计算宽度和高度
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