# coding=utf-8
from lxml import html
import requests
import json
import time

INIT = "http://elpais.com/tag/c/aac32d0cdce5eeb99b187a446e57a9f7"

def process_editorial_list(url):
    """
    Process a page that contains a list of editorials.
    Returns:
        - A list of URLs to individual editorial articles.
        - The URL to the next editorial list.
    """
    content = requests.get(url).text
    tree = html.fromstring(content)
    next_edlist = get_next_edlist(tree)
    artlist = get_edarticles(tree)
    
    return (artlist, next_edlist)

def get_next_edlist(tree):
    """
    Returns the URL for the next editorial page
    """
    next_edlist = tree.xpath(u'//a[@title="' + "Página siguiente".decode("utf8") + '"]/@href')
    next_edlist = "http://www.elpais.com" + next_edlist[0]
    return(next_edlist)

def get_edarticles(tree):
    """
    Returns a list with the URLs of the editorial articles
    from a page containing a list of editorials.
    """
    artlist = tree.xpath('//div[@class="columna_principal"]//h2/a[@title="Ver noticia"]/@href')
    return(artlist)
    
def get_article_info(url):
    """
    Returns a dictionary with the article info.
    The dictionary contains the following fields:
    - date
    - title
    - tags (list of tags at the end of the article)
    - url
    """
    content = requests.get(url).text
    tree = html.fromstring(content)
    title = tree.xpath('//h1[@id="articulo-titulo"]/text()')[0]
    date = tree.xpath('//time//a/text()')[0].strip()
    tags = tree.xpath('//li[@itemprop="keywords"]/a/text()')
    url = url

    result = {'date': date, 'title': title, 'tags': tags, 'url': url}
    return(result)    
    
if __name__ == "__main__":
    """
    Starting from the first editorial page, retrieve the information
    for all op-eds published in El Pais from 1976 until today.
    After each batch is processed, store the results as a json file
    for further processing.
    """
    results = []
    next_edlist = INIT
    while next_edlist and next_edlist.find('void') == -1:
        artlist, next_edlist = process_editorial_list(next_edlist)
        for article in artlist:
            time.sleep(1)
            info = get_article_info(article)
            print(info)
            results.append(info)
        # Save partial 
        with open("elpais_opeds.json", "w") as f:
            json.dump(results, f)
        