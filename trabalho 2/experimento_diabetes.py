"""
Caso 01 — IA e ciência de dados na saúde
Comparativo: Árvore de Decisão, Naive Bayes Gaussiano e KNN
Dataset: Pima Indians Diabetes (UCI)
Foco clínico: minimizar falsos negativos (maximizar Recall).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    auc,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import (
    GridSearchCV,
    StratifiedKFold,
    cross_validate,
    train_test_split,
)
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier

# -----------------------------------------------------------------------------
# Configuração
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "dados" / "diabetes.csv"
FIG_DIR = BASE_DIR / "figuras"
RESULT_DIR = BASE_DIR / "resultados"

FIG_DIR.mkdir(parents=True, exist_ok=True)
RESULT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42
N_SPLITS = 10  # K-Fold estratificado
TEST_SIZE = 0.20

# Colunas em que 0 no Pima representa valor ausente (não fisiológico)
ZERO_AS_MISSING = [
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
]

SCORING = {
    "accuracy": "accuracy",
    "precision": "precision",
    "recall": "recall",
    "f1": "f1",
    "roc_auc": "roc_auc",
}

sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams.update(
    {
        "figure.dpi": 120,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "font.size": 11,
    }
)


def carregar_dados(path: Path) -> tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    df = pd.read_csv(path)
    df_prep = df.copy()
    df_prep[ZERO_AS_MISSING] = df_prep[ZERO_AS_MISSING].replace(0, np.nan)

    X = df_prep.drop(columns=["Outcome"])
    y = df_prep["Outcome"]
    return X, y, df_prep


def construir_modelos() -> dict[str, Pipeline]:
    """Pipelines com imputação (e Min-Max no KNN) para evitar vazamento no CV."""
    imputer = SimpleImputer(strategy="median")

    dt = Pipeline(
        steps=[
            ("imputer", imputer),
            (
                "clf",
                DecisionTreeClassifier(
                    criterion="gini",
                    max_depth=5,
                    min_samples_leaf=10,
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )

    nb = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("clf", GaussianNB()),
        ]
    )

    knn = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", MinMaxScaler()),
            (
                "clf",
                KNeighborsClassifier(
                    n_neighbors=7,
                    metric="euclidean",
                    weights="distance",
                ),
            ),
        ]
    )

    return {
        "Árvore de Decisão": dt,
        "Naive Bayes (Gaussiano)": nb,
        "KNN": knn,
    }


def avaliar_cv(
    modelos: dict[str, Pipeline],
    X: pd.DataFrame,
    y: pd.Series,
) -> pd.DataFrame:
    cv = StratifiedKFold(
        n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE
    )
    linhas = []

    for nome, pipe in modelos.items():
        scores = cross_validate(
            pipe,
            X,
            y,
            cv=cv,
            scoring=SCORING,
            n_jobs=-1,
            return_train_score=False,
        )
        linha = {"modelo": nome}
        for metrica in SCORING:
            chave = f"test_{metrica}"
            linha[f"{metrica}_media"] = float(np.mean(scores[chave]))
            linha[f"{metrica}_desvio"] = float(np.std(scores[chave]))
        linhas.append(linha)
        print(
            f"{nome:28s} | Recall={linha['recall_media']:.3f}±{linha['recall_desvio']:.3f} "
            f"| F1={linha['f1_media']:.3f}±{linha['f1_desvio']:.3f} "
            f"| AUC={linha['roc_auc_media']:.3f}±{linha['roc_auc_desvio']:.3f}"
        )

    return pd.DataFrame(linhas)


def otimizar_hiperparametros(
    X_train: pd.DataFrame,
    y_train: pd.Series,
) -> dict[str, Pipeline]:
    """GridSearchCV com scoring=recall (prioridade clínica: menos FN)."""
    cv = StratifiedKFold(
        n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE
    )

    grids = {
        "Árvore de Decisão": (
            Pipeline(
                [
                    ("imputer", SimpleImputer(strategy="median")),
                    ("clf", DecisionTreeClassifier(random_state=RANDOM_STATE)),
                ]
            ),
            {
                "clf__criterion": ["gini", "entropy"],
                "clf__max_depth": [3, 4, 5, 6, 8, None],
                "clf__min_samples_leaf": [5, 10, 15, 20],
                "clf__min_samples_split": [2, 10, 20],
            },
        ),
        "Naive Bayes (Gaussiano)": (
            Pipeline(
                [
                    ("imputer", SimpleImputer(strategy="median")),
                    ("clf", GaussianNB()),
                ]
            ),
            {
                "clf__var_smoothing": np.logspace(-11, -7, 5),
            },
        ),
        "KNN": (
            Pipeline(
                [
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", MinMaxScaler()),
                    ("clf", KNeighborsClassifier()),
                ]
            ),
            {
                "clf__n_neighbors": list(range(3, 22, 2)),
                "clf__metric": ["euclidean", "manhattan"],
                "clf__weights": ["uniform", "distance"],
            },
        ),
    }

    melhores: dict[str, Pipeline] = {}
    resumo = []

    for nome, (pipe, param_grid) in grids.items():
        print(f"\n>>> GridSearchCV — {nome} (scoring=recall)")
        search = GridSearchCV(
            pipe,
            param_grid=param_grid,
            scoring="recall",
            cv=cv,
            n_jobs=-1,
            refit=True,
        )
        search.fit(X_train, y_train)
        melhores[nome] = search.best_estimator_
        resumo.append(
            {
                "modelo": nome,
                "best_params": search.best_params_,
                "best_cv_recall": float(search.best_score_),
            }
        )
        print(f"    Melhores params: {search.best_params_}")
        print(f"    Melhor Recall (CV): {search.best_score_:.4f}")

    pd.DataFrame(resumo).to_json(
        RESULT_DIR / "melhores_hiperparametros.json",
        orient="records",
        force_ascii=False,
        indent=2,
    )
    return melhores


def escolher_melhor_modelo(metricas_cv: pd.DataFrame) -> str:
    """Prioriza Recall; em empate, usa F1 e depois AUC."""
    ordenado = metricas_cv.sort_values(
        by=["recall_media", "f1_media", "roc_auc_media"],
        ascending=False,
    )
    return str(ordenado.iloc[0]["modelo"])


def avaliar_holdout(
    modelo: Pipeline,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
) -> dict:
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    if hasattr(modelo, "predict_proba"):
        y_score = modelo.predict_proba(X_test)[:, 1]
    else:
        y_score = modelo.decision_function(X_test)

    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()

    metricas = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred)),
        "recall": float(recall_score(y_test, y_pred)),
        "f1": float(f1_score(y_test, y_pred)),
        "roc_auc": float(roc_auc_score(y_test, y_score)),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }

    fpr, tpr, _ = roc_curve(y_test, y_score)
    metricas["fpr"] = fpr
    metricas["tpr"] = tpr
    metricas["y_pred"] = y_pred
    metricas["y_score"] = y_score
    metricas["cm"] = cm
    return metricas


# -----------------------------------------------------------------------------
# Figuras
# -----------------------------------------------------------------------------
def plot_comparativo_cv(metricas: pd.DataFrame, path: Path) -> None:
    mets = ["recall", "precision", "f1", "roc_auc", "accuracy"]
    labels = ["Recall", "Precision", "F1-Score", "AUC-ROC", "Acurácia"]

    x = np.arange(len(mets))
    width = 0.25
    fig, ax = plt.subplots(figsize=(10, 5.5))

    for i, (_, row) in enumerate(metricas.iterrows()):
        medias = [row[f"{m}_media"] for m in mets]
        desvios = [row[f"{m}_desvio"] for m in mets]
        ax.bar(
            x + i * width,
            medias,
            width,
            yerr=desvios,
            capsize=4,
            label=row["modelo"],
        )

    ax.set_xticks(x + width)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Score (média ± desvio no 10-Fold)")
    ax.set_title("Comparativo dos modelos — Validação Cruzada Estratificada (K=10)")
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def plot_matriz_confusao(cm: np.ndarray, nome_modelo: str, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 5))
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=["Não diabético (0)", "Diabético (1)"],
    )
    disp.plot(ax=ax, cmap="Blues", colorbar=False, values_format="d")
    ax.set_title(f"Matriz de Confusão — {nome_modelo}\n(conjunto de teste)")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def plot_curva_roc(
    fpr: np.ndarray,
    tpr: np.ndarray,
    roc_auc: float,
    nome_modelo: str,
    path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(fpr, tpr, lw=2, label=f"{nome_modelo} (AUC = {roc_auc:.3f})")
    ax.plot([0, 1], [0, 1], "k--", lw=1, label="Classificador aleatório (AUC = 0.50)")
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.05)
    ax.set_xlabel("Taxa de Falsos Positivos (1 − Especificidade)")
    ax.set_ylabel("Taxa de Verdadeiros Positivos (Recall / Sensibilidade)")
    ax.set_title(f"Curva ROC — {nome_modelo}")
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def plot_roc_todos(
    resultados_holdout: dict[str, dict],
    path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 6))
    for nome, res in resultados_holdout.items():
        ax.plot(
            res["fpr"],
            res["tpr"],
            lw=2,
            label=f"{nome} (AUC = {res['roc_auc']:.3f})",
        )
    ax.plot([0, 1], [0, 1], "k--", lw=1, label="Aleatório (AUC = 0.50)")
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.05)
    ax.set_xlabel("Taxa de Falsos Positivos (1 − Especificidade)")
    ax.set_ylabel("Taxa de Verdadeiros Positivos (Recall)")
    ax.set_title("Curvas ROC — comparação dos três modelos (hold-out)")
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def plot_missing_zeros(df_raw: pd.DataFrame, path: Path) -> None:
    """Visualiza quantos zeros (ausentes) existem nas colunas clínicas."""
    contagens = (df_raw[ZERO_AS_MISSING] == 0).sum()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    contagens.sort_values(ascending=False).plot(kind="bar", ax=ax, color="#2c7fb8")
    ax.set_title("Zeros tratados como valores ausentes (Pima Indians Diabetes)")
    ax.set_ylabel("Quantidade de zeros")
    ax.set_xlabel("")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def main() -> None:
    print("=" * 70)
    print("Caso 01 — Experimento comparativo (DT × Naive Bayes × KNN)")
    print("=" * 70)

    X, y, df_prep = carregar_dados(DATA_PATH)
    df_raw = pd.read_csv(DATA_PATH)

    print(f"\nDataset: {df_raw.shape[0]} amostras × {df_raw.shape[1]} colunas")
    print("Distribuição da classe (Outcome):")
    print(y.value_counts(normalize=True).rename("proporção").round(3))
    print("\nValores ausentes após tratar zeros clínicos:")
    print(df_prep[ZERO_AS_MISSING].isna().sum())

    plot_missing_zeros(df_raw, FIG_DIR / "01_zeros_como_ausentes.png")

    # Split hold-out para matriz de confusão / ROC finais (estratificado)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        stratify=y,
        random_state=RANDOM_STATE,
    )
    print(f"\nHold-out: treino={len(X_train)} | teste={len(X_test)}")

    # 1) Modelos baseline (hiperparâmetros razoáveis) + CV
    print("\n--- Validação cruzada (modelos base) ---")
    modelos_base = construir_modelos()
    metricas_base = avaliar_cv(modelos_base, X, y)
    metricas_base.to_csv(RESULT_DIR / "metricas_cv_base.csv", index=False)

    # 2) Otimização com foco em Recall
    print("\n--- Otimização de hiperparâmetros (scoring=recall) ---")
    modelos_otim = otimizar_hiperparametros(X_train, y_train)

    print("\n--- Validação cruzada (modelos otimizados, no conjunto completo) ---")
    metricas_otim = avaliar_cv(modelos_otim, X, y)
    metricas_otim.to_csv(RESULT_DIR / "metricas_cv_otimizados.csv", index=False)

    plot_comparativo_cv(metricas_otim, FIG_DIR / "02_comparativo_cv.png")

    melhor_nome = escolher_melhor_modelo(metricas_otim)
    print(f"\n>>> Modelo recomendado (prioridade Recall): {melhor_nome}")

    # 3) Avaliação hold-out de todos + destaque do melhor
    resultados_holdout: dict[str, dict] = {}
    linhas_holdout = []

    for nome, modelo in modelos_otim.items():
        res = avaliar_holdout(modelo, X_train, X_test, y_train, y_test)
        resultados_holdout[nome] = res
        linhas_holdout.append(
            {
                "modelo": nome,
                "accuracy": res["accuracy"],
                "precision": res["precision"],
                "recall": res["recall"],
                "f1": res["f1"],
                "roc_auc": res["roc_auc"],
                "tn": res["tn"],
                "fp": res["fp"],
                "fn": res["fn"],
                "tp": res["tp"],
            }
        )
        print(
            f"[Hold-out] {nome:28s} | "
            f"P={res['precision']:.3f} R={res['recall']:.3f} "
            f"F1={res['f1']:.3f} AUC={res['roc_auc']:.3f} | "
            f"FN={res['fn']} FP={res['fp']}"
        )

    pd.DataFrame(linhas_holdout).to_csv(
        RESULT_DIR / "metricas_holdout.csv", index=False
    )

    melhor_res = resultados_holdout[melhor_nome]
    print("\n" + classification_report(
        y_test,
        melhor_res["y_pred"],
        target_names=["Não diabético", "Diabético"],
        digits=3,
    ))

    plot_matriz_confusao(
        melhor_res["cm"],
        melhor_nome,
        FIG_DIR / "03_matriz_confusao_melhor.png",
    )
    plot_curva_roc(
        melhor_res["fpr"],
        melhor_res["tpr"],
        melhor_res["roc_auc"],
        melhor_nome,
        FIG_DIR / "04_curva_roc_melhor.png",
    )
    plot_roc_todos(resultados_holdout, FIG_DIR / "05_curvas_roc_todos.png")

    # Matrizes de confusão dos três modelos (painel)
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.2))
    for ax, (nome, res) in zip(axes, resultados_holdout.items()):
        sns.heatmap(
            res["cm"],
            annot=True,
            fmt="d",
            cmap="Blues",
            cbar=False,
            ax=ax,
            xticklabels=["0", "1"],
            yticklabels=["0", "1"],
        )
        ax.set_title(nome)
        ax.set_xlabel("Predito")
        ax.set_ylabel("Real")
    fig.suptitle("Matrizes de Confusão — conjunto de teste", y=1.02)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "06_matrizes_confusao_todos.png")
    plt.close(fig)

    # Resumo textual para o documento
    resumo = {
        "melhor_modelo": melhor_nome,
        "k_fold": N_SPLITS,
        "random_state": RANDOM_STATE,
        "test_size": TEST_SIZE,
        "holdout_melhor": {
            k: melhor_res[k]
            for k in [
                "accuracy",
                "precision",
                "recall",
                "f1",
                "roc_auc",
                "tn",
                "fp",
                "fn",
                "tp",
            ]
        },
        "interpretacao_auc": (
            "Uma AUC de 0.85 significa que, em ~85% dos pares "
            "(um paciente doente, um saudável) escolhidos ao acaso, "
            "o modelo atribui escore maior ao paciente doente."
        ),
    }
    pd.Series(resumo).to_json(
        RESULT_DIR / "resumo_experimento.json",
        force_ascii=False,
        indent=2,
    )

    print("\nFiguras salvas em:", FIG_DIR)
    print("Resultados salvos em:", RESULT_DIR)
    print("Concluído.")


if __name__ == "__main__":
    main()
