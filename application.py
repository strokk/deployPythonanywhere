from flask import Flask, jsonify, request, abort
from productsDAO import productsDAO
from flask_cors import CORS


app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)


#curl "http://127.0.0.1:5000/products"
@app.route('/products')
def getAll():
    #print("in getall")
    results = productsDAO.getAll()
    return jsonify(results)

#curl "http://127.0.0.1:5000/products/2"
@app.route('/products/<int:id>')
def findById(id):
    foundProduct = productsDAO.findByID(id)

    return jsonify(foundProduct)

#curl  -i -H "Content-Type:application/json" -X POST -d "{\"Product\":\"testProduct\",\"Model\":\"testModel\",\"Price\":123}" http://127.0.0.1:5000/products
@app.route('/products', methods=['POST'])
def create():
    
    if not request.json:
        abort(400)
    # other checking 
    products = {
        "Product": request.json['Product'],
        "Model": request.json['Model'],
        "Price": request.json['Price'],
    }
    values =(products['Product'],products['Model'],products['Price'])
    newId = productsDAO.create(values)
    products['id'] = newId
    return jsonify(products)

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"Product\":\"testProduct\",\"Model\":\"testModel\",\"Price\":125}" http://127.0.0.1:5000/products/1
@app.route('/products/<int:id>', methods=['PUT'])
def update(id):
    foundProduct = productsDAO.findByID(id)
    if not foundProduct:
        abort(404)
    
    if not request.json:
        abort(400)
    reqJson = request.json
    if 'Price' in reqJson and type(reqJson['Price']) is not int:
        abort(400)

    if 'Product' in reqJson:
        foundProduct['Product'] = reqJson['Product']
    if 'Model' in reqJson:
        foundProduct['Model'] = reqJson['Model']
    if 'Price' in reqJson:
        foundProduct['Price'] = reqJson['Price']
    values = (foundProduct['Product'],foundProduct['Model'],foundProduct['Price'],foundProduct['id'])
    productsDAO.update(values)
    return jsonify(foundProduct)
        

    

@app.route('/products/<int:id>' , methods=['DELETE'])
def delete(id):
    productsDAO.delete(id)
    return jsonify({"done":True})




if __name__ == '__main__' :
    app.run(debug= True)