import psycopg2
import re

conn = psycopg2.connect(
    host="127.0.0.1", port=5432, dbname="sistema_escolar",
    user="escola_admin", password=""
)
cur = conn.cursor()
cur.execute("DELETE FROM grade_horaria WHERE turno = %s AND ano_letivo = %s", ("Turno 1", 2026))

def fmt_nome(nome: str) -> str:
    nome = (nome or "").strip()
    if not nome:
        return nome
    partes = re.split(r"(\s+)", nome)
    out = []
    for p in partes:
        if p.isspace():
            out.append(p)
            continue
        # iniciais tipo P. ou O.E.
        if re.fullmatch(r"[A-Za-z]\.", p):
            out.append(p[0].upper() + ".")
            continue
        if re.fullmatch(r"[A-Za-z](\.[A-Za-z])+\.?", p):
            out.append(p.upper())
            continue
        out.append(p[:1].upper() + p[1:].lower())
    return "".join(out)

RAW = r'''
📅 SEGUNDA-FEIRA
🔹 6° Ano A
* 1ª Aula: LP - Rosangela
* 2ª Aula: LP - Rosangela
* 3ª Aula: INGLES - LUCINEIDE
* 4ª Aula: INGLES - LUCINEIDE
* 5ª Aula: HIST - Rosemeire
* 6ª Aula: MAT - Veronica
* 7ª Aula: MAT - Veronica
🔹 6° Ano B
* 1ª Aula: INGLES - LUCINEIDE
* 2ª Aula: INGLES - LUCINEIDE
* 3ª Aula: LP - Rosangela
* 4ª Aula: LP - Rosangela
* 5ª Aula: MAT - Veronica
* 6ª Aula: O.E. MAT - Jaqueline
* 7ª Aula: ARTE - Elaine
🔹 7° Ano A
* 1ª Aula: MAT - Veronica
* 2ª Aula: MAT - Veronica
* 3ª Aula: HIST - Rosemeire
* 4ª Aula: HIST - Rosemeire
* 5ª Aula: REDAÇÃO - Rosangela
* 6ª Aula: REDAÇÃO - Rosangela
* 7ª Aula: O.E. MAT - Jaqueline
🔹 7° Ano C
* 1ª Aula: LP - Rosemeire
* 2ª Aula: LP - Rosemeire
* 3ª Aula: MAT - Veronica
* 4ª Aula: TEC - FERNANDA
* 5ª Aula: TEC - FERNANDA
* 6ª Aula: GEO - SOLANGE
* 7ª Aula: GEO - SOLANGE
🔹 8° Ano A
* 1ª Aula: LP - PATRICIA
* 2ª Aula: LP - PATRICIA
* 3ª Aula: GEO - Geovana P.
* 4ª Aula: GEO - Geovana P.
* 5ª Aula: MAT - Jaqueline
* 6ª Aula: CIENCIAS - FERNANDA
* 7ª Aula: CIENCIAS - FERNANDA
🔹 8° Ano B
* 1ª Aula: GEO - Geovana P.
* 2ª Aula: GEO - Geovana P.
* 3ª Aula: MAT - Jaqueline
* 4ª Aula: LP - PATRICIA
* 5ª Aula: LP - PATRICIA
* 6ª Aula: CIENCIAS - FAGNA
* 7ª Aula: O.E.MAT. - SILVANA
🔹 8° Ano C
* 1ª Aula: MAT - Jaqueline
* 2ª Aula: MAT - Jaqueline
* 3ª Aula: CIENCIAS - FAGNA
* 4ª Aula: ED.FIN. - IGOR
* 5ª Aula: CIENCIAS - FAGNA
* 6ª Aula: LP - PATRICIA
* 7ª Aula: LP - PATRICIA
🔹 9° Ano A
* 1ª Aula: ARTE - Elaine
* 2ª Aula: LP - ITATIARA
* 3ª Aula: LP - ITATIARA
* 4ª Aula: MAT - SILVANA
* 5ª Aula: O.E. MAT. - IGOR
* 6ª Aula: INGLES - LUCINEIDE
* 7ª Aula: INGLES - LUCINEIDE
🔹 9° Ano B
* 1ª Aula: CIENCIAS - FAGNA
* 2ª Aula: CIENCIAS - FAGNA
* 3ª Aula: O.E.LP - Elaine
* 4ª Aula: O.E.LP - Elaine
* 5ª Aula: MAT - SILVANA
* 6ª Aula: LP - ITATIARA
* 7ª Aula: LP - ITATIARA
🔹 9° Ano C
* 1ª Aula: HISTÓRIA - SHIRLEY
* 2ª Aula: ARTE - Elaine
* 3ª Aula: O.E. MAT. - IGOR
* 4ª Aula: LP - ITATIARA
* 5ª Aula: LP - ITATIARA
* 6ª Aula: E.F. - Guilherme
* 7ª Aula: E.F. - Guilherme
🔹 3° A-TEC
* 1ª Aula: MAT - IGOR
* 2ª Aula: MAT - IGOR
* 3ª Aula: PROJ. MUL - ALNEI
* 4ª Aula: PROJ. MUL - ALNEI
* 5ª Aula: E.F. - Guilherme
* 6ª Aula: INOV - AMANDA
* 7ª Aula: INOV - AMANDA
🔹 3° B-TEC
* 1ª Aula: PROJ. MUL - ALNEI
* 2ª Aula: PROJ. MUL - ALNEI
* 3ª Aula: C. EMP - AMANDA
* 4ª Aula: C. EMP - AMANDA
* 5ª Aula: G.OP - Anderson
* 6ª Aula: FÍSICA - IGOR
* 7ª Aula: FÍSICA - IGOR
📅 TERÇA-FEIRA
🔹 6° Ano A
* 1ª Aula: TEC - FERNANDA
* 2ª Aula: TEC - FERNANDA
* 3ª Aula: MAT - Veronica
* 4ª Aula: E.F. - Guilherme
* 5ª Aula: E.F. - Guilherme
* 6ª Aula: GEO - SOLANGE
* 7ª Aula: GEO - SOLANGE
🔹 6° Ano B
* 1ª Aula: O.E. LP - ITATIARA
* 2ª Aula: O.E. LP - ITATIARA
* 3ª Aula: TEC - FERNANDA
* 4ª Aula: TEC - FERNANDA
* 5ª Aula: GEO - SOLANGE
* 6ª Aula: MAT - Veronica
* 7ª Aula: MAT - Veronica
🔹 7° Ano A
* 1ª Aula: LP - Elaine
* 2ª Aula: LP - Elaine
* 3ª Aula: INGLES - LUCINEIDE
* 4ª Aula: INGLES - LUCINEIDE
* 5ª Aula: HIST - Rosemeire
* 6ª Aula: TEC - FERNANDA
* 7ª Aula: TEC - FERNANDA
🔹 7° Ano C
* 1ª Aula: REDAÇÃO - Rosangela
* 2ª Aula: REDAÇÃO - Rosangela
* 3ª Aula: HIST - Rosemeire
* 4ª Aula: ED.FIN. - IGOR
* 5ª Aula: MAT - Veronica
* 6ª Aula: ARTE - Elaine
* 7ª Aula: ARTE - Elaine
🔹 8° Ano A
* 1ª Aula: HISTÓRIA - SHIRLEY
* 2ª Aula: HISTÓRIA - SHIRLEY
* 3ª Aula: MAT - Jaqueline
* 4ª Aula: P. V. - SOLANGE
* 5ª Aula: LP - PATRICIA
* 6ª Aula: INGLES - LUCINEIDE
* 7ª Aula: INGLES - LUCINEIDE
🔹 8° Ano B
* 1ª Aula: MAT - Jaqueline
* 2ª Aula: MAT - Jaqueline
* 3ª Aula: HISTÓRIA - SHIRLEY
* 4ª Aula: HISTÓRIA - SHIRLEY
* 5ª Aula: GEO - Geovana P.
* 6ª Aula: ED.FIN. - IGOR
* 7ª Aula: ED.FIN. - IGOR
🔹 8° Ano C
* 1ª Aula: GEO - Geovana P.
* 2ª Aula: GEO - Geovana P.
* 3ª Aula: O.E.MAT. - SILVANA
* 4ª Aula: MAT - Jaqueline
* 5ª Aula: MAT - Jaqueline
* 6ª Aula: HISTÓRIA - SHIRLEY
* 7ª Aula: HISTÓRIA - SHIRLEY
🔹 9° Ano A
* 1ª Aula: E.F. - Guilherme
* 2ª Aula: E.F. - Guilherme
* 3ª Aula: REDAÇÃO - Rosangela
* 4ª Aula: REDAÇÃO - Rosangela
* 5ª Aula: O.E. MAT. - IGOR
* 6ª Aula: CIENCIAS - FAGNA
* 7ª Aula: CIENCIAS - FAGNA
🔹 9° Ano B
* 1ª Aula: MAT - SILVANA
* 2ª Aula: MAT - SILVANA
* 3ª Aula: GEO - Geovana P.
* 4ª Aula: GEO - Geovana P.
* 5ª Aula: HISTÓRIA - SHIRLEY
* 6ª Aula: E.F. - Guilherme
* 7ª Aula: E.F. - Guilherme
🔹 9° Ano C
* 1ª Aula: CIENCIAS - FAGNA
* 2ª Aula: CIENCIAS - FAGNA
* 3ª Aula: O.E. MAT. - IGOR
* 4ª Aula: MAT - SILVANA
* 5ª Aula: MAT - SILVANA
* 6ª Aula: REDAÇÃO - Rosangela
* 7ª Aula: REDAÇÃO - Rosangela
🔹 3° A-TEC
* 1ª Aula: L P - LUCINEIDE
* 2ª Aula: L P - LUCINEIDE
* 3ª Aula: REDAÇÃO - FAGNA
* 4ª Aula: REDAÇÃO - FAGNA
* 5ª Aula: INOV - AMANDA
* 6ª Aula: G.FIN - Anderson
* 7ª Aula: G.FIN - Anderson
🔹 3° B-TEC
* 1ª Aula: LP - PATRICIA
* 2ª Aula: LP - PATRICIA
* 3ª Aula: E.F. - Guilherme
* 4ª Aula: G.FIN - Anderson
* 5ª Aula: G.FIN - Anderson
* 6ª Aula: INOV - AMANDA
* 7ª Aula: INOV - AMANDA
📅 QUARTA-FEIRA
🔹 6° Ano A
* 1ª Aula: ARTE - Elaine
* 2ª Aula: ARTE - Elaine
* 3ª Aula: LP - Rosangela
* 4ª Aula: LP - Rosangela
* 5ª Aula: CIENCIAS - FERNANDA
* 6ª Aula: ELETIVA - PATRICIA
* 7ª Aula: ELETIVA - PATRICIA
🔹 6° Ano B
* 1ª Aula: LP - Rosangela
* 2ª Aula: LP - Rosangela
* 3ª Aula: E.F. - Guilherme
* 4ª Aula: E.F. - Guilherme
* 5ª Aula: ARTE - Elaine
* 6ª Aula: ELETIVA - Geovana P.
* 7ª Aula: ELETIVA - Geovana P.
🔹 7° Ano A
* 1ª Aula: CIENCIAS - FERNANDA
* 2ª Aula: GEO - SOLANGE
* 3ª Aula: ARTE - Elaine
* 4ª Aula: ARTE - Elaine
* 5ª Aula: P. V. - Geovana P.
* 6ª Aula: ELETIVA - Veronica
* 7ª Aula: ELETIVA - Veronica
🔹 7° Ano C
* 1ª Aula: MAT - Veronica
* 2ª Aula: CIENCIAS - FERNANDA
* 3ª Aula: GEO - SOLANGE
* 4ª Aula: P. V. - Geovana P.
* 5ª Aula: O.E. MAT - Jaqueline
* 6ª Aula: ELETIVA - Rosemeire
* 7ª Aula: ELETIVA - Rosemeire
🔹 8° Ano A
* 1ª Aula: REDAÇÃO - Rosemeire
* 2ª Aula: REDAÇÃO - Rosemeire
* 3ª Aula: MAT - Jaqueline
* 4ª Aula: MAT - Jaqueline
* 5ª Aula: ED.FIN. - IGOR
* 6ª Aula: ELETIVA - SOLANGE
* 7ª Aula: ELETIVA - SOLANGE
🔹 8° Ano B
* 1ª Aula: LP - PATRICIA
* 2ª Aula: LP - PATRICIA
* 3ª Aula: REDAÇÃO - Rosemeire
* 4ª Aula: REDAÇÃO - Rosemeire
* 5ª Aula: CIENCIAS - FAGNA
* 6ª Aula: ELETIVA - SILVANA
* 7ª Aula: ELETIVA - SILVANA
🔹 8° Ano C
* 1ª Aula: MAT - Jaqueline
* 2ª Aula: INGLES - LUCINEIDE
* 3ª Aula: INGLES - LUCINEIDE
* 4ª Aula: LP - PATRICIA
* 5ª Aula: LP - PATRICIA
* 6ª Aula: ELETIVA - FERNANDA
* 7ª Aula: ELETIVA - FERNANDA
🔹 9° Ano A
* 1ª Aula: HISTÓRIA - SHIRLEY
* 2ª Aula: HISTÓRIA - SHIRLEY
* 3ª Aula: GEO - Geovana P.
* 4ª Aula: TEC - SILVANA
* 5ª Aula: TEC - SILVANA
* 6ª Aula: ELETIVA - Rosangela
* 7ª Aula: ELETIVA - Rosangela
🔹 9° Ano B
* 1ª Aula: LP - ITATIARA
* 2ª Aula: LP - ITATIARA
* 3ª Aula: MAT - SILVANA
* 4ª Aula: INGLES - LUCINEIDE
* 5ª Aula: INGLES - LUCINEIDE
* 6ª Aula: ELETIVA - SHIRLEY
* 7ª Aula: ELETIVA - SHIRLEY
🔹 9° Ano C
* 1ª Aula: TEC - SILVANA
* 2ª Aula: TEC - SILVANA
* 3ª Aula: HISTÓRIA - SHIRLEY
* 4ª Aula: HISTÓRIA - SHIRLEY
* 5ª Aula: P. V. - SOLANGE
* 6ª Aula: ELETIVA - Guilherme
* 7ª Aula: ELETIVA - Guilherme
🔹 3° A-TEC
* 1ª Aula: FÍSICA - IGOR
* 2ª Aula: FÍSICA - IGOR
* 3ª Aula: COM. - Ana Paula
* 4ª Aula: PROJ. MUL - ALNEI
* 5ª Aula: G.OP - Anderson
* 6ª Aula: G.OP - Anderson
* 7ª Aula: L P - LUCINEIDE
🔹 3° B-TEC
* 1ª Aula: MARKE. - Ana Paula
* 2ª Aula: MARKE. - Ana Paula
* 3ª Aula: MAT - IGOR
* 4ª Aula: MAT - IGOR
* 5ª Aula: PROJ. MUL - ALNEI
* 6ª Aula: REDAÇÃO - FAGNA
* 7ª Aula: REDAÇÃO - FAGNA
📅 QUINTA-FEIRA
🔹 6° Ano A
* 1ª Aula: HIST - Rosemeire
* 2ª Aula: HIST - Rosemeire
* 3ª Aula: REDAÇÃO - Rosangela
* 4ª Aula: REDAÇÃO - Rosangela
* 5ª Aula: GEO - SOLANGE
* 6ª Aula: MAT - Veronica
* 7ª Aula: MAT - Veronica
🔹 6° Ano B
* 1ª Aula: CIENCIAS - FERNANDA
* 2ª Aula: REDAÇÃO - Rosangela
* 3ª Aula: HIST - Rosemeire
* 4ª Aula: MAT - Veronica
* 5ª Aula: MAT - Veronica
* 6ª Aula: GEO - SOLANGE
* 7ª Aula: O.E. MAT - Jaqueline
🔹 7° Ano A
* 1ª Aula: REDAÇÃO - Rosangela
* 2ª Aula: GEO - SOLANGE
* 3ª Aula: MAT - Veronica
* 4ª Aula: LP - Elaine
* 5ª Aula: LP - Elaine
* 6ª Aula: CIENCIAS - FERNANDA
* 7ª Aula: CIENCIAS - FERNANDA
🔹 7° Ano C
* 1ª Aula: MAT - Veronica
* 2ª Aula: MAT - Veronica
* 3ª Aula: CIENCIAS - FERNANDA
* 4ª Aula: CIENCIAS - FERNANDA
* 5ª Aula: LP - Rosemeire
* 6ª Aula: LP - Rosemeire
* 7ª Aula: ED.FIN. - IGOR
🔹 8° Ano A
* 1ª Aula: HISTÓRIA - SHIRLEY
* 2ª Aula: E.F. - Guilherme
* 3ª Aula: E.F. - Guilherme
* 4ª Aula: TEC - Jaqueline
* 5ª Aula: TEC - Jaqueline
* 6ª Aula: ED.FIN. - IGOR
* 7ª Aula: LP - PATRICIA
🔹 8° Ano B
* 1ª Aula: TEC - Jaqueline
* 2ª Aula: TEC - Jaqueline
* 3ª Aula: HISTÓRIA - SHIRLEY
* 4ª Aula: CIENCIAS - FAGNA
* 5ª Aula: CIENCIAS - FAGNA
* 6ª Aula: E.F. - Guilherme
* 7ª Aula: E.F. - Guilherme
🔹 8° Ano C
* 1ª Aula: ED.FIN. - IGOR
* 2ª Aula: HISTÓRIA - SHIRLEY
* 3ª Aula: TEC - Jaqueline
* 4ª Aula: E.F. - Guilherme
* 5ª Aula: E.F. - Guilherme
* 6ª Aula: CIENCIAS - FAGNA
* 7ª Aula: CIENCIAS - FAGNA
🔹 9° Ano A
* 1ª Aula: O.E.LP - Elaine
* 2ª Aula: O.E.LP - Elaine
* 3ª Aula: P. V. - SOLANGE
* 4ª Aula: MAT - SILVANA
* 5ª Aula: MAT - SILVANA
* 6ª Aula: LP - ITATIARA
* 7ª Aula: LP - ITATIARA
🔹 9° Ano B
* 1ª Aula: CIENCIAS - FAGNA
* 2ª Aula: CIENCIAS - FAGNA
* 3ª Aula: MAT - SILVANA
* 4ª Aula: HISTÓRIA - SHIRLEY
* 5ª Aula: HISTÓRIA - SHIRLEY
* 6ª Aula: REDAÇÃO - Rosangela
* 7ª Aula: REDAÇÃO - Rosangela
🔹 9° Ano C
* 1ª Aula: INGLES - LUCINEIDE
* 2ª Aula: INGLES - LUCINEIDE
* 3ª Aula: GEO - Geovana P.
* 4ª Aula: LP - ITATIARA
* 5ª Aula: LP - ITATIARA
* 6ª Aula: MAT - SILVANA
* 7ª Aula: MAT - SILVANA
🔹 3° A-TEC
* 1ª Aula: P. V. - SOLANGE
* 2ª Aula: COM. - Ana Paula
* 3ª Aula: COM. - Ana Paula
* 4ª Aula: MARK - Ana Paula
* 5ª Aula: G.FIN - Anderson
* 6ª Aula: HISTÓRIA - SHIRLEY
* 7ª Aula: HISTÓRIA - SHIRLEY
🔹 3° B-TEC
* 1ª Aula: MARKE. - Ana Paula
* 2ª Aula: MAT - IGOR
* 3ª Aula: MAT - IGOR
* 4ª Aula: G.FIN - Anderson
* 5ª Aula: LP - PATRICIA
* 6ª Aula: G.OP - Anderson
* 7ª Aula: P. V. - SOLANGE
📅 SEXTA-FEIRA
🔹 6° Ano A
* 1ª Aula: O.E. LP - PATRICIA
* 2ª Aula: CIENCIAS - FERNANDA
* 3ª Aula: CIENCIAS - FERNANDA
* 4ª Aula: P. V. - Guilherme
* 5ª Aula: O.E. LP - PATRICIA
* 6ª Aula: O.E. MAT - Jaqueline
* 7ª Aula: O.E. MAT - Jaqueline
🔹 6° Ano B
* 1ª Aula: CIENCIAS - FERNANDA
* 2ª Aula: HIST - Rosemeire
* 3ª Aula: REDAÇÃO - Rosangela
* 4ª Aula: GEO - SOLANGE
* 5ª Aula: CIENCIAS - FERNANDA
* 6ª Aula: P. V. - Guilherme
* 7ª Aula: HIST - Rosemeire
🔹 7° Ano A
* 1ª Aula: E.F. - Guilherme
* 2ª Aula: O.E. LP - PATRICIA
* 3ª Aula: MAT - Veronica
* 4ª Aula: MAT - Veronica
* 5ª Aula: E.F. - Guilherme
* 6ª Aula: ED.FIN. - IGOR
* 7ª Aula: ED.FIN. - IGOR
🔹 7° Ano C
* 1ª Aula: HIST - Rosemeire
* 2ª Aula: E.F. - Guilherme
* 3ª Aula: E.F. - Guilherme
* 4ª Aula: O.E. LP - PATRICIA
* 5ª Aula: HIST - Rosemeire
* 6ª Aula: INGLES - LUCINEIDE
* 7ª Aula: INGLES - LUCINEIDE
🔹 8° Ano A
* 1ª Aula: O.E.MAT. - SILVANA
* 2ª Aula: O.E. LP - ITATIARA
* 3ª Aula: ARTE - Elaine
* 4ª Aula: MAT - Jaqueline
* 5ª Aula: GEO - Geovana P.
* 6ª Aula: CIENCIAS - FERNANDA
* 7ª Aula: CIENCIAS - FERNANDA
🔹 8° Ano B
* 1ª Aula: ARTE - Elaine
* 2ª Aula: MAT - Jaqueline
* 3ª Aula: MAT - Jaqueline
* 4ª Aula: INGLES - LUCINEIDE
* 5ª Aula: INGLES - LUCINEIDE
* 6ª Aula: P. V. - SOLANGE
* 7ª Aula: O.E. LP - ITATIARA
🔹 8° Ano C
* 1ª Aula: P. V. - SOLANGE
* 2ª Aula: ARTE - Elaine
* 3ª Aula: REDAÇÃO - Rosemeire
* 4ª Aula: REDAÇÃO - Rosemeire
* 5ª Aula: TEC - Jaqueline
* 6ª Aula: O.E. LP - ITATIARA
* 7ª Aula: GEO - Geovana P.
🔹 9° Ano A
* 1ª Aula: GEO - Geovana P.
* 2ª Aula: GEO - Geovana P.
* 3ª Aula: HISTÓRIA - SHIRLEY
* 4ª Aula: CIENCIAS - FAGNA
* 5ª Aula: CIENCIAS - FAGNA
* 6ª Aula: MAT - SILVANA
* 7ª Aula: MAT - SILVANA
🔹 9° Ano B
* 1ª Aula: O.E. MAT. - IGOR
* 2ª Aula: O.E. MAT. - IGOR
* 3ª Aula: TEC - SILVANA
* 4ª Aula: TEC - SILVANA
* 5ª Aula: ARTE - Elaine
* 6ª Aula: GEO - Geovana P.
* 7ª Aula: P. V. - SOLANGE
🔹 9° Ano C
* 1ª Aula: CIENCIAS - FAGNA
* 2ª Aula: CIENCIAS - FAGNA
* 3ª Aula: GEO - Geovana P.
* 4ª Aula: GEO - Geovana P.
* 5ª Aula: MAT - SILVANA
* 6ª Aula: O.E.LP - Elaine
* 7ª Aula: O.E.LP - Elaine
🔹 3° A-TEC
* 1ª Aula: MARK - Ana Paula
* 2ª Aula: MARK - Ana Paula
* 3ª Aula: L P - LUCINEIDE
* 4ª Aula: MAT - IGOR
* 5ª Aula: MAT - IGOR
* 6ª Aula: G.OP - Anderson
* 7ª Aula: G.OP - Anderson
🔹 3° B-TEC
* 1ª Aula: HISTÓRIA - SHIRLEY
* 2ª Aula: HISTÓRIA - SHIRLEY
* 3ª Aula: LP - PATRICIA
* 4ª Aula: G.OP - Anderson
* 5ª Aula: G.OP - Anderson
* 6ª Aula: INOV - AMANDA
* 7ª Aula: C. EMP - AMANDA
'''

