from importall import *


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
    dataTransferComplete = Signal()  # 数据传输完成信号

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

        for i in range(total_chunks):
            chunk = compressed_data[i * chunk_size:(i + 1) * chunk_size]
            encoded_chunk = base64.b64encode(chunk).decode('utf-8')  # 将字节数据转换为base64字符串
            logger.info(f"正在发送 {i + 1} 个数据块，总数据块为 {total_chunks}")
            self.sendChunkToJS.emit(encoded_chunk, i, total_chunks)  # 发送base64字符串数据块
        
        self.dataTransferComplete.emit()

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