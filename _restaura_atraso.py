from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

inicio = texto.find("        # ----------------------------------------------------\n        # REGISTRO DA SITUAÇÃO\n        # ----------------------------------------------------")
if inicio == -1:
    raise SystemExit("Nao achei o marcador REGISTRO DA SITUACAO dentro do atraso")

fim = texto.find("    # ========================================================\n    # MODELO GERAL\n    # ========================================================", inicio)
if fim == -1:
    raise SystemExit("Nao achei o marcador MODELO GERAL")

bloco_correto = r'''        # ----------------------------------------------------
        # REGISTRO DA SITUAÇÃO
        # ----------------------------------------------------

        adicionar_secao("REGISTRO DA SITUAÇÃO")

        tabela_atraso = Table(
            [
                [
                    "Horário Permitido",
                    "Horário de Chegada",
                    "Atrasos/Semana",
                    "Atrasos/Mês"
                ],
                [
                    horario_permitido or "07:00",
                    horario_chegada or "Não informado",
                    atrasos_semana,
                    atrasos_mes
                ]
            ],
            colWidths=[
                3.5 * cm,
                3.5 * cm,
                3.5 * cm,
                3.5 * cm
            ]
        )

        tabela_atraso.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                ("FONTNAME", (0, 0), (-1, 0), fonte_negrito),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ])
        )

        elementos.append(tabela_atraso)
        elementos.append(Spacer(1, 0.15 * cm))

        adicionar_paragrafo(
            "Justificativa apresentada: "
            + (justificativa_atraso if justificativa_atraso else "Não informada.")
        )

        # ----------------------------------------------------
        # ORIENTAÇÃO PEDAGÓGICA E IMPACTO
        # ----------------------------------------------------

        adicionar_secao("ORIENTAÇÃO PEDAGÓGICA E IMPACTO")

        adicionar_paragrafo(
            "A pontualidade é essencial para o desenvolvimento "
            "pedagógico e social do aluno. Atrasos recorrentes "
            "provocam a perda de conteúdos iniciais, interrompem "
            "a sequência didática e prejudicam o engajamento "
            "do estudante."
        )

        adicionar_paragrafo(
            "Solicitamos o apoio da família na organização dos "
            "horários para garantir o direito pleno à aprendizagem."
        )

        # ----------------------------------------------------
        # FUNDAMENTAÇÃO LEGAL E PROCEDIMENTOS
        # ----------------------------------------------------

        adicionar_secao("FUNDAMENTAÇÃO LEGAL E PROCEDIMENTOS")

        adicionar_paragrafo(
            "Conforme o ECA (Lei nº 8.069/1990) e a LDB "
            "(Lei nº 9.394/1996), é dever da família e da escola "
            "acompanhar a frequência, a pontualidade e o "
            "aproveitamento escolar do estudante."
        )

        adicionar_paragrafo(
            "• Registros internos: Todos os atrasos são arquivados "
            "no prontuário do aluno."
        )

        adicionar_paragrafo(
            "• Reincidência: Persistindo os atrasos, a família "
            "será convocada pela direção para definir um plano "
            "de acompanhamento."
        )

        adicionar_paragrafo(
            "• Medidas cabíveis: Caso o descumprimento permaneça "
            "e comprometa a rotina escolar, a escola adotará "
            "as providências previstas na legislação e nas "
            "normas da rede de ensino."
        )

        # ----------------------------------------------------
        # TERMO DE CIÊNCIA
        # ----------------------------------------------------

        adicionar_secao("TERMO DE CIÊNCIA")

        adicionar_paragrafo(
            "Este documento integra o acompanhamento escolar "
            "do estudante e busca fortalecer a parceria entre "
            "família e escola."
        )

        adicionar_paragrafo(
            "Data: ____ / ____ / ______"
        )

        elementos.append(Spacer(1, 0.35 * cm))

        assinaturas_atraso = Table(
            [
                [
                    "__________________________________",
                    "__________________________________"
                ],
                [
                    "Assinatura do Responsável",
                    "Assinatura do Representante da Escola"
                ]
            ],
            colWidths=[
                7.0 * cm,
                7.0 * cm
            ]
        )

        assinaturas_atraso.setStyle(
            TableStyle([
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 1), (-1, 1), fonte_normal),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ])
        )

        elementos.append(assinaturas_atraso)

    # ========================================================
    # MODELO: FORA DA SALA
    # ========================================================

    elif tipo_comunicado == "saida":

        adicionar_paragrafo(
            "Prezados pais e/ou responsáveis,"
        )

        adicionar_paragrafo(
            f"Informamos que o(a) estudante {nome}, "
            f"matriculado(a) no {turma}, foi registrado(a) "
            "pela escola por estar fora da sala de aula durante "
            "o horário letivo, sem autorização ou justificativa "
            "registrada."
        )

        adicionar_secao(
            "FUNDAMENTAÇÃO LEGAL E REGIMENTAL"
        )

        adicionar_paragrafo(
            "A Lei de Diretrizes e Bases da Educação Nacional — "
            "LDB (Lei nº 9.394/1996) estabelece a importância do "
            "cumprimento da carga horária escolar e da participação "
            "do estudante nas atividades pedagógicas."
        )

        adicionar_paragrafo(
            "O Estatuto da Criança e do Adolescente — ECA "
            "(Lei nº 8.069/1990) assegura o direito à educação "
            "e à permanência na escola, devendo a instituição "
            "promover condições de proteção e acompanhamento "
            "durante o período escolar."
        )

        adicionar_paragrafo(
            "As normas de convivência e o Regimento Escolar "
            "orientam a permanência do estudante nos espaços "
            "autorizados durante o horário letivo, respeitando "
            "a organização pedagógica e os procedimentos de "
            "segurança da unidade escolar."
        )

        adicionar_secao(
            "ORIENTAÇÃO À FAMÍLIA"
        )

        adicionar_paragrafo(
            "Solicitamos o apoio e a orientação da família para "
            "que o(a) estudante compreenda a importância de "
            "permanecer em sala durante o horário de aula, "
            "salvo quando houver autorização do professor ou "
            "da equipe responsável."
        )

        adicionar_paragrafo(
            "A permanência em sala contribui para o cumprimento "
            "da carga horária, para a continuidade das aprendizagens "
            "e para a segurança do próprio estudante e dos demais."
        )

        adicionar_secao(
            "TERMO DE CIÊNCIA — PERMANÊNCIA EM SALA DE AULA"
        )

        adicionar_paragrafo(
            f"Declaro que tomei ciência do comunicado referente "
            f"ao(à) estudante {nome}, da turma {turma}, sobre "
            "o registro de ausência da sala de aula durante "
            "o horário letivo, estando ciente das orientações "
            "apresentadas e comprometendo-me a orientar o(a) "
            "estudante quanto ao cumprimento das normas escolares."
        )

        elementos.append(Spacer(1, 0.25 * cm))

        termo = Table(
            [
                [
                    "Nome do Responsável:",
                    "____________________________________________"
                ],
                [
                    "Assinatura:",
                    "____________________________________________"
                ],
                [
                    "Data:",
                    "____/____/________"
                ]
            ],
            colWidths=[
                4.0 * cm,
                11.2 * cm
            ]
        )

        termo.setStyle(
            TableStyle([
                ("FONTNAME", (0, 0), (0, -1), fonte_negrito),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ])
        )

        elementos.append(termo)

'''

texto2 = texto[:inicio] + bloco_correto + texto[fim:]
path.write_text(texto2, encoding="utf-8")
print("ok: bloco atraso restaurado e modelo saida separado")
