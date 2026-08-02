class DiscoveryError(Exception):
    """
    Base exception for errors detected during campaign discovery.
    """

class InvalidCampaignError(DiscoveryError):
    """
    The campaign directory has an invalid structure.
    """

class MissingDeviceExportError(DiscoveryError):
    """
    A device is missing a required export.
    """ 

class DuplicateExportFileError(DiscoveryError):
    """
    More than one file was found for the same export type.  
    """
