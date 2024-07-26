import math
import numpy as np
from PIL import Image
"""
这是极坐标和图像坐标相互转化算法的初稿pyhon和html都用的这个算法，实际用的代码增加了一堆numpy优化性能导致算法看不懂了，但是思路是没变的，留这个初稿备份
"""
# 将直角坐标 (x, y) 转换为极坐标 (r, theta)
def 直角坐标转换为极坐标(x, y):
    r = math.sqrt(x**2 + y**2)  # 计算半径 r
    theta = math.degrees(math.atan2(y, x))  # 计算角度 theta，并将其转换为度数
    if theta < 0:
        theta += 360  # 确保角度在 0 到 360 度之间
    return r, theta

# 判定一个点可能对应的所有极坐标
def 像素坐标映射到极坐标(x, y, a=360):
    r, theta = 直角坐标转换为极坐标(x, y)  # 将直角坐标转换为极坐标
    b = r * math.sin(math.pi / a)  # 计算 b 值
    
    possible_polar_coords = [(round(r), round(theta))]  # 初始化列表，包含原始极坐标，先r后theta
        
    # 根据 b 值循环判定并添加额外的极坐标
    i = 1
    while b < (1 / (2 ** i)):  # 例如 b < 0.5, b < 0.25, b < 0.125, ...
        possible_polar_coords.append((round(r), round((theta + i) % 360)))
        possible_polar_coords.append((round(r), round((theta - i) % 360)))
        i += 1
    
    return list(set(possible_polar_coords))

# 将极坐标 (r, theta) 转换为直角坐标 (x, y)
def 极坐标转换为直角坐标(r, theta):
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y

# 查找满足条件的像素点
def 极坐标映射到像素坐标(r, theta, a=360):
    # 将角度 theta 从度数转换为弧度
    # 首先，将0.5度转换为弧度
    theta_rad = math.radians(theta)
    half_degree_in_radians = math.radians(0.5)
        
    # 将极坐标转换为直角坐标
    x_center, y_center = 极坐标转换为直角坐标(r, theta_rad)
    
    # 计算 b = r * sin(pi / a)
    b = r * math.sin(math.pi / a)

    if b < 1.2:# 应该是这个地方导致了很多点没有被选中，不能只返回一个值
        minpoint = 返回相邻点(x_center, y_center, r, theta, 3)
        return [(round(x_center), round(y_center))]+minpoint
    elif b < 0.3:
        return [(round(x_center), round(y_center))]
    
    # 定义要检查的范围 (四舍五入取整)
    x_min = round(x_center - b)
    x_max = round(x_center + b)
    y_min = round(y_center - b)
    y_max = round(y_center + b)
    
    pixels = []  # 用于存储满足条件的像素点
    
    # 遍历 (x_min, x_max) 和 (y_min, y_max) 范围内的所有点
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            # 检查条件 1：点 (x, y) 到原点的距离与 r 的差距在正负1以内
            r1,theta1 = 直角坐标转换为极坐标(x, y)
            
            if abs(r1 - r) <= 1:
                # 检查条件 2：x/r 的值在 sin(theta - 0.5) 和 sin(theta + 0.5) 范围内
                # 然后，使用转换后的弧度值来判断条件
                if abs(theta1 -theta) <=0.5:
                    pixels.append((x, y))
                    
    return pixels

# 计算和一个点最接近的相邻点，希望能通过这个避免条纹（条纹多就多选几个点）
def 返回相邻点(x_center, y_center, r, theta, num=1):
    differences = []
    # 遍历周围的八个点
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue  # 跳过中心点本身
            x = round(x_center) + dx
            y = round(y_center) + dy
            # 计算极坐标
            r_adj, theta_adj = 直角坐标转换为极坐标(x, y)
            # 计算与原始 r 和 theta 的差异
            diff = abs(r - r_adj) + abs(theta - theta_adj)
            # 添加到列表
            differences.append(((x, y), diff))
    
    # 根据差异排序
    differences.sort(key=lambda x: x[1])
    # 返回差异最小的两个点的坐标
    return [x[0] for x in differences[:num]] if len(differences) > 1 else [x[0] for x in differences]


