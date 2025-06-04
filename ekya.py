import random
import sys
import time
from datetime import datetime
from idlelib.macosx import isXQuartz

from PyQt5.QtCore import Qt, QBasicTimer, QRect, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QBrush, QGuiApplication, QFont, QIcon, QPen
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QHBoxLayout, QLabel, QComboBox, \
    QVBoxLayout, QTextEdit

from model import BOARD_DATA, Shape

G = [
    [1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1],
    [1, 0, 1, 1, 1],
    [0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1],
    [0, 1, 1, 1, 1],
    [0, 1, 1, 1, 1],
    [0, 1, 1, 1, 1],
    [0, 1, 1, 1, 1],
    [0, 1, 1, 1, 1],
    [0, 1, 1, 1, 1],
    [0, 1, 0, 1, 1],
    [0, 1, 0, 1, 1],
    [0, 1, 0, 1, 1],
    [1, 1, 0 ,1, 1],
    [1, 1, 0 ,1, 1],
    [1, 1, 0 ,1, 1],
    [1, 1, 1 ,1, 1],
    [1, 1, 1 ,1, 1],
    [1, 1, 1 ,1, 1],
    [1, 1, 1 ,1, 1],
    [1, 1, 1, 0, 1],
    [1, 1, 1, 0, 1],
    [1, 1, 1, 0, 0],
    [1, 1, 1, 0, 0],
    [1, 1, 1, 0, 0],
    [1, 1, 1, 1, 0],
    [1, 1, 1, 1, 0],
    [1, 1, 1, 1, 0],
    [1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    []]

R = [
    [0.2, 0, 0.5, 0, 0.3],
    [0.3, 0, 0.2, 0, 0.5],
    [0.1, 0, 0.4, 0.2, 0.3],
    [0.1, 0, 0.4, 0.2, 0.3],
    [0, 0, 0.1, 0.6, 0.3],
    [0, 0, 0.2, 0.3, 0.5],
    [0, 0.1, 0.4, 0.3, 0.2],
    [0, 0.4, 0.1, 0.3, 0.2],
    [0, 0.2, 0.3, 0.4, 0.1],
    [0, 0.3, 0.2, 0.1, 0.4],
    [0, 0.2, 0.3, 0.4, 0.1],
    [0, 0.2, 0.4, 0.1, 0.3],
    [0, 0.2, 0, 0.4, 0.4],
    [0, 0.1, 0, 0.6, 0.3],
    [0, 0.6, 0, 0.1, 0.3],
    [0.1, 0.4, 0, 0.1, 0.4],
    [0.1, 0.1, 0, 0.4, 0.4],
    [0.1, 0.2, 0, 0.3, 0.4],
    [0.4, 0.3, 0.1, 0.1, 0.1],
    [0.1, 0.3, 0.2, 0.3, 0.1],
    [0.1, 0.2, 0.3, 0.1, 0.3],
    [0.2, 0.3, 0.2, 0.1, 0.2],
    [0.1, 0.4, 0.2, 0, 0.3],
    [0.2, 0.4, 0.1, 0, 0.3],
    [0.1, 0.4, 0.5, 0, 0],
    [0.3, 0.2, 0.5, 0, 0],
    [0.5, 0.1, 0.4, 0, 0],
    [0.1, 0.2, 0.3, 0.4, 0],
    [0.3, 0.4, 0.2, 0.1, 0],
    [0.3, 0.4, 0.2, 0.1, 0],
    [0.2, 0.4, 0.2, 0.2, 0],
    [0.1, 0.3, 0.2, 0.1, 0.3],
    [0.2, 0.2, 0.2, 0.2, 0.2],
    [0.2, 0.4, 0.1, 0.1, 0.2],
    [0.2, 0.2, 0.2, 0.2, 0.2],
    []]

print("len(G): ", len(G))

current_row = G[0]

schedule_idx = 0

neurons_per_app = \
    [[4, 6, 3, 4, 5],
        [6, 4, 5, 6, 3],
     [4, 6, 5, 4, 4],
     [4, 3, 4, 3, 2],
    [3, 4, 3, 4, 2],
                   ]

neurons_per_line = [[0] * len(n) for n in G]

SPACEs = [[0] * len(group) for group in G]

groups = G[0]
resource_weights = R[0]
spacings = SPACEs[0]

# 每组的层数和每层的圆形数量
Layers = [12, 12, 16, 8, 10]
Circles_per_layer = [8, 6, 8, 6, 4]

colorTable = [QColor(0x86e3ce), QColor(0xd0e6a5), QColor(0xffdd94), QColor(0xfa897b), QColor(0xccabd8)]


total = sum(groups)
radius = 10
spacing = 5

axis_start_x = 60
axis_start_y = 80

title_start_x = 40

board_width = 530
print("board_width: ", board_width)

app_names= ["图像分类", "目标检测", "文本生成", "文本分类", "机器翻译"]
model_names = ["ViT", "DETR", "GPT", "BERT", "T5"]

# 为每个组分配一个颜色
group_colors = [_ for _ in range(5)]
for idx in range(5):
    group_colors[idx] = colorTable[idx]

GPU_cores = 10

one_circle_equal_neuron = 64

end_y = 100 # 解释框的高度

s_y = [0 for _ in range(5)]

gpu_core_x = [0 for _ in range(GPU_cores)]

max_h = 0
for idx in range(len(app_names)):
    max_h = max(max_h, ((Layers[idx] + 3) * (36 - 4 // 2) + 70 + 50))
    print("max_h: ", max_h)

board_height = end_y
structure_height = [0 for _ in range(5)]

for i in range(len(app_names)):
    structure_height[i] = Circles_per_layer[i] * (2 * radius + spacing) - spacing + 4
    print("structure_height: ", structure_height[i])
    board_height += structure_height[i] * 1.05 + 10
    s_y[i] = board_height

if len(app_names) < 5:
    for i in range(len(app_names), 5):
        structure_height[i] = 120
        board_height += structure_height[i] * 1.05
        s_y[i] = board_height

board_height += 50

time_step = ["30s", "1min", "2min", "5min"]

time_step_now = time_step[1]

max_apps = len(app_names)

max_num_per_line = len(app_names)

vis_reTrain = current_row

speed = 10000
delay_time = 6000
qidong_time = 4000
jieshu_time = 11000

currentRow = 0

event_idx = 1
event_idx_2 = 1

start_time = datetime.now()

class Tetris(QMainWindow):
    def __init__(self):
        global currentRow
        super().__init__()
        self.controlBoard = None
        self.max_sidePanel_height = None
        self.max_sidePanel_width = None
        self.tboard = None
        self.sidePanel = None
        self.isStarted = False
        self.isPaused = False
        self.nextMove = None
        self.currentRow = currentRow  # 当前填充的行数
        screen = QGuiApplication.primaryScreen().geometry()
        self.window_width = screen.width()
        self.window_height = screen.height()


        self.initUI()

    def initUI(self):
        self.speed = speed # 行填充速度

        self.timer = QBasicTimer()
        self.setFocusPolicy(Qt.StrongFocus)

        hLayout = QHBoxLayout()

        self.controlBoard = ControlBoard(self)
        hLayout.addWidget(self.controlBoard)
        control_board_width = self.controlBoard.width()

        self.sidePanel = SidePanel(self, board_width + self.controlBoard.width())
        hLayout.addWidget(self.sidePanel)

        self.tboard = Board(self, control_board_width)
        hLayout.addWidget(self.tboard)


        self.start()

        self.center()
        self.setWindowTitle(' ')
        self.setWindowIcon(QIcon('pic.png'))


        # 标签和对应的下拉框数据
        label_texts = [QLabel("调度器"), QLabel("时间步长"), QLabel("应用数"), QLabel("最大并发重训应用数")]

        # 创建标签和下拉框
        for i in range(4):
            label_texts[i].setFixedSize(100, 30)
            label_texts[i].move(60, 20 + i * 50)


        self.show()
        print("tboard width: ", self.tboard.width())
        self.setFixedSize(self.sidePanel.width() + self.tboard.width() + self.controlBoard.width(), self.sidePanel.height())


    def getTitleBarHeight(self):
        # 计算标题栏的高度
        return (self.frameGeometry().height() - self.geometry().height()) * 3

    def center(self):
        self.move(0, 0)

    def start(self):
        if self.isPaused:
            return

        self.isStarted = True

        self.timer.start(self.speed, self)

    def updateTimerInterval(self, new_interval):
        self.speed = new_interval
        self.timer.stop()
        self.timer.start(self.speed, self)

    def timerEvent(self, event):
        global groups, resource_weights, spacings, current_row, max_num_per_line, schedule_idx, currentRow
        if event.timerId() == self.timer.timerId():
            if currentRow < len(G):
                groups = G[currentRow]
                if len(groups) == 0:
                    return
                resource_weights = R[currentRow]
                spacings = SPACEs[currentRow]
                # 统计groups中非0的个数
                num = 0
                last_idx = num
                drop_weight = 0
                for i in range(len(groups)):
                    if i + 1 > max_apps or num > max_num_per_line:
                        groups[i] = 0
                        drop_weight += resource_weights[i]
                    if groups[i] != 0:
                        num += 1
                        if num > max_num_per_line:
                            groups[i] = 0
                            drop_weight += resource_weights[i]
                        else:
                            last_idx = i

                resource_weights[last_idx] += drop_weight

                current_row = groups
                groups = [a * b for a, b in zip(groups, neurons_per_app[schedule_idx])]


                # for idx, group in enumerate(groups):
                #     if self.currentRow == 0:
                #         if group != 0:
                #             self.controlBoard.text_area.append(f"第{self.currentRow + 1}分，应用{idx + 1}启动重训练")
                #         continue
                #     elif G[self.currentRow - 1][idx] == 0 and group != 0:
                #         self.controlBoard.text_area.append(f"第{self.currentRow + 1}分，应用{idx + 1}启动重训练")
                #     elif G[self.currentRow - 1][idx] != 0 and group == 0:
                #         self.controlBoard.text_area.append(f"第{self.currentRow + 1}分，应用{idx + 1}结束重训练")

                self.tboard.fillRow(currentRow)  # 填充当前行
                currentRow += 1  # 更新当前行数

            # self.update()

        else:
            super(Tetris, self).timerEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.black)
        end_x = self.width() - 40
        painter.drawLine(title_start_x, 0, title_start_x, end_y - 10)
        painter.drawLine(end_x, 0, end_x, end_y - 10)
        painter.drawLine(title_start_x, end_y - 10, end_x, end_y - 10)

        y_axis_y = (end_y - 10) / 2 - 10
        x_end = title_start_x + 120

        painter.drawLine(title_start_x + 30, y_axis_y, x_end, y_axis_y)

        # 画 X 轴箭头
        arrow_size = 10

        # x 轴右端箭头
        painter.drawLine(x_end - arrow_size, y_axis_y - arrow_size / 2, x_end, y_axis_y)  # 左箭头线
        painter.drawLine(x_end - arrow_size, y_axis_y + arrow_size / 2, x_end, y_axis_y)  # 右箭头线

        y_x_start = title_start_x + 250
        painter.drawLine(y_x_start, 10, y_x_start, end_y - 20)

        # 画 Y 轴箭头
        y_start = 10

        # y 轴上端箭头
        painter.drawLine(y_x_start - arrow_size / 2, y_start + arrow_size, y_x_start, y_start)  # 左箭头线
        painter.drawLine(y_x_start + arrow_size / 2, y_start + arrow_size, y_x_start, y_start)  # 右箭头线

        # 画模型的圆形
        for idx, color in enumerate(group_colors):
            if idx >= len(app_names):
                break
            painter.setBrush(QBrush(color))
            painter.setPen(color.darker(125))
            painter.drawEllipse(y_x_start + 200 + 200 * idx, (end_y - 10) / 2, radius * 2, radius * 2)

        painter.setFont(QFont("Arial", 12))
        painter.setPen(Qt.black)
        painter.drawText(x_end - 10, y_axis_y - 10, "x")
        painter.drawText(title_start_x + 30, y_axis_y + 40, "GPU计算资源(%)")

        painter.drawText(y_x_start - 20, y_start + 10, "y")
        painter.drawText(y_x_start + 20, (end_y - 10) / 2 + 10, f"时间片：{time_step_now}")

        for i in range(1, len(app_names) + 1):
            w = 125
            painter.setPen(QColor(w, w, w))
            painter.drawText(y_x_start + 200 + 200 * (i - 1) + radius / 2, (end_y - 10) / 2 + radius * 1.5, f"{i}")
            painter.setPen(Qt.black)
            painter.drawText(y_x_start + 200 + 200 * (i - 1) + radius * 3, (end_y - 10) / 2 + radius * 1.5, f"应用{i}的256个神经元")


class SidePanel(QFrame):
    def __init__(self, parent, start):
        super().__init__(parent)
        global delay_time, qidong_time, jieshu_time

        self.radius = radius  # 圆的半径
        self.spacing = spacing  # 圆与圆之间的间距
        self.layer_spacing = 40  # 层与层之间的间距
        self.space = 4

        self.max_rect_width = 0
        for i in range(len(app_names)):
            self.max_rect_width = max(self.max_rect_width, structure_height[i])

        self.rect_height = 2 * self.radius + self.space  # 矩形高度
        self.move(start, 0)
        self.start_x = 200  # 矩形的起始 x 坐标
        self.start_y = 10 + end_y
        print("start_x: ", self.start_x)
        print("rect_height: ", self.rect_height)
        self.setFixedSize(int(max_h + self.start_x), int(board_height))
        print("sidePanel width: ", self.width())
        print("sidePanel height: ", self.height())

        self.end_x = self.width() - 40

        # 判断所处阶段标志
        self.in_start = False
        self.in_retrain = False
        self.in_end = False


        self.weight_matrix = [[0] * Circles_per_layer[i] for i in range(len(app_names))]
        for i in range(len(app_names)):
            self.weight_matrix[i] = [[random.randint(50, 255) for _ in range(Circles_per_layer[i])] for _ in range(Layers[i])]

        # 初始化定时器
        self.start_timer = QTimer(self)  # 用于延迟启动
        self.start_qidong_timer = QTimer(self)  # 用于延迟启动
        self.start_jieshu_timer = QTimer(self)  # 用于延迟启动
        self.periodic_timer = QTimer(self)  # 用于周期性任务
        self.qidong_timer = QTimer(self)  # 用于启动重训练
        self.jieshu_timer = QTimer(self)  # 用于结束重训练

        # 配置延迟启动定时器
        self.start_timer.setSingleShot(True)  # 只触发一次
        self.start_qidong_timer.setSingleShot(True)  # 只触发一次
        self.start_jieshu_timer.setSingleShot(True)  # 只触发一次
        self.start_timer.timeout.connect(self.startPeriodicTimer)
        self.start_qidong_timer.timeout.connect(self.startQidongTimer)
        self.start_jieshu_timer.timeout.connect(self.startJieshuTimer)
        self.hasStarted = False

        # 配置周期性定时器
        self.periodic_timer.setInterval(speed)
        self.periodic_timer.timeout.connect(self.onPeriodicTimer)

        self.qidong_timer.setInterval(speed)
        self.qidong_timer.timeout.connect(self.onQidongTimer)

        self.jieshu_timer.setInterval(speed)
        self.jieshu_timer.timeout.connect(self.onJieshuTimer)

        # 启动延迟定时器
        self.start_timer.start(delay_time)
        self.start_qidong_timer.start(qidong_time)
        self.start_jieshu_timer.start(jieshu_time)

    def startPeriodicTimer(self):
        self.periodic_timer.start()  # 启动周期性定时器
        self.hasStarted = True

    def startQidongTimer(self):
        self.qidong_timer.start()

    def startJieshuTimer(self):
        self.jieshu_timer.start()

    def onQidongTimer(self):
        print("Qidong timer triggered!")
        self.in_start = True
        global vis_reTrain, current_row, currentRow, event_idx, start_time
        vis_reTrain = current_row
        if currentRow > len(G) - 2:
            return
        # print("groups: ", vis_reTrain)
        # print("currentRow: ", currentRow)
        # print("G[currentRow]: ", G[currentRow])
        current_time = datetime.now() - start_time  # 获取当前时间并格式化
        # self.parent().controlBoard.text_area.append(f"[{int(current_time.total_seconds())}]")
        # self.parent().controlBoard.text_area.append(f"启动重训练")

        for idx, group in enumerate(vis_reTrain):
            if currentRow == 1:
                if group != 0:
                    current_time = datetime.now() - start_time  # 获取当前时间并格式化
                    # self.parent().controlBoard.text_area.append(f"[{int(current_time.total_seconds())}]")
                    self.parent().controlBoard.text_area.append(
                        f"事件{event_idx}：第{currentRow - 1}分钟，应用{idx + 1}启动重训练")
                    event_idx += 1
                continue
            elif G[currentRow - 2][idx] == 0 and group != 0:
                current_time = datetime.now() - start_time  # 获取当前时间并格式化
                # self.parent().controlBoard.text_area.append(f"[{int(current_time.total_seconds())}]")
                self.parent().controlBoard.text_area.append(f"事件{event_idx}：第{currentRow - 1}分钟，应用{idx + 1}启动重训练")
                event_idx += 1

        self.update()


    def onJieshuTimer(self):
        print("jieshu timer triggered!")
        global event_idx, start_time
        self.in_end = True
        current_time = datetime.now() - start_time  # 获取当前时间并格式化
        # self.parent().controlBoard.text_area.append(f"[{int(current_time.total_seconds())}]")
        # self.parent().controlBoard.text_area.append(f"结束重训练")

        for idx, group in enumerate(vis_reTrain):
            if G[currentRow - 1][idx] == 0 and group != 0:
                current_time = datetime.now() - start_time  # 获取当前时间并格式化
                # self.parent().controlBoard.text_area.append(f"[{int(current_time.total_seconds())}]")
                self.parent().controlBoard.text_area.append(f"事件{event_idx}：第{currentRow - 1}分钟，应用{idx + 1}结束重训练")
                event_idx += 1

        self.update()


    def onPeriodicTimer(self):
        print("Periodic timer triggered!")
        self.in_retrain = True
        global vis_reTrain, current_row, currentRow, event_idx, start_time
        current_time = datetime.now() - start_time  # 获取当前时间并格式化
        # self.parent().controlBoard.text_area.append(f"[{int(current_time.total_seconds())}]")
        # self.parent().controlBoard.text_area.append(f"正在重训练")

        self.update()


    def paintEvent(self, event):
        painter = QPainter(self)
        start_y = self.start_y
        global max_apps, vis_reTrain
        for idx in range(min(max_apps, len(app_names))):
            if idx > 0:
                start_y += structure_height[idx - 1] * 1.05 + 10
            self.drawTransformerStructure(painter, Layers[idx], Circles_per_layer[idx], colorTable[idx], self.radius,
                                      self.spacing, self.layer_spacing, start_y, idx)

        if self.in_start:
            self.in_start = False
        elif self.in_retrain:
            self.in_retrain = False
        elif self.in_end:
            self.in_end = False

        if min(max_apps, len(app_names)) < 5:
            for i in range(min(max_apps, len(app_names)), 5):
                painter.drawLine(30, s_y[i - 1], self.end_x, s_y[i - 1])

        painter.setPen(Qt.black)
        painter.drawLine(30, board_height - 50, self.end_x, board_height - 50)
        painter.drawLine(30, end_y, 30, board_height - 50)
        painter.drawLine(self.end_x, end_y, self.end_x, board_height - 50)

        painter.setFont(QFont("Arial", 18))
        x_offset = 50
        painter.drawText(self.width() / 2 - x_offset, board_height - 10, "并发AI应用")


    def draw_model_name(self, painter, idx):
        painter.setPen(Qt.black)
        painter.setFont(QFont("Arial", 12))
        x_offset = 50
        global s_y, current_row, vis_reTrain, event_idx_2
        painter.drawText(x_offset, s_y[idx] - structure_height[idx] / 2 - 10, f"应用{idx + 1}: " + app_names[idx])
        painter.drawText(x_offset, s_y[idx] - structure_height[idx] / 2 + 10, "模型: " + model_names[idx])
        if len(current_row) == 0:
            return
        painter.setPen(QColor(0xFF0033))
        if currentRow < len(G) - 1 and self.hasStarted:
            if currentRow > 1:
                print("currentRow: ", currentRow, "idx:", idx , "group:", vis_reTrain[idx], "last:", G[currentRow - 2][idx])
            if self.in_start and vis_reTrain[idx]:
                if currentRow == 1 or G[currentRow - 2][idx] == 0:
                    painter.drawText(x_offset, s_y[idx] - structure_height[idx] / 2 + 30, f"事件{event_idx_2}：重训练启动")
                    event_idx_2 += 1
                elif G[currentRow - 2][idx] != 0:
                    painter.drawText(x_offset, s_y[idx] - structure_height[idx] / 2 + 30, f"正在重训练")
            elif self.in_retrain and vis_reTrain[idx]:
                painter.drawText(x_offset, s_y[idx] - structure_height[idx] / 2 + 30, f"正在重训练")
            elif self.in_end:
                if G[currentRow - 1][idx] == 0 and vis_reTrain[idx] != 0:
                    painter.drawText(x_offset, s_y[idx] - structure_height[idx] / 2 + 30, f"事件{event_idx_2}：重训练结束")
                    event_idx_2 += 1
                elif G[currentRow - 1][idx] != 0 and vis_reTrain[idx] != 0:
                    painter.drawText(x_offset, s_y[idx] - structure_height[idx] / 2 + 30, f"正在重训练")


    def drawArrow(self, painter, x, y, spacing):
        arrow_size = 4  # 箭头的大小

        # 绘制箭头的主干
        painter.setPen(Qt.black)
        painter.drawLine(int(x + self.rect_height), int(y), int(x + spacing), int(y))

        # 绘制箭头的尖端
        painter.drawLine(int(x + spacing), int(y), int(x + spacing - arrow_size), int(y - arrow_size))
        painter.drawLine(int(x + spacing), int(y), int(x + spacing - arrow_size), int(y + arrow_size))

    def drawTransformerStructure(self, painter, layers, circles_per_layer, color, radius, spacing, layer_spacing, start_y, idx):
        self.draw_model_name(painter, idx)
        rect_width = circles_per_layer * (2 * radius + spacing) - spacing + self.space  # 矩形宽度
        # 绘制每层
        for layer in range(layers):
            # 矩形的起始位置
            rect_x = self.start_x + layer * layer_spacing - spacing // 2  # 矩形边距
            rect_y = start_y - spacing // 2  # 矩形边距

            # 绘制矩形
            painter.setPen(Qt.black)
            painter.setBrush(Qt.NoBrush)  # 矩形颜色
            # painter.setBrush(base_color.lighter(125))
            painter.drawRect(int(rect_x), int(rect_y), int(self.rect_height), int(rect_width))

            # 绘制圆
            for circle in range(circles_per_layer):
                # 计算圆心位置
                x = self.start_x + layer * layer_spacing
                y = start_y + circle * (2 * radius + spacing)

                # 设置颜色和透明度
                opacity = self.weight_matrix[idx][layer][circle]  # 获取每个圆对应的透明度值
                color_with_opacity = QColor(color)
                color_with_opacity.setAlpha(opacity)  # 设置透明度

                # 绘制带透明度的圆
                painter.setBrush(QBrush(color_with_opacity))
                painter.setPen(color_with_opacity.darker(125))
                painter.drawEllipse(int(x), int(y), int(radius * 2), int(radius * 2))

                painter.setFont(QFont("Arial", 12))
                w = 125
                color_temp = QColor(w, w, w)
                painter.setPen(color_temp)
                painter.drawText(x + radius / 2, y + radius * 1.5, f"{idx + 1}")

            # 绘制箭头（如果不是最后一层）
            if layer < layers - 1:
                self.drawArrow(painter, rect_x, rect_y + rect_width / 2, layer_spacing)

            # 绘制分割线
            painter.setPen(Qt.black)
            painter.drawLine(30, start_y - 10, self.end_x, start_y - 10)


class Board(QFrame):
    speed = 10

    def __init__(self, parent, start):
        super().__init__(parent)
        self.move(start, 0)
        self.setFixedSize(board_width, board_height)
        self.filledRows = 0  # 已填充的行数
        self.rowColors = []  # 用于存储每一行的圆形颜色
        self.radius = radius  # 圆形的半径
        self.axis_start_x = axis_start_x # X轴的起始 x 坐标
        self.circles_per_row = (self.width() + spacing) // (2 * radius + spacing)
        self.initBoard()
        print("width: ", self.width())

    def initBoard(self):
        self.score = 0
        BOARD_DATA.clear()
        self.rowColors = [[] for _ in range(len(G))]  # 初始化存储颜色的数组

    def fillRow(self, row):
        if row < len(G):
            # 如果该行还没有颜色信息，随机生成并保存
            if not self.rowColors[row]:
                # 随机选择该行每个圆形的颜色，并根据 groups 分段
                self.rowColors[row] = []
                circle_now = 0
                # print(f"group: {groups}")
                for group_index, group_size in enumerate(groups):
                    # 为每个组生成对应数量的圆形颜色
                    self.rowColors[row] += [group_colors[group_index]] * group_size
                    width_now = (board_width - axis_start_x) * resource_weights[group_index]
                    if (width_now - 2 * spacing) > 2 * radius * groups[group_index]:
                        SPACEs[row][group_index] = 2 * radius + (width_now - 2 * spacing - 2 * radius * groups[group_index]) / (groups[group_index] - 1)
                    elif (width_now - 2 * spacing) == 2 * radius * groups[group_index]:
                        SPACEs[row][group_index] = 2 * radius
                    else:
                        SPACEs[row][group_index] = (width_now - 2 * spacing - 2 * radius) / (groups[group_index] - 1)
                    SPACEs[row][group_index] = max(5, SPACEs[row][group_index])
                    for circle in range(group_size):
                        color = QColor(self.rowColors[row][circle_now])
                        weight = random.randint(120, 255)
                        color.setAlpha(weight)
                        self.rowColors[row][circle_now] = color
                        circle_now += 1
            self.filledRows = row  # 更新已填充的行数
            neurons_per_line[row] = neurons_per_app[schedule_idx]

            global start_time
            current_time = datetime.now() - start_time  # 获取当前时间并格式化
            # self.parent().controlBoard.text_area.append(f"[{int(current_time.total_seconds())}]")
            # self.parent().controlBoard.text_area.append(f"fillRow: {row}")

            self.update()  # 触发重绘

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_gpu_lines(painter)

        # 绘制刻度轴
        self.drawAxes(painter)

        start_y = self.height() - axis_start_y  # 起始 y 坐标
        # 绘制已填充的行的圆形
        for y in range(self.filledRows):
            x_offset = spacing + self.axis_start_x  # 重置 x 坐标的偏移量
            circle_now = 0  # 当前圆形的索引
            max_y = self.height()
            line_now = [a * b for a, b in zip(G[y], neurons_per_line[y])]
            for group_index, group_size in enumerate(line_now):
                y_draw = start_y - (y + 1) * (self.radius * 2 + 5)
                max_y = min(max_y, y_draw)
                # 绘制每个组中的圆形
                for circle in range(group_size):
                    if circle < len(self.rowColors[y]):
                        color = QColor(self.rowColors[y][circle_now])  # 根据填充的颜色绘制
                        painter.setBrush(color)
                        painter.setPen(color.darker(150))
                        # 计算圆形的 x 坐标
                        x_offset_temp = x_offset
                        for x in gpu_core_x:
                            if x_offset <= x <= x_offset + radius * 2:
                                # print(f"row: {y}, group:{group_index}, circle: {circle}, x: {x}, x_offset: {x_offset + radius}")
                                if x_offset + radius <= x:
                                    x_offset_temp = x - radius * 2 - spacing / 2
                                elif x_offset + radius >= x:
                                    x_offset_temp = x + spacing / 2
                                else:
                                    x_offset_temp = x - radius * 2 - spacing / 2
                                break
                        w = 125
                        color_temp = QColor(w, w, w)
                        if x_offset_temp != x_offset:
                            painter.drawEllipse(int(x_offset_temp), int(y_draw),
                                                int(self.radius * 2),
                                                int(self.radius * 2))  # 绘制圆形
                            painter.setFont(QFont("Arial", 12))
                            painter.setPen(color_temp)
                            painter.drawText(x_offset_temp + radius / 2, y_draw + radius * 1.5, f"{group_index + 1}")
                        else:
                            painter.drawEllipse(int(x_offset), int(y_draw),
                                                int(self.radius * 2),
                                                int(self.radius * 2))
                            painter.setFont(QFont("Arial", 12))
                            painter.setPen(color_temp)
                            painter.drawText(x_offset + radius / 2, y_draw + radius * 1.5, f"{group_index + 1}")
                        if circle < group_size - 1:
                            x_offset += SPACEs[y][group_index]
                        circle_now += 1
                if group_size > 1:
                    x_offset += spacing * 2 + self.radius * 2  # 更新 x 坐标的偏移量

        # 绘制边框
        painter.setPen(Qt.black)
        painter.drawLine(board_width - 1, end_y, board_width - 1, board_height - axis_start_y + 10)
        painter.drawLine(board_width, end_y, board_width, board_height - axis_start_y + 10)

        self.draw_name(painter)


    def draw_gpu_lines(self, painter):
        dashline_color = QColor(0x777777)
        pen = QPen(dashline_color.lighter(160), 1, Qt.DashLine)
        painter.setPen(pen)
        x_offset = (board_width - axis_start_x) // GPU_cores
        global gpu_core_x
        for i in range(GPU_cores):
            gpu_core_x[i] = axis_start_x +(i + 1) * x_offset
            painter.drawLine(axis_start_x + (i + 1) * x_offset, end_y, axis_start_x + (i + 1) * x_offset, board_height - axis_start_y)


    def draw_name(self, painter):
        painter.setPen(Qt.black)
        painter.setFont(QFont("Arial", 18))
        x_offset = 40
        painter.drawText(self.width() / 2 - x_offset, self.height() - 10, "资源分配情况")

    def drawAxes(self, painter):
        # 刻度轴颜色
        axis_color = QColor(0x000000)
        painter.setPen(axis_color)
        font = QFont("Arial", 12)
        painter.setFont(font)
        # 画横轴（X轴） - 内存大小
        painter.drawLine(axis_start_x, self.height() - axis_start_y, self.width(), self.height() - axis_start_y)  # X轴
        # 刻度
        num_ticks_x = 5  # X轴刻度数量
        tick_interval_x = (self.width() - axis_start_x) // num_ticks_x
        for i in range(num_ticks_x + 1):
            x_pos = i * tick_interval_x + axis_start_x
            painter.drawLine(x_pos, board_height - axis_start_y, x_pos, board_height - axis_start_y + 10)  # X轴刻度线
            # 标注内存大小 (这里假设从 0 到 1000 逐步增加)
            if i == num_ticks_x:
                painter.drawText(x_pos - 27, board_height - axis_start_y + 30, f"{i * 20}")
            else:
                painter.drawText(x_pos - 10, board_height - axis_start_y + 30, f"{i * 20}")

        # 画纵轴（Y轴） - 时间
        painter.drawLine(self.axis_start_x, end_y, self.axis_start_x, board_height - axis_start_y)  # Y轴
        # 刻度
        num_ticks_y = len(G) - 2  # Y轴刻度数量
        tick_interval_y = (self.radius * 2 + 5) * 1  # Y轴刻度间隔
        for i in range(num_ticks_y + 1):
            y_pos = board_height - axis_start_y - i * tick_interval_y
            painter.drawLine(axis_start_x - 10, y_pos, axis_start_x, y_pos)  # Y轴刻度线
            # 标注时间 (假设每刻度是 1 秒)
            painter.drawText(axis_start_x - 30, y_pos + 5, f"{i}")

        # 绘制 Y 轴名称“时间”
        # 保存当前坐标系
        painter.save()

        # 移动到合适的位置并旋转 -90 度
        painter.translate(axis_start_x - 40, self.height() // 2)  # 平移到 Y 轴中间
        painter.rotate(-90)  # 旋转 -90 度，竖着绘制文本

        # 绘制竖着的文本“时间”
        painter.drawText(0, 0, "时间")

        # 恢复坐标系
        painter.restore()

        # painter.drawText(self.width() // 2 - 10, self.height() - 10 - axis_start_y + 60, "GPU计算资源（%）")


class ControlBoard(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        global start_time
        self.setFixedSize(420, board_height)

        # 创建垂直布局
        layout = QVBoxLayout(self)

        # 标签和对应的下拉框数据
        self.labels = [QLabel("调度器"), QLabel("时间步长"), QLabel("应用数"), QLabel("最大并发重训应用数")]
        self.combo_boxes = []
        self.combo_options = [
            ["Tetris", "EOMU", "ekya"],
            ["30s", "1min", "2min", "5min"],
            [str(i) for i in range(1, 6)],
            [str(i) for i in range(1, 6)]
        ]

        # 创建标签和下拉框，并添加到布局中
        for i, label in enumerate(self.labels):
            # 创建标签
            label.setFont(QFont("Arial", 14))
            layout.addWidget(label)

            # 创建下拉框
            comboBox = QComboBox()
            comboBox.setFixedSize(280, 30)
            comboBox.setFont(QFont("Arial", 12))
            comboBox.addItems(self.combo_options[i])
            self.combo_boxes.append(comboBox)
            layout.addWidget(comboBox)

            layout.addSpacing(30)

        self.combo_boxes[0].setCurrentIndex(2)
        self.combo_boxes[1].setCurrentIndex(1)
        self.combo_boxes[2].setCurrentIndex(4)
        self.combo_boxes[3].setCurrentIndex(4)

        self.combo_boxes[0].currentIndexChanged.connect(self.onSchedulerChanged)
        self.combo_boxes[1].currentIndexChanged.connect(self.onTimeStepChanged)
        self.combo_boxes[2].currentIndexChanged.connect(self.onAppNumChanged)
        self.combo_boxes[3].currentIndexChanged.connect(self.onMaxConcurrentAppChanged)

        # 添加多行文本区域
        self.text_area_label = QLabel("训练事件:")
        self.text_area_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.text_area_label)

        self.text_area = QTextEdit()
        self.text_area.setFixedSize(280, 400)
        self.text_area.setFont(QFont("Arial", 12))
        self.text_area.setReadOnly(True)  # 设置为只读
        start_time = datetime.now()  # 获取当前时间并格式化
        # format_t = start_time.strftime("%Y-%m-%d %H:%M:%S")
        # self.text_area.append(f"[{format_t}]\nStart")
        layout.addWidget(self.text_area)

        # 设置布局的边距
        layout.setContentsMargins(axis_start_x + 5, end_y + 50, 5, 10)  # 左上右下的边距

        layout.addStretch()  # 将控件置顶，底部留出空白

    def onSchedulerChanged(self, index):
        global schedule_idx, groups
        schedule_idx = index
        print(f"schedule_idx: {schedule_idx}")
        groups = [a * b for a, b in zip(groups, neurons_per_app[schedule_idx])]

    def onTimeStepChanged(self, index):
        global time_step_now
        time_step_now = time_step[index]
        # if index == 0:
        #     self.parent().updateTimerInterval(10000)
        # elif index == 1:
        #     self.parent().updateTimerInterval(5000)
        # elif index == 2:
        #     self.parent().updateTimerInterval(2500)
        # elif index == 3:
        #     self.parent().updateTimerInterval(1000)
        self.parent().update()

    def onAppNumChanged(self, index):
        global max_apps
        max_apps = index + 1
        self.parent().sidePanel.update()
        if self.combo_boxes[3].currentIndex() > index:
            self.combo_boxes[3].setCurrentIndex(index)

    def onMaxConcurrentAppChanged(self, index):
        app_num = self.combo_boxes[2].currentIndex()
        if index > app_num:
            self.combo_boxes[3].setCurrentIndex(app_num)
        global max_num_per_line
        max_num_per_line = index + 1

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.black)

        # 控制面板标题
        painter.setFont(QFont("Arial", 18))
        x_offset = 50
        painter.drawText(self.width() / 2 - x_offset, board_height - 10, "控制面板")

        # 绘制边框
        s_x = title_start_x
        e_x = self.width() - 50
        s_y = end_y
        e_y = self.height() - 50

        painter.drawLine(s_x, s_y, e_x, s_y)
        painter.drawLine(s_x, e_y, e_x, e_y)
        painter.drawLine(s_x, s_y, s_x, e_y)
        painter.drawLine(e_x, s_y, e_x, e_y)


if __name__ == '__main__':
    app = QApplication([])
    tetris = Tetris()
    sys.exit(app.exec_())
