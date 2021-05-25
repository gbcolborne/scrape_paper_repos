import re
from PaperRepoParser import PaperRepoParser, init_meta
from utils import get_soup

class ACLAnthologyParser(PaperRepoParser):

    def __init__(self):
        self.url_matchers = {}
<<<<<<< HEAD
        self.url_matchers["pdf"] = re.compile("(https?://)(www.)?aclanthology.org/.+\.pdf")
        self.url_matchers["landing"] = re.compile("(https?://)(www.)?aclanthology.org/.+")        
=======
        self.url_matchers["landing"] = re.compile("(https?://)www.aclweb.org/anthology/.+")

>>>>>>> 845d1e18f9c41db894be7fd2f9ee7758d3333aef

    def match_url(self, url):
        """ Match URL against known URL formats for the ACL
        Anthology. There are 2 URL formats. Return whichever one
        matches first."""
        match = None
        for t in ["landing"]:
            candidate_match = self.url_matchers[t].match(url)
            if candidate_match:
                match = candidate_match
                break
        return match

    def normalize_url(self, url):
        """Normalize URL, assuming it matches a known ACL Anthology URL
        format. If the query matches the URL format for PDFs, change
        it so that it points to the metadata page.  Return normalized
        URL.

        """
<<<<<<< HEAD
        match = self.url_matchers["pdf"].match(url)
        if match:
            url = url[:-4]
=======
        if url[-4:] == '.pdf':
            url = url[:-4]
        if url[-1] == '/':
            url = url[:-1]
>>>>>>> 845d1e18f9c41db894be7fd2f9ee7758d3333aef
        return url

    def parse(self, url):
        """ Given URL of an ACL Anthology page, extract
        metadata. Return metadata."""

        # Normalize URL
        url = self.normalize_url(url)

        # Parse
        soup = get_soup(url)
        meta_tags = soup.find_all("meta")
        meta = init_meta()
        for tag in meta_tags:
            attributes = tag.attrs
            if "content" in attributes:
                content = tag["content"]
            else:
                continue
            if "name" in attributes:
                name = tag["name"]
                if name == "citation_title":
                    meta["title"] = content
                elif name == "citation_author":
                    meta["authors"].append(content)
                elif name == "citation_publication_date":
                    meta["date"] = content
                elif name == "citation_conference_title":
                    meta["notes"].append("In {}".format(content))
                elif name == "citation_journal_title":
                    meta["notes"].append("Published in {}".format(content))
                elif name == "citation_doi":
                    meta["notes"].append("DOI: {}".format(content))
        # Search for the abstract. It may not be available in the
        # metadata page (and I don't want to implement converting the
        # PDF to text and extracting the abstract).
        abs_div = soup.find("div", class_=["card-body", "acl-abstract"])
        if abs_div:
            abstract = abs_div.h5.next_sibling.string
        else:
            abstract = None
        if abstract:
            meta["abstract"] = abstract
        else:
            meta["abstract"] = ""
        return meta
