from zope.annotation.interfaces import IAnnotations
from BTrees.OOBTree import OOBTree
from zope.interface import implements
from zope.interface import Interface
from zope.formlib import form
from zope.component import getUtility, getMultiAdapter, adapts
from zope.event import notify
from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces.http import IHTTPRequest

from persistent.mapping import PersistentMapping
from Products.Five  import BrowserView
from Products.Archetypes.BaseObject import Wrapper
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from kss.core import KSSView, kssaction

from plone.app.form.validators import null_validator
from AccessControl import getSecurityManager
from AccessControl.Permissions import view_management_screens
from plone.app.controlpanel.events import ConfigurationChangedEvent
from zope.schema import TextLine, Choice, List, Bool, Password
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot

from Products.statusmessages.interfaces import IStatusMessage

from plone.app.kss.plonekssview import PloneKSSView
from plone.app.kss.interfaces import IPloneKSSView
from plone.fieldsets.form import FieldsetsEditForm
from plone.app.controlpanel.interfaces import IPloneControlPanelForm
from plone.protect import CheckAuthenticator

from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from atreal.richfile.qualifier.interfaces import IRFPlugin, IRFView, IRFUtility, IFileQualifiable
from atreal.filestorage.common.interfaces import IAnnotFileStore
from atreal.richfile.qualifier import RichFileQualifierMessageFactory as _

try: 
    # Plone 4 and higher 
    import plone.app.upgrade 
    PLONE_VERSION = 4 
except ImportError: 
    PLONE_VERSION = 3

class RFPlugin(object):
    """ Base class """

    implements(IRFPlugin)

    _storage = None
    _info = None
    _request_info = None

    # 'plone' or 'convertdaemon'
    engine = 'plone'

    def __init__(self, context):
        """ """
        self.context = context


    @property
    def request_info(self):
        key = self.__class__.__name__
        if self._request_info is None:
            annotations = IAnnotations(self.context.REQUEST)
            if not annotations.has_key(key):
                annotations[key] = PersistentMapping()
            self._request_info = annotations[key]
        return self._request_info


    @property
    def info(self):
        key = self.__class__.__name__
        if self._info is None:
            annotations = IAnnotations(self.context)
            if not annotations.has_key(key):
                annotations[key] = PersistentMapping()
            self._info = annotations[key]
        return self._info


    @property
    def storage(self):
        key = self.__class__.__name__
        if self._storage is None:
            self._storage = IAnnotFileStore(self.context).getOrCreate(key)
        return self._storage


    def hasInfo(self):
        """ True if the plugin has storage """
        key = self.__class__.__name__
        annotations = IAnnotations(self.context)
        if annotations.has_key(key):
            return True
        else:
            return False


    def hasStorage(self):
        """ True if the plugin has storage """
        key = self.__class__.__name__
        afs = IAnnotFileStore(self.context)
        if afs.has_key(key):
            return True
        else:
            return False


    def isActive(self):
        """ True if the plugin is active on the object """
        if self.info.has_key('active'):
            return self.info['active']
        else:
            return True


    def active(self, value):
        """ Active or unactive the plugin on the object """
        if self.isActive() == value:
            return
        elif self.isActive() == True and value == False:
            # unactivation process
            self.cleanUp()
            self.info['active'] = value
        elif self.isActive() == False and value == True:
            # activation process
            self.info['active'] = value
            self.process()


    def process(self):
        """ This method has to be launched on first call """
        raise NotImplementedError("Subclass Responsiblity")


    def cleanUp(self):
        """ Clean all datas created by the plugin """
        key = self.__class__.__name__
        # info
        annotations = IAnnotations(self.context)
        if annotations.has_key(key):
            del annotations[key]
        self._info = None
        # storage
        afs = IAnnotFileStore(self.context)
        if afs.has_key(key):
            afs.remove(key)
        self._storage = None


    def getSubObject(self, id):
        """
        """
        fileobj = self.storage.getPath(id, None)
        if fileobj is None:
            raise AttributeError
        data = fileobj.open('r').read()
        mime = fileobj.getContentType()
        if mime is None:
            mtr = self.context.mimetypes_registry
            mime = mtr.classify(data, filename=id)
            mime = str(mime) or 'application/octet-stream'
        return (data, mime)


    def setSubObject(self, id, data, mime = None):
        """
        """
        fileobj = self.storage.getOrMakeFile(id)
        if isinstance(data, str):
            buffer = data
        else:
            buffer = []
            current = data
            while not current is None:
                buffer.append(current.data)
                current = current.next
            buffer = "".join(buffer)
        if mime is not None:
            fileobj.setContentType(mime)
        else:
            mtr = self.context.mimetypes_registry
            mime = mtr.classify(buffer, filename=id)
            mime = str(mime) or 'application/octet-stream'
        fileobj.open('wb').write(buffer)


