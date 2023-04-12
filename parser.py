from lexer import Lexer
from utils import *
"""
根据递归下降的原则完成语法分析
"""
class Parser():
    def __init__(self,Lexer,filename='test.der'):
        self.Lexer=Lexer
        self.filename=filename
        self.source_code=""
        self.cur_token=""
        self.token_list=[]
        self.line_num=1
        self.var_map={}
    # get token
    def get_next_token(self,pos):
        if pos > len(self.tokens)-1:
            return {'None':'EOF'}
        current_char=self.tokens[pos]
        return current_char

    # read token flows
    def parse(self):
        tokens=[]
        pos=0
        with open(self.filename,'r') as f:
            self.source_code=f.readlines()
        for line in self.source_code:
            self.tokens=self.Lexer.tokenize(line)
            self.token_list.append(self.tokens)
            for token in self.tokens: 
                if 'COMMENT' in token:
                    pass
                elif 'KEY_WORD' in token:
                    self.parse_k_w(token,self.tokens)
                else:
                    pass
                pos+=1
            self.line_num+=1
                
    # judge if the variable is a local variable
    def is_local_id(self,token):
        pass
    # judge if the variable is defined
    def is_new_id(self,token):
        if token not in self.var_map:
            # 加入行数
            self.var_map[token]=self.line_num
            return True
        return False
    def parse_k_w(self,token,tokens):
        """
        KEY_WORDS := der | if | while | for | do | switch | return 
        der := ID
        if := ( condition ) { statement }
        while := ( condition ) { statement }
        for := ( der; condition ; statement) { statement }
        """
        value=token
        # if token is a variable
        key_word=token.get('KEY_WORD')
        if 'der' in key_word:
            self.parse_var(token)
        # if is 'if statement'
        elif value=='if':
            self.parse_if(token)
        # if is 'while statement'
        elif value=='while':
            pass
        # if is for statement
        elif value=='for':
            pass
        # if is 'do-while statement'
        elif value=='do':
            pass
        # if is switch statement
        elif value=='switch':
            pass
        # if is return statement
        elif value=='return':
            pass
    def parse_if(self,token):
        pass
    def parse_sep(self):
        pass
    def parse_var(self,token):
        pos=1
        token=self.get_next_token(pos)
        name=token.get('ID')
        # check if variable name is valid
        if name is None:
            error("wrong variable define",self.line_num)
        elif not self.is_new_id(name):
            error("duplicate declare",self,line_num)
        else:
            pos+=1
            token=self.get_next_token(pos)
            check_next_token(token,'=',self.line_num)
            pos+=1
            token=self.get_next_token(pos)
            # save the variable value
            if token.get('NUM')is not None:
                self.var_map[name]=token.get('NUM')
            elif token.get('STR') is not None:
                self.var_map[name]=token.get('STR')
    def parse_enum(self):
        pass
    def read_statement(self):
        pass
    def parse_expr(self):
        pass   

if __name__=='__main__':
    lexer=Lexer()
    parser=Parser(lexer)
    parser.parse()
    print("token_list如下所示")
    print(parser.token_list)
    print("变量表如下所示:")
    print(parser.var_map)