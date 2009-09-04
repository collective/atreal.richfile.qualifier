from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager
from zope.component.interfaces import IObjectEvent
from atreal.richfile.qualifier import RichFileQualifierMessageFactory as _

# Adapters and markers #########################################################

class IFileQualifierLayer(Interface):
    """ Marker interface that defines a Zope 3 browser layer.
    """

class IFileQualifierSite(Interface):
    """ Marker interface for sites with this product installed.
    """ 
    
class IFileQualifiable(Interface):
    """
        Use this to mark your CT if it can be qualifiable
    """

class IFileQualifier(Interface):
    """
        Use to qualify a CT
    """


# Events #######################################################################

class IFileQualifiedEvent(IObjectEvent):
    """ Event notified after qualification process """
    
    
class IMimetypeChangedEvent(IObjectEvent):
    """ Event notified mimetype change """


# Base class ###################################################################
    
class IRFPlugin(Interface):
    """ Interface for base plugin """

    def isActive(self):
        """ True if the plugin is active on the object """

    def active(self, value):
        """ Active or unactive the plugin on the object """

    def process(self):
        """ This method has to be launched on first call """

    def cleanUp(self):
        """ Clean all datas created by the plugin """


class IRFView(Interface):

    def __init__(self, context, request):
        """
            This method as to be redefined in the plugin, in order to adapt the
            context with the right adapter, like :
            ...            
            self.object = IRFPlugin(context)
            ...
        """
    
    def update(self):
        """ User-called, to update the datas provided by the plugin """

    def active(self):
        """ User-called, active the plugin process """

    def unactive(self):
        """ User-called, un-active the plugin process """


# Utility ######################################################################

class IRFUtility(Interface):
    """ Component capable of triggering batched operations """
    
    
# Viewlet Manager ##############################################################
    
class IRFViewletManager(IViewletManager):
    """ A viewlet manager thats sits above content, used by richfile plugin viewlet
    """

