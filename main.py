from flask import Flask, request, redirect
import productService

app = Flask(__name__)



@app.route("/product/<source>/<product_id>", methods=['GET'])
def get_product(source, product_id):
    prod = productService.get_product(source, product_id)
    if prod is None:
        return "no product hes found"
    else:
        return prod


@app.route("/addproduct/<source>/<product_id>", methods=['POST'])
def add_product_to_list(source, product_id):
    email = request.args.get("email")
    if not email:
        return "Authorization is required"
    products = productService.add_product_to_list(source, product_id, email)
    if products is None:
        return "no product found"
        # return products
    return redirect(f"http://localhost:5000/getproductlist?email={email}")


@app.route("/getproductlist", methods=['Get'])
def get_user_prod_list():
    email = request.args.get("email")
    if not email:
        return "Authorization is required"
    products = productService.get_user_prod_list(email)
    if products is None:
        return "no List for this user"
    return products


if __name__ == '__main__':
    app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
