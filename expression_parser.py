# expression_parser.py

import re
import math

# 正则表达式，用于识别输入中的数学运算符、数字和函数名等。该正则表达式涵盖了加减乘除、乘方、用于函数名和变量名的字母序列等。
ZZBDS = re.compile(r'\*\*|\d+\.\d+|\d+|[-+*/()]|[a-zA-Z_][a-zA-Z0-9_]*')

jibenyvnsuan = {
    # 映射到lambda函数，返回对应的操作
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b,
    '**': lambda a, b: a ** b
}
# 定义了一组映射关系，将数学函数名称映射到Python math
# 库中相应的函数。这样做使得程序能够根据函数名调用正确的数学运算进行计算。
ZIDIANYINGSHE = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'sqrt': math.sqrt,
    'abs': abs,
    'max': max,
    'min': min
}

caozuofuyouxianji = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '**': 3
}
# 判断是否是操作符
def is_operator(token):
    return token in jibenyvnsuan
# 如果正则表达式的 match 函数返回的是非 None，则该令牌为数字。
def is_number(token):
    return re.match(r"^\d+\.?\d*$", token) is not None

def is_function(token):
    return token in ZIDIANYINGSHE

def tokenize(expression):
    # 匹配整个字符串中所有符合正则表达式的片段，返回一个令牌列表 tokens
    tokens = ZZBDS.findall(expression)
    processed_tokens = []

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '-' and (i == 0 or tokens[i - 1] in '/*-+('):
            processed_tokens.append(token + tokens[i + 1])
            i += 1
        else:
            processed_tokens.append(token)
        i += 1

    return processed_tokens

def infix_to_postfix(expression_tokens):

    # 函数将通常的中缀表达式转换为后缀表达式（逆波兰表示法）
    shuchuliebiao = []
    caozuofuzhan = []

    for token in expression_tokens:
        if is_number(token) or (token.startswith('-') and is_number(token[1:])):
            shuchuliebiao.append(token)
        elif token.isalpha() and not is_function(token):
            shuchuliebiao.append(token)
        elif is_function(token):
            caozuofuzhan.append(token)
        elif token == '(':
            caozuofuzhan.append(token)
        elif token == ')':
            while caozuofuzhan and caozuofuzhan[-1] != '(':
                shuchuliebiao.append(caozuofuzhan.pop())
            caozuofuzhan.pop()
            if caozuofuzhan and is_function(caozuofuzhan[-1]):
                shuchuliebiao.append(caozuofuzhan.pop())
        elif is_operator(token):
            while (caozuofuzhan and caozuofuzhan[-1] != '(' and
                   caozuofuyouxianji.get(token, 0) <= caozuofuyouxianji.get(caozuofuzhan[-1], 0)):
                shuchuliebiao.append(caozuofuzhan.pop())
            caozuofuzhan.append(token)

    while caozuofuzhan:
        shuchuliebiao.append(caozuofuzhan.pop())

    return shuchuliebiao

def evaluate_postfix(postfix_tokens, variable_values=None):
    if variable_values is None:
        variable_values = {}

    stack = []

    for token in postfix_tokens:
        print(f"Token: {token}, Stack: {stack}")  # Debugging purpose
        if token in jibenyvnsuan:
            if len(stack) < 2:
                raise ValueError(f"Not enough operands available for '{token}'")
            op2 = stack.pop()
            op1 = stack.pop()
            operation = jibenyvnsuan[token]
            stack.append(operation(op1, op2))
        elif token in ZIDIANYINGSHE:
            if len(stack) < 1:
                raise ValueError(f"Not enough arguments available for '{token}'")
            arg = stack.pop()
            result = ZIDIANYINGSHE[token](arg)
            stack.append(result)
        elif token.lstrip('-').replace('.', '', 1).isdigit():
            stack.append(float(token))
        elif token in variable_values:
            stack.append(float(variable_values[token]))
        else:
            raise ValueError(f"Unexpected token: {token}")

    if len(stack) != 1:
        raise ValueError("The stack did not end with a single result, indicating an error in expression.")
    return stack.pop()

# if __name__ == "__main__":
#     expression1 = "(7+5)/2-2.6**3+3*sin(2+5)-sqrt(9)"
#     tokens1 = tokenize(expression1)
#     postfix_expression1 = infix_to_postfix(tokens1)
#     print("Tokens:", tokens1)
#     print("Postfix Expression:", postfix_expression1)
#     try:
#         result1 = evaluate_postfix(postfix_expression1)
#         print("Result:", result1)
#     except Exception as e:
#         print("An error occurred:", e)
#
#     expression2 = "abs(-6)"
#     tokens2 = tokenize(expression2)
#     postfix_expression2 = infix_to_postfix(tokens2)
#     print("Tokens:", tokens2)
#     print("Postfix Expression:", postfix_expression2)
#     try:
#         result2 = evaluate_postfix(postfix_expression2)
#         print("Result:", result2)
#     except Exception as e:
#         print("An error occurred:", e)
