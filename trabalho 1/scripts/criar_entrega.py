"""Organiza pasta pipeline/ e cria .zip de entrega."""
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIPELINE = ROOT / "pipeline"
DADOS_SRC = ROOT / "dados"
RELATORIO = ROOT / "relatorio" / "relatorio_tecnico.pdf"
ZIP_NAME = "Integrante1_Sobrenome1_e_Integrante2_Sobrenome2.zip"


def organizar_pipeline():
    dados_dst = PIPELINE / "dados"
    if PIPELINE.exists():
        shutil.rmtree(PIPELINE)
    dados_dst.mkdir(parents=True)

    nb = "trabalho_mineracao_dados.ipynb"
    src = ROOT / nb
    if src.exists():
        shutil.copy2(src, PIPELINE / nb)

    csvs = [
        "transfermarkt_raw.csv",
        "dataset_final.csv",
        "clusters_resumo.csv",
        "metricas_classificacao.csv",
    ]
    for csv in csvs:
        src = DADOS_SRC / csv
        if src.exists():
            shutil.copy2(src, dados_dst / csv)

    print(f"Pipeline organizado em {PIPELINE}")


def criar_zip():
    zip_path = ROOT / ZIP_NAME
    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in PIPELINE.rglob("*"):
            if path.is_file():
                arcname = path.relative_to(ROOT)
                zf.write(path, arcname)
        if RELATORIO.exists():
            zf.write(RELATORIO, RELATORIO.relative_to(ROOT))

    print(f"ZIP criado: {zip_path} ({zip_path.stat().st_size / 1024:.0f} KB)")


def main():
    organizar_pipeline()
    criar_zip()


if __name__ == "__main__":
    main()
