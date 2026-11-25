#!/usr/bin/env python3
"""Gera os cards SVG de estatísticas do perfil (stats/*.svg).

Uso no GitHub Actions:  GITHUB_TOKEN=... python scripts/gerar_cards.py BrunoGTB
Teste local:            python scripts/gerar_cards.py --exemplo
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from html import escape
from pathlib import Path

# ---------- Paleta ----------
# Tirada do avatar em pixel art: fundo preto-arroxeado, roxo neon e tom quente de pele
BG = "#0b0710"
BG_TOPO = "#170d19"
BORDA = "#341d3c"
TITULO = "#a274ff"
ACENTO_1 = "#8b5cf6"
ACENTO_2 = "#612c7f"
QUENTE = "#d78564"
TEXTO = "#ece6f5"
SUAVE = "#9d8fae"
TRILHA = "#221430"
FONTE = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"

LARGURA, ALTURA = 495, 210
IGNORAR_LINGUAGENS = {"Jupyter Notebook"}  # notebooks inflam os bytes
RENOMEAR_LINGUAGENS = {"Hack": "PHP"}  # o linguist às vezes marca PHP como Hack
CORES_FIXAS = {"PHP": "#4F5D95"}
MAX_LINGUAGENS = 6

QUERY = """
query($login: String!) {
  user(login: $login) {
    name
    createdAt
    followers { totalCount }
    pullRequests { totalCount }
    issues { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
      contributionCalendar { totalContributions }
    }
  }
}
"""


def buscar_dados(login: str, token: str) -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "gerar-cards"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if "errors" in payload:
        raise SystemExit(f"Erro na API: {payload['errors']}")
    u = payload["data"]["user"]
    cc = u["contributionsCollection"]

    linguagens: dict[str, dict] = {}
    for repo in u["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            nome = RENOMEAR_LINGUAGENS.get(e["node"]["name"], e["node"]["name"])
            if nome in IGNORAR_LINGUAGENS:
                continue
            cor = CORES_FIXAS.get(nome) or e["node"]["color"] or SUAVE
            item = linguagens.setdefault(nome, {"bytes": 0, "cor": cor})
            item["bytes"] += e["size"]

    criado = datetime.fromisoformat(u["createdAt"].replace("Z", "+00:00"))
    return {
        "nome": u["name"] or login,
        "estrelas": sum(r["stargazerCount"] for r in u["repositories"]["nodes"]),
        "repos": u["repositories"]["totalCount"],
        "seguidores": u["followers"]["totalCount"],
        "prs": u["pullRequests"]["totalCount"],
        "issues": u["issues"]["totalCount"],
        "commits_ano": cc["totalCommitContributions"] + cc["restrictedContributionsCount"],
        "contribuicoes_ano": cc["contributionCalendar"]["totalContributions"],
        "desde": criado.year,
        "linguagens": linguagens,
    }


DADOS_EXEMPLO = {
    "nome": "Bruno Custódio", "estrelas": 12, "repos": 14, "seguidores": 23,
    "prs": 31, "issues": 9, "commits_ano": 486, "contribuicoes_ano": 612, "desde": 2020,
    "linguagens": {
        "Python": {"bytes": 420000, "cor": "#3572A5"}, "Java": {"bytes": 260000, "cor": "#b07219"},
        "JavaScript": {"bytes": 150000, "cor": "#f1e05a"}, "C": {"bytes": 90000, "cor": "#555555"},
        "HTML": {"bytes": 60000, "cor": "#e34c26"}, "CSS": {"bytes": 40000, "cor": "#563d7c"},
        "PHP": {"bytes": 15000, "cor": "#4F5D95"}, "Prolog": {"bytes": 5000, "cor": "#74283c"},
    },
}


def fmt(n: int) -> str:
    return f"{n/1000:.1f}k".replace(".0k", "k") if n >= 1000 else str(n)


def moldura(titulo: str, corpo: str, rotulo: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{LARGURA}" height="{ALTURA}" viewBox="0 0 {LARGURA} {ALTURA}" role="img" aria-label="{escape(rotulo)}">
  <title>{escape(rotulo)}</title>
  <defs>
    <linearGradient id="acento" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{ACENTO_1}"/><stop offset="1" stop-color="{ACENTO_2}"/>
    </linearGradient>
    <linearGradient id="anel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{QUENTE}"/><stop offset="0.45" stop-color="{ACENTO_1}"/><stop offset="1" stop-color="{ACENTO_2}"/>
    </linearGradient>
    <linearGradient id="fundo" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{BG_TOPO}"/><stop offset="1" stop-color="{BG}"/>
    </linearGradient>
  </defs>
  <style>
    text {{ font-family: {FONTE}; }}
    .titulo {{ font-size: 17px; font-weight: 700; fill: {TITULO}; }}
    .rotulo {{ font-size: 13px; fill: {SUAVE}; }}
    .valor {{ font-size: 13px; font-weight: 700; fill: {TEXTO}; }}
    .grande {{ font-size: 26px; font-weight: 800; fill: {TEXTO}; }}
    .pequeno {{ font-size: 11px; fill: {SUAVE}; }}
    .surge {{ animation: surgir .5s ease-out backwards; }}
    @keyframes surgir {{ from {{ opacity: 0; transform: translateX(-6px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes desenhar {{ from {{ stroke-dashoffset: var(--total); }} }}
    @keyframes crescer {{ from {{ transform: scaleX(0); }} }}
  </style>
  <rect x="0.5" y="0.5" width="{LARGURA-1}" height="{ALTURA-1}" rx="12" fill="url(#fundo)" stroke="{BORDA}"/>
  <rect x="0.5" y="0.5" width="4" height="{ALTURA-1}" rx="2" fill="url(#acento)"/>
  <text x="26" y="36" class="titulo">{escape(titulo)}</text>
  <g fill="{ACENTO_1}" opacity="0.55" shape-rendering="crispEdges">
    <rect x="{LARGURA-34}" y="18" width="3" height="9"/><rect x="{LARGURA-37}" y="21" width="9" height="3"/>
    <rect x="{LARGURA-54}" y="32" width="2" height="6"/><rect x="{LARGURA-56}" y="34" width="6" height="2"/>
  </g>
{corpo}
</svg>
"""


