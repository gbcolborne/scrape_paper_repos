#! /usr/bin/env python
#! coding: utf-8

""" Take URLs of ArXiv or ACL Anthology pages from stdin, extract data from URLs, write to stdout """

import sys
from ArXivParser import ArXivParser
from ACLAnthologyParser import ACLAnthologyParser

def main():
    # Make parsers
    parsers = {}
    parsers["arxiv"] = ArXivParser()
    parsers["acl"] = ACLAnthologyParser()

    # Define printing format of output text block for each input line
    print_format = "%s\n\n\n"
    
    for line in sys.stdin:
        url = line.rstrip()
        meta = None
        for parser_name in ["arxiv", "acl"]:
            parser = parsers[parser_name]
            match = parser.match_url(url)
            if match:
                meta = parser.parse(url)
                break
        
        # Check if one of the parsers handled the URL
        if meta is None:
            msg = "ERROR: URL '{}' does not match known formats (ArXiv and ACL Anthology).".format(url)
            sys.stderr.write(print_format % msg)
            continue

        # Check data types in metadata
        sub = "[PARSING ERROR]"        
        if not isinstance(meta["title"], str):
            meta["title"] = sub
        if not isinstance(meta["date"], str):
            meta["date"] = sub
        if not isinstance(meta["abstract"], str):
            meta["abstract"] = sub
        for i in range(len(meta["authors"])):
            if not isinstance(meta["authors"][i], str):
                meta["authors"][i] = sub
        for i in range(len(meta["notes"])):
            if not isinstance(meta["notes"][i], str):
                meta["authors"][i] = sub

        # Prepare output text block
        msgs = []
        msgs.append("# {}".format(meta["title"]))
        msgs.append("Authors: {}".format(" and ".join(meta["authors"])))
        msgs.append("Date: {}".format(meta["date"]))
        msgs.append("URL: {}".format(url))
        msgs.append('Abstract: "{}"'.format(meta["abstract"]))
        msgs.append("Notes:")
        if len(meta["notes"]):
            for n in meta["notes"]:
                msgs.append("- {}".format(n))
        msg = "\n".join(msgs)

        # Write
        sys.stdout.write(print_format % msg)
                              
        

if __name__ == "__main__":
    main()
