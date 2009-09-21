"""
FieldDiff.py - Text difference between objects

Author: Brent Hendricks
(C) 2005 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

import difflib
from Globals import InitializeClass
from BaseDiff import BaseDiff, _getValue, MergeError
from interfaces.portal_diff import IDifference

# definition of constants
STATE_NEUTRAL = "  "
STATE_INSERT  = "+ "
STATE_DELETE  = "- "

TAG_INSERT_OPEN  = "<ins>"
TAG_INSERT_CLOSE = "</ins>"
TAG_DELETE_OPEN  = "<del>"
TAG_DELETE_CLOSE = "</del>"


class FieldDiff(BaseDiff):
    """Text difference"""

    __implements__ = (IDifference)

    meta_type = "Field Diff"

    def _parseField(self, value):
        """Parse a field value in preparation for diffing"""
        # Since we only want to compare a single field, make a
        # one-item list out of it
        return [value]

    def getLineDiffs(self):
        a = self._parseField(self.oldValue)
        b = self._parseField(self.newValue)        
        return difflib.SequenceMatcher(None, a, b).get_opcodes()

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
        # compares two strings and returns a list of elements. The elements
        # have a length of three (two-letter code + character)
        e = difflib.Differ()
        result = list(e.compare(self.oldValue, self.newValue))
    
        # state machine
        state = STATE_NEUTRAL
        for count in range(len(result)):
            # returns two-letter code 
            mark = result[count][0:2]

            # runs through states and does the appropriate action
            tag = ""
            if (state == STATE_NEUTRAL):
                if (mark == STATE_NEUTRAL):
                    pass
                elif (mark == STATE_INSERT):
                    tag += TAG_INSERT_OPEN
                elif (mark == STATE_DELETE):
                    tag += TAG_DELETE_OPEN
            elif (state == STATE_INSERT):
                if (mark == STATE_NEUTRAL):
                    tag += TAG_INSERT_CLOSE
                elif (mark == STATE_INSERT):
                    pass
                elif (mark == STATE_DELETE):
                    tag += TAG_INSERT_CLOSE + TAG_DELETE_OPEN
            elif (state == STATE_DELETE):
                if (mark == STATE_NEUTRAL):
                    tag += TAG_DELETE_CLOSE
                elif (mark == STATE_INSERT):
                    tag += TAG_DELETE_CLOSE + TAG_INSERT_OPEN
                elif (mark == STATE_DELETE):
                    pass
            
            # changes are written back to result list
            result[count] = tag + result[count][2]
            
            # sets closing tag if it is last iteration
            if (count >= len(result)-1):
                if (mark == STATE_NEUTRAL):
                    pass
                elif (mark == STATE_INSERT):
                    result[count] = result[count] + TAG_INSERT_CLOSE
                elif (mark == STATE_DELETE):
                    result[count] = result[count] + TAG_DELETE_CLOSE
            
            # reinitialization for next iteration
            state = mark
        
        return "".join(result)
        
        #return self.same and self.oldValue or "<del>" + self.oldValue + "</del><ins>" + self.newValue + "</ins>"            

    def ndiff(self):
        """Return a textual diff"""
        r=[]
        a = self._parseField(self.oldValue)
        b = self._parseField(self.newValue)        
        for tag, alo, ahi, blo, bhi in self.getLineDiffs():
            if tag == 'replace':
                plain_replace(a, alo, ahi, b, blo, bhi, r)
            elif tag == 'delete':
                dump('-', a, alo, ahi, r)
            elif tag == 'insert':
                dump('+', b, blo, bhi, r)
            elif tag == 'equal':
                dump(' ', a, alo, ahi, r)
            else:
                raise ValueError, 'unknown tag ' + `tag`
        return '\n'.join(r)
        
InitializeClass(FieldDiff)

def dump(tag, x, lo, hi, r):
    for i in xrange(lo, hi):
        r.append(tag +' ' + str(x[i]))

def plain_replace(a, alo, ahi, b, blo, bhi, r):
    assert alo < ahi and blo < bhi
    # dump the shorter block first -- reduces the burden on short-term
    # memory if the blocks are of very different sizes
    if bhi - blo < ahi - alo:
        dump('+', b, blo, bhi, r)
        dump('-', a, alo, ahi, r)
    else:
        dump('-', a, alo, ahi, r)
        dump('+', b, blo, bhi, r)
