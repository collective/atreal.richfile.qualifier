from atreal.richfile.qualifier.interfaces import IFileQualifier
from atreal.richfile.qualifier.interfaces import IFileQualifiedEvent, IMimetypeChangedEvent
from zope.component.interfaces import ObjectEvent
from zope.interface import implements

from zope.interface.interfaces import IInterface
from zope.component import queryUtility


def is_filequalifier_installed():
    """
    """
    return queryUtility(IInterface, name=u'atreal.richfile.qualifier.IFileQualifierSite', default=False)


class FileQualifiedEvent(ObjectEvent):
    implements(IFileQualifiedEvent)


class MimetypeChangedEvent(ObjectEvent):
    implements(IMimetypeChangedEvent)


def markObject(obj, event):
    """ """
    if not is_filequalifier_installed():
        return
    # At the object creation, we don't have any form
    try:
        form = obj.REQUEST.form
    except AttributeError, e:
        return
    if form.get('file_delete', 'changed') == 'nochange':
        return
    IFileQualifier(obj).process()
    