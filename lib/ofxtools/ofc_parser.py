#coding: utf-8

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

#
#  ofxtools.ofc_parser - parser class for reading OFC documents.
#
import re
import ofxtools
from pyparsing import alphanums, CharsNotIn, Dict, Forward, Group, \
Literal, OneOrMore, White, Word, ZeroOrMore
from pyparsing import ParseException

class OfcParser:
    """Dirt-simple OFC parser for interpreting OFC documents."""
    def __init__(self, debug=False):
        aggregate = Forward().setResultsName("OFC")
        aggregate_open_tag, aggregate_close_tag = self._tag()
        content_open_tag = self._tag(closed=False)
        content = Group(content_open_tag + CharsNotIn("<\r\n"))
        aggregate << Group(aggregate_open_tag \
            + Dict(OneOrMore(aggregate | content)) \
            + aggregate_close_tag)

        self.parser = Group(aggregate).setResultsName("document")
        if (debug):
            self.parser.setDebugActions(ofxtools._ofxtoolsStartDebugAction,
                                        ofxtools._ofxtoolsSuccessDebugAction,
                                        ofxtools._ofxtoolsExceptionDebugAction)

    def _tag(self, closed=True):
        """Generate parser definitions for OFX tags."""
        openTag = Literal("<").suppress() + Word(alphanums + ".") \
            + Literal(">").suppress()
        if (closed):
            closeTag = Group("</" + Word(alphanums + ".") + ">" + ZeroOrMore(White())).suppress()
            return openTag, closeTag
        else:
            return openTag

    def parse(self, ofc):
        """Parse a string argument and return a tree structure representing
        the parsed document."""
        ofc = self.remove_inline_closing_tags(ofc)
        ofc = self.strip_empty_tags(ofc)
        ofc = self._translate_chknum_to_checknum(ofc)
        try:
          return self.parser.parseString(ofc).asDict()
        except ParseException:
          fixed_ofc = self.fix_ofc(ofc)
          return self.parser.parseString(fixed_ofc).asDict()

    def remove_inline_closing_tags(self, ofc):
        """
        Fix an OFC, by removing inline closing 'tags'
        """
        return re.compile(r'(\w+.*)<\/\w+>', re.UNICODE).sub(r'\1', ofc)

    def fix_ofc(self, ofc):
        """
        Do some magic to fix an bad OFC
        """
        ofc = self._remove_bad_tags(ofc)
        ofc = self._fill_dummy_tags(ofc)
        return self._inject_tags(ofc)

    def _remove_bad_tags(self, ofc):
        ofc_without_trnrs = re.sub(r'<[/]*TRNRS>', '', ofc)
        return re.sub(r'<[/]*CLTID>\w+', '', ofc_without_trnrs)

    def _fill_dummy_tags(self, ofc):
        expression = r'(<%s>)[^\w+]'
        replacement = r'<%s>0\n'
        ofc = re.sub(expression % 'FITID', replacement % 'FITID' , ofc)
        filled_ofc = re.sub(expression % 'CHECKNUM', replacement % 'CHECKNUM' , ofc)

        return filled_ofc

    def _translate_chknum_to_checknum(self, ofc):
        """
        Some banks put an CHKNUM instead of CHECKNUM. this method translates
        CHKNUM to CHECKNUM in order to parse this information correctly
        """
        return re.sub('CHKNUM', 'CHECKNUM', ofc)

    def strip_empty_tags(self, ofc):
        """Strips open/close tags that have no content."""
        strip_search = '<(?P<tag>[^>]+)>\s*</(?P=tag)>'
        return re.sub(strip_search, '', ofc)

    def _inject_tags(self, ofc):
        tags ="<OFC>\n<ACCTSTMT>\n<ACCTFROM>\n<BANKID>0\n<ACCTID>0\n<ACCTTYPE>0\n</ACCTFROM>\n"
        if not re.findall(r'<OFC>\w*\s*<ACCTSTMT>', ofc):
            return ofc.replace('<OFC>', tags).replace('</OFC>', '</ACCTSTMT>\n</OFC>')
