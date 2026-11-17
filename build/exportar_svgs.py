"""Exporta os SVGs da marca para ../svg e o tema do Power BI para ../powerbi.

Cada arquivo é autônomo: ids de gradiente próprios, dimensões explícitas, título e sem fonte externa.
Rodar: python exportar_svgs.py
"""
import json
import re
from pathlib import Path

import cores as C
import simbolo as S
import logotipo as L

RAIZ = Path(__file__).resolve().parent.parent
PRETO = "#000000"
BRANCO = "#FFFFFF"


def finalizar(svg, titulo):
    """Acrescenta largura/altura (a partir do viewBox) e <title>."""
    vb = re.search(r'viewBox="([-\d. ]+)"', svg).group(1).split()
    w, h = float(vb[2]), float(vb[3])
    esc = 1 if w >= 100 else 8
    svg = svg.replace("<svg ", f'<svg width="{round(w * esc)}" height="{round(h * esc)}" ', 1)
    svg = re.sub(r'(<svg [^>]*>)', rf'\1<title>{titulo}</title>', svg, count=1)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + svg + "\n"


def variantes(fn, **kw):
    """Gera as 4 versões: fundo escuro, fundo claro, preto puro, branco puro."""
    return {
        "escuro": fn(tema="dark", uid="x", **kw),
        "claro": fn(tema="light", uid="x", **kw),
        "mono-preto": fn(tema="mono", ink=PRETO, uid="x", **kw),
        "mono-branco": fn(tema="mono", ink=BRANCO, uid="x", **kw),
    }


def main():
    pasta = RAIZ / "svg"
    pasta.mkdir(exist_ok=True)
    arquivos = {}
    grupos = {
        "simbolo-completo": (S.completo, {}),
        "simbolo-compacto": (S.compacto, {}),
        "simbolo-minimo-32": (S.minimo, {}),
        "logo-horizontal": (L.horizontal, {}),
        "logo-horizontal-simbolo-completo": (L.horizontal, {"nivel": "completo"}),
        "logo-empilhado": (L.empilhado, {}),
    }
    for nome, (fn, kw) in grupos.items():
        for var, svg in variantes(fn, **kw).items():
            arquivos[f"{nome}-{var}.svg"] = svg
    # wordmark não tem uid
    for var, args in {"escuro": ("dark", C.TINTA), "claro": ("light", C.TINTA),
                      "mono-preto": ("mono", PRETO), "mono-branco": ("mono", BRANCO)}.items():
        arquivos[f"wordmark-{var}.svg"] = L.wordmark(args[0], args[1])
        arquivos[f"wordmark-sem-intelligence-{var}.svg"] = L.wordmark(args[0], args[1], com_sub=False)
    arquivos["favicon-escuro.svg"] = S.favicon("dark", uid="x")
    arquivos["favicon-claro.svg"] = S.favicon("light", uid="x")
    arquivos["favicon-mono-preto.svg"] = S.favicon("mono", ink=PRETO, uid="x")
    arquivos["avatar-escuro-400.svg"] = S.avatar("dark", uid="x")
    arquivos["avatar-claro-400.svg"] = S.avatar("light", uid="x")
    for nome, svg in arquivos.items():
        (pasta / nome).write_text(finalizar(svg, "Nexus Intelligence"), encoding="utf-8")

    tema = tema_powerbi()
    (RAIZ / "powerbi" / "Nexus-Intelligence-tema.json").write_text(json.dumps(tema, ensure_ascii=False, indent=2), encoding="utf-8")
    print(len(arquivos), "SVGs e 1 tema Power BI gravados em", RAIZ)


def tema_powerbi():
    """Tema de relatório escuro para material da Nexus (nunca de cliente)."""
    cores = [h for _, h in C.DADOS_ESCURO]
    fonte = "Segoe UI"
    return {
        "name": "Nexus Intelligence (escuro)",
        "dataColors": cores,
        "background": C.NOITE,
        "foreground": C.TEXTO,
        "tableAccent": C.VIOLETA,
        "good": C.STATUS[0][1],
        "neutral": C.STATUS[1][1],
        "bad": C.STATUS[2][1],
        "maximum": C.VIOLETA,
        "center": "#B9A8FF",
        "minimum": C.AQUA,
        "null": C.NEUTRO_DADOS[1],
        "textClasses": {
            "callout": {"fontSize": 28, "fontFace": "Segoe UI Semibold", "color": C.TEXTO},
            "title": {"fontSize": 14, "fontFace": "Segoe UI Semibold", "color": C.TEXTO},
            "header": {"fontSize": 12, "fontFace": fonte, "color": C.APOIO},
            "label": {"fontSize": 10, "fontFace": fonte, "color": C.APOIO},
        },
        "visualStyles": {
            "*": {"*": {
                "background": [{"color": {"solid": {"color": C.SUPERFICIE}}, "transparency": 0}],
                "border": [{"show": False}],
                "title": [{"fontColor": {"solid": {"color": C.TEXTO}}, "fontFamily": "Segoe UI Semibold"}],
            }},
        },
    }


if __name__ == "__main__":
    main()
