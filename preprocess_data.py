# -*- coding: utf-8 -*-

import xmltodict
import xml.etree.ElementTree as ET
import pandas as pd
from apkutils import apkfile
from apkutils.axml.axmlparser import AXML
from apkutils.dex.dexparser import DexFile
from apkutils.axml.arscparser import ARSCParser
import binascii
import xml

import os
import re
import pickle
import numpy as np
import hashlib as h

from nltk.util import ngrams
# from ttictoc import tictoc
# from skimage import io
import skimage.io as io
import matplotlib.pyplot as plt
from numpy.linalg import svd
import numpy as np
import pandas as pd
from PIL import Image

# import logging
# logger = logging.getLogger(__name__)


# %%

def extract_file_from_APK(path, file_type='manifest'):
    '''This function extract the file of interest takes as 
    Input: 
        the path : String, path where the zipfiles are
        the type : String in ['manifest','dex']
    Output:
        return a list containing those files
    '''

    extracted_files = []

    i = 0

    for _, _, f in os.walk(path):
        for file in f:
            i = i + 1
            apk_path = path+file
            try:
                with apkfile.ZipFile(apk_path, 'r') as unzip_file:
                    for name in unzip_file.namelist():
                        if file_type == 'manifest' and name.startswith('AndroidManifest') and name.endswith('.xml'):
                            try:
                                data = unzip_file.read(name)
                                axml = AXML(data).get_xml()
                                dat = xmltodict.parse(axml, False)['manifest']
                                extracted_files.append(
                                    {"file_name": file, "m_file": dat})
                                print(name + " " + str(i))
                            except Exception as e:
                                print(e)
                        elif file_type == 'dex' and name.startswith('classes') and name.endswith('.dex'):
                            try:
                                data = unzip_file.read(name)
                                dat = DexFile(data)
                                extracted_files.append(
                                    {"file_name": file, "d_file": dat})
                                print(name + " " + str(i))
                            except Exception as e:
                                print(e)
                        else:
                            pass
            except Exception as e:
                print("ERROR:")
                print(e)
                pass

    return extracted_files


# path = 'data_downloaded/Malicious_APK/'
# test = extract_file_from_APK(path, file_type='manifest')
# %%


def get_list_permission(filename):
    '''
    This function get of all the possible permission we can have in an android app

    Input:
        filename: String, path of the file containng the permission

    Output:
        return a dictionary of key: permission, value:0
    '''
    permissions_labels = []

    with open(filename) as f:
        for l in f:
            length = len(l)
            permissions_labels.append(l[19:length-1])

    permissions_labels = sorted(permissions_labels)

    permissions = {}

    for permission_label in permissions_labels:
        permissions[permission_label] = 0

    return permissions


def xmlToCSV(data, permission_dict):
    '''

    This function transform our xml file to a csv file with features
    Input:
        data : List, list of xml files to be transform as features
        permission_dict : dictionary,containing all the the permissions with values 0
    Output:
        return a DataFrame containng permissions with values 0 or 1

    '''

    features = pd.DataFrame(columns=sorted(
        list(permission_dict.keys())).insert(0, "id"))

    for idx, ele in enumerate(data):
        m_file = ele["m_file"]
        file_name = ele["file_name"]
        tree = []
        copy_permission_dict = permission_dict.copy()

        if 'permission' in list(m_file.keys()):
            if isinstance(m_file['permission'], dict):
                p = m_file['permission']['@android:name'].rpartition('.')[-1]
                tree.append(p) if p not in tree else tree
            elif isinstance(m_file['permission'], list):
                [tree.append(f['@android:name'].rpartition('.')[-1])
                 for f in m_file['permission'] if f['@android:name'].rpartition('.')[-1] not in tree]
            else:
                pass
        if 'uses-permission' in list(m_file.keys()):
            if isinstance(m_file['uses-permission'], dict):
                p = m_file['uses-permission']['@android:name'].rpartition(
                    '.')[-1]
                tree.append(p) if p not in tree else tree
            elif isinstance(m_file['uses-permission'], list):
                [tree.append(f['@android:name'].rpartition('.')[-1])
                 for f in m_file['uses-permission'] if f['@android:name'].rpartition('.')[-1] not in tree]
            else:
                pass

        for name, _ in copy_permission_dict.items():
            if name in tree:
                copy_permission_dict[name] = 1

        df = pd.DataFrame(copy_permission_dict, index=[idx])
        df["id"] = file_name

        features = pd.concat([features, df])

    return features


@staticmethod
def get_proto_string(return_type, param_types):
    proto = return_type.decode()
    if len(proto) > 1:
        proto = 'L'
    for item in param_types:
        param_type = item.decode()
        proto += 'L' if len(param_type) > 1 else param_type
    return proto


def _dex_files(dex_file):
    opcodes_l = []
    for dexClass in dex_file.classes:
        try:
            dexClass.parseData()
        except IndexError:
            continue

        for method in dexClass.data.methods:
            opcodes = ""
            if method.code:
                for bc in method.code.bytecode:
                    opcode = str(hex(bc.opcode)).upper()[2:]
                    if len(opcode) == 2:
                        opcodes = opcodes + opcode
                    else:
                        opcodes = opcodes + "0" + opcode

