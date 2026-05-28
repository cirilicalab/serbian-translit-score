import argparse
import os
import re
import shutil
import json
import sys

def parse_args():
    parser = argparse.ArgumentParser("Creates text files with most common transliteration errors. Used to summarize data for error analysis.")
    parser.add_argument("-wa", "--word-alignment", required=True, help="Word alignment TSV.")
    parser.add_argument("-od", "--out-dir", required=True, help="Output directory.")
    parser.add_argument("-c", "--count", type=int, default=100, help="How many errors to render to html files.")
    parser.add_argument("-ed", "--exp-dir", required=True, help="Directory with expected output files.")
    parser.add_argument("-ad", "--act-dir", required=True, help="Directory with actual output files.")
    return parser.parse_args()


class ErrorOccurrence:
    def __init__(self, filename, op, exp_idx, act_idx):
        self.filename = filename
        self.type = op
        self.exp_idx = int(exp_idx)
        self.act_idx = int(act_idx)


def simple_sanitize(filename):
    # Keep only letters, numbers, spaces, underscores, hyphens, and dots
    safe = re.sub(r'[^\w\s.-]', '_', filename)
    # Replace spaces with underscores
    safe = re.sub(r'\s+', '_', safe)
    return safe.strip('._')


def read_word_alignment(path):
    err2occurrences = {}
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.lower().startswith("file"):
                continue
            line = line.rstrip('\n')
            filename, op, exp_idx, act_idx, exp_word, act_word = line.split('\t')

            # ensure that error is tracked
            err = (exp_word, act_word)
            if not err in err2occurrences:
                err2occurrences[err] = []
            
            # add occurrence
            occurrence = ErrorOccurrence(filename, op, exp_idx, act_idx)
            err2occurrences[err].append(occurrence)
    return err2occurrences


def get_window(words, center_idx, window_size):
    start = max(0, center_idx - window_size)
    end = min(len(words) - 1, center_idx + window_size)
    return (start, end)
    

def file2words(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read().split()


def window2str(words, start, end, center_idx):
    out_words = []
    for i in range(start, end):
        word = words[i]
        if i == center_idx:
            word = "*" + word + "*"
        out_words.append(word)
    return " ".join(out_words)


def render_one_occurrence(occurrence: ErrorOccurrence, exp_dir: str, act_dir: str, out_file):
    window_size=8

    # get expected words window
    exp_path = os.path.join(exp_dir, occurrence.filename)
    exp_words = file2words(exp_path)
    exp_start, exp_end = get_window(exp_words, occurrence.exp_idx, window_size)

    # get actual words window
    act_path = os.path.join(act_dir, occurrence.filename)
    act_words = file2words(act_path)
    act_start, act_end = get_window(act_words, occurrence.act_idx, window_size)

    exp_str = window2str(exp_words, exp_start, exp_end, occurrence.exp_idx)
    act_str = window2str(act_words, act_start, act_end, occurrence.act_idx)

    out_file.write(exp_str + "\n")
    out_file.write(act_str + "\n")
    out_file.write("\n")


def render_one(err: tuple[str, str, str], occurrences: list[ErrorOccurrence], exp_dir: str, act_dir: str, out_dir):
    exp_word, act_word = err
    
    filename = "%06d_%s_%s.txt" % (len(occurrences), exp_word, act_word)
    filename = simple_sanitize(filename)
    out_path = os.path.join(out_dir, filename)
    assert not os.path.exists(out_path), "File already exists: %s" % out_path

    with open(out_path, 'w', encoding='utf-8') as out_file:
        out_file.write("%s\t%s\t%d\n\n" % (exp_word, act_word, len(occurrences)))
        for occurrence in occurrences[0:min(10, len(occurrences))]:
            render_one_occurrence(occurrence, exp_dir, act_dir, out_file)


if __name__ == "__main__":
    args = parse_args()

    # read word alignments, count occurrences
    err2occurrences = read_word_alignment(args.word_alignment)
    err_occurrences = sorted(err2occurrences.items(), key=lambda item: len(item[1]), reverse=True) 

    # ensure output directory exists
    if os.path.isdir(args.out_dir):
        shutil.rmtree(args.out_dir)
    os.mkdir(args.out_dir)

    for err, occurrences in err_occurrences[0:args.count]:
        render_one(err, occurrences, args.exp_dir, args.act_dir, args.out_dir)
