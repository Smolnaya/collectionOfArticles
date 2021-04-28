import time
import collector
import xmlGenerator
import datetime
import os

if __name__ == "__main__":
    start_time = time.time()

    # Количество потоков в THREAD_QUANTITY (collector.py)

    # Количество статей
    articleList = collector.getArticles(100)

    print('collectArticles ----   %s  ----',
          str(datetime.timedelta(seconds=(time.time() - start_time))))
    start_time2 = time.time()

    # Создать файлы xml в папке 'files'
    for article in articleList:
        xmlGenerator.generateXml(article)

    print('generateXml ----   %s  ----',
          str(datetime.timedelta(seconds=(time.time() - start_time2))))

    print('xml: ', len(os.listdir('files')))
