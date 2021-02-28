# Copyright (c) 2021 Faisal Alatawi. All rights reserved
# Using this source code is governed by an MIT license
# you can find it in the LICENSE file.

from textwrap import dedent
from typing import List, Tuple


def define_type(class_name: str, base_name: str, args: List[Tuple[str, str]]) -> str:
    constructor_args = ""
    for arg_name, arg_type in args:
        constructor_args += arg_name + " : " + arg_type + ", "
    constructor_args = constructor_args[:-2]

    out = "\n" + f"class {class_name}({base_name}):" + "\n"
    out += "\t" + f"def __init__(self, {constructor_args}):" + "\n"

    for arg_name, arg_type in args:
        out += "\t\t" + f"self.{arg_name} : {arg_type} = {arg_name} \n"

    out += "\n"

    out += "\t" + "def accept(self, visitor : VisitorInterface):" + "\n"
    out += "\t\t" + f"return visitor.visit{class_name}(self)" + "\n"

    return out


def define_AST(output_file, base_name: str,  grammer):
    base = f"""\
            # Copyright (c) 2021 Faisal Alatawi. All rights reserved
            # Using this source code is governed by an MIT license
            # you can find it in the LICENSE file.

            from typing import Union
            from lox.ast.token import Token 

            class Expr(object):
                def accept(self, visitor):
                    pass
            

            """
    base = dedent(base)
    output_file.write(base)

    # Visitor interface
    output_file.write("class VisitorInterface(object):" + "\n")
    for k in grammer.keys():
        output_file.write("\t" + f"def visit{k}(self, expr):" + "\n")
        output_file.write("\t\t" + "pass" + "\n")

    # Classes
    for class_name, args in grammer.items():
        output_file.write(define_type(class_name, base_name, args))

    output_file.close()


if __name__ == "__main__":
    path = "lox/ast/grammer.py"

    grammer = {
        "Binary": [("left", "Expr"), ("operator", "Token"), ("right", "Expr")],
        "Grouping": [("expression", "Expr")],
        "Literal": [("value", "Union[float, str]")],
        "Unary": [("operator", "Token"), ("right", "Expr")]
    }
    base_name = "Expr"

    with open(path, "w+") as output_file:
        define_AST(output_file, base_name, grammer)
