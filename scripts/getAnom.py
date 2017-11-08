#######################################################
# Script:
#    getAnom.py
# Usage:
#    python getAnom.py <input_file> <output_file>
# Description:
#    Detect anomalies on test data
# Authors:
#    Jasmin Nakic, jnakic@salesforce.com
#    Samir Pilipovic, spilipovic@salesforce.com
#######################################################

import sys
from math import sqrt
from math import floor
import numpy as np

# Script debugging flag
debugFlag = False
DIFFMIN = 70000
DEVCNT = 1.5

# Function to validate rule
def applyRule(V,P,D):
    lowPred = P - floor(D*DEVCNT)
    highPred = P + floor(D*DEVCNT)
    diff = P - V
    alert = ""
    if (V < lowPred or highPred < V) and abs(diff) > DIFFMIN:
        if P > V:
            alert = "HIGH"
        else:
            alert = "LOW"
    else:
        diff = 0
    return (alert,diff)

#end applyRule

# Iterate over test results
def getAnom(data):
    X = np.zeros(data.shape[0])
    Y = np.zeros(data.shape[0])
    row = 0
    raiseAlert = False
    for m in np.nditer(data):
        cMA = m['cntMA']
        pMA = m['predMA']
        pDev = m['predDev']
        (alert,diff) = applyRule(cMA,pMA,pDev)
        tmpRatio = 0.0
        if pDev > 0:
            tmpRatio = abs(cMA-pMA)/pDev
        if debugFlag:
            print("DEBUG: ",m['timeStamp'],alert,cMA,pMA,pDev,cMA-pMA,tmpRatio,diff)
        if alert != "":
            Y[row] = diff
            if alert == "HIGH":
                X[row] = 1
            else: # LOW
                X[row] = -1
            print(alert,"alert at", m['timeStamp'], "Moving average difference", diff, "from prediction", pMA)
        row = row + 1
    return (X,Y)
#end getAnom

# Write results to file
def writeResult(output,calcData,A,D):
    # generate result file
    result = np.array(
        np.empty(calcData.shape[0]),
        dtype=[
            ("timeStamp","|U19"),
            ("dateFrac",float),
            ("isHoliday",int),
            ("isSunday",int),
            ("cnt",int),
            ("predSimple",int),
            ("predTrig",int),
            ("predHourDay",int),
            ("predHourWeek",int),
            ("predHS",int),
            ("cntMA",int),
            ("predMA",int),
            ("devMA",int),
            ("predDev",int),
            ("alertVal",int),
            ("diffMA",int)
        ]
    )

    result["timeStamp"]    = calcData["timeStamp"]
    result["dateFrac"]     = calcData["dateFrac"]
    result["isHoliday"]    = calcData["isHoliday"]
    result["isSunday"]     = calcData["isSunday"]
    result["cnt"]          = calcData["cnt"]
    result["predSimple"]   = calcData["predSimple"]
    result["predTrig"]     = calcData["predTrig"]
    result["predHourDay"]  = calcData["predHourDay"]
    result["predHourWeek"] = calcData["predHourWeek"]
    result["predHS"]       = calcData["predHS"]
    result["cntMA"]        = calcData["cntMA"]
    result["predMA"]       = calcData["predMA"]
    result["devMA"]        = calcData["devMA"]
    result["predDev"]      = calcData["predDev"]
    result["alertVal"]     = A
    result["diffMA"]       = D

    if debugFlag:
        print("R 0-5: ", result[0:5])
    hdr = "timeStamp\tdateFrac\tisHoliday\tisSunday\tcnt\tpredSimple\tpredTrig\tpredHourDay\tpredHourWeek\tpredHS\tcntMA\tpredMA\tdevMA\tpredDev\talertVal\tdiffMA"
    np.savetxt(output,result,fmt="%s",delimiter="\t",header=hdr,comments="")
#end writeResult

# Process alerts for input file
def process(inputFile,outputFile):
    # timeStamp dateFrac isHoliday isSunday cnt predSimple predTrig predHourDay predHourWeek predHS cntMA predMA devMA predDev
    testData = np.genfromtxt(
        inputFile,
        delimiter='\t',
        names=True,
        dtype=("|U19",float,int,int,int,int,int,int,int,int,int,int,int,int)
    )

    (AV,DV) = getAnom(testData)
    writeResult(outputFile,testData,AV,DV)
#end process

# Start
inputFileName = sys.argv[1]
outputFileName = sys.argv[2]

process(inputFileName,outputFileName)

# Load results from file generated above using correct data types
results = np.genfromtxt(
    outputFileName,
    dtype=("|U19",float,int,int,int,int,int,int,int,int,int,int,int,int,int,int),
    delimiter='\t',
    names=True
)

# Examine result data
if debugFlag:
    print("Shape:", results.shape)
    print("Columns:", len(results.dtype.names))
    print(results[1:5])
