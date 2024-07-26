from importall import *
def matpainter(data, data_type, use_polar, file_name="",dpi=100, save_path=None,edgedict=None):
    logger.info(f"正在绘制{data_type}图像")
    """
    :param data: 数据-一个二维数组
    :param data_type: 数据类型（中文名字）
    :param use_polar: 是否使用极坐标绘图。True 表示使用极坐标，False 表示使用直角坐标
    :param file_name: 当前绘制的文件的文件名
    :param dpi: 图像分辨率
    :param save_path: 保存路径
    :param edgedict: 边缘坐标点集字典
    """
    if use_polar == True and data_type == '线性退偏振比':
        return
    if use_polar == True:
        # 定义颜色映射
        color_list = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        ]
        cmap = mcolors.ListedColormap(color_list)

        # 获取字段数据
        field_data = data

        # 创建极坐标图
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})

        # 准备绘制极坐标图的参数
        azimuth_angles = np.linspace(0, 2 * np.pi, 360, endpoint=False)  # 方位角从0到2π

        # 定义径向坐标点
        range_values = np.linspace(0, 16, num=field_data.shape[1])  # 假设的距离值
        radial_grid, azimuth_grid = np.meshgrid(range_values, azimuth_angles)

        # 确定数据的最小值和最大值以用于归一化
        data_min = np.nanmin(field_data)  # 忽略NaN值的最小值
        data_max = np.nanmax(field_data)  # 忽略NaN值的最大值

        # 色标和归一化参数的映射
        cmap_dict = {
            "雷达反射率":  'dBZ',
            "多普勒速度": 'm/s',
            "速度谱宽": 'm/s',
            "雷达信噪比": 'dBZ',
            "线性退偏振比":  'dB'
        }

        unit = cmap_dict[data_type]

        if unit == "m/s":
            cbar_label = 'Velocity (m/s)'
        elif unit == 'dBZ':
            cbar_label = 'Intensity (dBZ)'
        else:
            cbar_label = "Intensity (dB)"

        # 创建归一化对象
        norm = mcolors.Normalize(vmin=data_min, vmax=data_max, clip=True)

        # 绘制图形
        cax = ax.pcolormesh(azimuth_grid, radial_grid, field_data, shading='auto', cmap=cmap, norm=norm)

        # 添加色标，并设置单位
        cbar = plt.colorbar(cax, ax=ax, orientation='vertical')
        cbar.set_label(cbar_label)

        # 设置色标的刻度和标签
        num_ticks = 10
        tick_values = np.linspace(data_min, data_max, num=num_ticks)
        tick_labels = [f'{tick:.2f}' for tick in tick_values]
        cbar.set_ticks(tick_values)
        cbar.set_ticklabels(tick_labels)

        # 设置极坐标的角度刻度
        angle_ticks = np.arange(0, 360, 45)
        angle_labels = ['{:3d}°'.format(t) for t in angle_ticks]
        ax.set_thetagrids(angle_ticks, labels=angle_labels)

        # 设置标题
        ax.set_title(f'PPI Radar Data - {data_type}', va='bottom')

        ax.set_theta_offset(np.pi / 2)  # 起始角度顺时针旋转90度
        ax.set_theta_direction(-1)  # 角度方向逆时针

        # 设置标题，显示npz文件的文件名
        ax.set_title(f'{data_type} - {os.path.splitext(file_name)[0]}', va='bottom')

        # 添加最大值和最小值的文本标签
        ax.text(0.5, 1.1, f'Min: {data_min:.2f} {unit}', transform=ax.transAxes, ha='center', fontsize=12)
        ax.text(0.5, -0.1, f'Max: {data_max:.2f} {unit}', transform=ax.transAxes, ha='center', fontsize=12)

        # 保存图形到子文件夹，使用JPG格式
        plt.show()
    else:
        图像类型对应的源文件的key = {
"雷达反射率": "Z1",
"多普勒速度": "V1",
"速度谱宽": "W1",
"雷达信噪比": "SNR1",
"线性退偏振比": "LDR"
}

        # 定义字段和对应的颜色列表
        fields_colors = {
            'Z1': ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#C0C0C0",
                "#808080", "#800000", "#808000", "#008000", "#000080", "#800080",
                "#008080", "#C0C000", "#C000C0", "#0000C0", "#00C0C0", "#FFC0C0"],
            'SNR1': ["#FF0000", "#EE0000", "#CD0000", "#8B0000", "#800000", "#808000",
                    "#000080", "#0000CD", "#0000EE", "#0000FF", "#00FFFF", "#00EEFF",
                    "#90EE90", "#00CDFF", "#4B0082", "#FF1493", "#FF69B4", "#FFC0CB"],
            'LDR': ["#FF0000", "#FF5733", "#FFA500", "#FFFF00", "#00FF00", "#00FA9A",
                    "#00BFFF", "#1E90FF", "#0000FF", "#4B0082", "#8A2BE2", "#FF69B4",
                    "#DC143C", "#FFC0CB", "#F0E68C", "#ADFF2F", "#7CFC00"],
            'V1': ["#FF6347", "#4682B4", "#87CEEB", "#32CD32", "#FFD700", "#FF69B4",
                "#FF1493", "#4B0082", "#00BFFF", "#00FF00", "#FFFF00", "#00FFFF",
                "#800080", "#808000", "#A52A2A", "#000000"],
            'W1': ["#FF4500", "#4B0082", "#00FA9A", "#00BFFF", "#FFFF00", "#FFD700",
                "#FF69B4", "#8A2BE2", "#FF1493", "#ADFF2F", "#7CFC00"],
        }

        # 为每个字段定义色标区间的数量，这里设置的是区间数量
        fields_intervals = {
            'Z1': 16,  # 需要16个区间，对应15种颜色
            'SNR1': 16,  # 需要16个区间，对应15种颜色
            'LDR': 16,  # 需要16个区间，对应15种颜色
            'V1': 15,   # 需要15个区间，对应14种颜色
            'W1': 10,   # 需要10个区间，对应9种颜色
}
        Z = data.astype(np.float64)
        Z = Z.T
        Z[Z == 0] = np.nan

        # 找到数据的最大值和最小值，忽略NaN
        min_value = np.nanmin(Z)
        max_value = np.nanmax(Z)

        # 计算色标区间
        intervals = fields_intervals[图像类型对应的源文件的key[data_type]]
        boundaries = np.linspace(min_value, max_value, intervals + 1)
        cmap = mcolors.ListedColormap(fields_colors[图像类型对应的源文件的key[data_type]])
        norm = mcolors.BoundaryNorm(boundaries=boundaries, ncolors=intervals)

        # 创建图像和轴对象，可以在这里调整figsize来改变子图大小
        fig, ax = plt.subplots(figsize=(40, 20))  # 例如，设置为(12, 8)

        # 绘图
        CS = ax.contourf(np.linspace(0, 24, Z.shape[1]), np.linspace(0, 16, Z.shape[0]), Z, cmap=cmap, norm=norm)

        # 添加色标
        cbar = fig.colorbar(CS, ax=ax, orientation='horizontal', pad=0.1)
        cbar.set_label(f'Value [{图像类型对应的源文件的key[data_type]}]')

        # 设置X轴刻度显示0-24小时数
        ax.set_xticks(np.linspace(0, 24, 25))  # 设置25个刻度
        ax.set_xticklabels([f'{i}' for i in range(25)])  # 设置刻度标签为0-24

        # 设置图表标题和坐标轴标签
        ax.set_title(f'{图像类型对应的源文件的key[data_type]} Factor\nMin: {min_value:.2f}, Max: {max_value:.2f}')
        ax.set_xlabel('Time (hours)')
        ax.set_ylabel('Height (km)')

        # 设置刻度标签的字体大小
        for label in ax.get_xticklabels():
            label.set_fontsize(12)
        for label in ax.get_yticklabels():
            label.set_fontsize(12)

        # 保存图像和数据文件到与原始npz数据文件夹同名的文件夹中
        plt.show()