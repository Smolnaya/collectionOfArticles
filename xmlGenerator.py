import xml.etree.ElementTree as et
import service
import Article


def generateXml(article: Article):
    root = et.Element('doc')

    sourceElem = et.SubElement(root, 'source')
    sourceElem.text = article.source

    # categoryElem = et.SubElement(root, 'category')

    authorElem = et.SubElement(root, 'author')
    authorElem.text = article.author

    titleElem = et.SubElement(root, 'title')
    titleElem.text = article.title

    dateElem = et.SubElement(root, 'date')
    dateElem.text = service.convertDate(article.date)

    tagsElem = et.SubElement(root, 'tags')
    tagsElem.text = article.tags

    textElem = et.SubElement(root, 'text')
    textElem.text = f"![CDATA[{article.text}]]"

    tree = et.ElementTree(root)

    with open(f'files/{service.titleToFileName(article.title)}.xml', "wb") as files:
        tree.write(files, encoding='UTF-8', xml_declaration=True)
