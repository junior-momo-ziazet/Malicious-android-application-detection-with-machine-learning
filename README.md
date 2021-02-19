# Malicious Android Application Detection with Machine Learning

## Abstract
In the past decade, Android rose up to be the most used Mobile Operating System with an [87% market share](https://www.idc.com/promo/smartphone-market-share/os#:~:text=Android%3A%20Android's%20smartphone%20share%20will,response%20despite%20the%20pandemic%20hurdles). Compared to its main competitor iOS, Android is a lax system that allows downloads from a wide variety of sources. The openness of Android allows the user to install software from unsupervised third-party stores, and it causes the system to be vulnerable to the injection of malicious software that could cause security breach as well as data privacy endangerment. This project aims at analysing the APK (Android Application Package Kit) files of Android applications in order to extract important signatures for the detection of malicious applications. Feature extraction techniques will be applied on the APK file and once the best attributes are determined, we will use them to develop a malware scanner. This work uses the [Drebin](https://www.sec.cs.tu-bs.de/~danarp/drebin/) dataset containing 5560 APKs of malicious applications combined with [AndroZoo](https://androzoo.uni.lu/) dataset also containing 6000 APKs of benign applications.

## Introduction
At its I/O 2019 Developer Conference in Mountain View, Google revealed that Android now powers [2.5 billion active devices](https://venturebeat.com/2019/05/07/android-passes-2-5-billion-monthly-active-devices/). One of the reasons for this growth of Google-developed Android is it's free and open-source platform, which allows mobile phone manufacturers to use and adapt the operating system for their own devices. Being an open Operating System, Android is vulnerable to malicious software.
 
It is easy for those malwares to make their way through a phone’s system, and the damage it could potentially cause is significant. Malwares can spy on data (Spywares), block the phone’s access for a ransom (Ransomwares), harm or corrupt the system and even spread through connected devices (Worms).  In 2016, according to the [G Data H1/2016 report](https://file.gdatasoftware.com/web/en/documents/whitepaper/G_DATA_Mobile_Malware_Report_H1_2016_EN.pdf), 1,723,265 new malicious application examples were identified. Yet again, the amount of new malicious software is increasing, as well as the complexity of the current malwares such as new variants introduced to prevent their detection. Indeed, Malicious systems can penetrate the system through multiple techniques, such as downloading software in the background without the user’s consent (known as Drive by Download), encrypting malwares so that they can’t be recognized by the anti-virus (Dynamic Payloads) and exploiting the limited resources of the device hardware to bypass the security system (Stealth Malwares). Therefore, there is an urgent need to analyze these applications regarding malicious software to detect whether an application is benign or malicious.
 
In this study, we aim to prevent these malicious applications from being installed by developing a Machine Learning based detection system  that would  predict if a piece of software contains malwares . We want to first investigate how to extract useful features from APK data files, then represent these features as images, text, etc. and finally use them to build a malicious application detector.
 
From what we were able to find, several Machine Learning approaches have been proposed to detect malicious Android applications, and they fall into two general categories with respect to feature extraction, static and dynamic analysis.
The static analysis methods [1, 2, 3], analyze the features found in the .apk file such as permissions, APIs from an application’s code or metadata without executing the program (thus before being installed on the device). In [4, 5], Naive Bayes and random forest models are applied with APIs and metadata.  In [6], authors converted malware into gray images and used KNN to classify different malware families. 
On the contrary, dynamic analysis methods are based on the behavior of Android applications (thus executing the application and collecting behavioral events at runtime then transforming them into features). Such a method was used by [7, 8], where platform APIs, system calls, file and network access information were used as input features and Naive bayes was used to make the classification.

## Materials and Methods

The system will use the static analysis method for the analysis of Android applications. 
The data set created in the [Drebin](https://www.sec.cs.tu-bs.de/~danarp/drebin/) study was used for collecting the malicious applications, which has been shared as an open resource. This dataset contains 5560 applications from 179 different malware families. These samples were collected in February 2021 [9, 10]. To create a benign applications data set, we collected 6000 APKs from [AndroZoo](http://doi.acm.org/10.1145/2901739.2903508). As stated in the AndroZoo web page, these APKs were collected from several sources, including the official Google Play app market and then analysed by tens of different AntiVirus to fool proof the absence of malware in these applications.
Each unit of data is a compressed APK file containing different components and the most essential components are the AndroidManifest.xml, classes.dex, and resources.arsc files.  AndroidManifest.xml is an encoded XML file containing information about attributes and permissions of the app, and resources.arsc is an encoded file containing resource information about the app. Finally classes.dex, known as the Dex file, contains the compiled code that is used to run the app. In general, malicious code exists in an executable module found in classes.dex, it can also be detected through suspicious permissions stored in the AndroidManisfest.xml file. Therefore, we will focus on these two components, AndroidManifest.xml and classes.dex for our analysis.

We will use libraries such as apkutils, nltk, hashlib, xmltodict, binascii, to preprocess and clean the data and scikit learn to build the model.
We aim to do the parallel preprocessing and the training following these steps: 
1. Unpack the APK file using the unzip utility
2. Extract the AndroidManifest.xml and  classes.dex from all the APK using the [Apktool](https://ibotpeaches.github.io/Apktool) .
3. Use the Manifest file to map the permissions as features and attribute a value of 1 if the permission is used and 0 otherwise.
4. Sparse the class data from classes.dex file and extract the opcode sequence, then use n-gram technique to encode the opcode sequence to n-bit SimHash in order to get features with n number of elements per features.
5. Preprocess the extracted features in the steps above and apply dimension reduction with methods such as PCA, SVD, or t-SNE. 
6. Implement supervised classification techniques such as Logistic Regression, Random Forest, KNN or Multi Layer Perceptron, Decision Trees, Naive Bayes, and SVM.
7. Analyse, interpret and discuss the results, the limitations, and the scalability.

### References

[1] Peiravian N, Zhu X (2013) Machine learning for android malware detection using permission and API calls. Int Conf Tools Artif Intell:300–305

[2] Suarez-Tangil G, Kumar Dash S, Ahmadi M, Kinder J, Giacinto G, Cavallaro L (2017) DroidSieve: fast and accurate classification of obfuscated android malware. In: Proceedings of the seventh ACM on conference on data and application security and privacy. ACM, New York, pp 309–320

[3] . Aafer Y, Du W, Yin H (2013) Droidapiminer: mining api-level features for robust malware detection in android. In: International conference on security and privacy in communication systems, pp 86–103

[4] Ahmed F, Hameed H, Shafiq MZ, Farooq M (2009) Using spatio-temporal information in API calls with machine learning algorithms for malware detection. In: Proceedings of the 2nd ACM workshop on security and artificial intelligence. ACM, New York, pp 55–62 

[5] Tian R, Islam R, Batten L, Versteeg S (2010) Differentiating malware from cleanware using behavioural analysis. In: International conference on malicious and unwanted software

[6] L. Nataraj, S. Karthikeyan, G. Jacob, and B. S. Manjunath. 2011. Malware images : visualization and automatic classification. In Proceedings of the 8th international symposium on visualization for cyber security, Pittsburgh, Pennsylvania USA,July 2011 (VizSec 2011).DOI : http ://dx.doi.org/10.1145/2016904.2016908

[7] . Kumar Dash S, Suarez-Tangil G, Khan S (2016) DroidScribe: classifying android malware based on runtime behavior. In: IEEE security and privacy workshops. Conference Publishing Services, IEEE Computer Society, Los Alamitos, pp 252–261 

[8]. Chaba S, Kumar R, Pant R, Dave M, Malware detection approach for android systems using system call logs. arXiv preprint, arXiv:1709.08805

[9] Arp, D.; Spreitzenbarth, M.; Hubner, M.; Gascon, H.; Rieck, K. DREBIN: Effective and Explainable Detection of Android Malware in Your Pocket. In Proceedings of the Network and Distributed System Security Symposium (NDSS), San Diego, CA, USA, 23–26 February 2014

[10] Michael Spreitzenbarth, Florian Echtler, Thomas Schreck, Felix C. Freling, Johannes Hoffmann, "MobileSandbox: Looking Deeper into Android Applications", 28th International ACM Symposium on Applied Computing (SAC), March 2013
