# Copyright (c) 2020 Faisal Alatawi. All rights reserved
# Using this source code is governed by an MIT license
# you can find it in the LICENSE file.

import sys
from lox.token_type import TokenType
from termcolor import colored
from lox.scanner import Scanner
from lox.parser import Parser
from lox.ast_printer import ASTPrinter


# Global verabiles
# ++++++++++++++++++++++
HAD_ERROR = True
# ++++++++++++++++++++++


def run(source):
    scan = Scanner(source)
    tokens = scan.scanTokens()

    # for token in tokens:
    #     print(token)
    
    pars = Parser(tokens)
    result = pars.parse()

    print(ASTPrinter().print(result))


def runFile(path):
    f = open(path, "r")
    source = f.read()

    run(source)

    if HAD_ERROR:
        exit(65)


def runPrompt():
    while True:
        user_input = input("> ")
        run(user_input)


if __name__ == "__main__":
    arg_length = len(sys.argv)
    if arg_length > 3:
        print("Usage: PyLox [script]")
        exit(2)
    elif arg_length == 3:
        path = sys.argv[2]
        runFile(path)
    else:
        runPrompt()
