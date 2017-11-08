#!/bin/bash

RESULTDIR=../results
cp $RESULTDIR/train_data.txt .
cp $RESULTDIR/test_data.txt .
cp $RESULTDIR/train_detect.txt .
cp $RESULTDIR/test_detect.txt .

# Example how you can automate creation of json files
# python genjson.py > fields.json
# cat head.json fields.json tail.json > train_data_schema.json
# cat head.json fields.json tail.json > test_data_schema.json
# Now modify manually all json files...

./load_dataset.sh "My Private App" TrainData   train_data.txt
./load_dataset.sh "My Private App" TestData    test_data.txt
./load_dataset.sh "My Private App" TrainDetect train_detect.txt
./load_dataset.sh "My Private App" TestDetect  test_detect.txt
