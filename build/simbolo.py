"""Símbolo Nexus: três níveis do mesmo conceito.

Conceito: dados dispersos (círculos, à esquerda) convergem para um hub e saem alinhados
(células quadradas, à direita). Círculo é dado solto, quadrado é dado em ordem.

Níveis:
- completo (viewBox 240): 5 entradas, hub com halo e luz, 3 saídas alinhadas.
- compacto (viewBox 120): 3 entradas, hub, 3 saídas. Sem halo e sem brilho.
- minimo (viewBox 32): 3 entradas, hub, 3 saídas, desenhado para 32 px.
- favicon (viewBox 16): 2 entradas, hub, 1 saída, desenhado para a grade de 16 px.

Temas: "dark", "light" ou "mono" (uma cor só, passada em `ink`).
Cada chamada recebe um `uid` para que os ids de gradiente não colidam na mesma página.
"""
from math import cos, sin, radians
import cores as C

TEMAS = {
    "dark": dict(v=C.VIOLETA, a=C.AQUA, p=C.ROSA, core=C.TEXTO),
    "light": dict(v=C.VIOLETA_ESC, a=C.AQUA_ESC, p=C.ROSA_ESC, core=C.TINTA),
}


def _f(n):
    return f"{n:.2f}".rstrip("0").rstrip(".")


def _defs(uid, w, tema, ink):
    """Gradiente de assinatura (violeta para aqua) e brilho do hub."""
    if tema == "mono":
        return ""
    t = TEMAS[tema]
    glow = ""
    if tema == "dark":
        glow = (f'<radialGradient id="{uid}h" cx="50%" cy="50%" r="50%">'
                f'<stop offset="0" stop-color="{t["v"]}" stop-opacity=".55"/>'
                f'<stop offset="1" stop-color="{t["v"]}" stop-opacity="0"/></radialGradient>')
    return (f'<defs><linearGradient id="{uid}g" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{w}" y2="0">'
            f'<stop offset="0" stop-color="{t["v"]}"/><stop offset=".42" stop-color="{t["v"]}"/>'
            f'<stop offset="1" stop-color="{t["a"]}"/></linearGradient>{glow}</defs>')


def _cores(uid, tema, ink):
    if tema == "mono":
        return dict(line=ink, node=ink, core=ink, spark=ink)
    t = TEMAS[tema]
    return dict(line=f"url(#{uid}g)", node=f"url(#{uid}g)", core=t["core"], spark=t["p"])


def _entradas(hub, R, nos, angulos, sw, c, tension=0.45):
    """Curvas que saem de cada nó disperso e chegam ao anel do hub em leque."""
    hx, hy = hub
    saida = []
    for (x, y, r), ang in zip(nos, angulos):
        a = radians(ang)
        px, py = hx - R * cos(a), hy + R * sin(a)           # ponto de chegada no anel
        sx = x + r                                          # a curva sai da borda direita do nó
        k = tension * (px - sx)
        c1 = (sx + 0.5 * (px - sx), y)
        c2 = (px - cos(a) * k, py + sin(a) * k)
        saida.append(f'<path d="M{_f(sx)} {_f(y)}C{_f(c1[0])} {_f(c1[1])} {_f(c2[0])} {_f(c2[1])} {_f(px)} {_f(py)}" '
                     f'fill="none" stroke="{c["line"]}" stroke-width="{sw}" stroke-linecap="round"/>')
        saida.append(f'<circle cx="{_f(x)}" cy="{_f(y)}" r="{r}" fill="{c["node"]}"/>')
    return "".join(saida)


