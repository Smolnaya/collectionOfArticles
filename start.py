import time
import collector
import datetime
import os

if __name__ == "__main__":
    start_time = time.time()

    # Количество потоков в THREAD_QUANTITY (collector.py)

    # Создать файлы xml в папке 'files'
    if not os.path.isdir('files'):
        os.mkdir('files')

    # Количество статей
    q = int(input('Article quantity: '))
    collector.getArticles(q)

    print('Collecting Articles: ', str(datetime.timedelta(seconds=(time.time() - start_time))))

    print('Xml: ', len(os.listdir('files')))
