from flask_restful import reqparse

image_put_args = reqparse.RequestParser()
image_put_args.add_argument("name", type = str, help = "Name is reuqired", required = True)

image_input = reqparse.RequestParser()
image_input.add_argument("img_name", type = str, help = "Name is reuqired", required = True)

db_put_args = reqparse.RequestParser()
db_put_args.add_argument("name", type = str, help = "Database name is reuqired", required = True)
db_put_args.add_argument("tbname", type = str, help = "table name is reuqired")
db_put_args.add_argument("col_name", type = str, help = "Database name is reuqired")
db_put_args.add_argument("work_id", type = int, help = "table name is reuqired")

ins_details = reqparse.RequestParser()
ins_details.add_argument("workOrderID", type = str, help = "workOrderID is reuqired", required = True)
ins_details.add_argument("visitID", type = str, help = "visitID is reuqired", required = True)
ins_details.add_argument("msisdn", type = str, help = "MSISDN is reuqired", required = True)
ins_details.add_argument("accountID", type = str, help = "accountID is reuqired", required = True)

s3_details = reqparse.RequestParser()
s3_details.add_argument("work_order_id", type = str, help = "work_order_id is reuqired", required = True)

# Meta Data Args
img_meta_data = reqparse.RequestParser()
img_meta_data.add_argument("work_order_id", type = str, help = "work_order_id is reuqired", required = True)
img_meta_data.add_argument("msisdn", type = str, help = "msisdn is reuqired", required = True)
img_meta_data.add_argument("submissionStatus", type = str, help = "submissionStatus is reuqired", required = True)
img_meta_data.add_argument("image", type = str, help = "image details reuqired", required = True)