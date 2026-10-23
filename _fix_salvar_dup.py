from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
lines = path.read_text(encoding="utf-8").splitlines(keepends=True)

out = []
i = 0
removidos = 0
while i < len(lines):
    line = lines[i]
    # detecta início do botão Salvar atraso
    if 'st.button(' in line and i + 4 < len(lines):
        chunk = "".join(lines[i:i+8])
        if 'salvar_atraso_comunicado' in chunk or 'Salvar atraso' in chunk:
            removidos += 1
            depth = 0
            # pula até o fim do if st.button(...): bloco completo é mais complexo;
            # primeiro só remove o st.button(...) call; o corpo do if precisa ir junto
            # Estratégia: achar "if st.button(" com Salvar atraso e remover até o próximo
            # trecho no mesmo nível de indentação que não pertença ao if
            # Mais simples: marcar e processar depois
            pass

    out.append(line)
    i += 1

texto = "".join(lines)

# Conta quantas keys existem
print("keys=", texto.count('salvar_atraso_comunicado'))

# Remove TODOS os blocos if st.button Salvar atraso (do if até antes de linha menos indentada problemática)
# Abordagem prática: renomear keys para unicas e depois remover blocos extras por texto

parts = texto.split('key="salvar_atraso_comunicado"')
print("partes=", len(parts) - 1)

# Substitui todas as keys por unicas temporarias
n = 0
def trocar_key(s):
    global n
    n += 1
    return f'key="salvar_atraso_comunicado_{n}"'

import re
texto2, q = re.subn(r'key\s*=\s*["\']salvar_atraso_comunicado["\']', lambda m: trocar_key(m), texto)
print("keys_renomeadas=", q)

# Agora remove blocos extras do botão Salvar, mantendo só o primeiro
# Encontra todos os "if st.button(" que contenham Salvar atraso
padrao = re.compile(
    r'[ \t]*if st\.button\(\s*[^\)]*Salvar atraso[\s\S]*?key\s*=\s*["\']salvar_atraso_comunicado_\d+["\']\s*\)\s*:\s*'
    r'(?:\n(?:[ \t]{12,}|\t\t).*)*',
    re.MULTILINE,
)
blocos = list(padrao.finditer(texto2))
print("blocos_salvar=", len(blocos))

if len(blocos) >= 2:
    for b in reversed(blocos[1:]):
        texto2 = texto2[:b.start()] + texto2[b.end():]
    print("extras_removidos=", len(blocos) - 1)

# Normaliza a key restante para uma fixa
texto2 = re.sub(
    r'key\s*=\s*["\']salvar_atraso_comunicado_\d+["\']',
    'key="salvar_atraso_comunicado_unico"',
    texto2,
)

print("keys_final=", texto2.count('salvar_atraso_comunicado'))
path.write_text(texto2, encoding="utf-8")
print("ok")
