# -*- coding: utf-8 -*-

import xmltodict
import xml.etree.ElementTree as ET
import pandas as pd
from apkutils import apkfile
from apkutils.axml.axmlparser import AXML
from apkutils.dex.dexparser import DexFile

import os


#%%

def extract_file_from_APK(path, file_type ='manifest'):
    '''This function extract the file of interest takes as 
    Input: 
        the path : String, path where the zipfiles are
        the type : String in ['manifest','dex']
    Output:
        return a list containing those files
    '''
    
    extracted_files = []
    

    for _, _, f in os.walk(path):
        for file in f:
            #print(file)
            apk_path=path+file
            with apkfile.ZipFile(apk_path, 'r') as unzip_file:
                    for  name in unzip_file.namelist():
                        if file_type =='manifest' and name.startswith('AndroidManifest') and name.endswith('.xml'):
                            data = unzip_file.read(name)
                            axml = AXML(data).get_xml()
                            dat = xmltodict.parse(axml, False)['manifest']
                            #d = ET.parse(apk_path+'/'+name)
                            extracted_files.append(dat)
                            print(name)
                        elif file_type =='dex' and name.startswith('classes') and name.endswith('.dex'):
                            data = unzip_file.read(name)
                            dat = DexFile(data)
                            extracted_files.append(dat)
                            print(name)
                        else:
                            pass
                    
            
                       
    return extracted_files

path = 'data_downloaded/Benign_APK/'  
test = extract_file_from_APK(path, file_type ='manifest')
#%%
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


    return  permissions

        
def xmlToCSV(data, permission_dict):
    '''
    
    This function transform our xml file to a csv file with features
    Input:
        data : List, list of xml files to be transform as features
        permission_dict : dictionary,containing all the the permissions with values 0
    Output: 
        return a DataFrame containng permissions with values 0 or 1
        
    '''
    
    features = pd.DataFrame(columns=sorted(list(permission_dict.keys())))

    for idx,file in enumerate(data):
    #tree = ET.parse(filename)
        tree = []
        copy_permission_dict = permission_dict.copy()
       
        if 'permission' in list(file.keys()):
            if isinstance(file['permission'], dict):
                p = file['permission']['@android:name'].rpartition('.')[-1]
                tree.append(p) if p not in tree else tree
            elif isinstance(file['permission'], list):
                [tree.append(f['@android:name'].rpartition('.')[-1]) for f in file['permission'] if f['@android:name'].rpartition('.')[-1] not in tree]
            else:
                pass
        if 'uses-permission' in list(file.keys()):
            if isinstance(file['uses-permission'], dict):
                p = file['uses-permission']['@android:name'].rpartition('.')[-1]
                tree.append(p) if p not in tree else tree
            elif isinstance(file['uses-permission'], list):
                [tree.append(f['@android:name'].rpartition('.')[-1]) for f in file['uses-permission'] if f['@android:name'].rpartition('.')[-1] not in tree]
            else:
                pass


        for name,_ in copy_permission_dict.items():
            if name in tree:
                copy_permission_dict[name]=1 

        df = pd.DataFrame(copy_permission_dict,index=[idx])
    
        features = pd.concat([features, df])                    
    
    return features
    
def generate_manifest_features(path, all_permission_file, apk_type):
    
    APK_type = {'benign':'/Benign_APK/',
            'malicious': '/Malicious_APK/'}
            
    path = path+APK_type[apk_type]

    extract_file = extract_file_from_APK(path,'manifest')
    permission_dict = get_list_permission(all_permission_file)
    features = xmlToCSV(extract_file, permission_dict)
    
    return features
    #features.to_csv(apk_type+'_Export_dataframe.csv', index=False, header=True)
    
#def main(path, filename, apk_type):
    

path = 'data_downloaded'  
filename_path = 'all_permissions.txt'
dataset=[]
for apk_type in ['benign','malicious']:
    features = generate_manifest_features(path, filename_path, apk_type )
    features.to_csv(apk_type+'_dataframe.csv', index=False, header=True)
    dataset.append(features)
              
