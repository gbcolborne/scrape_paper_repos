from abc import ABC, abstractmethod

def init_meta():
    """ Initialize a dictionary that will contain the metadata. """
    meta = {}
    meta["title"] = None
    meta["authors"] = []
    meta["date"] = None
    meta["abstract"] = None
    meta["notes"] = []    
    return meta

class PaperRepoParser(ABC):

    @abstractmethod
    def match_url(self, url):
        """ Match URL against known URL formats for this repository 
        of papers (e.g. URL for papers and/or landing pages). Return 
        match object. """
        pass

    @abstractmethod
    def normalize_url(self, url):
        """ Return normalized URL, assuming it matches a known URL
        format for this repository of papers. Return
        normalized URL."""
        pass

    @abstractmethod
    def parse(self, url):
        """ Parse metadata of paper at given URL. Store in structure
        returned by utils.init_meta. Return metadata. """
        pass
