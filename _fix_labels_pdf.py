from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")
n = 0

# --- Labels quebrados na tela de atraso ---
subs = [
    ('"Hor?rio de chegada"', '"Horário de chegada"'),
    ('"Hor?rio permitido"', '"Horário permitido"'),
    ('"Atrasos no m?s"', '"Atrasos no mês"'),
    ("Atrasos no m?s", "Atrasos no mês"),
    ("Ex.: Transporte p?blico atrasado.", "Ex.: Transporte público atrasado."),
    ("placeholder=\"Ex.: Transporte p?blico atrasado.\"", 'placeholder="Ex.: Transporte público atrasado."'),
]

for old, new in subs:
    if old in texto:
        texto = texto.replace(old, new)
        n += 1
        print("fix_label:", old[:40])

# --- Garantir que PDF usa os contadores do formulario ---
# ja grava ocorrencia_data["atrasos_semana"] e ["atrasos_mes"]
# e total_atrasos_aluno; so garantir que zero real aparece como numero

old_pdf_at = '''    if formulario_branco:
        atrasos_semana = ""
        atrasos_mes = ""
    else:
        if not atrasos_semana or atrasos_semana == "0":
            atrasos_semana = "—"
        if not atrasos_mes or atrasos_mes == "0":
            atrasos_mes = "—"'''

new_pdf_at = '''    if formulario_branco:
        atrasos_semana = ""
        atrasos_mes = ""
    else:
        # Mantem o numero real (incluindo 0). Traco so se veio vazio.
        if atrasos_semana is None or str(atrasos_semana).strip() == "":
            atrasos_semana = "—"
        else:
            atrasos_semana = str(atrasos_semana)
        if atrasos_mes is None or str(atrasos_mes).strip() == "":
            atrasos_mes = "—"
        else:
            atrasos_mes = str(atrasos_mes)'''

if old_pdf_at in texto:
    texto = texto.replace(old_pdf_at, new_pdf_at, 1)
    n += 1
    print("fix_pdf_contadores")
else:
    # fallback: bloco antigo sem formulario_branco
    old2 = '''    if not atrasos_semana or atrasos_semana == "0":
        atrasos_semana = "—"

    if not atrasos_mes or atrasos_mes == "0":
        atrasos_mes = "—"'''
    new2 = '''    if formulario_branco if "formulario_branco" in dir() or "formulario_branco" in locals() else False:
        atrasos_semana = ""
        atrasos_mes = ""
    else:
        if atrasos_semana is None or str(atrasos_semana).strip() == "":
            atrasos_semana = "—"
        else:
            atrasos_semana = str(atrasos_semana)
        if atrasos_mes is None or str(atrasos_mes).strip() == "":
            atrasos_mes = "—"
        else:
            atrasos_mes = str(atrasos_mes)'''
    # melhor: detectar formulario_branco ja definido acima no arquivo
    new2 = '''    try:
        _fb = bool(formulario_branco)
    except Exception:
        _fb = bool(ocorrencia_data.get("formulario_branco") or aluno_data.get("formulario_branco"))
    if _fb:
        atrasos_semana = ""
        atrasos_mes = ""
    else:
        if atrasos_semana is None or str(atrasos_semana).strip() == "":
            atrasos_semana = "—"
        else:
            atrasos_semana = str(atrasos_semana)
        if atrasos_mes is None or str(atrasos_mes).strip() == "":
            atrasos_mes = "—"
        else:
            atrasos_mes = str(atrasos_mes)'''
    if old2 in texto:
        texto = texto.replace(old2, new2, 1)
        n += 1
        print("fix_pdf_contadores_fallback")
    else:
        print("AVISO: bloco pdf contadores nao encontrado (pode ja estar ok)")

path.write_text(texto, encoding="utf-8")
print("ok total_fixes=", n)
