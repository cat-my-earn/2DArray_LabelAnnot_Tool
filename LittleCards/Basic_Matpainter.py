from importall import *

def matpainter(data, data_type, use_polar, file_name="",dpi=100, save_path=None,edgedict=None):
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
