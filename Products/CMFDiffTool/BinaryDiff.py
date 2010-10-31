"""
BinaryDiff.py - Calculate differences between content objects

Author: Brent Hendricks
(C) 2005 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""
from zope.interface import implements

from Globals import InitializeClass
from BaseDiff import BaseDiff, _getValue, MergeError
from interfaces.portal_diff import IDifference


class BinaryDiff(BaseDiff):
    """Simple binary difference"""

    implements(IDifference)

    meta_type = "Binary Diff"

    def testChanges(self, ob):
        """Test the specified object to determine if the change set will apply without errors"""
        value = _getValue(ob, self.field)
        if not self.same and value != self.oldValue:
            raise MergeError("Conflict Error during merge", self.field, value, self.oldValue)
        
    def applyChanges(self, ob):
        """Update the specified object with the difference"""
        # Simplistic update
        self.testChanges(ob)
        if not self.same:
            setattr(ob, self.field, self.newValue)
            
    def htmlDiff(self):
        """Returns a diff representation in html format"""
        return self.newValue
        
InitializeClass(BinaryDiff)

