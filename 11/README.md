# 编译器

## RUN
```
python compiler.py xxx.jack|含有多个XXX.jack的dir_path
```
---
## 三个功能类
- class `Tokenizer`
  - .persistence() 保存XxxT.xml
- class `Parser`
  - .persistence() 保存Xxx.xml
- class `Generator`
  - 遍历parser tree，给每个表达式生成code
    - 主逻辑 `self.generateVmCode()` 
    - `class SymbolTable` 提供global和local变量解析


主流程`compiler.py`依次调用三个功能类，生成vm code

---
## 框架阐述(开发想法)
1) `try catch`使用场景
  - 尝试解析，并允许失败
  - jack语法函数有两种
  - gXxx 
    - 不处理Error, 直接return Node。caller酌情处理Error
  - gXxx_safe
      - 函数内部try catch Error，返回(True, node) 或者(False,None)

2) `递归处理`
  - 使用ParseNode构造解析树
  - LL1(根据当前token就能够消除歧义)
  - LL2(还不完全支持）
    - 比如：classVarName.funName, 不提前读取'.' 无法正确解析
    - 目前处理方式：设置parser逻辑解析顺序，优先长序列解析(贪心)

3) `code Generator`
  - 拿到paser的语法树,然后按照语法树的node和child 去生产code
    类似后序遍历,先生产subcode,后补cur_node的code

  - 复杂程度和parser的语法规模差不多
    - 遍历的地方，不用解析，已经是确定的表达式结构。
      对应的结构直接生成所需的vm代码即可(稍微简单点)

4) `local symbol table` 的处理情况
- 编译的时候并不会交叉引用，所以函数是一个接着一个的。
  同理，lst_stack 也是一个接着一个的，开始翻译新函数时会clean掉前一个lst，
  所以设置self.lst_stack 是没有实际意义的。
- 注：上述论述基于`jack`语言没有设置内嵌函数

---
## TODO
1) `class Generator`的逻辑可整合入`parseNode`, 类似`to_xmls()`
   去实现`to_codes()`。目前看代码不少，就把这些功能单独封装成
   generator类处理。

2) (可以改进, 方便阅读) node中的这些变量操作可以整合进 ParseNode里
    - 每个类型的Node都继承于ParseNode,提供各children的访问和验证
    - 例如:
      ``` python
      # varNameNode -> Identifier
      varName = node.children[1].children[0].token 
      ```