def _saidas(hub, R, xfim, dys, angulos, r_no, sw, c, x_reta):
    """Linhas que deixam o anel, se abrem e correm retas até nós alinhados."""
    hx, hy = hub
    saida = []
    for dy, ang in zip(dys, angulos):
        a = radians(ang)
        qx, qy = hx + R * cos(a), hy + R * sin(a)
        ey = hy + dy
        lado = r_no * 1.75                       # saída é célula de tabela: quadrado, não círculo
        x0 = xfim - lado / 2
        cx1, cy1 = qx + cos(a) * R * 0.85, qy + sin(a) * R * 0.85
        if abs(dy) < 0.01:
            d = f"M{_f(qx)} {_f(qy)}L{_f(x0)} {_f(ey)}"
        else:
            d = (f"M{_f(qx)} {_f(qy)}C{_f(cx1)} {_f(cy1)} {_f(x_reta - R * 1.5)} {_f(ey)} {_f(x_reta)} {_f(ey)}"
                 f"L{_f(x0)} {_f(ey)}")
        saida.append(f'<path d="{d}" fill="none" stroke="{c["line"]}" stroke-width="{sw}" stroke-linecap="round"/>')
        saida.append(f'<rect x="{_f(xfim - lado / 2)}" y="{_f(ey - lado / 2)}" width="{_f(lado)}" height="{_f(lado)}" '
                     f'rx="{_f(lado * 0.22)}" fill="{c["node"]}"/>')
    return "".join(saida)


def _envolver(vb, inner, extra=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb} {vb}" {extra}>{inner}</svg>'


# ----------------------------------------------------------------- níveis
def completo(tema="dark", ink="#0A0B1E", uid="s", extra="role=\"img\" aria-label=\"Símbolo Nexus Intelligence\""):
    return _envolver(240, miolo_completo(tema, ink, uid), extra)


def miolo_completo(tema="dark", ink="#0A0B1E", uid="s"):
    hub, R = (120, 120), 17
    c = _cores(uid, tema, ink)
    nos = [(22, 38, 7), (64, 74, 5), (12, 122, 8), (60, 166, 5), (34, 208, 6.5)]
    partes = [_defs(uid, 240, tema, ink)]
    if tema == "dark":
        partes.append(f'<circle cx="120" cy="120" r="46" fill="url(#{uid}h)"/>')
    if tema != "mono":
        # halo de camada: segundo anel fino, sugere profundidade
        partes.append(f'<circle cx="120" cy="120" r="31" fill="none" stroke="{c["line"]}" stroke-width="1.4" opacity=".38"/>')
    partes.append(_entradas(hub, R, nos, [-58, -29, 0, 29, 58], 3.2, c))
    partes.append(_saidas(hub, R, 212, [-44, 0, 44], [-35, 0, 35], 6.5, 3.2, c, 160))
    partes.append(f'<circle cx="120" cy="120" r="{R}" fill="none" stroke="{c["line"]}" stroke-width="5"/>')
    partes.append(f'<circle cx="120" cy="120" r="7" fill="{c["core"]}"/>')
    if tema != "mono":
        partes.append(f'<circle cx="120" cy="{120 - R}" r="4.4" fill="{c["spark"]}"/>')
    else:
        partes.append(f'<circle cx="120" cy="{120 - R}" r="4.4" fill="{c["line"]}"/>')
    return "".join(partes)


def miolo_compacto(tema="dark", ink="#0A0B1E", uid="s"):
    """Traço mais grosso que o completo: é o símbolo que convive com o wordmark nas assinaturas."""
    hub, R = (60, 60), 11.5
    c = _cores(uid, tema, ink)
    nos = [(14, 22, 6.2), (8.5, 60, 6.8), (16, 98, 6.2)]
    return (_defs(uid, 120, tema, ink)
            + _entradas(hub, R, nos, [-40, 0, 40], 5, c)
            + _saidas(hub, R, 105, [-30, 0, 30], [-32, 0, 32], 5.6, 5, c, 80)
            + f'<circle cx="60" cy="60" r="{R}" fill="none" stroke="{c["line"]}" stroke-width="5.4"/>'
            + f'<circle cx="60" cy="60" r="4.2" fill="{c["core"]}"/>'
            + f'<circle cx="60" cy="{60 - R}" r="3.4" fill="{c["spark" if tema != "mono" else "line"]}"/>')


