from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2


app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site""" 
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    

    if "cart" not in session:
        flash("Your cart is empty.")
        return redirect(url_for("list_melons"))

    full_cart = {}
    cart_total = 0
    """ take melon_id and qty from session and build line to send to table in list melons"""
    for item in session["cart"]:
        melon_id = item[0]
        melon = model.get_melon_by_id(melon_id)
        melon.qty = item[1]
        full_cart[melon_id] = melon
        cart_total += melon.price * melon.qty

    return render_template("cart.html", full_cart = full_cart, total="$%.2f"%cart_total)
    
@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """cart is the melon id and qty""" 

    if "cart" not in session:
        session["cart"] = []
    melon_id = id    
    found = False
    """ if the melon is in the cart or clicked on more than once, increment qty"""
    for melon in session["cart"]:
        if melon[0] == id:
            melon[1] += 1
            found = True
     """ if they haven't added anything to the cart, set up a blank cart. """
    if not found:
        session["cart"].append([melon_id, 1])
    flash("Successfully added to cart")
    return redirect(url_for('shopping_cart'))


@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """user enters email ,used to look up customer in DB."""
    form_email = request.form['email']
    """setting variable customer object to result of calling get_customer_by_email method from model"""
    customer = model.get_customer_by_email(form_email)
    if customer:
        """setting session to customer givenname to be used on base.html"""
        session["cust"] = customer.givenname
        flash("Login successful.  Welcome back!")
        return redirect("/melons")
    else:
        flash("No such email in our customer database. Please re-enter.")
        return redirect("/login")

@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

if __name__ == "__main__":
    app.run(debug=True)
