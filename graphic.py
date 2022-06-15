import re, curses

PYTHON_TABLE = {'30': ["COMMENT"], '34': ['(', ')', "{", "}"], '32': ["FUNCTIONS"], '35': ["while ", " in ", " is ", "try", "except", "pass", "=", "+", "-", "/", "*", "**", 'import ', 'class ', ' as ', 'for ', 'if ', 'elif ', 'else', 'from ', 'def ', 'with ', 'return '], "33": ["STR"]}
JSON_TABLE = {"34": ["[", "]", "{", "}"], "35": [":"], "33": ["STR"]}

def color_text(text, color, style):
    modificator = ""
    if style == "5": #for color 256
        modificator = "38;"
    return f"\033[{modificator}{style};{color}m{text}\033[0;0m"

def background(text, color, colors_256=False):
    modificator = ""
    if colors_256:
        modificator = "48;"
    return f"\033[{modificator}{color}m{text}\033[0;0m"

def highlightSyntax(text, table, show_lines = True):
    """This is function return render of text. 
            Argument "table" takes a dictinary in 
            which the keys are the number of the color, and the values
            are the list of word what be painted with this color"""
    result = text
    for color in table:
        for word in table[color]:
            if word == "STR": #all strings in text
                strings = re.findall("\"(.*?)\"", text)
                strings2 = re.findall("\'(.*?)\'", text)
                for string in strings:
                    result = result.replace(f'"{string}"', color_text(f'"{string}"', color, '1'))
                for string in strings2:
                    result = result.replace(f"'{string}'", color_text(f"'{string}'", color, '1'))
            elif word == "COMMENT": #all comments in text
                comments = []
                for line in text.split('\n'):
                    if '#' in line:
                        comments.append(line.rpartition('#')[2])
                for comment in comments:
                    result = result.replace(f'#{comment}', color_text(f'#{comment}', color, '1'))
            elif word == "FUNCTIONS": #all functions in text
                functions = re.findall('\s(.*?)\(', text)
                for func in functions:
                    functions[functions.index(func)] = func.rpartition(' ')[2].rpartition('.')[2]
                for func in functions:
                    result = result.replace(func, color_text(func, color, '1'))
            else:
                result = result.replace(word, color_text(word, color, '1'))
    if show_lines:
        line_num = 1
        len_text = str(len(result.split('\n')))
        out_text = []
        for line in result.split('\n'):
            spaces = ' '*(len(len_text) - len(str(line_num)))
            out_text.append(color_text(spaces+str(line_num), '30', '1')+ ' '+ line)
            line_num += 1
        return '\n'.join(out_text)
    else:
        return result
                      
#methods menu and checker_menu are test    
def menu(title, classes, color='white'):
    # define the curses wrapper
    def character(stdscr,):
        attributes = {}
        # stuff i copied from the internet that i'll put in the right format later
        icol = {
            1:'red',
            2:'green',
            3:'yellow',
            4:'blue',
            5:'magenta',
            6:'cyan',
            7:'white'
        }
        # put the stuff in the right format
        col = {v: k for k, v in icol.items()}

        # declare the background color

        bc = curses.COLOR_BLACK

        # make the 'normal' format
        curses.init_pair(1, 7, bc)
        attributes['normal'] = curses.color_pair(1)


        # make the 'highlighted' format
        curses.init_pair(2, col[color], bc)
        attributes['highlighted'] = curses.color_pair(2)


        # handle the menu
        c = 0
        option = 0
        while c != 10:

            stdscr.erase() # clear the screen (you can erase this if you want)

            # add the title
            stdscr.addstr(f"{title}\n", curses.color_pair(1))

            # add the options
            for i in range(len(classes)):
                # handle the colors
                if i == option:
                    attr = attributes['highlighted']
                else:
                    attr = attributes['normal']
                
                # actually add the options

                stdscr.addstr(f"", attr)
                stdscr.addstr(f'{classes[i]}' + '\n', attr)
            c = stdscr.getch()

            # handle the arrow keys
            if c == curses.KEY_UP:
                if option == 0:
                    option = len(classes)-1
                else:
                    option -= 1
            elif c == curses.KEY_DOWN:
                if option == len(classes)-1:
                    option = 0
                else:
                    option += 1
        return option
    return curses.wrapper(character)
  
def checker_menu(title, classes, color='white'):
    unchecked = "□"
    checked = "▣"
    checkers = [False]*len(classes)
    # define the curses wrapper
    def character(stdscr,):
        attributes = {}
        # stuff i copied from the internet that i'll put in the right format later
        icol = {
            1:'red',
            2:'green',
            3:'yellow',
            4:'blue',
            5:'magenta',
            6:'cyan',
            7:'white'
        }
        # put the stuff in the right format
        col = {v: k for k, v in icol.items()}

        # declare the background color

        bc = curses.COLOR_BLACK

        # make the 'normal' format
        curses.init_pair(1, 7, bc)
        attributes['normal'] = curses.color_pair(1)


        # make the 'highlighted' format
        curses.init_pair(2, col[color], bc)
        attributes['highlighted'] = curses.color_pair(2)


        # handle the menu
        c = 0
        option = 0
        while True:
            stdscr.erase() # clear the screen (you can erase this if you want)

            # add the title
            stdscr.addstr(f"{title}\n", curses.color_pair(1))

            # add the options
            for i in range(len(classes)):
                # handle the colors
                if i == option:
                    attr = attributes['highlighted']
                else:
                    attr = attributes['normal']
                
                # actually add the options
                opt = classes[i]
                if checkers[i]:
                    opt = checked + " "+opt
                else:
                    opt = unchecked+" "+opt

                stdscr.addstr(f'{opt}' + '\n', attr)
            c = stdscr.getch()

            # handle the arrow keys

            if c == curses.KEY_UP:
                if option == 0:
                    option = len(classes)-1
                else:
                    option -= 1
            elif c == curses.KEY_DOWN:
                if option == len(classes)-1:
                    option = 0
                else:
                    option += 1
            if c == 10:
                if checkers[option]:
                    checkers[option] = False
                else:
                    checkers[option] = True
            if c == 113:
                break
        return checkers
    return curses.wrapper(character)

def renderError(name_error, description, level="1"):
    """Method for render of errors."""
    if level == "0": #not critical error
        color = "33"
    else: #critical error
        color = "31"
    out = []
    if len(description)  > len(name_error):
        lenght_error = len(description)+6
    else:
        lenght_error = len(name_error)+6
    lenght = lenght_error+2
    minuses = int((lenght_error-len(name_error))/2)
    out.append('-'*minuses+f' {name_error} ' + '-'*minuses)
    out.append(description.center(lenght))
    out.append('-'*(lenght))
    for i in out:
        print(color_text(i, color, '1'))