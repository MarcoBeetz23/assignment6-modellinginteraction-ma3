import sys
from PyQt5 import uic, Qt
from PyQt5.QtWidgets import QDialog


class Calculator(QDialog):
    """
        Initiating all varbiables & UI...
    """
    MAX_ITEMS_IN_LIST = 12

    def __init__(self):
        super().__init__()
        self.calc_string = ""
        self.result = 0
        self.calc_list = [""]
        uic.loadUi("calculator.ui", self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Calculator')
        self.resize(500, 450)

        """
            Declaring & connecting all buttons...
        """

        self.dial_res.clicked.connect(self.res_clicked)
        self.dial_dif.clicked.connect(self.dif_clicked)
        self.dial_mul.clicked.connect(self.mul_clicked)
        self.dial_min.clicked.connect(self.min_clicked)
        self.dial_plu.clicked.connect(self.plu_clicked)

        self.dial_dot.clicked.connect(self.dot_clicked)
        self.dial_bs.clicked.connect(self.bs_clicked)
        self.clear_all.clicked.connect(self.clear_all_clicked)

        self.dial_0.clicked.connect(self.d0_clicked)
        self.dial_1.clicked.connect(self.d1_clicked)
        self.dial_2.clicked.connect(self.d2_clicked)
        self.dial_3.clicked.connect(self.d3_clicked)
        self.dial_4.clicked.connect(self.d4_clicked)
        self.dial_5.clicked.connect(self.d5_clicked)
        self.dial_6.clicked.connect(self.d6_clicked)
        self.dial_7.clicked.connect(self.d7_clicked)
        self.dial_8.clicked.connect(self.d8_clicked)
        self.dial_9.clicked.connect(self.d9_clicked)

    """
        Declaring button methods -.- ...
    """

    def res_clicked(self):
        self.calc_result()
        self.update()

    def dif_clicked(self):
        self.calc_string += "/"
        self.update()

    def mul_clicked(self):
        self.calc_string += "*"
        self.update()

    def min_clicked(self):
        self.calc_string += "-"
        self.update()

    def plu_clicked(self):
        self.calc_string += "+"
        self.update()

    def dot_clicked(self):
        self.calc_string += ","
        self.update()

    def bs_clicked(self):
        self.calc_string = self.calc_string[: -1]
        self.update()

    def clear_all_clicked(self):
        self.calc_string = ""
        self.update()

    def d0_clicked(self):
        self.calc_string += "0"
        self.update()

    def d1_clicked(self):
        self.calc_string += "1"
        self.update()

    def d2_clicked(self):
        self.calc_string += "2"
        self.update()

    def d3_clicked(self):
        self.calc_string += "3"
        self.update()

    def d4_clicked(self):
        self.calc_string += "4"
        self.update()

    def d5_clicked(self):
        self.calc_string += "5"
        self.update()

    def d6_clicked(self):
        self.calc_string += "6"
        self.update()

    def d7_clicked(self):
        self.calc_string += "7"
        self.update()

    def d8_clicked(self):
        self.calc_string += "8"
        self.update()

    def d9_clicked(self):
        self.calc_string += "9"
        self.update()

    """
        Update method:
    """

    def update(self):
        try:
            eval(self.calc_string.replace(",", "."))
            self.dial_res.setEnabled(True)
        except SyntaxError:
            self.dial_res.setEnabled(False)
            pass
        self.lineEdit.setText(self.calc_string)
        print(end="\r")
        print(self.calc_string, end='')
        self.result_label.setText(str(self.result))
        return

    """
        Handle keystroke:
    """

    def keyPressEvent(self, event):
        k = event.key()
        if k == 16777219:  # keycode of Backspace
            self.calc_string = self.calc_string[: -1]
            self.update()
            return
        if k > 128:  # no relevant characters above this keyID
            return
        k = chr(k)
        if k == ".":  # comma for dot
            k = ","
        if k == "=":  # Wanna calculate result?
            if self.dial_res.isEnabled():
                self.calc_result()
                self.update()
                return
        if self.filter_char(k):  # Last filter
            return
        self.calc_string += k
        self.update()

    """
        Calculating results:
    """

    def calc_result(self):

        d_string = self.calc_string.replace(",", ".")
        d_string = eval(d_string)
        self.result = str(round(d_string, 4)).replace(".", ",")
        self.calc_list.insert(0, " = " + self.calc_string)
        self.calc_list.insert(0, self.result)
        self.calc_string = self.result
        print(" = ", self.result)
        self.update_list()
        return

    @staticmethod
    def filter_char(char):
        sym = ["/", "*", "-", "+", ","]
        if char.isnumeric():
            return False
        if char in sym:
            return False
        return True

    """
        Update & draw list of calculations (calc_list):
    """

    def update_list(self):
        try:
            self.calc_list.insert(2, self.calc_list.pop(2) + self.calc_list.pop(2))
            self.calc_list.pop(self.MAX_ITEMS_IN_LIST)
        except IndexError:
            pass
        self.last_Calc.clear()
        for i in range(1, len(self.calc_list)):
            try:
                self.last_Calc.addItem(self.calc_list[i])
            except IndexError:
                pass


def main():
    app = Qt.QApplication(sys.argv)
    win = Calculator()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
