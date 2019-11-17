"""
Formatting helper functions
"""

from config import ascii_art, colors, colored


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