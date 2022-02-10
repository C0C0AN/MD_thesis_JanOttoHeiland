"""
Analysiere die Phasen (wann wurde welcher Aufgabentyp gelöst?).
Frage: ist dies bei jedem Probanden ungefährt gleich?
"""
from os import path
import pandas as pd


PREFIX = "/media/jan/Elements"
EXPERIMENT_TYPE = ["stress_run-1", "stress_run-2", "rest"]


def get_tsv(nr=3, exp=0):
    """Dateinamen für ein Probanden mit `nr` und Experimenttyp `exp`
    oder `None`, falls Datei nicht vorhanden.
    """
    prob = "sub-{nr:02d}".format(nr=nr)
    file_name = "{prefix}/HOAF/HOAF_BIDS/{prob}/func/{prob}_task-{exp}_events.tsv".format(
        prob=prob, exp=EXPERIMENT_TYPE[exp], prefix=PREFIX
    )
    if not path.exists(file_name):
        return None
    return file_name


def onset_sorted(nr, exp):
    """Prüfe, ob die `onset` Spalte sortiert ist.
    Hintergrund: Fehler beim Übertragen des Kommas.
    """
    file_name = get_tsv(nr=nr, exp=exp)
    if file_name is None:
        return True
    df = pd.read_csv(file_name, sep="\t")
    return df.onset.is_monotonic and df.onset.max() < 1000


if __name__ == "__main__":
    for exp in range(3):
        for nr in range(1, 30):
            if not onset_sorted(nr, exp):
                print(get_tsv(nr, exp))
