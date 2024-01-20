# 编译器

目前实现了两个功能类
- class `Tokenizer`
  - .persistence() 保存XxxT.xml
- class `Parser`
  - .persistence() 保存Xxx.xml

主流程`compiler.py` 调用两个功能类实现xml生成功能  


## 框架阐述
- try catch 使用场景
  - 尝试解析，并允许失败
  - jack语法函数有两种
  - gXxx 
    - 不处理Error, 直接return Node。caller酌情处理Error
  - gXxx_safe
      - 函数内部try catch Error，返回(True, node) 或者(False,None)

- 递归处理
  - 使用ParseNode构造解析树
  - LL1(根据当前token就能够消除歧义)
  - LL2(还不完全支持）
    - 比如：classVarName.funName, 不提前读取'.' 无法正确解析
    - 目前处理方式：设置parser逻辑解析顺序，优先长序列解析(贪心)

## Tips (!!! 初期想法，不是很正确 !!!)
1) 一个语法规则是否需要单独处理Error，在于语法规则里是否存在grammerRule* 或 grammerRule | grammerRule的操作
    - \* 允许解析失败。
    - |  允许前述操作解析失败，但在最后位置的解析必须成功，否则可原地抛出解析异常。
    - 其他语法解析失败，可原地抛出解析异常

## TODO
- 在project 10里完善文档
- 装饰器封装*？|三个基本操作，抽象语法处理流程