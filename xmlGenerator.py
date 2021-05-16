import xml.etree.ElementTree as et
from xml.dom import minidom

from service import *


def addAttrib(elem, attribList):
    lst = ['verify', 'type', 'auto']
    for i in range(len(lst)):
        elem.attrib[lst[i]] = attribList[i]
    return elem


def createElem(root, namesList, dataLst):
    for i in range(len(namesList)):
        elem = et.SubElement(root, namesList[i])
        if isinstance(dataLst[i], list):
            elem = addAttrib(elem, ['true', 'list', 'true'])
            for tagData in dataLst[i]:
                tag = et.SubElement(elem, 'tag')
                tag.text = tagData
        else:
            if namesList[i] == 'text':
                elem = addAttrib(elem, ['true', 'cdata', 'true'])
                elem.text = f"![CDATA[{[dataLst[i]]}]]"
            elif namesList[i] == 'date':
                elem = addAttrib(elem, ['true', 'date', 'true'])
                elem.text = convertDate(dataLst[i])
            else:
                elem = addAttrib(elem, ['true', 'text', 'true'])
                elem.text = dataLst[i]
    return root


def generateXml(article: list):
    root = et.Element('doc')

    namesList = ['title', 'date', 'author', 'text', 'tags', 'source', 'href']
    root = createElem(root, namesList, article)

    tree = minidom.parseString(et.tostring(root)).toprettyxml()

    with open(f'files/{titleToFileName(article[0])}.xml', "wb") as file:
        file.write(tree.encode('UTF-8'))
