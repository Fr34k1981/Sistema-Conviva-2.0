import ast
import os
import re
import psycopg2

APP = "app.py"

print("=" * 80)
print("DIAGNOSTICO 2 — CODIGO x POSTGRESQL")
print("=" * 80)

# ------------------------------------------------------------
# 1. SINTAXE
# ------------------------------------------------------------
with open(APP, "r", encoding="utf-8") as f:
    texto = f.read()

try:
    arvore = ast.parse(texto, APP)
    print("\n[1] SINTAXE")
    print("OK - AST valida")
except Exception as e:
    print("\n[1] SINTAXE")
    print("ERRO:", e)
    raise SystemExit

# ------------------------------------------------------------
# 2. TABELAS CITADAS PELO MOTOR SUPABASE/POSTGRES
# ------------------------------------------------------------
tabelas = set()

padroes = [
    r'_supabase_request\(\s*["\'](?:GET|POST|PATCH|DELETE)["\']\s*,\s*["\']([^?"\']+)',
    r'_supabase_get_dataframe\(\s*["\']([^?"\']+)',
    r'_supabase_mutation\(\s*["\'](?:POST|PATCH|DELETE)["\']\s*,\s*["\']([^?"\']+)',
]

for padrao in padroes:
    for m in re.finditer(padrao, texto):
        valor = m.group(1).strip()

        if valor:
            valor = valor.split("?")[0].strip()
            valor = valor.replace("{", "").replace("}", "")

            if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", valor):
                tabelas.add(valor)

# SQL literal simples
for m in re.finditer(
    r'\b(?:FROM|JOIN|INTO|UPDATE|DELETE\s+FROM)\s+["\']?([A-Za-z_][A-Za-z0-9_]*)',
    texto,
    re.IGNORECASE
):
    tabelas.add(m.group(1))

print("\n[2] TABELAS ENCONTRADAS NO APP")
for t in sorted(tabelas):
    print(" -", t)

# ------------------------------------------------------------
# 3. BANCO LOCAL
# ------------------------------------------------------------
print("\n[3] TABELAS DO POSTGRESQL LOCAL")

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="supabase_local",
        user="postgres"
    )

    cur = conn.cursor()

    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """)

    banco = {row[0] for row in cur.fetchall()}

    for t in sorted(banco):
        print(" -", t)

except Exception as e:
    print("\nERRO AO ACESSAR POSTGRESQL:")
    print(e)
    raise SystemExit

# ------------------------------------------------------------
# 4. COMPARACAO
# ------------------------------------------------------------
faltantes = sorted(tabelas - banco)

print("\n[4] TABELAS DO APP QUE NAO EXISTEM NO BANCO")

if faltantes:
    for t in faltantes:
        print(" !!! FALTA:", t)
else:
    print("OK - Nenhuma tabela faltante encontrada.")

# ------------------------------------------------------------
# 5. COMUNICADO / TURNO
# ------------------------------------------------------------
print("\n[5] COMUNICADO / TURNO")

linhas = texto.splitlines()

termos_turno = [
    "identificar_turno_comunicado",
    "horario_padrao_por_turno_comunicado",
    "horario_padrao_aluno_comunicado",
    "horario_padrao_comunicado",
    "horario_permitido_comunicado",
    "horario_permitido",
    "turno_comunicado",
    "gerar_pdf_comunicado",
]

achados = set()

for i, linha in enumerate(linhas, start=1):
    if any(t in linha for t in termos_turno):
        inicio = max(1, i - 3)
        fim = min(len(linhas), i + 3)

        chave = (inicio, fim)

        if chave not in achados:
            achados.add(chave)

            print(f"\n--- linhas {inicio}-{fim} ---")

            for n in range(inicio, fim + 1):
                print(f"{n}: {linhas[n-1]}")

# ------------------------------------------------------------
# 6. TUTORIA RESPONSAVEIS
# ------------------------------------------------------------
print("\n[6] TUTORIA_RESPONSAVEIS")

for i, linha in enumerate(linhas, start=1):
    if "tutoria_responsaveis" in linha.lower():
        inicio = max(1, i - 4)
        fim = min(len(linhas), i + 4)

        print(f"\n--- linhas {inicio}-{fim} ---")

        for n in range(inicio, fim + 1):
            print(f"{n}: {linhas[n-1]}")

# ------------------------------------------------------------
# 7. SQL DE TUTORIA DISPONIVEL NO PROJETO
# ------------------------------------------------------------
print("\n[7] ARQUIVOS SQL DE TUTORIA")

for raiz, dirs, arquivos in os.walk("."):
    dirs[:] = [d for d in dirs if d not in {"__pycache__", ".git"}]

    for nome in arquivos:
        if nome.lower().endswith(".sql") and "tutoria" in nome.lower():
            caminho = os.path.join(raiz, nome)
            print(" -", caminho)

# ------------------------------------------------------------
# FINAL
# ------------------------------------------------------------
cur.close()
conn.close()

print("\n" + "=" * 80)
print("FIM DO DIAGNOSTICO 2")
print("NENHUM ARQUIVO FOI ALTERADO")
print("=" * 80)
