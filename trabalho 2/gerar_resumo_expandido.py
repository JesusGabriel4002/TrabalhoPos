"""
Gera o Resumo Expandido (PDF) do Caso 01 no formato do template CSIAAM.
"""

from pathlib import Path

from fpdf import FPDF
from fpdf.enums import XPos, YPos

BASE = Path(__file__).resolve().parent
FIG = BASE / "figuras"
OUT = BASE / "Caso_01_Resumo_Expandido.pdf"
FONT = Path(r"C:\Windows\Fonts")

MC = dict(new_x=XPos.LMARGIN, new_y=YPos.NEXT)


class ResumoPDF(FPDF):
    def __init__(self):
        super().__init__(format="Letter", unit="mm")
        self.set_margins(left=23, top=22, right=23)
        self.set_auto_page_break(auto=True, margin=18)
        self.add_font("Arial", "", str(FONT / "arial.ttf"))
        self.add_font("Arial", "B", str(FONT / "arialbd.ttf"))
        self.add_font("Arial", "I", str(FONT / "ariali.ttf"))
        self.add_font("Arial", "BI", str(FONT / "arialbi.ttf"))

    def titulo(self, texto: str) -> None:
        self.set_font("Arial", "B", 16)
        self.multi_cell(0, 8, texto, align="C", **MC)
        self.ln(4)

    def autores(self, texto: str) -> None:
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 5.5, texto, align="C", **MC)

    def afiliacao(self, texto: str) -> None:
        self.set_font("Arial", "I", 9)
        self.multi_cell(0, 4.5, texto, align="C", **MC)

    def secao(self, texto: str) -> None:
        self.ln(3)
        self.set_font("Arial", "B", 12)
        self.multi_cell(0, 7, texto, align="L", **MC)
        self.ln(1)

    def paragrafo(self, texto: str) -> None:
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 5.4, texto, align="J", **MC)
        self.ln(1.5)

    def caption(self, texto: str) -> None:
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 5, texto, align="C", **MC)
        self.ln(2)

    def figura(self, path: Path, w: float = 145) -> None:
        if not path.exists():
            return
        x = (self.w - w) / 2
        self.image(str(path), x=x, w=w)
        self.ln(2)

    def referencia(self, texto: str) -> None:
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 5, texto, align="L", **MC)
        self.ln(1)


