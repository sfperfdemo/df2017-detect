# df2017-detect

## Anomaly Detection for Performance Data Using Einstein Analytics
Dreamforce 2017 Demo Scripts

## Prerequisites

Salesforce.com Analytics Cloud DatasetUtils

* [DatasetUtils](https://github.com/forcedotcom/Analytics-Cloud-Dataset-Utils)

Download and install Java JDK from Oracle

* [Oracle JDK](http://www.oracle.com/technetwork/java/javase/downloads/index.html)

After the installation is complete, open a console and check that Java version is 1.8 or higher by running the following command:

``java -version``

Download and install Python Programming Language

* [Python Software Foundation](https://www.python.org)

Download and install scikit-learn

* [Machine Learning in Python](http://scikit-learn.org)

## Files
* detect.sh - The main script to run all steps
* data/* - Training and test input data
* scripts/* - Python scripts to build model and get predictions
* results/ - Directory for result files
* analytics/ - Directory with Analytics Cloud load scripts
* chatter/ - Directory with sample scripts to send alerts to Salesforce Chatter