# 将极坐标数据映射到画布数组
def 完整极坐标数组到画布数组(polar_array,canvassize=1000):
    """
    输入的数组一维必须是角度，二维必须是半径
    """
    minnan = np.nanmin(polar_array)
    canvassize = 2000
    canvas = np.zeros((canvassize, canvassize))  # 创建一个 2000x2000 的空白二维数组
    Dimension = polar_array.shape[0] # 获取极坐标数组的维度

    for theta in range(len(polar_array)):
        for r in range(len(polar_array[theta])):
            pointlisttinal = []
            # 使用极坐标映射到像素坐标计算笛卡尔坐标
            pointlist = 极坐标映射到像素坐标(r, theta, Dimension)

            for x, y in pointlist:
                x_canvas = round(x + canvassize/2)
                y_canvas = round(y + canvassize/2)
                pointlisttinal.append((x_canvas, y_canvas))
            
            # 将坐标转换为画布上的坐标
            for x_canvas, y_canvas in pointlisttinal:   
                # 确保坐标在画布范围内
                if 0 <= x_canvas < canvassize and 0 <= y_canvas < canvassize:
                    # 在画布上标记点
                    if not np.isnan(polar_array[theta,r]):
                        canvas[x_canvas, y_canvas] = polar_array[theta, r] + minnan
                    else:
                        canvas[x_canvas, y_canvas] = 0
    return canvas

def 绘制灰度图直接绘制(canvas):
    # 确保 canvas 数组的数据类型为 float，以便进行数学运算
    canvas = canvas.astype(float)

    # 归一化 canvas 数组
    canvas -= canvas.min()  # 将数组最小值减去自身，确保最小值为0
    canvas_max = canvas.max()
    if canvas_max > 0:  # 防止除以0的情况
        canvas /= canvas_max  # 将数组最大值除以自身，确保最大值为1
    canvas *= 255.0  # 将归一化后的数组乘以255，映射到0-255的范围
    canvas = canvas.astype(np.uint8)  # 转换为 uint8 类型

    # 使用 PIL 将归一化后的二维数组转换为灰度图并显示
    image = Image.fromarray(canvas)
    image.show()

def 绘制颜色图输出十六进制(canvas):
    # 确保 canvas 数组的数据类型为 float，以便进行数学运算
    canvas = canvas.astype(float)

    # 归一化 canvas 数组
    canvas -= canvas.min()  # 将数组最小值减去自身，确保最小值为0
    canvas_max = canvas.max()
    if canvas_max > 0:  # 防止除以0的情况
        canvas /= canvas_max  # 将数组最大值除以自身，确保最大值为1
    canvas *= 255.0  # 将归一化后的数组乘以255，映射到0-255的范围
    canvas = canvas.astype(np.uint8)  # 转换为 uint8 类型

    # 创建一个与 canvas 同尺寸的三维数组，用于存储 RGB 颜色值
    color_canvas = np.zeros((canvas.shape[0], canvas.shape[1], 3), dtype=np.uint8)

    # 遍历 canvas，将灰度值转换为 RGB 十六进制颜色值
    for i in range(canvas.shape[0]):
        for j in range(canvas.shape[1]):
            gray_value = canvas[i, j]
            # 灰度值直接用于 RGB，生成灰度图
            color_canvas[i, j] = [gray_value, gray_value, gray_value]

    # 将 RGB 数组转换为十六进制颜色值的二维数组
    hex_color_canvas = np.zeros((canvas.shape[0], canvas.shape[1]), dtype=object)
    for i in range(color_canvas.shape[0]):
        for j in range(color_canvas.shape[1]):
            r, g, b = color_canvas[i, j]
            hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
            hex_color_canvas[i, j] = hex_color

    return hex_color_canvas

# 直接是零散像素点
def 零散画布位置列表到极坐标(canvas_list,canvas_size=1000):
    """
    输入参数是一系列像素坐标点的列表，每个元素是一个(x, y)坐标的元组。
    返回一堆极坐标点的集合。
    """
    # 初始化极坐标数组，这里假设极坐标的范围和精度，可能需要根据实际情况调整
    polar_coords = []

    for x, y in canvas_list:
        # 假设像素坐标映射到极坐标的函数已经定义
        pointlist = 像素坐标映射到极坐标(x - canvas_size // 2, y - canvas_size //2)
        polar_coords += pointlist

    return list(set(polar_coords))



def 零散极坐标位置到画布(polar_coords, canvas_size=1000):
    """
    输入参数是一系列极坐标点的列表，每个元素是一个(r, theta)坐标的元组。
    返回一堆像素坐标点的集合。
    """
    # 初始化像素坐标数组，这里假设像素坐标的范围和精度，可能需要根据实际情况调整
    canvas_coords = []

    for r, theta in polar_coords:
        # 假设极坐标映射到像素坐标的函数已经定义
        pointlist = 极坐标映射到像素坐标(r, theta)
        pointlist = [(x + canvas_size//2, y + canvas_size//2) for x, y in pointlist]
        # 确保pointlist中的每个元素都转换为元组
        canvas_coords += pointlist

    return list(set(canvas_coords))