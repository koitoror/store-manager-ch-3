from flask_restplus import Api
from flask import Blueprint

api_v2 = Blueprint('api', __name__)
from app.api.v2.utils.udto import api as auth_ns
from app.api.v2.utils.pdto import api as products_ns
from app.api.v2.utils.sdto import api as sales_ns


authorizations = {
    "apikey":{
        "type": "apiKey",
        "in": "header",
        "name": "x-access-token"
    }
}

api = Api(
    api_v2,
    title='StoreManager API :: v2',
    doc='/',
    version='2.0',
    authorizations=authorizations,
    description='StoreManager is a web application that helps store owners manage sales and product inventory records. This application is meant for use in a single store. A simple StoreManager API',
)

del api.namespaces[0]
api.add_namespace(auth_ns, path="/api/v2/auth")
api.add_namespace(products_ns, path="/api/v2")
api.add_namespace(sales_ns, path="/api/v2")
