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
        self.func_map={}
        self.token_index=0
        self.while_stack=[(-1,-1)]
    # reset to the last token
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
        self.token_index += 1
        if self.token_index > len(self.tokens)-1:
            return {'None':'EOF'}
        self.cur_token=self.tokens[self.token_index]
        return self.cur_token
    
    # check if the current token is of a given type and raise an error if not
    def check_current_token_type(self, token_type):
        if self.cur_token.get(token_type) == None:
            self.error(f"Expected token type: {token_type} but got {self.cur_token}")
    # change current token 
    def change_cur_token(self,token_index):
        self.token_index=token_index
        self.cur_token=self.tokens[token_index]
           
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
            
    # parse global declarations
    def parse_global_decl(self):
        self.cur_token=self.tokens[self.token_index]
        while self.token_index<len(self.tokens)-1:
            if self.cur_token.get('KEY_WORD') == 'dick':
                self.parse_var_decl()
            elif self.cur_token.get('KEY_WORD') == 'fuck':
                self.parse_func_decl()
            elif self.cur_token.get('COMMENT') is not None:
                self.get_next_token()
            else:
                self.error(f"Unexpected token: {self.cur_token}")
            
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
            # TODO:增加函数参数
            func_param=self.cur_token['ID']
            self.get_next_token()
            self.check_sep_token(')')
        else:
            self.check_sep_token(')')
        self.get_next_token()
        self.check_sep_token('{')
        self.get_next_token()
        self.parse_stmt()
        self.get_next_token()
        self.check_sep_token('}')
        
    # parse enum 
    def parse_enum(self):
        pass
    
    # parse statement
    """
    stmt = if_stmt | while_stmt | for_stmt| return_stmt | expression_stmt | empty_stmt
    if_stmt = if (expression){ statement }
    while_stmt = while (expression){ statement }
    return_stmt = return expression
    expression_stmt = expression
    empty_stmt
    """
    def parse_stmt(self):
        if self.cur_token.get('KEY_WORD') in ['if','else']:
            self.parse_if_stmt()
        elif self.cur_token.get('KEY_WORD') == 'while':
            self.parse_while_stmt()
        elif self.cur_token.get('KEY_WORD') == 'for':
            self.parse_for_stmt()
        elif self.cur_token.get('KEY_WORD') == 'return':
            self.parse_return_stmt()
        elif self.cur_token.get('KEY_WORD')=='break':
            self.parse_break_stmt() 
        elif self.cur_token.get('COMMENT'):
            self.parse_comment_stmt()
        elif self.cur_token.get('ID'):
            self.parse_expr_stmt()
        else:
            self.parse_empty_stmt()
            
    # parse if statement
    """
    if_stmt = if (expression){ statement } else { statement } | if (expression){ statement }
    stmt = if_stmt | while_stmt | for_stmt| return_stmt | expression_stmt | empty_stmt
    """
    def parse_if_stmt(self):
        # check that the current token is "if"
        self.check_current_token_type('KEY_WORD')
        if self.cur_token['KEY_WORD'] != 'if':
            self.error(f"Expected KEY_WORD 'if' but got {self.cur_token}")
            
        # get the opening parenthesis of the condition expression
        self.get_next_token()
        self.check_sep_token('(')
        self.get_next_token()
        
        # parse the condition expression
        cond=self.parse_cond()
        
        # ensure that the condition expression is a boolean value
        if not isinstance(cond, bool):
            self.error(f"Expected boolean expression for 'if' statement condition")
        
        # get the closing parenthesis of the condition expression
        self.check_sep_token(')')

        # get the opening curly brace of the if statement body
        self.get_next_token()
        self.check_sep_token('{')

        # choose which statement to execute based on the condition expression
        self.get_next_token()
        stmt_to_execute = self.parse_stmt() if cond else self.jump_token()

        # get the closing curly brace of the if statement body
        self.check_sep_token('}')

        # check for "else" keyword
        self.get_next_token()
        if self.cur_token == {'KEY_WORD': 'else'}:
            # parse the else statement body
            self.get_next_token()
            self.check_sep_token('{')
            # choose which statement to execute based on the condition expression
            self.get_next_token()
            stmt_to_execute = self.parse_stmt() if not cond else self.jump_token()
            # check for the closing curly brace of the else statement body
            self.check_sep_token('}')
        else:
            self.rewind_token_stream()
   
    # parse join
    """    
    join = join <= term | join >= term | join < term | join > term | join == term | join != term | term
    expr = expr + term | expr - term | term
    term = factor * factor | factor / factor | factor % factor | factor
    factor = num | str | id 
    """
    def parse_join(self):
        result=self.parse_expr()
        while self.cur_token.get('OPER') in ['<=','>=','<','>','==','!=']:
            op=self.cur_token['OPER']
            self.get_next_token()
            right=self.parse_expr()
            if op=='<=':
                result=result<=right
            elif op=='>=':
                result=result>=right
            elif op=='<':
                result=result<right
            elif op=='>':
                result=result>right
            elif op=='==':
                result=result==right
            elif op=='!=':
                result=result!=right
        return result
    
    # parse while statement
    """
    while_stmt = while (expression){ statement }
    """
    def parse_while_stmt(self):
        # save the while loop index,for 'break' statement
        start_token_index = self.token_index
        self.get_next_token()
        self.check_sep_token('(')
        self.get_next_token()
        # record the token index of the condition expression
        cond_token_index = self.token_index
        end_token_index = self.token_index
        cond=self.parse_cond()
        while(cond):
            self.check_sep_token(')')
            self.get_next_token()
            self.check_sep_token('{') 
            self.get_next_token()
            self.parse_stmt()
            self.get_next_token()
            self.check_sep_token('}')
            # change the end token index to the current token index,at the end of the loop
            end_token_index = self.token_index
            self.change_cur_token(cond_token_index)
            cond=self.parse_cond()
        self.while_stack.append((start_token_index,end_token_index))
        self.change_cur_token(end_token_index)
        
    # parse break statement
    def parse_break_stmt(self):
        # check if the current token is "break"
        start_index, end_index = None, None
        if len(self.while_stack) > 0:
            # find the innermost while loop
            for i in range(len(self.while_stack)-1, -1, -1):
                start_index, end_index = self.while_stack[i]
                if end_index is not None:
                    break
        if end_index is not None and start_index is not None:
            # if this is the first iteration of the loop and we encounter a break statement
            # set the end index to the current token index
            if start_index == end_index:
                end_index = self.token_index + 1
            self.change_cur_token(end_index)
        else:
            # ignore break statement outside of any loops
            self.get_next_token()

        
    # parse for statement
    def parse_for_stmt(self):
        pass
    
    # parse expression statement
    def parse_expr_stmt(self):
        variable=self.cur_token['ID']
        self.get_next_token()
        if self.cur_token.get('OPER')!='=':
            self.error(f"Expected '=' but got {self.cur_token}") 
        self.get_next_token()
        # process expression
        self.var_map[variable]=self.parse_expr()
        self.parse_stmt()
        
    # parse return statement
    def parse_return_stmt(self):
        pass
    
    # parse comment statement:
    def parse_comment_stmt(self):
        self.get_next_token()
        self.parse_stmt()
        
    # parse empty statement
    def parse_empty_stmt(self):
        pass
    
    # parse parameter
    def parse_param(self):
        pass
    
    # parse normal expression
    def parse_normal_stmt(self):
        pass
    
    # parse  condition
    """
    cond = cond || join | cond && join
    join = join <= term | join >= term | join < term | join > term | join == term | join != term | term
    expr = expr + term | expr - term | term
    term = factor * factor | factor / factor | factor % factor | factor
    factor = num | str | id 
    """
    def parse_cond(self):
        result=self.parse_join()
        while self.cur_token.get('OPER') in ['||','&&']:
            op=self.cur_token['OPER']
            self.get_next_token()
            right=self.parse_join()
            if op=='||':
                result=result or right
            elif op=='&&':
                result=result and right
        return result 
    # parse expression
    """
    expr = expr + term | expr - term | term
    term = term * factor | term / factor | factor
    factor = num | str | id 
    """
    def parse_expr(self):
        result=self.parse_term()
        
        while self.cur_token.get('OPER') in ['+', '-']:
            op = self.cur_token['OPER']
            self.get_next_token()
            right = self.parse_term()
            
            if op == '+':
                result += right
            elif op == '-':
                result -= right
        return result

    # parse term
    def parse_term(self):
        result=self.parse_factor()

        while self.cur_token.get('OPER') in ['*', '/']:
            op = self.cur_token['OPER']
            self.get_next_token()
            right = self.parse_factor()
            
            if op == '*':
                result *= right
            elif op == '/':
                result /= right
        
        return result

    # parse factor
    def parse_factor(self):
        token = self.cur_token

        if token.get('OPER') in ['-', '+', '!']:
            self.get_next_token()
            return -self.parse_factor() if token.get('OPER') == '-' else +self.parse_factor() if token.get('OPER') == '+' else not self.parse_factor()
        else:
            return self.parse_primary()

            
    # parse primary type
    def parse_primary(self):
        token=self.cur_token
        if token.get('NUM'):
            result = int(token['NUM'])
            self.get_next_token()
            return result
        elif token.get('ID'):
            result = token['ID']
            value=int(self.var_map.get(result))
            if value is None:
                self.error(f"Undefined variable '{var_name}'")
            self.get_next_token()
            return value
        elif token.get('KEY_WORD') in ['true','false']:
            self.get_next_token()
            return token.get('KEY_WORD')=='true'
        elif token.get('SEP') == '(':
            self.get_next_token()
            result = self.parse_expr()
            self.check_sep_token(')')
            self.get_next_token()
            return result
        else:
            self.error(f"Unexpected token: {token}")
            
    # judge if the token is the expect token
    def check_sep_token(self,token):
        if self.cur_token.get('SEP')!=token:
            self.error(f"Expected '{token}', but got '{next(iter(self.cur_token.values()))}' ")
            
    # jump the token until the token is the expect token
    def jump_token(self):
        brace_count=1
        while self.cur_token.get('SEP')!='}':
            self.get_next_token()
            if self.cur_token=={'SEP':'{'}:
                brace_count+=1
            elif self.cur_token=={'SEP':'}'}:
                brace_count-=1
        if brace_count!=0:
            self.error("Unmatched curly braces")
            
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
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("变量表如下所示:")
    print(parser.var_map)
