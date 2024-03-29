#
# CMFDiffTool tests
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.CMFDiffTool.FieldDiff import FieldDiff
        
_marker = []

class A:
    attribute = "value"
    def method(self):
        return "method value"

class B:
    attribute = "different value"
    def method(self):
        return "different method value"

class TestFieldDiff(ZopeTestCase.ZopeTestCase):
    """Test the FieldDiff class"""

    def testInterface(self):
        """Ensure that tool instances implement the portal_diff interface"""
        from Products.CMFDiffTool.interfaces.portal_diff import IDifference
        self.failUnless(IDifference.isImplementedByInstancesOf(FieldDiff))
    
    def testAttributeSame(self):
        """Test attribute with same value"""
        a = A()
        fd = FieldDiff(a, a, 'attribute')
        self.failUnless(fd.same)

    def testMethodSame(self):
        """Test method with same value"""
        a = A()
        fd = FieldDiff(a, a, 'method')
        self.failUnless(fd.same)

    def testAttributeDiff(self):
        """Test attribute with different value"""
        a = A()
        b = B()
        fd = FieldDiff(a, b, 'attribute')
        self.failIf(fd.same)

    def testMethodDiff(self):
        """Test method with different value"""
        a = A()
        b = B()
        fd = FieldDiff(a, b, 'method')
        self.failIf(fd.same)

    def testGetLineDiffsSame(self):
        """test getLineDiffs() method with same value"""
        a = A()
        fd = FieldDiff(a, a, 'attribute')
        expected = [('equal', 0, 1, 0, 1)]
        self.assertEqual(fd.getLineDiffs(), expected)

    def testGetLineDiffsDifferent(self):
        """test getLineDiffs() method with different value"""
        a = A()
        b = B()
        fd = FieldDiff(a, b, 'attribute')
        expected = [('replace', 0, 1, 0, 1)]
        self.assertEqual(fd.getLineDiffs(), expected)
        
    def testSameText(self):
        """Test text diff output with same value"""
        a = A()
        fd = FieldDiff(a, a, 'attribute')
        self.assertEqual(fd.ndiff(), '  value')

    def testDiffText(self):
        """Test text diff output with different value"""
        a = A()
        b = B()
        expected = "- value\n+ different value"
        fd = FieldDiff(a, b, 'attribute')
        self.assertEqual(fd.ndiff(), expected)


if __name__ == '__main__':
    framework()
else:
    import unittest
    def test_suite():
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestFieldDiff))        
        return suite

