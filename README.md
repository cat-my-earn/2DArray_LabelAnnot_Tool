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
稍后补充视频和图片的，愿意硬啃文本的话可以先看 【Chinese_Documentation┃操作说明.md】 / To be added later






## 背景和需求 / Background and Needs
最初是任务要求要训练个神经网络，去判定雷达图中的不同目标物。

首先肯定要做训练集嘛，然后就卡在那里了。

老师的要求是模型输出应该是一个对输入数据的每个像素点标定0、1、2、3的数组，分别代表不同的回波类型。我直观的去想……那我的训练集也应该是原始数据，标签应该是一个原始数据同尺寸的不同数字的遮罩数组。

然后搜了很多工具……发现没有一个能做到这个的，大家都是往越来越智能的方向发展，拿一个多边形哐哐哐就把东西圈出来了，更简单的如labeling，一个矩形搞定。

这时候我想着我思路肯定错了……做的也不是什么新鲜东西，训练个神经网络都是被无数人做烂的事情，我能走不通绝对是我思路错了，正常做法肯定不是这么来的。

然后我用labeling试着标记了好些图片，很快啊，一千五百张两三天就搞定了……虽然过程很痛苦，毕竟雷达图卫星图这种东西，哪里是一张图能判定类型的，都得多个通道多个参数一起看，labeling又不支持，我只能不停地切图、找点位，严重拖慢速度。而且labeling还不能放大，找小目标物打框要痛苦死了。

但是我做着做着感觉不对劲。众所周知，很多气象目标物都是很小的，像是冰雹龙卷在回波上就几个像素点，杂波在正常回波的边缘也是零星的像素点，画圈画多边形要么很粗糙的一个框把杂波和正常回波圈进去，然后再将杂波单独圈出来，要么就得画特别特别多的框……

这样下来做是做完了，但是数据标签之粗糙——毕竟验证标准也是要按像素点级别去判定的，标签这么粗糙感觉有问题。

还有一个就是我手头上明明有原始数据，却要拿原始数据画出图再拿图去打标签感觉怪怪的，直接用原始数据去训练肯定比用二次操作生成的图去训练效果好啊。况且matplotlib绘图出来的结果和像素点也对不上，怎么都对不上，模型要从图再还原出原来的原始数据数组尺寸的遮罩感觉也有点问题……

还有就是直角坐标和极坐标，直角坐标还好，实在不行用PIL也能输出尺寸和数组完全一样的，虽然不方便加色标。PPI这种极坐标图，图像上的点和原始数据数组根本对不上。

犹豫再三还是用老思路——对原始数组每个点单独打标签，但是市面上也没有能达到类似功能的工具，随即就决定自己写一个。

写好之后实用起来，发现打标签的速度异常慢——用labeling一两分钟之内肯定搞定一张图了，用这东西直接就是五六分钟起步，看着数据集的大小，数据标注的时间消耗是原来预期的五六倍。

出现这个问题一个是内部数据计算耗时比较大，另一个是像素级的标记要求精校，也是巨量的耗时，原来labeling一个框拉过去完事的现在要一个点一个点标出来。

这肯定有问题，数据标注不应该这么慢的，我到现在都觉得我思路不对，肯定不是这么搞的，如果大家都搞这种像素点级的标签，几千的数据集就要快一周，上万的数据集不得直接完蛋？

如果看到这里的客官能够提供下正确的思路，我将不胜感激！！！！！

也希望如果真有要用到这个程序的，审慎回顾一下技术路线，虽然我最后写出来也实际用它干活了，但我依然感觉这是条歧路。






## [开发过程](src/Development%20Process.md) / Development Process

有空就写写这坨屎山是怎么产生的……毕竟被它折磨了一段时间，不记录一下说不过去。
Please click the link to view, but note that the document is in Chinese.
