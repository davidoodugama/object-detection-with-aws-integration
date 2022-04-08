from connections.DB import db, cursor

from const.const import INSTALLATION_TB


class DB_config:
    def __init__(self, db_name):

        self.db_name = db_name
        #self.work_id = int(work_id)

    def useDB(self):
        sql = '''use %s''' % (self.db_name)
        cursor.execute(sql)

    def createDB(self):
        sql = '''create database %s''' % (self.db_name)
        cursor.execute(sql)
        cursor.connection.commit()
        db.commit()

    def createTable(self, tb_name):
        sql = '''use %s''' % (self.db_name)
        cursor.execute(sql)

        self.tb_name = tb_name
        sql = '''create table %s (
            id int not null auto_increment,
            work_id int,
            img_name text,
            img_url text,
            primary key(id) 
            )''' % (self.tb_name)
        cursor.execute(sql)
        db.commit()

        return "Table name " + self.tb_name + " created"

    # Insert value to Image_Table
    def insertValues(self, tb_name, imageMajorIndex, path, imageMinorIndex, imageName, workOrderID, skip_reason):
        self.useDB()

        sql = '''insert into %s(imageName, imageMinorIndex, imageMajorIndex, skip_reason, workOrderID, imageURL) values('%s', %i, %i, '%s',%i, '%s')
        ''' % (tb_name,
               imageName,
               int(imageMinorIndex),
               int(imageMajorIndex),
               skip_reason,
               int(workOrderID),
               path)

        cursor.execute(sql)
        db.commit()
        return "Values inserted to table " + tb_name

    def getAllData(self, tb_name):
        self.useDB()
        sql = '''select * from %s''' % (tb_name)
        cursor.execute(sql)
        out_put = cursor.fetchall()
        return out_put

    # Insert value to Installation_detail
    def insertInstallationDetailsDB(self, workOrderID, visitID, msisdn, accountID):
        self.useDB()

        sql = '''insert into %s(workOrderID, msisdn, visitID, accountId) 
                values(%i, %i, %i, %i)
                ''' % (
            INSTALLATION_TB,
            int(workOrderID),
            int(msisdn),
            int(visitID),
            int(accountID))

        cursor.execute(sql)
        db.commit()

        return "Values inserted to table " + INSTALLATION_TB + " for Work order ID " + workOrderID

    # Get Image detials to move the image to a different bucket
    def getImageavailabilitystatus(self, workOrderID, imageMajorIndex, tb_name):
        self.useDB()
        sql = '''select imageURL, imageName
                 from %s 
                 where workOrderID = %i AND
                 imageMajorIndex = %i
                ''' % (
            tb_name,
            int(workOrderID),
            int(imageMajorIndex)
        )
        cursor.execute(sql)
        out_put = cursor.fetchall()
        return out_put

    def UpdateImgTable(self, tb_name, workOrderID, status, score, imageName):
        self.useDB()
        sql = '''update %s
                 set pre_status = '%s', score = %i
                 where workOrderID = %i AND imageName = '%s'
                ''' % (
            tb_name,
            str(status),
            int(score),
            int(workOrderID),
            imageName
        )
        cursor.execute(sql)
        db.commit()
        return "Values inserted to table " + tb_name
