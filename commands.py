from os import system
import math
import re

def write(message):
    return message

def readLine(line):
    ln = input(line)
    return ln

def math_exec(line):
    line = line.replace('^', '**').replace('pi', str(math.pi))
    factorial = re.findall("\d*!", line)
    for fact in factorial:
        line = line.replace(fact, str(math.factorial(int(fact[:-1]))))
    sinus = re.findall("sin\(\d*\)", line)
    for sin in sinus:
        line = line.replace(sin, str(math.sin(int(sin[4:-1]))))
    cosinus = re.findall("cos\(\d*\)", line)
    for cos in cosinus:
        line = line.replace(cos, str(math.cos(int(cos[4:-1]))))
    return eval(line)

def clear():
    system('clear')