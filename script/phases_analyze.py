"""Analysiere die Start- und Endzeitpunkte der Phasen."""
import pandas as pd


def load_phasen(file_name="phasen.tsv", means=True):
    pf = pd.read_csv(file_name, sep="\t")
    pf = pf.set_index(list(pf.columns[:5]))
    pf = pf.sort_values(["prob_nr", "run", "start"])
    if means:
        return pf.groupby(level=[1, 2, 3, 4], sort=False).mean()
    return pf


if __name__ == "__main__":
    runs = load_phasen("phasen.tsv", means=True)
    r1, r2 = runs.loc[1], runs.loc[2]
    print(
        "maximale Abweichung zwischen den Runs",
        abs(r1.values - r2.values).round(3).max(),
    )
    runs.round(3).to_html("phasen_zeiten.html")
