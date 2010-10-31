"""
TextDiff.py - Text difference between objects

Author: Brent Hendricks
(C) 2005 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""
from zope.interface import implements

from Globals import InitializeClass
from FieldDiff import FieldDiff
from interfaces.portal_diff import IDifference


class TextDiff(FieldDiff):
    """Text difference"""

    implements(IDifference)

    meta_type = "Lines Diff"

    def _parseField(self, value):
        """Parse a field value in preparation for diffing"""
        # Split the text into a list for diffs
        return value.split('\n')

InitializeClass(TextDiff)
