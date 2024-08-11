# expression_evaluator.py

import operator
from function import SinFunction, CosFunction, TanFunction, SqrtFunction, AbsFunction, MaxFunction, MinFunction


sin_function = SinFunction()
cos_function = CosFunction()
tan_function = TanFunction()
sqrt_function = SqrtFunction()
abs_function = AbsFunction()
max_function = MaxFunction()
min_function = MinFunction()


jibenyvnsuan = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '**': operator.pow
}

ZIDIANYINGSHE = {
    'sin': sin_function.evaluate,
    'cos': cos_function.evaluate,
    'tan': tan_function.evaluate,
    'sqrt': sqrt_function.evaluate,
    'abs': abs_function.evaluate,
    'max': max_function.evaluate,
    'min': min_function.evaluate,
}

# 求值后缀表达式的代码
def evaluate_postfix(postfix_tokens, variable_values=None):
    if variable_values is None:
        variable_values = {}

    stack = []

    for token in postfix_tokens:
        print(f"Token: {token}, Stack: {stack}")
        if token in jibenyvnsuan:
            if len(stack) < 2:
                raise ValueError(f"Not enough operands available for '{token}'")
            op2, op1 = stack.pop(), stack.pop()
            operation = jibenyvnsuan[token]
            stack.append(operation(op1, op2))
        elif token in ZIDIANYINGSHE:
            if token in ['max', 'min']:
                args = []

                while stack:
                    arg = stack.pop()
                    if arg == '(':
                        break
                    args.append(arg)
                if len(args) < 2:
                    raise ValueError(f"Not enough arguments available for '{token}'")
                result = ZIDIANYINGSHE[token](*args)
            else:
                if len(stack) < 1:
                    raise ValueError(f"Not enough arguments available for '{token}'")
                arg = stack.pop()
                result = ZIDIANYINGSHE[token](arg)
            stack.append(result)

        elif token.lstrip('-').replace('.', '', 1).isdigit():
            # 如果令牌表示数字（整数或浮点数），将其转换为
            # float
            # 类型并压入栈中
            stack.append(float(token))
        elif token in variable_values:
            stack.append(float(variable_values[token]))
        else:
            raise ValueError(f"Unexpected token: {token}")
    if len(stack) != 1:
        # 如果遇到无法识别的令牌（不是操作符、数字、函数或变量的令牌），将抛出一个 ValueError 异常。
        raise ValueError("The stack did not end with a single result, indicating an error in expression.")
    return stack.pop()


# 假设已有后缀表达式为 ['-4.5', 'abs']
postfix_expression = ['-4.5', 'abs']

# 计算后缀表达式
result = evaluate_postfix(postfix_expression)
print("Result:", result)

