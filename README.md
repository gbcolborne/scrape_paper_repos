# scrape_paper_repos

Code to scrape paper repositories such as arXiv and the ACL Anthology.

The main script is `scrape_paper_repos.py`.

Input is a list of URLs of papers. Output is a file that contains
metadata for each paper, e.g. title, year, author, and abstract.

At the moment, I've implemented parsers for arXiv and the ACL
Anthology. To scrape other repositories you can create your own
PaperRepoParser, and modify the code to exploit that subclass.
