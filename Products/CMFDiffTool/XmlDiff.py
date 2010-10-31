"""
XmlDiff.py - XML difference between objects

Author: Simon Mueller
(C) 2005 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""
from zope.interface import implements

#import difflib
from Globals import InitializeClass
from BaseDiff import BaseDiff, _getValue, MergeError
from interfaces.portal_diff import IDifference


class XmlDiff(BaseDiff):
    """XML difference"""

    implements(IDifference)

    meta_type = "XML Diff"
    
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
        """Return a revised xml document"""
        from Stream import ListStream
        from DiffExecutor import XMLDiffExecutor
        from xml.dom.ext import Print
        from Products.CNXMLDocument import XMLService

        diff = XMLDiffExecutor(self.oldValue, self.newValue)
        diff.execute()
        strm = ListStream()
        Print(diff.getRevisedDocument().getDocumentRoot(), stream=strm)

		# ignore <?xml ..>
        return strm.read()[38:]
        
InitializeClass(XmlDiff)
