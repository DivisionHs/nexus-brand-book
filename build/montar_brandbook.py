"""Monta o brand book a partir de partes/*.html, trocando os marcadores por SVG e tabelas gerados.

Marcadores:
  {{@tipo|tema|w=120,class=x}}  figura SVG (tipo: simbolo, compacto, minimo, favicon, avatar, horizontal,
                                 horizontal_completo, empilhado, wordmark, wordmark_nosub, protecao,
                                 guias_wordmark, construcao, padrao, prisma, camadas, grade, ...)
  {{#nome}}                     bloco HTML calculado em figuras.py

Saídas (na pasta acima de build/):
  Nexus-Brand-Book.html   documento autônomo
  build/_artifact.html    versão sem <html>/<head>/<body>, para publicar como artifact
Rodar: python montar_brandbook.py
"""
import re
from pathlib import Path

import cores as C
import simbolo as S
import logotipo as L
import conceitos as K
import figuras as F

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent

TEMAS = {  # nome no template -> (tema, tinta)
    "dark": ("dark", None), "light": ("light", None),
    "monopreto": ("mono", "#000000"), "monobranco": ("mono", "#FFFFFF"),
    "monorosa": ("mono", C.ROSA), "monoink": ("mono", C.TINTA),
}


def figura(tipo, nome_tema, extras):
    tema, tinta = TEMAS[nome_tema]
    uid = f"{tipo}{nome_tema}"[:18]
    kw = dict(tema=tema, uid=uid)
    if tinta:
        kw["ink"] = tinta
    if tipo == "simbolo":
        svg = S.completo(**kw)
    elif tipo == "compacto":
        svg = S.compacto(**kw)
    elif tipo == "minimo":
        svg = S.minimo(**kw)
    elif tipo == "favicon":
        svg = S.favicon(**kw)
    elif tipo == "avatar":
        svg = S.avatar(tema, uid=uid)
    elif tipo == "horizontal":
        svg = L.horizontal(**kw)
    elif tipo == "horizontal_completo":
        svg = L.horizontal(nivel="completo", **kw)
    elif tipo == "empilhado":
        svg = L.empilhado(**kw)
    elif tipo in ("wordmark", "wordmark_nosub"):
        svg = L.wordmark(tema, tinta or C.TINTA, com_sub=(tipo == "wordmark"))
    elif tipo == "protecao":
        svg = F.protecao(uid)
    elif tipo == "guias_wordmark":
        svg = F.guias_wordmark()
    elif tipo == "construcao":
        svg = F.construcao(uid)
    elif tipo == "padrao":
        svg = F.padrao(uid)
    elif tipo == "padrao_banner":
        svg = F.padrao(uid, hub_x=500, opac=.32)
    elif tipo in ("prisma", "camadas", "grade"):
        svg = getattr(K, tipo)("mono" if tema == "mono" else "dark", **({"ink": tinta} if tinta else {}))
    else:
        raise KeyError(tipo)
    attrs = ""
    for par in filter(None, extras.split(",")):
        k, v = par.split("=", 1)
        attrs += f' {"width" if k == "w" else k}="{v}"'
    return svg.replace("<svg ", f"<svg{attrs} ", 1) if attrs else svg


BLOCOS = {
    "contraste_escuro": lambda: F.contraste(C.PARES_ESCURO),
    "contraste_claro": lambda: F.contraste(C.PARES_CLARO),
    "contraste_proibido": F.contraste_proibido,
    "dados_escuro": lambda: F.chips_dados(C.DADOS_ESCURO),
    "dados_claro": lambda: '<div style="background:#fff;border-radius:10px;padding:12px;display:flex;gap:8px;flex-wrap:wrap;color:#0A0B1E">'
                          + F.chips_dados(C.DADOS_CLARO, claro=True).replace("var(--aqua)", "#0B7F8F") + "</div>",
    "status": F.chips_status,
    "cvd_escuro": lambda: F.cvd(C.DADOS_ESCURO),
    "cvd_claro": lambda: F.cvd(C.DADOS_CLARO),
    "distancias": F.distancias,
    "grafico_barras": lambda: F.grafico_barras(),
    "pbi_barras": lambda: F.grafico_barras(),
    "pbi_linhas": lambda: F.grafico_linhas(),
    "lista_arquivos": F.lista_arquivos,
    "json_tema": F.json_tema,
}


def preencher(texto):
    texto = re.sub(r"\{\{@(\w+)\|(\w+)(?:\|([^}]*))?\}\}", lambda m: figura(m.group(1), m.group(2), m.group(3) or ""), texto)
    return re.sub(r"\{\{#(\w+)\}\}", lambda m: BLOCOS[m.group(1)](), texto)


def main():
    partes = sorted((AQUI / "partes").glob("*.html"))
    cabeca = preencher(partes[0].read_text(encoding="utf-8"))
    corpo = "\n".join(preencher(p.read_text(encoding="utf-8")) for p in partes[1:])
    restante = re.findall(r"\{\{[^}]*\}\}", cabeca + corpo)
    if restante:
        raise SystemExit(f"marcadores sem troca: {restante[:5]}")
    # versão para artifact: título e estilos no topo, conteúdo em seguida
    (AQUI / "_artifact.html").write_text(cabeca + "\n" + corpo, encoding="utf-8")
    # versão autônoma: head separado do body
    titulo = re.search(r"<title>.*?</title>", cabeca).group(0)
    resto = cabeca.replace(titulo, "")
    completo = ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
                f'{titulo}\n{resto}\n</head>\n<body>\n{corpo}\n</body>\n</html>\n')
    completo = completo.replace('<meta name="claude:viewport-fit-sides" content="cover">', "")
    (RAIZ / "Nexus-Brand-Book.html").write_text(completo, encoding="utf-8")
    print("ok:", len(completo) // 1024, "KB")


if __name__ == "__main__":
    main()
