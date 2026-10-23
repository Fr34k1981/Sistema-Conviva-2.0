from pathlib import Path
import re
from collections import Counter

texto = Path(r"C:\SistemaConviva\app.py").read_text(encoding="utf-8", errors="ignore")

# nomes definidos
defs = re.findall(r"(?m)^(?:async\s+)?def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", texto)
defs = sorted(set(defs))

# contagem de uso (nome aparece no arquivo)
uso = {}
for nome in defs:
    # total de ocorrencias do identificador
    total = len(re.findall(rf"\b{re.escape(nome)}\b", texto))
    # desconta a propria definicao (aprox. 1)
    refs = max(total - 1, 0)
    uso[nome] = refs

# ordena: menos usadas primeiro
ordenadas = sorted(uso.items(), key=lambda x: (x[1], x[0]))

print(f"Total de funcoes: {len(defs)}\n")
print("=== Candidatas a pouco uso / mortas (0-2 referencias) ===")
mortas = [(n, c) for n, c in ordenadas if c <= 2]
for n, c in mortas[:80]:
    print(f"{c:4d}  {n}")

print(f"\nTotal com <=2 refs: {len(mortas)}")

# salva relatorio
out = Path(r"C:\SistemaConviva\data\relatorio_funcoes_uso.txt")
out.parent.mkdir(parents=True, exist_ok=True)
linhas = [f"{c}\t{n}" for n, c in ordenadas]
out.write_text("refs\tnome\n" + "\n".join(linhas), encoding="utf-8")
print(f"\nRelatorio salvo em: {out}")
