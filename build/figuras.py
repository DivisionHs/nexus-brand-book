"""Figuras e tabelas geradas para o brand book (tudo calculado a partir de cores.py).

Cada função devolve uma string SVG ou HTML pronta para entrar no template.
"""
import html
import json
import re
from math import cos, sin, radians

import cores as C
import simbolo as S
import logotipo as L
import exportar_svgs as E


def _f(n):
    return f"{n:.2f}".rstrip("0").rstrip(".")


def _miolo(svg):
    return re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1)


def _viewbox(svg):
    return [float(v) for v in re.search(r'viewBox="([-\d. ]+)"', svg).group(1).split()]


# ------------------------------------------------------------ figuras do símbolo e do logotipo
def construcao(uid="cons"):
    """Símbolo completo sobre grade de 20, com guias do hub e as três zonas."""
    grade = "".join(f'<path d="M{x} 0V240M0 {x}H240" stroke="{C.LINHA}" stroke-width=".5"/>' for x in range(0, 241, 20))
    zonas = (f'<rect x="0" y="0" width="92" height="240" fill="{C.VIOLETA}" opacity=".07"/>'
             f'<rect x="92" y="0" width="56" height="240" fill="{C.TEXTO}" opacity=".05"/>'
             f'<rect x="148" y="0" width="92" height="240" fill="{C.AQUA}" opacity=".07"/>')
    guias = (f'<circle cx="120" cy="120" r="17" fill="none" stroke="{C.TEXTO}" stroke-width=".6" stroke-dasharray="2 2"/>'
             f'<circle cx="120" cy="120" r="31" fill="none" stroke="{C.TEXTO}" stroke-width=".6" stroke-dasharray="2 2"/>'
             f'<path d="M0 120H240M120 0V240" stroke="{C.ROSA}" stroke-width=".6" stroke-dasharray="3 3" opacity=".7"/>')
    rot = lambda x, t, c: (f'<text x="{x}" y="254" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="7" '
                           f'letter-spacing="1" fill="{c}">{t}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 262" role="img" aria-label="Construção do símbolo">'
            f'{zonas}{grade}{guias}{S.miolo_completo("dark", uid=uid)}'
            f'{rot(46, "DISPERSO", C.VIOLETA)}{rot(120, "HUB", C.TEXTO)}{rot(194, "EM ORDEM", C.AQUA)}</svg>')


def protecao(uid="prot"):
    """Assinatura horizontal com a área de proteção x = metade da altura do N (63/2)."""
    inner = L.horizontal("dark", uid=uid)
    vx, vy, w, h = _viewbox(inner)
    x = 31.5
    tag = f'viewBox="{_f(vx)} {_f(vy)} {_f(w)} {_f(h)}"'
    cantos = "".join(
        f'<rect x="{px}" y="{py}" width="{x}" height="{x}" fill="{C.AQUA}" opacity=".16"/>'
        f'<text x="{px + x / 2}" y="{py + x / 2 + 3}" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="9" fill="{C.AQUA}">x</text>'
        for px, py in [(0, 0), (w + x, 0), (0, h + x), (w + x, h + x)])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_f(w + 2 * x)} {_f(h + 2 * x)}" role="img" aria-label="Área de proteção">'
            f'<rect x=".5" y=".5" width="{_f(w + 2 * x - 1)}" height="{_f(h + 2 * x - 1)}" fill="none" stroke="{C.AQUA}" stroke-width=".8" stroke-dasharray="4 3"/>'
            f'<rect x="{x}" y="{x}" width="{_f(w)}" height="{_f(h)}" fill="none" stroke="{C.APOIO}" stroke-width=".5"/>'
            f'{cantos}<svg x="{x}" y="{x}" width="{_f(w)}" height="{_f(h)}" {tag}>{_miolo(inner)}</svg></svg>')


