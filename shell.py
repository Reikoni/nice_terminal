from os import nice
import sys
import nice_core

def Shell(params: list):
    command = nice_core.getCommand(params[0])
    if len(command) == 4:
        if command[2]: #if command is accessed
            if command[0] != "": #if path not empty append path to sys.path
                sys.path.append(command[0])
            exec(f'from {command[1].replace(".py", "")} import *') #import all from file
            arguments = ", ".join(params[1]) #arguments for python function
            output = str(f'{eval(f"{command[3]}({arguments})")}') #get output command
            if output != "None":
                if params[2] == "": #if not out object
                    print(output)
                else:
                    if params[2] in nice_core.varses or len(params[2].split()) == 1:
                        nice_core.workVar(params[2], output)
                    else:
                        answer = params[2].partition('|~|')[0].strip().replace('[~]', output)  + ' |~| ' + params[2].partition('|~|')[2]
                        Shell(nice_core.getLine(answer))
    else:
        nice_core.graphic.renderError('NotFoundCommand', f'Command "{params[0]}" not found!')