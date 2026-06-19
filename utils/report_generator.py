import pandas as pd


def generate_csv(results):

    df = pd.DataFrame(
        results
    )

    file_path = (
        "reports/report.csv"
    )

    df.to_csv(
        file_path,
        index=False
    )

    return file_path