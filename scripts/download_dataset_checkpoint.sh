#! /bin/bash

DATASET_DIR="dataset/flowers"
#mkdir -p $DATASET_DIR

echo -e "\n********** Download and convert dataset **********"
python download_and_convert_flowers.py

echo -e "\n********** Download checkpoint for inception_resnet_v2 **********"
CHECKPOINT_DIR="checkpoint"
mkdir ${CHECKPOINT_DIR}
wget https://storage.googleapis.com/download.tensorflow.org/models/pnasnet-5_large_2017_12_13.tar.gz --no-check-certificate
tar -zxvf pnasnet-5_large_2017_12_13.tar.gz -C ${CHECKPOINT_DIR}
