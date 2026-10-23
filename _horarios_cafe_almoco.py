from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

marcador = '        st.subheader("Grade de janelas · Almoço e H.E.")\n        st.caption("Clique nas células VAGO e marque ALMOÇO ou H.E. · aulas com turma ficam bloqueadas")'

if marcador not in texto:
    # tenta variante sem acento
    marcador = '        st.subheader("Grade de janelas'
    idx = texto.find(marcador)
    if idx == -1:
        raise SystemExit("Nao achei subheader da aba janelas")
    # achar fim do caption seguinte
    cap = texto.find("st.caption(", idx)
    if cap == -1:
        raise SystemExit("Nao achei caption")
    fim_cap = texto.find("\n", texto.find(")", cap))
    bloco_antigo = texto[idx:fim_cap+1]
else:
    bloco_antigo = marcador

bloco_novo = '''        st.subheader("Grade de janelas · Almoço e H.E.")
        st.caption("Células VAGO: marque ALMOÇO ou H.E. do professor · aulas com turma ficam bloqueadas")

        st.markdown("""
<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.75rem;margin:0.75rem 0 1rem 0;">
  <div style="padding:0.85rem 1rem;border-radius:10px;background:#eff6ff;border-left:5px solid #2563eb;">
    <div style="font-weight:800;color:#1e3a8a;margin-bottom:0.35rem;">6º · 7º · 3º TEC</div>
    <div style="color:#1e40af;font-size:0.92rem;line-height:1.55;">
      <b>Café:</b> 08:40 às 09:00<br>
      <b>Almoço:</b> 10:40 às 11:30
    </div>
  </div>
  <div style="padding:0.85rem 1rem;border-radius:10px;background:#fef3c7;border-left:5px solid #d97706;">
    <div style="font-weight:800;color:#92400e;margin-bottom:0.35rem;">8º · 9º</div>
    <div style="color:#b45309;font-size:0.92rem;line-height:1.55;">
      <b>Café:</b> 09:30 às 09:50<br>
      <b>Almoço:</b> 11:30 às 12:20
    </div>
  </div>
</div>
<p style="margin:0 0 0.75rem 0;font-size:0.85rem;color:#64748b;">
  Esses horários são dos <b>estudantes</b>. O ALMOÇO / H.E. marcados na grade abaixo são do <b>professor</b>.
</p>
""")
'''

if bloco_antigo in texto:
    texto = texto.replace(bloco_antigo, bloco_novo, 1)
else:
    # inserir apos o primeiro caption da aba janelas
    i = texto.find("    with aba_janelas_prof:")
    if i == -1:
        raise SystemExit("Nao achei aba_janelas_prof")
    j = texto.find("st.caption(", i)
    if j == -1:
        raise SystemExit("Nao achei caption janelas")
    k = texto.find("\n", texto.find(")", j))
    texto = texto[:k+1] + "\n" + bloco_novo.split("st.caption")[0].split("st.subheader")[0] + texto[k+1:]
    # simpler: just insert cards after caption line
    cards = '''
        st.markdown("""
<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.75rem;margin:0.75rem 0 1rem 0;">
  <div style="padding:0.85rem 1rem;border-radius:10px;background:#eff6ff;border-left:5px solid #2563eb;">
    <div style="font-weight:800;color:#1e3a8a;margin-bottom:0.35rem;">6º · 7º · 3º TEC</div>
    <div style="color:#1e40af;font-size:0.92rem;line-height:1.55;">
      <b>Café:</b> 08:40 às 09:00<br>
      <b>Almoço:</b> 10:40 às 11:30
    </div>
  </div>
  <div style="padding:0.85rem 1rem;border-radius:10px;background:#fef3c7;border-left:5px solid #d97706;">
    <div style="font-weight:800;color:#92400e;margin-bottom:0.35rem;">8º · 9º</div>
    <div style="color:#b45309;font-size:0.92rem;line-height:1.55;">
      <b>Café:</b> 09:30 às 09:50<br>
      <b>Almoço:</b> 11:30 às 12:20
    </div>
  </div>
</div>
<p style="margin:0 0 0.75rem 0;font-size:0.85rem;color:#64748b;">
  Esses horários são dos <b>estudantes</b>. O ALMOÇO / H.E. marcados na grade abaixo são do <b>professor</b>.
</p>
""")
'''
    # if first replace failed, try insert after caption only
    if "6º · 7º · 3º TEC" not in texto:
        texto = texto[:k+1] + cards + texto[k+1:]
        print("ok: cards inseridos (fallback)")
    else:
        print("ok: cards via replace")

if "6º · 7º · 3º TEC" in texto or "6º · 7º · 3º TEC" in texto:
    pass

path.write_text(texto, encoding="utf-8")

# verificacao
if "08:40" in path.read_text(encoding="utf-8") and "11:30" in path.read_text(encoding="utf-8"):
    print("ok: horarios dos estudantes inseridos")
else:
    raise SystemExit("Falhou insercao dos horarios")
