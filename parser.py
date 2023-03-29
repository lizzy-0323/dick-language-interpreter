from lexer import Lexer
"""
根据递归下降的原则完成C语言的语法分析其
"""
class Parser():
    def __init__(self,Lexer):
        self.Lexer=Lexer
        self.token_list=Lexer.token_list
        self.pos=0
    # 按顺序读取token
    def get_next_token(self):
        if self.pos > len(self.token_list)-1:
            return {'None':'EOF'}
        current_char=self.token_list[self.pos]
        self.pos+=1
        return current_char
    # 错误处理
    def error(self):
        raise Exception('invalid syntax')
    # 读取token
    def read_tokens(self):
        if self.get_next_token()!=
if __name__=='__main__':
    lexer=Lexer('test.c')
    parser=Parser(lexer)
    # print(lexer.token_list)
    print(parser.token_list)