# third-party imports
from flask_restplus import Resource

# local imports
from ..utils.sdto import api, products, post_products, product_parser, update_product_parser
from ..utils.decorators import token_required
from ..utils.validators import validate_product_data, validate_update_product
from ..models.sale import Sale
from app.database import Database


conn = Database()
cursor = conn.cursor
dict_cursor = conn.dict_cursor

@api.route("/products")
class ProductList(Resource):
    """Displays a list of all products and lets you POST to add new products."""

    @api.expect(post_products)
    @api.doc('adds an product')
    @api.response(201, "Created")
    @token_required
    @api.doc(security='apikey')
    @api.header('x-access-token', type=str, description='access token')
    def post(user_id, self):
        """Creates a new Product."""
        args = product_parser.parse_args()

        # validate the product payload
        invalid_data = validate_product_data(args)
        if invalid_data:
            return invalid_data

        product_name = args["product_name"]
        product_quantity = args["product_quantity"]
        Product.add_product(cursor, product_name, product_quantity, user_id)
        return {"message": "Product added successfully"}, 201

    @api.doc("list_products")
    @api.response(404, "Products Not Found")
    @api.marshal_list_with(products, envelope="products")
    @token_required
    @api.doc(security='apikey')
    @api.header('x-access-token', type=str, description='access token')
    def get(user_id, self):
        """List all Products"""
        products = Product.get_all(dict_cursor, user_id)
        if not products:
            api.abort(404, "No products for user {}".format(user_id))
        return products

@api.route("/products/<int:productId>")
@api.param("productId", "product identifier")
@api.response(404, 'Product not found')
class ProductClass(Resource):
    """Displays a single product item and lets you delete them."""

    @api.marshal_with(products)
    @api.doc('get one product')
    @token_required
    @api.doc(security='apikey')
    @api.header('x-access-token', type=str, description='access token')
    def get(user_id, self, productId):
        """Displays a single Product."""
        product = Product.get_product_by_id(dict_cursor, productId)
        if product["user_id"] != str(user_id):
            api.abort(401, "Unauthorized to view this product")
        return product


    @api.doc('updates an product')
    @api.expect(post_products)
    @token_required
    @api.doc(security='apikey')
    @api.header('x-access-token', type=str, description='access token')
    def put(user_id, self, productId):
        """Updates a single Product."""
        args = update_product_parser.parse_args()
        product_name = args["product_name"]
        product_quantity = args["product_quantity"]
        product = {"product_name": product_name, "product_quantity":product_quantity}
        product = Product.get_product_by_id(dict_cursor, productId)

        invalid_data = validate_update_product(product, args)

        if invalid_data:
            return invalid_data
        
        Product.modify_product(dict_cursor, cursor, args["product_name"], args["product_quantity"], productId, user_id)
        return {"message": "Updated successfully", "product":product}

    @api.doc('deletes an product')
    @api.response(204, 'Product Deleted')
    @token_required
    @api.doc(security='apikey')
    @api.header('x-access-token', type=str, description='access token')
    def delete(user_id, self, productId):
        """Deletes a single Product."""

        Product.delete_product(dict_cursor, cursor, productId, user_id)
        return {"message": "Product deleted successully"}, 200