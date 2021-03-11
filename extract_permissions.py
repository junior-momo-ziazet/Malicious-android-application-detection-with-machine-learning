import xml.etree.ElementTree as ET
import pandas as pd
import csv
import os
import zipfile

# CODE TO UNZIP THE APK AND RETURN FILE

permissions_labels = []

with open("./all_permissions.txt") as f:
    for l in f:
        length = len(l)
        permissions_labels.append(l[19:length-1])

permissions_label = sorted(permissions_labels)

data = pd.DataFrame(columns=permissions_labels)


def xmlToCSV(filename):
    permissions = {}
    for permission_label in permissions_labels:
        permissions[permission_label] = 0
    tree = ET.parse(filename)
    for elem in tree.iter():
        if elem.tag == "permission" or elem.tag == "uses-permission":
            permissions[elem.attrib["{http://schemas.android.com/apk/res/android}name"][19:]] = 1

    df = pd.DataFrame(permissions, index=[0]).sort_index(axis=1)
    return pd.concat([data, df])


base_path = os.path.expanduser("~/Desktop/benign_apk")

for filename in os.listdir(base_path):
    abs_path = base_path + "/" + filename
    if filename[-4:] == ".zip":
        with zipfile.ZipFile(abs_path, 'r') as unzipped_file:
            file_path = base_path + "/" + filename[:-4]
            unzipped_file.extractall(file_path)
            os.remove(abs_path)
            # data = xmlToCSV(file_path + "/AndroidManifest.xml")

data.to_csv('Export_dataframe.csv', index=False, header=True)
