# 2DArray_Label_Annotation_tool
对二维数组进行像素点数据标注的小工具，生成一个和二维数组同尺寸的遮罩。 


A tool for pixel data annotation of 2D arrays that generates a mask of the same size as the original array.

![painter-example](https://github.com/user-attachments/assets/79c5cf64-5715-4929-9640-5c95be5b9373)


## 适用范围
假如你有一个二维数组（可能表示一个图像或者其他什么，但前提是这个二维数组可以被matplotlib绘制出来，即结构整齐且值必须为纯数字），你要对每一个数据点标注类型，可以使用该程序。

If you have a 2D array (which might represent an image or something else, but the premise is that this 2D array can be plotted using matplotlib, meaning its structure is regular and the values must be pure numbers), and you want to annotate each data point, you can use this program.

It only supports Chinese now, because tool's annotations are too large to translate.

## 功能概述 / Functional Overview

### 主要功能概述 / Main Functional Overview
- 使用画笔、圆形、矩形、多边形和油漆桶工具，以绘图的形式对二维数组进行标注。标注结果将以“Musk”键储存在新生成的npz文件中。
  - Annotate a 2D array using tools like brush, circle, rectangle, polygon, and paint bucket. The annotation results will be stored in a newly generated npz file under the key "Musk".

- 可以自定义标注类型和绘图时对应的颜色。
  - Customize annotation types and the corresponding colors when drawing.

- 可以自定义被标注的数据点范围，通过将尺寸相同的零和一构成的数组以键“Musk_nan”添加到npz文件中实现。
  - Customize the range of data points to be annotated by adding arrays consisting of zeros and ones with the same size under the key “Musk_nan” in the npz file.

- 可以加载多个二维数组，由matplotlib绘制图像，不同图像比较以确定标注类型。
  - Load multiple 2D arrays, plot images with matplotlib, and compare different images to determine annotation types.

- 支持自定义绘图函数，程序将传入二维数组和其他必要参数，由自定义函数绘制出matplotlib图像。
  - Support custom drawing functions, where the program passes the 2D array and other necessary parameters, and the custom function draws the matplotlib image.

- 支持十字标注线：显示绘图区鼠标位置在其他参考图像上的位置。
  - Support crosshair annotation: display the mouse position in the drawing area on other reference images.

- 支持缩放、拖动绘图画布，绘制到一半时缩放和拖动可以中断图形绘制，结束时恢复绘制。
  - Support zooming and dragging the drawing canvas. Zooming and dragging can interrupt drawing midway, and resume drawing afterward.

- 支持一键将所有参考图缩放、移动到绘图区背景图的位置。
  - Support one-click scaling and moving of all reference images to the position of the background image in the drawing area.

- 支持按照数组数值对数组进行预处理，即自动将特征明确像素点标注好，剩下的再人工标注。
  - Support preprocessing the array based on array values, i.e., automatically annotate clearly defined feature pixels and then manually annotate the remaining parts.

- 支持绘制出消除特定标注类型的参考图（也支持将消除特定注释类型后的数据导出成npz或npy文件）。
  - Support drawing reference images with specific annotation types removed (also supports exporting data with specific annotation types removed as npz or npy files).

- 支持对标注类型进行边缘提取而后在参考图上呈现（相当于将标注区域用笔在参考图上圈出来）。
  - Support edge extraction for annotation types and then present them on the reference image (equivalent to circling the annotated area on the reference image).

- 支持导出参考图（包括消除特定标注区域的、和边缘提取后的参考图）。
  - Support exporting reference images (including those with specific annotated areas removed and those after edge extraction).

- 支持对目录下的文件批量导出参考图（批量对每一个文件用自定义绘图函数绘制出matplotlib图像后导出到对应文件夹）。
  - Support batch exporting reference images for files in a directory (batch drawing matplotlib images for each file using a custom drawing function and exporting them to the corresponding folder).

- 支持对目录下的文件批量预处理（批量对每一个文件按照预设条件生成一个对应的包含“Musk”键和“Musk_nan”键的npz文件）。
  - Support batch preprocessing for files in a directory (batch generating a corresponding npz file with the "Musk" and "Musk_nan" keys for each file according to preset conditions).

- 使用配置文件，可以批量修改配置项。
  - Use configuration files to batch modify configuration items.

### 图形界面自定义 / GUI Customization
- 夜间模式
  - Night mode

- 自定义主题色
  - Custom theme colors

- 可选图标
  - Optional icons

## 软件界面 / Software Interface

### 主绘图界面 / Main Drawing Interface
![Main Drawing Interface](https://github.com/user-attachments/assets/30f25f26-bb9c-470b-a655-f41f62697b2b)

![Main Drawing Interface Dark](https://github.com/user-attachments/assets/d78cc821-af84-4058-9e69-07a0d8eb378d)


### 设置界面 / Settings Interface
![Settings Interface](https://github.com/user-attachments/assets/516cbd2a-ea23-495e-84e8-b070d7493100)

![Settings Interface Dark](https://github.com/user-attachments/assets/f4293717-0b18-4293-86e5-38df001bf884)






## 使用教程 / User Guide
稍后补充视频和图片的，愿意硬啃文本的话可以先看 [纯文本使用说明](Chinese_Documentation┃操作说明.md) / To be added later

建议clone整个项目到本地，然后将venv文件夹里的venv.zip下载到本地，解压到venv文件夹里，双击bat即可运行。

也可以使用自己的环境，运行MainWindow.py即可。

如果不想太麻烦，可以在[release](https://github.com/cat-my-earn/2DArray_LabelAnnot_Tool/releases/tag/v1.0)里下载exe可执行文件，双击后等待半分钟即可启动。

但是加载自定义绘图函数的时候，只能使用源码里import的库，可执行文件没法修改源码，只能使用‌`matplotlib‌`库，无法添加诸如‌`scipy‌`、‌`cartopy‌`等辅助绘图的库。




## [背景和需求](src/Background%20and%20Needs.md) / Background and Needs

可以通过查看我开发这个程序时的背景、遇到的问题以及使用它做了什么事情，来判断该程序是否适合您的使用场景。可以点击上方链接查看。

You can assess whether this program fits your use case by reviewing the background, issues encountered, and tasks performed during its development. 

Please click the link to view, but note that this document is in Chinese.




## [开发过程](src/Development%20Process.md) / Development Process

有空就写写这坨屎山是怎么产生的……毕竟被它折磨了一段时间，不记录一下说不过去。

Please click the link to view, but note that the document is in Chinese.
