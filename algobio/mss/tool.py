#!/bin/python
import argparse
import mss
import urllib.request
import io

## Transformiert ein FASTA-File (oder anderen Input in Form eines Streams)
## zu einer Liste von Zahlen, auf die dann die Algorithmen
## angewendet werden können
def transform_fasta(fasta: io.TextIOBase, schema):
    transformed = []
    fasta.readline() # skip header
    for line in fasta:
        for c in line.strip():
            transformed.append(schema[c])

    return transformed

parser = argparse.ArgumentParser(description="Finds hydrophobic regions in a protein primary sequence downloaded from SWISSPROT/UniProt.")

parser.add_argument("-m", dest="model", help="Hydrophobicity index to use. Defaults to ARGP820101, available via the AAindex", type=argparse.FileType('r'), default=None)

inputmode = parser.add_mutually_exclusive_group(required=True)
inputmode.add_argument("-i", dest="in_file", help="File to use as FASTA input.", type=argparse.FileType('r'))
inputmode.add_argument("-s", dest="in_id", help="UniProt ID to use when downloading from the web", type=str)

args = parser.parse_args()

# available at https://www.genome.jp/entry/aaindex:ARGP820101
schema = {'A': 0.61, 'R':0.60, 'N':0.06, 'D':0.46, 'C':1.07,
        'Q':0, 'E':0.47, 'G':0.07, 'H':0.61, 'I':2.22,
        'V':1.32, 'Y':1.88, 'W':2.65, 'T':0.05, 'S':0.05,
        'P':1.95, 'F':2.02, 'M':1.18, 'K':1.15, 'L':1.53
        }

kv_list = []
if args.model:
    for l in args.model:
        for pair in l.split(","):
            if pair.strip() == "":
                continue
            contents = pair.split(":")
            kv_list.append( (contents[0].strip(), float(contents[1].strip())) )

schema.update(kv_list)

fasta = ""
if args.in_id:
    url = f"https://www.uniprot.org/uniprot/{args.in_id}.fasta"
    fasta = io.StringIO(urllib.request.urlopen(url).read().decode('UTF8'))

# choose file over ID
if args.in_file:
    fasta = args.in_file

transformed = transform_fasta(fasta, schema)
# uses the linear algorithm, because it has a small memory footprint
# and avoids recursive calls
# in practice, the square term in its complexity should be relatively small
for lmss in mss.linear(transformed, agg=True, feature="long"): # equivalent to aL
    print("\t".join(map(
        lambda x: str(x),
        lmss)))