def card_estatisticas(d: dict) -> str:
    linhas = [
        ("Commits no último ano", d["commits_ano"]),
        ("Pull requests", d["prs"]),
        ("Repositórios públicos", d["repos"]),
        ("Seguidores", d["seguidores"]),
        ("Estrelas recebidas", d["estrelas"]),
    ]
    corpo = []
    for i, (rotulo, valor) in enumerate(linhas):
        y = 66 + i * 24
        corpo.append(
            f'  <g class="surge" style="animation-delay:{150 + i*120}ms">'
            f'<rect x="26" y="{y-8}" width="6" height="6" fill="{QUENTE}" shape-rendering="crispEdges"/>'
            f'<text x="42" y="{y}" class="rotulo">{rotulo}</text>'
            f'<text x="290" y="{y}" class="valor" text-anchor="end">{fmt(valor)}</text></g>'
        )

    # anel de contribuições
    cx, cy, r = 395, 104, 50
    circ = 2 * 3.14159 * r
    progresso = min(d["contribuicoes_ano"] / 365, 1)  # meta visual: 1 por dia
    corpo.append(f"""  <g class="surge" style="animation-delay:200ms">
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{TRILHA}" stroke-width="9"/>
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#anel)" stroke-width="9" stroke-linecap="round"
      stroke-dasharray="{circ:.1f}" stroke-dashoffset="{circ*(1-progresso):.1f}" transform="rotate(-90 {cx} {cy})"
      style="--total:{circ:.1f}; animation: desenhar 1.2s ease-out"/>
    <text x="{cx}" y="{cy+4}" class="grande" text-anchor="middle">{fmt(d['contribuicoes_ano'])}</text>
    <text x="{cx}" y="{cy+22}" class="pequeno" text-anchor="middle">contribuições</text>
    <text x="{cx}" y="{cy+74}" class="pequeno" text-anchor="middle">no último ano</text>
  </g>""")
    corpo.append(
        f'  <text x="26" y="{ALTURA-16}" class="pequeno">No GitHub desde {d["desde"]}</text>'
    )
    return moldura("Estatísticas no GitHub", "\n".join(corpo), "Estatísticas do GitHub")


def card_linguagens(d: dict) -> str:
    itens = sorted(d["linguagens"].items(), key=lambda kv: kv[1]["bytes"], reverse=True)
    total = sum(v["bytes"] for _, v in itens) or 1
    topo = itens[:MAX_LINGUAGENS]
    resto = sum(v["bytes"] for _, v in itens[MAX_LINGUAGENS:])
    if resto:
        topo.append(("Outras", {"bytes": resto, "cor": "#4a4a57"}))

    x0, largura_barra, y_barra = 26, LARGURA - 52, 58
    corpo = [f'  <clipPath id="barra"><rect x="{x0}" y="{y_barra}" width="{largura_barra}" height="10" rx="5"/></clipPath>',
             f'  <g clip-path="url(#barra)" style="transform-origin:{x0}px 0; animation: crescer .9s ease-out">']
    x = x0
    for nome, v in topo:
        w = largura_barra * v["bytes"] / total
        corpo.append(f'    <rect x="{x:.2f}" y="{y_barra}" width="{w + 0.5:.2f}" height="10" fill="{v["cor"]}"/>')
        x += w
    corpo.append("  </g>")

    for i, (nome, v) in enumerate(topo):
        col, lin = i % 2, i // 2
        lx, ly = 26 + col * 230, 100 + lin * 28
        pct = 100 * v["bytes"] / total
        corpo.append(
            f'  <g class="surge" style="animation-delay:{300 + i*90}ms">'
            f'<circle cx="{lx+5}" cy="{ly-4}" r="5" fill="{v["cor"]}"/>'
            f'<text x="{lx+18}" y="{ly}" class="valor">{escape(nome)}</text>'
            f'<text x="{lx+205}" y="{ly}" class="rotulo" text-anchor="end">{pct:.1f}%</text></g>'
        )
    return moldura("Linguagens mais usadas", "\n".join(corpo), "Linguagens mais usadas")


def main() -> None:
    if "--exemplo" in sys.argv:
        dados = DADOS_EXEMPLO
    else:
        login = sys.argv[1] if len(sys.argv) > 1 else os.environ["GITHUB_REPOSITORY_OWNER"]
        dados = buscar_dados(login, os.environ["GITHUB_TOKEN"])
    saida = Path("stats")
    saida.mkdir(exist_ok=True)
    (saida / "estatisticas.svg").write_text(card_estatisticas(dados), encoding="utf-8")
    (saida / "linguagens.svg").write_text(card_linguagens(dados), encoding="utf-8")
    print("Cards gerados em", saida.resolve())


if __name__ == "__main__":
    main()
