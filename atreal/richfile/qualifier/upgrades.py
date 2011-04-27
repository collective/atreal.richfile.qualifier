"""Misc GenericSetup upgrade steps"""

PROFILE_NAME = 'profile-atreal.richfile.qualifier:default'


def runAllImportSteps(setuptool):
    """We import all steps 
    """
    setuptool.runAllImportStepsFromProfile(PROFILE_NAME)
    return
