from bs4 import BeautifulSoup
import requests
import re
import json

def biz_links(articles, link_list):
#Input: Beautiful soup object, parsed for a search result page from Yelp and a list of existing links
#Output: List of links to all businesses on that page

    articles = articles.find_all("div", class_="biz-listing-large")
    for article in articles:
        match = re.search(r'href=[\'"]?([^\'" >]+)', str(article.find_all(href = True)))
        if match:
            link = match.group(0)
            link = link[6:]
        link_list.append(link)
        
    return link_list
    

## <span class="business-attribute price-range">$$</span>
## JSON file of all the reviews: <script type="application/ld+json">  
## "city": "Washington", "state": "DC", for longitutde/latitud

def scrap_reviews(biz_link, base_url):
#Input: Beautiful soup object, parsed for a search result page from Yelp and a list of existing links
#Output: List of links to all businesses on that page
    target = base_url + biz_link
    try:
        raw_html = requests.get(target)
        soup = BeautifulSoup(raw_html.text, 'html.parser')
        json_reviews = json.loads(soup.select_one("script[type=application/ld+json]").text)
        return json_reviews
    except ConnectionError:
        return "Captcha is preventing script from loading " + target

def scrap_bizinfo(link_list, base_url):
#Input: List of business links and the base_url for the yelp site
#Output: A dictionary where the keys are business names and the entries are business details

    for link in link_list:
        biz_name = link.replace('?osq=Restaurants', '')
        biz_name = re.sub("-washington*", '', biz_name)
        biz_dict[biz_name] = {}
        
        raw_html = requests.get(base + link)
        soup = BeautifulSoup(raw_html.text, 'html.parser')
        parse_string = str(soup.find_all("script"))
        parse_list = parse_string.split('<script>')
    
        try:
            match = re.sub(".*,null,",'', [s for s in parse_list if re.search(".*latitude.*", s)][0])
        except IndexError:
            "The regexp is matching too many JSON entries, please take a look at " + str(link)
    
        biz_dict[biz_name] = json.loads(re.sub(", \"geoquad\".*",'', match) + '}')
        
    return biz_dict