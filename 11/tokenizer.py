import re
from typing import Any
from utils import TokenizerError, SplitLineError
from symbol_table import terminalType


'''
jack lexicon

integerConstant: a decimal number in the range 0 ... 32767

StringConstant: '"' a sequence of Unicode characters,
                not including double quote or newline '"'

identifier: a sequence of letters, digits, and
            underscore ( '_' ) not starting with a digit.
'''

KeyWord = {
    'class', 'constructor', 'function', 'method',
    'field', 'static', 'var', 'int',
    'char', 'boolean', 'void', 'true',
    'false', 'null', 'this', 'let',
    'do', 'if', 'else', 'while', 'return',
}

Symbol = {
    '{', '}', '(', ')', '[', ']', '.', ',', ';', '+',
    '-', '*', '/', '&', '|', '<', '>', '=', '~'}

SymbolReplace = {
    '<' : '&lt;',
    '>' : '&gt;',
    r'"': '&quot;',
    '&'  : '&amp;',
}

class Token:
    def __init__(self, token, typetag) -> None:
        self.typetag = typetag
        self.token = token

    def to_txml(self):
        if (self.typetag == terminalType.symbol) and (self.token in SymbolReplace):
            return  r'<{}> {} </{}>'.format(self.typetag, SymbolReplace[self.token], self.typetag)
        
        return r'<{}> {} </{}>'.format(self.typetag, self.token, self.typetag)

    def to_xmls(self):
        return [self.to_txml()]
       

class Tokenizer:
    def __init__(self, file_path) -> None:
        self.infile = file_path
        self._tokens:list[Token] = []
        self.compile() # token化操作

    def tokens(self):
        return self._tokens
    
    def __getitem__(self, index):
        return self._tokens[index]

    def compile(self): 
        with open(self.infile, 'r') as f:
            raw_code = f.read()
    
        # 0. 预处理，删除注释
        clean_code = Tokenizer.removeCommand(raw_code)
        if len(clean_code)==0:
            print("Note: file with empty valid code!!!")
            return
        
        # 1. 使用symbol、whitespace字符切分string line (note:字符串里的空字符不能动)
        token_list = Tokenizer.splitLine(clean_code)

        # 2 识别各split token
        for token in token_list:
            if token in KeyWord:
                self._tokens.append(Token(token, terminalType.keyword))
            
            elif token in Symbol:
                self._tokens.append(Token(token, terminalType.symbol))

            elif token.isdigit():
                assert 0<=int(token)<2**15, "regi is 16bit, ensure int({}) in [0, 2**15) ".format(token)
                self._tokens.append(Token(token, terminalType.integerConstant))
            
            elif Tokenizer.matchStringConstant(token):
                self._tokens.append(Token(token[1:-1], terminalType.stringConstant))
            
            elif Tokenizer.matchIdentifier(token):
                self._tokens.append(Token(token, terminalType.identifier))
            
            else:
                print('[{}]-[{}]'.format(token, token_list))
                raise TokenizerError(message=token)

        return

    
    # 输出XxxT.xml文件
    def persistence(self):
        
        out_path = self.infile[:-5]+'T.xml'
        token_xmls = [tk.to_txml() for tk in self._tokens]
                
        xmls = ['<tokens>'] + token_xmls + ['</tokens>'] # root tag
        xmls = [line+"\n" for line in xmls] # 加入换行
        with open(out_path, 'w') as f:
            f.writelines(xmls)
        print('write[{}] done'.format(out_path))
    
    '''******************** Terminal Grammer Rules **********************'''
    @staticmethod
    def removeCommand(line):
        # 规则1:  //
        re1 = r'//.*'
        line = re.sub(re1, '', line) 
        # 规则2: /* */ 或 /** */
        re2 = r'/\*.*?\*/'
        line = re.sub(re2, '', line, flags=re.S) # re.S使得.匹配\n
        # 规则3:掐头去尾
        line = line.strip()    
        return line

    @staticmethod
    def matchStringConstant(input_string):
        pattern = r'^".*"$'
        return re.match(pattern, input_string)

    @staticmethod
    def matchIdentifier(input_string):
        pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
        return re.match(pattern, input_string)

    @staticmethod
    def splitLine(str_line):
        def append_cache(arr, ss):
            if len(ss)>0:
                arr.append(''.join(ss))
    
        inquote = False
        tokens = []
        cache = []
    
        for s in str_line:
            if s == r'"':
                if inquote: # 离开字符串
                    cache.append(s)
                    append_cache(tokens, cache)
                    cache = []
                    inquote = False
                    continue    
                else:       # 进入字符串
                    append_cache(tokens, cache) # 清空cache
                    cache = [s]
                    inquote = True
                    continue
            
            # 非"字符   
            if inquote: # 字符串内
                cache.append(s)
                continue
            
            else:       # 字符串外
                if s in {' ', '\t', '\n'} : # 空白字符分割
                    append_cache(tokens, cache)
                    cache = []
                    continue

                if s in Symbol:             # symbol 强分割
                    append_cache(tokens, cache)
                    cache = []
                    tokens.append(s)        # add symbol字符
                    continue
                
                cache.append(s)             # 不需要分割的字符
                continue

        # raise SplitLineError('not hit if any branch')
        return tokens