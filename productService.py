import requests
import repository


def get_product(source, product_id):
    prod = fetch_product(source, product_id)
    if prod is None:
        return None
    existing = repository.get_prod_by_id(product_id)
    if existing:
        return existing
    # product = (prod.product_id, prod.title, prod.price, prod.source)
    repository.insert_prod(prod)
    existing = repository.get_prod_by_id(product_id)
    return existing


def add_product_to_list(source, product_id, email):
    user = repository.get_user_by_email(email)
    print(user)
    if user is None:
        new_user_id = repository.insert_user(email)
    else:
        new_user_id = user[0]['user_id']

    prod = get_product(source, product_id)
    if prod is None:
        return None
    if not is_product_in_list(new_user_id, product_id):
        repository.add_users_to_prod(new_user_id, product_id)
    # products = repository.get_users_prod(new_user_id)
    # return  products
    return prod

    # return products_res_to_json(products)


def get_user_prod_list(email):
    user = repository.get_user_by_email(email)
    print(user)
    if user is None:
        return None
    products = repository.get_users_prod(user[0]['user_id'])
    return  products
    # return products_res_to_json(products)


def is_product_in_list(user_id, prod_id):
    user_products = repository.get_users_prod(user_id)
    if user_products is None:
        return False
    for up in user_products:
        if prod_id == up['product_id']:
            return True
        return False


def fetch_product(source, product_id):
    response_api = requests.get(f'https://ebazon-prod.herokuapp.com/ybl_assignment/{source}/{product_id}/'
                                f'yblmendip829aljfy59')
    json = response_api.json()
    if 'data' not in json:
        return None
    data = json['data']
    prod_id = str(data['source_id'])
    source = data['source']
    price = str(data['source_price'])
    title = data['title']
    product = (prod_id, title, price, source)

    return product