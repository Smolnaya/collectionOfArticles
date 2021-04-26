import xml.etree.ElementTree as et
import service


def generateXml(title, date, author, text, tags, source):
    root = et.Element('doc')

    sourceElem = et.SubElement(root, 'source')
    sourceElem.text = source

    # categoryElem = et.SubElement(root, 'category')

    authorElem = et.SubElement(root, 'author')
    authorElem.text = author

    titleElem = et.SubElement(root, 'title')
    titleElem.text = title

    dateElem = et.SubElement(root, 'date')
    dateElem.text = service.convertDate(date)

    tagsElem = et.SubElement(root, 'tags')
    tagsElem.text = ','.join(tags)

    textElem = et.SubElement(root, 'text')
    textElem.text = f"![CDATA[{text}]]"

    tree = et.ElementTree(root)

    with open(f'files/{service.titleToFileName(title)}.xml', "wb") as files:
        tree.write(files, encoding='UTF-8', xml_declaration=True)
