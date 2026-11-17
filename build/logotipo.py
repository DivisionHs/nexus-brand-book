"""Logotipo Nexus Intelligence: letreiramento próprio em traço único + assinaturas.

O letreiramento é desenhado, não digitado: nada depende de fonte instalada e o SVG
abre igual em qualquer máquina. Traço de espessura constante, pontas e quinas
arredondadas (mesma linguagem das linhas do símbolo).

"Nexus": altura de caixa-baixa 40, altura de maiúscula 56, traço 7.
O "x" é quatro braços e um nó central: um hub em miniatura.
"INTELLIGENCE": maiúsculas altura 14, traço 2.6, espaçadas para fechar
exatamente a largura de "Nexus".
"""
from math import cos, sin, radians, atan2, hypot
import cores as C
import simbolo as S

SW = 7            # traço de "Nexus"
BASE = 60         # linha de base
XH = 20           # topo da caixa-baixa
GAP = 14          # espaço entre letras (centro a centro dos traços)
LARG_NEXUS = 232  # largura visual de "Nexus"

SW_SUB = 2.6
ALT_SUB = 14

PALETAS = {
    "dark": dict(main=C.TEXTO, dot=C.AQUA, sub=C.APOIO),
    "light": dict(main=C.TINTA, dot=C.AQUA_ESC, sub=C.APOIO_CLARO),
}


def _f(n):
    return f"{n:.2f}".rstrip("0").rstrip(".")


def _pal(tema, ink):
    if tema == "mono":
        return dict(main=ink, dot=ink, sub=ink)
    return PALETAS[tema]


def _glifos_nexus():
    """Retorna lista de (rótulo, largura, caminho_local, ponto_central?)."""
    n = f"M0 {BASE}V4L36 {BASE}V4"
    cx, r = 20, 20
    e = (f"M0 40H40A{r} {r} 0 1 0 {_f(cx + r * cos(radians(40)))} {_f(40 + r * sin(radians(40)))}")
    # x: quatro braços que não chegam ao centro; o nó fica no meio
    w, cy, gap = 34, 40, 11
    cxx = w / 2
    bracos = []
    for (px, py) in [(0, XH), (w, XH), (0, BASE), (w, BASE)]:
        dx, dy = cxx - px, cy - py
        d = hypot(dx, dy)
        fim = (cxx - dx / d * gap, cy - dy / d * gap)
        bracos.append(f"M{px} {py}L{_f(fim[0])} {_f(fim[1])}")
    x = "".join(bracos)
    u = f"M0 {XH}V43A17 17 0 0 0 34 43M34 {XH}V{BASE}"
    s = (f"M{_f(12.5 + 12.5 * cos(radians(25)))} {_f(30 - 10 * sin(radians(25)))}"
         f"A12.5 10 0 1 0 12.5 40A12.5 10 0 1 1 {_f(12.5 - 12.5 * cos(radians(25)))} {_f(50 + 10 * sin(radians(25)))}")
    return [("N", 36, n, None), ("e", 40, e, None), ("x", 34, x, (cxx, cy)), ("u", 34, u, None), ("s", 25, s, None)]


def nexus(tema="dark", ink="#0A0B1E"):
    """Palavra 'Nexus' como grupo de caminhos. Origem: centro do traço da esquerda do N."""
    p = _pal(tema, ink)
    x0, partes = 0, []
    for rot, larg, d, ponto in _glifos_nexus():
        partes.append(f'<path transform="translate({_f(x0)} 0)" d="{d}" fill="none" stroke="{p["main"]}" '
                      f'stroke-width="{SW}" stroke-linecap="round" stroke-linejoin="round"/>')
        if ponto:
            partes.append(f'<circle cx="{_f(x0 + ponto[0])}" cy="{_f(ponto[1])}" r="4.2" fill="{p["dot"]}"/>')
        x0 += larg + GAP
    return "".join(partes)


# ------------------------------------------------------------- INTELLIGENCE
def _caps():
    h = ALT_SUB
    rx, ry = 6.5, 7
    ini = (rx + rx * cos(radians(-40)), ry + ry * sin(radians(-40)))
    fimc = (rx + rx * cos(radians(40)), ry + ry * sin(radians(40)))
    return {
        "I": (0, f"M0 0V{h}"),
        "N": (10, f"M0 {h}V0L10 {h}V0"),
        "T": (10, f"M0 0H10M5 0V{h}"),
        "E": (8, f"M8 0H0V{h}H8M0 {h / 2}H6.5"),
        "L": (8, f"M0 0V{h}H8"),
        "G": (13, f"M{_f(ini[0])} {_f(ini[1])}A{rx} {ry} 0 1 0 13 7H7.5"),
        "C": (11.5, f"M{_f(ini[0])} {_f(ini[1])}A{rx} {ry} 0 1 0 {_f(fimc[0])} {_f(fimc[1])}"),
    }


