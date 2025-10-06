import pandas as pd
import os
from ydata_profiling import ProfileReport
from datetime import datetime

ALLOWED_EXT = [".csv", ".xlsx", ".xls"]


def read_dataset(path: str) -> pd.DataFrame:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        return pd.read_csv(path)
    elif ext in [".xlsx", ".xls"]:
        return pd.read_excel(path)
    else:
        raise ValueError("Format non supporté")


def sanitize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    return df


def analyze_dataset(input_path: str, output_dir: str) -> str:
    """
    Reads dataset, runs ydata_profiling and saves an HTML report. Returns path to HTML report.
    """
    os.makedirs(output_dir, exist_ok=True)
    df = read_dataset(input_path)
    df = sanitize_columns(df)

    # Basic checks
    n_rows, n_cols = df.shape

    profile = ProfileReport(df, title="Rapport d'audit automatisé", explorative=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(output_dir, f"report_{timestamp}.html")
    profile.to_file(report_path)

    return report_path