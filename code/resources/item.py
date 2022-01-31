import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type=float,
    required=True,
    help='This field cannot be left blank!'
    )

    @jwt_required()
    def get(self, name):
        item  = self.find_by_name(name)
        if item:
            return item

        return {'message':'item not found'}, 404

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name, ))
        # row = result.fetchone()
        # connection.close()

        # if row:
        #     return{'item':{'name': row[0], 'price':row[1]}}
        # return {'message': 'Item not found'}, 404

        # item = next(filter(lambda x: x['name']==name, items ), None)
        # return {'item':item}, 200 if item  else 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name, ))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        #data = request.get_json()
        #You can use force or silent inside request.get_json()
        data = Item.parser.parse_args()

        item = {'name':name, 'price':data['price']}

        try:
            self.insert(item)
        except:
            return {"message": "An error occurred inserting the item"}, 500 #internal server error

        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self, name):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE from items WHERE name = ?"
        cursor.execute(query, (name, ))

        connection.commit()
        connection.close()
        return {'message': 'Item Deleted'}

        # global items
        # items = list(filter(lambda x: x['name']!= name, items))
        # return {'message':'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        # item = next(filter(lambda x: x['name'] == name, items), None)

        if item is None:
            # item = {'name': name, 'price': data['price']}
            # items.append(item)
            try:
                self.insert(item)
            except:
                return {"message":"An error occurred inserting the item"}, 500
        else:
            # item.update(data)
            try:
                self.update(updated_item)
            except:
                return {"message":"An error occurred updating the item."},500
        return item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name':row[0], 'price':row[1]})

        connection.close()
        # rows = result.fetchall()
        # return {'items':rows}
        return {'items':items}
