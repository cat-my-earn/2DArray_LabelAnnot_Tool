from importall import *

def matpainter(data, data_type, use_polar, file_name="",dpi=100, save_path=None,edgedict=None):
    logger.info(f"正在绘制{data_type}图像")
    """
    :param data: 数据-一个二维数组
    :param data_type: 数据类型（中文名字）
    :param use_polar: 是否使用极坐标绘图。True 表示使用极坐标，False 表示使用直角坐标
    :param file_name: 当前绘制的文件的文件名
    :param dpi: 图像的分辨率
    :param save_path: 保存路径
    :param edgedict: 边缘位置点集字典
    """

    # 色标配置
    # Z色标
    rgb_Z = [[0,193,189],[173,196,222],[101,148,231],[1,0,253],
            [146,236,144],[46,205,55],[0,129,0],
            [253,255,0],[192,190,0],[181,135,8],
            [255,181,193],[255,95,74],[252,1,0],
            [222,159,219],[196,0,195]]
    rgbn_Z = np.array(rgb_Z) / 255.0
    icmap_Z = mpl.colors.ListedColormap(rgbn_Z, name='Z_color')
    bounds_Z = [-40, -35, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35]
    norm_Z = mpl.colors.BoundaryNorm(bounds_Z, icmap_Z.N)

    # V色标
    rgb_V = [[139,204,232], [0,255,254],[0,193,189],
            [0,255,0],[46,207,52],[1,126,5],
            [169,169,169],[211,211,211],
            [254,0,0],[255,124,84],[254,192,201],
            [255,162,0],[249,217,1],[254,255,0]]
    rgbn_V = np.array(rgb_V) / 255.0
    icmap_V = mpl.colors.ListedColormap(rgbn_V, name='V_color')
    bounds_V = [-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7]
    norm_V = mpl.colors.BoundaryNorm(bounds_V, icmap_V.N)

    # SW色标
    rgb_SW = [[192,192,192],[1,125,6],[46,207,51],[0,255,250],[137,205,234],
            [255,96,73],[255,192,200],[255,162,0],[250,217,0],[254,255,0]]
    rgbn_SW = np.array(rgb_SW) / 255.0
    icmap_SW = mpl.colors.ListedColormap(rgbn_SW, name='SW_color')
    bounds_SW = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    norm_SW = mpl.colors.BoundaryNorm(bounds_SW, icmap_SW.N)

    # SNR色标
    rgb_SNR = [[0,193,189],[177,196,220],[101,149,233],[0,0,254],
            [148,235,146],[46,207,52],[1,125,7],[254,255,0],[188,192,0],[181,134,13],
            [250,184,191],[255,96,74],[254,0,0],[220,160,218],[195,0,192]]
    rgbn_SNR = np.array(rgb_SNR) / 255.0
    icmap_SNR = mpl.colors.ListedColormap(rgbn_SNR, name='SNR_color')
    bounds_SNR = [-40, -35, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35]
    norm_SNR = mpl.colors.BoundaryNorm(bounds_SNR, icmap_SNR.N)

    # LDR色标
    rgb_LDR = [[4,192,188],[101,148,236],[3,0,249],[143,239,140],[47,206,50],
            [2,128,2],[253,255,3],[160,159,57],[186,132,17],
            [255,180,193],[249,98,68],[251,2,0],[225,157,225],[195,0,193]]
    rgbn_LDR = np.array(rgb_LDR) / 255.0
    icmap_LDR = mpl.colors.ListedColormap(rgbn_LDR, name='LDR_color')
    bounds_LDR = [-40, -35, -30, -25, -20, -15, -10, -5, 0, 2, 4, 6, 8, 10, 12]
    norm_LDR = mpl.colors.BoundaryNorm(bounds_LDR, icmap_LDR.N)

    # 图像类型对应的源文件的key
    data_keys = {
        "雷达反射率": "Z1",
        "多普勒速度": "V1",
        "速度谱宽": "W1",
        "雷达信噪比": "SNR1",
        "线性退偏振比": "LDR"
    }

    # 色标和归一化参数的映射
    cmap_dict = {
        "雷达反射率": (icmap_Z, norm_Z, bounds_Z, 'dBZ'),
        "多普勒速度": (icmap_V, norm_V, bounds_V, 'm/s'),
        "速度谱宽": (icmap_SW, norm_SW, bounds_SW, 'm/s'),
        "雷达信噪比": (icmap_SNR, norm_SNR, bounds_SNR, 'dBZ'),
        "线性退偏振比": (icmap_LDR, norm_LDR, bounds_LDR, 'dB')
    }


    ##——颜色映射——##


    # 定义一个列表，其中包含元组，每个元组代表一个颜色范围和对应的RGB颜色值
    # 雷达反射率的颜色映射


    # 雷达反射率的颜色映射
    Z1_color_scale = [
        ((-40, -35), "#00aca4"),
        ((-35, -30), "#c0c0fe"),
        ((-30, -25), "#7a72ee"),
        ((-25, -20), "#1e26d0"),
        ((-20, -15), "#a6fca8"),
        ((-15, -10), "#00ea00"),
        ((-10, -5), "#10921a"),
        ((-5, 0), "#fcf464"),
        ((0, 5), "#c8c802"),
        ((5, 10), "#8c8c00"),
        ((10, 15), "#feacad"),
        ((15, 20), "#fe6454"),
        ((20, 25), "#ee0230"),
        ((25, 30), "#d48efe"),
        ((30, 35), "#aa24fa")
    ]



    # 多普勒速度的颜色映射
    V1_color_scale = [
        ((-7, -6), "rgb(126, 224, 254)"),
        ((-6, -5), "rgb(0, 224, 254)"),
        ((-5, -4), "rgb(0, 176, 176)"),
        ((-4, -3), "rgb(0, 254, 0)"),
        ((-3, -2), "rgb(0, 196, 0)"),
        ((-2, -1), "rgb(0, 128, 0)"),
        ((-1, 0), "rgb(211, 211, 211)"),
        ((0, 1), "rgb(169, 169, 169)"),
        ((1, 2), "rgb(254, 0, 0)"),
        ((2, 3), "rgb(254, 88, 88)"),
        ((3, 4), "rgb(254, 176, 176)"),
        ((4, 5), "rgb(254, 124, 0)"),
        ((5, 6), "rgb(254, 210, 0)"),
        ((6, 7), "rgb(254, 254, 0)")
    ]


    # 多普勒谱宽的颜色映射
    W1_color_scale = [
        ((0, 0.5), "rgb(192,192,192)"),
        ((0.5, 1), "rgb(1,129,2)"),
        ((1, 1.5), "rgb(48,206,52)"),
        ((1.5, 2), "rgb(0,255,252)"),
        ((2, 2.5), "rgb(138,205,234)"),
        ((2.5, 3), "rgb(250,101,67)"),
        ((3, 3.5), "rgb(255,191,204)"),
        ((3.5, 4), "rgb(255,162,0)"),
        ((4, 4.5), "rgb(249,217,2)"),
        ((4.5, 5), "rgb(255,254,0)")
    ]


    # 信噪比的颜色映射
    SNR1_color_scale = [
        ((-55, -50), "rgb(131,0,129)"),
        ((-50, -40), "rgb(192,192,192)"),
        ((-40, -35), "rgb(0,193,189)"),
        ((-35, -30), "rgb(177,196,220)"),
        ((-30, -25), "rgb(100,150,229)"),
        ((-25, -20), "rgb(0,0,254)"),
        ((-20, -15), "rgb(145,238,142)"),
        ((-15, -10), "rgb(45,208,51)"),
        ((-10, -5), "rgb(2,125,7)"),
        ((-5, 0), "rgb(255,254,0)"),
        ((0, 5), "rgb(188,193,0)"),
        ((5, 10), "rgb(178,138,8)"),
        ((10, 15), "rgb(255,182,190)"),
        ((15, 20), "rgb(255,97,72)"),
        ((20, 25), "rgb(254,0,5)"),
        ((25, 30), "rgb(221,160,221)"),
        ((30, 35), "rgb(195,0,192)")
    ]


    # 线性退极化比的颜色映射
    LDR_color_scale = [
        ((-40, -35), "rgb(4,192,188)"),
        ((-35, -30), "rgb(101,148,236)"),
        ((-30, -25), "rgb(3,0,249)"),
        ((-25, -20), "rgb(143,239,140)"),
        ((-20, -15), "rgb(47,206,50)"),
        ((-15, -10), "rgb(2,128,2)"),
        ((-10, -5), "rgb(253,255,3)"),
        ((-5, 0), "rgb(160,159,57)"),
        ((0, 2), "rgb(186,132,17)"),
        ((2, 4), "rgb(255,180,193)"),
        ((4, 6), "rgb(249,98,68)"),
        ((6, 8), "rgb(251,2,0)"),
        ((8, 10), "rgb(225,157,225)"),
        ((10, 12), "rgb(195,0,193)")
    ]

    Z1_color_scale_hex = [
        ((-40, -35), "#00aca4"), 
        ((-35, -30), "#c0c0fe"), 
        ((-30, -25), "#7a72ee"), 
        ((-25, -20), "#1e26d0"), 
        ((-20, -15), "#a6fca8"), 
        ((-15, -10), "#00ea00"), 
        ((-10, -5), "#10921a"), 
        ((-5, 0), "#fcf464"), 
        ((0, 5), "#c8c802"), 
        ((5, 10), "#8c8c00"), 
        ((10, 15), "#feacad"), 
        ((15, 20), "#fe6454"), 
        ((20, 25), "#ee0230"), 
        ((25, 30), "#d48efe"), 
        ((30, 35), "#aa24fa")
    ]

    V1_color_scale_hex = [
        ((-7, -6), "#7ee0fe"), 
        ((-6, -5), "#00e0fe"), 
        ((-5, -4), "#00b0b0"), 
        ((-4, -3), "#00fe00"), 
        ((-3, -2), "#00c400"), 
        ((-2, -1), "#008000"), 
        ((-1, 0), "#d3d3d3"), 
        ((0, 1), "#a9a9a9"), 
        ((1, 2), "#fe0000"), 
        ((2, 3), "#fe5858"), 
        ((3, 4), "#feb0b0"), 
        ((4, 5), "#fe7c00"), 
        ((5, 6), "#fed200"), 
        ((6, 7), "#fefe00")
    ]

    W1_color_scale_hex = [
        ((0, 0.5), "#c0c0c0"), 
        ((0.5, 1), "#018102"), 
        ((1, 1.5), "#30ce34"), 
        ((1.5, 2), "#00fffc"), 
        ((2, 2.5), "#8acdea"), 
        ((2.5, 3), "#fa6543"), 
        ((3, 3.5), "#ffbfcc"), 
        ((3.5, 4), "#ffa200"), 
        ((4, 4.5), "#f9d902"), 
        ((4.5, 5), "#fffe00")
    ]

    SNR1_color_scale_hex = [
        ((-55, -50), "#830081"), 
        ((-50, -40), "#c0c0c0"), 
        ((-40, -35), "#00c1bd"), 
        ((-35, -30), "#b1c4dc"), 
        ((-30, -25), "#6496e5"), 
        ((-25, -20), "#0000fe"), 
        ((-20, -15), "#91ee8e"), 
        ((-15, -10), "#2dd033"), 
        ((-10, -5), "#027d07"), 
        ((-5, 0), "#fffe00"), 
        ((0, 5), "#bcc100"), 
        ((5, 10), "#b28a08"), 
        ((10, 15), "#ffb6be"), 
        ((15, 20), "#ff6148"), 
        ((20, 25), "#fe0005"), 
        ((25, 30), "#dda0dd"), 
        ((30, 35), "#c300c0")
    ]

    LDR_color_scale_hex = [
        ((-40, -35), "#04c0bc"), 
        ((-35, -30), "#6594ec"), 
        ((-30, -25), "#0300f9"), 
        ((-25, -20), "#8fef8c"), 
        ((-20, -15), "#2fce32"), 
        ((-15, -10), "#028002"), 
        ((-10, -5), "#fdff03"), 
        ((-5, 0), "#a09f39"), 
        ((0, 2), "#ba8411"), 
        ((2, 4), "#ffb4c1"), 
        ((4, 6), "#f96244"), 
        ((6, 8), "#fb0200"), 
        ((8, 10), "#e19de1"), 
        ((10, 12), "#c300c1")
    ]

    # 定义一个函数，用于创建自定义colormap和norm对象
    def create_custom_colormap(color_scale_corrected):
        """
        根据给定的颜色列表创建自定义colormap和norm对象。
        
        参数:
        - color_scale_corrected: 一个包含(范围, 颜色字符串)元组的列表。
        
        返回:
        - cmap: 自定义的colormap对象。
        - norm: 与colormap相对应的BoundaryNorm对象。
        - colors: 转换后的颜色列表。
        - boundaries: 颜色对应的边界值列表。
        """
        def convert_color(color_str):
            """
            安全地将颜色字符串（RGB或十六进制）转换为matplotlib可接受的格式。
            """
            if color_str in ["nan", "inf"]:
                # 返回白色
                return (1.0, 1.0, 1.0)
            # 检查是否为十六进制格式
            if color_str.startswith("#"):
                # 从十六进制转换
                color_str = color_str.lstrip("#")
                rgb = tuple(int(color_str[i:i+2], 16) for i in (0, 2, 4))
            else:
                # 从RGB字符串转换
                rgb_values = color_str.strip("rgb()").replace(" ", "").split(",")
                rgb = tuple(int(value) for value in rgb_values)
            return tuple(c / 255. for c in rgb)

        # 转换color_scale_corrected到matplotlib格式
        colors = [convert_color(c[1]) for c in color_scale_corrected]
        boundaries = [c[0][0] for c in color_scale_corrected] + [color_scale_corrected[-1][0][1]]

        # 创建自定义colormap
        cmap = mcolors.LinearSegmentedColormap.from_list("custom_cmap", colors)
        norm = mcolors.BoundaryNorm(boundaries, cmap.N)

        cmap.set_bad(color='white')  # 将NaN和Inf的颜色设置为白色

        return cmap, norm, colors, boundaries

    图像类型对应的源文件的key= {
                "雷达反射率": "Z1",
                "多普勒速度": "V1",
                "速度谱宽": "W1",
                "雷达信噪比": "SNR1",
                "线性退偏振比": "LDR"
            }




    cmap, norm, bounds, unit = cmap_dict[data_type]
    cmap, norm, colors, boundaries = create_custom_colormap(eval(f"{图像类型对应的源文件的key[data_type]}_color_scale_hex"))
    key = data_keys[data_type]
    title = f"{data_type} - {file_name}"

    if use_polar:
        max_dim = max(data.shape)
        img_side = max_dim
        extra_width = 150
        extra_height = 0

        total_width_px = img_side + extra_width
        total_height_px = img_side + extra_height
        distances = np.linspace(0, 2 * np.pi, data.shape[1])
        angles = np.arange(data.shape[0])
        r = np.linspace(0, data.shape[1], data.shape[1])
        theta = np.linspace(0, 2 * np.pi, data.shape[0])
        R, Theta = np.meshgrid(r, theta)

        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, dpi=dpi)
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.set_title(title)

        contourf_plot = ax.contourf(Theta, R, data, levels=boundaries, cmap=cmap, norm=norm)
        cb = fig.colorbar(contourf_plot, ticks=bounds, ax=ax)
        cb.ax.set_title(unit)
        ax.grid(True)
        plt.show()
    else:
        data_height, data_width = data.shape
        img_width_px = data_height
        img_height_px = data_width
        extra_width = 200
        extra_height = 70

        total_width_px = (img_width_px + extra_width) * 2 / dpi
        total_height_px = (img_height_px + extra_height) * 2 / dpi

        # 生成 X 和 Y 的坐标数据
        X, Y = np.meshgrid(np.arange(data.shape[0]), np.arange(data.shape[1]))

        fig, ax = plt.subplots(figsize=(total_width_px, total_height_px), dpi=dpi)
        ax.set_title(title)

        # 使用 contourf 进行绘制
        contourf_plot = ax.contourf(X, Y, data.T, levels=boundaries, cmap=cmap, norm=norm)

        cb = fig.colorbar(contourf_plot, ticks=bounds, ax=ax, pad=0.01, aspect=20)
        cb.ax.set_title(unit)
        ax.grid(False)

        plt.tight_layout()
        plt.show()

    
