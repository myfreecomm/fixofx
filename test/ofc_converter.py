#coding: utf-8
import sys
sys.path.insert(0, '../3rdparty')
sys.path.insert(0, '../lib')

from ofxtools.ofc_converter import OfcConverter
from os.path import join, realpath, dirname

import unittest


no_bankinfo_ofc_path = join(realpath(dirname(__file__)), 'fixtures', 'nobankinfo_and_trnrs.ofc')

def assert_not_raises(function, param, exception):
    try:
      function(param)
    except exception:
      raise AssertionError, "Exception %s raised" %exception


class OFCConverterWithNoBankInfoTestCase(unittest.TestCase):
    """
    Testing an special case that doesn't has the bank info 'tags'
    and instead of having ACCTSTMT, it has TRNRS which has the same
    information needed
    """

    def setUp(self):
        self.ofc = open(no_bankinfo_ofc_path, 'r').read()

    def test_converting_ofc_with_no_bankinfo_should_not_raise_KeyError(self):
        assert_not_raises(OfcConverter, self.ofc, KeyError)

    def test_ofc_converter_getting_balance_value(self):
        ofc_converter = OfcConverter(self.ofc)
        self.assertEqual(ofc_converter.balance, '350.66')

    def test_ofc_converter_getting_start_date(self):
        ofc_converter = OfcConverter(self.ofc)
        self.assertEqual(ofc_converter.start_date, '20101214')

    def test_ofc_converter_getting_end_date(self):
        ofc_converter = OfcConverter(self.ofc)
        self.assertEqual(ofc_converter.end_date, '20110113')

if __name__ == '__main__':
    unittest.main()
