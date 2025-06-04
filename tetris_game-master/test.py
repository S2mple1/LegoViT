from PyQt5.QtWidgets import QApplication, QFrame, QGridLayout
import pyqtgraph as pg

class CustomPlotBoard(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(400, 600)

        # 使用 QGridLayout 来布局
        self.layout = QGridLayout(self)

        # 添加第一个 PlotWidget，并设置位置
        self.plot1 = pg.PlotWidget(self)
        self.plot1.setFixedSize(300, 150)
        self.plot1.setBackground("w")
        self.layout.addWidget(self.plot1, 0, 0)  # 第1行第1列

        # 添加第二个 PlotWidget，并设置位置
        self.plot2 = pg.PlotWidget(self)
        self.plot2.setFixedSize(300, 150)
        self.plot2.setBackground("w")
        self.layout.addWidget(self.plot2, 1, 0)  # 第2行第1列

        # 添加第三个 PlotWidget，并设置位置
        self.plot3 = pg.PlotWidget(self)
        self.plot3.setFixedSize(300, 150)
        self.plot3.setBackground("w")
        self.layout.addWidget(self.plot3, 2, 0)  # 第3行第1列

# 测试代码
if __name__ == "__main__":
    app = QApplication([])
    window = QFrame()
    window.setFixedSize(500, 700)
    plot_board = CustomPlotBoard(window)
    window.show()
    app.exec_()
