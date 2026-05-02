import argparse
import os
import sys
import Levenshtein

#
# Terminology
#   act : actual transliteration output
#   exp : expected transliteration output
#   t : token count
#   i : insertion count
#   s : substitution count
#   d : deletion count
#   err : Error rate (i + s + d) / total_count
#   wer : word error rate
#   cer : character error rate
#

g_output_level=0

def parse_args():
    parser = argparse.ArgumentParser("Computes score of Serbian Latin to Serbian Cyrillic transliteration.")
    parser.add_argument("mode", choices=["file", "dir", "title"], 
                        help="Selects scoring mode. Use 'file' to score individual files, use 'dir' to score all files within directory")
    parser.add_argument("-a", "--act", required=False, help="Path to actual transliterator output.")
    parser.add_argument("-e", "--exp", required=False, help="Path to expected output.")
    return parser.parse_args()


class EditCounts:
    """
    Tuple that holds total count and insertion, substitution and deletion error counts. 
    Convenient for passing by reference.
    """
    def __init__(self, t=0, i=0, s=0, d=0):
        self.t = t
        self.i = i
        self.s = s
        self.d = d

    def __add__(self, other):
        result = EditCounts()
        result.i = self.i + other.i
        result.s = self.s + other.s
        result.d = self.d + other.d
        result.t = self.t + other.t
        return result

    def __iadd__(self, other):
        self.i += other.i
        self.s += other.s
        self.d += other.d
        self.t += other.t
        return self

    def __eq__(self, other):
        return self.i == other.i and self.s == other.s and self.d == other.d and self.t == other.t
    
    def __repr__(self):
        return "EditCounts t=%d, i=%d, s=%d, d=%d" % (self.t, self.i, self.s, self.d)


def edit_ops_to_counts(seq_len, edit_ops, counts: EditCounts):
    """Interprets output of Levenshtein.editops() and increments EditCounts."""
    counts.t += seq_len
    for op_name, _, _ in edit_ops:
        if op_name == "insert":
            counts.i += 1
        elif op_name == "replace":
            counts.s += 1
        elif op_name == "delete":
            counts.d += 1
        else:
            assert False, "Unknown operation name"


def update_counts(exp, act, counts):
    """
    Computes EditCounts between transliteration output and expected sequence. 
    
    Works for both char edit counts and word edit counts
    """
    edit_ops = Levenshtein.editops(exp, act)
    edit_ops_to_counts(len(exp), edit_ops, counts)


def file2str(path):
    """Reads entire file into string"""
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


def file2words(path):
    """Reads file into list of words."""
    with open(path, 'r', encoding='utf-8') as file:
        return file.read().split()


def file_counts(exp_path, act_path, file2seq_func):
    """
    Computes EditCounts for pair of transliterator output file and expected file
    """
    act = file2seq_func(act_path)
    exp = file2seq_func(exp_path)
    counts = EditCounts()
    update_counts(exp, act, counts)
    return counts


def dir_counts(exp_dir, act_dir, file2seq_func):
    """
    Scans directories and computes EditCounts for each pair of trans/exp files that is found.
    Returns list of (filename, EditCounts) tuples.
    
    file2seq_func:
        - file2str for character EditCounts.
        - file2words for word EditCounts.
    """
    results = []
    for filename in os.listdir(exp_dir):
        exp_path = os.path.join(exp_dir, filename)
        if not os.path.isfile(exp_path):
            continue
        act_path = os.path.join(act_dir, filename)
        
        if not os.path.isfile(act_path):
            sys.stderr("Skipping file because no transcription was found: %s" % filename)
            continue

        counts = file_counts(exp_path, act_path, file2seq_func)
        results.append((filename, counts))

    return results    


def summarize_counts(counts_list):
    """Computes total counts"""
    total_counts = EditCounts()
    for counts in counts_list:
        total_counts += counts
    return total_counts


def safe_div(a, b):
    if b == 0 and a >= 0:
        return float('inf')
    elif b == 0 and a < 0:
        return float('-inf')
    else:
        return a / b;

def compute_error(counts):
    error_count = counts.i + counts.s + counts.d
    return safe_div(error_count, counts.t)


def err_str(err):
    return "%.2f" % (100 * err)


def print_result(word_counts, char_counts, print_col_names=True, print_results=True):
    # compute character error rate
    cer = compute_error(char_counts)

    # compute word error rate
    wer = compute_error(word_counts)

    # output result
    col_names = ["wer", "cer"] 
    col_values = [err_str(wer), err_str(cer)]
    
    col_names.extend(["#words", "wins", "wsub", "wdel"])
    col_values.extend([str(word_counts.t), str(word_counts.i), str(word_counts.s), str(word_counts.d)])

    col_names.extend(["#chars", "cins", "csub", "cdel"])
    col_values.extend([str(char_counts.t), str(char_counts.i), str(char_counts.s), str(char_counts.d)])

    if print_col_names:
        print("\t".join(col_names))
    if print_results:
        print("\t".join(col_values))


def file_mode(exp_path, act_path):
    if g_output_level > 0:
        sys.stderr.write("Compare files")
        sys.stderr.write("    act: %s" % act_path)
        sys.stderr.write("    exp: %s" % exp_path)
        sys.stderr.write("\n")

    # compute counts
    char_counts = file_counts(act_path, exp_path, file2str)
    word_counts = file_counts(act_path, exp_path, file2words)

    # output result
    print_result(word_counts, char_counts)


def dir_mode(exp_dir, act_dir):
    global g_output_level
    if g_output_level > 0:
        sys.stderr.write("Compare files")
        sys.stderr.write("    act: %s" % act_dir)
        sys.stderr.write("    exp: %s" % exp_dir)
        sys.stderr.write("\n")

    # compute counts
    file_and_char_counts_list = dir_counts(exp_dir, act_dir, file2str)
    file_and_word_counts_list = dir_counts(exp_dir, act_dir, file2words)

    # cumulate counts
    total_char_counts = summarize_counts([counts for _, counts in file_and_char_counts_list])
    total_word_counts = summarize_counts([counts for _, counts in file_and_word_counts_list])

    # output result
    print_result(total_word_counts, total_char_counts)



if __name__ == "__main__":
    args = parse_args()

    if args.mode == "file":
        file_mode(args.exp, args.act)
        exit()

    if args.mode == "dir":
        dir_mode(args.exp, args.act)
        exit()

    if args.mode == "title":
        print_result(EditCounts(), EditCounts(), print_col_names=True, print_results=False)
        exit()

    assert False, "Unknown mode: %s" % (args.mode)
