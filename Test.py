from Lexer.HulkTokenize import hulk_tokenize

with open("Test1.txt", "r", encoding="utf-8") as file:
    text = file.read()

tokens = []
tokens = hulk_tokenize(text)
print (tokens, sep = "\n")





