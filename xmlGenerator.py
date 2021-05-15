import xml.etree.ElementTree as et
import service
import Article


def generateXml(article: Article):
    root = et.Element('doc')

    sourceElem = et.SubElement(root, 'source')
    sourceElem.text = article.source
    sourceElem.attrib['verify'] = "true"
    sourceElem.attrib['type'] = "str"
    sourceElem.attrib['auto'] = "true"

    # categoryElem = et.SubElement(root, 'category')

    authorElem = et.SubElement(root, 'author')
    authorElem.text = article.author
    authorElem.attrib['verify'] = "true"
    authorElem.attrib['type'] = "str"
    authorElem.attrib['auto'] = "true"

    titleElem = et.SubElement(root, 'title')
    titleElem.text = article.title
    titleElem.attrib['verify'] = "true"
    titleElem.attrib['type'] = "str"
    titleElem.attrib['auto'] = "true"

    dateElem = et.SubElement(root, 'date')
    dateElem.text = service.convertDate(article.date)
    dateElem.attrib['verify'] = "true"
    dateElem.attrib['type'] = "date"
    dateElem.attrib['auto'] = "true"

    tagsElem = et.SubElement(root, 'tags')
    tagsElem.text = article.tags
    tagsElem.attrib['verify'] = "true"
    tagsElem.attrib['type'] = "str"
    tagsElem.attrib['auto'] = "true"

    textElem = et.SubElement(root, 'text')
    textElem.text = f"![CDATA[{article.text}]]"
    textElem.attrib['verify'] = "true"
    textElem.attrib['type'] = "str"
    textElem.attrib['auto'] = "true"

    tree = et.ElementTree(root)

    with open(f'files/{service.titleToFileName(article.title)}.xml', "wb") as files:
        tree.write(files, encoding='UTF-8', xml_declaration=True)
