from flask import Flask, jsonify, request, send_from_directory
from flask_restful import Api, Resource
from flask_cors import CORS
import os

app = Flask(__name__)
api = Api(app)
CORS(app)

app.config["UPLOAD_FOLDER"] = "static/images/"

products = [
    {
        "id": 1,
        "name": "Iphone X - 256 GB",
        "description": "Esta es la descripción del iphone X",
        "price": 450,
        "image": "iphone-x.png"
    },
    {
        "id": 2,
        "name": "Iphone 11 Pro Max - 64 GB",
        "description": "Esta es la descripción del iphone 11 Pro Max",
        "price": 580,
        "image": "iphone-11promax.png"
    }
]

class Product(Resource):
    def get(self, id):
        for product in products:
            if product["id"] == id:
                product["image_url"] = request.host_url + os.path.join(app.config["UPLOAD_FOLDER"], product["image"])
                return jsonify(product)
        return jsonify({"error": "Producto no encontrado"})

    def put(self, id):
        for product in products:
            if product["id"] == id:
                product["name"] = request.json["name"]
                product["description"] = request.json["description"]
                product["price"] = request.json["price"]
                return jsonify(product)
        return jsonify({"error": "Producto no encontrado"})

class Products(Resource):
    def get(self):
        for product in products:
            product["image_url"] = request.host_url + os.path.join(app.config["UPLOAD_FOLDER"], product["image"])
        return jsonify(products)

    def post(self):
        new_product = {
            "id": len(products) + 1,
            "name": request.json["name"],
            "description": request.json["description"],
            "price": request.json["price"],
            "image": request.json["image"]
        }
        products.append(new_product)
        return jsonify(new_product)

@app.route("/static/images/<path:filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=False)

api.add_resource(Product, "/product/<int:id>")
api.add_resource(Products, "/products")

if __name__ == "__main__":
    app.run(debug=True)
