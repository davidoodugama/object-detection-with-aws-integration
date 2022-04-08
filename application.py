from flask import Flask, request, jsonify, session
from flask_restful import Api, Resource, request
import requests
import shutil
import time
# from ocr.ocr import OCR
import numpy as np
# from connections.DB import cursor
from Controller import S3_config, DB_config
from const.const import IMG_DB_NAME, IMG_TB_NAME, SECRET_KEY
import collections
import json
from args.args import db_put_args, ins_details, s3_details
#cmd = 'chmod -rwx ffmpeg'
# os.system(cmd)


application = Flask(__name__)
api = Api(application)

application.secret_key = SECRET_KEY

# Store installation detials in RDS DB


class StoreInstallationDetails(Resource):
    def post(self):

        args = ins_details.parse_args()
        db = DB_config.DB_config(IMG_DB_NAME)

        workOrderID = args['workOrderID']
        msisdn = args['msisdn']
        visitID = args['visitID']
        accountID = args['accountID']

        res = db.insertInstallationDetailsDB(
            workOrderID, visitID, msisdn, accountID)
        session['workOrderID'] = workOrderID

        return jsonify({"response": res})

# Store images in S3 bucket and update RDS table


class Storeimage(Resource):
    def post(self):

        file = request.files['img']
        imageMajorIndex = request.form['imageMajorIndex']
        imageMinorIndex = request.form['imageMinorIndex']
        imageName = request.form['imageName']
        workOrderID = request.form['workOrderID']

        if "skip_reason" in request.form:
            skip_reason = request.form['skip_reason']
        else:
            skip_reason = 'null'

        if "workOrderID" in session:
            workOrderID = session["workOrderID"]

        db = DB_config.DB_config(IMG_DB_NAME)
        s3 = S3_config.S3Bucket(workOrderID)

        # Upload images to S3 and inserting values to DBs
        path, img_name = s3.renameFile_upload(file, imageName, workOrderID)
        # try:
        res = db.insertValues(IMG_TB_NAME, imageMajorIndex, path,
                              imageMinorIndex, imageName, workOrderID, skip_reason)
        # except:
        #print("DB is crashed")
        # s3.deletefile(path)

        return jsonify({"Message": img_name + " is uploaded and " + res})

# Resubmit an image and move the previous image to a different bucket


class resubmitImg(Resource):
    def post(self):
        '''file = request.files['img']
        imageMajorIndex = request.form['imageMajorIndex']'''
        file = request.files['img']
        imageMajorIndex = request.form['imageMajorIndex']
        imageMinorIndex = request.form['imageMinorIndex']
        imageName = request.form['imageName']

        if "skip_reason" in request.form:
            skip_reason = request.form['skip_reason']
        else:
            skip_reason = 'null'

        if "workOrderID" in session:
            workOrderID = session["workOrderID"]

        db_name = IMG_DB_NAME
        tb_name = IMG_TB_NAME

        db = DB_config.DB_config(db_name)
        s3 = S3_config.S3Bucket(workOrderID)
        img_url = db.getImageavailabilitystatus(
            workOrderID, imageMajorIndex, tb_name)
        url = img_url[0][0]
        img_name = img_url[0][1]
        print(img_name)
        path, imageName = s3.Img_available(
            url, img_name, file, imageName, workOrderID)

        res = db.insertValues(IMG_TB_NAME, imageMajorIndex, path,
                              imageMinorIndex, imageName, workOrderID, skip_reason)

        return res


