from enum import Enum, auto

# 静态变量
CompareLabelCount = 0
LogicLabelCount = 0

# commandType = {
#     "C_ARITHMETIC":0,
#     "C_PUSH":1,
#     "C_POP":2,
#     "C_LABEL":3,
#     "C_GOTO":4,
#     "C_IF":5,
#     "C_FUNCTION":6,
#     "C_RETURN":7,
#     "C_CALL":8,
# }

class CommandType(Enum):
    C_ARITHMETIC = auto()
    C_PUSH = auto()
    C_POP = auto()
    C_LABEL = auto()
    C_GOTO = auto()
    C_IF = auto()
    C_FUNCTION = auto()
    C_RETURN = auto()
    C_CALL = auto()

class ST:
    push = 'push'
    pop  = 'pop'
    
    constant  = 'constant'
    local     = 'local'
    argument  = 'argument'
    this      = 'this'
    that      = 'that'
    static    = 'static'
    temp      = 'temp'
    pointer   = 'pointer'
    
    op_add  = 'add'
    op_sub  = 'sub'
    op_neg  = 'neg'
    op_eq   = 'eq'
    op_gt   = 'gt'
    op_lt   = 'lt'
    op_and  = 'and'
    op_or   = 'or'
    op_not  = 'not'
    
Segment2Addr = {
    ST.local    : 'LCL',
    ST.argument : 'ARG',
    ST.this     : 'THIS',
    ST.that     : 'THAT',
    }

ArithmeticOps = {
    ST.op_add,
    ST.op_sub,
    ST.op_neg,
    ST.op_eq,
    ST.op_gt,
    ST.op_lt,
    ST.op_and,
    ST.op_or,
    ST.op_not,
    }

UnitOps = {
    ST.op_neg,
    ST.op_not,
    }

PushPopArgs = {
    ST.local,
    ST.argument,
    ST.this,
    ST.that,
    ST.constant,
    ST.static,
    ST.temp,
    ST.pointer,
    }
