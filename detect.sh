#!/bin/bash
#######################################################
# Script:
#    detect.sh
# Usage:
#    ./detect.sh
# Description:
#    Generate input data sets
#    Build the predictive model using training data
#    Get the prediction on test data
#    Detect exceptions and generate alerts
# Authors:
#    Jasmin Nakic,    jnakic@salesforce.com
#    Samir Pilipovic, spilipovic@salesforce.com
#######################################################

SCRIPTDIR=scripts
INPUTDIR=data
RESULTDIR=results

python $SCRIPTDIR/genFeatures.py $INPUTDIR/train_input.txt > $RESULTDIR/train_data.txt
python $SCRIPTDIR/genFeatures.py $INPUTDIR/test_input.txt  > $RESULTDIR/test_data.txt

python $SCRIPTDIR/trainPerf.py    $RESULTDIR/train_data.txt $RESULTDIR/train_hourly.txt
python $SCRIPTDIR/trainHoliday.py $RESULTDIR/train_data.txt $RESULTDIR/train_hourly.txt $RESULTDIR/train_holiday.txt
python $SCRIPTDIR/trainExc.py     $RESULTDIR/train_data.txt $RESULTDIR/train_hourly.txt $RESULTDIR/train_exc.txt

python $SCRIPTDIR/testPerf.py    $RESULTDIR/test_data.txt $RESULTDIR/test_hourly.txt
python $SCRIPTDIR/testHoliday.py $RESULTDIR/test_data.txt $RESULTDIR/test_hourly.txt $RESULTDIR/test_holiday.txt
python $SCRIPTDIR/testExc.py     $RESULTDIR/test_data.txt $RESULTDIR/test_hourly.txt $RESULTDIR/test_exc.txt

python $SCRIPTDIR/genDev.py $RESULTDIR/train_exc.txt $RESULTDIR/train_ma.txt
python $SCRIPTDIR/genDev.py $RESULTDIR/test_exc.txt  $RESULTDIR/test_ma.txt

# Prepare data for anomaly detection - cut the input file due to outliers
awk -f $SCRIPTDIR/dev.awk $RESULTDIR/train_ma.txt | head -1191 > $RESULTDIR/train_dev.txt
python $SCRIPTDIR/genFeatures.py $RESULTDIR/train_dev.txt  > $RESULTDIR/train_dev_pred.txt
awk -f $SCRIPTDIR/dev.awk $RESULTDIR/test_ma.txt > $RESULTDIR/test_dev.txt
python $SCRIPTDIR/genFeatures.py $RESULTDIR/test_dev.txt  > $RESULTDIR/test_dev_pred.txt

# Build the model to learn deviation patterns
python $SCRIPTDIR/trainDev.py $RESULTDIR/train_dev_pred.txt $RESULTDIR/train_devMA.txt
join -j 1 -t "	" -o 1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,1.10,1.11,1.12,1.13,2.4 $RESULTDIR/train_ma.txt $RESULTDIR/train_devMA.txt > $RESULTDIR/train_anom.txt
# Generate deviation predictions for test data
python $SCRIPTDIR/testDev.py  $RESULTDIR/test_dev_pred.txt  $RESULTDIR/test_devMA.txt
join -j 1 -t "	" -o 1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,1.10,1.11,1.12,1.13,2.4 $RESULTDIR/test_ma.txt  $RESULTDIR/test_devMA.txt  > $RESULTDIR/test_anom.txt

# Detect anomalies
echo DETECT
python $SCRIPTDIR/getAnom.py $RESULTDIR/train_anom.txt $RESULTDIR/train_detect.txt > detect.out.train
python $SCRIPTDIR/getAnom.py $RESULTDIR/test_anom.txt $RESULTDIR/test_detect.txt > detect.out.test
