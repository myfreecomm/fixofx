#coding: utf-8
import re

def strip_empty_tags(ofx):
    """Strips open/close tags that have no content."""
    strip_search = '<(?P<tag>[^>]+)>\s*</(?P=tag)>'
    return re.sub(strip_search, '', ofx)

