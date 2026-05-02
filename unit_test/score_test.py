import unittest
import os
from tools.score import *

# helper method for tests
def compute_counts(act, exp):
    counts = EditCounts()
    update_counts(act, exp, counts)
    return counts

class TestEditCounts(unittest.TestCase):
    def test_edit_counts(self):
        counts = EditCounts()
        self.assertEqual(EditCounts(t=0, i=0, s=0, d=0), counts)

        counts2 = EditCounts(t=10, i=1, s=2, d=3)
        
        counts += counts2
        self.assertEqual(EditCounts(t=10, i=1, s=2, d=3), counts)

        counts += counts2
        self.assertEqual(EditCounts(t=20, i=2, s=4, d=6), counts)

        counts3 = counts + counts2
        self.assertEqual(EditCounts(t=30, i=3, s=6, d=9), counts3)


    def test_err(self):
        counts = EditCounts(t=1, i=0, s=0, d=0)
        err = compute_error(counts)
        self.assertEqual(0, err)

        counts = EditCounts(t=10, i=1, s=2, d=3)
        err = compute_error(counts)
        self.assertEqual(0.6, err)


    def test_compute_counts(self):
        self.assertEqual(EditCounts(t=4, i=1, s=0, d=0), compute_counts("abcd", "abbcd"))
        self.assertEqual(EditCounts(t=4, i=0, s=0, d=1), compute_counts("abcd", "acd"))
        self.assertEqual(EditCounts(t=4, i=0, s=1, d=0), compute_counts("abcd", "accd"))
        self.assertEqual(EditCounts(t=4, i=0, s=0, d=0), compute_counts("abcd", "abcd"))

        self.assertEqual(EditCounts(t=4, i=1, s=0, d=0), compute_counts(["a", "b", "c", "d"], ["a", "b", "b", "c", "d"]))
        self.assertEqual(EditCounts(t=4, i=0, s=0, d=1), compute_counts(["a", "b", "c", "d"], ["a", "c", "d"]))
        self.assertEqual(EditCounts(t=4, i=0, s=1, d=0), compute_counts(["a", "b", "c", "d"], ["a", "c", "c", "d"]))
        self.assertEqual(EditCounts(t=4, i=0, s=0, d=0), compute_counts(["a", "b", "c", "d"], ["a", "b", "c", "d"]))


def norm_path(path):
    root_dir=os.path.dirname(__file__)
    return os.path.join(root_dir, path)


class TestScore(unittest.TestCase):
    def test_read_file(self):
        seq = file2str(norm_path("data/test_read.txt"))
        self.assertEqual(seq, "aaa bbb\nccc\nd\te\nf  g\n\n")

        seq = file2words(norm_path("data/test_read.txt"))
        self.assertEqual(seq, ["aaa", "bbb", "ccc", "d", "e", "f", "g"])

    def test_file_counts(self):
        counts = file_counts(norm_path("data/exp/test.txt"), norm_path("data/act/test.txt"), file2str)
        self.assertEqual(EditCounts(t=8, i=1, s=0, d=1), counts)

        counts = file_counts(norm_path("data/exp/test.txt"), norm_path("data/act/test.txt"), file2words)
        self.assertEqual(EditCounts(t=2, i=0, s=2, d=0), counts)
    
    def test_dir_counts(self):
        results = dir_counts(norm_path("data/exp"), norm_path("data/act"), file2str)
        self.assertEqual([("test.txt", EditCounts(t=8, i=1, s=0, d=1))], results)

        results = dir_counts(norm_path("data/exp"), norm_path("data/act"), file2words)
        self.assertEqual([("test.txt", EditCounts(t=2, i=0, s=2, d=0))], results)


if __name__ == '__main__':
    unittest.main()

