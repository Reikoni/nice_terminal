import nice_core
from shell import *
import graphic, json, os

size = nice_core.size

activity_programm = [] #name, titile, errors, file
manager = ['', '', ''] #input_text, tips, ask
end = False

def endProgramm():
    global end
    end = True

def askManager(ask):
    manager[2] = ask 
    
def getValueManager():
    return manager[0]

def ManagerProgramm():
    if manager[2].strip() != "":
        line = input(f'[{manager[2]}] > ')
        if line == ":q":
            endProgramm()
            manager[0] = ''
        else:
            manager[0] = line
        manager[2] = ''
          
def LanguageParser(file_name):
    if file_name.endswith('.ncmd'):
        with open(file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith('#'):
                    continue
                else:
                    Shell(nice_core.getLine(line))
                
def programmTitle():
    name = activity_programm[0]
    title = activity_programm[1]
    spaces = int((int(size[0])-len(name)-len(title))/2)
    color = str(42 if len(activity_programm[2]) == 0 else 41)
    print(graphic.background('  '+name+' '*(spaces-2)+title+' '*spaces, color))
    
def editProgramm(what, value):
    global activity_programm
    if what == 'title':
        activity_programm[1] = value
    elif what == 'error-add':
        activity_programm[2].append(value)
    elif what == 'error-del':
        activity_programm[2].remove(value)
        
def killProgramm(): #kill programm
    global activity_programm
    activity_programm = []

def execProgramm(manifest_file): #execute a programm
    global activity_programm, end
    with open(manifest_file, "r") as file_info:
        data = json.load(file_info)
    name = data['name']
    if data['type'] == "programm":
        activity_programm = [name, '', [], data['file']]
    if activity_programm[3].endswith('.ncmd'):
        with open(activity_programm[3], 'r') as file:
            lines = file.readlines()
    while end != True:
        os.system('clear')
        programmTitle()
        for line in lines:
            if name in activity_programm:
                if line.startswith('#'):
                    continue
                else:
                    Shell(nice_core.getLine(line))
                ManagerProgramm()
    end = False
    #os.system('clear')
            
            
            
def run(command=""): #main method
    LanguageParser('autoload.ncmd')
    while True:
        if command.strip() != "":
            prompt = command
        else:
            prompt = input(nice_core.getPanel('Default:prompt'))
        if "|||" in prompt:
            for pr in prompt.split('|||'):
                Shell(nice_core.getLine(pr))
        else:
            Shell(nice_core.getLine(prompt))
        if command.strip() != "":
            break
        
def if_block(condition, code, else_=""): #command "if"
    if eval(condition):
        run(code)
    else:
        if else_ != "":
            run(else_)
        
run()