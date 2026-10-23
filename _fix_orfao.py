from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
lines = path.read_text(encoding="utf-8").splitlines(keepends=True)

# Remove o bloco orfao que comeca em:
# data_reg = data_atraso_comunicado.strftime(...)  (sem indentacao correta)
# ate o except Exception do segundo salvar

out = []
i = 0
removidos = 0
while i < len(lines):
    raw = lines[i]
    stripped = raw.lstrip()

    # detecta inicio do bloco orfao
    if stripped.startswith('data_reg = data_atraso_comunicado.strftime') and not raw.startswith(' '):
        # pula ate depois do except/st.error correspondente
        removidos += 1
        i += 1
        while i < len(lines):
            s = lines[i].lstrip()
            # fim do bloco orfao: linha em branco apos o except error
            if s.startswith('st.error(f"❌ Erro ao salvar atraso:') or s.startswith("st.error(f\"❌ Erro ao salvar atraso:"):
                i += 1
                # pula linhas em branco seguintes uma vez
                while i < len(lines) and lines[i].strip() == "":
                    i += 1
                break
            i += 1
        continue

    out.append(raw)
    i += 1

texto = "".join(out)

# Conferencias
print("salvar_keys=", texto.count("salvar_atraso_comunicado"))
print("Salvar atraso texto=", texto.count("Salvar atraso"))
print("data_reg orfao=", sum(1 for l in texto.splitlines() if l.startswith("data_reg = data_atraso_comunicado")))

path.write_text(texto, encoding="utf-8")
print("ok: bloco orfao removido")
