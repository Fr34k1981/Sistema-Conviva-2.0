from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

# A) No modo formulário em branco: enviar campos vazios + flag
old_branco = '''            aluno_data = {
                "nome": "________________________________",
                "ra": "____________________",
                "turma": "____________________",
                "total_ocorrencias": 0,
            }'''

new_branco = '''            aluno_data = {
                "nome": "",
                "ra": "",
                "turma": "",
                "total_ocorrencias": "",
                "formulario_branco": True,
            }
            ocorrencia_data["formulario_branco"] = True
            ocorrencia_data["horario_permitido"] = ""
            ocorrencia_data["horario_chegada"] = ""
            ocorrencia_data["justificativa"] = ""
            ocorrencia_data["atrasos_semana"] = ""
            ocorrencia_data["atrasos_mes"] = ""'''

if old_branco not in texto:
    raise SystemExit("Nao achei aluno_data do formulario em branco")
texto = texto.replace(old_branco, new_branco, 1)

# B) Nao forcar 07:00 quando for formulario em branco
old_hp = '''    horario_permitido = limpar(
        ocorrencia_data.get("horario_permitido")
        or ocorrencia_data.get("hora_permitida")
        or ocorrencia_data.get("horario_inicio")
        or "07:00"
    )'''

new_hp = '''    formulario_branco = bool(
        ocorrencia_data.get("formulario_branco")
        or aluno_data.get("formulario_branco")
    )

    horario_permitido = limpar(
        ocorrencia_data.get("horario_permitido")
        or ocorrencia_data.get("hora_permitida")
        or ocorrencia_data.get("horario_inicio")
        or ("" if formulario_branco else "07:00")
    )'''

if old_hp not in texto:
    raise SystemExit("Nao achei bloco horario_permitido")
texto = texto.replace(old_hp, new_hp, 1)

# C) Nao usar traco em atrasos quando em branco
old_at = '''    if not atrasos_semana or atrasos_semana == "0":
        atrasos_semana = "—"

    if not atrasos_mes or atrasos_mes == "0":
        atrasos_mes = "—"'''

new_at = '''    if formulario_branco:
        atrasos_semana = ""
        atrasos_mes = ""
    else:
        if not atrasos_semana or atrasos_semana == "0":
            atrasos_semana = "—"
        if not atrasos_mes or atrasos_mes == "0":
            atrasos_mes = "—"'''

if old_at not in texto:
    raise SystemExit("Nao achei bloco atrasos_semana/mes")
texto = texto.replace(old_at, new_at, 1)

# D) Tabela DADOS DO ESTUDANTE vazia no branco
old_dados = '''        dados_bilhete = [
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

new_dados = '''        if formulario_branco:
            dados_bilhete = [
                ["Nome:", ""],
                ["RA:", "                         |    Turma: "],
                ["Ocorrências anteriores:", ""],
            ]
        else:
            dados_bilhete = [
                [
                    "Nome:",
                    nome
                ],
                [
                    "RA:",
                    ra + "    |    Turma: " + turma
                ],
                [
                    "Ocorrências anteriores:",
                    str(ocorrencias_anteriores)
                ]
            ]'''

if old_dados not in texto:
    # tenta com Ocorrencias sem acento
    old_dados2 = old_dados.replace("Ocorrencias", "Ocorrências")
    if old_dados2 in texto:
        texto = texto.replace(old_dados2, new_dados, 1)
    else:
        raise SystemExit("Nao achei dados_bilhete do atraso")
else:
    texto = texto.replace(old_dados, new_dados, 1)

# E) Horarios vazios na tabela + justificativa sem texto padrao
old_tab = '''                [
                    horario_permitido or "07:00",
                    horario_chegada or "Não informado",
                    atrasos_semana,
                    atrasos_mes
                ]'''

new_tab = '''                [
                    "" if formulario_branco else (horario_permitido or "07:00"),
                    "" if formulario_branco else (horario_chegada or "Não informado"),
                    atrasos_semana,
                    atrasos_mes
                ]'''

if old_tab not in texto:
    raise SystemExit("Nao achei linha de valores da tabela atraso")
texto = texto.replace(old_tab, new_tab, 1)

old_just = '''        adicionar_paragrafo(
            "Justificativa apresentada: "
            + (justificativa_atraso if justificativa_atraso else "Não informada.")
        )'''

new_just = '''        if formulario_branco:
            adicionar_paragrafo("Justificativa apresentada: ")
        else:
            adicionar_paragrafo(
                "Justificativa apresentada: "
                + (justificativa_atraso if justificativa_atraso else "Não informada.")
            )'''

if old_just not in texto:
    raise SystemExit("Nao achei justificativa do atraso")
texto = texto.replace(old_just, new_just, 1)

path.write_text(texto, encoding="utf-8")
print("ok: pdf em branco com campos vazios")
