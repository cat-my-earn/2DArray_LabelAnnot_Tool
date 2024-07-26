from importall import *


# 大佬的ui没法实现进度条类，我只能自己写一个，哎，写了好多
class ProgressFlyoutView(FlyoutViewBase):
    def __init__(self, parent=None, startfunc=None, pausefunc=None, finishfunc=None):
        super().__init__(parent)
        self.startfunc = startfunc  # 开始按钮的回调函数
        self.pausefunc = pausefunc  # 暂停按钮的回调函数
        self.finishfunc = finishfunc  # 结束按钮的回调函数
        self.start_time = None  # 记录开始时间
        self.elapsed_time = timedelta()  # 记录已消耗时间
        self.timer = QTimer()  # 定时器用于更新时间
        self.timer.timeout.connect(self.update_time)  # 连接定时器的超时信号到更新时间的槽函数
        self.files_processed = 0  # 已处理文件数
        self.start_processing_time = None  # 记录处理开始时间
        self.totle_files = 100  # 总文件数
        self.now_filename = "待加载"  # 当前文件名
        self.progress_exist = True  # 进度条是否存在
        self.keynote = ""
        self.Oprah = ""
        self.labelstart = "批处理开始"
        self.labelpaus_stop = "批处理暂停"
        self.labelpaus_restart = "批处理继续"
        self.labelfinish = "批处理已结束"
        self.beforestart = "这里将会显示进度信息"

        # 垂直布局
        self.vBoxLayout = QVBoxLayout(self)

        # 文字信息标签
        self.label = BodyLabel(self.beforestart)
        self.label.setAlignment(Qt.AlignCenter)  # 设置文本居中
        self.vBoxLayout.addWidget(self.label)

        # 进度条
        self.progressBar = ProgressBar()
        self.progressBar.setRange(0, self.totle_files)
        self.vBoxLayout.addWidget(self.progressBar)

        # 横向布局用于按钮
        hBoxLayout = QHBoxLayout()

        # 添加按钮
        self.startButton = PushButton("开始")
        self.pauseButton = PushButton("暂停")
        self.resetButton = PushButton("终止")

        # 在按钮两侧添加弹性空间
        hBoxLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        hBoxLayout.addWidget(self.startButton)
        hBoxLayout.addWidget(self.pauseButton)
        hBoxLayout.addWidget(self.resetButton)
        hBoxLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # 将按钮布局添加到垂直布局
        self.vBoxLayout.addLayout(hBoxLayout)

        # 设置默认大小
        self.setFixedSize(500, 250)

        # 连接按钮信号到槽函数
        self.startButton.clicked.connect(self.start_progress)
        self.pauseButton.clicked.connect(self.pause_or_resume_progress)
        self.resetButton.clicked.connect(self.reset_progress)

    def start_progress(self):
        # 处理开始进度
        self.progress_exist = True  # 进度条是否存在
        self.progressBar.setValue(0)  # 设置进度条初始值为0
        self.label.setText(self.labelstart)  # 更新标签文本
        self.start_time = datetime.now()  # 记录开始时间
        self.start_processing_time = self.start_time  # 记录处理开始时间
        self.timer.start(1000)  # 每秒更新一次
        self.startButton.hide()  # 隐藏开始按钮
        if self.startfunc:
            logger.info("开始调用批处理函数")
            self.startfunc()  # 调用开始回调函数

    def pause_or_resume_progress(self):
        if self.timer.isActive():
            # 暂停进度
            self.label.setText(self.labelpaus_stop)  # 更新标签文本
            self.elapsed_time += datetime.now() - self.start_time  # 更新已消耗时间
            self.timer.stop()  # 停止定时器
            self.pauseButton.setText("继续")  # 更新按钮文本
            if self.pausefunc:
                self.pausefunc(False)  # 调用暂停回调函数
        else:
            # 恢复进度
            self.label.setText(self.labelpaus_restart)  # 更新标签文本
            self.start_time = datetime.now()  # 重新记录开始时间
            self.timer.start(1000)  # 重新启动定时器
            self.pauseButton.setText("暂停")  # 更新按钮文本
            if self.pausefunc:
                self.pausefunc(True)  # 调用暂停回调函数

    def reset_progress(self):
        # 处理重置进度
        self.progressBar.setValue(0)  # 重置进度条
        self.label.setText(self.labelfinish)  # 更新标签文本
        self.timer.stop()  # 停止定时器
        self.start_time = None  # 重置开始时间
        self.elapsed_time = timedelta()  # 重置已消耗时间
        self.pauseButton.setText("暂停")  # 恢复暂停按钮文本
        self.progress_exist = False  # 进度条不存在
        self.startButton.show()
        if self.finishfunc:
            self.finishfunc()  # 调用结束回调函数

    def update_time(self):
        if self.start_time:
            current_time = datetime.now()  # 获取当前时间
            self.elapsed_time += current_time - self.start_time  # 更新已消耗时间
            self.start_time = current_time  # 重新记录开始时间
            self.update_label_info()  # 更新标签信息

    def update_label_info(self):
        if self.totle_files  <= self.files_processed:
            self.progress_exist = False
            self.timer.stop()
            self.label.setText("批处理已结束")  # 更新标签文本
            self.reset_progress()

        if self.files_processed > 0 and self.start_processing_time:
            # 计算平均每个文件处理时间
            total_processing_time = datetime.now() - self.start_processing_time
            avg_time_per_file = total_processing_time.total_seconds() / self.files_processed
        else:
            avg_time_per_file = 0

        self.progressBar.setValue(self.files_processed)
        remaining_files = self.totle_files - self.files_processed  # 计算剩余文件数量

        if avg_time_per_file > 0:
            remaining_time = remaining_files * avg_time_per_file  # 计算剩余时间
            estimated_completion_time = datetime.now() + timedelta(seconds=remaining_time)  # 计算预计完成时间
            estimated_completion_time_str = estimated_completion_time.strftime("%Y-%m-%d %H:%M:%S")  # 将预计完成时间格式化为字符串
        else:
            remaining_time = 0
            estimated_completion_time_str = "未知"

        def format_time(days, hours, minutes, seconds):
            """格式化时间，忽略值为0的部分"""
            parts = []
            if days > 0:
                parts.append(f"{days}天")
            if hours > 0:
                parts.append(f"{hours}小时")
            if minutes > 0:
                parts.append(f"{minutes}分钟")
            if seconds > 0:
                parts.append(f"{seconds}秒")
            return " ".join(parts) if parts else "0秒"

        # 假设remaining_time是剩余时间的秒数
        remaining_time_seconds = remaining_time  # 从你的代码或计算中获取剩余秒数

        # 创建timedelta对象
        td = timedelta(seconds=remaining_time_seconds)

        # 获取天数、小时数、分钟数、秒数
        days = td.days
        hours = td.seconds // 3600
        minutes = (td.seconds % 3600) // 60
        seconds = (td.seconds % 3600) % 60

        # 格式化预计剩余时间
        formatted_remaining_time = format_time(days, hours, minutes, seconds)

        # 假设elapsed_time和avg_time_per_file是已经计算好的值
        # 例如:
        # elapsed_time = 12345  # 已消耗时间的秒数
        # avg_time_per_file = 123  # 平均每个文件消耗时间的秒数

        # 格式化已消耗时间和平均每个文件消耗时间
        elapsed_td = self.elapsed_time
        avg_td = timedelta(seconds=avg_time_per_file)

        formatted_elapsed_time = format_time(elapsed_td.days, elapsed_td.seconds // 3600, (elapsed_td.seconds % 3600) // 60, (elapsed_td.seconds % 3600) % 60)
        formatted_avg_time_per_file = format_time(avg_td.days, avg_td.seconds // 3600, (avg_td.seconds % 3600) // 60, (avg_td.seconds % 3600) % 60)

        self.label.setText(
            f"{self.keynote}\n"
            f"当前运行的操作：{self.Oprah}\n"
            f"总共文件数：{self.totle_files}\n"  # 显示总文件数
            f"当前操作的文件名：{self.now_filename}\n"  # 当前文件名
            f"已处理文件数：{self.files_processed}\n"  # 已处理文件数
            f"已消耗时间：{formatted_elapsed_time}\n"  # 已消耗时间
            f"平均每个文件消耗时间：{formatted_avg_time_per_file}\n"  # 平均每个文件消耗时间
            f"预计还需要处理多久：{formatted_remaining_time}\n"  # 预计剩余时间
            f"预计完成时间：{estimated_completion_time_str}"  # 预计完成时间
        )

    def set_files_processed(self, files_processed, now_filename):
        # 设置已处理文件数
        self.progressBar.setRange(0, self.totle_files)
        self.files_processed = files_processed
        self.now_filename = now_filename
        self.update_label_info()  # 更新进度信息
