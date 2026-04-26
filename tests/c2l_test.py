import unittest
from tools.c2l import *


class TestC2L(unittest.TestCase):
    def test_srb_latin(self):
        # cyrillic to serbian latin
        c2l = C2L("lat")
        cyrillic_text = "абвгдђежзијклљмнњопрстћуфхцчџшАБВГДЂЕЖЗИЈКЛЉМНЊОПРСТЋУФХЦЧЏШ"
        srb_latin_text = c2l.conv(cyrillic_text)
        self.assertEqual("abvgdđežzijklljmnnjoprstćufhcčdžšABVGDĐEŽZIJKLLjMNNjOPRSTĆUFHCČDžŠ", srb_latin_text)

        # cyrillic to english latin
        c2l = C2L("eng")
        cyrillic_text = "абвгдђежзијклљмнњопрстћуфхцчџшАБВГДЂЕЖЗИЈКЛЉМНЊОПРСТЋУФХЦЧЏШ"
        eng_latin_text = c2l.conv(cyrillic_text)
        self.assertEqual("abvgddjezzijklljmnnjoprstcufhccdzsABVGDDjEZZIJKLLjMNNjOPRSTCUFHCCDzS", eng_latin_text)

        # cyrillic to english latin 2
        c2l = C2L("eng2")
        cyrillic_text = "абвгдђежзијклљмнњопрстћуфхцчџшАБВГДЂЕЖЗИЈКЛЉМНЊОПРСТЋУФХЦЧЏШ"
        eng2_latin_text = c2l.conv(cyrillic_text)
        self.assertEqual("abvgddjezhzijklljmnnjoprstchufhcchdzshABVGDDjEZhZIJKLLjMNNjOPRSTChUFHCChDzSh", eng2_latin_text)


if __name__ == '__main__':
    unittest.main()
