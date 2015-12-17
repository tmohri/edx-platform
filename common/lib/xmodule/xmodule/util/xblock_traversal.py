"""
Utility functions related to traversal of XBlock relationships
"""


def get_xblock_parent(xblock, category=None):
    """
    Returns the parent of the given XBlock. If an optional category is supplied,
    traverses the ancestors of the XBlock and returns the first with the
    given category.

    Arguments:
        xblock (XBlock): Get the parent of this XBlock
        category (str): Find an ancestor with this category (e.g. sequential)
    """
    parent = xblock.get_parent()
    if parent and category:
        if parent.category == category:
            return parent
        else:
            return get_xblock_parent(parent, category)
    return parent
