import re
"""
在C语言中，单词包括关键字、标识符、运算符、分隔符（统称为操作符），以及数字和字符串（统称为变量），
词法分析就是将它们分析成语法分析容易分析的类型
"""
# 词法分析器，读取代码输入，并将它处理成可以给语法分析的格式
class Lexer():
    def __init__(self,filename='test.c'):
        # c语言关键字
        self.key_words=['auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
        'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if', 'int',
        'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
        'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile',
        'while',]
        # c语言操作符
        self.operators=['+', '-', '*', '/', '%', '++', '--', '==', '!=', '<', '>', '<=', '>=',
        '&&', '||', '!', '&', '|', '^', '~', '<<', '>>', '=', '+=', '-=', '*=',
        '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', '->', '...', ]
        # 分隔符
        self.separators=[';',',','(', ')',
        '[', ']', '{', '}','#','?','.','\\']
        # 标识符定义
        self.identifier_pattern='[a-zA-Z_][a-zA-Z0-9_]*'
        # 数字定义
        self.number_pattern='[0-9]+'
        # 字符串定义
        self.string_pattern='".*?"'
        # 两种注释定义
        self.comment_pattern='//.*|/\*[\s\S]*?\*/'
        self.filename=filename
        self.source_code=""
        self.tokens=[]
        self.token_list=[]
    def read_tokens(self):
        with open(self.filename,"r",encoding='utf-8') as f:
            self.source_code=f.read()
        # 定义匹配模式
        pattern='|'.join([self.string_pattern,self.identifier_pattern,self.number_pattern,self.comment_pattern]+list(map(re.escape, self.operators + self.separators)))
        self.tokens=re.findall(pattern, self.source_code)
        # 遍历单词列表
        for token in self.tokens:
            # 优先原则，匹配关键字
            if token in self.key_words:
                self.token_list.append({token:'KEY_WORD'})
            # 匹配操作符
            elif token in self.operators:
                self.token_list.append({token:'OPERATOR'})
            # 匹配分隔符
            elif token in self.separators:
                self.token_list.append({token:'SEPARATOR'})
            # 匹配字符串
            elif re.match(self.string_pattern, token):
                self.token_list.append({token:'STRING'})
            # 匹配标识符
            elif re.match(self.identifier_pattern, token):
                self.token_list.append({token:'IDENTIFIER'})
            # 匹配数字
            elif re.match(self.number_pattern, token):
                self.token_list.append({token:'NUMBER'})
            # 匹配注释
            elif re.match(self.comment_pattern, token):
                self.token_list.append({token:'COMMENT'})
            else:
                print(f"错误的操作符{token}")

if __name__=='__main__':
    lexer=Lexer('test.c')
    lexer.read_tokens()
    print(lexer.token_list)
    
    