#!/usr/bin/env python
# -*- coding: utf-8 -*-

__atuthor__ = "ketian"
__time__ = "fall2017"


import re
import os
import requests
from bs4 import BeautifulSoup
import codecs

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

import tldextract

from sys import platform

if platform == "linux" or platform == "linux2":
    path_to_chrome_driver = os.getcwd() + "/dependence/linux/chromedriver"
elif platform == "darwin":
    path_to_chrome_driver = os.getcwd() + "/dependence/chromedriver"
else:
    raise Exception('Not supported platform')


#FIXME UA String List
UA_IE8_Windows7 = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)"
UA_Safari_Mac = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
UA_Chrome_Windows = "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36"
UA_Firefox_Window = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0"

UAs = [UA_IE8_Windows7,UA_Chrome_Windows,UA_Firefox_Window,UA_Safari_Mac]


os.environ["webdriver.chrome.driver"] = path_to_chrome_driver
print (path_to_chrome_driver)


class ChromeConsoleLogging(object):

    def __init__(self, ):
        self.driver = None

    def setUp(self, user_agent=None):

        if user_agent is None:
            self.user_agent = UA_IE8_Windows7
        else:
            self.user_agent = user_agent

        desired = DesiredCapabilities.CHROME

        chrome_options = Options()

        chrome_options.add_argument("user-agent="+self.user_agent)

        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-wifi")
        chrome_options.add_argument("--disable-local-storage")
        chrome_options.add_argument("--disable-gpu")

        chrome_options.add_argument('--disable-application-cache')
        chrome_options.add_argument("--disable-background-networking")


        self.driver = webdriver.Chrome(executable_path=path_to_chrome_driver, desired_capabilities=desired,
                                       chrome_options=chrome_options)
        self.driver.set_page_load_timeout(15)


    def quitDriver(self, ):
        self.driver.quit()

    def get_screenshot(self,site,screenshot=None):
        try:
            self.driver.maximize_window()
            self.driver.get(site)

        except Exception:

            print ("PAGE LOAD Time out")
            self.quitDriver()
            self.setUp()
            return None

        if screenshot is None:
            ex = tldextract.extract(site)
            screenshot = ex.domain+'.'+ex.suffix

        content = self.driver.page_source

        write_page_into_html(screenshot, content)
        self.driver.save_screenshot(screenshot+'.png')
        self.driver.close()



def write_page_into_html(filename,text):
    with codecs.open(filename, 'w', encoding='utf8') as f:
        f.write(text)
        f.flush()
        f.close()


def get_html_page_and_imgs(site):
    response = requests.get(site)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    urls = [img['src'] for img in img_tags]


    for url in urls:
        filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
        with open(filename.group(1), 'wb') as f:
            if 'http' not in url:
                # sometimes an image source can be relative
                # if it is provide the base url which also happens
                # to be the site variable atm.
                url = '{}{}'.format(site, url)
                response = requests.get(url)
                f.write(response.content)



site = 'http://sewauk.org/wp-content/upgrade/025485121information/LOGS/448621c7f53fc6f147b47e5468eb1dbc/'
if __name__ == "__main__":
    chrome = ChromeConsoleLogging()
    chrome.setUp()
    chrome.get_screenshot(site)
