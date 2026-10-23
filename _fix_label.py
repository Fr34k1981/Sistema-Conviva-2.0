from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

alvo = '["Ocorrências anteriores:", str(ocorrencias_anteriores)]'
novo = '''[
                "Ocorrencias anteriores:",
                str(ocorrencias_anteriores)
            ]'''

if alvo not in texto:
    raise SystemExit("Nao achei a linha exata da tabela. Pare e me avise.")

texto2 = texto.replace(alvo, novo, 1)
path.write_text(texto2, encoding="utf-8")
print("ok: rotulo ajustado")
