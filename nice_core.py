#import libs
import json
import re
import hashlib
import os
import graphic
 
with open("setting.json", "r") as file: #open file with commands
        settings = json.load(file)
with open('locked_files.acmd', 'r') as l_file:
    locked_files = l_file.read().split('\n')
preffix = settings['preffix'] #preffix for arguments
id_currect_user = settings['default_user']
root = False
pwd = os.getcwd()

size = re.findall('\d+', str(os.get_terminal_size())) #size of terminal

varses = {} #dictinary for varses
panels = {}

def printDir():
    """This is method print a current dir"""
    return os.getcwd()

def changeDir(path):
    """"This is method change a dir"""
    p = os.getcwd()
    os.chdir(path)
    if os.getcwd() in locked_files:
        os.chdir(p)
        return graphic.renderError("🔒 PathError: PathLocked", f'"{path}" is locked! You can\'t move to this path!')
    
def listFiles(path="", hide_files=False):
    """"This is method print list files and catalogs in path"""
    if str(hide_files).lower() == "false":
        hide_files = False
    else:
        hide_files = True
    if path.strip() == "":
        path = os.getcwd()
    else:
        if os.path.exists(path):
            path = pwd+'/'+path
    if path not in locked_files:
        out = []
        lf = os.listdir(path)
        pd = printDir()
        os.chdir(path)
        files = [file for file in lf if os.path.isfile(file)]
        for catalog in lf:
            if os.path.isdir(catalog):
                if catalog.startswith('.'):
                    if hide_files:
                        out.append("📁 "+graphic.color_text(catalog, '30', '1'))
                else:
                    out.append("📁 "+graphic.color_text(catalog, '35', '1'))
        for file in files:
            if file.endswith(".py"): #if file of python
                out.append("🐍 "+ graphic.color_text(file, '34', '1'))
            elif file.endswith('.json'): #if file of json
                out.append("📄 "+ graphic.color_text(file, '33', '1'))
            elif file.startswith('.'):
                if hide_files:
                    out.append("📄 "+ graphic.color_text(file, '30', '1'))
            else:
                out.append("📄 "+ file)
        os.chdir(pd)
        return "\n".join(out)
    else:
        return graphic.renderError("🔒 PathError: PathLocked", f'"{path}" is locked! You can\'t list filed in this path!')
    
def readFile(file, show_lines=True):
    """"This is method read of files with highligth syntax"""
    path_my = os.getcwd()
    if '/' in file:
        path_to = file.rpartition('/')[0]
        changeDir(path_to)
        file = os.getcwd()+'/'+file.rpartition('/')[2]
        changeDir(path_my)
    if file not in locked_files:
        with open(file, 'r') as f:
            text = f.read()
        table = ""
        if file.endswith('.py'):
            table = graphic.PYTHON_TABLE
        if file.endswith('.json'):
            table = graphic.JSON_TABLE
        return graphic.highlightSyntax(text, table, show_lines)
    else:
        return graphic.renderError("🔒 PathError: FileLocked", f'"{file}" is locked! You can\'t work with this file!')
        
def newFile(file):
    """"This is method create a new file"""
    if not os.path.exists(file):
        f = open(file, 'w')
        f.close()
    else:
        return graphic.renderError("FileExists", f'"{file}" is exist!')
        
def workVar(name, value):#var <name> <0>
    name = name.strip().replace(' ', '')
    varses[name] = value

def Initialize(file):
    with open(file, "r") as file_info:
        data_init = json.load(file_info)
    if data_init["type"] == "panel":
        for file_ in data_init["files"]:
            if data_init["name"] not in panels:
                panels[data_init["name"]] = {}
            panels[data_init["name"]][file_] = pwd+'/'+data_init["files"][file_]
              
def get_info_user(id_user):
    with open(pwd+'/users.json', 'r') as user_file:
        user_data = json.load(user_file)
    if id_user in user_data:
        data = user_data[id_user]["info"].split(':')
        rules = []
        for i in data[0]:
            rules.append(i.lower() == "t")
        return [data[1], data[2], rules, data[3]]

def getPanel(id_):
    pack_name = id_.partition(':')[0]
    id_panel = id_.partition(':')[2]
    with open(panels[pack_name][id_panel], 'r') as panel_file:
        data_panel = json.load(panel_file)
    structure = data_panel["structure"]
    widgets = data_panel["widgets"]
    for widget in widgets:
        text = widgets[widget]['text']
        color = widgets[widget]['color']
        style = widgets[widget]['style']
        if text == "$ROOT$":
            text2 = widgets[widget]['text2']
            text = graphic.color_text(text2[0 if root else 1], color[0 if root else 1], style)
        elif text == "$NAME-USER$":
            text = graphic.color_text(get_info_user(id_currect_user)[0], color, style)
        else:
            text = graphic.color_text(text, color, style)
        structure = structure.replace(f'${widget}$', text)
    return structure

