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

 

确定生成了配置文件.json后关闭软件，重新打开软件，如果在主界面能够看到生成的图片，就表明已经可以进行数据标注了，如果没看到重新点击一下选择文件试试看。左边一列第一个容器是绘图区容器，右边一列第第一个容器是显示遮罩的容器，除此之外其他都是参考图容器。

 

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
   【一定要仔细看说明！！定义色标等各种量的时候定义成函数域内变量，不要定义成全局变量！！！全局变量只能有一个函数名！！需要用到matplotlib、numpy、pandas、PIL、cv2之外的库，需要去源代码的主程序里import，在n \】

 

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
