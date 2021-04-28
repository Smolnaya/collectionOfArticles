from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from Article import Article

import concurrent.futures

THREAD_QUANTITY = 4


def getArticles(articleNumber):
    articles = list()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(THREAD_QUANTITY):
            thread = executor.submit(collectArticles, articleNumber, i)
        val = thread.result()
        articles.extend(val)
    return articles


def splitList(fullList, wanted_parts=THREAD_QUANTITY):
    length = len(fullList)
    return [fullList[i * length // wanted_parts: (i + 1) * length // wanted_parts]
            for i in range(wanted_parts)]


def collectArticles(articleNumber, param):
    url = 'https://the-geek.ru/category/news'
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(url)
    assert 'Новости' in driver.title

    articleElem = list()
    while len(articleElem) < articleNumber:
        html = driver.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        articleElem = driver.find_elements_by_xpath('//article')
    print('articleElem: ', len(articleElem))

    parts = splitList(articleElem)
    lst = parts[param]

    articleList = list()
    for article in lst:
        href = driver.find_element_by_xpath(f"//article[@id='{article.get_attribute('id')}']/a") \
            .get_attribute('href')
        driver.execute_script(f"window.open('{href}', 'new_window')")
        driver.switch_to.window(driver.window_handles[1])
        try:
            title = driver.find_element_by_xpath("//article/header/h1").text
            date = driver.find_element_by_xpath(f"//article/div/div/a[@href='{href}']").text
            author = driver.find_element_by_xpath(f"//article/div/div/a[@href!='{href}']").text
            source = driver.find_element_by_xpath("//article/div/div/div/div/div/a").text
            textList = driver.find_elements_by_xpath("//article/div/div/p")
            tagList = driver.find_elements_by_xpath("//article/div[3]/div[3]/a")
            text = ''
            tags = ''
            for elem in textList:
                text += elem.text + '\n'
            for elem in tagList:
                tags += elem.text + '\n'
            articleList.append(Article(title, date, author, text.strip(), tags.strip(), source))
        except Exception as err:
            print(f'Exception: {err}')
        finally:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    driver.close()
    return articleList
