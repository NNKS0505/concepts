# test_formats.py

import os
import unittest

import pytest

from concepts.formats import Format, Cxt, Table, Csv, WikiTable

DIRECTORY = 'test-output'


@pytest.mark.parametrize('name, expected', [
    ('table', Table),
    ('cxt', Cxt),
    ('csv', Csv),
    ('wikitable', WikiTable),
])
def test_getitem(name, expected):
    assert Format[name] is expected is Format[name.upper()]


def test_getitem_invalid():
    with pytest.raises(KeyError):
        Format['spam']


@pytest.mark.parametrize('filename, expected', [
    ('spam.TXT', 'table'),
    ('spam.cxt', 'cxt'),
    ('spam.spam.csv', 'csv')
])
def test_infer_format(filename, expected):
    assert Format.infer_format(filename) == expected


def test_infer_format_invalid():
    with pytest.raises(ValueError, match=r'filename suffix'):
        Format.infer_format('spam.spam')


class LoadsDumps(object):

    def test_loads(self):
        try:
            objects, properties, bools = self.format.loads(self.result)
        except NotImplementedError:
            pass
        else:
            self.assertSequenceEqual(objects, self.objects)
            self.assertSequenceEqual(properties, self.properties)
            self.assertSequenceEqual(bools, self.bools)

    def test_dumps(self):
        result = self.format.dumps(self.objects, self.properties, self.bools)
        self.assertEqual(result, self.result)

    def test_dump_load(self, outdir=DIRECTORY):
        if not os.path.exists(outdir):
            os.mkdir(outdir)

        extension = getattr(self.format, 'extension', '.txt')
        filepath = os.path.join(outdir, self.__class__.__name__ + extension)
        self.format.dump(filepath,
                         self.objects, self.properties, self.bools,
                         self.encoding)

        try:
            objects, properties, bools = self.format.load(filepath,
                                                          self.encoding)
        except NotImplementedError:
            pass
        else:
            self.assertSequenceEqual(objects, self.objects)
            self.assertSequenceEqual(properties, self.properties)
            self.assertSequenceEqual(bools, self.bools)


class Ascii(LoadsDumps):

    objects = ('Cheddar', 'Limburger')
    properties = ('in_stock', 'sold_out')
    bools = [(False, True), (False, True)]

    encoding = None


class Unicode(LoadsDumps):

    objects = ('M\xf8\xf8se', 'Llama')
    properties = ('majestic', 'bites')
    bools = [(True, True), (False, False)]

    encoding = 'utf-8'


class TestCxtAscii(unittest.TestCase, Ascii):

    format = Cxt
    result = 'B\n\n2\n2\n\nCheddar\nLimburger\nin_stock\nsold_out\n.X\n.X\n'


class TextCxtUnicode(unittest.TestCase, Unicode):

    format = Cxt
    result = 'B\n\n2\n2\n\nM\xf8\xf8se\nLlama\nmajestic\nbites\nXX\n..\n'


class TestTableAscii(unittest.TestCase, Ascii):

    format = Table
    result = ('         |in_stock|sold_out|\n'
              'Cheddar  |        |X       |\n'
              'Limburger|        |X       |')


class TestTableUnicode(unittest.TestCase, Unicode):

    format = Table
    result = ('     |majestic|bites|\n'
              'M\xf8\xf8se|X       |X    |\n'
              'Llama|        |     |')


class TestCsvAscii(unittest.TestCase, Ascii):

    format = Csv
    result = (',in_stock,sold_out\r\n'
              'Cheddar,,X\r\n'
              'Limburger,,X\r\n')


class TestCsvUnicode(unittest.TestCase, Unicode):

    format = Csv
    result = (',majestic,bites\r\n'
              'M\xf8\xf8se,X,X\r\n'
              'Llama,,\r\n')


class TestWikitableAscii(unittest.TestCase, Ascii):

    format = WikiTable
    result = ('{| class="featuresystem"\n'
              '!\n'
              '!in_stock!!sold_out\n'
              '|-\n'
              '!Cheddar\n'
              '|        ||X       \n'
              '|-\n'
              '!Limburger\n'
              '|        ||X       \n'
              '|}')


class TestWikitableUnicode(unittest.TestCase, Unicode):

    format = WikiTable
    result = ('{| class="featuresystem"\n'
              '!\n'
              '!majestic!!bites\n'
              '|-\n'
              '!M\xf8\xf8se\n|X       ||X    \n'
              '|-\n'
              '!Llama\n'
              '|        ||     \n'
              '|}')
