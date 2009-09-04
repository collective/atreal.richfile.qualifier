from zope.interface import implements

from Products.CMFCore.utils import getToolByName

from atreal.richfile.qualifier.interfaces import IRFUtility
from atreal.richfile.qualifier.registry import provided_interfaces


class RFUtility(object):
    """ Component capable of triggering batched operations """
    
    implements(IRFUtility)
    
    def update(self, context, iface, ifaces_str):
        """ """
        return self._walker(context, iface, ifaces_str, 'process')


    def clear(self, context, iface, ifaces_str):
        """ """
        return self._walker(context, iface, ifaces_str, 'cleanUp')
    
    
    def _walker(self, context, iface, ifaces_str, meth):
        """ """
        pc = getToolByName(context, 'portal_catalog')
        bad_objects = []
        i = 0
        brains = pc(object_provides = ifaces_str)
        for brain in brains:
            try:
                process = getattr(iface(brain.getObject()), meth, None)
                if process != None:
                    process()
                i += 1
            except:
                bad_objects.append(brain.getPath())
                continue
        return i, bad_objects
