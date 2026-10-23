from pathlib import Path
import re

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

# Bloco atual que sobrescreve o modelo pela categoria da ocorrência
padrao = re.compile(
    r"tipo_comunicado\s*=\s*limpar\(modelo\)\.lower\(\)\s*"
    r"\n\s*if any\(termo in categoria_normalizada for termo in termos_atraso\):\s*"
    r"\n\s*tipo_comunicado\s*=\s*[\"']atraso[\"']\s*"
    r"\n\s*elif any\(termo in categoria_normalizada for termo in termos_saida\):\s*"
    r"\n\s*tipo_comunicado\s*=\s*[\"']saida[\"']",
    re.DOTALL,
)

novo = '''tipo_comunicado = limpar(modelo).lower()

    # Se o usuário escolheu um modelo explícito, respeita a escolha.
    # Só usa a categoria da ocorrência quando o modelo for geral/vazio.
    if tipo_comunicado in ("", "geral", "none", "nan"):
        if any(termo in categoria_normalizada for termo in termos_atraso):
            tipo_comunicado = "atraso"
        elif any(termo in categoria_normalizada for termo in termos_saida):
            tipo_comunicado = "saida"'''

texto2, n = padrao.subn(novo, texto, count=1)
print("alteracoes=%d" % n)

if n != 1:
    raise SystemExit("Nao achei o bloco de sobrescrita do modelo. Pare e me avise.")

path.write_text(texto2, encoding="utf-8")
print("ok: modelo do dropdown passa a ser respeitado")
