import ast
lines = open('C:/SistemaConviva/app.py', encoding='utf-8', errors='ignore').readlines()
try:
    ast.parse(''.join(lines))
    print('SINTAXE OK!')
except SyntaxError as e:
    print(f'ERRO LINHA {e.lineno}: {e.msg}')
    print('CONTEUDO:', repr(lines[e.lineno-1]))
