import math
import sys
from PyQt5.QtCore import Qt, QRect, QPoint, QTimer
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPolygon, QTextDocument, QPainterPath
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QHBoxLayout, QPushButton


class Neuron_layer(QWidget):
    def __init__(self, parent=None):
        super(Neuron_layer, self).__init__(parent)

        self.center_x = 600  # 箭头起点x坐标

        # 初始位置
        self.start_x = [552.5, 552.5, 540, 540, 515, 515, 477, 477]  # 起始x位置（右侧）
        self.end_x = [200, 200, 200, 200, 200, 200, 200, 200]  # 结束x位置（左侧）
        self.current_x = [self.start_x[i] for i in range(8)]  # 当前x位置

        self.start_x_new = [1000, 1000]  # 起始x位置（右侧）
        self.end_x_new = [552.5, 527.5]
        self.current_x_new = [self.start_x_new[i] for i in range(2)]

        # 所有原始块的信息
        self.block_start_y = 200
        self.y_spacing = 50

        self.layer_counts = [2, 2, 2, 2, 2, 2, 2, 2]  # 每个块的层数
        self.neuron_counts = [2, 2, 3, 3, 5, 5, 8, 8]  # 每个块的神经元数量
        self.sizes = [2.5, 2.5, 3.75, 3.75, 6.25, 6.25, 10.0, 10.0]  # 每个块的大小
        self.replace = [False, False, False, True, False, False, False, True]  # 是否替换块
        self.neuron_counts_new = [2, 4]  # 替换块的神经元数量

        self.widths = [200, 200, 200, 200, 200, 200, 200, 200]  # 每个块的宽度
        self.heights = [70, 70, 70, 70, 70, 70, 70, 70]  # 每个块的高度
        self.cur_ys = [self.block_start_y]  # 每个块的y坐标

        y_sum = self.block_start_y
        for idx, h in enumerate(self.heights):
            if idx == len(self.heights) - 1:
                break
            y_sum += h + self.y_spacing
            self.cur_ys.append(y_sum)

        # 移动控制
        self.speed = 5  # 移动速度（像素/帧）
        self.is_moving1 = False
        self.is_moving2 = False

        # 设置定时器
        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.update_position1)
        self.timer1.setInterval(20)  # 约30FPS

        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.update_position2)
        self.timer2.setInterval(20)  # 约30FPS

        # 窗口属性
        self.setAttribute(Qt.WA_TranslucentBackground)  # 启用透明度支持
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框（可选）

    def calculate_circle_radius(self, width, height, layer_count, neuron_count):
        """根据可用空间自动计算合适的圆形半径"""
        # 计算每个神经元层的灰色矩形高度
        box_height = (height - 20 * (layer_count + 1)) / layer_count  # 减去上下边距

        # 计算水平间距
        box_width = width - 20  # 减去左右边距
        horizontal_space = box_width / (neuron_count + 1)

        # 计算最大可能半径（不超过灰色矩形高度的一半）
        max_radius_from_height = box_height * 0.4  # 保留20%的边距
        max_radius_from_width = horizontal_space * 0.4

        # 取两者中较小的值
        circle_radius = min(max_radius_from_height, max_radius_from_width)

        # 限制在5到20像素范围内
        return max(5, min(20, circle_radius))

    def start_movement(self):
        """开始移动和透明度变化"""
        self.current_x = [self.start_x[i] for i in range(8)]
        self.current_x_new = [self.start_x_new[i] for i in range(2)]

        self.is_moving1 = True
        self.is_moving2 = True
        self.timer1.start()
        self.timer2.start()

    def reset(self):
        """重置到初始状态"""
        self.timer1.stop()
        self.timer2.stop()

        self.current_x = [self.start_x[i] for i in range(8)]
        self.current_x_new = [self.start_x_new[i] for i in range(2)]

        self.is_moving1 = False
        self.is_moving2 = False
        self.update()  # 触发重绘

    def update_position1(self):
        """更新位置和透明度"""
        if not self.is_moving1:
            return

        # 更新位置（向右移动）
        # self.current_x_1 -= self.speed
        # self.current_x_2 -= self.speed
        # self.current_x_3 -= self.speed
        self.current_x[3] -= self.speed
        # self.current_x_5 -= self.speed
        # self.current_x_6 -= self.speed
        # self.current_x_7 -= self.speed
        # self.current_x_8 -= self.speed

        self.current_x_new[0] -= self.speed
        # self.current_x_new_2 -= self.speed

        # 到达终点时停止
        if self.current_x_new[0] <= self.end_x_new[0]:
            self.current_x_new[0] = self.end_x_new[0]
            self.is_moving1 = False
            self.timer1.stop()

        self.update()  # 触发重绘

    def update_position2(self):
        """更新位置和透明度"""
        if not self.is_moving2:
            return

        # 更新位置（向右移动）
        self.current_x[7] -= self.speed
        self.current_x_new[1] -= self.speed

        # 到达终点时停止
        if self.current_x_new[1] <= self.end_x_new[1]:
            self.current_x_new[1] = self.end_x_new[1]
            self.is_moving2 = False
            self.timer2.stop()

        self.update()  # 触发重绘

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        self.draw_io_name(painter, self.block_start_y)

        # 绘制块
        for i in range(len(self.cur_ys)):
            self.draw_neuron_block(
                painter=painter,
                cur_x=self.current_x[i],
                cur_y=self.cur_ys[i],
                s_x=self.start_x[i],
                e_x=self.end_x[i],
                width=self.widths[i],
                height=self.heights[i],
                is_new=False,
                layer_count=self.layer_counts[i],
                neuron_count=self.neuron_counts[i],
            )

        # 替换块 1
        width_1_new = 170
        height_1_new = self.heights[3]
        self.draw_neuron_block(
            painter=painter,
            cur_x=self.current_x_new[0],
            cur_y=self.cur_ys[3],
            s_x=self.start_x_new[0],
            e_x=self.end_x_new[0],
            width=width_1_new,
            height=height_1_new,
            is_new=True,
            layer_count=2,
            neuron_count=self.neuron_counts_new[0],
        )

        # 替换块 2
        width_2_new = 145
        height_2_new = self.heights[7]
        self.draw_neuron_block(
            painter=painter,
            cur_x=self.current_x_new[1],
            cur_y=self.cur_ys[7],
            s_x=self.start_x_new[1],
            e_x=self.end_x_new[1],
            width=width_2_new,
            height=height_2_new,
            is_new=True,
            layer_count=2,
            neuron_count=self.neuron_counts_new[1],
        )

        # 绘制箭头连接到下一个层块
        for idx, y in enumerate(self.cur_ys):
            if idx == 0:
                continue
            self.draw_arrow(painter, QPoint(self.center_x, y - self.y_spacing), QPoint(self.center_x, y))

        # 绘制块名称
        text_spacing = 200
        for i in range(len(self.cur_ys)):
            self.draw_block_name(
                painter=painter,
                cur_x=self.current_x[i] - text_spacing,
                cur_y=self.cur_ys[i],
                s_x=self.start_x[i] - text_spacing,
                e_x=self.end_x[i] - text_spacing,
                width=self.widths[i],
                height=self.heights[i],
                idx_name=f"Block: b_{{{i + 1}, 0}}",
                size_name=f"Size: {self.sizes[i]}MB",
                is_new=False,
                replace=self.replace[i]
            )

        # 绘制替换块名称
        self.draw_block_name(
            painter=painter,
            cur_x=self.current_x_new[0] - text_spacing,
            cur_y=self.cur_ys[3],
            s_x=self.start_x_new[0] - text_spacing,
            e_x=self.end_x_new[0] - text_spacing,
            width=width_1_new,
            height=height_1_new,
            idx_name="Block: b_{4, 1}",
            size_name=f"Size: {self.sizes[3] * self.neuron_counts_new[0] / self.neuron_counts[3]}MB",
            is_new=True,
            replace=True
        )

        self.draw_block_name(
            painter=painter,
            cur_x=self.current_x_new[1] - text_spacing,
            cur_y=self.cur_ys[7],
            s_x=self.start_x_new[1] - text_spacing,
            e_x=self.end_x_new[1] - text_spacing,
            width=width_2_new,
            height=height_2_new,
            idx_name="Block: b_{8, 1}",
            size_name=f"Size: {self.sizes[7] * self.neuron_counts_new[1] / self.neuron_counts[7]}MB",
            is_new=True,
            replace=True
        )

    def draw_io_name(self, painter, block_start_y):
        """绘制输入输出名称"""
        # 绘制输入文本框（在第一个块上方）
        in_rect_width = 200
        input_rect = QRect(self.center_x - in_rect_width / 2, block_start_y - self.y_spacing - 60, in_rect_width, 60)
        painter.setPen(QPen(Qt.black, 2))
        # painter.drawRect(input_rect)

        # 绘制输入文本
        input_doc = QTextDocument()
        input_doc.setPlainText("Input image")
        input_font = painter.font()
        input_font.setFamily("Arial")
        input_font.setPointSize(14)
        input_font.setBold(False)
        input_doc.setDefaultFont(input_font)
        input_doc.setTextWidth(input_rect.width())

        # 计算文本居中位置
        x_offset = input_rect.width() / 4  # 水平居中偏移
        y_offset = input_rect.height() / 4  # 垂直居中偏移

        painter.save()
        # 先平移坐标系到矩形左上角，再应用居中偏移
        painter.translate(input_rect.x() + x_offset - 10, input_rect.y() + y_offset)
        input_doc.drawContents(painter)
        painter.restore()

        # 绘制从输入到第一个块的箭头
        self.draw_arrow(painter,
                        QPoint(input_rect.x() + input_rect.width() // 2, input_rect.y() + input_rect.height()),
                        QPoint(input_rect.x() + input_rect.width() // 2, block_start_y))

        # 绘制输出文本框（在最后一个块下方）
        out_rect_width = 200
        output_rect = QRect(self.center_x - out_rect_width / 2, self.cur_ys[-1] + self.heights[-1] + self.y_spacing,
                            out_rect_width, 60)
        painter.setPen(QPen(Qt.black, 2))
        # painter.drawRect(output_rect)

        # 绘制输出文本
        output_doc = QTextDocument()
        output_doc.setPlainText("Classification\n      result")
        output_font = painter.font()
        output_font.setFamily("Arial")
        output_font.setPointSize(14)
        output_font.setBold(False)
        output_doc.setDefaultFont(output_font)
        output_doc.setTextWidth(output_rect.width())

        # 计算文本居中位置
        x_offset = input_rect.width() / 4  # 水平居中偏移
        y_offset = input_rect.height() / 4  # 垂直居中偏移

        painter.save()
        painter.translate(output_rect.x() + 30, output_rect.y() + y_offset)
        output_doc.drawContents(painter)
        painter.restore()

        # 绘制从最后一个块到输出的箭头
        self.draw_arrow(painter,
                        QPoint(output_rect.x() + output_rect.width() // 2, self.cur_ys[-1] + self.heights[-1]),
                        QPoint(output_rect.x() + output_rect.width() // 2, output_rect.y()))

    def __draw_brace(self, painter, right_x, top_y, height, width=20, line_width=2):
        """私有方法：绘制全曲线大括号（右侧对齐）"""
        painter.save()
        painter.setPen(QPen(Qt.black, line_width))

        # 计算控制点位置
        half_width = width / 2
        third_height = height / 3  # 将高度分为三等分

        # 创建大括号路径（全部使用贝塞尔曲线）
        path = QPainterPath()
        path.moveTo(right_x, top_y)

        # 第一段曲线：从上到第一个转折点
        path.cubicTo(
            right_x - 10, top_y,  # 控制点1
            right_x - 0, top_y + height / 4,  # 控制点2
            right_x - 15, top_y + height / 2  # 结束点
        )

        path.moveTo(right_x, top_y + height)
        path.cubicTo(
            right_x - 10, top_y + height,  # 控制点1
            right_x - 0, top_y + height * 0.75,  # 控制点2
            right_x - 15, top_y + height / 2,  # 结束点
        )

        painter.drawPath(path)
        painter.restore()

    def draw_neuron_block(self, painter, cur_x, cur_y, s_x, e_x=0., width=300., height=200., is_new=False,
                          layer_count=2, neuron_count=6, draw_black_line=True):
        """绘制单个神经元层块的辅助方法"""

        # 设置整体透明度
        # 计算进度百分比（0到1之间）
        progress = (s_x - cur_x) / (s_x - e_x)
        progress = max(0, min(1, progress))  # 限制在0-1范围内

        # 更新透明度（从1到0线性变化）
        if not is_new:
            opacity = 1.0 - progress
        else:
            opacity = progress

        painter.setOpacity(opacity)

        # 计算圆形的位置
        # circle_spacing = box_rect.width() / (neuron_count + 1)
        circle_spacing = 25
        # print(circle_spacing)

        # 计算半径
        # circle_radius = self.calculate_circle_radius(width, height, layer_count, neuron_count)
        # print(circle_radius)
        circle_radius = 8

        # 计算每个灰色矩形框的尺寸和位置
        box_height = height // layer_count
        # box_width = outer_rect.width() - 20
        spacing = circle_spacing - 2 * circle_radius
        box_width = circle_spacing * (neuron_count + 1)

        # 绘制黑色外框
        width = box_width + 20
        # print(600 - width / 2)
        outer_rect = QRect(cur_x, cur_y, width, height)

        if draw_black_line:
            painter.setPen(QPen(Qt.black, 2))
            painter.drawRect(outer_rect)

        # 绘制残差连接
        res_line_y_spacing = 20
        res_line_x_spacing = 20
        painter.drawLine(QPoint(self.center_x, cur_y - res_line_y_spacing),
                         QPoint(self.center_x + width / 2 + res_line_x_spacing, cur_y - res_line_y_spacing))

        painter.drawLine(QPoint(self.center_x + width / 2 + res_line_x_spacing, cur_y - res_line_y_spacing),
                         QPoint(self.center_x + width / 2 + res_line_x_spacing, cur_y + height + res_line_y_spacing / 2))

        painter.drawLine(QPoint(self.center_x + width / 2 + res_line_x_spacing, cur_y + height + res_line_y_spacing / 2),
                         QPoint(self.center_x, cur_y + height + res_line_y_spacing / 2))

        painter.drawLine(QPoint(self.center_x, cur_y + height + res_line_y_spacing / 2),
                         QPoint(self.center_x + 6, cur_y + height + res_line_y_spacing / 2 - 4))

        painter.drawLine(QPoint(self.center_x, cur_y + height + res_line_y_spacing / 2),
                         QPoint(self.center_x + 6, cur_y + height + res_line_y_spacing / 2 + 4))

        # 绘制灰色矩形框和圆形
        for i in range(layer_count):
            # 灰色矩形框
            box_rect = QRect(
                outer_rect.x() + 10,
                outer_rect.y() + 5 + i * box_height,
                box_width,
                box_height - 10
            )
            painter.setBrush(QBrush(QColor(200, 200, 200)))
            painter.setPen(QPen(Qt.gray, 1))
            painter.drawRect(box_rect)

            # 绘制圆形
            for j in range(neuron_count):
                center_x = box_rect.x() + (j + 1) * circle_spacing
                center_y = box_rect.y() + box_rect.height() // 2

                painter.setBrush(Qt.NoBrush)  # 空心圆
                painter.setPen(QPen(QColor(100, 100, 100), 2))
                painter.drawEllipse(
                    QPoint(center_x, center_y),
                    circle_radius,
                    circle_radius
                )

            # 在块左侧绘制大括号
            self.__draw_brace(painter, cur_x - 10, cur_y, height, width=20, line_width=2)

    def draw_arrow(self, painter, start_point, end_point, arrow_size=10):
        """绘制带箭头的直线"""
        painter.setPen(QPen(Qt.black, 2))  # 设置黑色笔刷
        painter.setOpacity(1.0)  # 确保箭头不透明
        # 绘制直线
        painter.drawLine(start_point, end_point)

        # 计算箭头角度和位置
        angle = math.atan2(end_point.y() - start_point.y(), end_point.x() - start_point.x())

        # 箭头点1
        p1 = QPoint(
            end_point.x() - arrow_size * math.cos(angle - math.pi / 6),
            end_point.y() - arrow_size * math.sin(angle - math.pi / 6)
        )
        painter.drawLine(p1, end_point)

        # 箭头点2
        p2 = QPoint(
            end_point.x() - arrow_size * math.cos(angle + math.pi / 6),
            end_point.y() - arrow_size * math.sin(angle + math.pi / 6)
        )
        painter.drawLine(p2, end_point)

    def draw_block_name(self, painter, cur_x, cur_y, s_x, e_x, width, height, idx_name, size_name, is_new=False,
                        replace=False):
        """绘制神经元层块名称"""

        # 设置整体透明度
        # 计算进度百分比（0到1之间）
        progress = (s_x - cur_x) / (s_x - e_x)
        progress = max(0, min(1, progress))  # 限制在0-1范围内

        # 更新透明度（从1到0线性变化）
        if not is_new:
            opacity = 1.0 - progress
        else:
            opacity = progress

        if replace:
            painter.setOpacity(opacity)
        else:
            painter.setOpacity(1.0)

        # 创建HTML文本
        html_text = idx_name.replace("b_{", "b<sub>").replace("}", "</sub>")

        # 创建QTextDocument来渲染HTML
        doc = QTextDocument()
        doc.setHtml(html_text)

        # 设置字体
        font = painter.font()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        doc.setDefaultFont(font)

        # 计算文本位置（居中）
        text_rect = QRect(cur_x, cur_y - 20, width, height)
        doc.setTextWidth(text_rect.width())

        # 保存painter状态
        painter.save()

        # 平移坐标系到绘制位置
        painter.translate(text_rect.x() + 20, text_rect.y() + 20)

        # 绘制idx_name文本
        doc.drawContents(painter)

        # 恢复painter状态
        painter.restore()

        # 绘制size_name（在idx_name下方）
        # 创建另一个QTextDocument来渲染size_name
        size_doc = QTextDocument()
        size_doc.setPlainText(size_name)  # 或者使用setHtml如果需要HTML格式

        # 设置size_name的字体（可以比idx_name小一些）
        size_font = painter.font()
        size_font.setFamily("Arial")
        size_font.setPointSize(12)  # 比idx_name小一些
        size_font.setBold(True)  # 可以不加粗
        size_doc.setDefaultFont(size_font)

        # 计算size_name的位置（在idx_name下方）
        # 获取idx_name的高度
        idx_name_height = doc.size().height()

        # 再次保存painter状态
        painter.save()

        # 平移坐标系到绘制位置（向下偏移idx_name的高度）
        painter.translate(text_rect.x() + 20, text_rect.y() + 20 + idx_name_height + 5)  # +5为间距

        # 绘制size_name文本
        size_doc.drawContents(painter)

        # 恢复painter状态
        painter.restore()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Neuron Layer with Opacity")
        self.resize(1400, 1800)

        # 主布局
        layout = QVBoxLayout(self)

        # 添加神经元层（现在可以自定义参数）
        self.neuron_layer_origin = Neuron_layer()
        layout.addWidget(self.neuron_layer_origin, stretch=1)

        # 添加控制按钮
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)

        # 开始按钮
        start_btn = QPushButton("Start")
        start_btn.setFixedSize(200, 50)
        start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #2E7D32;
            }
        """)
        start_btn.clicked.connect(self.neuron_layer_origin.start_movement)

        # 重置按钮
        reset_btn = QPushButton("Reset")
        reset_btn.setFixedSize(200, 50)
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """)
        reset_btn.clicked.connect(self.neuron_layer_origin.reset)

        # 按钮布局
        control_layout.addStretch()
        control_layout.addWidget(start_btn)
        control_layout.addWidget(reset_btn)
        control_layout.addStretch()

        layout.addWidget(control_panel)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
