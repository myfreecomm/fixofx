# Copyright 2005-2010 Wesabe, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
sys.path.insert(0, '../3rdparty')
sys.path.insert(0, '../lib')

import ofx
import ofx_test_utils

import os
import unittest

class ParserTests(unittest.TestCase):
    def setUp(self):
        parser = ofx.Parser()
        checking_stmt = ofx_test_utils.get_checking_stmt()
        self.checkparse = parser.parse(checking_stmt)

        creditcard_stmt = ofx_test_utils.get_creditcard_stmt()
        self.creditcardparse = parser.parse(creditcard_stmt)

        blank_memo_stmt = ofx_test_utils.get_blank_memo_stmt()
        self.blank_memoparse = parser.parse(blank_memo_stmt)

    def test_successful_parse(self):
        """Test parsing a valid OFX document containing a 'success' message."""
        self.assertEqual("SUCCESS",
            self.checkparse["body"]["OFX"]["SIGNONMSGSRSV1"]["SONRS"]["STATUS"]["MESSAGE"])

    def test_successfull_parse_for_blank_memo(self):
        """Test parsing a valid OFX document with blank memo containing a 'success' message."""
        self.assertEqual("INFO",
            self.blank_memoparse["body"]["OFX"]["SIGNONMSGSRSV1"]["SONRS"]["STATUS"]["SEVERITY"])

    def test_body_read(self):
        """Test reading a value from deep in the body of the OFX document."""
        self.assertEqual("-5128.16",
            self.creditcardparse["body"]["OFX"]["CREDITCARDMSGSRSV1"]["CCSTMTTRNRS"]["CCSTMTRS"]["LEDGERBAL"]["BALAMT"])

    def test_body_read_for_blank_memo(self):
        """Test reading a value from deep in the body of the OFX document."""
        self.assertEqual("-23.26",
            self.blank_memoparse["body"]["OFX"]["BANKMSGSRSV1"]["STMTTRNRS"]["STMTRS"]["BANKTRANLIST"]["STMTTRN"]["TRNAMT"])

    def test_header_read(self):
        """Test reading a header from the OFX document."""
        self.assertEqual("100", self.checkparse["header"]["OFXHEADER"])

    def test_header_read_for_blank_memo(self):
        """Test reading a header from the OFX document."""
        self.assertEqual("100", self.blank_memoparse["header"]["OFXHEADER"])

    def test_parse_with_empty_tag(self):
        """Test reading a header from the OFX document."""
        parser = ofx.Parser()
        empty_tag_stmt = \
            ofx_test_utils.get_savings_with_self_closed_empty_tag_stmt()
        self.empty_tag = parser.parse(empty_tag_stmt)
        bank_acc_from = self.empty_tag["body"]["OFX"]["BANKMSGSRSV1"]["STMTTRNRS"]["STMTRS"]["BANKACCTFROM"]
        self.assertEqual(bank_acc_from['BANKID'], '1')
        self.assertEqual(bank_acc_from['ACCTID'], '/')
        self.assertEqual(bank_acc_from['ACCTTYPE'], 'SAVINGS')
        self.assertEqual(['ACCTID', 'ACCTTYPE', 'BANKID'], bank_acc_from.keys())

    def test_parse_tag_with_line_break(self):
        """Test reading a header from the OFX document."""
        parser = ofx.Parser()
        stmt =  ofx_test_utils.get_tag_with_line_break_stmt()
        result = parser.parse(stmt)
        subject = result["body"]["OFX"]["BANKMSGSRSV1"]["STMTTRNRS"]["STMTRS"]["BANKTRANLIST"]["STMTTRN"]

        self.assertEqual(False, "OBSV" in subject)


if __name__ == '__main__':
    unittest.main()
