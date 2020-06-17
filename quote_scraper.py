from bs4 import BeautifulSoup
import requests
import re


def get_soup(url):
    """ makes request then returns soup object"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def scrape_quotes():
    """ 
    scrapes every page on quote website and returns list of lists with
    author, quote, and link to bio
    """
    url = "http://quotes.toscrape.com/"
    lol_quotes = [] 
    more_pages = True 
    while more_pages:
        
        # Make request and parse
        soup = get_soup(url)
        quotes = soup.select('.quote') # Grab quotes
        
        # Check to see if there is a next page 
        if not soup.find(class_="next"):
            more_pages = False

        # From quotes we need to grab: text of quote, name of person, link to persons bio 
        for q in quotes:
            quote = q.find('span', class_='text').get_text()
            name = q.find('small').get_text()
            p_path = q.find('a').get('href')
            bio_url = f"http://quotes.toscrape.com{p_path}"
            lol_quotes.append([quote, name, bio_url])
        
        # Grab the next page to scrape
        if more_pages:
            next_href = soup.select('.next')[0].find('a').get('href')
            url = f"http://quotes.toscrape.com{next_href}"
    
    return lol_quotes    


def scrape_dob_loc(url):
    """ Scrapes the authors bio for his date of birth and birth location """
    soup = get_soup(url)
    dob = soup.select_one('.author-born-date').get_text()
    location = soup.select_one('.author-born-location').get_text()
    return f"{dob} {location}"

def get_description(url):
    """ Gets the description of the author and splits it into a list at the end of each sentence"""
    soup = get_soup(url)
    description = soup.select_one('.author-description').get_text()
    description_sentences = re.split(r"(?<=\w)[.](?=\s)", description)
    return description_sentences

def scrape_first_two(url):
    """ Gets first two sentences of the author bio description """
    s = get_description(url)
    first_two = " ".join(s[:2])
    return first_two.lstrip()

def scrape_second_two(url):
    """ Gets second two sentences of the author bio description """
    s = get_description(url)
    second_two = " ".join(s[2:5])
    return second_two.lstrip()
    
    
    