def guias_wordmark():
    """Wordmark com linhas de base, altura x, maiúscula e altura de 'Intelligence'."""
    def linha(y, t):
        return (f'<path d="M-10 {y}H236" stroke="{C.AQUA}" stroke-width=".5" stroke-dasharray="3 3" opacity=".8"/>'
                f'<text x="-14" y="{y + 2.5}" text-anchor="end" font-family="JetBrains Mono,monospace" font-size="6.5" fill="{C.AQUA}">{t}</text>')
    topo_sub = L._topo_sub()
    guias = (linha(4, "maiúscula 56") + linha(20, "caixa-baixa 40") + linha(60, "base")
             + linha(topo_sub, "Intelligence 14") + linha(topo_sub + 14, ""))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-104 -14 350 120" role="img" aria-label="Anatomia do letreiramento">'
            f'{guias}{L.bloco_texto("dark")}</svg>')


def padrao(uid="pad", hub_x=440, opac=.55):
    """Padrão de convergência para fundos: linhas fracas de muitos pontos para um hub à direita."""
    W, H = 640, 360
    hub = (hub_x, 180)
    R = 16
    seeds = [(28, 30), (90, 78), (40, 130), (150, 40), (120, 160), (60, 205), (190, 110), (30, 290),
             (130, 250), (230, 200), (90, 330), (210, 300), (260, 70), (300, 250)]
    seeds.sort(key=lambda p: p[1])
    n = len(seeds)
    out = [f'<defs><linearGradient id="{uid}g" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0">'
           f'<stop offset="0" stop-color="{C.VIOLETA}"/><stop offset=".6" stop-color="{C.VIOLETA}"/><stop offset="1" stop-color="{C.AQUA}"/></linearGradient>'
           f'<radialGradient id="{uid}r" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{C.VIOLETA}" stop-opacity=".45"/>'
           f'<stop offset="1" stop-color="{C.VIOLETA}" stop-opacity="0"/></radialGradient>'
           f'<pattern id="{uid}p" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".6" fill="{C.TEXTO}" opacity=".12"/></pattern></defs>'
           f'<rect width="{W}" height="{H}" fill="{C.NOITE}"/><rect width="{W}" height="{H}" fill="url(#{uid}p)"/>'
           f'<circle cx="{hub[0]}" cy="{hub[1]}" r="170" fill="url(#{uid}r)"/>']
    for i, (x, y) in enumerate(seeds):
        a = radians(-72 + 144 * i / (n - 1))
        px, py = hub[0] - R * cos(a), hub[1] + R * sin(a)
        k = 0.5 * (px - x)
        out.append(f'<path d="M{x} {y}C{_f(x + k)} {y} {_f(px - cos(a) * k * .6)} {_f(py + sin(a) * k * .6)} {_f(px)} {_f(py)}" fill="none" '
                   f'stroke="url(#{uid}g)" stroke-width="1.4" opacity="{opac}" stroke-linecap="round"/>'
                   f'<circle cx="{x}" cy="{y}" r="{2.2 + (i % 4)}" fill="url(#{uid}g)" opacity=".85"/>')
    fim = W - 46
    comp = fim - (hub[0] + R)
    for dy in (-60, 0, 60):
        x0 = hub[0] + R
        out.append(f'<path d="M{x0} {hub[1]}C{_f(x0 + comp * .3)} {hub[1]} {_f(x0 + comp * .3)} {hub[1] + dy} {_f(x0 + comp * .62)} {hub[1] + dy}L{fim} {hub[1] + dy}" '
                   f'fill="none" stroke="url(#{uid}g)" stroke-width="2" opacity=".8" stroke-linecap="round"/>'
                   f'<rect x="{fim}" y="{hub[1] + dy - 6}" width="12" height="12" rx="2.6" fill="{C.AQUA}"/>')
    out.append(f'<circle cx="{hub[0]}" cy="{hub[1]}" r="{R}" fill="none" stroke="url(#{uid}g)" stroke-width="4"/>'
               f'<circle cx="{hub[0]}" cy="{hub[1]}" r="6" fill="{C.TEXTO}"/><circle cx="{hub[0]}" cy="{hub[1] - R}" r="3.4" fill="{C.ROSA}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" '
            f'style="width:100%;height:100%;max-width:none" aria-hidden="true">{"".join(out)}</svg>')


