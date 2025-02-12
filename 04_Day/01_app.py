from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login')
def login():
    return render_template('auth/login.html')

@app.route('/register')
def ragister():
    return render_template('auth./ragister.html')

@app.route('/cart.html')
def cart():
    return render_template('cart.html')

@app.route('/store.html')
def store():
    return render_template('store.html')

@app.route('/product-detail.html')
def productdetail():
    return render_template('product-detail.html')

@app.route('/place-order.html')
def placeorder():
    return render_template('place-order.html')

if __name__ == "__main__":
    app.run(debug=True)
