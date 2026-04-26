import argparse
import sys
import os


def parse_args():
    parser = argparse.ArgumentParser("Converts Serbian Cyrillic text to Latin text.", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "-a", "--alphabet", required=True, choices=["lat", "eng", "eng2"], help="Which Latin alphabet should be used for encoding.\n"
        "Possible values: \n"
        "  'lat'  : Serbian Latin alphabet (contains letters: đžćčš)\n"
        "  'eng'  : English Latin alphabet - no diacritics (џ:dj, ж:z, ћ:c, ч:c, ш:s, џ:dz)\n"
        "  'eng2' : English Latin alphabet - use h instead of diacritic (џ:dj, ж:zh, ћ:ch, ч:ch, ш:sh џ:dz)")
    parser.add_argument("-i", "--in-dir", required=False, help="Directory with input cyrillic files.")
    parser.add_argument("-o", "--out-dir", required=False, help="Output directory with output latin files.")
    return parser.parse_args()



#
# Cyrillic to Latin conversion tables
#
srb_cyrillic_list = [
    "а", "б", "в", "г", "д", "ђ", "е", "ж", "з", "и", "ј", "к", "л", "љ", "м",
    "н", "њ", "о", "п", "р", "с", "т", "ћ", "у", "ф", "х", "ц", "ч", "џ", "ш",
    "А", "Б", "В", "Г", "Д", "Ђ", "Е", "Ж", "З", "И", "Ј", "К", "Л", "Љ", "М",
    "Н", "Њ", "О", "П", "Р", "С", "Т", "Ћ", "У", "Ф", "Х", "Ц", "Ч", "Џ", "Ш"]
srb_latin_list = [
    "a", "b", "v", "g", "d", "đ", "e", "ž", "z", "i", "j", "k", "l", "lj", "m",
    "n", "nj", "o", "p", "r", "s", "t", "ć", "u", "f", "h", "c", "č", "dž", "š",
    "A", "B", "V", "G", "D", "Đ", "E", "Ž", "Z", "I", "J", "K", "L", "Lj", "M",
    "N", "Nj", "O", "P", "R", "S", "T", "Ć", "U", "F", "H", "C", "Č", "Dž", "Š"]
eng_latin_list = [
    "a", "b", "v", "g", "d", "dj", "e", "z", "z", "i", "j", "k", "l", "lj", "m",
    "n", "nj", "o", "p", "r", "s", "t", "c", "u", "f", "h", "c", "c", "dz", "s",
    "A", "B", "V", "G", "D", "Dj", "E", "Z", "Z", "I", "J", "K", "L", "Lj", "M",
    "N", "Nj", "O", "P", "R", "S", "T", "C", "U", "F", "H", "C", "C", "Dz", "S"]
eng2_latin_list = [
    "a", "b", "v", "g", "d", "dj", "e", "zh", "z", "i", "j", "k", "l", "lj", "m",
    "n", "nj", "o", "p", "r", "s", "t", "ch", "u", "f", "h", "c", "ch", "dz", "sh",
    "A", "B", "V", "G", "D", "Dj", "E", "Zh", "Z", "I", "J", "K", "L", "Lj", "M",
    "N", "Nj", "O", "P", "R", "S", "T", "Ch", "U", "F", "H", "C", "Ch", "Dz", "Sh"]


def create_dict(keys, values):
    return dict(zip(keys, values))


def create_c2l_dict(alphabet):
    if alphabet == "lat":
        return create_dict(srb_cyrillic_list, srb_latin_list)
    elif alphabet == "eng":
        return create_dict(srb_cyrillic_list, eng_latin_list)
    elif alphabet == "eng2":
        return create_dict(srb_cyrillic_list, eng2_latin_list)
    else:
        raise RuntimeError("Unknown latin alphabet: %s" % alphabet)


class C2L:
    """This class converts Serbian Cyrillic text to Latin."""
    def __init__(self, alphabet):
        self.cyr2lat = create_c2l_dict(alphabet)

    def conv_char(self, c_char):
        """Convert single character cyrillic string to latin string"""
        return self.cyr2lat.get(c_char, c_char)

    def conv(self, c_text):
        """Convert cyrillic string to latin string"""
        l_chars = []
        for c_char in c_text:
            l_chars.append(self.conv_char(str(c_char)))
        return "".join(l_chars)


def convert_stream(c2l, in_stream, out_stream):
    """Convert text from input stream with c2l converter"""
    for line in in_stream:
        out_stream.write(c2l.conv(line))


def convert_file(c2l, in_path, out_path):
    """Convert single text file with c2l converter"""
    with open(in_path, 'r', encoding='utf-8') as in_file, open(out_path, 'w', encoding='utf-8') as out_file:
        convert_stream(c2l, in_file, out_file)


def ensure_dir(path):
    if os.path.exists(path):
        return
    os.makedirs(path)


def convert_dir(in_dir, out_dir, c2l):
    ensure_dir(out_dir)
    for filename in os.listdir(in_dir):
        in_path = os.path.join(in_dir, filename)
        out_path = os.path.join(out_dir, filename)
        convert_file(c2l, in_path, out_path)


if __name__ == "__main__":
    args = parse_args()

    # create converter
    c2l = C2L(args.alphabet)

    if args.in_dir:
        # we are asked to convert all files in the directory
        assert args.out_dir, "Output directory must be given when input directory is used."

        if os.path.exists(args.out_dir):
            print("Error: output directory %s already exists." % args.out_dir)
            exit(1)
        
        convert_dir(args.in_dir, args.out_dir, c2l)

    else:
        # we are asked to convert stdin input
        assert args.out_dir is None , "Option --out-dir can't be used without option --in--dir."
        convert_stream(c2l, sys.stdin, sys.stdout)