# ------------------------------------------------------------ gráficos de exemplo (dados fictícios)
def grafico_barras(w=380, h=210, comp=False):
    series = [n for n, _ in C.DADOS_ESCURO[:4]]
    cores = [c for _, c in C.DADOS_ESCURO[:4]]
    meses = ["Jun", "Jul", "Ago", "Set", "Out", "Nov"]
    dados = [[22, 18, 14, 10], [24, 18, 15, 11], [25, 20, 14, 12], [27, 21, 16, 12], [30, 22, 17, 13], [32, 24, 17, 14]]
    ml, mt, mb, mr = 30, 28, 22, 8
    pw, ph = w - ml - mr, h - mt - mb
    teto = 100
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Volume por mês e origem, dados fictícios" font-family="JetBrains Mono,monospace" font-size="9">']
    lx = ml
    for nome, cor in zip(["Fonte A", "Fonte B", "Fonte C", "Fonte D"], cores):
        out.append(f'<rect x="{lx}" y="8" width="9" height="9" rx="2" fill="{cor}"/><text x="{lx + 13}" y="16" fill="{C.APOIO}">{nome}</text>')
        lx += 62
    for t in (0, 25, 50, 75, 100):
        y = mt + ph - ph * t / teto
        out.append(f'<path d="M{ml} {_f(y)}H{w - mr}" stroke="{C.LINHA}" stroke-width=".7"/><text x="{ml - 6}" y="{_f(y + 3)}" text-anchor="end" fill="{C.APOIO}">{t}</text>')
    bw = pw / len(meses) * 0.56
    for i, (m, vs) in enumerate(zip(meses, dados)):
        x = ml + pw / len(meses) * (i + .5) - bw / 2
        base = mt + ph
        for v, cor in zip(vs, cores):
            hh = ph * v / teto
            base -= hh
            out.append(f'<rect x="{_f(x)}" y="{_f(base)}" width="{_f(bw)}" height="{_f(hh - 1)}" rx="1.5" fill="{cor}"/>')
        out.append(f'<text x="{_f(x + bw / 2)}" y="{h - 7}" text-anchor="middle" fill="{C.APOIO}">{m}</text>')
    out.append("</svg>")
    return "".join(out)