mapa_dia = {
    "SEGUNDA-FEIRA": "Segunda",
    "TERÇA-FEIRA": "Terça",
    "TERCA-FEIRA": "Terça",
    "QUARTA-FEIRA": "Quarta",
    "QUINTA-FEIRA": "Quinta",
    "SEXTA-FEIRA": "Sexta",
}

rows = []
dia = None
turma = None
for line in RAW.splitlines():
    line = line.strip()
    if not line:
        continue
    if line.startswith("📅"):
        chave = line.replace("📅", "").strip().upper()
        dia = mapa_dia.get(chave)
        if not dia:
            raise SystemExit(f"Dia nao mapeado: {chave}")
        continue
    if line.startswith("🔹"):
        turma = line.replace("🔹", "").strip()
        continue
    m = re.match(r"\*\s*(\d+)ª\s*Aula:\s*(.+)$", line)
    if not m:
        continue
    aula = int(m.group(1))
    resto = m.group(2).strip()
    if " - " in resto:
        disc, prof = resto.rsplit(" - ", 1)
    else:
        disc, prof = resto, ""
    disc = disc.strip()
    prof = fmt_nome(prof.strip())
    rows.append(("Turno 1", dia, aula, turma, disc, prof, 2026))

cur.executemany(
    """INSERT INTO grade_horaria
       (turno, dia_semana, aula, turma, disciplina, professor, ano_letivo)
       VALUES (%s,%s,%s,%s,%s,%s,%s)""",
    rows,
)
conn.commit()

cur.execute("SELECT COUNT(*) FROM grade_horaria WHERE turno='Turno 1'")
total = cur.fetchone()[0]
cur.execute("SELECT COUNT(DISTINCT professor) FROM grade_horaria WHERE turno='Turno 1'")
profs = cur.fetchone()[0]
cur.execute("SELECT DISTINCT professor FROM grade_horaria WHERE professor ILIKE '%alnei%' OR professor ILIKE '%rosangela%' ORDER BY 1")
print("exemplos:", cur.fetchall())
print(f"ok: {total} aulas | {profs} professores")
cur.close()
conn.close()
