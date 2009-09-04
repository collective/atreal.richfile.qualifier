import logging
logger = logging.getLogger('atreal.richfile.qualifier')
LOG = logger.info

provided_interfaces = []
filequalifier_registry = {}

def registerRFPlugin(interface, mimetypes):
    """
    Use it to register the plugin with the qualifier.
    
    # To register your own plugin, add the sample below 
    ---
    from atreal.richfile.streaming.interfaces import IMyPluggin
    try:
        from atreal.richfile.qualifier.registry import registerRFPlugin
    except:
        return
    supported_mimetypes = [
        'application/zip',
        ]
    registerRFPlugin(IMyPlugin, supported_mimetypes)
    ---
    """
    
    # We add our interface
    if not interface in provided_interfaces:
        provided_interfaces.append(interface)
        
    # We link our interface to the supported mimetypes
    for mt in mimetypes:
        if not filequalifier_registry.has_key(mt):
            filequalifier_registry[mt] = [interface,]
        elif not interface in filequalifier_registry[mt]:
            filequalifier_registry[mt] = filequalifier_registry[mt]+[interface,]
    
    LOG("%s plugin added" % interface)
