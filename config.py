"""
Global configuration required to make things pretty when possible
"""
ascii_art = False
colors = False
colored = lambda x, y, attrs=None: x

def set_colors():
        global colors
        global colored
        
        try:
                import termcolor
                colored = termcolor.colored

                import colorama
                colorama.init()
                colors = True
            
        except ModuleNotFoundError:
                colors = False



def set_ascii_art():
        global ascii_art
        
        try:
            import pyfiglet
            ascii_art = True
        except ModuleNotFoundError:
            ascii_art = False

set_colors()
set_ascii_art()