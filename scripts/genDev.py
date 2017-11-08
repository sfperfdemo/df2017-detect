#######################################################
# Script:
#    genDev.py
# Usage:
#    python getnDev.py <input_file> <output_file>
# Description:
#    Generate deviation for last 3 measures
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

# Iterate over test results
def getStdDev(data):
    X = np.zeros(data.shape[0])
    Y = np.zeros(data.shape[0])
    Z = np.zeros(data.shape[0])
    v = [0,0,0]
    p = [0,0,0]
    idx = 0
    row = 0
    raiseAlert = False
    for m in np.nditer(data):
        idx = idx + 1
        v[0] = v[1] if idx > 2 else 0
        v[1] = v[2] if idx > 1 else 0
        v[2] = m['cnt']
        p[0] = p[1] if idx > 2 else 0
        p[1] = p[2] if idx > 1 else 0
        p[2] = m['predHS']
        if idx > 2:
            # Calculate MA for values and predictions
            X[row] = floor((v[0] + v[1] + v[2]) / 3)
            Y[row] = floor((p[0] + p[1] + p[2]) / 3)
            # Calculate Deviation
            Z[row] = floor(sqrt(((p[0] - v[0])**2 + (p[1] - v[1])**2 + (p[2] - v[2])**2)/2))
        row = row + 1
    return (X,Y,Z)
#end getStdDev

# Write results to file
def writeResult(output,calcData,C,P,D):
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
            ("devMA",int)
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
    result["cntMA"]        = C
    result["predMA"]       = P
    result["devMA"]        = D

    if debugFlag:
        print("R 0-5: ", result[0:5])
    hdr = "timeStamp\tdateFrac\tisHoliday\tisSunday\tcnt\tpredSimple\tpredTrig\tpredHourDay\tpredHourWeek\tpredHS\tcntMA\tpredMA\tdevMA"
    np.savetxt(output,result,fmt="%s",delimiter="\t",header=hdr,comments="")
#end writeResult

# Process alerts for input file
def process(inputFile,outputFile):
    # timeStamp dateFrac isHoliday isSunday cnt predSimple predTrig predHourDay predHourWeek predHS
    testData = np.genfromtxt(
        inputFile,
        delimiter='\t',
        names=True,
        dtype=("|U19",float,int,int,int,int,int,int,int,int)
    )

    (CA,PA,DV) = getStdDev(testData)
    writeResult(outputFile,testData,CA,PA,DV)
#end process

# Start
inputFileName = sys.argv[1]
outputFileName = sys.argv[2]

process(inputFileName,outputFileName)

# Load results from file generated above using correct data types
results = np.genfromtxt(
    outputFileName,
    dtype=("|U19",float,int,int,int,int,int,int,int,int,int,int,int),
    delimiter='\t',
    names=True
)

# Examine result data
print("Shape:", results.shape)
print("Columns:", len(results.dtype.names))
print(results[1:5])
