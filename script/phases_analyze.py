"""Analysiere die Start- und Endzeitpunkte der Phasen."""
import pandas as pd


def load_phasen(file_name="phasen.tsv"):
    pf = pd.read_csv(file_name, sep="\t")
    pf = pf.set_index(list(pf.columns[:5]))
    pf = pf.sort_values(["prob_nr", "run", "start"])
    return pf


def group_except(index="prob_nr", pf=None):
    if pf is None:
        pf = load_phasen()
    if isinstance(index, str):
        return mean_over([index], pf=pf)
    assert isinstance(index, list)
    idx = [i for i in pf.index.names if i not in index]
    return pf.groupby(idx, sort=False)


if __name__ == "__main__":
    pf = load_phasen("phasen.tsv")
    runs = group_except(["prob_nr"], pf).mean()
    r1, r2 = runs.loc[1], runs.loc[2]
    print(
        "maximale Abweichung zwischen den Runs",
        abs(r1.values - r2.values).round(3).max(),
    )
