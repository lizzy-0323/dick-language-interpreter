# check if the next token is expect token 
def check_next_token(token,correct_token,line_num):
    if token.get('OPER')!=correct_token:
        error(f"except '{correct_token}', get{token}",line_num)     
# error handle
def error(err,line):
    raise Exception(f'In line {line}, {err}') 