#######################################################
# Script:
#    testDev.py
# Usage:
#    python testDev.py <input_file> <output_file>
# Description:
#    Get the prediction based on training data model
#    Pass 1: prediction based on hours in a week
# Authors:
#    Jasmin Nakic, jnakic@salesforce.com
#    Samir Pilipovic, spilipovic@salesforce.com
#######################################################

import sys
import numpy as np
from sklearn import linear_model
from sklearn.externals import joblib

debugFlag = False
# Feature list
hourWeekCols = ["dateFrac", "isHoliday"]
for d in range(0,7):
    for h in range(0,24):
        hourWeekCols.append("H_" + str(d) + "_" + str(h))

def addColumns(dest, src, colNames):
    # Initialize temporary array
    tmpArr = np.empty(src.shape[0])
    cols = 0
    # Copy column content
    for name in colNames:
        if cols == 0: # first column
            tmpArr = np.copy(src[name])
            tmpArr = np.reshape(tmpArr,(-1,1))
        else:
            tmpCol = np.copy(src[name])
            tmpCol = np.reshape(tmpCol,(-1,1))
            tmpArr = np.append(tmpArr,tmpCol,1)
        cols = cols + 1
    return np.append(dest,tmpArr,1)
#end addColumns

def getPredictions(data,colList,modelName):
    # Initialize array
    X = np.zeros(data.shape[0])
    X = np.reshape(X,(-1,1))

    # Add columns
    X = addColumns(X,data,colList)

    if debugFlag:
        print("X 0: ", X[0:5])

    Y = np.copy(data["cnt"])
    if debugFlag:
        print("Y 0: ", Y[0:5])

    model = joblib.load(modelName)
    P = model.predict(X)
    print("SCORE values: ", model.score(X,Y))
    if debugFlag:
        print("P 0-5: ", P[0:5])

    return P
#end getPredictions

def writeResult(output,data,p):
    # generate result file
    result = np.array(
       np.empty(data.shape[0]),
       dtype=[
           ("timeStamp","|U19"),
           ("dateFrac",float),
           ("cnt",int),
           ("predDev",int)
        ]
    )

    result["timeStamp"]    = data["timeStamp"]
    result["dateFrac"]     = data["dateFrac"]
    result["cnt"]          = data["cnt"]
    result["predDev"]      = p

    if debugFlag:
        print("R 0-5: ", result[0:5])
    hdr = "timeStamp\tdateFrac\tcntDev\tpredDev"
    np.savetxt(output,result,fmt="%s",delimiter="\t",header=hdr,comments="")
#end writeResult

# Start
inputFileName = sys.argv[1]
outputFileName = sys.argv[2]
# All input columns - data types are strings, float and int
testData = np.genfromtxt(
    inputFileName,
    delimiter='\t',
    names=True,
    dtype=("|U19","|U10",int,float,int,float,float,int,float,float,
           int,int,int,int,int,int,int,int,int,int,
           int,int,int,int,int,int,int,int,int,int,
           int,int,int,int,int,int,int,int,int,int,
           int,int,int,int,int,int,int,int,int,int,
           int,int,int,int,int,int,int,int,int,int,
           int,int,int,int,int,int,int,int,int,int,
           int,int,int,int,int,int,int,int,int,int,
           int,int,int,int,int,int,int,int,int,int,
           int,int,int,int,int,int,int,int,int,int,
           int,int,int,int,int,int,int,int,int,int,
           int,int,int,int,int,int,int,int,int,int,
           int,int,int,int,int,int,int,int,int,int,
           int,int,int,int,int,int,int,int,int,int,
           int,int,int,int,int,int,int,int,int,int,
           int,int,int,int,int,int,int,int,int,int,
           int,int,int,int,int,int,int,int,int,int,
           int,int,int,int,int,int,int,int,int,int,
           int,int,int,int,int,int,int,int,int,int,
           int,int,int,int,int,int,int,int,int,int,
           int,int,int,int,int,int,int,int,int,int
    )
)

P = getPredictions(testData,hourWeekCols,"modelTrainDev")

writeResult(outputFileName,testData,P)
