from pathlib import Path
import re

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

# Troca o bloco dados_bilhete inteiro por versão estável
padrao = re.compile(
    r"dados_bilhete\s*=\s*\[\s*"
    r"\[\s*[\"']Nome:[\"']\s*,\s*nome\s*\]\s*,\s*"
    r"\[\s*[\"']RA:[\"']\s*,\s*ra\s*\+\s*[\"']\s+\|\s+Turma:\s+[\"']\s*\+\s*turma\s*\]\s*,\s*"
    r"\[[^\]]+\]\s*"
    r"\]",
    re.DOTALL,
)

novo = '''dados_bilhete = [
            [
                "Nome:",
                nome
            ],
            [
                "RA:",
                ra + "    |    Turma: " + turma
            ],
            [
                "Ocorrencias anteriores:",
                str(ocorrencias_anteriores)
            ]
        ]'''

texto2, n = padrao.subn(novo, texto, count=1)
print("blocos_alterados=%d" % n)

if n != 1:
    raise SystemExit("Nao encontrei o bloco dados_bilhete. Pare.")

path.write_text(texto2, encoding="utf-8")
print("ok")
