import re
"""
单词包括关键字、标识符、运算符、分隔符（统称为操作符），以及数字和字符串（统称为变量），
词法分析就是将它们分析成语法分析容易分析的类型
"""
# 词法分析器，读取代码输入，并将它处理成可以给语法分析的格式
class Lexer():
    def __init__(self):
        # 关键字
        self.key_words=['dick', 'const',  'do','else', 'enum',  'for', 'if',  'return', 'fuck','switch', 
        'while']
        # 操作符
        self.operators=['+', '-', '*', '/', '%', '++', '--', '==', '!=', '<', '>', '<=', '>=',
        '&&', '||', '!', '&', '|', '^', '~', '<<', '>>', '=', '+=', '-=', '*=',
        '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', '->', '...',]
        # 分隔符
        self.separators=[';',',','(', ')',
        '[', ']', '{', '}','?','.','\\']
        # 标识符定义
        self.identifier_pattern='[a-zA-Z_][a-zA-Z0-9_]*'
        # 数字定义
        self.number_pattern='[0-9]+'
        # 字符串定义
        self.string_pattern='".*?"'
        # 两种注释定义
        self.comment_pattern='//.*|/\*[\s\S]*?\*/'
        self.source_code=""
        self.tokens=[]
    # 读取代码
    def tokenize(self,line):
        token_list=[]
        self.source_code=line
        # 定义匹配模式
        pattern='|'.join([self.string_pattern,self.identifier_pattern,self.number_pattern,self.comment_pattern]+list(map(re.escape, self.operators + self.separators)))
        self.tokens=re.findall(pattern, self.source_code)
        # 遍历单词列表
        for token in self.tokens:
            # 优先原则，匹配关键字
            if token in self.key_words:
                token_list.append({'KEY_WORD':token})
            # 匹配操作符
            elif token in self.operators:
                token_list.append({'OPER':token})
            # 匹配分隔符
            elif token in self.separators:
                token_list.append({'SEP':token})
            # 匹配字符串
            elif re.match(self.string_pattern, token):
                token_list.append({'STR':token})
            # 匹配标识符
            elif re.match(self.identifier_pattern, token):
                token_list.append({'ID':token})
            # 匹配数字
            elif re.match(self.number_pattern, token):
                token_list.append({'NUM':token})
            # 匹配注释
            elif re.match(self.comment_pattern, token):
                token_list.append({'COMMENT':token})
            else:
                print(f"错误的操作符{token}")
        return token_list
    # 输出词法分析之后的代码
    def get_next_token(self):
        if self.pos>len(token_list)-1:
            return {'EOF':None}
        current_char=token_list[self.pos]
        self.pos+=1
        return current_char
    
if __name__=='__main__':
    lexer=Lexer()
    
    