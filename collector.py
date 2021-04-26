import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import xmlGenerator


def condition(driver):
    ret = False
    time.sleep(10)
    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
    return ret


if __name__ == "__main__":
    url = 'https://the-geek.ru/category/news'
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(url)
    assert 'Новости' in driver.title

    # for i in range(1):
    #     html = driver.find_element_by_tag_name('html')
    #     html.send_keys(Keys.END)

    articleList = driver.find_elements_by_xpath('//article')

    # for article in articleList:
    href = driver.find_element_by_xpath(
        f"//article[@id='{articleList[0].get_attribute('id')}']/a").get_attribute('href')
    driver.execute_script(f"window.open('{href}', 'new_window')")
    driver.switch_to.window(driver.window_handles[1])
    title = driver.find_element_by_xpath("//article/header/h1").text
    date = driver.find_element_by_xpath(f"//article/div/div/a[@href='{href}']").text
    author = driver.find_element_by_xpath(f"//article/div/div/a[@href!='{href}']").text
    textList = driver.find_elements_by_xpath("//article/div/div/p")
    text = ''
    for elem in textList:
        text += elem.text + '\n'
    tags = ''
    source = ''
    try:
        source = driver.find_element_by_xpath("//div[@class='news-source']/a").text
        tagList = driver.find_elements_by_xpath("//div[@class='entry-tags']/a")
        for elem in tagList:
            tags += elem.text + '\n'
    except NoSuchElementException:
        pass

    print(title, date, author, text.strip(), tags.strip(), source, sep='\n******\n')

    # xmlGenerator.generateXml(title, date, author, text, tags, source)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    driver.close()
