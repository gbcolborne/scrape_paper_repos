import re
from PaperRepoParser import PaperRepoParser, init_meta
from utils import get_soup

class ArXivParser(PaperRepoParser):

    def __init__(self):
        self.url_matcher = re.compile("(https?://)arxiv.org/(abs|pdf)/(\d{4}\.\d{5,6}v?\d?)(\.pdf)?")

    def match_url(self, url):
        """ Check URL against known URL formats for ArXiv pages. Return match object. """
        return self.url_matcher.match(url)

    def normalize_url(self, url):
        """ Normalize URL, assuming it matches a known ArXiv URL
        format. If the query matches the URL format for PDFs, change
        it so that it points to the metadata (landing) page. Return
        normalized URL."""
        match = self.url_matcher.match(url)
        url = match.group(0)
        url = self.url_matcher.sub("https://arxiv.org/abs/\\3", url)
        return url

    def parse(self, url):
        """ Given URL of an ArXiv page, extract metadata. Return
        metadata."""

        # Normalize URL
        url = self.normalize_url(url)

        # Parse
        soup = get_soup(url)
        meta_tags = soup.find_all("meta")
        meta = init_meta()
        for tag in meta_tags:
            attributes = tag.attrs
            content = tag["content"]
            if "name" in attributes:
                name = tag["name"]
                if name == "citation_title":
                    meta["title"] = content
                elif name == "citation_author":
                    meta["authors"].append(content)
                elif name == "citation_date" or name == "citation_online_date":
                    meta["date"] = content
            if "property" in attributes:
                prop = tag["property"]
                if prop == "og:description":
                    meta["abstract"] = content
                    # remove line breaks
                    # meta["abstract"] = meta["abstract"].replace("\n", " ")

        # Extract additional metadata
        table_tags = soup.find_all("table")
        for tag in table_tags:
            attributes = tag.attrs
            if "summary" in attributes and tag["summary"] == "Additional metadata":
            
                # loop over table rows (children of tag)
                rows = tag.find_all("tr")
                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) < 2:
                        break
                    # check if the text content if the first td
                    # matches one of the relevant fields (that we want
                    # to include in our notes)
                    if cols[0].string is None:
                        label = "".join([s.strip() for s in cols[0].strings])
                    else:
                        label = cols[0].string.strip()
                    if label in ["Comments:", "Journal\xa0reference:", "DOI:"]:
                        if label == "DOI":
                            metadata = cols[1].a["data-doi"]
                        else:
                            metadata = cols[1].string
                        meta["notes"].append("{} {}".format(label, metadata))
        return meta
