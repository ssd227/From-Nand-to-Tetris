import glob


def list_dir_jack_files(dirpath):
    files = []
    base = dirpath + '*.jack'
    for f in glob.glob(base):
        files.append(f)
    return files

class TokenizerError(Exception):
    def __init__(self, message):
        self.message = r'token[{}] can\'t match Tokenizer rules'.format(message)
        super().__init__(self.message)

class SplitLineError(Exception):
    def __init__(self, msg):
        self.message = r'Split_Line_Error, {}'.format(msg)
        super().__init__(self.message)
        
class SyntaxError(Exception):
    def __init__(self, msg):
        self.message = r'Syntax_Error, {}'.format(msg)
        super().__init__(self.message)
        
class CodingError(Exception):
    def __init__(self, msg):
        self.message = r'Coding_Error, {}'.format(msg)
        super().__init__(self.message)

class STError(Exception):
    def __init__(self, msg):
        self.message = r'ST_Error, {}'.format(msg)
        super().__init__(self.message)