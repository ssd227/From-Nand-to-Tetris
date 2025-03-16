from collections import namedtuple
from utils import STError

class terminalType:
    keyword = "keyword"
    symbol = "symbol"
    integerConstant = "integerConstant"
    stringConstant = "stringConstant"
    identifier = "identifier"
    

class VarKind:
    field = 'field'
    static = 'static'
    local = 'local'
    argument = 'argument'
    

Row = namedtuple('STCols', ['vtype', 'vkind', 'vid'])

class SymbolTable:    
    def __init__(self, scop=0) -> None:
        self.ids = {'field'    : 0,
                    'static'   : 0,
                    'argument' : 0,
                    'local'    : 0,
                    }
        
        self.hash_table = dict()
        self.scope = scop # scope (class level, subroutine level) 分别用(0，1)表示
    
    def add(self, key, vtype, vkind):
        if key not in self.hash_table:
            row = Row(vtype, vkind, self.ids[vkind])
            self.ids[vkind] += 1
            self.hash_table[key] = row
        else:
            raise STError('变量重复声明 key-[{}], type-[{}], kind-[{}]'.format(key, vtype, vkind))
    
    def vmstr(self, key):
        row = self.hash_table[key]
        if  row.vkind == 'field':
            segment_kind = 'this'
        else:
            segment_kind = row.vkind
        return '{} {}'.format(segment_kind, row.vid)
    
    def type(self, key):
        row = self.hash_table[key]
        return row.vtype
    
    def clean(self):
        self.hash_table = dict()
        for k in self.ids.keys():
            self.ids[k] = 0
        
    def local_num(self):
        return self.ids['local']
    
    def field_num(self):
        return self.ids['field']        

    # in op
    def __contains__(self, item):
        return item in self.hash_table