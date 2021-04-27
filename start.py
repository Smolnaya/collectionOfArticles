import collector
import xmlGenerator

if __name__ == "__main__":
    articleList = collector.collectArticles(1000)
    for article in articleList:
        xmlGenerator.generateXml(article)
