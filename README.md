# 2DArray_Label_Annotation_tool
对二维数组进行像素点数据标注的小工具，生成一个和二维数组同尺寸的遮罩。 


A tool for pixel data annotation of 2D arrays that generates a mask of the same size as the original array.



## 适用范围
假如你有一个二维数组（可能表示一个图像或者其他什么，但前提是这个二维数组可以被matplotlib绘制出来，即结构整齐且值必须为纯数字），你要对每一个数据点标注类型，可以使用该程序。
目前只支持中文……工具注释的文本量太大了有点翻译不过来。

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

- 支持对目录下的文件批量预处理（批量对每一个文件按照预设条件生成一个对应的包含“Musk”键的npz文件）。
  - Support batch preprocessing for files in a directory (batch generating a corresponding npz file with the "Musk" key for each file according to preset conditions).

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

### 设置界面 / Settings Interface
![Settings Interface](https://github.com/user-attachments/assets/516cbd2a-ea23-495e-84e8-b070d7493100)

## 使用教程 / User Guide
稍后补充 / To be added later

## 开发背景 / Development Background
稍后补充 / To be added later