def grafico_linhas(w=240, h=210):
    cores = [c for _, c in C.DADOS_ESCURO[:3]]
    pts = [[40, 46, 52, 58, 66, 74], [30, 31, 36, 34, 40, 41], [20, 18, 24, 22, 21, 26]]
    ml, mt, mb, mr = 26, 14, 20, 38
    pw, ph = w - ml - mr, h - mt - mb
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Tendência, dados fictícios" font-family="JetBrains Mono,monospace" font-size="9">']
    for t in (0, 25, 50, 75, 100):
        y = mt + ph - ph * t / 100
        out.append(f'<path d="M{ml} {_f(y)}H{w - mr}" stroke="{C.LINHA}" stroke-width=".7"/><text x="{ml - 6}" y="{_f(y + 3)}" text-anchor="end" fill="{C.APOIO}">{t}</text>')
    for k, (serie, cor) in enumerate(zip(pts, cores)):
        xy = [(ml + pw * i / (len(serie) - 1), mt + ph - ph * v / 100) for i, v in enumerate(serie)]
        d = "M" + "L".join(f"{_f(x)} {_f(y)}" for x, y in xy)
        if k == 0:
            out.append(f'<path d="{d}L{_f(xy[-1][0])} {mt + ph}L{_f(xy[0][0])} {mt + ph}Z" fill="{cor}" opacity=".12"/>')
        out.append(f'<path d="{d}" fill="none" stroke="{cor}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
        out.append(f'<circle cx="{_f(xy[-1][0])}" cy="{_f(xy[-1][1])}" r="3.4" fill="{cor}"/>'
                   f'<text x="{_f(xy[-1][0] + 7)}" y="{_f(xy[-1][1] + 3)}" fill="{cor}">{["A", "B", "C"][k]}</text>')
    for i, m in enumerate(["Jun", "Ago", "Out", "Nov"]):
        out.append(f'<text x="{_f(ml + pw * i / 3)}" y="{h - 5}" text-anchor="middle" fill="{C.APOIO}">{m}</text>')
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------------------ tabelas HTML
def _pill(ok):
    return '<span class="pill ok">passa</span>' if ok else '<span class="pill no">reprova</span>'


def contraste(pares, titulo_col="Par"):
    linhas = []
    for item in pares:
        rot, f, b = item[0], item[1], item[2]
        uso = item[3] if len(item) > 3 else "texto"
        r = C.contraste(f, b)
        if uso == "decorativo":
            sel = '<span class="pill am">decorativo</span>'
        else:
            sel = _pill(r >= 4.5)
        linhas.append(f'<tr><td><span class="sq" style="background:{f}"></span>{html.escape(rot)}</td>'
                      f'<td class="n">{str(f"{r:.1f}").replace(".", ",")}:1</td><td>{sel}</td><td class="n">{_pill(r >= 3)}</td></tr>')
    return (f'<table class="tb" style="min-width:0"><thead><tr><th>{titulo_col}</th><th>Razão</th><th>Texto 4,5:1</th><th>Gráfico 3:1</th></tr></thead>'
            f'<tbody>{"".join(linhas)}</tbody></table>')


def contraste_proibido():
    linhas = []
    for rot, f, b in C.PARES_PROIBIDOS:
        r = C.contraste(f, b)
        linhas.append(f'<tr><td><span class="sq" style="background:{f}"></span>{html.escape(rot)}</td>'
                      f'<td class="n">{str(f"{r:.1f}").replace(".", ",")}:1</td><td>{_pill(r >= 4.5)}</td></tr>')
    return (f'<table class="tb" style="min-width:0"><thead><tr><th>Par</th><th>Razão</th><th>Texto 4,5:1</th></tr></thead>'
            f'<tbody>{"".join(linhas)}</tbody></table>')


def chips_dados(lista, claro=False):
    cor_t = C.TINTA if claro else C.TEXTO
    return "".join(
        f'<div style="display:grid;gap:4px;width:92px"><span style="height:46px;border-radius:8px;background:{h};'
        f'box-shadow:inset 0 0 0 1px rgba({"0,0,0" if claro else "255,255,255"},.14)"></span>'
        f'<b style="font:600 12px var(--f-display);color:{cor_t if False else "inherit"}">{n}</b>'
        f'<button data-copy="{h}" style="all:unset;cursor:pointer;font:500 11px var(--f-mono);color:var(--aqua)">{h}</button></div>'
        for n, h in lista)


def chips_status():
    formas = {
        "Ok": '<circle cx="9" cy="9" r="7" fill="{c}"/>',
        "Atenção": '<path d="M9 2L17 16H1Z" fill="{c}"/>',
        "Crítico": '<rect x="2" y="2" width="14" height="14" rx="2" fill="{c}"/>',
    }
    out = []
    for n, h in C.STATUS:
        out.append(f'<div style="display:grid;gap:4px;width:110px"><svg width="18" height="18" viewBox="0 0 18 18" style="margin-bottom:6px">{formas[n].format(c=h)}</svg>'
                   f'<b style="font:600 12px var(--f-display)">{n}</b><button data-copy="{h}" style="all:unset;cursor:pointer;font:500 11px var(--f-mono);color:var(--aqua)">{h}</button></div>')
    out.append(f'<div style="display:grid;gap:4px;width:110px"><span style="width:18px;height:6px;margin:6px 0 12px;border-radius:3px;background:{C.NEUTRO_DADOS[1]}"></span>'
               f'<b style="font:600 12px var(--f-display)">Outros</b><button data-copy="{C.NEUTRO_DADOS[1]}" style="all:unset;cursor:pointer;font:500 11px var(--f-mono);color:var(--aqua)">{C.NEUTRO_DADOS[1]}</button></div>')
    return "".join(out)


def cvd(lista):
    rot = {"normal": "Visão típica", "protanopia": "Protanopia", "deuteranopia": "Deuteranopia", "tritanopia": "Tritanopia"}
    linhas = []
    for tipo in ("normal", "protanopia", "deuteranopia", "tritanopia"):
        linhas.append(f'<span>{rot[tipo]}</span>' + "".join(f'<span class="q" style="background:{C.simular(h, tipo)}" title="{n}"></span>' for n, h in lista))
    return "".join(linhas)


def distancias():
    rot = {"normal": "Visão típica", "protanopia": "Protanopia", "deuteranopia": "Deuteranopia", "tritanopia": "Tritanopia"}
    linhas = []
    for tipo in ("normal", "protanopia", "deuteranopia", "tritanopia"):
        e = C.menor_distancia(C.DADOS_ESCURO, tipo)
        c = C.menor_distancia(C.DADOS_CLARO, tipo)
        linhas.append(f'<tr><td>{rot[tipo]}</td><td class="n">{e[0]:.1f}</td><td>{e[1]} e {e[2]}</td><td class="n">{c[0]:.1f}</td><td>{c[1]} e {c[2]}</td></tr>')
    return ('<table class="tb"><thead><tr><th>Visão</th><th>Escura, mínimo</th><th>Par mais próximo</th><th>Clara, mínimo</th><th>Par mais próximo</th></tr></thead>'
            f'<tbody>{"".join(linhas)}</tbody></table>')


GRUPOS = [
    ("simbolo-completo", "Símbolo completo, 96 px ou mais"),
    ("simbolo-compacto", "Símbolo compacto, 32 a 95 px"),
    ("simbolo-minimo-32", "Símbolo mínimo, 20 a 31 px"),
    ("logo-horizontal", "Assinatura horizontal, símbolo compacto"),
    ("logo-horizontal-simbolo-completo", "Assinatura horizontal, símbolo completo"),
    ("logo-empilhado", "Assinatura empilhada"),
    ("wordmark", "Logotipo Nexus com Intelligence"),
    ("wordmark-sem-intelligence", "Logotipo só Nexus"),
]


def lista_arquivos():
    linhas = []
    for pref, desc in GRUPOS:
        linhas.append(f'<tr><td class="n">svg/{pref}-<br>[escuro, claro, mono-preto, mono-branco].svg</td><td>{desc}</td></tr>')
    linhas.append('<tr><td class="n">svg/favicon-[escuro, claro, mono-preto].svg</td><td>Favicon de 16 px, com tile</td></tr>')
    linhas.append('<tr><td class="n">svg/avatar-[escuro, claro]-400.svg</td><td>Avatar quadrado de 400 px</td></tr>')
    linhas.append('<tr><td class="n">powerbi/Nexus-Intelligence-tema.json</td><td>Tema de relatório escuro</td></tr>')
    linhas.append('<tr><td class="n">Nexus-Brand-Book.html</td><td>Este documento, autônomo</td></tr>')
    return f'<table class="tb" style="min-width:0"><thead><tr><th>Arquivo</th><th>Uso</th></tr></thead><tbody>{"".join(linhas)}</tbody></table>'


def json_tema():
    return html.escape(json.dumps(E.tema_powerbi(), ensure_ascii=False, indent=2))