class RFView(PloneKSSView):
    """ Base browser view for RFPlugin """

    implements((IRFView,IPloneKSSView))

    plugin_interface = None
    kss_id = None
    viewlet_name = None
    update_message = None
    waiting_message = _("Your file is being processed. Please come back later.")
    active_message = None
    unactive_message = None


    def __init__(self, context, request):
        """
        """
        PloneKSSView.__init__(self, context, request)
        self.object = self.plugin_interface(context)


    @kssaction
    def update(self, viewlet):
        """ User-called, to update the datas provided by the plugin """
        print "viewlet : %s \n kss_id : %s" % (viewlet, self.kss_id)
        self.object.process()
        self._buildKSSResponse(self.waiting_message, self.update_message)


    @kssaction
    def active(self, viewlet):
        """ User-called, active the plugin process """
        self.object.active(True)
        self._buildKSSResponse(self.active_message, self.active_message)
        print "%s activated on %s" % (self.object.__class__.__name__,
                                   '/'.join(self.context.getPhysicalPath()))


    @kssaction
    def unactive(self, viewlet):
        """ User-called, un-active the plugin process """
        self.object.active(False)
        self._buildKSSResponse(self.unactive_message, self.unactive_message)
        print "%s un-activated on %s" % (self.object.__class__.__name__,
                                   '/'.join(self.context.getPhysicalPath()))
    
    
    @kssaction
    def refresh(self, viewlet):
        """ User-called, to refresh the viewlet """
        ksscore = self.getCommandSet('core')
        zopecommands = self.getCommandSet('zope')
        selector = ksscore.getHtmlIdSelector(self.kss_id)
        zopecommands.refreshViewlet(selector, 'richfile.manager', self.viewlet_name)        


    def _buildKSSResponse(self, msg1, msg2):
        ksscore = self.getCommandSet('core')
        plonecommands = self.getCommandSet('plone')
        zopecommands = self.getCommandSet('zope')
        if self.object.engine == 'convertdaemon':
            plonecommands.issuePortalMessage(msg1, msgtype='info')
        else:
            plonecommands.issuePortalMessage(msg2, msgtype='info')
            selector = ksscore.getHtmlIdSelector(self.kss_id)
            zopecommands.refreshViewlet(selector, 'richfile.manager', self.viewlet_name)


    def __bobo_traverse__(self, REQUEST, name):
        """ transparent access to document subobjects
        """
        try:
            data, mime = self.object.getSubObject(name)
        except AttributeError:
            pass
        else:
            return Wrapper(data, name, mime).__of__(self)
        return getattr(self, name)


class RFTraverse(object):
    """Used to traverse to get subobject method on adapter """
    
    implements(ITraversable)
    adapts(IFileQualifiable, IHTTPRequest)
    
    plugin_interface = None
    
    def __init__(self, context, request=None):
        self.context = context
        self.request = request
        self.object = self.plugin_interface(self.context)
        
    def traverse(self, name, ignore):
        try:
            data, mime = self.object.getSubObject(name)
        except AttributeError:
            pass
        else:
            return Wrapper(data, name, mime).__of__(self.context)
        return None


# Base control panel ###########################################################

class RFControlPanel(FieldsetsEditForm):
    """ A base form to update/clear RF plugin. """

    implements(IPloneControlPanelForm)

    template = None
    form_fields = None
    label = None
    description = None
    form_name = None
    plugin_iface = None 
    # Should be iterable == ((interface, ,...)
    supported_ifaces = None
    

    @form.action(_(u'Update all contents'), name=u'update')
    def handle_update_action(self, action, data):
        CheckAuthenticator(self.request)
        rfutility = getUtility(IRFUtility)
        nb_items, bad_items = rfutility.update(self.context, self.plugin_iface, self.supported_ifaces)
        updated = u'%d %s' % (nb_items, _(u'objects updated.'))
        if not bad_items:
            self.status = updated
        else:
            self.status = u'%s, %d %s: %s' % (updated,
                                              len(bad_items),
                                              _(u'update(s) on object(s) failed'),
                                                ','.join(bad_items),
                                             )        


    @form.action(_(u'Clean all contents'), name=u'clean')
    def handle_clean_action(self, action, data):
        CheckAuthenticator(self.request)
        rfutility = getUtility(IRFUtility)
        nb_items, bad_items = rfutility.clear(self.context, self.plugin_iface, self.supported_ifaces)
        cleaned = u'%d %s' % (nb_items, _(u'objects cleaned.'))
        if not bad_items:
            self.status = cleaned
        else:
            self.status = u'%s, %d %s: %s' % (cleaned,
                                              len(bad_items),
                                              _(u'clean-up on object(s) failed'),
                                                ','.join(bad_items),
                                             )


    @form.action(_(u'label_save', default=u'Save'), name=u'save')
    def handle_edit_action(self, action, data):
        CheckAuthenticator(self.request)
        if form.applyChanges(self.context, self.form_fields, data,
                             self.adapters):
            self.status = _("Changes saved.")
            notify(ConfigurationChangedEvent(self, data))
            #self._on_save(data)
        else:
            self.status = _("No changes made.")


    @form.action(_(u'label_cancel', default=u'Cancel'),
                 validator=null_validator,
                 name=u'cancel')
    def handle_cancel_action(self, action, data):
        IStatusMessage(self.request).addStatusMessage(_("Changes canceled."),
                                                      type="info")
        url = getMultiAdapter((self.context, self.request),
                              name='absolute_url')()
        self.request.response.redirect(url + '/plone_control_panel')
        return ''

    def available(self):
        root = aq_inner(self.context).getPhysicalRoot()
        sm = getSecurityManager()
        return sm.checkPermission(view_management_screens, root)

    def isPlone3(self):
        if PLONE_VERSION == 3:
            return True
        return False

    def isPlone4(self):
        if PLONE_VERSION == 4:
            return True
        return False
