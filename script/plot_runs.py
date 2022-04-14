"""Plotte die Werte über die Zeit."""
import matplotlib.pyplot as plt
import pandas as pd
from os import path
from collect import baseline_correction, load_phasen


def plot_phases(colors=["0.3", "0.9"], alpha=0.06, ax=plt):
    """Stress und Entspannungsphasen des Experiments."""
    pf = load_phasen()
    phases = 0.5 * (pf.loc[1].values + pf.loc[2].values)
    for i, phase in enumerate(phases):
        ax.axvspan(phase[0], phase[1], facecolor=colors[i % 2], alpha=alpha)


def plot_runs(tf, ylabel="Puls [BPM]", top_xaxis=False, values="puls"):
    probanden = tf["prob_id"].unique()
    times = tf["time"].unique()
    times.sort()
    tf.sort_values(["prob_id", "time"], inplace=True)

    fig, axs = plt.subplots(2)
    if top_xaxis:
        axs[0].xaxis.set_label_position("top")
        axs[0].xaxis.set_ticks_position("top")
    vmin, vmax = tf[values].min(), tf[values].max()
    d = 0.2 * (vmax + vmin)
    vmin, vmax = vmin - d, vmax + d
    for (run, uf), ax in zip(tf.groupby("run"), axs):
        vf = uf.pivot_table(columns="prob_id", values=values, index="time")
        ax.plot(vf, color="black", linewidth=1.5, alpha=0.15)
        ax.plot(vf.mean(axis=1), color="black", linewidth=2)
        ax.set_ylabel(ylabel)
        ax.set_ylim(vmin, vmax)
        ax.set_xlim(tf["time"].min(), tf["time"].max())
        plot_phases(ax=ax, colors=["green", "green"])
    plt.xlabel("time [sec]")


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "data",
        nargs="?",
        default=path.join(path.dirname(__file__), "puls", "puls_long.tsv"),
    )
    p.add_argument("-B", "--no-baseline", action="store_true")
    p.add_argument(
        "-t",
        "--top-xaxis",
        action="store_true",
        help="Plotte die mittlere x-Achse oben",
    )
    p.add_argument(
        "-v", "--values", default="puls", help="Spalte, die die Werte enthält"
    )
    p.add_argument("-y", "--yaxis", default="Puls [BPM]", help="y-Achse Beschriftung")
    p.add_argument(
        "-o", "--out", type=str, default=None, help="Speichere die Abbildung in OUT"
    )
    p.add_argument("-z", "--zscore", action="store_true", help="Plot Z-Score.")
    args = p.parse_args()

    df = pd.read_csv(args.data, sep="\t")
    if "time" not in df.columns:
        assert "time_point" in df.columns
        df["time"] = df["time_point"] * 1.45
    if "prob_nr" in df.columns:
        df.rename(columns={"prob_nr": "prob_id"}, inplace=True)

    if not args.no_baseline:
        df = baseline_correction(df, column=args.values)
    if args.zscore:
        for i in df["prob_id"].unique():
            mask = df["prob_id"] == i
            df.loc[mask, args.values] /= df.loc[mask, args.values].std()

    tf = df[["time", args.values, "prob_id", "run"]].copy()
    plot_runs(tf, top_xaxis=args.top_xaxis, values=args.values, ylabel=args.yaxis)
    if args.out:
        plt.savefig(args.out)
    else:
        plt.show()
