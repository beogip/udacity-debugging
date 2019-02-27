#!/usr/bin/env python
# Simple Daikon-style invariant checker
# Andreas Zeller, May 2012
# Complete the provided code around lines 28 and 44
# Do not modify the __repr__ functions.
# Modify only the classes Range and Invariants,
# if you need additional functions, make sure
# they are inside the classes.

import sys
import math
import random

def square_root(x, eps = 0.00001):
    assert x >= 0
    y = math.sqrt(x)
    assert abs(square(y) - x) <= eps
    return y
    
def square(x):
    return x * x

# The Range class tracks the types and value ranges for a single variable.
class Range:
    def __init__(self):
        self.min  = None  # Minimum value seen
        self.max  = None  # Maximum value seen
    
    # Invoke this for every value
    def track(self, value):
        if self.min == None and self.max == None:
            self.min = self.max = value
        if self.min > value:
            self.min = value
        elif self.max < value:
            self.max = value
        assert self.min <= self.max
            
    def __repr__(self):
        return repr(self.min) + ".." + repr(self.max)


# The Invariants class tracks all Ranges for all variables seen.
class Invariants:
    def __init__(self):
        # Mapping (Function Name) -> (Event type) -> (Variable Name)
        # e.g. self.vars["sqrt"]["call"]["x"] = Range()
        # holds the range for the argument x when calling sqrt(x)
        self.vars = {}
    
    def track_range(self, vars, key, value):
        if(not key in vars):
            vars[key] = Range()
        vars[key].track(value)
        assert key in vars

    def init_name(self, vars, name):
        assert name != None
        if(not name in vars):
            vars[name] = {}
        assert name in vars
        

    def init_event(self, vars, event):
        assert event != None
        if(not event in vars):
            vars[event] = {}
        assert event in vars

    def track(self, frame, event, arg):
        self.init_name(self.vars, frame.f_code.co_name)
        if event == "call" or event == "return":
            # YOUR CODE HERE. 
            # MAKE SURE TO TRACK ALL VARIABLES AND THEIR VALUES
            # If the event is "return", the return value
            # is kept in the 'arg' argument to this function.
            # Use it to keep track of variable "ret" (return)
            self.init_event(self.vars[frame.f_code.co_name],event)
            if(event == 'return'):
                self.track_range(self.vars[frame.f_code.co_name][event], 'ret', arg)
                return
            for key,value in frame.f_locals.items():
                self.track_range(self.vars[frame.f_code.co_name][event], key, value)
        elif event == 'line':
            self.init_event(self.vars[frame.f_code.co_name], 'return')
            for key,value in frame.f_locals.items():
                self.track_range(self.vars[frame.f_code.co_name]['return'], key, value)
    
    def __repr__(self):
        # Return the tracked invariants
        s = ""
        for function, events in self.vars.items():
            for event, vars in events.items():
                s += event + " " + function + ":\n"
                # continue
                
                for var, range in vars.items():
                    s += "    assert "
                    if range.min == range.max:
                        s += var + " == " + repr(range.min)
                    else:
                        s += repr(range.min) + " <= " + var + " <= " + repr(range.max)
                    s += "\n"
                
        return s

invariants = Invariants()
    
def traceit(frame, event, arg):
    invariants.track(frame, event, arg)
    return traceit

sys.settrace(traceit)
# Tester. Increase the range for more precise results when running locally
eps = 0.000001
for i in range(1, 10):
    r = int(random.random() * 1000) # An integer value between 0 and 999.99
    z = square_root(r, eps)
    z = square(z)
sys.settrace(None)
print(invariants)


