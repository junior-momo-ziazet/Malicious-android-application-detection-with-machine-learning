import xml.etree.ElementTree as ET
tree = ET.parse("./test.xml")

permissions = {}

with open("./all_permissions.txt") as f:
    for l in f:
        length = len(l)
        permissions[l[19:length-1]] = 0

for elem in tree.iter():
    if elem.tag == "permission" or elem.tag == "uses-permission":
        print(elem)
