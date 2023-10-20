from CarDealz_app.config.mysqlconnection import connectToMySQL
from CarDealz_app.models import user 
from flask import flash

class Car:
    def __init__(self, data):
        self.id=data['id']
        self.price=data['price']
        self.model=data['model']
        self.make=data['make']
        self.year=data['year']
        self.description=data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_owner_id=data['user_owner_id']

    @classmethod
    def getAll (cls):
        query="SELECT * FROM cars;"
        results=connectToMySQL('exam2').query_db(query)
        cars=[]
        for car in results:
            cars.append(cls(car))
        return cars
        
    @classmethod
    def getId (cls,id):
        query="SELECT * FROM cars WHERE id = %(id)s"
        data={
            'id':id
        }
        result=connectToMySQL('exam2').query_db(query,data)
        print("Result", result)
        if len(result)>0:
            return cls(result[0])
        else:
            return None
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO cars (id, price, model, make, year, description, created_at, updated_at, user_owner_id) VALUES (%(id)s,%(price)s,%(model)s,%(make)s,%(year)s,%(description)s, NOW(),NOW(),%(user_owner_id)s);"
        print(query)
        mysql = connectToMySQL('exam2')
        result = mysql.query_db(query, data)
        data_usuario={'id':data['id']}
        return cls.getId(data_usuario['id'])
    @classmethod
    def edit (cls, data):
        query = 'UPDATE cars SET price = %(price)s, model=%(model)s, make=%(make)s, year=%(year)s, description=%(description)s WHERE id = %(id)s;'
        mysql = connectToMySQL('exam2')
        result = mysql.query_db(query, data)
        return result
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM cars WHERE id = %(id)s and user_owner_id = %(user_owner_id)s;"
        mysql = connectToMySQL('exam2')
        result = mysql.query_db(query, data)
        return result
    @classmethod
    def getPurchased(cls):
        query= f"SELECT car_id FROM purchases;"
        results=  connectToMySQL('exam2').query_db( query )
        print("Purchased Cars:",results)
        cars=[]
        for car in results:
            cars.append(car.get('car_id'))
        print (cars)
        return cars
    @classmethod
    def getOwnersInfo(cls):
        query='SELECT users.fname,users.lname, user_owner_id, users.id as user_id, cars.id as car_id FROM cars LEFT JOIN users ON users.id=user_owner_id;'
        results=  connectToMySQL('exam2').query_db( query )
        print(results)
        return results
    @classmethod
    def getCarOwnerInfo(cls,car_id):
        query=f'SELECT users.fname,users.lname, user_owner_id, users.id as user_id, cars.id as car_id FROM cars LEFT JOIN users ON users.id=user_owner_id WHERE cars.id={car_id};'
        results=  connectToMySQL('exam2').query_db( query )
        print(results)
        return results

    @staticmethod
    def validations(car):
        is_valid=True
        if car['model'] == "":
            flash('Model is required')
            is_valid=False
        if car['make'] == "":
            flash('Make is required')
            is_valid=False
        if car['price'] == 0:
            flash('Price is required')
            is_valid=False
        if car['year'] == 0:
            flash('Year is required')
            is_valid=False
        if car['description'] == "":
            flash('Description is required')
            is_valid=False

        return is_valid
