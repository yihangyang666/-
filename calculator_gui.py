# # calculator_gui.py
import sys
import re
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLineEdit,
    QVBoxLayout, QWidget, QGridLayout, QMessageBox, QInputDialog, QSizePolicy
)
from expression_evaluator import ZIDIANYINGSHE, evaluate_postfix
from expression_parser import infix_to_postfix, tokenize

class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('表达式求值器1.0')
        self.setGeometry(500, 300, 400, 450)

        # 给所有按钮和显示区域设置样式，包括透明度
        self.setStyleSheet("""
            QMainWindow {
                background-image: url(R.jpg);
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover; /* 如果你想要背景图覆盖整个窗口 */
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 150); /* 将alpha值降低以增加透明度 */
                border-radius: 5px; /* 设置按钮的圆角 */
                color: black; /* 按钮文本颜色 */
            }
            QLineEdit {
                background-color: rgba(255, 255, 255, 150); /* 同样降低显示区域的alpha值 */
                color: black; /* 输入框文本颜色 */
            }
            QLabel {
                background-color: rgba(255, 255, 255, 150); /* 标题背景半透明 */
                color: black; /* 标题文本颜色 */
            }
        """)
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.general_layout = QVBoxLayout()

        self.create_display()
        self.create_buttons()
        self.setup_connections()

        self.main_widget.setLayout(self.general_layout)

    def create_display(self):
        self.input_display = QLineEdit()
        self.input_display.setFixedHeight(35)
        self.input_display.setAlignment(Qt.AlignRight)
        self.input_display.setReadOnly(False)
        self.input_display.setFont(QFont("微软雅黑", 12))
        self.input_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.general_layout.addWidget(self.input_display)

        self.output_display = QLineEdit()
        self.output_display.setFixedHeight(35)
        self.output_display.setAlignment(Qt.AlignRight)
        self.output_display.setReadOnly(True)
        self.output_display.setFont(QFont("微软雅黑", 12))
        self.output_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.general_layout.addWidget(self.output_display)

    def create_button(self, text, pos, layout):
        button = QPushButton(text)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button.setFont(QFont("微软雅黑", 12))
        if text == '=':
            button.setStyleSheet("background-color: rgba(211, 211, 211, 150);")  # 浅红色
        elif text in '0123456789':
            button.setStyleSheet("background-color: rgba(240, 128, 128, 150);")
        else:
            button.setStyleSheet("background-color: rgba(173, 216, 230, 150);")  # 浅蓝色
        layout.addWidget(button, pos[0], pos[1])
        self.buttons[text] = button

    def create_buttons(self):
        self.buttons = {}
        buttons_layout = QGridLayout()
        buttons = {
            '7': (0, 0), '8': (0, 1), '9': (0, 2), '/': (0, 3), '清除': (0, 4),
            '4': (1, 0), '5': (1, 1), '6': (1, 2), '*': (1, 3), '(': (1, 4),
            '1': (2, 0), '2': (2, 1), '3': (2, 2), '.': (2, 3), ')': (2, 4),
            '-': (3, 0), '0': (3, 1), '+': (3, 2), '退格': (3, 3), 'sin': (3, 4),
            'max': (4, 0), 'min': (4, 1), ',': (4, 2), 'sqrt': (4, 3), '=': (4, 4)
        }
        for text, pos in buttons.items():
            self.create_button(text, pos, buttons_layout)
        self.general_layout.addLayout(buttons_layout)

    def setup_connections(self):
        for btn_text, btn in self.buttons.items():
            if btn_text == '=':
                btn.clicked.connect(self.on_equal)
            elif btn_text == '清除':
                btn.clicked.connect(self.clear)
            elif btn_text == '退格':
                btn.clicked.connect(self.backspace_expression)
            else:
                btn.clicked.connect(self.add_to_expression)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjust_font_size()

    def adjust_font_size(self):
        display_font = self.input_display.font()
        display_font_size = self.get_optimal_font_size(self.input_display)
        display_font.setPointSize(display_font_size)
        self.input_display.setFont(display_font)
        self.output_display.setFont(display_font)

        for button in self.buttons.values():
            button_font = button.font()
            button_font_size = self.get_optimal_font_size(button)
            button_font.setPointSize(button_font_size)
            button.setFont(button_font)

    def get_optimal_font_size(self, widget):
        widget_rect = widget.contentsRect()
        font = widget.font()
        font_metrics = QFontMetrics(font)
        optimal_size = font.pointSize()

        while True:
            if font_metrics.height() > widget_rect.height() or font_metrics.width(widget.text()) > widget_rect.width():
                optimal_size -= 1
                font.setPointSize(optimal_size)
                font_metrics = QFontMetrics(font)
            else:
                break

        return optimal_size

    def add_to_expression(self):
        button = self.sender()
        current_expression = self.get_input_text()
        new_expression = current_expression + button.text()
        self.set_input_text(new_expression)

    def is_function(self, token):
        return token in ZIDIANYINGSHE

    def on_equal(self):
        try:
            expression = self.get_input_text()
            tokens = tokenize(expression)
            variable_tokens = [token for token in tokens if token.isalpha() and not self.is_function(token)]
            if variable_tokens:
                variable_values = self.get_variable_values(variable_tokens)
                if variable_values is None:
                    return
                postfix_tokens = infix_to_postfix(tokens)
                result = evaluate_postfix(postfix_tokens, variable_values)
            else:
                postfix_tokens = infix_to_postfix(tokens)
                result = evaluate_postfix(postfix_tokens)
            #     输出表达式结果
            self.set_output_text(str(result))
        except Exception as e:
            # 输出错误原因
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            self.clear()

    def backspace_expression(self):
        current_expression = self.get_input_text()
        if current_expression:
            new_expression = current_expression[:-1]
            self.set_input_text(new_expression)

    def clear(self):
        self.set_input_text('')
        self.set_output_text('')
    # 用于在用户输入的表达式中收集并解析变量的值
    def get_variable_values(self, tokens):
        variable_values = {}
        seen_variables = set()
        for token in tokens:
            if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", token) and token not in ZIDIANYINGSHE:
                if token not in seen_variables:
                    while True:
                        value, ok = QInputDialog.getText(self, "Variable Input", f"Enter value for {token}:")
                        if ok and value:
                            try:
                                variable_values[token] = float(value)
                                seen_variables.add(token)
                                break
                            except ValueError:
                                QMessageBox.critical(self, "Error", f"Invalid input for {token}. Please enter a numeric value.")
                        else:
                            if not ok:
                                QMessageBox.warning(self, "Variable Input", "Calculation cancelled.")
                                return None
                            QMessageBox.critical(self, "Error", "Input required for the calculation.")
        return variable_values

    def set_input_text(self, text):
        self.input_display.setText(text)
        self.input_display.setFocus()

    def get_input_text(self):
        return self.input_display.text()

    def set_output_text(self, text):
        self.output_display.setText(text)

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("微软雅黑"))
    view = CalculatorApp()
    view.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()