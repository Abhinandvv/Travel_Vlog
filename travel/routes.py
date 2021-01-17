import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from travel import app, db, bcrypt
from travel.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, UpdateForm
from travel.models import User, Post, Gallery
from flask_login import login_user, current_user, logout_user, login_required

# home and login route
@app.route('/', methods=['GET', 'POST'])
def home():
    lform = LoginForm()
    posts = Post.query.all()
    gallery = Gallery.query.all()
    if lform.validate_on_submit():
        user = User.query.filter_by(email=lform.email.data).first()
        if user and bcrypt.check_password_hash(user.password, lform.password.data):
            login_user(user, remember=lform.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessfull. Please check email and password', 'danger') 
    return render_template('index1.html', title='Home', lform=lform, posts=posts, gallery=gallery) 
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
"""
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
"""

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img/profilepic', picture_fn)
    form_picture.save(picture_path)
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
        if form.picture2.data:
            img_file2 = save_picture(form.picture2.data)
            img2 = img_file2
        else:
            img2 = "null"
        if form.picture3.data:
            img_file3 = save_picture(form.picture3.data)
            img3 = img_file3
        else:
            img3 = "null"
        if form.picture4.data:
            img_file4 = save_picture(form.picture4.data)
            img4 = img_file4
        else:
            img4 = "null"
        post = Post(title=form.title.data, place=form.place.data, content=form.content.data, content2=form.content2.data, content3=form.content3.data, content4=form.content4.data, image_file=img, image_file2=img2, image_file3=img3, image_file4=img4, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your Post hase been created!', 'success')
        return redirect(url_for('home'))
    return render_template('addstory.html', title='New Story', lform=lform, form=form)
@app.route('/post/<int:post_id>')
def post(post_id):
    lform = LoginForm()
    post = Post.query.get_or_404(post_id)
    user = User.query.filter_by(id=post.user_id).first()
    return render_template('single.html', title=post.title, post=post, lform=lform, user=user)
@app.route('/post/<int:post_id>/update',  methods=['GET', 'POST'])
def update_post(post_id):
    lform = LoginForm()
    current_post = Post.query.filter_by(id=post_id).first()
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            try:
                os.unlink(os.path.join(app.root_path, 'static/img/profilepic', current_post.image_file))
                img_file = save_picture(form.picture.data)
                current_post.image_file = img_file
            except:
                img_file = save_picture(form.picture.data)
                current_post.image_file = img_file
        if form.picture2.data:
            try:
                os.unlink(os.path.join(app.root_path, 'static/img/profilepic', current_post.image_file2))
                img_file2 = save_picture(form.picture2.data)
                current_post.image_file2 = img_file2
            except:
                img_file2 = save_picture(form.picture2.data)
                current_post.image_file2 = img_file2
        if form.picture3.data:
            try:
                os.unlink(os.path.join(app.root_path, 'static/img/profilepic', current_post.image_file3))
                img_file3 = save_picture(form.picture3.data)
                current_post.image_file3 = img_file3
            except:
                img_file3 = save_picture(form.picture3.data)
                current_post.image_file3 = img_file3
        if form.picture4.data:
            try:
                os.unlink(os.path.join(app.root_path, 'static/img/profilepic', current_post.image_file4))
                img_file4 = save_picture(form.picture4.data)
                current_post.image_file4 = img_file4
            except:
                img_file4 = save_picture(form.picture4.data)
                current_post.image_file4 = img_file4
        post.title = form.title.data
        post.content = form.content.data
        post.content2 = form.content2.data
        post.content3 = form.content3.data
        post.content4 = form.content4.data
        db.session.commit()
        flash('Your story has been updated', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.content3.data = post.content3
        form.content2.data = post.content2
        form.content4.data = post.content4
        form.picture.data = post.image_file
        form.picture2.data = post.image_file2
        form.picture3.data = post.image_file3
        form.picture4.data = post.image_file4
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
    return redirect(url_for('account', post=post ))

# search
@app.route('/search', methods=['POST'])
def search():
    lform = LoginForm()
    place = request.form['search_place']
    posts = Post.query.filter_by(place=place).all()
    return render_template('search.html', title='Search result', lform=lform, posts=posts, place=place)
@app.route('/gallery/<string:district>', methods=['GET', 'POST'])
def gallery_by_district(district):
    lform = LoginForm()
    gallery = Gallery.query.filter_by(district=district).all()
    return render_template('gallery.html', gallery=gallery, lform=lform)