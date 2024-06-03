class RedefineException(Exception):
    def __init__(self, type, name):
        print(type, " with the same name (", name, ") already in context.")
        super().__init__()
