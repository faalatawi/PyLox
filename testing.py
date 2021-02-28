# Copyright (c) 2020 Faisal Alatawi. All rights reserved
# Using this source code is governed by an MIT license
# you can find it in the LICENSE file.


def test_interpreter():
    from lox.scanner import Scanner
    from lox.parser import Parser
    from lox.ast.ast_printer import ASTPrinter
    from lox.interpreter import Interpreter

    source = """ 1 + 999 """

    lox_scan = Scanner(source)

    tokens = lox_scan.scanTokens()

    print("Tokens:")
    for tok in tokens:
        print(tok)
    print("\n")

    lox_parser = Parser(tokens)
    result = lox_parser.parse()

    printer = ASTPrinter()

    print(printer.print(result))

    print(Interpreter().evaluate(result))


def test_parser():
    from lox.scanner import Scanner
    from lox.parser import Parser
    from lox.ast.ast_printer import ASTPrinter

    source = " 1 + 2 >= 133 + \" gggg \""

    lox_scan = Scanner(source)

    tokens = lox_scan.scanTokens()

    print("Tokens:")
    for tok in tokens:
        print(tok)
    print("\n")

    lox_parser = Parser(tokens)
    result = lox_parser.parse()

    printer = ASTPrinter()

    print(printer.print(result))


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


def test_ASTPrinter():
    from lox.ast.token import TokenType, Token
    from lox.ast.ast_printer import ASTPrinter
    from lox.ast.grammer import Binary, Unary, Grouping, Literal

    expression = Binary(
        left=Unary(
            operator=Token(TokenType.MINUS, "-", None, 1),
            right=Literal(123)
        ),
        operator=Token(TokenType.STAR, "*", None, 1),
        right=Grouping(
            expression=Literal(45.67)
        )

    )

    print(ASTPrinter().print(expression))


if __name__ == "__main__":
    test_interpreter()
