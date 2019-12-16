import mysql.connector
import dbconfig as cfg

class ProductsDAO:
    db=""
    def connectToDB(self):
        self.db = mysql.connector.connect(
            host=       cfg.mysql['host'],
            user=       cfg.mysql['user'],
            password=   cfg.mysql['password'],
            database=   cfg.mysql['database']
        )
    def __init__(self): 
        self.connectToDB()
     
    
    def getCursor(self):
        if not self.db.is_connected():
            self.connectToDB()
        return self.db.cursor()
    
            
    def create(self, values):
        cursor = self.getCursor()
        sql="insert into products (Product,Model, Price) values (%s,%s,%s)"
        cursor.execute(sql, values)

        self.db.commit()
        lastRowId=cursor.lastrowid
        cursor.close
        return lastRowId

    def getAll(self):
        cursor = self.getCursor()
        sql="select * from products"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))
        cursor.close
        return returnArray

    def findByID(self, id):
        cursor = self.getCursor()
        sql="select * from products where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        products=self.convertToDictionary(result)
        cursor.close()
        return products

    def update(self, values):
        cursor = self.getCursor()
        sql="update products set Product= %s,Model=%s, Price=%s  where id = %s"
        cursor.execute(sql, values)
        self.db.commit()
    def delete(self, id):
        cursor = self.db.cursor()
        sql="delete from products where id = %s"
        values = (id,)

        cursor.execute(sql, values)

        self.db.commit()
        cursor.close()
        

    def convertToDictionary(self, result):
        colnames=['id','Product','Model', "Price"]
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
        
productsDAO = ProductsDAO()