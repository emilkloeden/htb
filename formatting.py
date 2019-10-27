ascii_art = False
colors = False
colored = lambda x, y, attrs=None: x

def init():
        __set_ascii_art()
        __set_colors()

def __set_colors():
        global colors
        global colored
        
        try:
                from termcolor import colored
                import colorama
                colorama.init()
                colors = True
        except ModuleNotFoundError:
                colors = False

def __set_ascii_art():
        global ascii_art
        
        try:
            import pyfiglet
            ascii_art = True
        except ModuleNotFoundError:
            ascii_art = False

def sentence_case(string: str) -> str:
        """
        Return a string with its first character in Uppercase and the rest in lowercase
        """
        if len(string) > 1:
                return f"{string[0].upper()}{string[1:].lower()}"
        elif len(string) == 1:
                return string[0].upper()
        return ""


def green(string: str) -> str:
        return string if not colors else colored(string, 'green')

def bold_green(string: str) -> str:
        return string if not colors else colored(string, 'green', attrs=['bold'])

def yellow(string: str) -> str:
        return string if not colors else colored(string, 'yellow')

def red(string: str) -> str:
        return string if not colors else colored(string, 'red')