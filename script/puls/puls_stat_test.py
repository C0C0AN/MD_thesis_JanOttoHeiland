import scipy.stats
import pandas as pd


def stat_test(file_name, run=1):
    df = pd.read_csv(file_name, sep="\t")
    df = df[df.run == run]
    df = df[["trial", "puls"]]
    print("mean\n", df.groupby("trial").mean())
    print("\n\nstd\n", df.groupby("trial").std())
    (_, a), (_, b) = df.groupby("trial")
    test = scipy.stats.ttest_ind(a["puls"], b["puls"])
    print(test)
    return df, test


if __name__ == "__main__":
    stat_test("musik_vs_sound_under_relex.tsv")
    print("*" * 80)
    stat_test("stress_vs_relax.tsv")
