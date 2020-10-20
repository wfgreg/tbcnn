class JsonTree:
    tree = None
    def __init__(self,root=None):
        tree = root
    @classmethod
    def f(self):
        return

    @staticmethod
    def iter_child_nodes(data):
        # if data has nodes
        if isinstance(data, list):
            for field in data:
                if isinstance(field, dict):
                    yield field
                elif isinstance(field, list):
                    for subitem in field:
                        if isinstance(subitem, dict):
                            yield subitem
        elif isinstance(data, dict):
            if "attributes" in data.keys():
                for key in data['attributes'].keys():
                    data[key] = data['attributes'][key]

            for fieldkey in data.keys():
                if fieldkey == "attributes":
                    continue
                field=data[fieldkey]
                if isinstance(field, dict):
                    yield field
                elif isinstance(field, list):
                    for subitem in field:
                        if isinstance(subitem, dict):
                            yield subitem

#  root node is an unnamed 'stmts' type with no attributes/name/etc - its contents are an array

# treat any objects with a 'stmts' list as a new node
#def iter_fields(node):
#    """
#    Yield a tuple of ``(fieldname, value)`` for each field in ``node._fields``
#    that is present on *node*.
#    """
#    for field in node._fields:
#        try:
#            yield field, getattr(node, field)
#        except AttributeError:
#            pass
#
#
#def iter_child_nodes(node):
#    """
#    Yield all direct child nodes of *node*, that is, all fields that are nodes
#    and all items of fields that are lists of nodes.
#    """
#    for name, field in iter_fields(node):
#        if isinstance(field, AST):
#            yield field
#        elif isinstance(field, list):
#            for item in field:
#                if isinstance(item, AST):
#                    yield item
