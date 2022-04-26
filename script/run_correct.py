"""Perform a baseline correction"""
from collect import baseline_correction
import pandas as pd

if __name__ == "__main__":
    import argparse
    
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("fname", help="Input TSV file")
    p.add_argument("-c", "--col", help="Column to baseline correct")
    p.add_argument("out", help="Output file name")
    args = p.parse_args()
    
    df = pd.read_csv(args.fname, sep="\t")
    df = baseline_correction(df, args.col)
    df.to_csv(args.out, sep="\t", float_format="%0.2f", index=False)
