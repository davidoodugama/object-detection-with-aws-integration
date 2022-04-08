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
