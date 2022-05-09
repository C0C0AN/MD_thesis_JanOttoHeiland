"""Fix Onset Bug."""
from os import path
import pandas as pd
from data import PREFIX


EXPERIMENT_TYPE = ["stress_run-1", "stress_run-2", "rest"]


def get_tsv(nr=3, exp=0):
    """Dateinamen fuer ein Probanden mit `nr` und Experimenttyp `exp`
    oder `None`, falls Datei nicht vorhanden.
    """
    prob = "sub-{nr:02d}".format(nr=nr)
    file_name = (
        "{prefix}/HOAF/HOAF_BIDS/{prob}/func/{prob}_task-{exp}_events.tsv".format(
            prob=prob, exp=EXPERIMENT_TYPE[exp], prefix=PREFIX
        )
    )
    if not path.exists(file_name):
        print(f"warning: could not find {file_name=}")
        return None
    return file_name


def out_tsv(nr=3, exp=0):
    """Dateiname, unter dem die bereinigte TSV Datei abgelegt wird."""
    dir = "{prefix}/HOAF/tsv".format(prefix=PREFIX)
    if not path.exists(dir):
        from os import makedirs
        makedirs(dir, mode=771)
    prob = "sub-{nr:02d}".format(nr=nr)
    file_name = "{dir}/{prob}_{exp}_events.tsv".format(
        dir=dir, prob=prob, exp=EXPERIMENT_TYPE[exp]
    )
    return file_name


def onset_sorted(nr, exp):
    """Pruefe, ob die `onset` Spalte sortiert ist.

    Hintergrund: Fehler beim Uebertragen des Kommas.
    """
    file_name = get_tsv(nr=nr, exp=exp)
    if file_name is None:
        return True
    df = pd.read_csv(file_name, sep="\t")
    return df.onset.is_monotonic and df.onset.max() < 1000


def fix_onset(nr=3, exp=0):
    """Gehe die "onset" Spalte durch und füge ein Komma ein, falls nicht vorhanden.

    Das Komma wird so eingefügt, dass die Werte aufsteigend sind.
    """
    file_name = get_tsv(nr, exp)
    if file_name is None:
        return
    df = pd.read_csv(file_name, sep="\t", dtype=str)
    if len(df) <= 0:
        return
    last = len(df) - 1
    assert "." in df.onset[last]
    b = float(df.onset[last])
    for i in range(len(df))[::-1]:
        a = df.onset[i]
        a = float(a)
        while a > b:
            a = a / 10
        df.onset[i] = "{:08.4f}".format(a)
        b = a
    out_fname = out_tsv(nr, exp)
    print(f"writing {out_fname}")
    df.to_csv(out_fname, sep="\t", index=False)


if __name__ == "__main__":
    for exp in range(3):
        for nr in range(1, 30):
            try:
                fix_onset(nr, exp)
            except:
                print("Error on file '{}'".format(get_tsv(nr, exp)))
                raise
