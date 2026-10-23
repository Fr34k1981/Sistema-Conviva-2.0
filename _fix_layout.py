from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")
original = texto

# 1) Garantir import do TA_JUSTIFY
if "TA_JUSTIFY" not in texto:
    texto = texto.replace(
        "from reportlab.lib.enums import TA_CENTER, TA_LEFT",
        "from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY",
        1
    )
    # caso o import esteja em outra forma dentro da função
    if "TA_JUSTIFY" not in texto:
        texto = texto.replace(
            "from reportlab.lib.enums import TA_CENTER, TA_LEFT",
            "from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY",
        )

# 2) Texto justificado no estilo do comunicado
texto = texto.replace(
    """estilo_texto = ParagraphStyle(
        "TextoComunicado",
        parent=estilos["Normal"],
        fontName=fonte_normal,
        fontSize=10,
        leading=12,
        alignment=TA_LEFT,
        spaceAfter=4
    )""",
    """estilo_texto = ParagraphStyle(
        "TextoComunicado",
        parent=estilos["Normal"],
        fontName=fonte_normal,
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=8
    )""",
    1
)

# 3) Mais espaço antes/depois dos títulos de seção
texto = texto.replace(
    """estilo_secao = ParagraphStyle(
        "SecaoComunicado",
        parent=estilos["Heading2"],
        fontName=fonte_negrito,
        fontSize=10,
        leading=12,
        alignment=TA_LEFT,
        spaceBefore=3,
        spaceAfter=4
    )""",
    """estilo_secao = ParagraphStyle(
        "SecaoComunicado",
        parent=estilos["Heading2"],
        fontName=fonte_negrito,
        fontSize=10,
        leading=13,
        alignment=TA_LEFT,
        spaceBefore=10,
        spaceAfter=8
    )""",
    1
)

if texto == original:
    raise SystemExit("Nenhuma alteracao aplicada. Me avise.")

path.write_text(texto, encoding="utf-8")
print("ok: texto justificado + espaco entre secoes")
