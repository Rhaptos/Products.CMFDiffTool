"""
ListDiff.py - List differences between objects

Author: Brent Hendricks
(C) 2005 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""
from zope.interface import implements

from Globals import InitializeClass
from FieldDiff import FieldDiff
from interfaces.portal_diff import IDifference


class ListDiff(FieldDiff):
    """Text difference"""

    implements(IDifference)

    meta_type = "List Diff"

    def _parseField(self, value):
        """Parse a field value in preparation for diffing"""
        # Return the list as is for diffing
        return value
        
    def getAllItems(self):
        rv = {}
        
        # deleted items
        for i in self.oldValue:
            if i not in self.newValue:
                rv[i] = 'd'
            else:
                rv[i] = 'u'
        
        # inserted items
        for i in self.newValue:
            if i not in self.oldValue:
                rv[i] = 'i'
            else:
                rv[i] = 'u'
                
        return rv
        
InitializeClass(ListDiff)
