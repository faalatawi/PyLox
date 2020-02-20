# Copyright (c) 2020 Faisal Alatawi. All rights reserved
# Using this source code is governed by an MIT license
# you can find it in the LICENSE file.


def test_interpreter():
    from lox import interpreter
    from lox.token_type import TokenType
    # interpreter.Interpreter()

    raise interpreter.RuntimeError(TokenType.MINUS, "this is test")



if __name__ == "__main__":
    test_interpreter()




