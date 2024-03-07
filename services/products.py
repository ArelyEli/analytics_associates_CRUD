from services.helpers import is_product_in_db
from models.product import create_new_product, get_products
from services.errors import ProducAlreadyExistError
from schemas.products import Product, GetAllProductsResponse

def create_product(session, product, user):
    if is_product_in_db(session, product.name):
        raise ProducAlreadyExistError()
    
    create_new_product(session, product, user)

def get_all_products(session):
    products = get_products(session)

    products = [Product(
        id = product.id,
        name = product.name,
        description = product.description,
        price = product.price,
        stock = product.stock
    ) for product in products]

    return GetAllProductsResponse(
        products = products
    )
