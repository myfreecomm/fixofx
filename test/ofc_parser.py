#coding: utf-8
import sys
sys.path.insert(0, '../3rdparty')
sys.path.insert(0, '../lib')

from ofxtools.ofc_parser import OfcParser
from os.path import join, realpath, dirname
from pyparsing import ParseException

import unittest

FIXTURES_PATH = join(realpath(dirname(__file__)), 'fixtures')

def assert_not_raises(function, param, exception):
    try:
      function(param)
    except exception:
      raise AssertionError, "Exception %s raised" %exception

read_file = lambda f: open(join(FIXTURES_PATH, f), 'rU').read()

class OFCParserTestCase(unittest.TestCase):

    def setUp(self):
        self.ofc = read_file('bad.ofc')
        self.parser = OfcParser()

    def test_parsing_bad_ofc_should_not_raise_exception(self):
        assert_not_raises(self.parser.parse, self.ofc, ParseException)

    def test_parsing_ofc_without_bank_info_not_raise_Exception(self):
        self.ofc = read_file('nobankinfo_and_trnrs.ofc')
        assert_not_raises(self.parser.parse, self.ofc, Exception)

    def test_chknum_to_checknum_translation(self):
        self.ofc = read_file('ofc_with_chknum.ofc')
        #ensure that the CHECKNUM was translated
        self.assertTrue('CHECKNUM' in str(self.parser._translate_chknum_to_checknum(self.ofc)))
        self.assertFalse('CHKNUM' in str(self.parser._translate_chknum_to_checknum(self.ofc)))

    def test_not_crashes_when_an_OFC_has_empty_tags(self):
        ofc = read_file('empty_tags.ofx')#it is an ofc by inside
        assert_not_raises(self.parser.parse, ofc, ParseException)

    def test_not_exceed_max_recursion_limit(self):
        """
          For some reason, this file exceeds the normal recursion_limit
          i've solved this setting the max recursion depth.
        """
        ofc = read_file('recursion_depth_exceeded.ofx')
        assert_not_raises(self.parser.parse, ofc, RuntimeError)


if __name__ == '__main__':
    unittest.main()
