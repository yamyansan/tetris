#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import subprocess
from argparse import ArgumentParser
from start import start
from start import get_option as get_input_option
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator


class MainWindow(QMainWindow):

    param_height = 50

    label_list = [
        ["user name", ["user_name", "u"]],
        ["game level", ["game_level", "l"]],
        ["game time", ["game_time", "t"], ": (s)"],
        [
            "mode",
            ["mode", "m"],
            [
                "default",
                "keyboard",
                "gamepad",
                "sample",
                "art",
                "train",
                "predict",
                "train_sample",
                "predict_sample",
                "train_sample2",
                "predict_sample2",
            ],
        ],
    ]

    def __init__(self):
        super().__init__()
        self.args = MainWindow.get_option()
        self.title = "tetris control"
        self.width = 380
        self.height = (len(MainWindow.label_list) + 1) * 50

        self.setWindowTitle(self.title)
        self.setGeometry(320, 240, self.width, self.height)
        self.qedit = {}
        self.qcombobox = {}
        button_colum = 0
        for i, l in enumerate(MainWindow.label_list):
            print(i, l)
            if len(l) == 3:
                if isinstance(l[2], list):
                    self.set_select(column=i, name=l[0], tag=l[1][0], labels=l[2])
                else:
                    self.set_label(column=i, name=l[0], tag=l[1][0], ext_label=l[2])
            else:
                self.set_label(column=i, name=l[0], tag=l[1][0])
            button_colum = i + 1
        # ボタン
        btn = QPushButton("Start", self)
        btn.move(20, MainWindow.param_height * button_colum)
        btn.resize(self.width - 40, 30)
        btn.clicked.connect(self.click_event)
        self.show()

    def reset_argv():
        for l in MainWindow.label_list:
            for i, tag in enumerate(l[1]):
                if i == 0:
                    t = "--" + tag
                else:
                    t = "-" + tag
                if t in sys.argv:
                    del sys.argv[sys.argv.index(t) : sys.argv.index(t) + 2]
                    break

    def update_argv(tag, param):
        sys.argv.append("--" + tag)
        sys.argv.append(param)

    def click_event(self):
        MainWindow.reset_argv()
        for l, e in self.qedit.items():
            if type(getattr(self.args, l)) is int:
                setattr(self.args, l, int(e.text()))
            else:
                setattr(self.args, l, e.text())
            MainWindow.update_argv(l, e.text())
        for l, e in self.qcombobox.items():
            setattr(self.args, l, e.currentText())
            MainWindow.update_argv(l, e.currentText())
        print(sys.argv)

        start()

    def set_label(self, column: int, name: str, tag: str, ext_label: str = None):
        qlabel = QLabel(name, self)
        qlabel.move(20, column * MainWindow.param_height)
        tmpl = QLabel(":", self)
        tmpl.move(110, column * MainWindow.param_height)
        self.qedit[tag] = QLineEdit(self)
        if type(getattr(self.args, tag)) is int:
            self.qedit[tag].setValidator(QIntValidator())
        self.qedit[tag].setText(str(getattr(self.args, tag)))
        self.qedit[tag].move(120, column * MainWindow.param_height)
        self.qedit[tag].resize(200, 35)
        self.qedit[tag].setAlignment(Qt.AlignRight)
        if ext_label is not None:
            extlabel = QLabel(ext_label, self)
            extlabel.move(320, column * MainWindow.param_height)

    def set_select(self, column: int, name: str, tag: str, labels):
        qlabel = QLabel(name, self)
        qlabel.move(20, column * MainWindow.param_height)
        self.qcombobox[tag] = QComboBox(self)
        for l in labels:
            self.qcombobox[tag].addItem(l)
        self.qcombobox[tag].resize(200, 35)
        self.qcombobox[tag].move(120, column * MainWindow.param_height)

    def get_option():
        ## default value
        GAME_LEVEL = 1
        GAME_TIME = 180
        IS_MODE = "default"
        IS_SAMPLE_CONTROLL = "n"
        INPUT_RANDOM_SEED = -1
        INPUT_DROP_INTERVAL = -1
        DROP_INTERVAL = 1000  # drop interval
        RESULT_LOG_JSON = "result.json"
        USER_NAME = "window_sample"
        SHAPE_LIST_MAX = 6
        BLOCK_NUM_MAX = -1
        TRAIN_YAML = "config/default.yaml"
        PREDICT_WEIGHT = "outputs/latest/best_weight.pt"
        ART_CONFIG = "default.json"

        ## update value if args are given
        args = get_input_option(
            GAME_LEVEL,
            GAME_TIME,
            IS_MODE,
            INPUT_RANDOM_SEED,
            INPUT_DROP_INTERVAL,
            RESULT_LOG_JSON,
            TRAIN_YAML,
            PREDICT_WEIGHT,
            USER_NAME,
            SHAPE_LIST_MAX,
            BLOCK_NUM_MAX,
            ART_CONFIG,
        )
        return args


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    # app.exec()
    sys.exit(app.exec_())
    # start()
