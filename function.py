# # function.py


import math
from function_base import FunctionBase
# class FunctionBase:
#     def evaluate(self, *args):
#         raise NotImplementedError("Subclasses should implement this method")

class SinFunction(FunctionBase):
    def evaluate(self, arg):
        return math.sin(arg)

class CosFunction(FunctionBase):
    def evaluate(self, arg):
        return math.cos(arg)

class TanFunction(FunctionBase):
    def evaluate(self, arg):
        return math.tan(arg)

class SqrtFunction(FunctionBase):
    def evaluate(self, arg):
        return math.sqrt(arg)

class AbsFunction(FunctionBase):
    def evaluate(self, arg):
        return abs(arg)

class MaxFunction(FunctionBase):
    def evaluate(self, *args):
        return max(args)

class MinFunction(FunctionBase):
    def evaluate(self, *args):
        return min(args)
