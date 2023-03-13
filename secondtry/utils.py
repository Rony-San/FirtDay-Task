import concurrent.futures
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def check_translation(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        hindi_tags = soup.find_all(lambda tag: tag.name == 'p' and tag.has_attr('lang') and tag['lang'].startswith('hi'))
        if not hindi_tags:
            hindi_tags = soup.find_all(lambda tag: tag.name.startswith('h') and tag.has_attr('lang') and tag['lang'].startswith('hi'))
        if not hindi_tags:
            hindi_tags = soup.find_all(lambda tag: tag.name == 'p' and re.search('[\u0900-\u097f]', tag.text))
        if hindi_tags:
            return {'url': url, 'status': 'PASS'}
        else:
            return {'url': url, 'status': 'FAIL'}
    except requests.exceptions.RequestException as e:
        return {'url': url, 'status': 'ERROR', 'error_message': f"{str(e)}"}
    except Exception as e:
        return {'url': url, 'status': 'ERROR', 'error_message': 'Unknown error occurred.'}


def get_redirect_url(url):
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        hindi_tags = soup.find_all(lambda tag: tag.name == 'p' and tag.has_attr('lang') and tag['lang'].startswith('hi'))
        if not hindi_tags:
            hindi_tags = soup.find_all(lambda tag: tag.name.startswith('h') and tag.has_attr('lang') and tag['lang'].startswith('hi'))
        if not hindi_tags:
            hindi_tags = soup.find_all(lambda tag: tag.name == 'p' and re.search('[\u0900-\u097f]', tag.text))
        if hindi_tags:
            driver.quit()
            return {'url': url, 'status': 'PASS'}
        else:
            driver.quit()
            return {'url': url, 'status': 'FAIL'}
    except requests.exceptions.RequestException as e:
        return {'url': url, 'status': 'ERROR', 'error_message': f"{str(e)}"}
    except Exception as e:
        driver.quit()
        return {'url': url, 'status': 'ERROR', 'error_message': 'Unknown error occurred.'}
