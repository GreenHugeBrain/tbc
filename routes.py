from fileinput import filename
from ntpath import join
from os import path
from flask import flash, render_template, redirect, url_for
from ext import app, db
from forms import AddCommentForm, AddProduct, EditProductForm, RegisterForm, LoginForm
from werkzeug.utils import secure_filename
from models import Comment, Product, User
from flask_login import login_required, login_user, logout_user, current_user

@app.route('/', methods=['POST', 'GET'])
def home():

    return render_template("index.html")


@app.route('/product1', methods=['POST', 'GET'])
def product():
    form = AddProduct()

    products = Product.query.limit(12).all()

    return render_template("productpage.html", form=form, products=products)


@app.route('/feedback', methods=['POST', 'GET'])
def Feedback():
    form = AddCommentForm()
    comments = Comment.query.all()

    products = Product.query.all()

    if form.validate_on_submit():
        new_comment = Comment(name=form.name.data, comment=form.comment.data)
        new_comment.create()
        return redirect('/feedback')

    return render_template("feedback.html", form=form, comments=comments, products=products)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()

        if existing_user:
            flash('Username already exists. Please choose a different username.', 'danger')
        else:
                new_user = User(username=form.username.data, password=form.password.data)
                new_user.create()
                return redirect('/login')

    return render_template('registration.html', form=form)


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        login_user(user)
        return redirect('/')
    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/admindashboard', methods=['POST', 'GET'])
@login_required
def admindashboard():
    if 'admin' in current_user.role:  
        form = AddProduct()
        
        products = Product.query.all()
        if form.validate_on_submit():
            new_product = Product(name=form.name.data, img=form.img.data.filename)
            new_product.create()

            file_dir = path.join(app.root_path, "static", form.img.data.filename)
            form.img.data.save(file_dir)
            
            return redirect("/admindashboard")
            
        return render_template('admindashboard.html', form=form, products=products)
    else:
        return redirect('/')

        
@app.route('/editproduct/<int:index>', methods=['POST', 'GET'])
def edit_product(index):
    product = Product.query.get(index)

    if product:
        form = EditProductForm()
        if form.validate_on_submit():
            product.name = form.name.data

            if form.img.data:
                filename = secure_filename(form.img.data.filename)
                product.img = filename

                file_dir = join(app.root_path, "static", filename)
                form.img.data.save(file_dir)

            db.session.commit()
            return redirect("/admindashboard")

        form.name.data = product.name

        return render_template('admindashboard.html', form=form)
    else:
        return redirect('/admindashboard')
        
@app.route('/removeproduct/<int:index>', methods=['POST', 'DELETE'])
@login_required
def remove_product(index):
    product = Product.query.get(index)

    if product:
        product.delete()
    else:
        flash('You do not have permission to access the admin dashboard.', 'danger')

    return redirect("/admindashboard")