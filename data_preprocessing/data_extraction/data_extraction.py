import xmltodict
import pandas as pd
from apkutils import apkfile
from apkutils.axml.axmlparser import AXML
from apkutils.dex.dexparser import DexFile
import os
import numpy as np
import hashlib as h
from nltk.util import ngrams
from numpy.linalg import svd


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


def generate_xml_features(xml_data, xml_filename, permission_dict):
    '''

    This function transform a xml file to a csv file with features
    Input:
        data : xml, xml file to be transform as features
        permission_dict : dictionary,containing all the the permissions with values 0
    Output:
        return a DataFrame containng permissions with values 0 or 1

    '''

    tree = []
    copy_permission_dict = permission_dict.copy()

    if 'permission' in list(xml_data.keys()):
        if isinstance(xml_data['permission'], dict):
            try:
                p = xml_data['permission']['@android:name'].rpartition('.')[-1]
                tree.append(p) if p not in tree else tree
            except Exception as e:
                print('1', e)
        elif isinstance(xml_data['permission'], list):
            try:
                [tree.append(f['@android:name'].rpartition('.')[-1])
                 for f in xml_data['permission'] if f['@android:name'].rpartition('.')[-1] not in tree]
            except Exception as e:
                print('2', e)

        else:
            pass
    if 'uses-permission' in list(xml_data.keys()):
        if isinstance(xml_data['uses-permission'], dict):
            try:
                p = xml_data['uses-permission']['@android:name'].rpartition(
                    '.')[-1]
                tree.append(p) if p not in tree else tree
            except Exception as e:
                print('3', e)
        elif isinstance(xml_data['uses-permission'], list):
            try:
                [tree.append(f['@android:name'].rpartition('.')[-1])
                 for f in xml_data['uses-permission'] if f['@android:name'].rpartition('.')[-1] not in tree]
            except Exception as e:
                print('4', e)
        else:
            pass

    for name, _ in copy_permission_dict.items():
        if name in tree:
            copy_permission_dict[name] = 1

    row_df = pd.DataFrame([copy_permission_dict])
    row_df["id"] = xml_filename

    return row_df


def generate_dex_features(dex_data, dex_filename):
    '''

    This function transform a DEX file to a csv file with features
    Input:
        data : dex, .DEX file to be transform as features
        permission_dict : dictionary,containing all the the permissions with values 0
    Output:
        return a DataFrame containng features after a SVD Singular Value Decomposition

    '''

    width_height = [(32, 32)]
    try:
        opcode_list = _dex_files(dex_data)
        for w_h in width_height:
            hash_list = make_hash(
                opcode_list, bits=w_h[1]*w_h[0], gram=None)

            for index, each in enumerate(hash_list):
                if each > 0:
                    hash_list[index] = 255.
                else:
                    hash_list[index] = 0.

            image = np.asarray(
                hash_list, dtype=np.uint8).reshape(w_h[1], w_h[0])
            U, S, V = svd(image, full_matrices=True)
            row_df = pd.DataFrame(
                [[item for sublist in [[dex_filename], S] for item in sublist]])

    except Exception as e:
        print("An error occured " + str(e))

    return row_df


def _dex_files(dex_file):
    '''

    This function transform a DEX file to a serie of opcodes
    Input:
        dex_file : dex, DEX file to be used to generate opcodes 

    Output:
        return a list of opcodes 

    '''
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

            opcodes_l.append(opcodes)
    return opcodes_l


def make_hash(opcode_list, bits, gram):
    '''

    This function generate the hash given opcodes 
    Input:
        opcode_list : list, list of opcodes 
        bits: number of bits of the hash 
        gram: number of gram using N-gram if gram is not None

    Output:
        return hash representation

    '''

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


def extract_feature_from_APK(path, permission_dict, file_type='manifest'):
    '''This function extract features of interest takes as 
    Input: 
        the path : String, path where the zipfiles are
        permission_dict : Dictionary; containing all the permissions
        the type : String in ['manifest','dex']
    Output:
        return a dataframe containing the requested features
    '''
    if file_type == 'manifest':

        df = pd.DataFrame(columns=sorted(
            list(permission_dict.keys())).insert(0, "id"))
    else:
        df = pd.DataFrame()

    i = 0

    for _, _, f in os.walk(path):
        for file in f:
            i = i + 1
            if i == 8:
                break

            apk_path = path+file
            try:
                with apkfile.ZipFile(apk_path, 'r') as unzip_file:
                    for name in unzip_file.namelist():
                        if file_type == 'manifest' and name.startswith('AndroidManifest') and name.endswith('.xml'):
                            try:
                                data = unzip_file.read(name)
                                axml = AXML(data).get_xml()
                                dat = xmltodict.parse(axml, False)['manifest']
                                print(name + " " + str(i))
                                features = generate_xml_features(
                                    dat, file, permission_dict)
                                print(features)
                                df = pd.concat([df, features])
                                print(name + " " + str(i))
                            except Exception as e:
                                print("manifest error", e)

                        elif file_type == 'dex' and name.startswith('classes') and name.endswith('.dex'):
                            try:
                                data = unzip_file.read(name)
                                dat = DexFile(data)
                                print(name + " " + str(i))
                                features = generate_dex_features(dat, file)

                                df = pd.concat(
                                    [df, features], ignore_index=True)

                                print(name + " " + str(i))
                            except Exception as e:
                                print("dex error", e)
                        else:
                            pass
            except Exception as e:
                print("ERROR:")
                print(e)
                pass

    return df


def main(apk_type='benign', f_type='dex'):
    '''
    This function save  the csv of featuresgiven the type of apk and file
    Input:
        apk_type: String in ['benign','malicious']
        f_type : String in ['manifest','dex']
    '''

    path = '../../data/'
    all_permission_file = './all_permissions.txt'

    APK_type = {'benign': '/Benign_APK/',
                'malicious': '/Malicious_APK/'}

    permission_dict = get_list_permission(all_permission_file)

    path = path + APK_type[apk_type]

    feature = extract_feature_from_APK(path, permission_dict, file_type=f_type)

    feature.to_csv(apk_type+"_"+f_type+"_dataset.csv")


main(apk_type='benign', f_type='dex')
main(apk_type='benign', f_type='manifest')
main(apk_type='malicious', f_type='dex')
main(apk_type='malicious', f_type='manifest')
