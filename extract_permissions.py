import xml.etree.ElementTree as ET
import pandas as pd
import csv

permissions_labels = []

with open("./all_permissions.txt") as f:
    for l in f:
        length = len(l)
        permissions_labels.append(l[19:length-1])

permissions_label = sorted(permissions_labels)

data = pd.DataFrame(columns=permissions_labels)


def xmlToCSV(data, filename):
    permissions = {}
    for permission_label in permissions_labels:
        permissions[permission_label] = 0
    tree = ET.parse(filename)
    for elem in tree.iter():
        if elem.tag == "permission" or elem.tag == "uses-permission":
            permissions[elem.attrib["{http://schemas.android.com/apk/res/android}name"][19:]] = 1

    df = pd.DataFrame(permissions, index=[0]).sort_index(axis=1)
    return pd.concat([data, df])


files = ["./test.xml", "./test.xml"]

for filename in files:
    data = xmlToCSV(data, filename)

data.to_csv('Export_dataframe.csv', index=False, header=True)
