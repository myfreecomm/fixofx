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

import os

fixtures = os.path.join(os.path.dirname(__file__) or '.', "fixtures")

def get_checking_stmt():
    return _read_file("checking.ofx")

def get_savings_stmt():
    return _read_file("savings.ofx")

def get_savings_with_self_closed_empty_tag_stmt():
    return _read_file("savings_with_self_closed_empty_tag.ofx")

def get_creditcard_stmt():
    return _read_file("creditcard.ofx")

def get_blank_memo_stmt():
    return _read_file("blank_memo.ofx")

def get_tag_with_line_break_stmt():
    return _read_file("tag_with_line_break.ofx")

def _read_file(filename):
    return open(os.path.join(fixtures, filename), 'rU').read()


