"""Module for configuring project."""

from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent.parent
DATA_DIR: Path = BASE_DIR / "data"
RAW_DATA_DIR: Path = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"

SELECTED_COLUMNS: dict[str, tuple[str, ...]] = {
    "DATA": ("data", "datetime64[ns]"),
    "CO_ID": ("compra_id", "object"),
    "CL_ID": ("cliente_id", "object"),
    "CL_GENERO": ("genero", "category"),
    "CL_EC": ("estado_civil", "category"),
    "CL_FHL": ("n_filhos", "int"),
    "CL_SEG": ("classe_social", "category"),
    "PR_ID": ("produto_id", "object"),
    "PR_CAT": ("categoria", "category"),
    "PR_NOME": ("produto", "object"),
}

if __name__ == "__main__":
    print("BASE_DIR:", BASE_DIR)
    print("DATA_DIR:", DATA_DIR)
    print("RAW_DATA_DIR:", RAW_DATA_DIR)
    print("PROCESSED_DATA_DIR:", PROCESSED_DATA_DIR)
