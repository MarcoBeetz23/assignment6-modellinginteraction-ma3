import sys
import time

from PyQt5 import uic, Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.uic.Compiler.qtproxies import QtGui


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
        print("timestamp, key, input_type")
        self.test_started = False

    def initUI(self):
        self.setWindowTitle('Calculator')
        self.resize(500, 450)

        """
            Declaring & connecting all buttons...
        """

        self.dial_res.clicked.connect(lambda: self.b_calc_clicked("res"))
        self.dial_dif.clicked.connect(lambda: self.b_calc_clicked("/"))
        self.dial_mul.clicked.connect(lambda: self.b_calc_clicked("*"))
        self.dial_min.clicked.connect(lambda: self.b_calc_clicked("-"))
        self.dial_plu.clicked.connect(lambda: self.b_calc_clicked("+"))

        self.dial_dot.clicked.connect(lambda: self.b_calc_clicked(","))
        self.dial_bs.clicked.connect(lambda: self.b_calc_clicked("bs"))
        self.clear_all.clicked.connect(lambda: self.b_calc_clicked("ca"))

        self.dial_0.clicked.connect(lambda: self.b_calc_clicked("0"))
        self.dial_1.clicked.connect(lambda: self.b_calc_clicked("1"))
        self.dial_2.clicked.connect(lambda: self.b_calc_clicked("2"))
        self.dial_3.clicked.connect(lambda: self.b_calc_clicked("3"))
        self.dial_4.clicked.connect(lambda: self.b_calc_clicked("4"))
        self.dial_5.clicked.connect(lambda: self.b_calc_clicked("5"))
        self.dial_6.clicked.connect(lambda: self.b_calc_clicked("6"))
        self.dial_7.clicked.connect(lambda: self.b_calc_clicked("7"))
        self.dial_8.clicked.connect(lambda: self.b_calc_clicked("8"))
        self.dial_9.clicked.connect(lambda: self.b_calc_clicked("9"))

    """
        Declaring button methods -.- ...
    """

    def b_calc_clicked(self, symbol):
        if not self.test_started:
            self.test_started = self.__note_test_state_change("BUTTON", self.test_started)
        self.__generate_timestamp(symbol, "BUTTON")
        if symbol == "res":
            self.calc_result()
        elif symbol == "bs":
            self.calc_string = self.calc_string[: -1]
        elif symbol == "ca":
            self.calc_string = ""
        else:
            self.calc_string += symbol
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
        # print(end="\r")
        # print(self.calc_string, end='')
        self.result_label.setText(str(self.result))
        return

    """
        Handle keystroke:
    """

    def keyPressEvent(self, event):
        input_type = "KEYSTROKE"
        if not self.test_started:
            self.test_started = self.__note_test_state_change(input_type, self.test_started)
        k = event.key()
        if k == 16777219:  # keycode of Backspace
            self.calc_string = self.calc_string[: -1]
            self.__generate_timestamp("bs", input_type)
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
                self.__generate_timestamp("res", input_type)
                self.update()
                return
        if self.filter_char(k):  # Last filter
            return
        self.__generate_timestamp(k, input_type)
        self.calc_string += k
        self.update()

    """
        generating Timestamps:
    """

    @staticmethod
    def __generate_timestamp(symbol, input_type):
        print(str(time.time()) + ", " + str(symbol) + ",", input_type)

    def __note_test_state_change(self, input_type, state):
        event_name = "START"
        if state:
            event_name = "END"
        self.__generate_timestamp(event_name, input_type)
        return not state

    def closeEvent(self, event):
        if self.test_started:
            self.__note_test_state_change("BUTTON", self.test_started)

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
        # print(" = ", self.result)
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
