#python -m PyQt5.uic.pyuic -x [FILENAME].ui -o [FILENAME].py



from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut
from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QKeySequence, QFontMetrics
import sys, decimal, clipboard
from functools import partial
from expression_evaluator import ExpressionEvaluator

class MyCalculatorWindow(QMainWindow):

    def __init__(self):
        super(MyCalculatorWindow, self).__init__()

        self.SCREEN_WIDTH = 600
        self.SCREEN_HEIGHT = 900

        self.LABEL_WIDTH = 560
        self.LABEL_HEIGHT = 300

        self.BUTTON_WIDTH = 140
        self.BUTTON_HEIGHT = 102

        self.WIDTH_SPACE = 20
        self.HEIGHT_SPACE = 20

        self.MENU_HEIGHT = 30

        self.LIGHT_MODE_LABEL = '''
        QLabel {
            background-color: white;
            color: black;
        }
        '''
        self.LIGHT_MODE_BUTTON = '''
        QPushButton {
            background-color: light gray;
            color: black;
        }
        QPushButton:hover{
            background-color: light blue;
            color: black;
        }
        '''
        self.LIGHT_MODE_MENU_BAR = '''
        QMenuBar {
            background-color: light gray;
            color: black;
        }
        QMenuBar::item:selected {
            background-color: light blue;
            color: black;
        }
        '''
        self.LIGHT_MODE_MENU = '''
        QMenu {
            background-color: light gray;
            color: black;
        }
        QMenu:selected {
            background-color: light blue;
            color: black;
        }
        '''

        self.DARK_MODE_LABEL = '''
        QLabel {
            background-color: rgb(66, 66, 66);
            color: white
        }
        '''
        self.DARK_MODE_BUTTON = '''
        QPushButton {
            background-color: rgb(30, 30, 30);
            color: white;
        }
        QPushButton:hover {
            background-color: rgb(40, 40, 40);
            color: white;
        }
        '''
        self.DARK_MODE_ORANGE_BUTTON = '''
        QPushButton {
            background-color: rgb(255, 140, 0);
            color: white;
        }
        QPushButton:hover {
            background-color: orange;
            color: white;
        }
        '''

        self.DARK_MODE_MENU_BAR = '''
        QMenuBar {
            background-color: rgb(45, 45, 45);
            color: white;
        }
        QMenuBar::item:selected {
            background-color: rgb(60, 60, 60);
            color: white;
        }
        '''
        self.DARK_MODE_MENU = '''
        QMenu {
            background-color: rgb(45, 45, 45);
            color: white;
        }
        QMenu:selected {
            background-color: rgb(60, 60, 60);
            color: white;
        }
        '''

        self.light_mode = True

        self.initUI()


    def init_label(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(self.WIDTH_SPACE, self.HEIGHT_SPACE + self.MENU_HEIGHT,
                               self.LABEL_WIDTH, self.LABEL_HEIGHT)
        self.label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        self.LABEL_FONT_SIZE = 35
        self.label_font_size = self.LABEL_FONT_SIZE
        self.label.setFont(QFont('Arial', self.label_font_size))

        self.typed_text = '0'
        self.label.setText(self.typed_text)

        self.label.setStyleSheet(self.LIGHT_MODE_LABEL)


    def make_new_button(self, x, y, text, shortcut_sequence):
        button = QtWidgets.QPushButton(self)
        button.setGeometry(x, y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        button.setText(text)

        self.BUTTON_FONT = 15
        button.setFont(QFont('Arial', self.BUTTON_FONT))

        shortcut = QShortcut(QKeySequence(shortcut_sequence), self)
        shortcut.activated.connect(lambda: self.add_character(text))

        button.setStyleSheet(self.LIGHT_MODE_BUTTON)

        return button


    def init_buttons(self):

        self.buttons = [[None, self.WIDTH_SPACE,
                         2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + self.MENU_HEIGHT,
                         'CE', ''],

                        [None, self.WIDTH_SPACE + self.BUTTON_WIDTH,
                         2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + self.MENU_HEIGHT,
                         '(', '('],

                        [None, self.WIDTH_SPACE + 2 * self.BUTTON_WIDTH,
                         2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + self.MENU_HEIGHT,
                         ')', ')'],

                        [None, self.WIDTH_SPACE + 3 * self.BUTTON_WIDTH,
                         2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + self.MENU_HEIGHT,
                         'DEL', 'Backspace'],

                        [None, self.WIDTH_SPACE,
                         2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                         '7', '7'],

                        [None, self.WIDTH_SPACE + self.BUTTON_WIDTH,
                         2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                         '8', '8'],

                        [None, self.WIDTH_SPACE + 2 * self.BUTTON_WIDTH,
                         2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                         '9', '9'],

                        [None, self.WIDTH_SPACE + 3 * self.BUTTON_WIDTH,
                         2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                         '/', '/'],

                        [None, self.WIDTH_SPACE,
                         2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + 2 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                         '4', '4'],

                        [None, self.WIDTH_SPACE + self.BUTTON_WIDTH,
                         2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + 2 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                         '5', '5'],

                        [None, self.WIDTH_SPACE + 2 * self.BUTTON_WIDTH,
                         2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + 2 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                         '6', '6'],

                        [None, self.WIDTH_SPACE + 3 * self.BUTTON_WIDTH,
                         2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + 2 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                         'x', '*'],

                        [None, self.WIDTH_SPACE,
                         2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + 3 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                         '1', '1'],

                        [None, self.WIDTH_SPACE + self.BUTTON_WIDTH,
                         2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + 3 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                         '2', '2'],

                        [None, self.WIDTH_SPACE + 2 * self.BUTTON_WIDTH,
                         2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT +
                         3 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                         '3', '3'],

                        [None, self.WIDTH_SPACE + 3 * self.BUTTON_WIDTH,
                         2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + 3 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                         '-', '-'],

                        [None, self.WIDTH_SPACE,
                         2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + 4 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                         '.', '.'],

                        [None, self.WIDTH_SPACE + self.BUTTON_WIDTH,
                         2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + 4 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                         '0', '0'],

                        [None, self.WIDTH_SPACE + 2 * self.BUTTON_WIDTH,
                         2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + 4 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                         '=', 'Return'],

                        [None, self.WIDTH_SPACE + 3 * self.BUTTON_WIDTH,
                         2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + 4 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                         '+', '+']

                        ]

        for index in range(len(self.buttons)):
            self.buttons[index][0] = self.make_new_button(self.buttons[index][1], self.buttons[index][2],
                                                          self.buttons[index][3], self.buttons[index][4])

        self.attach_button_functions()


    def attach_button_functions(self):
        for index in range(len(self.buttons)):
            self.buttons[index][0].clicked.connect(partial(self.add_character, self.buttons[index][3]))


    def copy_action_function(self):
        clipboard.copy(self.typed_text)

    def paste_action_function(self):
        current_paste = clipboard.paste()
        for character in current_paste:
            self.add_character(character)

    def exit_action_function(self):
        sys.exit()

    def update_label(self):
        if self.light_mode == True:
            style = self.LIGHT_MODE_LABEL
        else:
            style = self.DARK_MODE_LABEL
        self.label.setStyleSheet(style)

    def update_buttons(self):
        if self.light_mode == True:
            style = self.LIGHT_MODE_BUTTON
        else:
            style = self.DARK_MODE_BUTTON

        for index in range(len(self.buttons)):
            if self.buttons[index][3] in ('+', '-', '/', 'x', 'DEL')\
                    and self.light_mode == False:
                self.buttons[index][0].setStyleSheet(self.DARK_MODE_ORANGE_BUTTON)
            else:
                self.buttons[index][0].setStyleSheet(style)


    def dark_mode_action_function(self):
        self.setStyleSheet('background-color: rgb(48, 48, 48)')
        self.light_mode = False
        self.update_label()
        self.update_buttons()

        self.menu_bar.setStyleSheet(self.DARK_MODE_MENU_BAR)
        self.menu_file.setStyleSheet(self.DARK_MODE_MENU)
        self.menu_edit.setStyleSheet(self.DARK_MODE_MENU)
        self.menu_settings.setStyleSheet(self.DARK_MODE_MENU)


    def light_mode_action_function(self):
        self.setStyleSheet('background-color: light gray')
        self.light_mode = True
        self.update_label()
        self.update_buttons()

        self.menu_bar.setStyleSheet(self.LIGHT_MODE_MENU_BAR)
        self.menu_file.setStyleSheet(self.LIGHT_MODE_MENU)
        self.menu_edit.setStyleSheet(self.LIGHT_MODE_MENU)
        self.menu_settings.setStyleSheet(self.LIGHT_MODE_MENU)


    def init_menu(self):
        self.menu_bar = self.menuBar()
        self.menu_bar.setGeometry(0, 0, self.SCREEN_WIDTH, self.MENU_HEIGHT)

        self.menu_file = self.menu_bar.addMenu('File')
        self.menu_edit = self.menu_bar.addMenu('Edit')
        self.menu_settings = self.menu_bar.addMenu('Settings')

        self.exit_action = self.menu_file.addAction('Exit')
        self.copy_action = self.menu_edit.addAction('Copy')
        self.paste_action = self.menu_edit.addAction('Paste')

        self.dark_mode_action = self.menu_settings.addAction('Dark mode')
        self.light_mode_action = self.menu_settings.addAction('Light mode')


        self.exit_action.setShortcut('Esc')
        self.exit_action.triggered.connect(self.exit_action_function)

        self.copy_action.setShortcut('Ctrl+C')
        self.copy_action.triggered.connect(self.copy_action_function)
        self.paste_action.setShortcut('Ctrl+V')
        self.paste_action.triggered.connect(self.paste_action_function)

        self.light_mode_action.triggered.connect(self.light_mode_action_function)
        self.dark_mode_action.triggered.connect(self.dark_mode_action_function)

    def adjust_label_font(self):
        font = QFont('Arial', self.label_font_size)
        fm = QFontMetrics(font)

        label_width = self.label.frameGeometry().width()

        while self.label_font_size < self.LABEL_FONT_SIZE and \
                fm.width(self.typed_text) <= label_width:
            self.label_font_size += 1
            font = QFont('Arial', self.label_font_size)
            fm = QFontMetrics(font)


        while fm.width(self.typed_text) >= label_width:
            self.label_font_size -= 1
            font = QFont('Arial', self.label_font_size)
            fm = QFontMetrics(font)

        self.label.setFont(font)


    def add_character(self, character):
        if character.isdigit() == True:
            if self.typed_text[-1] == '0':
                if len(self.typed_text) == 1 or self.typed_text[-2].isdigit() == False:
                    self.typed_text = self.typed_text[:-1]

            self.typed_text += character

        elif character == 'CE':
            self.typed_text = '0'

        elif character == 'DEL':
            if len(self.typed_text) == 1:
                self.typed_text = '0'
            else:
                self.typed_text = self.typed_text[:-1]

        elif character == '(':
            if len(self.typed_text) == 1 and self.typed_text[0] == '0':
                self.typed_text = '('
            else:
                self.typed_text += '('

        elif character == '=':
            expr_eval = ExpressionEvaluator(self.typed_text)
            fraction = expr_eval.evaluate_expression()

            if fraction[0] != 'Error':
                answer = decimal.Decimal(fraction[0]) / decimal.Decimal(fraction[1])
            else:
                answer = 'Error'

            self.typed_text = str(answer)
        else:
            self.typed_text += character

        self.adjust_label_font()
        self.label.setText(self.typed_text)


    def initUI(self):
        self.setFixedSize(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.setWindowTitle('Calculator')

        self.init_label()
        self.init_buttons()
        self.init_menu()


if __name__ == '__main__':
    calculator_app = QApplication(sys.argv)
    window = MyCalculatorWindow()
    window.show()
    sys.exit(calculator_app.exec_())