
from suds.client import Client

class WoRMSClient(object): 
    """
    Class for accessing the WoRMS taxonomic name database via the AphiaNameService. 
    
    The Aphia names services are described at http://marinespecies.org/aphia.php?p=soap. 
    """
    
    WORMS_APHIA_NAME_SERVICE_URL = 'http://marinespecies.org/aphia.php?p=soap&wsdl=1'

    def __init__(self, marine_only=False):
        """ Initialize a SOAP client using the WSDL for the WoRMS Aphia names service"""        
        self._client = Client(self.WORMS_APHIA_NAME_SERVICE_URL)
        self._marine_only = marine_only

    def aphia_record_by_exact_name(self, name):
        """
        Perform an exact match on the input name against the taxon names in WoRMS.
        
        This function first invokes an Aphia names service to lookup the Aphia ID for
        the taxon name.  If exactly one match is returned, this function retrieves the
        Aphia record for that ID and returns it. 
        """        
        aphia_id = self._client.service.getAphiaID(name, self._marine_only);
        if aphia_id is None or aphia_id == -999:         # -999 indicates multiple matches
            return None
        else:
            return self._client.service.getAphiaRecordByID(aphia_id)

    def aphia_record_by_fuzzy_name(self, name):
        """
        Perform fuzzy match search for the input name against the taxon names in WoRMS.
        
        The invoked Aphia names service returns a list of list matches.  This function 
        returns a match only if exactly one match is returned by the AphiaNameService. 
        """        
        matches = self._client.service.matchAphiaRecordsByNames(name, self._marine_only);
        if len(matches) == 1 and len(matches[0]) == 1:
            return matches[0][0]
        else:
            return None
      
if __name__ == '__main__':
    """ Demonstration of class usage"""
    wc = WoRMSClient()
    print wc.aphia_record_by_taxon_name('Mollusca')[1]
    print wc.aphia_record_by_taxon_name('Architectonica reevi')[1]