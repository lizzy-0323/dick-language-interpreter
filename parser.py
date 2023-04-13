from lexer import Lexer
"""
根据递归下降的原则完成语法分析
"""
class Parser():
    def __init__(self,Lexer,filename='test.dick'):
        self.Lexer=Lexer
        self.filename=filename
        self.source_code=""
        self.cur_token=None
        self.tokens=[]
        self.line_num=1
        self.var_map={}
        self.token_index=0
    def rewind_token_stream(self):
        # set the token stream position back by one
        self.token_index -= 1
        # ensure that the new current token is valid
        if self.token_index >= 0 and self.token_index < len(self.tokens):
            self.cur_token = self.tokens[self.token_index]
        else:
            self.cur_token = None   
    # get token
    def get_next_token(self):
        self.token_index+=1
        if self.token_index > len(self.tokens)-1:
            return {'None':'EOF'}
        self.cur_token=self.tokens[self.token_index]
        return self.cur_token
    
    # check if the current token is of a given type and raise an error if not
    def check_current_token_type(self, token_type):
        if self.cur_token.get(token_type) == None:
            self.error(f"Expected token type: {token_type} but got {self.cur_token}")
            
    # read token flows
    def parse(self):
        """
        global_decl = var_decl | func_decl | comment
        var_decl = dick id
        func_decl = fuck id ( param_decl ) { statement }
        param_decl = param: id
        statement = if_stmt | while_stmt | for_stmt| return_stmt | empty_stmt | normal_stmt 
        ------------------------
        if_stmt = if (expression){ statement }
        normal_stmt = expression
        id = expression
        """
        with open(self.filename,'r') as f:
            self.source_code=f.readlines()
        for line in self.source_code:
            self.tokens+=self.Lexer.tokenize(line)
        self.cur_token=self.tokens[0]
        self.parse_global_decl()
            # self.token_list.append(self.tokens)
            # for token in self.tokens: 
            #     if 'COMMENT' in token:
            #         pass
            #     elif 'KEY_WORD' in token:
            #         self.parse_k_w(token,self.tokens)
            #     elif 'SEP' in token:
            #         self.parse_sep(token)
            #     else:
            #         pass
            #     pos+=1
            # self.line_num+=1
            
    # parse global declarations
    def parse_global_decl(self):
        self.cur_token=self.tokens[self.token_index]
        while self.token_index<len(self.tokens):
            if self.cur_token.get('KEY_WORD') == 'dick':
                self.parse_var_decl()
            elif self.cur_token.get('KEY_WORD') == 'fuck':
                self.parse_func_decl()
            elif self.cur_token.get('COMMENT') is not None:
                self.get_next_token()
            else:
                self.error(f"Unexpected token: {self.cur_token}")
            
    # parse key word
    def parse_k_w(self,token,tokens):
        """
        KEY_WORDS := dick | if | while | for | do | return 
        dick := ID
        if := ( condition ) { statement }
        while := ( condition ) { statement }
        for := ( dick; condition ; statement) { statement }
        """
        value=token
        # if token is a variable
        key_word=token.get('KEY_WORD')
        if 'dick' in key_word:
            self.parse_var(token)
        # if token is a statement
        else:
            self.parse_stmt(token)
            
    # parse separater  
    def parse_sep(self,token):
        if(token=='{'):
            pass
        
    # report an error message containing the line number
    def error(self, message):
        raise Exception(f"Error on line {self.line_num}: {message}") 
      
    # parse variable
    def parse_var_decl(self):
        var_name=None
        var_value=None
        self.get_next_token()
        self.check_current_token_type('ID')
        var_name=self.cur_token['ID']
        
        # check if variable name is valid
        if not self.is_new_id(var_name):
            self.error(f"Variable '{var_name}' has already been declared")
    
        # get the equal token
        self.get_next_token()
        if self.cur_token.get('OPER')!='=':
            self.error(f"Expected '=' but got {self.cur_token}")
        self.get_next_token()
        
        # get the value
        var_value=self.cur_token
        if var_value.get('NUM'):
            self.var_map[var_name]=var_value.get('NUM')
        elif var_value.get('STR'):
            self.var_map[var_name]=var_value.get('STR')
        else:
            self.error(f"Unexpected token type for variable value: {self.cur_token}")
        self.get_next_token()
        
    # parse function
    def parse_func_decl(self):  
        func_name=None
        func_param=None
        self.get_next_token()
        self.check_current_token_type('ID')
        func_name=self.cur_token['ID']
        self.get_next_token()
        self.check_sep_token('(')
        self.get_next_token()
        # if the function have params
        if self.cur_token!={'SEP':')'}:
            func_param=self.cur_token['ID']
            self.get_next_token()
            self.check_sep_token(')')
        else:
            self.check_sep_token(')')
        self.get_next_token()
        self.check_sep_token('{')
        self.get_next_token()
        self.parse_stmt()
        
    # parse enum 
    def parse_enum(self):
        pass
    
    # parse statement
    def parse_stmt(self):
        if self.cur_token.get('KEY_WORD') == 'if':
            self.parse_if_stmt()
        elif self.cur_token.get('KEY_WORD') == 'while':
            self.parse_while_stmt()
        elif self.cur_token.get('KEY_WORD') == 'for':
            self.parse_for_stmt()
        elif self.cur_token.get('KEY_WORD') == 'return':
            self.parse_return_stmt()
        else:
            self.parse_normal_stmt()
        
    # parse expression
    def parse_expr(self):
        pass

    # parse if statement
    def parse_if_stmt(self):
        # check that the current token is "if"
        self.check_current_token_type('KEY_WORD')
        if self.cur_token['KEY_WORD'] != 'if':
            self.error(f"Expected KEY_WORD 'if' but got {self.cur_token}")
            
        # get the opening parenthesis of the condition expression
        self.get_next_token()
        self.check_sep_token('(')
            
        # parse the condition expression
        cond=self.parse_expr()
        
        # ensure that the condition expression is a boolean value
        if not isinstance(cond, bool):
            self.error(f"Expected boolean expression for 'if' statement condition")
        
        # get the closing parenthesis of the condition expression
        self.check_sep_token(')')

        # get the opening curly brace of the if statement body
        self.get_next_token()
        self.check_sep_token('{')

        # parse the if statement body
        self.parse_stmt()

        # get the closing curly brace of the if statement body
        self.check_sep_token('}')
        
        # check for "else" keyword
        self.get_next_token()
        if self.cur_token == {'KEY_WORD': 'else'}:
            # parse the else statement body
            self.get_next_token()
            if self.cur_token != {'OPER': '{'}:
                self.error(f"Expected OPER '{{' but got {self.cur_token}")
            self.parse_stmt()
            if self.cur_token != {'OPER': '}'}:
                self.error(f"Expected OPER '}}' but got {self.cur_token}")
        else:
            self.rewind_token_stream()
            
    # parse while statement
    def parse_while_stmt(self):
        pass

    # parse for statement
    def parse_for_stmt(self):
        pass

    # parse return statement
    def parse_return_stmt(self):
        pass
    
    # parse parameter
    def parse_param(self):
        pass
    
    # parse normal expression
    def parse_normal_stmt(self):
        pass
    
    # parse expression
    def parse_expr(self):
        self.parse_term()
        
        while self.cur_token.get('OPER') in ['+', '-']:
            op = self.cur_token['OPER']
            self.get_next_token()
            self.parse_term()

    # parse term
    def parse_term(self):
        self.parse_factor()

        while self.cur_token.get('OPER') in ['*', '/']:
            op = self.cur_token['OPER']
            self.get_next_token()
            self.parse_factor()

    # parse factor
    def parse_factor(self):
        if self.cur_token.get('NUM'):
            self.get_next_token()
        elif self.cur_token.get('ID'):
            self.get_next_token()
        elif self.cur_token.get('OPER') == '(':
            self.get_next_token()
            self.parse_expr()
            self.check_sep_token(')')
            self.get_next_token()
        else:
            self.error(f"Unexpected token: {self.cur_token}")
    # judge if the token is the expect token
    def check_sep_token(self,token):
        if self.cur_token.get('SEP')!=token:
            self.error(f"Expected '{token}', but got '{self.cur_token.get('SEP')}' ")
    # judge if the variable is a local variable
    def is_local_id(self,token):
        pass
    
    # judge if the variable is defined
    def is_new_id(self,token):
        if token not in self.var_map:
            # 加入行数
            self.var_map[token] = self.line_num
            return True
        return False
if __name__=='__main__':
    lexer=Lexer()
    parser=Parser(lexer)
    parser.parse()
    print("token_list如下所示")
    print(parser.tokens)
    print("变量表如下所示:")
    print(parser.var_map)
