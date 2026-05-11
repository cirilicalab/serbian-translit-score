import argparse
import os
import json
import sys

def parse_args():
    parser = argparse.ArgumentParser("Parses HF dataset.")
    parser.add_argument("-o", "--output", required=True, help="Output directory where text files will be stored.")
    parser.add_argument("-j", "--json", required=False, help="HF json file")
    return parser.parse_args()


def text2file(text, path):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(text + '\n')


if __name__ == "__main__":
    args = parse_args()

    # open input stream
    istream = sys.stdin
    if args.json:
        istream = open(args.json, 'r', encoding='utf-8')
    
    # make sure that destination dir exists
    os.makedirs(args.output, exist_ok=True)

    # iterate and save to disk
    for line in istream:
        line = line.strip()
        if not line:
            continue

        record = json.loads(line)

        out_path = os.path.join(args.output, record["id"] + ".txt")
        text2file(record["text"], out_path)

