"""Paleta Nexus Intelligence e validações.

Funções:
- contraste(a, b): razão de contraste WCAG entre dois HEX.
- simular(hex, tipo): cor vista por pessoa com protanopia, deuteranopia ou tritanopia.
- delta_e(a, b): distância de cor (CIE76) entre dois HEX.
- menor_distancia(lista, tipo): menor distância entre pares de uma paleta.

Rodar direto (python cores.py) imprime as tabelas para conferência.
"""
from itertools import combinations

# ---------------------------------------------------------------- marca (escuro)
NOITE = "#0A0B1E"
SUPERFICIE = "#14152B"
TEXTO = "#F4F5FA"
APOIO = "#9AA0BA"
VIOLETA = "#8B6DFF"
AQUA = "#22D8E8"
ROSA = "#FF4FB8"
LINHA = "#2A2C4D"   # hairline sobre a base escura

# ---------------------------------------------------------------- marca (claro)
PAPEL = "#FFFFFF"
TINTA = "#0A0B1E"
VIOLETA_ESC = "#5A3FD6"
AQUA_ESC = "#0B7F8F"
ROSA_ESC = "#C21F86"
APOIO_CLARO = "#4B4F6B"
LINHA_CLARA = "#D9DBE8"

# ---------------------------------------------------------------- dados
DADOS_ESCURO = [
    ("Violeta", "#8B6DFF"),
    ("Aqua", "#22D8E8"),
    ("Pedra", "#A99F8E"),
    ("Lilás", "#B9A8FF"),
    ("Ardósia", "#5F6B8C"),
    ("Índigo", "#5D45E0"),
]
DADOS_CLARO = [
    ("Violeta", "#5A3FD6"),
    ("Aqua", "#0B7F8F"),
    ("Pedra", "#7A6F5A"),
    ("Lilás", "#8B78E6"),
    ("Ardósia", "#8A93AD"),
    ("Índigo", "#2E2490"),
]
STATUS = [("Ok", "#2EC27E"), ("Atenção", "#F2B84B"), ("Crítico", "#F0545B")]
NEUTRO_DADOS = ("Outros", "#5B6080")


def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _hex(rgb):
    return "#%02X%02X%02X" % tuple(max(0, min(255, round(v))) for v in rgb)


def _lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _unlin(c):
    c = max(0.0, min(1.0, c))
    return 255 * (12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055)


def luminancia(h):
    r, g, b = (_lin(v) for v in _rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b):
    la, lb = luminancia(a), luminancia(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# Matrizes de Machado, Oliveira e Fernandes (2009), severidade total
_CVD = {
    "protanopia": [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
    "deuteranopia": [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
    "tritanopia": [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]],
}


def simular(h, tipo):
    if tipo == "normal":
        return h.upper()
    lin = [_lin(v) for v in _rgb(h)]
    m = _CVD[tipo]
    out = [sum(m[i][j] * lin[j] for j in range(3)) for i in range(3)]
    return _hex([_unlin(v) for v in out])


def _lab(h):
    r, g, b = (_lin(v) for v in _rgb(h))
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = (0.2126 * r + 0.7152 * g + 0.0722 * b)
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116

    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def delta_e(a, b):
    la, lb = _lab(a), _lab(b)
    return sum((p - q) ** 2 for p, q in zip(la, lb)) ** 0.5


def menor_distancia(cores, tipo="normal"):
    """Menor distância entre qualquer par, já simulando o tipo de visão."""
    sim = [(n, simular(h, tipo)) for n, h in cores]
    pior = None
    for (n1, h1), (n2, h2) in combinations(sim, 2):
        d = delta_e(h1, h2)
        if pior is None or d < pior[0]:
            pior = (d, n1, n2)
    return pior


# Pares de contraste mostrados no brand book: (rótulo, frente, fundo, uso)
PARES_ESCURO = [
    ("Texto claro sobre Noite", TEXTO, NOITE, "texto"),
    ("Texto claro sobre Superfície", TEXTO, SUPERFICIE, "texto"),
    ("Cinza de apoio sobre Noite", APOIO, NOITE, "texto"),
    ("Cinza de apoio sobre Superfície", APOIO, SUPERFICIE, "texto"),
    ("Violeta Nexus sobre Noite", VIOLETA, NOITE, "texto"),
    ("Violeta Nexus sobre Superfície", VIOLETA, SUPERFICIE, "texto"),
    ("Aqua sobre Noite", AQUA, NOITE, "texto"),
    ("Aqua sobre Superfície", AQUA, SUPERFICIE, "texto"),
    ("Rosa faísca sobre Noite", ROSA, NOITE, "decorativo"),
    ("Noite sobre Violeta (botão)", NOITE, VIOLETA, "texto"),
    ("Noite sobre Aqua (botão)", NOITE, AQUA, "texto"),
]
PARES_CLARO = [
    ("Tinta sobre branco", TINTA, PAPEL, "texto"),
    ("Apoio claro sobre branco", APOIO_CLARO, PAPEL, "texto"),
    ("Violeta escuro sobre branco", VIOLETA_ESC, PAPEL, "texto"),
    ("Aqua escuro sobre branco", AQUA_ESC, PAPEL, "texto"),
    ("Rosa escuro sobre branco", ROSA_ESC, PAPEL, "decorativo"),
    ("Branco sobre Violeta escuro (botão)", PAPEL, VIOLETA_ESC, "texto"),
]
PARES_PROIBIDOS = [
    ("Aqua neon sobre branco", AQUA, PAPEL),
    ("Violeta neon sobre branco", VIOLETA, PAPEL),
    ("Rosa faísca sobre branco", ROSA, PAPEL),
    ("Rosa faísca sobre Violeta", ROSA, VIOLETA),
    ("Aqua sobre Violeta", AQUA, VIOLETA),
]

if __name__ == "__main__":
    print("== contrastes (escuro)")
    for r, f, b, u in PARES_ESCURO:
        print(f"{r:40s} {contraste(f, b):5.2f}  {u}")
    print("== contrastes (claro)")
    for r, f, b, u in PARES_CLARO:
        print(f"{r:40s} {contraste(f, b):5.2f}  {u}")
    print("== proibidos")
    for r, f, b in PARES_PROIBIDOS:
        print(f"{r:40s} {contraste(f, b):5.2f}")
    print("== dados escuro: contraste com Noite e Superfície (gráfico pede 3:1)")
    for n, h in DADOS_ESCURO + [NEUTRO_DADOS]:
        print(f"{n:10s} {h} {contraste(h, NOITE):5.2f} {contraste(h, SUPERFICIE):5.2f}")
    print("== dados claro: contraste com branco")
    for n, h in DADOS_CLARO:
        print(f"{n:10s} {h} {contraste(h, PAPEL):5.2f}")
    print("== menor distância entre pares (CIE76)")
    for tipo in ("normal", "protanopia", "deuteranopia", "tritanopia"):
        print(tipo, "escuro", menor_distancia(DADOS_ESCURO, tipo), "claro", menor_distancia(DADOS_CLARO, tipo))
    print("== status vs dados (escuro, normal)")
    for sn, sh in STATUS:
        d = min((delta_e(sh, h), n) for n, h in DADOS_ESCURO)
        print(sn, sh, "mais próximo da paleta de dados:", d)
    for n, h in STATUS:
        print(n, [round(contraste(h, NOITE), 2)])