def workUser(action, id_user="", edit_info=""):
    if action == "get-info":
        info = get_info_user(id_user)
        out = graphic.color_text('ID: ', '33', '1')+id_user+'\n'+graphic.color_text('Login: ', '33', '1')+info[0]+'\n'+graphic.color_text('Password: ', '33', '1')
        if root:
            out += info[1]
        else:
            out += '🔒'
        print(out)
    elif action == "change":
        global id_currect_user
        id_currect_user = id 
    elif action == "create":
        with open('users.json', 'r') as file:
            data =json.load(file)
        new_id = str(int(list(data)[-1])+1) #
        count_zero = 3-len(new_id)
        new_id = "0"*count_zero+new_id
        pass_info = "ff:0:0:"
        data[new_id] = {"info": pass_info+id_currect_user, "files": []}
        with open('users.json', 'w') as write_file:
            json.dump(data, write_file, indent=4)
    elif action == "edit":
        if get_info_user(id_user)[3] == id_currect_user:
            split_info = edit_info.split()
            split_info[2] = hashlib.sha1(bytes(split_info[2].strip().replace(' ', ''), encoding="utf-8")).hexdigest()
            with open('users.json', 'r') as file:
                data =json.load(file)
            data[id_user]['info'] = ":".join(split_info)+':'+data[id_user]['info'].rpartition(':')[2]
            with open('users.json', 'w') as write_file:
                json.dump(data, write_file, indent=4)
        
def auth():
    global root
    line = input(f'Entry password from user [{get_info_user(id_currect_user)[0]}] ').strip().replace(' ', '')
    pw = hashlib.sha1(bytes(line, encoding="utf-8")).hexdigest()
    if pw == get_info_user(id_currect_user)[1]:
        root = True
    else:
        root = False

def getLine(line):
    if '%' in line:
        system_vars = re.findall(r"%(.*?)%", line)
        for var in system_vars:
            outs = str(f'{eval(f"{var}")}')
            line = line.replace(f'%{var}%', outs)
    if '$' in line:
        system_vars = re.findall(r"\$(.*?)\$", line)
        for var in system_vars:
            outs = varses[var]
            line = line.replace(f'${var}$', outs)
    command = line.split()[0] #get command from line
    out_object = line.partition("|~|")[2].strip() if '|~|' in line else "" #get out object from line
    atributes = re.findall(r"\<(.*?)\>", line.partition('|~|')[0]) #get atributes from line
    for atribute in atributes.copy():
        atributes[atributes.index(atribute)] = atribute.replace('/*', "<").replace('*/', ">") #replace /* and */ from atributes
    for atribute in atributes:
        atribute = str(atribute)
        if atribute.startswith('[') and atribute.endswith(']'):
            atributes[atributes.index(atribute)] = f"{[el.strip() for el in atribute[1:-2].split(';')]}"
        else:
            atributes[atributes.index(atribute)] = f'"{atribute}"'
    with open(pwd+"/commands.json", "r") as file: #open file with commands
        data = json.load(file)
    for atr in atributes.copy():
        atr =str(atr)
        if atr[1:-1].startswith(preffix) and ':' in atr:
            argument = atr[1:-1].partition(':')[0]
            value_argument = atr[1:-1].partition(':')[2].strip()
            argument_without_preffix = argument.replace(preffix, '')
            for arg in data[command]["args"]:
                if argument_without_preffix == arg or argument_without_preffix in data[command]["args"][arg]:
                    atributes[atributes.index(atr)] = arg+'='+f'"{value_argument}"'
    return [command, atributes, out_object] #return list from three elements

def getCommand(command: str) -> list:
    with open(pwd+"/commands.json", "r") as file: #open file with commands
        data_command = json.load(file)
    if command in data_command:
        function = data_command[command]["function"]
        function_in_code = data_command[command]["function"].partition('>')[2].strip() #function that will execute
        if ">" in function:
            if "/" in function:
                path_to_file = function.rpartition("/")[0].strip()+"/" #find path to file
            else:
                path_to_file = ""
            file = function.rpartition("/")[2].partition('>')[0].strip() #file
            return [path_to_file, file, data_command[command]["access"], function_in_code] 
    else:
        return [""]