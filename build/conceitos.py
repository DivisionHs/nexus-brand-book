"""Esboços dos conceitos comparados no brand book (viewBox 120).

C1 Convergência e ordem: é o símbolo final (simbolo.compacto).
C2 Prisma: facetas em cores de acento.
C3 Camadas: anéis concêntricos, da dispersão ao núcleo.
C4 Grade com N escondido: pontos que se alinham e formam uma estrutura.
Cada função aceita tema "dark" ou "mono" (para mostrar o teste de uma cor só).
"""
from math import cos, sin, radians
import cores as C


def _f(n):
    return f"{n:.2f}".rstrip("0").rstrip(".")


def _svg(inner):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" role="img">{inner}</svg>'


def prisma(tema="dark", ink="#000"):
    cx = cy = 60
    R = 52
    v = [(cx + R * cos(radians(-90 + 60 * k)), cy + R * sin(radians(-90 + 60 * k))) for k in range(6)]
    cores_f = [(C.VIOLETA, .95), (C.VIOLETA, .55), (C.AQUA, .85), (C.VIOLETA, .3), (C.AQUA, .5), (C.VIOLETA, .75)]
    out = []
    for k in range(6):
        a, b = v[k], v[(k + 1) % 6]
        fill, op = cores_f[k] if tema != "mono" else (ink, 1)
        out.append(f'<polygon points="{cx},{cy} {_f(a[0])},{_f(a[1])} {_f(b[0])},{_f(b[1])}" fill="{fill}" fill-opacity="{op}"/>')
    if tema != "mono":
        out.append(f'<circle cx="{cx}" cy="{cy}" r="4.5" fill="{C.ROSA}"/>')
    return _svg("".join(out))


def camadas(tema="dark", ink="#000"):
    lc = C.VIOLETA if tema != "mono" else ink
    ac = C.AQUA if tema != "mono" else ink
    out = []
    for r, op in ((50, .45), (34, .7), (18, 1)):
        out.append(f'<circle cx="60" cy="60" r="{r}" fill="none" stroke="{lc}" stroke-width="2.6" opacity="{op if tema != "mono" else 1}"/>')
    for ang, r, rad in ((-70, 50, 4.4), (-10, 50, 3.6), (50, 50, 4.8), (120, 50, 3.8), (200, 50, 4.2)):
        out.append(f'<circle cx="{_f(60 + r * cos(radians(ang)))}" cy="{_f(60 + r * sin(radians(ang)))}" r="{rad}" fill="{lc}"/>')
    for k in range(6):
        out.append(f'<circle cx="{_f(60 + 34 * cos(radians(-90 + 60 * k)))}" cy="{_f(60 + 34 * sin(radians(-90 + 60 * k)))}" r="3.4" fill="{lc}"/>')
    for k in range(3):
        out.append(f'<circle cx="{_f(60 + 18 * cos(radians(-90 + 120 * k)))}" cy="{_f(60 + 18 * sin(radians(-90 + 120 * k)))}" r="3" fill="{ac}"/>')
    out.append(f'<circle cx="60" cy="60" r="5.5" fill="{ac}"/>')
    return _svg("".join(out))


def grade(tema="dark", ink="#000"):
    xs, ys = (26, 60, 94), (26, 60, 94)
    lc = C.VIOLETA if tema != "mono" else ink
    ac = C.AQUA if tema != "mono" else ink
    linhas = f'M26 94V26L94 94V26'
    out = [f'<path d="{linhas}" fill="none" stroke="{lc}" stroke-width="4.4" stroke-linecap="round" stroke-linejoin="round"/>']
    for x in xs:
        for y in ys:
            principal = (x in (26, 94)) or (x == y)
            out.append(f'<circle cx="{x}" cy="{y}" r="{7 if principal else 4}" fill="{ac if principal else lc}" '
                       f'opacity="{1 if principal or tema == "mono" else .55}"/>')
    return _svg("".join(out))
