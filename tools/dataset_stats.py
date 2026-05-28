import argparse
import sys
import os


def parse_args():
    parser = argparse.ArgumentParser("Computes dataset statistics.", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-t", "--title", action="store_true", help="Only output title row and exit")
    parser.add_argument("-i", "--in-dir", required=False, help="Directory with input cyrillic files.")
    parser.add_argument("-n", "--name", required=False, default="-", help="Dataset name")
    parser.add_argument("-u", "--unit", required=False, default="", help="Unit: K, M")
    return parser.parse_args()



srb_cyrillic_list = [
    "а", "б", "в", "г", "д", "ђ", "е", "ж", "з", "и", "ј", "к", "л", "љ", "м",
    "н", "њ", "о", "п", "р", "с", "т", "ћ", "у", "ф", "х", "ц", "ч", "џ", "ш",
    "А", "Б", "В", "Г", "Д", "Ђ", "Е", "Ж", "З", "И", "Ј", "К", "Л", "Љ", "М",
    "Н", "Њ", "О", "П", "Р", "С", "Т", "Ћ", "У", "Ф", "Х", "Ц", "Ч", "Џ", "Ш"]
srb_cyrillic_set = set(srb_cyrillic_list)

class Stats:
    def __init__(self):
        self.word_count = 0
        self.cyr_word_count = 0
        self.alpha_count = 0
        self.cyr_count = 0


def count_chars(text):
    alpha_count = 0
    cyr_count = 0

    for ch in text:
        if not ch.isalpha():
            continue
        alpha_count += 1
        if ch in srb_cyrillic_list:
            cyr_count += 1
            
    return alpha_count, cyr_count


def count_words(text):
    word_count = 0
    cyr_word_count = 0
    for word in text.split():
        alpha_count, cyr_count = count_chars(word)
        if alpha_count < 0.6 * len(word):
            continue
        word_count += 1

        if cyr_count > alpha_count / 2:
            cyr_word_count += 1

    return word_count, cyr_word_count

def stream_stats(in_stream, stats: Stats):
    """Convert text from input stream with c2l converter"""
    for line in in_stream:
        line.strip('\n\r')

        # count chars
        alpha_count, cyr_count = count_chars(line)
        stats.alpha_count += alpha_count
        stats.cyr_count += cyr_count

        # count words
        word_count, cyr_word_count = count_words(line)
        stats.word_count += word_count
        stats.cyr_word_count += cyr_word_count


def file_stata(path, stats: Stats):
    """Convert single text file with c2l converter"""
    with open(path, 'r', encoding='utf-8') as in_file:
        stream_stats(in_file, stats)


def dir_stats(in_dir, stats: Stats):
    for filename in os.listdir(in_dir):
        in_path = os.path.join(in_dir, filename)
        file_stata(in_path, stats)


def get_unit_value(unit):
    if unit == "":
        return 1
    if unit == "K":
        return 1000
    if unit == "M":
        return 1000000
    assert False

if __name__ == "__main__":
    args = parse_args()

    if args.title:
        out = ["dataset", "#word", "#chars", "cyr_ratio"]
        print("\t".join(out))
        exit()

    stats = Stats()
    dataset_name = args.name
    if args.in_dir:
        dir_stats(args.in_dir, stats)

    else:
        # we are asked to convert stdin input
        stream_stats(sys.stdin, stats)


    cyr_word_ratio = 100.0 * stats.cyr_word_count / stats.word_count
    cyr_alpha_ratio = 100.0 * stats.cyr_count / stats.alpha_count
    unit = get_unit_value(args.unit)
    word_count = stats.word_count / unit
    alpha_count = stats.alpha_count / unit


    out = [dataset_name, str(word_count), str(alpha_count), str(cyr_alpha_ratio)]
    print("\t".join(out))