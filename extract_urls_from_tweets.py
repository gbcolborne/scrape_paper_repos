import argparse, json, requests
from ArXivParser import ArXivParser
from ACLAnthologyParser import ACLAnthologyParser

""" Take list of Twitter statuses (in JSON text format), extract URLs
belonging to certain domains (arXiv, ACL Anthology). """

def expand_short_url(url):
    r = requests.get(url, allow_redirects=False)
    try:
        return r.headers['location']
    except KeyError:
        print(url, "Page doesn't exist!")
        return None

def extract_urls_from_status_first_level(status):
    """ Extract URLs from a Twitter status, without looking at any quoted statuses. """
    return [url["expanded_url"] for url in status["entities"]["urls"]]

def extract_urls_from_status(status, include_quoted=True):
    """ Extract all URLs from a Twitter status, including those in the quoted status, if applicable. """
    urls = extract_urls_from_status_first_level(status)
    # Check if it's a retweet
    if include_quoted and status["is_quote_status"] and "quoted_status" in status:
        quoted_status = status["quoted_status"]
        urls += extract_urls_from_status_first_level(quoted_status)
    return urls

def extract_user_name_from_status(status):
    return status["user"]["name"]

def extract_user_name_from_status(status):
    return status["user"]["name"]

def extract_date_from_status(status):
    return status["created_at"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", type=str, help="Path of text file containing Twitter statuses in JSON format")
    parser.add_argument("output_path", type=str, help="Path of output text file containing URLs")
    args = parser.parse_args()

    # Make parsers
    parsers = {}
    parsers["arxiv"] = ArXivParser()
    parsers["acl"] = ACLAnthologyParser()

    # Load statuses
    statuses = json.load(open(args.input_path))
    print("Loaded {} statuses...".format(len(statuses)))
    
    # Extract URLs
    print("Extracting URLs...")
    data = []
    for status in statuses:
        user = extract_user_name_from_status(status)
        date = extract_date_from_status(status)
        urls = extract_urls_from_status(status, include_quoted=True)
        for url in urls:
            # Expand if this is a t.co link
            if len(url) > 13 and url[:13] == "https://t.co/":
                url = expand_short_url(url)
                if url == None:
                    continue
                else:
                    print(url)
            data.append((user,date,url))
            
    # Filter URLs by domain
    urls = {k:[] for k in parsers.keys()}
    seen_urls = set()
    for user,date,url in data:
        if url not in seen_urls:
            seen_urls.add(url)
            for parser_name in parsers.keys():
                if parsers[parser_name].match_url(url):
                    urls[parser_name].append(parsers[parser_name].normalize_url(url))
                    break
    print("Found {} relevant URLs".format(len(urls)))
    for k,v in urls.items():
        print("  - {}: {}".format(k, len(v)))

    # Write URLs
    with open(args.output_path, "w") as f:
        for k,v in urls.items():
            urls = sorted(v)
            for url in urls:
                f.write("{}\n".format(url))
    print("Wrote URLs --> {}".format(args.output_path))

if __name__ == "__main__":
    main()
