from flask_restplus import Namespace, fields, reqparse

api = Namespace("sales", description="Sales related operations")

sales = api.model("sales", {
    "id": fields.Integer(readonly=True),
    "product_name":fields.String(required=True, description="The product product_name"),
    "product_quantity":fields.String(required=True, description="The product product_quantity"),
    "user_id":fields.String(required=True, description="The product user_id"),
    "created_at":fields.String(required=True, description="The product creation date")
    })

post_sales = api.model("post_sales", {
        "product_name": fields.String(required=True,description="sales product_name", example='This is my first product.'),
        "product_quantity": fields.String(required=True,description="sales product_quantity", example='This is my first quantity.')
    }
)

product_parser = reqparse.RequestParser()
product_parser.add_argument('product_name', required=True, type=str, help='product_name should be a string')
product_parser.add_argument('product_quantity', required=True, type=str, help='product_quantity should be a string')

update_product_parser = reqparse.RequestParser()
update_product_parser.add_argument('product_name', required=True, type=str, help='product_name should be a string')
update_product_parser.add_argument('product_quantity', required=True, type=str, help='product_quantity should be a string')