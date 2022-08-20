import sql

def get_prod_by_id(id):
    val = [id]
    with sql.Database(sql.db_config) as test:
        prod = test.get_row(sql.prod_by_id, val)

        print(prod)
    if prod:
        return prod
    else:
        return None


def get_user_by_email(email):
    val = [email]
    with sql.Database(sql.db_config) as test:
        user = test.get_row(sql.user_by_email, val)
    if user:
        return user
    else:
        return None


def insert_prod(prod):
    with sql.Database(sql.db_config) as test:
        prod_no = test.insert_row(sql.add_product, prod)
    return prod_no


def insert_user(email):
    print(" in insert_user")
    # val = email
    with sql.Database(sql.db_config) as test:
        user_no = test.insert_row(sql.add_user, (email,))
    return user_no


def add_users_to_prod(user_id, prod_id):
    user_prod = (user_id, prod_id)
    with sql.Database(sql.db_config) as test:
        test.insert_row(sql.user_to_prod, user_prod)
    return


def get_users_prod(user_id):
    val = [user_id]
    with sql.Database(sql.db_config) as test:
        user_products = test.get_row(sql.user_products_query, val)

    # mydb.commit()
    return user_products

