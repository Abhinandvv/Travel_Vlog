import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from travel import app, db, bcrypt
from travel.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from travel.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(app, name='admin', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# home and login route
@app.route('/', methods=['GET', 'POST'])
def home():
    lform = LoginForm()
    posts = Post.query.all()
    if lform.validate_on_submit():
        user = User.query.filter_by(email=lform.email.data).first()
        if user and bcrypt.check_password_hash(user.password, lform.password.data):
            login_user(user, remember=lform.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessfull. Please check email and password', 'danger') 
    return render_template('index1.html', title='Home', lform=lform, posts=posts) 
# sign up route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    lform = LoginForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created For {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('Signup.html', title='Signup', form=form, lform=lform)
# logout route
@app.route('/logout')
def logout():
     logout_user()
     return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img/profilepic', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def account():
    lform = LoginForm()
    form =  UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Acoount has been Updated...', 'success')
        return redirect(url_for('account'))
    elif  request.method =='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='img/profilepic/' + current_user.image_file)
    post = Post.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', title='Profile', lform=lform, image_file=image_file, form=form, post=post)
@app.route('/post/new',  methods=['GET', 'POST'])
@login_required
def addstory():
    lform = LoginForm()
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            img_file = save_picture(form.picture.data)
            img = img_file
        post = Post(title=form.title.data, content=form.content.data, image_file=img, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your Post hase been created!', 'success')
        return redirect(url_for('home'))
    return render_template('addstory.html', title='New Story', lform=lform, form=form)
@app.route('/post/<int:post_id>')
def post(post_id):
    lform = LoginForm()
    post = Post.query.get_or_404(post_id)
    return render_template('single-blog.html', title=post.title, post=post, lform=lform)
@app.route('/post/<int:post_id>/update',  methods=['GET', 'POST'])
def update_post(post_id):
    lform = LoginForm()
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = post.content
        db.session.commit()
        flash('Your story has been updated', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('updatestory.html', title='Update Story', lform=lform, form=form, post=post)
@app.route('/post/<int:post_id>/delete',  methods=['POST'])
@login_required
def delete_post(post_id):
    lform = LoginForm()
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your story has been deleted', 'success')
    return redirect(url_for('account', post=post))
