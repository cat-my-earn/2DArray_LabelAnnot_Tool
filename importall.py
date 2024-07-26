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
import requests

# PySide6 导入
from PySide6.QtCore import (QCoreApplication,QMetaObject, QObject,QResource, QFile, QIODevice,
                             QRect, QSize, Qt, Slot, Signal,  QThread,QTimer, QUrl)
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
from src.res import *

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