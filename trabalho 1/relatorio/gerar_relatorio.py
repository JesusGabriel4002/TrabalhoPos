"""Gera relatório técnico PDF a partir dos resultados e figuras."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fpdf import FPDF
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent.parent
DADOS = ROOT / "dados"
FIGURAS = Path(__file__).resolve().parent / "figuras"
OUTPUT = Path(__file__).resolve().parent / "relatorio_tecnico.pdf"
FONT_DIR = Path(r"C:\Windows\Fonts")


class RelatorioPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("Arial", "", str(FONT_DIR / "arial.ttf"))
        self.add_font("Arial", "B", str(FONT_DIR / "arialbd.ttf"))
        self.add_font("Arial", "I", str(FONT_DIR / "ariali.ttf"))
        self.set_auto_page_break(auto=True, margin=20)

    def titulo_secao(self, texto):
        self.set_font("Arial", "B", 14)
        self.multi_cell(0, 8, texto)
        self.ln(2)

    def paragrafo(self, texto):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 6, texto)
        self.ln(2)

    def figura(self, caminho, w=170):
        if Path(caminho).exists():
            self.image(str(caminho), w=w)
            self.ln(4)


def gerar_confusion_matrix_fig(df):
    feature_cols = [
        "gols", "assistencias", "xG", "passes_prog", "pct_passes",
        "desarmes", "interceptacoes", "bloqueios", "cortes",
        "chutes", "chutes_gol", "defesas_gk", "pct_defesas", "clean_sheets",
        "idade", "amarelos", "vermelhos", "jogos",
        "posicao_enc", "liga_enc", "avaliacao_fotmob",
    ]
    X = StandardScaler().fit_transform(df[feature_cols].fillna(0))
    y = df["target"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    modelos = {
        "Random Forest": RandomForestClassifier(
            n_estimators=100, class_weight="balanced", random_state=42
        ),
        "Regressão Logística": LogisticRegression(
            class_weight="balanced", max_iter=1000, random_state=42
        ),
    }
    for ax, (nome, modelo) in zip(axes, modelos.items()):
        modelo.fit(X, y)
        y_pred = modelo.predict(X)
        cm = confusion_matrix(y, y_pred)
        disp = ConfusionMatrixDisplay(cm, display_labels=["Rotação (0)", "Titular (1)"])
        disp.plot(ax=ax, cmap="Blues", colorbar=False)
        ax.set_title(nome)
    fig.tight_layout()
    path = FIGURAS / "09_matrizes_confusao.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def tabela_metricas(pdf, metricas_df):
    pdf.set_font("Arial", "B", 10)
    cols = ["Modelo", "Acurácia", "Precisão", "Recall", "F1-Score"]
    widths = [55, 30, 30, 30, 30]
    for w, c in zip(widths, cols):
        pdf.cell(w, 8, c, border=1, align="C")
    pdf.ln()
    pdf.set_font("Arial", "", 10)
    for _, row in metricas_df.iterrows():
        pdf.cell(55, 8, str(row["Modelo"]), border=1)
        for col in cols[1:]:
            pdf.cell(30, 8, f"{row[col]:.4f}", border=1, align="C")
        pdf.ln()


def tabela_clusters(pdf, clusters_df):
    nomes = {0: "Meias/Rotacionados", 1: "Atacantes/Ofensivos", 2: "Goleiros"}
    pdf.set_font("Arial", "B", 9)
    headers = ["Cluster", "Nome", "N", "Gols", "xG", "Min", "Defesas GK", "Valor médio (Mi)"]
    widths = [18, 42, 12, 18, 18, 22, 28, 34]
    for w, h in zip(widths, headers):
        pdf.cell(w, 8, h, border=1, align="C")
    pdf.ln()
    pdf.set_font("Arial", "", 9)
    for _, row in clusters_df.iterrows():
        c = int(row["cluster"])
        pdf.cell(18, 8, str(c), border=1, align="C")
        pdf.cell(42, 8, nomes.get(c, row["nome_cluster"]), border=1)
        pdf.cell(12, 8, str(int(row["n_jogadores"])), border=1, align="C")
        pdf.cell(18, 8, f"{row['gols']:.1f}", border=1, align="C")
        pdf.cell(18, 8, f"{row['xG']:.1f}", border=1, align="C")
        pdf.cell(22, 8, f"{row['minutos']:.0f}", border=1, align="C")
        pdf.cell(28, 8, f"{row['defesas_gk']:.1f}", border=1, align="C")
        pdf.cell(34, 8, f"{row['valor_mercado']/1e6:.1f}", border=1, align="C")
        pdf.ln()


def main():
    df = pd.read_csv(DADOS / "dataset_completo_analise.csv")
    metricas = pd.read_csv(DADOS / "metricas_classificacao.csv")
    clusters = pd.read_csv(DADOS / "clusters_resumo.csv")
    cm_path = gerar_confusion_matrix_fig(df)

    pdf = RelatorioPDF()
    pdf.add_page()

    # Capa
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 12, "Relatório Técnico", ln=True, align="C")
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Mineração de Dados — Pitch Intelligence", ln=True, align="C")
    pdf.ln(6)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, "Universidade de Marília (UNIMAR)", ln=True, align="C")
    pdf.cell(0, 8, "Integrante 1 Sobrenome1 | Integrante 2 Sobrenome2", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "I", 11)
    pdf.multi_cell(
        0, 6,
        "Sistema de apoio à decisão para convocações da Copa do Mundo FIFA 2026, "
        "integrando dados do FBref (Big 5 + Brasileirão) e valor de mercado do Transfermarkt.",
        align="C",
    )

    # 1. Introdução
    pdf.add_page()
    pdf.titulo_secao("1. Introdução")
    pdf.paragrafo(
        "A startup fictícia Pitch Intelligence foi contratada por uma federação nacional para "
        "desenvolver um pipeline de inteligência esportiva. O objetivo pedagógico deste trabalho "
        "é percorrer todas as etapas de um projeto real de mineração de dados: coleta, integração, "
        "limpeza, exploração, modelagem e interpretação."
    )
    pdf.paragrafo(
        "O dataset combina estatísticas de 2.953 jogadores das cinco maiores ligas europeias e do "
        "Campeonato Brasileiro (temporada 2025-26), enriquecidas com valor de mercado do Transfermarkt "
        "para os ~500 jogadores mais valiosos do mundo."
    )

    # 2. Etapa 1
    pdf.add_page()
    pdf.titulo_secao("2. Etapa 1 — Construção da Base de Dados")
    pdf.paragrafo(
        "Fonte 1 (FBref): arquivo fbref_big5_brasileirao_2526_V2.csv carregado com pandas, "
        "contendo 123 colunas (FBref + FotMob). Fonte 2 (Transfermarkt): raspagem de 8 páginas "
        "com BeautifulSoup e requests, respeitando User-Agent e pausa de 2 segundos entre páginas."
    )
    pdf.paragrafo(
        "Desafios: (1) normalização de nomes com unicodedata e remoção de acentos para o merge; "
        "(2) conversão de valores como '€ 200.00 mi.' para float em euros; "
        "(3) cobertura parcial do Transfermarkt (~6,7% dos jogadores FBref)."
    )
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "Estatísticas do merge:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 6, "• Jogadores FBref (base): 2.953", ln=True)
    pdf.cell(0, 6, "• Jogadores Transfermarkt: 200", ln=True)
    pdf.cell(0, 6, "• Com valor de mercado: 197 (6,7%)", ln=True)
    pdf.cell(0, 6, "• Validação HTML goleiros Brasileirão: 33 (HTML) vs 32 (CSV)", ln=True)
    pdf.ln(4)

    # 3. Etapa 2
    pdf.add_page()
    pdf.titulo_secao("3. Etapa 2 — Pré-processamento e EDA")
    pdf.paragrafo(
        "Posição simplificada pela primeira sigla (ex.: 'DF,MF' → DF). Estatísticas posicionais "
        "ausentes foram preenchidas com 0 (goleiro sem xG, atacante sem defesas). xG e avaliação "
        "FotMob ausentes foram imputados pela mediana da posição."
    )
    pdf.figura(FIGURAS / "01_valor_mercado.png")
    pdf.paragrafo(
        "Interpretação: apenas 6,7% dos jogadores possuem valor no Transfermarkt (top mundial). "
        "A mediana reflete o mercado de elite — jogadores abaixo dessa faixa podem ser "
        "oportunidades subvalorizadas para a federação."
    )

    pdf.add_page()
    pdf.figura(FIGURAS / "02_perfil_posicao.png")
    pdf.paragrafo(
        "Interpretação: atacantes concentram gols e xG; meias lideram em volume defensivo "
        "(interceptações); a separação por posição valida a estratégia de zeros posicionais."
    )
    pdf.figura(FIGURAS / "03_nacionalidades.png", w=160)
    pdf.paragrafo(
        "Interpretação: nacionalidades europeias e sul-americanas dominam o valor médio, "
        "refletindo concentração de talentos nas Big 5."
    )

    pdf.add_page()
    pdf.figura(FIGURAS / "04_minutos_liga.png", w=150)
    pdf.paragrafo(
        "Interpretação: Big5 e Brasileirão têm medianas de minutos comparáveis, mas o Brasileirão "
        "pode ter mais ausências em stats avançadas (cobertura Opta menor)."
    )
    pdf.figura(FIGURAS / "05_correlacao.png", w=160)
    pdf.paragrafo(
        "Interpretação: gols e xG correlacionam fortemente; métricas de goleiro são ortogonais "
        "às ofensivas, favorecendo separação em clusters."
    )

    # 4. Etapa 3
    pdf.add_page()
    pdf.titulo_secao("4. Etapa 3 — Clusterização")
    pdf.paragrafo(
        "K-Means com StandardScaler sobre 15 features (incluindo zeros posicionais). "
        "Escolha de k=3 via Silhouette Score (complementado pelo método do cotovelo)."
    )
    pdf.figura(FIGURAS / "06_elbow_silhouette.png", w=160)
    tabela_clusters(pdf, clusters)
    pdf.ln(4)
    pdf.paragrafo(
        "Cluster 0 (Meias/Rotacionados): 2.403 jogadores, ~1.009 min, poucos gols — elenco de rotação. "
        "Cluster 1 (Atacantes/Ofensivos): 439 jogadores, ~2.019 min, 6,5 gols e 6,3 xG. "
        "Cluster 2 (Goleiros): 111 jogadores, 79 defesas e 7,6 clean sheets em média."
    )
    pdf.figura(FIGURAS / "07_pca_clusters.png", w=160)

    # 5. Etapa 4
    pdf.add_page()
    pdf.titulo_secao("5. Etapa 4 — Classificação")
    pdf.paragrafo(
        "Target binário: minutos > mediana (1.025) = Titular Regular (1) vs Rotação/Reserva (0). "
        "Classes balanceadas (~50/50). Excluídos das features: minutos, 90s, starts, valor_mercado."
    )
    pdf.paragrafo(
        "Modelos: Random Forest e Regressão Logística com class_weight='balanced' e "
        "StratifiedKFold (k=5)."
    )
    tabela_metricas(pdf, metricas)
    pdf.ln(4)
    pdf.figura(cm_path, w=160)
    pdf.figura(FIGURAS / "08_feature_importance.png", w=160)
    pdf.paragrafo(
        "A variável 'jogos' (partidas disputadas) é a mais importante (33%), correlacionando "
        "fortemente com minutos — o que pode inflacionar as métricas (~92%). Isso deve ser "
        "considerado como limitação metodológica."
    )
    pdf.paragrafo(
        "Reflexão Precisão vs Recall: falso negativo (titular não identificado) é mais crítico "
        "para a Copa do Mundo do que falso positivo — priorizar Recall na escolha do modelo."
    )

    # 6. Etapa 5
    pdf.add_page()
    pdf.titulo_secao("6. Etapa 5 — Recomendação Estratégica")
    pdf.paragrafo(
        "Um elenco equilibrado para a Copa deve combinar os três perfis identificados: "
        "goleiros titulares (Cluster 2), meias/defensores de volume (Cluster 0) e "
        "atacantes ofensivos (Cluster 1)."
    )
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "Jogadores citados (Nível Copa):", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(
        0, 6,
        "• Akor Adams (Sevilla, FW): 1.947 min, 10 gols, xG 10,0, cluster Atacantes, "
        "probabilidade titular 100%. Contribuição ofensiva consistente com alta expectativa de gols.\n"
        "• Michel Aebischer (Pisa, MF): 2.742 min, 33 interceptações, titular regular apesar do "
        "perfil de rotação — volume defensivo elevado.\n"
        "• Fábio (Fluminense, GK): 1.350 min, cluster Goleiros — referência do Brasileirão "
        "para análise do mercado local."
    )
    pdf.ln(4)
    pdf.titulo_secao("7. Limitações")
    pdf.paragrafo(
        "• Target proxy (minutos) não captura qualidade tática ou momento de forma.\n"
        "• Merge Transfermarkt cobre apenas 6,7% dos jogadores.\n"
        "• Feature 'jogos' correlacionada com target pode inflacionar acurácia.\n"
        "• Ausência de dados de lesões, vídeo e scouting subjetivo.\n"
        "• Cobertura Opta menor no Brasileirão pode enviesar comparações."
    )

    pdf.titulo_secao("8. Conclusão")
    pdf.paragrafo(
        "O pipeline integra com sucesso dados heterogêneos, identifica perfis táticos via "
        "clusterização não supervisionada e classifica jogadores como titulares regulares "
        "com acurácia superior a 92%. As visualizações e métricas fornecem subsídio concreto "
        "para decisões de convocação, reconhecendo limitações que um sistema profissional "
        "de scouting deveria complementar."
    )

    pdf.output(str(OUTPUT))
    print(f"Relatório salvo em {OUTPUT}")


if __name__ == "__main__":
    main()
