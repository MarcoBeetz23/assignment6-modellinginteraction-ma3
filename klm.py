import configparser
import os
import sys


class Klm_File:
    def __init__(self, path, custom_operators=None):
        self.content = list()
        self.result_list = []
        self.result_list.append(self.content)
        self.__read_file(path)
        self.custom_operation_enabled = False
        if custom_operators is not None:
            self.custom_op = self.__setup_custom_op(custom_operators)
            if self.custom_op is not None:
                self.custom_operation_enabled = True
        self.calc_results()
        self.write_results()

    def __read_file(self, path):
        f = open(path, "r")
        enable_reading = True
        for line in f:
            content = ""
            for char in line:
                if char == "#":
                    enable_reading = False
                if char == "\n":
                    enable_reading = True
                if enable_reading:
                    char = self.__check_char(char, content)
                    if char is not None:
                        content += str(char)
            if content != "":
                self.content.append(content[:-1])

    @staticmethod
    def __check_char(char, content):
        string = ""
        if char.isalpha():
            string = char.lower()
            try:
                if content[-1].isnumeric():
                    string = "*" + string
            except IndexError:
                pass
            string += "+"
        if char.isnumeric():
            string = char
        return string

    def __interpret_operator(self, operator, use_cust):
        switch = {  # defaults defined by Card, Moran, Newell (1980) and Kieras (2011)
            "k": 0.28,
            "p": 1.10,
            "b": 0.10,
            "m": 1.20,
            "h": 0.40,
            "w": 0
        }
        if use_cust:
            return self.custom_op.get(operator)
        return switch.get(operator)

    @staticmethod
    def __setup_custom_op(path):
        switch = None
        try:
            config = configparser.ConfigParser()
            config.read(path)
            switch = {
                "k": float(config['Custom_KLM_Operators']['K']),
                "p": float(config['Custom_KLM_Operators']['P']),
                "b": float(config['Custom_KLM_Operators']['B']),
                "m": float(config['Custom_KLM_Operators']['M']),
                "h": float(config['Custom_KLM_Operators']['H']),
                "w": float(config['Custom_KLM_Operators']['W'])
            }
        except KeyError:
            dialog("confNVal")
        return switch

    def __results(self, use_cust):
        results = list()
        for line in self.content:
            for char in line:
                if char.isalpha():
                    line = line.replace(char, str(self.__interpret_operator(char, use_cust)))
            results.append(eval(line))
        return results

    def calc_results(self):
        self.result_list.append(self.__results(False))
        if self.custom_operation_enabled:
            self.result_list.append(self.__results(True))

    def write_results(self):
        string = ""
        for i in range(len(self.result_list)):
            sum = 0
            for j in range(len(self.result_list[i])):
                string += str(self.result_list[i][j]) + ", "
                if i != 0:
                    sum += self.result_list[i][j]
            string = string[:-2]
            if i != 0:
                modus = "default"
                if i > 1:
                    modus = "custom"
                string += " | " + modus + " -- Summe: " + str(sum)
            string += "\n"
        print(string)


def args_handler():  # how to handle the possible arguments (Dialogtree u.a)
    if len(sys.argv) != 2:
        exception_handler("noArgs")
    if not (os.path.isfile(sys.argv[1])):
        exception_handler("noFile")
    return sys.argv[1]


def exception_handler(case):  # exiting earlier due to .. reasons
    print(dialog(case))
    sys.exit()
    pass


def dialog(case):  # inspired from this website: https://data-flair.training/blogs/python-switch-case/
    switch = {  # a simple dialog manager
        "noArgs": "Please provide a filepath as an argument!",
        "noFile": "Couldn't open file!",
        "klmDef?": "Use KLM default operators?(Y/N) : ",
        "klmCust": "Please provide valid configuration file path for custom KLM operators: ",
        "confNVal": "Configuration file either not complete or doesn't posses the correct values\n"
                    "Next time please provide a configuration file with the following settings in the category\n"
                    "\'Custom_KLM_Operators\':\n"
                    "\'K\', \'P\', \'B\', \'M\', \'H\', \'W\'"
    }
    return switch.get(case)


def main():
    args = args_handler()
    operator_defaults = True
    operator_defaults = input(dialog("klmDef?")).lower()[0] != "n"
    if operator_defaults:
        file = Klm_File(args).__dict__
    else:
        while True:
            filepath = input(dialog("klmCust"))
            if os.path.isfile(filepath):
                break
        file = Klm_File(args, filepath).__dict__


if __name__ == "__main__":
    main()
