"""
Faisal Alatawi
Feb, 2020

"""
import sys
from termcolor import colored
from Scanner import lox_scanner

# Global verabiles
# ++++++++++++++++++++++
HAD_ERROR = True
# ++++++++++++++++++++++


def report(line, where, message):
    out = "[line " + line + "] Error" + where + ": " + message
    print(colored(out, 'red'))


def lox_error(line, message):
    report(line, "", message)


def run(source):
    scanner = lox_scanner(source)
    tokens = scanner.scanTokens()

    for token in tokens:
        print(token)


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
