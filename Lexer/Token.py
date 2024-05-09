import re

class Token:
    """
    Basic token class.

    Parameters
    ----------
    lex : str
        Token's lexeme.
    token_type : Enum
        Token's type.
    """
    
    def __init__(self, lex: str, token_type, line: int, column: int):
        self.lex = lex
        self.token_type = token_type
        self.line = line
        self.column = column

    def __str__(self):
        return f'{self.token_type}: {self.lex}'

    def __repr__(self):
        return str(self)
 
class TokenPattern:
    """
    Token pattern class.

    Parameters
    ----------
    pattern : str
        Token's pattern.
    follow : str
        Token's follow pattern.
    token_type : Enum
        Token's type.
    """
 
    def __init__(self, token_type, pattern: str, follow = None):
        self.token_type = token_type
        self.pattern = re.compile(pattern) 
        self.follow = re.compile(follow) if follow else None
      
    def __str__(self):
        return f'{self.token_type}: {self.pattern}'

    def __repr__(self):
        return str(self)
