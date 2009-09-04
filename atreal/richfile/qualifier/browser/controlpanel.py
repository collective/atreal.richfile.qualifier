from zope.interface import Interface
from zope.component import adapts
from zope.interface import implements
from zope.schema import TextLine, Choice, List, Bool
from zope.formlib import form

from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from atreal.richfile.qualifier import RichFileQualifierMessageFactory as _
from atreal.richfile.qualifier.common import RFControlPanel

from atreal.richfile.qualifier.interfaces import IFileQualifier
from plone.app.controlpanel.form import ControlPanelForm


class IRichFileQualifierSchema(Interface):
    """ """

    
    
class RichFileQualifierControlPanelAdapter(SchemaAdapterBase):
    """ """
    adapts(IPloneSiteRoot)
    implements(IRichFileQualifierSchema)
    
    
    
class RichFileQualifierControlPanel(RFControlPanel):
    template = ZopeTwoPageTemplateFile('controlpanel.pt')
    form_fields = form.FormFields(IRichFileQualifierSchema)
    label = _("RichFileQualifier settings")
    description = _("RichFileQualifier settings for this site.")
    form_name = _("RichFileQualifier settings")
    plugin_iface = IFileQualifier
    supported_ifaces = ('atreal.richfile.qualifier.interfaces.IFileQualifiable',)
