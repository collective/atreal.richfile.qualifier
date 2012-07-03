from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter, queryMultiAdapter, queryUtility
from Products.CMFPlone.interfaces import IPloneSiteRoot

from atreal.richfile.qualifier import RichFileQualifierMessageFactory as _

class RichfileViewlet(ViewletBase):
    """ """
    
    controls = ViewPageTemplateFile("controls.pt")
    marker_interface = None
    plugin_interface = None
    plugin_id = None
    plugin_title = None
    controlpanel_interface = None
    
    def getPluginTitle(self):
        """ Get the localized plugin title """
        return _(self.plugin_title)

    def actions(self):
        """ """
        ctx = getMultiAdapter((self.context, self.request),
                                     name='plone_context_state')
        return ctx.actions()['richfile']

    def actions_menus(self):
        """ """
        ctx = getMultiAdapter((self.context, self.request),
                                     name='plone_context_state')
        menus_actions = []
        for k,v in ctx.actions().items():
            if k.find('richfile/') != -1:
                menus_actions.append(v)
        return menus_actions

    def update(self):
        super(RichfileViewlet, self).update()
        self.tools = getMultiAdapter((self.context, self.request),
                                     name='plone_tools')


    @property
    def active(self):
        return self.plugin_interface(self.context).isActive()

    
    def anonymous(self):
        return self.portal_state.anonymous()


    def canModify(self):
        membership = self.tools.membership()
        authorized = membership.checkPermission('Modify portal content', self.context)
        return authorized


    @property
    def available(self):
        #active = self.plugin_interface(self.context).isActive()
        marked = self.marker_interface.providedBy(self.context)
        if not marked:
            return False
        if self.active:
            return True
        if not self.active and self.canModify():
            return True
        return False
    
    
    def getKSSAttr(self):
        kssattr = ("kssattr-viewlet-%(v)s "
                  "kssattr-bodyId-%(v)sBody "
                  "kssattr-toggleOnExpand-%(v)sCollapse "
                  "kssattr-toggleOnCollapse-%(v)sExpand "
                  "kssattr-menuId-%(v)sMenu "
                  % dict(v=self.plugin_id))
        return kssattr
    
    
    def collapsed(self):
        """ Return 'rfcollapsed' if the viewlet should be collapsed on load, None either
        """
        if self.anonymous():
            return
        config = self._getConfig()
        if not config:
            return
        if getattr(config, 'rf_%s_collapsed' % self.plugin_id, None):
            return 'rfcollapsed'
        return


    def collapsedControlClass(self):
        config = self._getConfig()
        if not config:
            return None
        collapsed = getattr(config, 'rf_%s_collapsed' % self.plugin_id, False)
        if collapsed:
            return 'rfcollapsed'
        else:
            return None

    
    def expandedControlClass(self):
        config = self._getConfig()
        if not config:
            return 'rfcollapsed'
        collapsed = getattr(config, 'rf_%s_collapsed' % self.plugin_id, False)
        if collapsed:
            return None
        else:
            return 'rfcollapsed'

    
    def _getConfig(self):
        siteroot = queryUtility(IPloneSiteRoot)
        config = self.controlpanel_interface(siteroot)
        return config
        


  
