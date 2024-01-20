from tokenizer import Tokenizer
from symbol_table import terminalType
from utils import SyntaxError

'''
# 一些写法上的改进
TODO *操作 能不能用装饰器去抽象，不用每次都显式操作
        进一步不仅仅能封装一个函数，能不能封装多个函数
        
TODO |操作同理，能不能抽象封装 


TODO 还存在一个问题，主编译流程抛出异常，每次都需要重新编译前文的所有内容，效率不高
'''

UnshowXmlTag = {'op',
                'unaryOp',
                'gVarName',
                'subroutineName',
                'className', 
                'subroutineCall',
                'integerConstant',
                'stringConstant',
                'keywordConstant',
                'statement',}

class ParseNode:
    def __init__(self, typetag) -> None:
        self.typetag = typetag
        self.children=[]
        self.unshowFlag = True
    
    def add(self, x):
        self.children.append(x)
        
    def empty(self):
        return len(self.children) == 0

    def to_xmls(self):
        xmls = []
        for child in self.children:
            xmls += child.to_xmls()
        if self.unshowFlag and self.typetag in UnshowXmlTag:
            return xmls
        
        xmls = ['<{}>'.format(self.typetag)] + xmls + ['</{}>'.format(self.typetag)]
        return xmls

class Parser:
    def __init__(self, file_path, tokenizer:Tokenizer) -> None:
        self.infile = file_path
        self.tokenizer = tokenizer
        self.tokens = tokenizer.tokens()
        self.root = None

        self.ctid = 0   # current Token ID
        self.compile()
        
    # 输出Xxx.xml文件
    def persistence(self):
        out_path = self.infile[:-4]+'xml'
        
        # 遍历树结构
        xmls = self.root.to_xmls()
        xmls = [line+"\n" for line in xmls] # 加入换行
        with open(out_path, 'w') as f:
            f.writelines(xmls)
        print('write[{}] done'.format(out_path))


    def compile(self):
        # 每个文件只有一个class, 解析完就结束了
        self.ctid = 0
        self.root = self.gClass()
        return

    '''******************** Terminal & Non-Terminal Grammer Rules **********************'''
    # Note: def gXXX(self) means grammer rule function
    
    '''-------------------- Grammar: program structure ------------------'''
    # class: 'class' className '{' classVarDec* subroutineDec* '}'
    def gClass(self):
        node = ParseNode('class')
        node.add(self.gWord("class"))
        node.add(self.gClassName())
        node.add(self.gWord("{"))
        
        # classVarDec*
        while True:
            ok, chil_node = self.gClassVarDec_safe()
            if ok: node.add(chil_node)
            else: break
        
        # subroutineDec*
        while True:
            ok, chil_node = self.gSubRoutineDec()
            if ok: node.add(chil_node)
            else: break

        node.add(self.gWord("}"))    
        return node
    
    # classVarDec: ('static'|'field') type varName (',' varNmae)* ';'
    def gClassVarDec_safe(self):
        checkpointA = self.ctid
        try:
            node = ParseNode('classVarDec')
            
            # try first 'static'
            ok, chil_node = self.gWord_safe('static')
            if not ok:
                # try second 'field'
                ok, chil_node = self.gWord_safe('field')
            if chil_node: # 解析非空
                node.add(chil_node)
            else:
                raise SyntaxError("gClassVarDec Error no ['static or field']")
            
            node.add(self.gType())
            node.add(self.gVarName())
                
            # (',' varName)*
            while True:
                try:
                    # 存在解析失败的情况，使用cache保证原子操作
                    checkpointB = self.ctid
                    cache = [] 
                    cache.append(self.gWord(','))
                    cache.append(self.gVarName())
                except SyntaxError:
                    self.ctid = checkpointB # 回到未解析状态，cache作废
                    break
                else:
                    # 成功解析后，add cache[成功解析的结果]
                    [node.add(item) for item in cache]
                    continue

            node.add(self.gWord(';'))
            
        except SyntaxError:
            self.ctid = checkpointA
            return False, None
        
        return True, node

    # type: 'int'|'char'|'boolean'|className
    def gType(self):
        # branch1 int
        ok, chil_node = self.gWord_safe('int')
        if ok: return chil_node
        
        # branch2 char
        ok, chil_node = self.gWord_safe('char')
        if ok: return chil_node
        
        # branch3 boolean
        ok, chil_node = self.gWord_safe('boolean')
        if ok: return chil_node
        
        # TODO 要不要统一修改成返回 (ok, Node)的格式
        # branch4 className
        chil_node = self.gClassName() # or的最后一个条件必须成功解析，否则就报错
        return chil_node

    # subroutineDec: ('constructor'|'function'|'method') ('void'|type) subroutineName
    #   '(' parameterList ')' subroutineBody
    def gSubRoutineDec(self):
        checkpointA = self.ctid
        try:
            node = ParseNode('subroutineDec')
            
            # ('constructor'|'function'|'method')
            ok, chil_node = self.gWord_safe('constructor')
            if not ok:
                ok, chil_node = self.gWord_safe('function')
                if not ok:
                    chil_node = self.gWord('method') # 仍没有命中, 抛出异常
            node.add(chil_node)
            
            # ('void'|type)
            ok, chil_node = self.gWord_safe('void')
            if not ok:
                chil_node = self.gType()
            node.add(chil_node)

            # subroutineName
            node.add(self.gSubRoutineName())
            node.add(self.gWord('('))
            node.add(self.gParameterList())
            
            node.add(self.gWord(')'))
            node.add(self.gSubRoutineBody())
        except SyntaxError:
            self.ctid = checkpointA
            return False, None

        return True, node

    # parameterList: ((type varName) (',' type varName)*)?
    def gParameterList(self):
        checkpointA = self.ctid
        try:
            node = ParseNode('parameterList')
            node.add(self.gType())
            node.add(self.gVarName())
            
            # (',' type varNmae)*
            while True:
                try:
                    # 存在解析失败的情况，使用cache保证原子操作
                    checkpointB = self.ctid
                    cache = [] 
                    cache.append(self.gWord(','))
                    cache.append(self.gType())
                    cache.append(self.gVarName())
                except SyntaxError:
                    self.ctid = checkpointB # 回到未解析状态，cache作废
                    break
                else:
                    # 成功解析后，add cache[成功解析的结果]
                    [node.add(item) for item in cache]
                    continue
        except SyntaxError:
            self.ctid = checkpointA
            return ParseNode('parameterList') # ?允许0或1, 此时返回空解析[]

        return node

    # subroutineBody: '{' varDec* statements '}'
    def gSubRoutineBody(self):
        node = ParseNode('subroutineBody')
        node.add(self.gWord('{'))
        
        # varDec*
        while True:
            ok, chil_node = self.gVarDec_safe()
            if ok: node.add(chil_node)
            else: break
        
        node.add(self.gStatements()) # TODO  可能是个空的 Node.children == []
        node.add(self.gWord('}'))
        
        return node
        
    # varDec: 'var' type varName (',' varName)* ';'
    def gVarDec_safe(self):
        checkpointA = self.ctid
        try:
            node = ParseNode('varDec')
            node.add(self.gWord("var"))
            node.add(self.gType())
            node.add(self.gVarName())
        
            # (',' varName)*
            while True:
                try:
                    # 存在解析失败的情况，使用cache保证原子操作
                    checkpointB = self.ctid
                    cache = [] 
                    cache.append(self.gWord(','))
                    cache.append(self.gVarName())
                except SyntaxError:
                    self.ctid = checkpointB # 回到未解析状态，cache作废
                    break
                else:
                    # 成功解析后，add cache[成功解析的结果]
                    [node.add(item) for item in cache]
                    continue
                
            node.add(self.gWord(';')) # 吃不掉就抛出异常

        except SyntaxError:
            self.ctid = checkpointA # 回到未解析状态，letNode作废
            return False, None
        
        return True, node

    # className: identifier
    def gClassName(self):
        node = ParseNode('className')
        child_node = self.gIdentifier()
        node.add(child_node)
        return node
    
    # subroutineName: identifier
    def gSubRoutineName(self):
        node = ParseNode('subroutineName')
        child_node = self.gIdentifier()
        node.add(child_node)
        return node
    
    # varName: identifier
    def gVarName(self):
        node = ParseNode('gVarName')
        node.add(self.gIdentifier())
        return node
    
    # varName: identifier
    def gVarName_safe(self):
        node = ParseNode('gVarName')
        try:
            chil_node = self.gIdentifier()
            node.add(chil_node)
        except SyntaxError:
            return False, None
        return True, node
    
    '''-------------------- Grammar: statements ------------------'''
    # statements: statement*
    def gStatements(self):
        node = ParseNode('statements')
        while True:
            ok, chil_node = self.gStatement_safe()
            if ok:
                node.add(chil_node)
            else:
                break # 结束 *的解析
        return node # 允许[] TODO 空statement需不需要添加删除逻辑

    # statement: letStatement|ifStatement|whileStatement|doStatement|returnStatement
    def gStatement_safe(self):  
        node = ParseNode('statement')
        ok, chil_node = self.gLetStatement_safe()
        if not ok:
            ok, chil_node = self.gIfStatement_safe()
            if not ok:
                ok, chil_node = self.gWhileStatement_safe()
                if not ok:
                    ok, chil_node = self.gDoStatement_safe()
                    if not ok:
                        ok, chil_node = self.gReturnStatement_safe() # TODO 这几个safe类型的函数，能不能简单用装饰器封装得到。保留原始出异常的函数 return node 设定
        if chil_node:
            node.add(chil_node)
            return True, node

        return False, None

    # 'let' varName ('[' expression ']')? '=' expression ';'
    def gLetStatement_safe(self):
        checkpointA = self.ctid
        try:
            letNode = ParseNode('letStatement')
            letNode.add(self.gWord("let"))
            letNode.add(self.gVarName())
            
            # ('[' expression ']')?
            checkpointB = self.ctid
            try:
                cache = []
                cache.append(self.gWord('['))
                cache.append(self.gExpression())
                cache.append(self.gWord(']'))
            except SyntaxError as e:
                self.ctid = checkpointB
            else:
                [letNode.add(item) for item in cache]

            letNode.add(self.gWord("="))
            letNode.add(self.gExpression())    
            letNode.add(self.gWord(";"))    
        except SyntaxError as e:
            self.ctid = checkpointA # 回到未解析状态，letNode作废
            return False, None

        return True, letNode
    
    # ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?     
    def gIfStatement_safe(self):
        checkpointA = self.ctid
        try:
            ifNode = ParseNode('ifStatement')
            ifNode.add(self.gWord("if"))
            ifNode.add(self.gWord("("))
            ifNode.add(self.gExpression())
            ifNode.add(self.gWord(")"))
            ifNode.add(self.gWord("{"))
            ifNode.add(self.gStatements())
            ifNode.add(self.gWord("}"))
            
            checkpointB = self.ctid
            try:
                cache = []
                cache.append(self.gWord("else"))
                cache.append(self.gWord("{"))
                cache.append(self.gStatements())
                cache.append(self.gWord("}"))
            except:
                self.ctid = checkpointB
            else:
                [ifNode.add(chil_node) for chil_node in cache]

        except SyntaxError:
            self.ctid = checkpointA # 回到未解析状态，ifNode作废
            return False, None

        # 完成解析，正确返回
        return True, ifNode

    # whileStatement: 'while' '(' expression ')' '{' statements '}'
    def gWhileStatement_safe(self):  # (代码无关)感觉做梦又梦到这个情景了
        checkpointA = self.ctid
        try:
            whileNode = ParseNode('whileStatement')
            whileNode.add(self.gWord("while"))
            whileNode.add(self.gWord("("))
            whileNode.add(self.gExpression())
            whileNode.add(self.gWord(")"))
            whileNode.add(self.gWord("{"))
            whileNode.add(self.gStatements())
            whileNode.add(self.gWord("}"))
        except SyntaxError:
            self.ctid = checkpointA # 回到未解析状态，letNode作废
            return False, None

        return True, whileNode

    # doStatement: 'do' subroutineCall ';'
    def gDoStatement_safe(self):
        checkpointA = self.ctid
        try:
            doNode = ParseNode('doStatement')
            doNode.add(self.gWord("do"))
            doNode.add(self.gSubRoutinueCall())
            doNode.add(self.gWord(";"))
        except SyntaxError as e:
            self.ctid = checkpointA # 回到未解析状态，doNode作废
            return False, None

        return True, doNode

    # returnStatement: 'return' expression? ';'
    def gReturnStatement_safe(self):
        checkpointA = self.ctid
        try:
            returnNode = ParseNode('returnStatement')
            returnNode.add(self.gWord("return"))
            
            # expression?
            checkpointB = self.ctid
            try:
                chil_node = self.gExpression()
            except SyntaxError:
                self.ctid = checkpointB # 解析失败，返回检查点
            else:
                returnNode.add(chil_node) # 解析成功
            returnNode.add(self.gWord(";"))
        
        except SyntaxError:
            self.ctid = checkpointA
            return False, None

        return True, returnNode
    '''-------------------- Grammar: expressions ------------------'''
    # expression: term (op term)*
    def gExpression(self):
        node = ParseNode('expression')
        node.add(self.gTerm())
        
        # (op term)*
        while True:
            try:
                checkpointB=self.ctid
                cache = []
                cache.append(self.gOp())
                cache.append(self.gTerm())
            except SyntaxError:
                self.ctid = checkpointB
                break
            else:
                [node.add(item) for item in cache]
        
        return node
        
    # term: integerConstant| stringConstant| keywordConstant | varName |
    #   varName'[' expression']' | subroutinueCall | '(' expression ')' | unaryOp term
    def gTerm(self):
        node = ParseNode("term")
        
        # subroutinueCall (不止LL1，XXX.XXX), 改变解析位置只是个取巧的方法（贪心解析）
        checkpointB = self.ctid
        try:
            chil_node = self.gSubRoutinueCall()
        except SyntaxError:
            self.ctid = checkpointB
        else:
            node.add(chil_node)
            return node
        
        # varName'[' expression']'
        checkpointA = self.ctid
        try:
            cache = []
            cache.append(self.gVarName())
            cache.append(self.gWord('['))
            cache.append(self.gExpression())
            cache.append(self.gWord(']'))
        except SyntaxError:
            self.ctid = checkpointA
        else:
            [node.add(item) for item in cache]
            return node
        
        # '(' expression ')'
        checkpointC = self.ctid
        try:
            cache = []
            cache.append(self.gWord('('))
            cache.append(self.gExpression())
            cache.append(self.gWord(')'))
        except SyntaxError:
            self.ctid = checkpointC
        else:
            [node.add(item) for item in cache]
            return node
        
        # integerConstant
        ok, chil_node = self.gIntegerConstant_safe()
        if ok:
            node.add(chil_node)
            return node

        # stringConstant
        ok, chil_node = self.gStringConstant_safe()
        if ok:
            node.add(chil_node)
            return node
        
        # keywordConstant
        ok, chil_node = self.gKeyWordConstant_safe()
        if ok:
            node.add(chil_node)
            return node
        
        # varName
        ok, chil_node = self.gVarName_safe()
        if ok:
            node.add(chil_node)
            return node
        
        ''' last or_branch, 可以抛出异常'''
        # unaryOp term
        node.add(self.gUnaryOp())
        node.add(self.gTerm())
        return node

    # subroutineCall: subroutineName '(' expressionList ')' |
    #                   (className | varName) '.' subroutineName '( expressionList )'
    def gSubRoutinueCall(self):
        node = ParseNode('subroutineCall')
        
        # subroutineName '(' expressionList ')'
        checkpointA = self.ctid
        try:
            cache = []
            cache.append(self.gSubRoutineName())
            cache.append(self.gWord('('))
            cache.append(self.gExpressionList())
            cache.append(self.gWord(')'))
            
        except SyntaxError:
            self.ctid = checkpointA
        else:
            [node.add(item) for item in cache]
            return node
        
        #  (className | varName) '.' subroutineName '( expressionList )'
        checkpointB = self.ctid
        try:
            cache = []
            
            # 解析(className | varName)成功，否则会立即抛出异常
            checkpointC= self.ctid # TODO 上个保险，其实可以不加
            try:
                chil_node= self.gClassName()
            except:
                self.ctid = checkpointC
                chil_node = self.gVarName()
            cache.append(chil_node)
            
            cache.append(self.gWord('.'))
            cache.append(self.gSubRoutineName())
            cache.append(self.gWord('('))

            cache.append(self.gExpressionList()) # TODO 重点排查bug
            cache.append(self.gWord(')'))

        except SyntaxError as e:
            self.ctid = checkpointB
            raise SyntaxError('[gSubRoutinueCall] parsing error after |') 
        else:
            [node.add(item) for item in cache]
            return node

    # expressionList: (expression (',' expression)* )?
    def gExpressionList(self):
        checkpointA = self.ctid
        try:
            node = ParseNode('expressionList')
            node.add(self.gExpression())
            
            # (',' expression)*
            while True:
                try:
                    checkpointB = self.ctid
                    cache = []
                    cache.append(self.gWord(','))
                    cache.append(self.gExpression())
                except:
                    self.ctid = checkpointB
                    break
                else:
                    [node.add(item) for item in cache]
        except:
            self.ctid = checkpointA
            return ParseNode('expressionList')  # ?=0
        return node # ?=1

    # op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    def gOp(self):
        node = ParseNode('op')
        tknode = self.curTokenNode()
        if tknode.token in {'+', '-', '*', '/', '&', '|', '<', '>', '='}:
            node.add(tknode)
            self.ctid+=1
            return node
        raise SyntaxError('gOp:{}'.format(tknode.token))

    # unaryOp: '-' | '~'
    def gUnaryOp(self):
        node = ParseNode('unaryOp')
        tknode = self.curTokenNode()
        if tknode.token in {'-', '~'}:
            node.add(tknode)
            self.ctid+=1
            return node
        raise SyntaxError('gOp:{}'.format(tknode.token))

    # keywordConstant: 'true' | 'false' | 'null' | 'this'
    def gKeyWordConstant(self):
        node = ParseNode('keywordConstant')
        tknode = self.curTokenNode()
        if tknode.token in {'true', 'false', 'null', 'this'}:
            node.add(tknode)
            self.ctid+=1
            return node
        raise SyntaxError('gOp:{}'.format(tknode.token))
    

    # keywordConstant: 'true' | 'false' | 'null' | 'this'
    def gKeyWordConstant_safe(self):
        node = ParseNode('keywordConstant')
        tknode = self.curTokenNode()
        if tknode.token in {'true', 'false', 'null', 'this'}:
            node.add(tknode)
            self.ctid+=1
            return True, node
        return False, None

    # integerConstant
    def gIntegerConstant_safe(self):
        node = ParseNode('integerConstant')
        tknode = self.curTokenNode()
        if tknode.typetag == terminalType.integerConstant:
            node.add(tknode)
            self.ctid+=1
            return True, node
        return False, None
    
    # stringConstant
    def gStringConstant_safe(self):
        node = ParseNode('stringConstant')
        tknode = self.curTokenNode()
        if tknode.typetag == terminalType.stringConstant:
            node.add(tknode)
            self.ctid+=1
            return True, node
        return False, None

    '''-------------------- help grammer function ------------------'''
    # 匹配特定字符ss, 并吃掉对应token, mismatch则抛出解析异常
    def gWord(self, ss):
        tk_node = self.curTokenNode()
        if tk_node.token != ss:
            raise SyntaxError('gWord: tokens[{}]-[{}] VS need-[{}]'.format(self.ctid, tk_node.token, ss))
        self.ctid+=1
        return tk_node
    
    def gWord_safe(self, ss):
        tk_node = self.curTokenNode()
        if tk_node.token != ss:
            return False, None
        self.ctid+=1
        return True, tk_node

    def gIdentifier(self):
        tk_node = self.curTokenNode()
        if tk_node.typetag != terminalType.identifier:
            raise SyntaxError('gVarName:{}'.format(tk_node.token))
        self.ctid += 1
        return tk_node

    def curTokenNode(self):
        return self.tokens[self.ctid]