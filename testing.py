# Copyright (c) 2020 Faisal Alatawi. All rights reserved
# Using this source code is governed by an MIT license
# you can find it in the LICENSE file.


def test_interpreter():
    from lox import interpreter
    from lox.token_type import TokenType
    # interpreter.Interpreter()

    raise interpreter.RuntimeError(TokenType.MINUS, "this is test")


def test_scanner():
    from lox.scanner import Scanner

    lox_scanner = Scanner("""
        var x = 12.1
        if else 
        for 
        // kdjkdkkd
        /
        {}
        ()
        print 
        "fias'' // "

        class
        @ 
        " student 
        
        // this is a comment
        (( )){} // grouping stuff
        !*+-/=<> <= == // operators
    """)

    token_list = lox_scanner.scanTokens()

    for tok in token_list:
        print(tok)


if __name__ == "__main__":
    test_scanner()
