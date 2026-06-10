"""Exporta figuras do relatório a partir dos CSVs em dados/."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import LabelEncoder, StandardScaler

ROOT = Path(__file__).resolve().parent.parent
DADOS = ROOT / "dados"
FIGURAS = Path(__file__).resolve().parent / "figuras"
RANDOM_STATE = 42

plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("husl")


def carregar_dados():
    df = pd.read_csv(DADOS / "dataset_completo_analise.csv")
    df_final = pd.read_csv(DADOS / "dataset_final.csv")
    df["pais"] = (
        df_final["nacionalidade"]
        .astype(str)
        .str.extract(r"([A-Z]{3})\s*$", expand=False)
        .fillna(df_final["nacionalidade"].astype(str).str[-3:])
    )
    return df


def fig_valor_mercado(df):
    valores = df["valor_mercado"].dropna()
    mediana = valores.median()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(valores / 1e6, bins=30, color="steelblue", edgecolor="white", alpha=0.85)
    ax.axvline(mediana / 1e6, color="crimson", linestyle="--", linewidth=2,
               label=f"Mediana: € {mediana/1e6:.1f} Mi")
    ax.set_title("Distribuição do Valor de Mercado (Transfermarkt)")
    ax.set_xlabel("Valor de mercado (milhões de euros)")
    ax.set_ylabel("Número de jogadores")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURAS / "01_valor_mercado.png", dpi=150)
    plt.close(fig)


def fig_perfil_posicao(df):
    metricas = ["gols", "assistencias", "desarmes", "passes_prog", "xG"]
    perfil = df.groupby("posicao")[metricas].mean().reindex(["GK", "DF", "MF", "FW"])
    fig, ax = plt.subplots(figsize=(12, 6))
    perfil.plot(kind="bar", ax=ax, width=0.8)
    ax.set_title("Perfil Médio por Posição — Métricas-Chave")
    ax.set_xlabel("Posição")
    ax.set_ylabel("Média na temporada")
    ax.legend(title="Métrica", bbox_to_anchor=(1.02, 1))
    plt.xticks(rotation=0)
    fig.tight_layout()
    fig.savefig(FIGURAS / "02_perfil_posicao.png", dpi=150)
    plt.close(fig)


def fig_nacionalidades(df):
    stats = (
        df.dropna(subset=["valor_mercado"])
        .groupby("pais")
        .agg(valor_medio=("valor_mercado", "mean"), n=("nome", "count"))
        .query("n >= 5")
        .sort_values("valor_medio", ascending=False)
        .head(10)
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(stats.index[::-1], stats["valor_medio"][::-1] / 1e6, color="teal")
    ax.set_title("Top-10 Nacionalidades por Valor Médio (mín. 5 jogadores)")
    ax.set_xlabel("Valor médio (milhões de euros)")
    ax.set_ylabel("Nacionalidade")
    fig.tight_layout()
    fig.savefig(FIGURAS / "03_nacionalidades.png", dpi=150)
    plt.close(fig)


def fig_minutos_liga(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df, x="liga", y="minutos", ax=ax, palette=["#4C72B0", "#DD8452"])
    ax.set_title("Distribuição de Minutos Jogados por Liga")
    ax.set_xlabel("Liga")
    ax.set_ylabel("Minutos na temporada")
    fig.tight_layout()
    fig.savefig(FIGURAS / "04_minutos_liga.png", dpi=150)
    plt.close(fig)


def fig_correlacao(df):
    cols = [
        "minutos", "gols", "assistencias", "xG", "passes_prog", "pct_passes",
        "desarmes", "interceptacoes", "cortes", "chutes", "chutes_gol",
        "defesas_gk", "clean_sheets", "idade",
    ]
    corr = df[cols].corr()
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=ax, square=True)
    ax.set_title("Correlação entre Features de Clusterização")
    fig.tight_layout()
    fig.savefig(FIGURAS / "05_correlacao.png", dpi=150)
    plt.close(fig)


def preparar_cluster(df):
    for col in ["minutos", "idade"]:
        if col == "idade":
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna(0)
    features = [
        "minutos", "gols", "assistencias", "xG", "passes_prog", "pct_passes",
        "desarmes", "interceptacoes", "cortes", "chutes", "chutes_gol",
        "defesas_gk", "clean_sheets", "idade", "posicao_enc",
    ]
    X = StandardScaler().fit_transform(df[features])
    return df, X, features


def fig_elbow_silhouette(df):
    df, X, _ = preparar_cluster(df.copy())
    k_range = range(2, 11)
    inertias, silhouettes = [], []
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
        labels = km.fit_predict(X)
        inertias.append(km.inertia_)
        silhouettes.append(silhouette_score(X, labels))
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].plot(list(k_range), inertias, "o-", color="steelblue")
    axes[0].set_title("Método do Cotovelo (Inércia)")
    axes[0].set_xlabel("Número de clusters (k)")
    axes[0].set_ylabel("Inércia")
    axes[1].plot(list(k_range), silhouettes, "o-", color="darkorange")
    axes[1].set_title("Silhouette Score")
    axes[1].set_xlabel("Número de clusters (k)")
    axes[1].set_ylabel("Silhouette")
    fig.tight_layout()
    fig.savefig(FIGURAS / "06_elbow_silhouette.png", dpi=150)
    plt.close(fig)
    return int(list(k_range)[int(np.argmax(silhouettes))])


def fig_pca_clusters(df, k=3):
    df = df.copy()
    df, X, _ = preparar_cluster(df)
    df["cluster"] = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10).fit_predict(X)
    pca = PCA(n_components=2, random_state=RANDOM_STATE)
    coords = pca.fit_transform(X)
    fig, ax = plt.subplots(figsize=(10, 7))
    scatter = ax.scatter(coords[:, 0], coords[:, 1], c=df["cluster"], cmap="tab10", alpha=0.6, s=30)
    ax.set_title("Clusters de Jogadores (PCA 2D)")
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% variância)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% variância)")
    plt.colorbar(scatter, label="Cluster")
    fig.tight_layout()
    fig.savefig(FIGURAS / "07_pca_clusters.png", dpi=150)
    plt.close(fig)


def fig_feature_importance(df):
    feature_cols = [
        "gols", "assistencias", "xG", "passes_prog", "pct_passes",
        "desarmes", "interceptacoes", "bloqueios", "cortes",
        "chutes", "chutes_gol", "defesas_gk", "pct_defesas", "clean_sheets",
        "idade", "amarelos", "vermelhos", "jogos",
        "posicao_enc", "liga_enc", "avaliacao_fotmob",
    ]
    X = StandardScaler().fit_transform(df[feature_cols].fillna(0))
    y = df["target"]
    rf = RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=RANDOM_STATE)
    rf.fit(X, y)
    imp = pd.Series(rf.feature_importances_, index=feature_cols).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    imp.head(10).plot(kind="barh", ax=ax, color="forestgreen")
    ax.set_title("Top 10 — Importância de Features (Random Forest)")
    ax.set_xlabel("Importância")
    fig.tight_layout()
    fig.savefig(FIGURAS / "08_feature_importance.png", dpi=150)
    plt.close(fig)


def main():
    FIGURAS.mkdir(parents=True, exist_ok=True)
    df = carregar_dados()
    fig_valor_mercado(df)
    fig_perfil_posicao(df)
    fig_nacionalidades(df)
    fig_minutos_liga(df)
    fig_correlacao(df)
    k = fig_elbow_silhouette(df)
    fig_pca_clusters(df, k=k)
    fig_feature_importance(df)
    print(f"Figuras salvas em {FIGURAS} ({len(list(FIGURAS.glob('*.png')))} arquivos)")


if __name__ == "__main__":
    main()
