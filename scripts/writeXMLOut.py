import xml.etree.ElementTree as ET
import lxml.etree as etree

filename = "/scratch/anamikas/hyp/v2/out.xml"

root = ET.Element("articles")
sub = ET.SubElement(root, 'article')
sub.set('id', '000001')
sub.set('prediction', 'True')
sub = ET.SubElement(root, 'article')
sub.set('id', '000002')
sub.set('prediction', 'False')
# ET.SubElement(root, 'article').set('prediction', 'True')

tree = ET.ElementTree(root)
#print(ET.tostring(root).decode())

# x = etree.parse(filename)
# print(etree.tostring(x, pretty_print=True))

with open(filename, "wb") as fh:
    tree.write(fh)
