'''
# 拿到paser的语法树,然后按照语法树的node和child 去生产code
    # 类似后序遍历,先生产subcode,后补cur_node的code

复杂程度和parser的语法规模差不多
    遍历的地方，不用解析，已经是确定的表达式结构
    直接对 对应的结构生产所需的vm代码即可(稍微简单点)

处理逻辑可以整合到parseNode,类似to_xmls() 写to_codes()
    代码不少，把这些功能单抽一个类，单独处理

# TODO (可以改进, 方便阅读) node中的这些变量操作可以整合进 ParseNode里
    #   每个类型的Node都继承于ParseNode,提供各children的访问和验证
    例如:
        varName = node.children[1].children[0].token # varNameNode -> Identifier
        
# 编译的时候并不会交叉引用，所以函数是一个接着一个的
    # 同理，lst_stack 也是一个接着一个的，开始翻译新函数时会clean掉前一个lst，
    #   所以设置self.lst_stack 是没有实际意义的。
    # 上述论述基于 jack语言没有设置内嵌函数
'''

from symbol_table import SymbolTable
from utils import CodingError

class Generator:
    def __init__(self, parse_tree_root) -> None:
        self.root = parse_tree_root
        self.gst = SymbolTable() # (global st) -- class level symbol table
        self.lst = SymbolTable()  # (local st) -- subroutine level symbol table
        self.className = None
        self.curFunName = None
        self.label_uid = 0 # 全局的uid
        self.codes = self.generateVmCode()
    
    def new_label(self) -> str:
        self.label_uid +=1
        # label: 类名+函数名+uid
        return 'LABEL_{}_{}_{}'.format(self.className, self.curFunName, self.label_uid)

    def searchST(self, key):
        if key in self.lst:
            return self.lst.vmstr(key)
        elif key in self.gst:
            return self.gst.vmstr(key)
        else:
            raise CodingError('[searchST] not defined var-{}'.format(key))
        
    def searchST_type(self, key):
        if key in self.lst:
            return True, self.lst.type(key)
        elif key in self.gst:
            return True, self.gst.type(key)
        else:
            return False, None
    
    def generateVmCode(self):
        return self.codeClass(self.root)
    
    # class: 'class' className '{' classVarDec* subroutineDec* '}'
    def codeClass(self, node):
        assert node.typetag == 'class'
        self.className = node.children[1].children[0].token 
        
        codes = []
        for chil in node.children[3:-1]:
            if chil.typetag == 'classVarDec':
                codes += self.codeClassVarDec(chil) # class-level symbol table
            elif chil.typetag == 'subroutineDec':
                codes += self.codeSubroutineDec(chil)
            else:
                raise CodingError('in [codeClass]')
        return codes
    
    # build the class-level symbol table
    # classVarDec: ('static'|'field') type varName (',' varNmae)* ';' # 仅类声明
    def codeClassVarDec(self, node):
        assert node.typetag == 'classVarDec'
        vkind = node.children[0].token # static | field
        vtype = node.children[1].token # int、char、boolean...
        
        for chil in node.children[2:]:
            if chil.typetag == 'varName':
                varname = chil.children[0].token
                self.gst.add(varname, vtype, vkind)
        return []
    
    # varDec: 'var' type varName (',' varName)* ';' 仅函数声明
    def codeVarDec(self, node):
        assert node.typetag == 'varDec'
        vtype = node.children[1].token
        
        for chil in node.children[2:]:
            if chil.typetag == 'varName':
                varname = chil.children[0].token
                self.lst.add(varname, vtype, 'local')
        return []
    
    # subroutineDec: ('constructor'|'function'|'method') ('void'|type) subroutineName
    #   '(' parameterList ')' subroutineBody
    def codeSubroutineDec(self, node):
        assert node.typetag == 'subroutineDec'
        # 进入新函数
        funtype = node.children[0].token # 'constructor'|'function'|'method'
        subroutine_name= node.children[2].children[0].token
        self.curFunName = subroutine_name 
        self.lst.clean()
        
        # lst 的特殊处理
        if 'method' == funtype: # 类方法第一个参数是this
            key, vtype, vkind =  'this', node.children[1].token, 'argument'
            self.lst.add(key, vtype, vkind)
        
        params_node = node.children[-3]
        self.codeParameterList(params_node) # 无codes生成
        
        body_node= node.children[-1]
        body_codes = self.codeSubRoutineBody(body_node) # 声明初需要init lst
        
        codes = []
        # 函数头定义 (function ClassName.SubName local_var_num)
        codes += ["function {}.{} {}".format(self.className,
                                            self.curFunName,
                                            self.lst.local_num()),]
        
        # 进入函数体的特殊处理
        if 'constructor' == funtype:
            # 分配内存，构造类。也可以根据 函数名new来判定 
            codes += [
                    "push constant {}".format(self.gst.field_num()), # field 变量数目, 不包括局部变量
                    "call Memory.alloc 1", # 内存分配，1个输入参数
                    "pop pointer 0", # 分配的结果保存到pointer 0 (this)
                    ]
        elif 'method' == funtype:
            codes += [
                    "push argument 0", # this = argument 0
                    "pop pointer 0",]
        else: #'function' == funtype:
           pass

        codes += body_codes
        
        return codes

    # parameterList: ((type varName) (',' type varName)*)?
    def codeParameterList(self, node):
        assert node.typetag == 'parameterList'

        i = 0
        while i < len(node.children):
            if node.children[i+1].typetag == 'varName':
                vtype =  node.children[i].token
                var_node =  node.children[i+1]
                var_name = var_node.children[0].token
                
                self.lst.add(var_name, vtype, 'argument')
                # codes += self.codePushVarName(var_node)
                i+=3
        return []

    # subroutineBody: '{' varDec* statements '}'
    def codeSubRoutineBody(self, node):
        assert node.typetag == 'subroutineBody'
        codes = []
        for chil in node.children[1:-2]:
            if chil.typetag == 'varDec':
                codes += self.codeVarDec(chil)
            else:
                raise CodingError('varDec* code error in [codeSubRoutineBody]')
        if node.children[-2].typetag == 'statements':
            codes += self.codeStatements(node.children[-2])
        else:
            raise CodingError('statements code error in [codeSubRoutineBody]')
        return codes
    
    # subroutineCall: subroutineName '(' expressionList ')' |
    #                   (className | varName) '.' subroutineName '(' expressionList ')'
    def codeSubRoutineCall(self, node):
        assert node.typetag == 'subroutineCall'
        codes = []
        # subroutineName '(' expressionList ')'
        if len(node.children)==4:
            subroutine_name = node.children[0].children[0].token
            exps_node = node.children[-2]
            
            # push self（第一个参数）类内的method调用
            codes += ['push pointer 0'] # push pointer this; 
            
            exps_code, param_len = self.codeExpressionList(exps_node)
            codes += exps_code # push 参数列表
            codes += ['call {}.{} {}'.format(self.className, subroutine_name, param_len+1)]
            return codes
        
        # (className | varName) '.' subroutineName '(' expressionList ')'
        elif len(node.children)==6:
            # TODO 注意，解析时无法区分 className 和 varName（查表symbol table）
            var_name = node.children[0].children[0].token
            ok, class_name = self.searchST_type(var_name) # 查表找到var对应的类
            if ok:
                # if 'varName' == node.children[0].typetag:
                var_node = node.children[0]
                codes += self.codePushVarName(var_node) # push self（第一个参数）
                param_this_len = 1 # one more this param            
            else:
                # 'className' == node.children[0].typetag:
                class_name = var_name
                param_this_len = 0
            
            exps_node = node.children[-2]
            exps_code, param_len = self.codeExpressionList(exps_node)
            codes += exps_code # push 参数列表
            param_len += param_this_len
            
            subroutine_name = node.children[2].children[0].token
            codes += ["call {}.{} {}".format(class_name, subroutine_name, param_len)]        
            return codes
        else:
            raise CodingError('in [codeSubRoutineCall]')

        # Q: 如何知道调用的函数是void？
        # A: 调用方是do XXX.XXX(), pop temp 0 处理掉无用的返回值 （trick）
        # 关键字还能起这个作用？减少编译时的工作量。同理 void func 用 return;直接表达，编译器部分不做额外处理。

    '''-------------------- Grammar: statements ------------------'''
    # statements: statement*
    def codeStatements(self, node):
        assert node.typetag == 'statements'
        codes = []
        for chil in node.children:
            codes += self.codeStatement(chil)
        return codes
    
    # statement: letStatement|ifStatement|whileStatement|doStatement|returnStatement
    def codeStatement(self, node):
        assert node.typetag == 'statement'
        chil = node.children[0]
        codes = []
        if 'letStatement' == chil.typetag: 
            codes += self.codeLet(chil)
        elif 'ifStatement' == chil.typetag:
            codes += self.codeIf(chil)
        elif 'whileStatement' == chil.typetag:
            codes += self.codeWhile(chil)
        elif 'doStatement' == chil.typetag:
            codes += self.codeDo(chil)
        elif 'returnStatement' == chil.typetag:
            codes += self.codeReturn(chil)
        else:
            raise CodingError('in [codeStatement]')
        return codes
    
    # 'let' varName ('[' expression ']')? '=' expression ';'
    def codeLet(self, node):
        assert node.typetag == 'letStatement'
        var_node = node.children[1]
        codes = []

        # 'let' varName '=' expression ';'
        if len(node.children) == 5:
            exp_node = node.children[3]
            codes += self.codeExpression(exp_node)
            codes += self.codePopVarName(var_node)
            return codes

        # 'let' varName ('[' expression ']')? '=' expression ';' 
        elif len(node.children) == 8:
            exp1_node = node.children[3]
            exp2_node = node.children[6]
            
            codes += self.codePushVarName(var_node)
            codes += self.codeExpression(exp1_node)
            codes += ['add']
            
            codes += self.codeExpression(exp2_node)
            codes += ['pop temp 0', # temp 0 = the value of expression2
                      'pop pointer 1',
                      'push temp 0',
                      'pop that 0'] 
            return codes
        else:
            raise CodingError('in [codeLet]')

    # returnStatement: 'return' expression? ';'
    def codeReturn(self, node):
        assert node.typetag == 'returnStatement'
        codes = []

        # return ;
        if len(node.children) == 2:
            codes += ['push constant 0'] # return for void （不保证与返回声明一致，如void）

        # return expression;
        elif len(node.children) == 3:
            exp_node = node.children[1]
            codes += self.codeExpression(exp_node)
        else:
            raise CodingError('in [codeReturn]')
        
        codes += ['return']
        return codes            
        
    # doStatement: 'do' subroutineCall ';'
    def codeDo(self, node):
        assert node.typetag == 'doStatement'
        if len(node.children) == 3:
            subRoutineNode = node.children[1]
            codes =[]
            codes += self.codeSubRoutineCall(subRoutineNode)
            codes += ['pop temp 0']
            return codes
        else:
            raise CodingError('in [codeDo]')
    
    # ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?  
    def codeIf(self, node):
        assert node.typetag == 'ifStatement'

        if len(node.children) == 7:
            exp_node = node.children[2]
            states1_node = node.children[5]
            L1 = self.new_label()
            codes = []
            codes += self.codeExpression(exp_node)
            codes += ['not']
            codes += ['if-goto {}'.format(L1)]
            codes += self.codeStatements(states1_node)
            codes += ['label {}'.format(L1)]
            return codes

        if len(node.children) == 11:
            exp_node = node.children[2]
            states1_node = node.children[5]
            states2_node = node.children[9]
            L1 = self.new_label()
            L2 = self.new_label()
            codes = []
            codes += self.codeExpression(exp_node)
            codes += ['not']
            codes += ['if-goto {}'.format(L1)]
            codes += self.codeStatements(states1_node)
            codes += ['goto {}'.format(L2)]
            codes += ['label {}'.format(L1)]
            codes += self.codeStatements(states2_node)
            codes += ['label {}'.format(L2)]
            return codes
        else:
            raise CodingError('in [codeIf]')
    
    # whileStatement: 'while' '(' expression ')' '{' statements '}' 
    def codeWhile(self, node):
        assert node.typetag == 'whileStatement'

        if len(node.children) == 7:
            exp_node = node.children[2]
            states1_node = node.children[5]
            L1 = self.new_label()
            L2 = self.new_label()
            codes = []
            codes += ['label {}'.format(L1)]
            codes += self.codeExpression(exp_node)
            codes += ['not']
            codes += ['if-goto {}'.format(L2)]
            codes += self.codeStatements(states1_node)
            codes += ['goto {}'.format(L1)]
            codes += ['label {}'.format(L2)]
            return codes
        else:
            raise CodingError('in [codeWhile]')

    '''-------------------- Grammar: expressions ------------------'''
    # expressionList: (expression (',' expression)* )?
    def codeExpressionList(self, node):
        assert node.typetag == 'expressionList'
        codes = []
        exp_num = 0
        
        for chil in node.children:
            if chil.typetag == 'expression':
                exp_num +=1
                codes += self.codeExpression(chil)
        return codes, exp_num

    # expression: term (op term)*  需要把值push到栈上
    def codeExpression(self, node):
        assert node.typetag == 'expression'
        codes = []
        
        term1_node = node.children[0]
        codes += self.codeTerm(term1_node)
        
        i = 1
        while i < len(node.children):
            op_node = node.children[i]
            term2_node = node.children[i+1]
            codes += self.codeTerm(term2_node)
            codes += self.codeOp(op_node)
            i+=2
        return codes
    
    # term: integerConstant| stringConstant| keywordConstant | varName |
    #   varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
    def codeTerm(self, node):
        assert node.typetag == 'term'
        if len(node.children)==1:
            chil = node.children[0]
            
            if 'integerConstant' == chil.typetag:
                return self.codeIntegerConstant(chil)
            elif 'stringConstant' == chil.typetag:
                return self.codeStringConstant(chil)
            elif 'keywordConstant' == chil.typetag:
                return self.codeKeyWordConstant(chil)
            elif 'varName' == chil.typetag:
                return self.codePushVarName(chil)
            elif 'subroutineCall' == chil.typetag:
                return self.codeSubRoutineCall(chil)
            else:
                raise CodingError('in codeTerm [len=1]')

        # unaryOp term
        elif len(node.children)==2:
            codes = []
            codes += self.codeTerm(node.children[1])
            codes += self.codeUnaryOp(node.children[0])
            return codes
        
        #  '(' expression ')'
        elif len(node.children)==3:
            return self.codeExpression(node.children[1])
        
        # varName '[' expression ']'
        elif len(node.children)==4:
            # set pointer 1 to arr + i
            # push / pop that 0
            var_node = node.children[0]
            exp_node = node.children[2]
            codes =[]
            
            codes += self.codePushVarName(var_node)
            codes += self.codeExpression(exp_node)
            codes += ['add']
            
            codes += [
                'pop pointer 1',
                'push that 0',
                ]
            return codes

    # varName: identifier
    def codePushVarName(self, node):
        # assert node.typetag == 'varName'  TODO 暂时无法区分 className varName
        var_name = node.children[0].token
        return ['push {}'.format(self.searchST(var_name))]

    # varName: identifier
    def codePopVarName(self, node):
        assert node.typetag == 'varName'
        var_name = node.children[0].token
        return ['pop {}'.format(self.searchST(var_name))]
    
    # keywordConstant: 'true' | 'false' | 'null' | 'this'
    def codeKeyWordConstant(self, node):
        assert node.typetag == 'keywordConstant'
        
        if len(node.children)==1:
            keyWord = node.children[0].token
            if keyWord == 'true':
                return ['push constant 1', 'neg']
            if keyWord == 'false' or keyWord == 'null':
                return ['push constant 0']
            if keyWord == 'this':
                return ['push pointer 0']   
        else:
            raise CodingError('in [codeKeyWordConstant]')
    
    # integerConstant
    def codeIntegerConstant(self, node):
        assert node.typetag == 'integerConstant'
        i = node.children[0].token
        return ['push constant {}'.format(i)]
    
    # stringConstant
    def codeStringConstant(self, node):
        assert node.typetag == 'stringConstant'
        ss = node.children[0].token
        strlen = len(ss)
        codes = []
        codes += [
            'push constant {}'.format(strlen),
            'call String.new 1',
            ]
        
        for s in ss:
            codes += [
                'push constant {}'.format(ord(s)),
                'call String.appendChar 2',
                ]

        return codes
    
    # op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    def codeOp(self, node):
        assert node.typetag == 'op'
        index = {
            '+' : 'add',
            '-' : 'sub',
            '*' : 'call Math.multiply 2',
            '/' : 'call Math.divide 2',
            '&' : 'and',
            '|' : 'or',
            '<' : 'lt',
            '>' : 'gt',
            '=' : 'eq',
        }
        op = node.children[0].token
        codes = [index[op]]
        return codes
    
    # unaryOp: '-' | '~'
    def codeUnaryOp(self, node):
        assert node.typetag == 'unaryOp'
        index = {
            '-' : 'neg',
            '~' : 'not',
        }
        unary_op = node.children[0].token
        codes = [index[unary_op]]
        return codes