def gerar() -> Path:
    pdf = ResumoPDF()
    pdf.add_page()

    # ---- Cabeçalho (template CSIAAM) ----
    pdf.titulo(
        "Otimização de Diagnóstico em Telemedicina: Comparativo de "
        "Árvore de Decisão, Naive Bayes e KNN no Dataset Pima Indians Diabetes"
    )
    pdf.ln(2)
    pdf.autores("Jesus Gabriel Leiva")
    pdf.afiliacao(
        "Pós-graduação em Ciência de Dados e Inteligência Artificial — "
        "Caso 01: IA e ciência de dados na saúde"
    )
    pdf.afiliacao("Autor para correspondência: jesusgabrielleiva1@gmail.com")
    pdf.ln(6)

    # ---- Resumo ----
    pdf.secao("Resumo")
    pdf.paragrafo(
        "Este trabalho apresenta um experimento comparativo de aprendizado de "
        "máquina clássico para apoio ao diagnóstico precoce de diabetes, "
        "utilizando o dataset Pima Indians Diabetes. Foram avaliados Árvore de "
        "Decisão, Naive Bayes Gaussiano e K-Nearest Neighbors (KNN), com "
        "validação cruzada estratificada (K=10) e otimização de hiperparâmetros "
        "orientada ao Recall, priorizando a redução de falsos negativos — custo "
        "clínico crítico em telemedicina. Zeros fisiologicamente inconsistentes "
        "foram tratados como valores ausentes e imputados por mediana dentro de "
        "pipelines, evitando vazamento de informação. A Árvore de Decisão "
        "(critério Gini, profundidade máxima 4) obteve o melhor compromisso "
        "entre sensibilidade e estabilidade (Recall médio de 0,675 no CV; "
        "Recall 0,722, F1 0,709 e AUC 0,805 no hold-out), sendo recomendada "
        "para integração ao sistema, sobretudo por alinhar desempenho preditivo "
        "à interpretabilidade exigida no setor de saúde."
    )

    # ---- Abstract ----
    pdf.secao("Abstract")
    pdf.paragrafo(
        "This paper presents a comparative classical machine learning experiment "
        "to support early diabetes diagnosis using the Pima Indians Diabetes "
        "dataset. Decision Tree, Gaussian Naive Bayes and K-Nearest Neighbors "
        "were evaluated with stratified 10-fold cross-validation and "
        "recall-oriented hyperparameter tuning, prioritizing false-negative "
        "reduction — a critical clinical cost in telemedicine. Physiologically "
        "implausible zeros were treated as missing values and median-imputed "
        "inside pipelines to prevent information leakage. The Decision Tree "
        "(Gini criterion, max depth 4) achieved the best trade-off between "
        "sensitivity and stability (mean CV recall 0.675; hold-out recall "
        "0.722, F1 0.709 and AUC 0.805) and is recommended for production, "
        "balancing predictive performance with the interpretability required "
        "in healthcare."
    )

    pdf.set_font("Arial", "B", 11)
    pdf.write(5.4, "Palavras-chaves: ")
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(
        0,
        5.4,
        "aprendizado de máquina; diabetes; árvore de decisão; naive bayes; "
        "KNN; validação cruzada; telemedicina.",
        align="J",
        **MC,
    )

    # ---- 1. Introdução / contexto ----
    pdf.secao("1. Introdução")
    pdf.paragrafo(
        "A MedTech Solutions demanda um classificador robusto para suporte ao "
        "diagnóstico em telemedicina, com ênfase em minimizar falsos negativos: "
        "deixar de identificar um paciente diabético implica risco clínico "
        "elevado. O conjunto Pima Indians Diabetes, do repositório UCI, contém "
        "768 registros femininos com atributos clínicos contínuos (glicose, "
        "pressão arterial, IMC, insulina, espessura da pele, pedigrí de "
        "diabetes e idade) e o número de gestações, além do rótulo binário "
        "Outcome. Cerca de 34,9% das amostras pertencem à classe positiva, "
        "configurando desbalanceamento moderado que motiva validação "
        "estratificada e métricas além da acurácia."
    )
    pdf.paragrafo(
        "O experimento compara três famílias clássicas — Árvore de Decisão, "
        "Naive Bayes e KNN — documentando escolhas metodológicas, "
        "comportamento sob as condições dos dados e recomendação para "
        "produção, sem tratar os modelos como caixa-preta."
    )

    # ---- 2. Metodologia de validação ----
    pdf.secao("2. Metodologia de Validação")
    pdf.paragrafo(
        "Dada a natureza finita do conjunto (n=768), adotou-se Stratified "
        "K-Fold Cross Validation com K=10. Esse valor é o padrão empírico "
        "para conjuntos de porte similar: cada fold de teste contém cerca de "
        "77 amostras, o que estabiliza a estimativa sem reduzir excessivamente "
        "o conjunto de treino (como ocorreria em leave-one-out). A "
        "estratificação preserva a proporção das classes em cada partição, "
        "evitando folds atípicos da classe minoritária."
    )
    pdf.paragrafo(
        "A validação cruzada mitiga o viés de um único particionamento "
        "arbitráio treino/teste e permite estimar a variância do erro de "
        "generalização (média ± desvio entre folds), tornando o desempenho "
        "reportado mais representativo. Complementarmente, reservou-se um "
        "hold-out estratificado de 20% (random_state=42) para matriz de "
        "confusão, Precision, Recall, F1-Score, curva ROC e AUC do modelo "
        "final, após seleção de hiperparâmetros no conjunto de treino via "
        "GridSearchCV com scoring=recall."
    )
    pdf.paragrafo(
        "Pré-processamento: zeros em Glucose, BloodPressure, SkinThickness, "
        "Insulin e BMI foram interpretados como ausências (não como valores "
        "clínicos) e imputados pela mediana. Imputação e, no KNN, "
        "normalização Min-Max foram encapsuladas em Pipeline do scikit-learn, "
        "ajustadas apenas nos folds de treino, prevenindo vazamento."
    )

    pdf.figura(FIG / "01_zeros_como_ausentes.png", w=130)
    pdf.caption(
        "Figura 1: Quantidade de zeros tratados como valores ausentes nas "
        "variáveis clínicas do Pima Indians Diabetes."
    )

    # ---- 3. Modelos ----
    pdf.secao("3. Engenharia e Seleção de Modelos")

    pdf.set_font("Arial", "BI", 11)
    pdf.multi_cell(0, 5.4, "3.1 Árvores de Decisão", align="L", **MC)
    pdf.ln(1)
    pdf.paragrafo(
        "A impureza dos nós foi avaliada por Índice de Gini e Entropia de "
        "Shannon: ambos medem homogeneidade da classe e guiam a escolha do "
        "atributo de divisão que mais reduz a impureza. O Gini tende a "
        "favorecer partições com classes majoritárias mais puras; a Entropia "
        "penaliza mais misturas equilibradas. A restrição de profundidade "
        "(max_depth) e o mínimo de amostras por folha (min_samples_leaf) "
        "atuam como regularização / pós-poda, limitando a capacidade de "
        "memorizar o treino e reduzindo overfitting — especialmente relevante "
        "em dados clínicos ruidosos e com n moderado. O melhor arranjo "
        "encontrado foi criterion=gini, max_depth=4, min_samples_leaf=20."
    )

    pdf.set_font("Arial", "BI", 11)
    pdf.multi_cell(0, 5.4, "3.2 Naive Bayes", align="L", **MC)
    pdf.ln(1)
    pdf.paragrafo(
        "Optou-se pelo Naive Bayes Gaussiano, adequado a atributos contínuos; "
        "o Multinomial é voltado a contagens/frequências (ex.: texto) e não "
        "casa com o perfil do Pima. A hipótese de independência condicional "
        "dos atributos, dadas as classes, é frequentemente violada em dados "
        "clínicos (ex.: glicose correlacionada a IMC e idade). Na prática, "
        "essa simplificação pode degradar as estimativas de probabilidade, "
        "mas o classificador permanece competitivo quando as margens de "
        "decisão são favoráveis. Ajuste fino de var_smoothing teve impacto "
        "marginal; o Recall médio no CV ficou em 0,601."
    )

    pdf.set_font("Arial", "BI", 11)
    pdf.multi_cell(0, 5.4, "3.3 KNN", align="L", **MC)
    pdf.ln(1)
    pdf.paragrafo(
        "O KNN é sensível à escala: variáveis com maior amplitude (ex.: "
        "Insulina) dominariam a distância sem normalização. Aplicou-se "
        "Min-Max para mapear cada atributo ao intervalo [0,1]. O "
        "hiperparâmetro K controla o compromisso viés–variância: K pequeno "
        "produz fronteiras irregulares e maior sensibilidade a ruído; K "
        "maior suaviza a decisão. A métrica Euclidiana enfatiza diferenças "
        "globais em todas as dimensões; a Manhattan é mais robusta a "
        "desvios em poucas coordenadas. O melhor conjunto foi K=5, "
        "métrica euclidiana e pesos uniformes."
    )

    # ---- 4. Resultados ----
    pdf.secao("4. Avaliação de Performance")
    pdf.paragrafo(
        "A Tabela 1 resume o desempenho médio (± desvio) no Stratified "
        "10-Fold. A Árvore de Decisão liderou em Recall (0,675 ± 0,133), "
        "métrica prioritária do Dr. Arnaldo, com AUC competitiva "
        "(0,813 ± 0,052). Naive Bayes e KNN apresentaram Recall inferior, "
        "embora a acurácia dos três fique em faixa semelhante (~0,74–0,75), "
        "ilustrando por que a acurácia sozinha é insuficiente em cenário "
        "clínico desbalanceado."
    )

    # Tabela CV
    pdf.set_font("Arial", "B", 9)
    col_w = [42, 22, 24, 22, 22, 22]
    headers = ["Modelo", "Acurácia", "Precision", "Recall", "F1", "AUC"]
    rows = [
        ["Árvore de Decisão", "0,741±0,05", "0,640±0,10", "0,675±0,13", "0,642±0,06", "0,813±0,05"],
        ["Naive Bayes", "0,746±0,06", "0,661±0,12", "0,601±0,11", "0,622±0,09", "0,813±0,06"],
        ["KNN", "0,750±0,06", "0,654±0,10", "0,612±0,09", "0,631±0,09", "0,794±0,06"],
    ]
    pdf.set_fill_color(230, 230, 230)
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 6, h, border=1, align="C", fill=True)
    pdf.ln()
    pdf.set_font("Arial", "", 8)
    for row in rows:
        for i, val in enumerate(row):
            pdf.cell(col_w[i], 6, val, border=1, align="C")
        pdf.ln()
    pdf.ln(1)
    pdf.caption(
        "Tabela 1: Métricas médias (± desvio) na validação cruzada "
        "estratificada (K=10) após otimização orientada ao Recall."
    )

    pdf.figura(FIG / "02_comparativo_cv.png", w=150)
    pdf.caption(
        "Figura 2: Comparativo dos modelos na validação cruzada estratificada "
        "(K=10)."
    )

    pdf.paragrafo(
        "No hold-out (154 amostras; 54 diabéticas), a Árvore alcançou "
        "Precision=0,696, Recall=0,722, F1=0,709 e AUC=0,805, com matriz "
        "TN=83, FP=17, FN=15 e TP=39. Ou seja, 15 pacientes diabéticos não "
        "foram sinalizados — desempenho superior ao Naive Bayes (FN=20) e "
        "ao KNN (FN=24) no mesmo particionamento. O Recall permanece a "
        "métrica-chave: mede a fração de doentes corretamente identificados "
        "e, portanto, a capacidade de evitar o erro clinicamente mais grave."
    )

    pdf.figura(FIG / "03_matriz_confusao_melhor.png", w=100)
    pdf.caption(
        "Figura 3: Matriz de confusão da Árvore de Decisão no conjunto de teste."
    )

    pdf.figura(FIG / "04_curva_roc_melhor.png", w=115)
    pdf.caption(
        "Figura 4: Curva ROC da Árvore de Decisão (AUC = 0,805)."
    )

    pdf.paragrafo(
        "Em termos práticos para a diretoria: uma AUC de 0,85 significaria "
        "que, em aproximadamente 85% dos pares formados por um paciente "
        "doente e um saudável escolhidos ao acaso, o modelo atribui escore "
        "maior ao paciente doente — evidência de boa capacidade de "
        "ranqueamento diagnóstico. No experimento, a Árvore atingiu AUC "
        "0,805 (próxima a esse patamar ilustrativo), enquanto Naive Bayes "
        "e KNN ficaram em 0,765 e 0,774, respectivamente (Figura 5)."
    )

    pdf.figura(FIG / "05_curvas_roc_todos.png", w=120)
    pdf.caption(
        "Figura 5: Curvas ROC dos três modelos no hold-out estratificado."
    )

    pdf.figura(FIG / "06_matrizes_confusao_todos.png", w=155)
    pdf.caption(
        "Figura 6: Matrizes de confusão comparativas no conjunto de teste."
    )

    # ---- 5. Conclusão ----
    pdf.secao("5. Conclusão")
    pdf.paragrafo(
        "Recomenda-se a Árvore de Decisão para produção no cenário da "
        "MedTech Solutions. Ela apresentou o melhor Recall na validação "
        "cruzada e no hold-out, reduzindo falsos negativos em relação às "
        "alternativas, com AUC competitiva. Do ponto de vista de "
        "governança em saúde, a árvore oferece interpretabilidade intrínseca "
        "(regras explícitas de decisão), favorecendo auditoria clínica e "
        "explicabilidade regulatória — vantagem frente ao KNN (baseado em "
        "instâncias) e ao Naive Bayes (probabilidades sob hipótese forte de "
        "independência). O trade-off entre transparência e capacidade "
        "preditiva, neste dataset e sob a restrição de minimizar FN, "
        "favorece a árvore regularizada (profundidade limitada), que evita "
        "sobreajuste sem abrir mão de desempenho."
    )
    pdf.paragrafo(
        "Limitações: o Pima é relativamente pequeno e datado; zeros "
        "imputados (especialmente Insulina e SkinThickness) introduzem "
        "incerteza; e o limiar de decisão padrão (0,5) pode ser recalibrado "
        "para elevar ainda mais o Recall, às custas de Precision. Como "
        "próximos passos, sugerem-se calibração de probabilidade, análise "
        "de custo clínico assimétrico e validação externa em coortes "
        "contemporâneas antes da integração definitiva ao fluxo de "
        "telemedicina."
    )

    # ---- Referências ----
    pdf.secao("Referências")
    pdf.referencia("Materiais disponibilizados pelo professor.")

    pdf.output(str(OUT))
    return OUT


if __name__ == "__main__":
    path = gerar()
    print(f"PDF gerado: {path}")