def intelligence(tema="dark", ink="#0A0B1E", largura=LARG_NEXUS):
    """'INTELLIGENCE' fechando exatamente `largura` (visual, incluindo as pontas)."""
    p = _pal(tema, ink)
    caps = _caps()
    palavra = "INTELLIGENCE"
    soma = sum(caps[ch][0] for ch in palavra)
    vão = (largura - SW_SUB - soma) / (len(palavra) - 1)
    x0 = SW_SUB / 2 - SW / 2          # alinha a borda esquerda visual com a do N
    out = []
    x = x0
    for ch in palavra:
        larg, d = caps[ch]
        out.append(f'<path transform="translate({_f(x)} 0)" d="{d}"/>')
        x += larg + vão
    return (f'<g fill="none" stroke="{p["sub"]}" stroke-width="{SW_SUB}" stroke-linecap="round" '
            f'stroke-linejoin="round">{"".join(out)}</g>')


def _topo_sub():
    return BASE + SW / 2 + 13


def bloco_texto(tema="dark", ink="#0A0B1E", com_sub=True):
    """Nexus + INTELLIGENCE. Origem em (0,0) = centro do traço esquerdo do N na linha de topo da caixa."""
    s = nexus(tema, ink)
    if com_sub:
        s += f'<g transform="translate(0 {_f(_topo_sub())})">{intelligence(tema, ink)}</g>'
    return s


ALT_BLOCO_SUB = _topo_sub() + ALT_SUB + SW_SUB / 2      # base do bloco com sub
ALT_BLOCO = BASE + SW / 2                               # base do bloco sem sub
TOPO_BLOCO = 4 - SW / 2                                 # topo do N


def _svg(vb, inner, extra=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" {extra}>{inner}</svg>'


def _simb(tema, ink, uid, tam, x, y, nivel="completo"):
    """Símbolo aninhado em caixa tam x tam. nivel: completo (240) ou compacto (120)."""
    if nivel == "completo":
        return (f'<g transform="translate({_f(x)} {_f(y)}) scale({_f(tam / 240)})">'
                f'{S.miolo_completo(tema, ink, uid)}</g>')
    return (f'<g transform="translate({_f(x)} {_f(y)}) scale({_f(tam / 120)})">'
            f'{S.miolo_compacto(tema, ink, uid)}</g>')


def wordmark(tema="dark", ink="#0A0B1E", com_sub=True, extra='role="img" aria-label="Nexus Intelligence"'):
    alt = ALT_BLOCO_SUB if com_sub else ALT_BLOCO
    m = 4
    vb = f"{_f(-SW / 2 - m)} {_f(TOPO_BLOCO - m)} {LARG_NEXUS + 2 * m} {_f(alt - TOPO_BLOCO + 2 * m)}"
    return _svg(vb, bloco_texto(tema, ink, com_sub), extra)


EXT = {   # x0, x1, y0, y1, lado da caixa: extensão real do desenho em cada nível
    "completo": (4, 218.5, 31, 214.5, 240),
    "compacto": (1.7, 109.9, 15.8, 104.2, 120),
}


def _simb_ajustado(tema, ink, uid, nivel, altura, x, y_centro):
    """Posiciona o símbolo pela extensão real: conteúdo com `altura`, canto esquerdo em x, centro vertical em y_centro."""
    x0, x1, y0, y1, caixa = EXT[nivel]
    esc = altura / (y1 - y0)
    tam = caixa * esc
    sx = x - x0 * esc
    sy = y_centro - (y0 + y1) / 2 * esc
    largura = (x1 - x0) * esc
    return _simb(tema, ink, uid, tam, sx, sy, nivel), largura


def horizontal(tema="dark", ink="#0A0B1E", uid="lh", com_sub=True, nivel="compacto",
               extra='role="img" aria-label="Nexus Intelligence"'):
    """Símbolo à esquerda, wordmark à direita. O símbolo tem a mesma altura do bloco de texto."""
    alt = ALT_BLOCO_SUB if com_sub else ALT_BLOCO
    h = alt - TOPO_BLOCO
    ct = (TOPO_BLOCO + alt) / 2
    simb, larg_s = _simb_ajustado(tema, ink, uid, nivel, h * (1.0 if nivel == "compacto" else 0.98), 0, ct)
    txt_x = larg_s + 24 + SW / 2
    total = txt_x - SW / 2 + LARG_NEXUS
    vb = f"-2 {_f(TOPO_BLOCO - 4)} {_f(total + 4)} {_f(h + 8)}"
    inner = simb + f'<g transform="translate({_f(txt_x)} 0)">{bloco_texto(tema, ink, com_sub)}</g>'
    return _svg(vb, inner, extra)


def empilhado(tema="dark", ink="#0A0B1E", uid="lv", nivel="compacto", extra='role="img" aria-label="Nexus Intelligence"'):
    """Símbolo centralizado acima, wordmark abaixo."""
    larg = LARG_NEXUS + 24
    altura_s = 112 if nivel == "completo" else 92
    simb, larg_s = _simb_ajustado(tema, ink, uid, nivel, altura_s, 0, altura_s / 2)
    sx = (larg - larg_s) / 2
    simb, larg_s = _simb_ajustado(tema, ink, uid, nivel, altura_s, sx, altura_s / 2)
    ty = altura_s + 26 - TOPO_BLOCO
    inner = simb + f'<g transform="translate({_f(12 + SW / 2)} {_f(ty)})">{bloco_texto(tema, ink)}</g>'
    return _svg(f"0 -4 {larg} {_f(ty + ALT_BLOCO_SUB + 8)}", inner, extra)


if __name__ == "__main__":
    print(len(wordmark()), len(horizontal()), len(empilhado()))
