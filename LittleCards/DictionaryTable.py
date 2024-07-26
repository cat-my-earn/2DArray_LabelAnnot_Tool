from importall import *



class DictTableWidget(QWidget):
    """
    自定义控件，用于展示和编辑原始字典数据。
    
    参数:
    original_dict: 原始字典，用于初始化数据。如果是字符串，将从父控件中获取对应属性。如果不是字符串，直接使用。
    contextstr: 控件的上下文说明字符串。
    parent: 父控件，默认为None。
    parentup: 搜寻原始字典储存的父=控件类，用于更新原始字典，默认为None。
    colorselect: 是否启用颜色选择器，默认为False。使用颜色选择器的话，表格里值的部分将会是颜色选择器按钮，效果一样。
    """
    
    def __init__(self, original_dict, contextstr, parent=None ,parentup=None, colorselect = False):
        super().__init__(parent)
        
        self.parentup = parentup
        self.original_dict_notuse = original_dict
        self.colorselect = colorselect

        if isinstance(original_dict, str) and not hasattr(parentup, original_dict):
            logger.error(f'父控件中没有属性 {original_dict}，肯定哪里输错了，建议重输。')
        
        # 初始化原始字典和数据字典
        # 从parent类里面获取cfgobjextstr名字的属性
        self.objectflag = False
        if parent:
            if isinstance(original_dict, str) and hasattr(parentup, original_dict):
                logger.info(f'从父控件中获取了属性 {original_dict}')
                self.original_dict = getattr(parentup, original_dict)
                logger.info(f'从父控件中获取了属性 {original_dict}，值为 {self.original_dict}')
                self.objectflag = True
            else:
                self.original_dict = original_dict
        else:
            self.original_dict = {}
        self.data_dict = {}  # 初始化空字典，稍后将转换
        # 转换原始数据到字典格式
        self.convert_original_to_dict()
        # 初始化表格项变更的槽函数
        self.item_changed_slot = None  # 保存 itemChanged 信号连接的槽函数对象
        
        # 初始化表格
        self.table = TableWidget()
        self.table.setColumnCount(4)  # 设置列数为4
        self.table.verticalHeader().setVisible(False)  # 不显示垂直表头
        self.table.setHorizontalHeaderLabels(['序号', '键', '值', '操作'])  # 设置表头标签
        self.update_table(self.data_dict)  # 初始化表格数据
        
        # 初始化说明标签
        self.label = BodyLabel(contextstr)
        self.label.setAlignment(Qt.AlignCenter)  # 设置文字居中
        
        # 初始化添加行按钮，并连接点击事件
        button_layout = QHBoxLayout()
        self.add_row_button = PrimaryPushButton('添加行')
        self.add_row_button.clicked.connect(self.add_new_row)
        button_layout.addWidget(self.add_row_button)
        
        # 组合布局
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(button_layout)
        self.main_layout.addWidget(self.table)
        
        # 设置控件布局
        self.setLayout(self.main_layout)

        # 调整窗口高度
        self.adjust_height()

    def adjust_height(self):
        total_height = self.calculate_total_height() + 15 # 不知道为什么，获取的高度不足以显示完整，所以加了60
        self.setFixedHeight(total_height)

    def calculate_total_height(self):
        total_height = 0
        # 遍历布局中的所有控件
        for i in range(self.main_layout.count()):
            item = self.main_layout.itemAt(i)
            widget = item.widget() if item else None
            if widget:  # 确保是控件
                # 检查控件是否为表格
                if isinstance(widget, QTableWidget):
                    # 计算表格的总高度，包括所有行和表头
                    table_height = widget.horizontalHeader().height()  # 表头高度
                    for row in range(widget.rowCount()):
                        table_height += widget.rowHeight(row)  # 累加每一行的高度
                    if widget.horizontalScrollBar().isVisible():  # 如果水平滚动条可见
                        table_height += widget.horizontalScrollBar().height()  # 添加滚动条的高度
                    total_height += table_height
                else:
                    total_height += widget.sizeHint().height() + 20
        
        # 获取布局的间距和边距
        spacing = self.main_layout.spacing()
        margins = self.main_layout.contentsMargins()
        # 计算总高度，包括间距和上下边距
        total_height += (self.main_layout.count() - 1) * spacing  # 控件间的间距
        total_height += margins.top() + margins.bottom()  # 上下边距
        
        return total_height
    
    def convert_original_to_dict(self):
        # 将self.original_dict 转换为 self.data_dict 的形式
        self.data_dict.clear()  # 清空 self.data_dict
        for idx, (key, value) in enumerate(self.original_dict.items(), start=1):
            self.data_dict[idx] = {'key': key, 'value': value}
    
    
    def update_table(self, data_dict):
        self.table.clearContents()
        self.table.setRowCount(len(data_dict))  # 设置行数为字典长度
        
        # 断开之前的信号连接
        if self.item_changed_slot:
            self.table.itemChanged.disconnect(self.item_changed_slot)
        
        for row, (index, item) in enumerate(sorted(data_dict.items())):
            index_item = QTableWidgetItem(str(index))
            index_item.setTextAlignment(Qt.AlignCenter)  # 第一列居中对齐
            self.table.setItem(row, 0, index_item)  # 第一列是序号
            
            key_item = QTableWidgetItem(item['key'])
            key_item.setTextAlignment(Qt.AlignCenter)  # 第二列居中对齐
            self.table.setItem(row, 1, key_item)  # 第二列是键
            
            if self.colorselect:
                # 在for循环中，创建ColorPickerButton后
                color_button = ColorPickerButton(QColor(item['value']), item['value'], self, enableAlpha=False)
                color_button.colorChanged.connect(lambda color, idx=index: self.update_color(idx, color))

                # 创建一个QWidget作为容器
                widget = QWidget()
                # 创建一个水平布局
                layout = QHBoxLayout()
                # 将布局的对齐方式设置为居中
                layout.setAlignment(Qt.AlignCenter)
                # 将按钮添加到布局中
                layout.addWidget(color_button)
                # 将布局设置到QWidget容器中
                widget.setLayout(layout)

                # 将QWidget容器（现在包含按钮）设置为单元格的小部件
                self.table.setCellWidget(row, 2, widget)
            else:
                value_item = QTableWidgetItem(item['value'])
                value_item.setTextAlignment(Qt.AlignCenter)  # 第三列居中对齐
                self.table.setItem(row, 2, value_item)  # 第三列是值
            
            # 添加删除按钮到最后一列
            delete_button = TransparentPushButton(FIF.DELETE,"删除")
            delete_button.clicked.connect(lambda _, idx=index: self.delete_row(idx))
            self.table.setCellWidget(row, 3, delete_button)

        # 清除表格选中状态
        self.table.clearSelection()
        # 连接信号
        self.item_changed_slot = self.table.itemChanged.connect(self.update_dict_from_table)
    
    

    # 处理颜色改变信号
    def update_color(self, index, color):
        key = self.data_dict[index]['key']
        new_value = color.name()

        # 检查是否有重复的颜色
        for idx, item in self.data_dict.items():
            if idx != index and item['value'] == new_value:
                self.parentup.显示消息框函数("error", "警告", "已存在相同的颜色，请修改后再保存。", "右下", 5000)
                # 恢复原来的颜色
                current_color = QColor(item['value'])
                self.table.cellWidget(idx - 1, 2).setColor(current_color)
                return

        # 更新self.data_dict中的值
        self.data_dict[index]['value'] = new_value

        # 更新self.original_dict中对应的值
        self.original_dict[key] = new_value
        if self.objectflag:
            setattr(self.parentup, self.original_dict_notuse, self.original_dict)

        logger.info(f'更新原始字典中键 {key} 的颜色值为 {new_value}')
        logger.info(f'当前字典内容：{self.original_dict}')


    # 删除特定行
    def delete_row(self, index):
        if index not in self.data_dict:
            logger.error(f'试图删除无效索引 {index}')
            return
        logger.info(f'删除序号为 {index} 的行')
        del_key = self.data_dict[index]['key']
        logger.info(f'删除的键为 {del_key}')
        logger.info(f'删除的对象为 {self.data_dict[index]}')
        del_value = self.data_dict[index]['value']
        
        del self.data_dict[index]
        
        # 更新self.original_dict中对应的键值对
        del self.original_dict[del_key]
        logger.debug(f"更新标志位：{self.objectflag}，更新属性名：{self.original_dict_notuse}")
        if self.objectflag:
            setattr(self.parentup, self.original_dict_notuse, self.original_dict)
        
        # 更新表格显示
        self.update_table(self.data_dict.copy())
        self.update_row_indices()  # 更新所有行的序号
        self.update_table(self.data_dict.copy())
        
        
        logger.info(f'从字典中删除了序号为 {index} 的行')
        logger.info(f'当前字典内容：{self.original_dict}')
        logger.info(f'当前表格内容：{self.data_dict}')
    
    # 添加新行，默认内容
    def add_new_row(self):
        """
        向表格中添加新行，并在字典中记录相应的键值对。
        新行的键和值基于已有最大键值加一生成，确保唯一性。
        如果生成的键或值与已有项重复，将提示用户并取消添加。
        """
        self.table.itemChanged.disconnect(self.item_changed_slot)
        # 收集现有行中键的数字部分以确定新行的键值
        existing_indexes = []
        for row in range(self.table.rowCount()):
            # 假设键存储在第一列
            key = self.table.item(row, 1).text()
            # 提取键名中的数字部分
            try:
                index = int(''.join(filter(str.isdigit, key)))
            except ValueError:
                continue
            existing_indexes.append(index)

        logger.info(f'现有键的数字部分：{existing_indexes}')
        
        # 查找不存在于现有键中的最小整数键值
        # 从1开始查找不在existing_indexes中的最小数字
        default_index = 1
        while default_index in existing_indexes:
            default_index += 1
        
        # 根据默认索引生成新的键和值
        default_key = f'key{default_index}'
        default_value = f'value{default_index}'
        if self.colorselect:
            default_value = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)).name()
        
        # 检查新生成的键或值是否已存在于字典中
        # 检查新增的键和值是否已存在
        if any(item['key'] == default_key or item['value'] == default_value for item in self.data_dict.values()):
            self.parentup.显示消息框函数("error","警告","新行的键或值已存在，请将原来的键对应的值修改完再添加。","右下",5000)
            return
        
        # 在字典中添加新的键值对
        self.data_dict[default_index] = {'key': default_key, 'value': default_value}
        
        # 更新self.original_dict中的对应值
        self.original_dict[default_key] = default_value
        logger.debug(f"更新标志位：{self.objectflag}，更新属性名：{self.original_dict_notuse}")
        if self.objectflag:
            setattr(self.parentup, self.original_dict_notuse, self.original_dict)
        
        # 在表格中插入新行并设置相应单元格的值
        self.table.insertRow(self.table.rowCount())
        
        index_item = QTableWidgetItem(str(default_index))
        index_item.setTextAlignment(Qt.AlignCenter)  # 设置序号居中
        self.table.setItem(self.table.rowCount() - 1, 0, index_item)
        
        key_item = QTableWidgetItem(default_key)
        key_item.setTextAlignment(Qt.AlignCenter)  # 设置键居中
        self.table.setItem(self.table.rowCount() - 1, 1, key_item)
        
        # 替换为随机颜色的按钮
        if self.colorselect:
            # 生成随机颜色按钮
            color_button = ColorPickerButton(default_value, default_value, self, enableAlpha=False)
            color_button.colorChanged.connect(lambda color, idx=index: self.update_color(idx, color))

            # 创建一个QWidget作为容器
            widget = QWidget()
            # 创建一个水平布局
            layout = QHBoxLayout()
            # 将布局的对齐方式设置为居中
            layout.setAlignment(Qt.AlignCenter)
            # 将按钮添加到布局中
            layout.addWidget(color_button)
            # 将布局设置到QWidget容器中
            widget.setLayout(layout)

            # 将QWidget容器（现在包含按钮）设置为单元格的小部件
            self.table.setCellWidget(self.table.rowCount() - 1, 2, widget)
        else:
            value_item = QTableWidgetItem(default_value)
            value_item.setTextAlignment(Qt.AlignCenter)  # 设置值居中
            self.table.setItem(self.table.rowCount() - 1, 2, value_item)
        
        # 在新行的最后列添加删除按钮
        delete_button = TransparentPushButton(FIF.DELETE,"删除")
        delete_button.clicked.connect(lambda _, idx=index: self.delete_row(idx))
        self.table.setCellWidget(self.table.rowCount() - 1, 3, delete_button)

        self.item_changed_slot = self.table.itemChanged.connect(self.update_dict_from_table)

        # 输出添加的新行信息
        logger.info(f'向字典中添加了新行，序号为 {default_index}')
        logger.info(f'当前字典内容：{self.original_dict}')
        
        # 更新表格显示
        self.update_row_indices()  # 更新所有行的序号
        self.update_table(self.data_dict.copy())
        
    # 更新所有行的序号
    def update_row_indices(self):
        self.data_dict.clear()  # 清空原有字典
        for row in range(self.table.rowCount()):
            new_index = row + 1  # 从1开始的序号
            item = QTableWidgetItem(str(new_index))
            item.setTextAlignment(Qt.AlignCenter)  # 设置文本居中
            self.table.setItem(row, 0, item)
            key = self.table.item(row, 1).text()
            # 检查单元格是否有小部件，并且该小部件是否包含布局
            if isinstance(self.table.cellWidget(row, 2), QWidget) and self.table.cellWidget(row, 2).layout() is not None:
                widget = self.table.cellWidget(row, 2)
                layout = widget.layout()
                # 假设ColorPickerButton是布局中的第一个（也可能是唯一一个）小部件
                color_button = layout.itemAt(0).widget()
                if isinstance(color_button, ColorPickerButton):
                    # 从颜色选择按钮获取颜色值
                    color = color_button.color  # 直接对按钮对象.color可以获得对应的pyside6 QColor 对象
                    value = color.name()  # 获取颜色的十六进制字符串
            else:
                value = self.table.item(row, 2).text()
            self.data_dict[new_index] = {'key': key, 'value': value}
        
        logger.info(f'更新所有行的序号，当前字典内容：{self.data_dict}')
    
    # 从表格更新字典内容
    def update_dict_from_table(self, item):
        if item.column() == 1:  # 第二列是键
            row = item.row()
            if row >= len(self.data_dict):
                return
            
            index = int(self.table.item(row, 0).text())
            new_key = item.text()
            
            old_key = self.data_dict[index]['key']
            
            # 检查是否有重复的键
            for key, value in self.data_dict.items():
                if key != index and value['key'] == new_key:
                    self.parentup.显示消息框函数("error","警告","已存在相同的键，请修改后再保存。","右下",5000)
                    item.setText(old_key)  # 恢复原来的值
                    return
            
            # 更新self.data_dict中的键
            self.data_dict[index]['key'] = new_key
            
            # 更新self.original_dict中对应的键值
            del self.original_dict[old_key]
            self.original_dict[new_key] = self.data_dict[index]['value']
            if self.objectflag:
                setattr(self.parentup, self.original_dict_notuse, self.original_dict)
            
            logger.info(f'更新原始字典中键 {old_key} 为 {new_key}，当前内容：{self.original_dict}')
            logger.info(f'更新字典中序号为 {index} 的键为 {new_key}')
        
        elif item.column() == 2:  # 第三列是值
            row = item.row()
            if row >= len(self.data_dict):
                return
            
            index = int(self.table.item(row, 0).text())
            new_value = item.text()
            
            # 检查是否有重复的值
            for key, value in self.data_dict.items():
                if key != index and value['value'] == new_value:
                    self.parentup.显示消息框函数("error","警告","已存在相同的值，请修改后再保存。","右下",5000)
                    item.setText(self.data_dict[index]['value'])  # 恢复原来的值
                    return
            
            # 更新self.data_dict中的值
            self.data_dict[index]['value'] = new_value
            
            # 更新self.original_dict中对应的值
            self.original_dict[self.data_dict[index]['key']] = new_value
            if self.objectflag:
                setattr(self.parentup, self.original_dict_notuse, self.original_dict)
            
            logger.info(f'更新原始字典中键 {self.data_dict[index]["key"]} 的值为 {new_value}，当前内容：{self.original_dict}')
            logger.info(f'更新字典中序号为 {index} 的值为 {new_value}')


    def resizeEvent(self, event):
        # 重写resizeEvent方法以调整列宽
        total_width = self.width() - 20  # 获取QWidget的当前宽度（全满居然会出现滑动条……所以要减掉一点）
        column_width = total_width // 4   # 计算前三列的宽度
        last_column_width = total_width - (column_width * 3)  # 计算最后一列的宽度，以吸收可能的余数

        # 设置前三列的宽度
        for i in range(3):
            self.table.setColumnWidth(i, column_width)
        # 设置最后一列的宽度
        self.table.setColumnWidth(3, last_column_width)

        super().resizeEvent(event)  # 调用父类的resizeEvent方法
