# Malicious Android Application Detection with Machine Learning

# Abstract

In the past decade, Android rose up to be the most used Mobile Operating System with an  [87% market share](https://www.idc.com/promo/smartphone-market-share/os#:~:text=Android%3A%20Android's%20smartphone%20share%20will,response%20despite%20the%20pandemic%20hurdles). Compared to its main competitor iOS, Android is a lax system that allows downloads from a wide variety of sources. The openness of Android causes the system to be vulnerable to the injection of Malicious Software that could cause security breach as well as data privacy endangerment. In this report, we will discuss how we used 6000 Benign APKs from the [AndroZoo dataset](https://androzoo.uni.lu/) and 5560 Malicious APKs from the [Drebin dataset](https://www.sec.cs.tu-bs.de/~danarp/drebin/) to conduct a Dataset Analysis in order to create a Prediction System that determines whether an Application is Malicious or not. We go over the different steps of our solution such as Data Extraction, which consists of converting the APK to a set of features, different Machine Learning Models Training, Observations, and Results Analysis. The report also talks about the potential improvements, the limitations, and the scalability of the project, as well as its relevance in the Malware Detection Field.

# Introduction

At its I/O 2019 Developer Conference in Mountain View, Google revealed that Android now powers [2.5 billion active devices](https://venturebeat.com/2019/05/07/android-passes-2-5-billion-monthly-active-devices/). One of the reasons for this growth of Google-developed Android is it's free and open-source platform, which allows mobile phone manufacturers to use and adapt the operating system for their own devices. Being an open Operating System, Android is vulnerable to malicious software.

It is easy for those malwares to make their way through a phone’s system, and the damage it could potentially cause is significant. Malwares can spy on data (Spywares), block the phone’s access for a ransom (Ransomwares), harm or corrupt the system and even spread through connected devices (Worms). In 2016, according to the [G Data H1/2016 report](https://file.gdatasoftware.com/web/en/documents/whitepaper/G_DATA_Mobile_Malware_Report_H1_2016_EN.pdf), 1,723,265 new malicious application examples were identified. Yet again, the amount of new malicious software is increasing, as well as the complexity of the current malwares such as new variants introduced to prevent their detection. Indeed, Malicious systems can penetrate the system through multiple techniques, such as downloading software in the background without the user’s consent (known as Drive by Download), encrypting malwares so that they can’t be recognized by the anti-virus (Dynamic Payloads) and exploiting the limited resources of the device hardware to bypass the security system (Stealth Malwares). Therefore, there is an urgent need to analyze these applications regarding Malicious Software to detect whether an application is Benign or Malicious.

In this study, we aim to prevent these malicious applications from being installed by developing a Machine Learning based detection system that would predict if a piece of software contains Malwares . We want to first investigate how to extract useful features from APK data files, preprocess these features to numerical values, and use them to build a Malicious Application Detector.

From what we were able to find, several Machine Learning approaches have been proposed to detect malicious Android applications, and they fall into two general categories with respect to feature extraction, Static and Dynamic Analysis. The static analysis methods [1, 2, 3], analyzes the features found in the .apk file such as permissions, APIs from an application’s code or Metadata without executing the program (thus before being installed on the device). In [4, 5], Naive Bayes and Random Forest models are applied with APIs and metadata. In [6], authors converted malware into gray images and used KNN to classify different Malware Families. On the contrary, Dynamic Analysis methods are based on the behavior of Android applications (thus executing the application and collecting behavioral events at runtime then transforming them into features). Such a method was used by [7, 8], where platform APIs, system calls, file and network access information were used as input features and Naive bayes was used to make the classification.

The report will be structured in three parts: [Section 2 - Material and Methods](#materials-and-methods) where we describe the tools and techniques used to solve the problem, [Section 3 - Results](#results), where we present the results obtained, and [Section 4 - Discussion](#discussion), where we discuss the relevance of our solution, point the limitations, and discuss possible future work.

# Materials and Methods
The Material and Methods section consists on explaining the different steps of our process to build the Malware Application Detector, such as Data Collection, Data Extraction, Data Preprocessing, and Model Training.

## Data Collection

The proposed approach will use the Static Analysis method of Android Applications. The Dataset created by the Drebin study was used for collecting the Malicious Applications, which has been shared as open source [9, 10]. This Dataset contains 5560 Applications from 179 different Malware Families. We collected 6000 Malware-free foolproof APKs from AndroZoo, in order to create a Benign Applications Dataset. Both Datasets were collected in February 2021.

## Data Extraction

The instances from the dataset were in APK folder format. We had to extract the information we needed from the APK and convert it into data the model understands.
In general, malicious code exists in an executable module found in classes.dex, it can also be detected through suspicious permissions stored in the AndroidManisfest.xml file.
Therefore, AndroidManifest.xml, indicating the permissions the App is using, and classes.dex, containing information on the code of the app such as classes and methods, were the files of interest in the APK folder. [Figure 1]

### Manifest File
As shown in [Figure 2], we extracted data from the AndroidManifest.xml by mapping the permissions as features and attribute a value of 1 if the permission is used and 0 otherwise.

### Dex File
In order to extract valuable information from the DexFile, we had to refer to the data section where the code is contained. We then converted the different instructions into opcode sequences, and mapped them to a 32x32-bit SimHash Matrix. We then took the singular values of the Singular Value Decomposition of this Matrix and added them as features. [Figure 3]

We labeled Malicious instances as 1 and Benign instances as 0 for Supervised Classification purposes.

## Data Preprocessing
Once we gathered the different features, we needed to preprocess the data, for training optimization purposes. We used different preprocessing techniques to process rows (instances), columns (features), and values:

### Row Preprocessing
We had to filter the rows that were failing upon either Android Manifest or DexFile extraction as we couldn’t merge all the columns of these instances. We also removed the APKs that had multiple DexFile, which caused multiple rows for the same instance.

### Column Preprocessing
We had over 250 permissions in total, and a consequential part was never used by any of the applications, as we can see on [Figure 5], the red lines indicate the permissions that weren’t being used. We decided to remove them in order to reduce the number of features.

### Value Preprocessing
We used Scikit-Learn’s Standardscaler to process the values of our features, as the difference between Manifest features and DexFile features was considerable.

After Preprocessing, we managed to reduce our feature count from 356 to 184, and our rows from 11,560 to 10,778 (5230 Benign, 5548 Malicious). [Figure 5]

## Model Training
We approached model training by experimenting on various models, and different data structures.

### Dataset
We applied the different models on 3 separate datasets:
* Manifest features
* DexFile features
* Manifest-DexFile features Merge
We split the dataset into Training (80%) and Testing (20%) sets in order to test the model and compare results.

### Models
We selected seven models to train our data:
* Decision Tree Classifier
* Random Forest Classifier
* Multi Layer Perceptron (MLP)
* K Nearest Neighbors (KNN)
* Support Vector Machine (SVM)
* Gaussian Naïve Bayes
* Ensemble Methods on the Best Models

### Training
We used Scikit-Learn’s Randomized Search to perform 10-Fold Cross Validation and hyperparameter tuning on our models.

### Metrics
We compared our models based on the F1-score each model got after test set predictions.


# Results

## Dataset Comparison
After running the different models on our three datasets, we plotted the results of each model in order to compare their F1 scores.
We realized that the most performant Dataset was the Merged Dataset, ranging from an F1 score of 88.8% to 92.3%, compared to the other datasets (56.9% to 85.6% for DexFile and 80.7% to 86.8% for Manifest).

## Best Model
Upon dataset selection, we observed that the most performant model is SVC. We got an F1 score of 92.4% and an accuracy of 92.6% [Figure 9]. We also plotted the Confusion Matrix to compare the true and false predictions. [Figure 10].

## Optimization
In order to improve the performance of our models, we decided to combine multiple models using the Bagging Method from the Merged Dataset, as most of them were performant but different in the way they are designed.
The goal behind the Bagging Method is to improve the generalizability and the robustness of a particular model.
We merged the predictions of SVC, MLP, KNN, Decision Tree Classifier, and Random Forest Classifier. We then made the models vote to compute a final prediction.

## Final Results
We improved the F1 Score by 1.7%, and the Accuracy by 1.5% using the Bagging Model as shown in [Figure 11].

# Discussion

## Relevance
In this research work, we studied Android malware and used machine learning methods for its detection.
We have shown how the combination of features from certain files, namely Manifest and Classes.dex files, can be realized to represent significant features for the Machine Learning model and enhance detection performance.
We believe that the data extraction techniques proposed in our work, could lead to improvements in the field of Smartphone Malware Detection such as Android.
Our work provides reasonable evidence that good Feature Extraction and Model selection can have a great impact on increasing Malware threats. We firmly believe that our work will lead the scientific community to focus on feature extraction so that detection platforms become more adaptive, more accurate, and more secure.

## Limitations
Even though our solution got 94% in both F1-Score and Accuracy, it has some limitations regarding many aspects such as the data used, the features selected, and real world application. Some limitations are:
* The Model may not detect new Malwares (also known as Zero-Day Attacks). As the Malwares may modify the features (Permissions and DexFile features) into a new pattern the model implemented doesn’t recognize.
* As presented in the Introduction, there are two types of Analysis when it comes to Android Malware, Static and Dynamic Analyses. The solution proposed only analyzes the Static Features, without taking the behavior of the Application into consideration (Dynamic Malware Analysis).
* We only considered Android.manifest and classes.dex during feature extraction, but the APK has more resources such as API calls, Intent, APK signatures etc. Which we could’ve added to our set of features.

## Scalability
As of the scalability of our solution, we realized that we could improve on the Data Volume aspect due to two factors:
* The Dataset used represents less than 0.002% of the Android Applications on both the Playstore and Third Party markets.
* New Applications are constantly being released and the Automatic Extraction of the APK we’ve implemented makes the data extraction universal to any new application that is published.
 
# Conclusion
This work implemented a static detection method based on Machine Learning providing advantages in the comprehensiveness, accuracy, and expertless dependence of detection. We combined features from both AndroidManifest.xml and classes.dex files, then implemented Machine Learning models. The Bagging model outperformed the other proposed models with an accuracy of 94% and a F1-score of 94%. Although our work also has some limitations, it could be expanded via dynamic malware analysis as well as additional feature extraction in future implementation. It has also shown that malwares can be perceived by examining different aspects of permissions and opcodes.

# References

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
