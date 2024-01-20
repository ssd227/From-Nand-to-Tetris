

def remove_comment(input_string):
    result = input_string.split('//')[0]
    return result

########################  自定义异常  ##########################
class PushPopPointerError(Exception):
    def __init__(self, message="push/pop Pointer Error, ensure arg2-idx is 0|1."):
        self.message = message
        super().__init__(self.message)