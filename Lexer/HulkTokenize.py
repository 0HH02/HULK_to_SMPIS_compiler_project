from enum import Enum
from Lexer.Token import TokenPattern
from Lexer.Lexer import lexer
import json

def hulk_tokenize(text):
    
    with open("Lexer/HulkTokenList.json", "r", encoding="utf-8") as file:
        patterns = json.load(file)

    TokenType = Enum('TokenType', [pattern[0] for pattern in patterns])

    token_patterns = [TokenPattern(TokenType[pattern[0]], pattern[1], pattern[2] if len(pattern) == 3 else None) for pattern in patterns]
    
    return lexer(token_patterns, text)
   
