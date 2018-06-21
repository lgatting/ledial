import resample
import argparse
import heapq

parser = argparse.ArgumentParser()
parser.add_argument("-src", help="Source file")
parser.add_argument("-dst", help="Destination file")
args = parser.parse_args()

print "Resampling", args.src, "to", args.dst

resample.resample(args.src, args.dst, resampling_fn=lambda x: min(x), cutoff_less=True)