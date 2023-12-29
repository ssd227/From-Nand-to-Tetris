import re


########################  字符串预处理  ##########################
def replace_whitespace(input_string, replacement=''):
    # 使用正则表达式替换所有空白字符
    result = re.sub(r'\s', replacement, input_string)
    return result


def remove_comment(input_string):
    result = input_string.split('//')[0]
    return result


########################  自定义异常  ##########################
class RedefineError(Exception):
    def __init__(self, message="redefine symbol"):
        self.message = message
        super().__init__(self.message)
        
class OpsError(Exception):
    def __init__(self, message="unsupport ops"):
        self.message = message
        super().__init__(self.message)
