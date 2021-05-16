from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

import xmlGenerator

import concurrent.futures

THREAD_QUANTITY = 4
URL = 'https://the-geek.ru/category/news'


def splitList(fullList):
    length = len(fullList)
    return [fullList[i * length // THREAD_QUANTITY: (i + 1) * length // THREAD_QUANTITY]
            for i in range(THREAD_QUANTITY)]


def getArticles(articleNumber):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(10)
    driver.get(URL)
    assert 'Новости' in driver.title

    aList = list()
    while len(aList) < articleNumber:
        html = driver.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        aList = driver.find_elements_by_xpath(f"//article/a")

    hrefList = list()
    for i in range(articleNumber):
        hrefList.append(aList[i].get_attribute('href'))

    driver.quit()

    print('Href: ', len(hrefList))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(THREAD_QUANTITY):
            executor.submit(collectArticles, i, hrefList)


def collectArticles(param, hrefList):
    parts = splitList(hrefList)
    lst = parts[param]

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    for href in lst:
        try:
            driver.get(href)
            title = driver.find_element_by_xpath(
                "//h1[contains(@class, 'entry-title')]").text
            date = driver.find_element_by_xpath(
                "//div[contains(@class, 'entry-action')]/div/a[1]").text
            author = driver.find_element_by_xpath(
                "//div[contains(@class, 'entry-action')]/div/a[2]").text
            textList = driver.find_elements_by_xpath(
                "//div[contains(@class, 'entry-content')]/p")
            source = driver.find_elements_by_xpath(
                "//div[contains(@class, 'news-source')]/a")
            tagList = driver.find_elements_by_xpath(
                "//div[contains(@class, 'entry-tags')]/a")

            if len(source) > 0:
                source = source[0].text
            else:
                source = ''
            text = [textList[i].text for i in range(len(textList) - 2)]
            text = ' '.join(text)
            tagListText = [elem.text for elem in tagList]
            article = [title, date, author, text, tagListText, source, href]
            xmlGenerator.generateXml(article)
        except TimeoutException as err:
            print(err)
            pass

    driver.quit()
