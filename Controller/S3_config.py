import os
from connections.S3 import s3, s3_1
from const.const import BUCKET_NAME, FILE_URL, FILE_NOT_EXIST, DELETED_IMG_BUCKET_NAME
import time
from datetime import date
import botocore
import glob
from base64 import encodebytes
import io
from PIL import Image
import collections


class S3Bucket:
    def __init__(self, work_id):

        self.work_id = work_id
        self.current_date = date.today()

    # Rename and store image
    def renameFile_upload(self, file, imageName, workOrderID):

        current_time = str(time.time() * 1000)
        current_time = current_time.replace(".", "")

        file.save(imageName)
        directory = str(self.current_date) + '/' + str(self.work_id)
        s3.Bucket(BUCKET_NAME).upload_file(
            Filename=imageName, Key=directory + '/' + imageName)
        path = FILE_URL + directory + '/' + imageName

        if os.path.exists(imageName):
            os.remove(imageName)
        else:
            print(FILE_NOT_EXIST + str(imageName))

        return path, imageName

    # Delete files
    def deletefile(self, key):
        s3.Object(BUCKET_NAME, key).delete()

        return "Delete successful"

    # Resubmiting and deleting img

    def Img_available(self, url, img_name, file, imageName, workOrderID):
        url = url.replace(FILE_URL, "")
        directory = str(self.current_date) + '/' + \
            str(self.work_id) + '/' + img_name

        # Checking whether object iss available in S3 bucket
        # Move the object into another bucket
        try:
            s3.Object(BUCKET_NAME, url).load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print('object does not exsit')
            else:
                print("internal error")
                raise
        else:
            print("object exsit")
            copy_source = {'Bucket': BUCKET_NAME, 'Key': url}
            s3.meta.client.copy(
                copy_source, DELETED_IMG_BUCKET_NAME, directory)

        # Delete the moved object from current S3 buckets
        s3.Object(BUCKET_NAME, directory).delete()

        # Store the new file in the bucket
        path, imageName = self.renameFile_upload(file, imageName, workOrderID)
        return path, imageName

    def get_response_image(self, image_path):
        pil_img = Image.open(image_path, mode='r')  # reads the PIL image
        byte_arr = io.BytesIO()
        # convert the PIL image to byte array
        pil_img.save(byte_arr, format='jpeg')
        encoded_img = encodebytes(byte_arr.getvalue()).decode(
            'ascii')  # encode as base64
        return encoded_img

    def getimages(self, image_name, work_order_id, msisdn):

        path1 = "work_order " + str(work_order_id) + "_" + str(msisdn)
        isFile = os.path.isfile(path1)

        if isFile == False:
            os.mkdir(path1)
        else:
            pass
        os.chdir(path1)

        response = s3_1.list_objects_v2(Bucket=BUCKET_NAME, Prefix=str(
            self.current_date) + "/" + str(self.work_id))
        files = response.get("Contents")

        # Get the images list in s3 bucket
        for file in files:
            s3_path = file['Key']
            name = s3_path.replace(str(self.current_date) +
                                   "/" + str(self.work_id) + "/", "")

            # Downloading Files
            if name in image_name:
                s3.Bucket(BUCKET_NAME).download_file(
                    Key=s3_path, Filename=name)

        # Go back from download folder
        os.chdir('../')

        images = []
        super_dict1 = collections.defaultdict(list)
        super_dict1["work_order_id"] = work_order_id
        super_dict1["Status"] = 'Success'
        super_dict2 = collections.defaultdict(list)
        for file in glob.glob(path1 + "/*.jpg"):
            i = image_name.index(file.replace(path1 + "\\", ""))
            encoded_img = self.get_response_image(file)
            my_message = 'here is my message'  # create your message as per your need
            images.append(encoded_img)
            super_dict2["image_details"].append({"Image_name": image_name[i],
                                                 "imagebytes": images})

        # print(super_dict2["image_details"])
        super_dict1["imagebytes"].append(super_dict2)
        # for sup in super_dict1["imagebytes"]:
        #     for sup1 in sup["image_details"]:
        #         print(sup1)
        return super_dict1, path1

    # Download files
    def downloadImages(self, image_name, work_order_id):
        li = []

        response = s3_1.list_objects_v2(Bucket=BUCKET_NAME, Prefix=str(
            self.current_date) + "/" + str(self.work_id))
        files = response.get("Contents")

        for file in files:
            li.append(file['Key'])

        path1 = "OCR_work_order " + str(work_order_id) + "_"
        isFile = os.path.isfile(path1)

        if isFile == False:
            os.mkdir(path1)
        else:
            pass

        os.chdir(path1)

        for i in range(len(li)):
            name = li[i]
            name = name.replace(str(self.current_date) +
                                "/" + str(self.work_id) + "/", "")
            if name == image_name:
                s3.Bucket(BUCKET_NAME).download_file(
                    Key=li[i], Filename=image_name)

        os.chdir('../')

        return path1