#                    proto = get_proto_string(method.id.return_type, method.id.param_types)

#                    item = {}
#                    item['super_class'] = dexClass.super.decode()
#                    item['class_name'] = method.id.cname.decode()
#                    item['method_name'] = method.id.name.decode()
#                    item['method_desc'] = method.id.desc.decode()
#                    item['proto'] = proto
#                    item['opcodes'] = opcodes
            opcodes_l.append(opcodes)
    return opcodes_l


def make_hash(opcode_list, bits, gram):

    hash_v = np.zeros([bits])

    if gram == None:

        for opcode in opcode_list:
            binary = bin(int(h.sha512(opcode.encode()).hexdigest(), 16))[2:]
            binary = list(binary)
            temp = bits - len(binary)

            for i in range(temp):
                binary.insert(0, '0')

            binary = np.array(
                list(map(lambda x: -1 if x == '0'else 1, binary)))
            hash_v = hash_v + binary

    elif gram == 2:

        opcode_ngram_tuple = list(ngrams(opcode_list, n=gram))

        for word1, word2 in opcode_ngram_tuple:

            opcode = word1+word2

            binary = bin(int(h.sha512(opcode.encode()).hexdigest(), 16))[2:]
            binary = list(binary)
            # temp is for inserting '0' omitted automatically
            temp = bits - len(binary)

            for i in range(temp):
                binary.insert(0, '0')

            binary = np.array(
                list(map(lambda x: -1 if x == '0'else 1, binary)))
            hash_v = hash_v + binary

    elif gram == 3:
        opcode_ngram_tuple = list(ngrams(opcode_list, n=gram))

        for word1, word2, word3 in opcode_ngram_tuple:

            opcode = word1+word2+word3

            binary = bin(int(h.sha512(opcode.encode()).hexdigest(), 16))[2:]
            binary = list(binary)
            # temp is for inserting '0' omitted automatically
            temp = bits - len(binary)

            for i in range(temp):
                binary.insert(0, '0')

            binary = np.array(
                list(map(lambda x: -1 if x == '0'else 1, binary)))
            hash_v = hash_v + binary

    return hash_v


def generate_manifest_features(path, all_permission_file, apk_type):

    APK_type = {'benign': '/Benign_APK/',
                'malicious': '/Malicious_APK/'}

    path = path+APK_type[apk_type]

    extract_file = extract_file_from_APK(path, 'manifest')
    permission_dict = get_list_permission(all_permission_file)
    features = xmlToCSV(extract_file, permission_dict)

    return features
    #features.to_csv(apk_type+'_Export_dataframe.csv', index=False, header=True)

# def main(path, filename, apk_type):


path = 'data_downloaded'
filename_path = 'all_permissions.txt'
width_height = [(32, 32)]

images_paths = {(32, 32): "apk_images/32_32/",
                (64, 64): "apk_images/64_64/",
                (128, 128): "apk_images/128_128/"}
dataset = []


def generate_dex_features(path, apk_type):
    df = pd.DataFrame()
    APK_type = {'benign': '/Benign_APK/',
                'malicious': '/Malicious_APK/'}

    path = path + APK_type[apk_type]

    extract_file = extract_file_from_APK(path, "dex")
    # opcode_list = []
    j = 0
    for some_file in extract_file:
        filename = some_file["file_name"]
        d_file = some_file["d_file"]
        if (j % 10) == 0:
            print(str(round(((j / len(extract_file)) * 100), 2)) + "%")
        try:
            opcode_list = _dex_files(d_file)
            for w_h in width_height:
                hash_list = make_hash(
                    opcode_list, bits=w_h[1]*w_h[0], gram=None)

                for index, each in enumerate(hash_list):
                    if each > 0:
                        hash_list[index] = 255.
                    else:
                        hash_list[index] = 0.

                # image_path = "./"+path+images_paths[w_h]+str(j)+".png"

                image = np.asarray(
                    hash_list, dtype=np.uint8).reshape(w_h[1], w_h[0])
                # image = Image.open(img_path)
                # image = Image.convert("LA")
                # image = np.array(list(image.getdata(band=0)),
                #                  float).reshape(w_h[1], w_h[0])
                U, S, V = svd(image, full_matrices=True)
                row_df = pd.DataFrame(
                    [[item for sublist in [[filename], S] for item in sublist]])
                df = pd.concat([df, row_df], ignore_index=True)
                print("df no " + str(j) + " created")

        except Exception as e:
            print("An error occured " + str(e))
        j = j+1
    return df


final_df = pd.DataFrame()
for apk_type in ['malicious']:
    features = generate_manifest_features(path, filename_path, apk_type)
    final_df = pd.concat([final_df, features])
    # features.to_csv("drebin_manifest_analysis.csv")
    # dataset.append(features)
    # some_df = generate_dex_features(path, apk_type)
    # some_df.to_csv("drebin_dexfile_analysis_6.csv")

final_df.set_index("id").to_csv("drebin_manifest_analysis.csv")
# print(dataset)
# %%
