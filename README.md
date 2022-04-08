# object-detection-with-aws-integration

This repo contains AWS S3 and RDS integration.
S3 - is used to store images. From S3 bucket model will retreive the image and make the predictions.
RDS - is used to store Image and prediction detials.

DB_config file contains all the CRUD operation for DB
S3_config file contains storing images function, Removing images and storing them in removed bucket function and many more.

Additionally 2 OCR technologies has been used here.
1. PaddleOCR
2. Easy OCR

Reason for using 2 techniques - Paddle OCR has the ability to detect blur images with high accuracy and convert the image keeping the letters only.
                              - Easy OCR has the ability to read line by line but Paddle OCR wont read line by line. So Easy OCR is used in here.
