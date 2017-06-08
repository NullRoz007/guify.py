from tkinter import *
import tkinter.messagebox

class GenericGui:
    def __init__(self, name, arg_count, arg_names, functions, backend):
        self.name = name
        self.arg_count = arg_count
        self.arg_names = arg_names
        self.functions = functions
        self.tk = Tk()
        self.tk.title(self.name)
        self.tk.geometry("300x200+200+200")        
        self.labels = []
        self.backend = backend
        l = Label(self.tk, text="Class Constructor: ")
        for i in arg_names:
            l = Label(self.tk, text="%"+i+"%")
            self.labels.append(l)
            l.pack()
    def f_where(self, name):
        for f in self.functions:
            if f['name'] == name: return f
            
    def Run(self, args):
        constructor = self.f_where("__init__")
        arg_count = constructor['arg_count']
        backend = self.backend
        
        #Fill constructor arguments:
        n = 0
        for a in args:
            self.labels[n].config(text = a+": "+args[a])
            self.labels[n].pack()
            n += 1          
        i = 1
        for f in self.functions:
            if(f['name'] != '__init__'):
                fL_x = 0
                fL_y = 2

                f_l = Label(self.tk, text = f['name'])
            f_l.pack(side="top")
            
                      
        self.tk.mainloop()
        
class ClassRep:
    def __init__(self, name, arg_count, arg_names, functions, backend):
        self.name = name
        self.arg_count = arg_count
        self.arg_names = arg_names
        self.functions = functions
        name = self.name.split('.')[1]
        self.Interface = GenericGui(name, self.arg_count, self.arg_names, self.functions, backend)
        
        
def func_added(f_list, name):
    for f in f_list:
        if(f['name'] == name):
            return True
    return False

def _get_name(o):
    if "'" in str(o):
        return str(o).split("'")[1]
    else: return str(o)
    
def guify(o):
    dict  = o.__dict__
    name = _get_name(o)
    c_arg_count = 0
    c_arg_names = []
    functions = []

    for m in dict:
        output = ""
        arg_count = 0
        arg_names = []        
        if(callable(getattr(o, str(m)))):
            f = getattr(o, m)
            output = m
            output += ": Function"
            if(m == "__init__"):
                output += " - Class Constructor"
                c_arg_count = f.__code__.co_argcount
                c_arg_names = f.__code__.co_varnames
                
            output += " - ("
            
            arg_count = f.__code__.co_argcount
            arg_names = f.__code__.co_varnames
            
            if(not func_added(functions, m)): functions.append({'name': m, 'arg_names':arg_names, 'arg_count':arg_count})  
            
            i = 0
            for arg in arg_names:
                output += arg
                if(i < arg_count - 1):
                    output += ", "
                i+= 1
            output += ")"
            
        elif(m != "__weakref__" and m != "__module__" and m != "__doc__" and m != "__dict__"):
            output = m
        
    cr = ClassRep(name, c_arg_count, c_arg_names, functions, o)
    return cr

class Example:
    def __init__(self, test):
        self.test = test
    def function_example(self, a, b):
        print(test)
        
cr = guify(Example)
cr.Interface.Run({"self": "Class Contructor", "test": "8=D"})