class getTableVaule(Resource):
    def get(self):
        args = db_put_args.parse_args()
        db_name = args['name']
        tb_name = args['tbname']
        # work_id = args['work_id']
        db = DB_config.DB_config(db_name)
        res = db.getAllData(tb_name)
        super_dict1 = collections.defaultdict(list)
        super_dict2 = collections.defaultdict(list)
        work = []
        '''for x in range(len(res[1])):
                work.append(x)'''
        [work.append(x[1]) for x in res]
        work = np.unique(np.array(work))
        print("workList: " + str(work))
        for i in work:
            print("work " + str(i))
            super_dict2 = collections.defaultdict(list)
            # super_dict1["work_id"] = int(i)
            for tup in res:
                print("tuple " + str(tup[1]))

                if int(tup[1]) == int(i):
                    print(int(tup[1]) == int(i))

                    # out = {  "work_id" : tup[1],
                    #          "Image Name" : tup[2],
                    #          "Image URL" : tup[3]}
                    super_dict2["img"].append({"work_id": tup[1],
                                               "Image Name": tup[2],
                                               "Image URL": tup[3]})
                #print("work " + str(i))
                    print("out " + str({"work_id": tup[1],
                                        "Image Name": tup[2],
                                        "Image URL": tup[3]}))
                    print("super_dict2 " + str(super_dict2))
            super_dict1["image_details"].append(super_dict2)
            print("super_dict1 " + str(super_dict1))
        #print("work " + str(i) )
        #print("out " + super_dict2)
        # super_dict2["img"].append(super_dict1["image_details"])

        return jsonify(super_dict1)


class GetTablesValues(Resource):
    def get(self):
        args = db_put_args.parse_args()
        db_name = args['name']
        tb_name = args['tbname']
        sql = '''select * from %s''' % (tb_name)
        cursor.execute(sql)
        out_put = cursor.fetchall()
        # Get name pf the image from the response
        return jsonify({"Image_name": out_put[0][1]})

# Get Image meta data and predicted results and store in RDS


class GetImageMetaData(Resource):
    def post(self):
        images = []
        req_data = request.get_json()
        workOrderID = req_data['workOrderID']
        msisdn = req_data['msisdn']

        for imgs in req_data['image']:
            images.append(imgs['imageName'])
        s3 = S3_config.S3Bucket(workOrderID)
        db = DB_config.DB_config(IMG_DB_NAME)
        res, path1 = s3.getimages(images, workOrderID, msisdn)

        url1 = "https://w7lefk1fm8.execute-api.us-east-1.amazonaws.com/default/myModel"
        headers = {'Content-type': "application/json"}

        t1 = time.time()
        print('t1: {}'.format(t1))

        r1 = requests.post(url1, headers=headers, data=json.dumps(res))

        t2 = time.time()
        print('time: {}'.format(t2 - t1))
        r2 = r1.json()

        try:
            shutil.rmtree(path1)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
        #
        #
        #
        '''status = r1['response'][0]['detections'][0]['class']
        score = r1['response'][0]['detections'][0]['confidence']
        imageName = r1['response'][0]['image']'''
        #r1 = requests.post(url1, files={'file':(file.filename, file.stream, file.content_type, file.headers)})
        # res = db.UpdateImgTable(IMG_TB_NAME, workOrderID, status, score, imageName)
        # return jsonify('r2')
        return jsonify(r2)


class getFilesInS3(Resource):
    def get(self):
        args = s3_details.parse_args()
        work_order_id = args['work_order_id']
        s3 = S3_config.S3Bucket(work_order_id)
        res = s3.getimages()
        return jsonify(res)


class getOCRValues(Resource):

    def post(self):
        im = []
        req_data = request.get_json()
        workOrderID = req_data['workOrderID']
        image_name = req_data['img_name']
        s3 = S3_config.S3Bucket(workOrderID)
        res = s3.downloadImages(image_name, workOrderID)
        '''workOrderID = req_data['workOrderID']
        msisdn = req_data['msisdn']
        submissionStatus = req_data['submissionStatus']
        image_name = req_data['image'][0]["imageName"]'''
        ocr = OCR(workOrderID)
        ocr.paddleTextDetector(res, image_name)
        #pwr, ber, cn = ocr.detectText(res, image_name)
        '''res = {
            "PWR": pwr,
            "BER": ber,
            "CN": cn
        }'''
        return jsonify('res')


api.add_resource(Storeimage, "/upload_img")
api.add_resource(getOCRValues, "/getOCRValues")
api.add_resource(GetTablesValues, "/getvalues")
api.add_resource(getTableVaule, "/getablevalues")
api.add_resource(StoreInstallationDetails, "/StoreInstallationDetails")
api.add_resource(resubmitImg, "/resubmitImg")
api.add_resource(getFilesInS3, "/getFilesInS3")
api.add_resource(GetImageMetaData, "/getImageMetaData")


if __name__ == "__main__":
    application.run(debug=True)