def compacto(tema="dark", ink="#0A0B1E", uid="s", extra="role=\"img\" aria-label=\"Símbolo Nexus Intelligence\""):
    return _envolver(120, miolo_compacto(tema, ink, uid), extra)


def minimo(tema="dark", ink="#0A0B1E", uid="s", extra="role=\"img\" aria-label=\"Símbolo Nexus Intelligence\""):
    """32 px: três entradas, hub cheio com anel fino, três saídas alinhadas."""
    hub, R = (16, 16), 4.6
    c = _cores(uid, tema, ink)
    nos = [(3, 6, 2.3), (2.6, 16, 2.4), (3.6, 26, 2.3)]
    inner = (_defs(uid, 32, tema, ink)
             + _entradas(hub, R, nos, [-40, 0, 40], 1.8, c, tension=0.35)
             + _saidas(hub, R, 29, [-8, 0, 8], [-35, 0, 35], 2.3, 1.8, c, 24)
             + f'<circle cx="16" cy="16" r="{R}" fill="none" stroke="{c["line"]}" stroke-width="2"/>'
             + f'<circle cx="16" cy="16" r="1.7" fill="{c["core"]}"/>')
    return _envolver(32, inner, extra)


def favicon(tema="dark", ink="#0A0B1E", uid="s", extra="role=\"img\" aria-label=\"Nexus Intelligence\"", tile=True):
    """16 px: duas entradas que convergem, hub, uma saída. Mesmo conceito, menos peças."""
    c = _cores(uid, tema, ink)
    if tema == "mono":
        fundo = ""
    elif tema == "dark":
        fundo = f'<rect width="16" height="16" rx="3.6" fill="{C.NOITE}"/>' if tile else ""
    else:
        fundo = f'<rect width="16" height="16" rx="3.6" fill="{C.PAPEL}" stroke="{C.LINHA_CLARA}" stroke-width=".6"/>' if tile else ""
    fino = "1.5"
    inner = (_defs(uid, 16, tema, ink) + fundo
             + f'<path d="M3 4.2C6 4.2 6.6 8 8.6 8" fill="none" stroke="{c["line"]}" stroke-width="{fino}" stroke-linecap="round"/>'
             + f'<path d="M3 11.8C6 11.8 6.6 8 8.6 8" fill="none" stroke="{c["line"]}" stroke-width="{fino}" stroke-linecap="round"/>'
             + f'<path d="M8.6 8H12.2" fill="none" stroke="{c["line"]}" stroke-width="{fino}" stroke-linecap="round"/>'
             + f'<circle cx="3" cy="4.2" r="1.15" fill="{c["node"]}"/><circle cx="3" cy="11.8" r="1.15" fill="{c["node"]}"/>'
             + f'<rect x="11.4" y="6.5" width="3" height="3" rx=".7" fill="{c["node"]}"/>'
             + f'<circle cx="8.6" cy="8" r="2.1" fill="{c["core"] if tema != "mono" else c["line"]}"/>')
    return _envolver(16, inner, extra)


def avatar(tema="dark", uid="a", simbolo="compacto", padding=0.2):
    """Avatar quadrado (LinkedIn, YouTube): símbolo centralizado sobre a base Noite."""
    bg = C.NOITE if tema == "dark" else C.PAPEL
    s = 400 * (1 - 2 * padding)
    o = 400 * padding
    miolo = {"compacto": compacto, "completo": completo}[simbolo](tema, uid=uid, extra=f'x="{_f(o)}" y="{_f(o)}" width="{_f(s)}" height="{_f(s)}"')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" role="img" aria-label="Avatar Nexus Intelligence">'
            f'<rect width="400" height="400" fill="{bg}"/>{miolo}</svg>')


if __name__ == "__main__":
    for n in (completo, compacto, minimo, favicon):
        print(n.__name__, len(n()))
