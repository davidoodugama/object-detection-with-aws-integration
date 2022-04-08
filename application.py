from flask import Flask, request, jsonify, session
from flask_restful import Api, Resource
# from ocr.ocr import OCR
import numpy as np
# from connections.DB import cursor
from Controller import DB_config
from const.const import IMG_DB_NAME, IMG_TB_NAME, SECRET_KEY
import collections
import json
from args.args import ins_details
#cmd = 'chmod -rwx ffmpeg'
# os.system(cmd)


application = Flask(__name__)
api = Api(application)

application.secret_key = SECRET_KEY

# Store Images detials in RDS DB


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
api.add_resource(StoreInstallationDetails, "/StoreInstallationDetails")

if __name__ == "__main__":
    application.run(debug=True)
