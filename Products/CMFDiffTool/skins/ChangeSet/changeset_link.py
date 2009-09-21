##parameters=id
obj = context[id]
typeInfo = obj.getTypeInfo();
act = typeInfo.getActionById('view')
url = ''.join((obj.absolute_url(), '/', act))
return url
