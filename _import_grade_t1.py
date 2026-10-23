import psycopg2

conn = psycopg2.connect(
    host="127.0.0.1", port=5432, dbname="sistema_escolar",
    user="escola_admin", password=""
)
cur = conn.cursor()

# limpa so Turno 1 2026 para poder reimportar
cur.execute("DELETE FROM grade_horaria WHERE turno = %s AND ano_letivo = %s", ("Turno 1", 2026))

turmas = [
    "6ºA", "6ºB", "7ºA", "7ºC", "8ºA", "8ºB",
    "8ºC", "9ºA", "9ºB", "9ºC", "3ºA-TEC", "3ºB-TEC"
]

# dia -> aula -> lista de 12 celulas "DISCIPLINA - PROFESSOR"
GRADE = {
"Segunda": {
1: ["LP - RO","INGLES - LUCINEIDE","MAT - VERON","LP - ROSE","LP - PATRICIA","GEO - PATROC","MAT - JAQ","ARTE - ELIANE","CIENCIAS - FAGNA","HISTÓRIA - SHIRLEY","MAT - IGOR","PROJ. MUL - ALNEI"],
2: ["LP - RO","INGLES - LUCINEIDE","MAT - VERON","LP - ROSE","LP - PATRICIA","GEO - PATROC","MAT - JAQ","LP - ITATIARA","CIENCIAS - FAGNA","ARTE - ELIANE","MAT - IGOR","PROJ. MUL - ALNEI"],
3: ["INGLES - LUCINEIDE","LP - RO","HIST - ROSE","MAT - VERON","GEO - PATROC","MAT - JAQ","CIENCIAS - FAGNA","LP - ITATIARA","O.E.LP - ELIANE","O.E. MAT. - IGOR","PROJ. MUL - ALNEI","C. EMP - AMANDA"],
4: ["INGLES - LUCINEIDE","LP - RO","HIST - ROSE","TEC - FERNANDA","GEO - PATROC","LP - PATRICIA","ED.FIN. - IGOR","MAT - SILVANA","O.E.LP - ELIANE","LP - ITATIARA","PROJ. MUL - ALNEI","C. EMP - AMANDA"],
5: ["HIST - ROSE","MAT - VERON","GEO - SOLANGE","TEC - FERNANDA","MAT - JAQ","LP - PATRICIA","CIENCIAS - FAGNA","O.E. MAT. - IGOR","MAT - SILVANA","LP - ITATIARA","E.F. - GUI","G.OP - ANDER"],
6: ["MAT - VERON","O.E. MAT - JAQ","REDAÇÃO - RO","GEO - SOLANGE","CIENCIAS - FERNANDA","CIENCIAS - FAGNA","LP - PATRICIA","INGLES - LUCINEIDE","LP - ITATIARA","E.F. - GUI","INOV - AMANDA","FÍSICA - IGOR"],
7: ["MAT - VERON","ARTE - ELIANE","O.E. MAT - JAQ","GEO - SOLANGE","CIENCIAS - FERNANDA","O.E.MAT. - SILVANA","LP - PATRICIA","INGLES - LUCINEIDE","LP - ITATIARA","E.F. - GUI","INOV - AMANDA","FÍSICA - IGOR"],
},
"Terça": {
1: ["TEC - FERNANDA","O.E. LP - ITATIARA","LP - ELIANE","REDAÇÃO - RO","HISTÓRIA - SHIRLEY","MAT - JAQ","GEO - PATROC","E.F. - GUI","MAT - SILVANA","CIENCIAS - FAGNA","LP - LUCINEIDE","LP - PATRICIA"],
2: ["TEC - FERNANDA","O.E. LP - ITATIARA","LP - ELIANE","REDAÇÃO - RO","HISTÓRIA - SHIRLEY","MAT - JAQ","GEO - PATROC","E.F. - GUI","MAT - SILVANA","CIENCIAS - FAGNA","LP - LUCINEIDE","LP - PATRICIA"],
3: ["MAT - VERON","TEC - FERNANDA","INGLES - LUCINEIDE","HIST - ROSE","MAT - JAQ","HISTÓRIA - SHIRLEY","O.E.MAT. - SILVANA","REDAÇÃO - RO","GEO - PATROC","O.E. MAT. - IGOR","REDAÇÃO - FAGNA","E.F. - GUI"],
4: ["E.F. - GUI","TEC - FERNANDA","INGLES - LUCINEIDE","ED.FIN. - IGOR","P. V. - SOLANGE","HISTÓRIA - SHIRLEY","MAT - JAQ","REDAÇÃO - RO","GEO - PATROC","MAT - SILVANA","REDAÇÃO - FAGNA","G.FIN - ANDER"],
5: ["E.F. - GUI","GEO - SOLANGE","HIST - ROSE","MAT - VERON","LP - PATRICIA","GEO - PATROC","MAT - JAQ","O.E. MAT. - IGOR","HISTÓRIA - SHIRLEY","MAT - SILVANA","INOV - AMANDA","G.FIN - ANDER"],
6: ["GEO - SOLANGE","MAT - VERON","TEC - FERNANDA","ARTE - ELIANE","INGLES - LUCINEIDE","ED.FIN. - IGOR","HISTÓRIA - SHIRLEY","CIENCIAS - FAGNA","E.F. - GUI","REDAÇÃO - RO","G.FIN - ANDER","INOV - AMANDA"],
7: ["GEO - SOLANGE","MAT - VERON","TEC - FERNANDA","ARTE - ELIANE","INGLES - LUCINEIDE","ED.FIN. - IGOR","HISTÓRIA - SHIRLEY","CIENCIAS - FAGNA","E.F. - GUI","REDAÇÃO - RO","G.FIN - ANDER","INOV - AMANDA"],
},
"Quarta": {
1: ["ARTE - ELIANE","LP - RO","CIENCIAS - FERNANDA","MAT - VERON","REDAÇÃO - ROSE","LP - PATRICIA","MAT - JAQ","HISTÓRIA - SHIRLEY","LP - ITATIARA","TEC - SILVANA","FÍSICA - IGOR","MARKE. - Ana Paula"],
2: ["ARTE - ELIANE","LP - RO","GEO - SOLANGE","CIENCIAS - FERNANDA","REDAÇÃO - ROSE","LP - PATRICIA","INGLES - LUCINEIDE","HISTÓRIA - SHIRLEY","LP - ITATIARA","TEC - SILVANA","FÍSICA - IGOR","MARKE. - Ana Paula"],
3: ["LP - RO","E.F. - GUI","ARTE - ELIANE","GEO - SOLANGE","MAT - JAQ","REDAÇÃO - ROSE","INGLES - LUCINEIDE","GEO - PATROC","MAT - SILVANA","HISTÓRIA - SHIRLEY","COM. - Ana Paula","MAT - IGOR"],
4: ["LP - RO","E.F. - GUI","ARTE - ELIANE","P. V. - PATROC","MAT - JAQ","REDAÇÃO - ROSE","LP - PATRICIA","TEC - SILVANA","INGLES - LUCINEIDE","HISTÓRIA - SHIRLEY","PROJ. MUL - ALNEI","MAT - IGOR"],
5: ["CIENCIAS - FERNANDA","ARTE - ELIANE","P. V. - PATROC","O.E. MAT - JAQ","ED.FIN. - IGOR","CIENCIAS - FAGNA","LP - PATRICIA","TEC - SILVANA","INGLES - LUCINEIDE","P. V. - SOLANGE","G.OP - ANDER","PROJ. MUL - ALNEI"],
6: ["ELETIVA - PATRICIA","ELETIVA - PATROC","ELETIVA - VERON","ELETIVA - ROSE","ELETIVA - SOLANGE","ELETIVA - SILVANA","ELETIVA - FERNANDA","ELETIVA - RO","ELETIVA - SHIRLEY","ELETIVA - GUI","G.OP - ANDER","REDAÇÃO - FAGNA"],
7: ["ELETIVA - PATRICIA","ELETIVA - PATROC","ELETIVA - VERON","ELETIVA - ROSE","ELETIVA - SOLANGE","ELETIVA - SILVANA","ELETIVA - FERNANDA","ELETIVA - RO","ELETIVA - SHIRLEY","ELETIVA - GUI","LP - LUCINEIDE","REDAÇÃO - FAGNA"],
},
"Quinta": {
1: ["HIST - ROSE","CIENCIAS - FERNANDA","REDAÇÃO - RO","MAT - VERON","HISTÓRIA - SHIRLEY","TEC - JAQ","ED.FIN. - IGOR","O.E.LP - ELIANE","CIENCIAS - FAGNA","INGLES - LUCINEIDE","P. V. - SOLANGE","MARKE. - Ana Paula"],
2: ["HIST - ROSE","REDAÇÃO - RO","GEO - SOLANGE","MAT - VERON","E.F. - GUI","TEC - JAQ","HISTÓRIA - SHIRLEY","O.E.LP - ELIANE","CIENCIAS - FAGNA","INGLES - LUCINEIDE","COM. - Ana Paula","MAT - IGOR"],
3: ["REDAÇÃO - RO","HIST - ROSE","MAT - VERON","CIENCIAS - FERNANDA","E.F. - GUI","HISTÓRIA - SHIRLEY","TEC - JAQ","P. V. - SOLANGE","MAT - SILVANA","GEO - PATROC","COM. - Ana Paula","MAT - IGOR"],
4: ["REDAÇÃO - RO","MAT - VERON","LP - ELIANE","CIENCIAS - FERNANDA","TEC - JAQ","CIENCIAS - FAGNA","E.F. - GUI","MAT - SILVANA","HISTÓRIA - SHIRLEY","LP - ITATIARA","MARK - Ana Paula","G.FIN - ANDER"],
5: ["GEO - SOLANGE","MAT - VERON","LP - ELIANE","LP - ROSE","TEC - JAQ","CIENCIAS - FAGNA","E.F. - GUI","MAT - SILVANA","HISTÓRIA - SHIRLEY","LP - ITATIARA","G.FIN - ANDER","LP - PATRICIA"],
6: ["MAT - VERON","GEO - SOLANGE","CIENCIAS - FERNANDA","LP - ROSE","ED.FIN. - IGOR","E.F. - GUI","CIENCIAS - FAGNA","LP - ITATIARA","REDAÇÃO - RO","MAT - SILVANA","HISTÓRIA - SHIRLEY","G.OP - ANDER"],
7: ["MAT - VERON","O.E. MAT - JAQ","CIENCIAS - FERNANDA","ED.FIN. - IGOR","LP - PATRICIA","E.F. - GUI","CIENCIAS - FAGNA","LP - ITATIARA","REDAÇÃO - RO","MAT - SILVANA","HISTÓRIA - SHIRLEY","P. V. - SOLANGE"],
},
"Sexta": {
1: ["O.E. LP - PATRICIA","CIENCIAS - FERNANDA","E.F. - GUI","HIST - ROSE","O.E.MAT. - SILVANA","ARTE - ELIANE","P. V. - SOLANGE","GEO - PATROC","O.E. MAT. - IGOR","CIENCIAS - FAGNA","MARK - Ana Paula","HISTÓRIA - SHIRLEY"],
2: ["CIENCIAS - FERNANDA","HIST - ROSE","O.E. LP - PATRICIA","E.F. - GUI","O.E. LP - ITATIARA","MAT - JAQ","ARTE - ELIANE","GEO - PATROC","O.E. MAT. - IGOR","CIENCIAS - FAGNA","MARK - Ana Paula","HISTÓRIA - SHIRLEY"],
3: ["CIENCIAS - FERNANDA","REDAÇÃO - RO","MAT - VERON","E.F. - GUI","ARTE - ELIANE","MAT - JAQ","REDAÇÃO - ROSE","HISTÓRIA - SHIRLEY","TEC - SILVANA","GEO - PATROC","LP - LUCINEIDE","LP - PATRICIA"],
4: ["P. V. - GUI","GEO - SOLANGE","MAT - VERON","O.E. LP - PATRICIA","MAT - JAQ","INGLES - LUCINEIDE","REDAÇÃO - ROSE","CIENCIAS - FAGNA","TEC - SILVANA","GEO - PATROC","MAT - IGOR","G.OP - ANDER"],
5: ["O.E. LP - PATRICIA","CIENCIAS - FERNANDA","E.F. - GUI","HIST - ROSE","GEO - PATROC","INGLES - LUCINEIDE","TEC - JAQ","CIENCIAS - FAGNA","ARTE - ELIANE","MAT - SILVANA","MAT - IGOR","G.OP - ANDER"],
6: ["O.E. MAT - JAQ","P. V. - GUI","ED.FIN. - IGOR","INGLES - LUCINEIDE","CIENCIAS - FERNANDA","P. V. - SOLANGE","O.E. LP - ITATIARA","MAT - SILVANA","GEO - PATROC","O.E.LP - ELIANE","G.OP - ANDER","INOV - AMANDA"],
7: ["O.E. MAT - JAQ","HIST - ROSE","ED.FIN. - IGOR","INGLES - LUCINEIDE","CIENCIAS - FERNANDA","O.E. LP - ITATIARA","GEO - PATROC","MAT - SILVANA","P. V. - SOLANGE","O.E.LP - ELIANE","G.OP - ANDER","C. EMP - AMANDA"],
},
}

rows = []
for dia, aulas in GRADE.items():
    for aula, celulas in aulas.items():
        if len(celulas) != 12:
            raise SystemExit(f"Dia {dia} aula {aula}: {len(celulas)} celulas (esperado 12)")
        for turma, cel in zip(turmas, celulas):
            cel = cel.strip()
            if " - " in cel:
                disc, prof = cel.rsplit(" - ", 1)
            else:
                disc, prof = cel, ""
            rows.append(("Turno 1", dia, aula, turma, disc.strip(), prof.strip(), 2026))

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
print(f"ok: {total} aulas importadas | {profs} professores distintos")
cur.close()
conn.close()
