import time
from threading import Thread

from PySide6.QtWidgets import QApplication, QMainWindow
# PySide6-uic demo.ui -o ui_demo.py
# from ui_demo import Ui_Demo
from task import add
from ui_demo import Ui_MainWindow

from Signal import my_signal


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()  # UI类的实例化()
        self.ui.setupUi(self)
        self.band()

    def band(self):
        # self.ui.___ACTION___.triggered.connect(___FUNCTION___)
        # self.ui.___BUTTON___.clicked.connect(___FUNCTION___)
        # self.ui.___COMBO_BOX___.currentIndexChanged.connect(___FUNCTION___)
        # self.ui.___SPIN_BOX___.valueChanged.connect(___FUNCTION___)
        # 自定义信号.属性名.connect(___FUNCTION___)

        self.ui.pushButton.clicked.connect(self.handle_click)

        my_signal.setProgressBar.connect(self.set_progress_bar)

        my_signal.setResult.connect(self.set_result)

    def set_result(self, result: str):
        self.ui.result.setText(result)

    def set_progress_bar(self, progress: int):
        self.ui.progressBar.setValue(progress)

    def handle_click(self):
        def innerFunc():
            a = self.ui.inputA.value()
            b = self.ui.inputB.value()

            time_cost = self.ui.timeCost.value()

            for index, _ in enumerate(range(time_cost)):
                progress = index * 100 // time_cost
                my_signal.setProgressBar.emit(progress)
                time.sleep(1)
            my_signal.setProgressBar.emit(100)

            result = str(add(a, b))
            my_signal.setResult.emit(result)

        task = Thread(target=innerFunc)
        task.start()


if __name__ == '__main__':
    app = QApplication([])  # 启动一个应用
    window = MainWindow()  # 实例化主窗口
    window.show()  # 展示主窗口
    app.exec()  # 避免程序执行到这一行后直接退出
