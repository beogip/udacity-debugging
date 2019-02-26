import sys

def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s: 
        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif (c == '"' or c == "'") and tag:
            quote = not quote
        elif not tag:
            out = out + c
    return out

stepping = False
breakpoints = {9: True, 14: True}
watchpoints = {'c': True}

def debug(command, arg, locals):
    global stepping
    global breakpoints
    if command.find(' ') > 0:
        arg = command.split(' ')[1]
    else:
        arg = None

    if command.startswith('s'): # step
        stepping = True
        return True
    elif command.startswith('c'): # continue
        stepping = False
        return True
    elif command.startswith('p'):  # print 
        if(arg in locals):
            print(arg,'=',locals[arg])
        elif(not arg):
            print(locals)
        else:
            print("No such variable: ", arg)
        return False
    elif command.startswith('b'):    # breakpoint     
        if(not arg):
            print("You must supply a line number")
        breakpoints[int(arg)] = True
        return False
    elif command.startswith('w'):    # watch variable
        if(not arg):
            print("You must supply a variable name")
            return False
        watchpoints[arg] = True
        return False
    elif command.startswith('q'):
        sys.exit(0)
    else:
        print("No such command", repr(command))

def input_command():
    return input(" (my-spider) ")

def traceit(frame, event, arg):
    global stepping
    global breakpoints
    if event == 'line':
        if stepping or frame.f_lineno in breakpoints:
            resume = False
            while not resume:
                print(event, frame.f_lineno, frame.f_code.co_name, frame.f_locals)
                command = input_command()
                resume = debug(command, arg, frame.f_locals)
    return traceit

sys.settrace(traceit)
print(remove_html_markup('xyz'))
sys.settrace(None)