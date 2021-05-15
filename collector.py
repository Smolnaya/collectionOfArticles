from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

import xmlGenerator
from Article import Article

import concurrent.futures

THREAD_QUANTITY = 1
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
    for a in aList:
        hrefList.append(a.get_attribute('href'))

    driver.quit()

    print('Href: ', len(hrefList))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(THREAD_QUANTITY):
            thread = executor.submit(collectArticles, i, hrefList)


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
            title = driver.find_element_by_xpath("//article/header/h1").text
            date = driver.find_element_by_xpath(f"//article/div/div/a[@href='{href}']").text
            author = driver.find_element_by_xpath(f"//article/div/div/a[@href!='{href}']").text
            textList = driver.find_elements_by_xpath("//article/div/div/p")
            source = driver.find_elements_by_xpath("//article/div/div/div/div/div/a")
            tagList = driver.find_elements_by_xpath("//article/div[3]/div[3]/a")
            text = ''
            tags = ''
            if len(source) > 0:
                source = source[0].text
            else:
                source = ''
            for i in range(len(textList) - 1):
                text += textList[i].text + '\n'
            for elem in tagList:
                tags += elem.text + '\n'
            article = Article(title, date, author, text.strip(), tags.strip(), source)
            xmlGenerator.generateXml(article)
        except TimeoutException as err:
            print(err)
            pass

    driver.quit()
