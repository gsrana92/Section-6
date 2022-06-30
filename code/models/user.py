import sqlite3
from db import db
# from datetime import datetime, timedelta
# from azure.storage.blob import generate_container_sas, ContainerSasPermissions
# from azure.storage.blob import generate_blob_sas, BlobSasPermissions

class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    # account_name = 'covidreporting92sa'
    # account_key = 'Tal7dGBIaNCZVceVZ1/cbTs3vmH7IenOnTlLPjcojx4RK3qHqyZn9fQIqekq+v6PkdhbmowKQYfI+ASteTKWxw=='
    # container_name = 'population'
    #
    # def get_img_url_with_container_sas_token(blob_name)



    def __init__(self, username, password):

        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls,  username):
        return cls.query.filter_by(username=username).first()

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM users WHERE username=?"
        # result = cursor.execute(query, (username,))
        # row = result.fetchone()
        # if row:
        #     #user = cls(row[0], row[1], row[2])
        #     user = cls(*row)
        # else:
        #     user = None
        #
        # connection.close()
        # return user

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id)

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM users WHERE id=?"
        # result = cursor.execute(query, (_id,))
        # row = result.fetchone()
        # if row:
        #     # user = cls(row[0], r
        #    # ow[1], row[2])
        #     user = cls(*row)
        # else:
        #     user = None
        #
        # connection.close()
        # return user
