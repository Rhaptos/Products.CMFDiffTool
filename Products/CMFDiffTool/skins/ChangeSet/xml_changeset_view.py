## Script (Python) "onEditChangeSet"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Compute object differences
##
from Products.CNXMLDocument.XMLService import XMLError
from Products.CNXMLDocument import XMLService

diffs = context.getDiffs()
if not diffs:
    return "no changes"

return XMLService.transform(diffs[0].htmlDiff(), "/home/simon/xml/cnxml/style/unibrowser.xsl")
