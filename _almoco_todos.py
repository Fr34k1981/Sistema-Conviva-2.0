import psycopg2

conn = psycopg2.connect(host="127.0.0.1", port=5432, dbname="sistema_escolar", user="escola_admin", password="")
cur = conn.cursor()

dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]

# professores da grade
cur.execute("SELECT DISTINCT professor FROM grade_horaria WHERE turno='Turno 1' AND ano_letivo=2026")
professores = [r[0] for r in cur.fetchall() if r[0]]

# limpa ALMOCO antigo nas aulas 4 e 5 para recriar
cur.execute("DELETE FROM grade_janelas WHERE ano_letivo=2026 AND aula IN (4,5) AND tipo ILIKE 'ALMO%%'")

inseridos = 0
for prof in professores:
    for dia in dias:
        for aula in (4, 5):
            cur.execute(
                """
                SELECT 1 FROM grade_horaria
                WHERE turno='Turno 1' AND ano_letivo=2026
                  AND professor=%s AND dia_semana=%s AND aula=%s
                LIMIT 1
                """,
                (prof, dia, aula),
            )
            tem_aula = cur.fetchone() is not None
            if tem_aula:
                continue
            # so marca ALMOCO se estiver livre
            cur.execute(
                """
                INSERT INTO grade_janelas (professor, dia_semana, aula, tipo, ano_letivo)
                VALUES (%s,%s,%s,'ALMOÇO',2026)
                ON CONFLICT (professor, dia_semana, aula, ano_letivo)
                DO UPDATE SET tipo = EXCLUDED.tipo
                """,
                (prof, dia, aula),
            )
            inseridos += 1

conn.commit()
print(f"ok: {inseridos} almoco(s) marcados em aulas 4/5 livres")
cur.close()
conn.close()
