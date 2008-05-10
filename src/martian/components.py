##############################################################################
#
# Copyright (c) 2006-2007 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

from zope.interface import implements

from martian.interfaces import IGrokker, IComponentGrokker
from martian import util

NOT_DEFINED = object()

class GrokkerBase(object):
    implements(IGrokker)

    priority = 0
    
    def grok(self, name, obj, **kw):
        raise NotImplementedError

    
class GlobalGrokker(GrokkerBase):
    """Grokker that groks once per module.
    """

    def grok(self, name, obj, **kw):
        raise NotImplementedError
    

class ComponentGrokkerBase(GrokkerBase):
    implements(IComponentGrokker)

    component_class = NOT_DEFINED

    def grok(self, name, obj, **kw):
        raise NotImplementedError


class ClassGrokker(ComponentGrokkerBase):
    """Grokker that groks classes in a module.
    """
    # Use a tuple instead of a list here to make it immutable, just to be safe
    directives = ()

    def grok(self, name, class_, module_info=None, **kw):
        module = None
        if module_info is not None:
            module = module_info.getModule()

        # Populate the data dict with information from the directives:
        for directive in self.directives:
            kw[directive.name] = directive.get(class_, module, **kw)
        return self.execute(class_, **kw)

    def execute(self, class_, **data):
        raise NotImplementedError

class InstanceGrokker(ComponentGrokkerBase):
    """Grokker that groks instances in a module.
    """
    pass
