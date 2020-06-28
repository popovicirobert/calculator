#python -m PyQt5.uic.pyuic -x [FILENAME].ui -o [FILENAME].py

#style = '''
'''QPushButton {
    background-color: light gray
}
QPushButton:hover {
    background-color: blue;
    color: white;
}'''
#'''


from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut, QMenuBar
from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QKeySequence
import sys, clipboard
from expression_evaluator import ExpressionEvaluator

class MyCalculatorWindow(QMainWindow):

    def __init__(self):
        super(MyCalculatorWindow, self).__init__()

        self.SCREEN_WIDTH = 520
        self.SCREEN_HEIGHT = 590

        self.LABEL_WIDTH = 480
        self.LABEL_HEIGHT = 170

        self.BUTTON_WIDTH = 105
        self.BUTTON_HEIGHT = 50

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
        self.LIGHT_MODE_MENU = '''
        menuBar {
            background-color: light gray;
            color: black;
        }
        menuBar:hover{
            background-color: light blue;
            color: black;
        }
        '''

        self.DARK_MODE_LABEL = '''
        QLabel {
            background-color: #424242;
            color: white
        }
        '''
        self.DARK_MODE_BUTTON = '''
        QPushButton {
            background-color: rgb(30, 30, 30);
            color: white;
        }
        '''
        self.DARK_MODE_MENU = '''
        background-color: #424242;
        color: white;
        '''


        self.light_mode = True

        self.label = None
        self.ce_button = None
        self.open_bracket_button = None
        self.close_bracket_button = None
        self.delete_button = None
        self.button7 = None
        self.button8 = None
        self.button9 = None
        self.divide_button = None
        self.button4 = None
        self.button5 = None
        self.button6 = None
        self.multiply_button = None
        self.button1 = None
        self.button2 = None
        self.button3 = None
        self.minus_button = None
        self.period_button = None
        self.button0 = None
        self.equal_button = None
        self.plus_button = None


        self.initUI()

    def make_new_button(self, x, y, text, shortcut_sequence = ''):

        button = QtWidgets.QPushButton(self)
        button.setFixedSize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        button.move(x, y)
        button.setText(text)

        self.BUTTON_FONT = 15
        button.setFont(QFont('Arial', self.BUTTON_FONT))

        shortcut = QShortcut(QKeySequence(shortcut_sequence), self)
        shortcut.activated.connect(lambda: self.add_character(text))

        if self.light_mode == True:
            style = self.LIGHT_MODE_BUTTON
        else:
            style = self.DARK_MODE_BUTTON

        button.setStyleSheet(style)

        if text in ('+', '-', '/', 'x', 'DEL') and self.light_mode == False:
            button.setStyleSheet('background-color: rgb(254, 140, 0)')

        return button

    def init_label(self):
        if not self.label:
            self.label = QtWidgets.QLabel(self)
            self.label.setGeometry(self.WIDTH_SPACE, self.HEIGHT_SPACE + self.MENU_HEIGHT,
                                   self.LABEL_WIDTH, self.LABEL_HEIGHT)
            self.label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

            self.BIG_LABEL_FONT = 25
            self.SMALL_LABEL_FONT = 15
            self.TEXT_LIMIT = 17
            self.label_font = self.BIG_LABEL_FONT
            self.label.setFont(QFont('Arial', self.label_font))

            self.typed_text = '0'
            self.label.setText(self.typed_text)

        if self.light_mode == True:
            style = self.LIGHT_MODE_LABEL
        else:
            style = self.DARK_MODE_LABEL

        self.label.setStyleSheet(style)


    def init_buttons(self):


        '''self.ce_button = self.make_new_button(self.WIDTH_SPACE,
                                              2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + self.MENU_HEIGHT,
                                              'CE')

        self.open_bracket_button = self.make_new_button(2 * self.WIDTH_SPACE + self.BUTTON_WIDTH,
                                                        2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + self.MENU_HEIGHT,
                                                        '(', shortcut_sequence='(')

        self.close_bracket_button = self.make_new_button(3 * self.WIDTH_SPACE + 2 * self.BUTTON_WIDTH,
                                                         2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + self.MENU_HEIGHT,
                                                         ')', shortcut_sequence=')')

        self.delete_button = self.make_new_button(4 * self.WIDTH_SPACE + 3 * self.BUTTON_WIDTH,
                                                  2 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + self.MENU_HEIGHT,
                                                'DEL', shortcut_sequence='Backspace')

        self.button7 = self.make_new_button(self.WIDTH_SPACE,
                                            3 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + self.BUTTON_HEIGHT
                                            + self.MENU_HEIGHT,
                                            '7', shortcut_sequence='7')

        self.button8 = self.make_new_button(2 * self.WIDTH_SPACE + self.BUTTON_WIDTH,
                                            3 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + self.BUTTON_HEIGHT
                                            + self.MENU_HEIGHT,
                                            '8', shortcut_sequence='8')

        self.button9 = self.make_new_button(3 * self.WIDTH_SPACE + 2 * self.BUTTON_WIDTH,
                                            3 * self.HEIGHT_SPACE + self.LABEL_HEIGHT + self.BUTTON_HEIGHT
                                            + self.MENU_HEIGHT,
                                            '9', shortcut_sequence='9')

        self.divide_button = self.make_new_button(4 * self.WIDTH_SPACE + 3 * self.BUTTON_WIDTH,
                                                  3 * self.HEIGHT_SPACE + self.LABEL_HEIGHT +
                                                  self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                                                  '/', shortcut_sequence='/')

        self.button4 = self.make_new_button(self.WIDTH_SPACE,
                                            4 * self.HEIGHT_SPACE + self.LABEL_HEIGHT +
                                            2 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                                            '4', shortcut_sequence='4')

        self.button5 = self.make_new_button(2 * self.WIDTH_SPACE + self.BUTTON_WIDTH,
                                            4 * self.HEIGHT_SPACE + self.LABEL_HEIGHT +
                                            2 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                                            '5', shortcut_sequence='5')

        self.button6 = self.make_new_button(3 * self.WIDTH_SPACE + 2 * self.BUTTON_WIDTH,
                                            4 * self.HEIGHT_SPACE + self.LABEL_HEIGHT +
                                            2 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                                            '6', shortcut_sequence='6')

        self.multiply_button = self.make_new_button(4 * self.WIDTH_SPACE + 3 * self.BUTTON_WIDTH,
                                                    4 * self.HEIGHT_SPACE + self.LABEL_HEIGHT +
                                                    2 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                                                    'x', shortcut_sequence='*')

        self.button1 = self.make_new_button(self.WIDTH_SPACE,
                                            5 * self.HEIGHT_SPACE + self.LABEL_HEIGHT +
                                            3 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                                            '1', shortcut_sequence='1')

        self.button2 = self.make_new_button(2 * self.WIDTH_SPACE + self.BUTTON_WIDTH,
                                            5 * self.HEIGHT_SPACE + self.LABEL_HEIGHT +
                                            3 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                                            '2', shortcut_sequence='2')

        self.button3 = self.make_new_button(3 * self.WIDTH_SPACE + 2 * self.BUTTON_WIDTH,
                                            5 * self.HEIGHT_SPACE + self.LABEL_HEIGHT +
                                            3 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                                            '3', shortcut_sequence='3')

        self.minus_button = self.make_new_button(4 * self.WIDTH_SPACE + 3 * self.BUTTON_WIDTH,
                                                 5 * self.HEIGHT_SPACE + self.LABEL_HEIGHT +
                                                 3 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                                                 '-', shortcut_sequence='-')

        self.period_button = self.make_new_button(self.WIDTH_SPACE,
                                                  6 * self.HEIGHT_SPACE + self.LABEL_HEIGHT +
                                                  4 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                                                  '.', shortcut_sequence='.')

        self.button0 = self.make_new_button(2 * self.WIDTH_SPACE + self.BUTTON_WIDTH,
                                            6 * self.HEIGHT_SPACE + self.LABEL_HEIGHT +
                                            4 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                                            '0', shortcut_sequence='0')

        self.equal_button = self.make_new_button(3 * self.WIDTH_SPACE + 2 * self.BUTTON_WIDTH,
                                                 6 * self.HEIGHT_SPACE + self.LABEL_HEIGHT +
                                                 4 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                                                 '=', shortcut_sequence='Return')

        self.plus_button = self.make_new_button(4 * self.WIDTH_SPACE + 3 * self.BUTTON_WIDTH,
                                                6 * self.HEIGHT_SPACE + self.LABEL_HEIGHT +
                                                4 * self.BUTTON_HEIGHT + self.MENU_HEIGHT,
                                                '+', shortcut_sequence='+')
        '''

        self.buttons = [[self.ce_button, 'CE', ],]

        self.attach_button_functions()


    def copy_action_function(self):
        clipboard.copy(self.typed_text)

    def paste_action_function(self):
        current_paste = clipboard.paste()
        for character in current_paste:
            self.add_character(character)

    def exit_action_function(self):
        sys.exit()

    def dark_mode_action_function(self):
        self.setStyleSheet('background-color: #303030')
        self.light_mode = False
        self.init_label()
        self.init_buttons()
        self.light_mode_action.setCheckable(False)
        self.dark_mode_action.setCheckable(True)
        self.menu_bar.setStyleSheet(self.DARK_MODE_MENU)

    def light_mode_action_function(self):
        self.setStyleSheet('background-color: light gray')
        self.light_mode = True
        self.init_label()
        self.init_buttons()
        self.light_mode_action.setCheckable(True)
        self.dark_mode_action.setCheckable(False)
        self.menu_bar.setStyleSheet(self.LIGHT_MODE_MENU)

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
            answer = expr_eval.evaluate_expression()

            if answer != 'Error':
                if int(answer) == answer:
                    answer = int(answer)
                else:
                    answer = round(answer, 12)

            self.typed_text = str(answer)
        else:
            self.typed_text += character

        if len(self.typed_text) > self.TEXT_LIMIT:
            self.label_font = self.SMALL_LABEL_FONT
        else:
            self.label_font = self.BIG_LABEL_FONT

        self.label.setFont(QFont('Arial', self.label_font))
        self.label.setText(self.typed_text)


    def attach_button_functions(self):
        '''self.button0.clicked.connect(lambda: self.add_character('0'))
        self.button1.clicked.connect(lambda: self.add_character('1'))
        self.button2.clicked.connect(lambda: self.add_character('2'))
        self.button3.clicked.connect(lambda: self.add_character('3'))
        self.button4.clicked.connect(lambda: self.add_character('4'))
        self.button5.clicked.connect(lambda: self.add_character('5'))
        self.button6.clicked.connect(lambda: self.add_character('6'))
        self.button7.clicked.connect(lambda: self.add_character('7'))
        self.button8.clicked.connect(lambda: self.add_character('8'))
        self.button9.clicked.connect(lambda: self.add_character('9'))
        self.ce_button.clicked.connect(lambda: self.add_character('CE'))
        self.delete_button.clicked.connect(lambda: self.add_character('DEL'))
        self.equal_button.clicked.connect(lambda: self.add_character('='))
        self.plus_button.clicked.connect(lambda: self.add_character('+'))
        self.multiply_button.clicked.connect(lambda: self.add_character('x'))
        self.minus_button.clicked.connect(lambda: self.add_character('-'))
        self.divide_button.clicked.connect(lambda: self.add_character(r'/'))
        self.period_button.clicked.connect(lambda: self.add_character('.'))
        self.open_bracket_button.clicked.connect(lambda: self.add_character('('))
        self.close_bracket_button.clicked.connect(lambda: self.add_character(')'))
        '''
        pass

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