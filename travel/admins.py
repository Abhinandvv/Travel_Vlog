from flask_admin import Admin
from travel import app, db, file_path
from flask import render_template, url_for, request, redirect, session, flash, redirect, Blueprint, abort
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import form
from flask_admin.contrib import sqla
from travel.models import User, Post, Gallery, Feedback
from flask_admin.menu import MenuLink
from jinja2 import Markup


app.config['FLASK_ADMIN_SWATCH'] = 'slate'

admin = Admin(app, name='Admin', template_mode='bootstrap3')

class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)

@app.route("/adminlogout")
def adminlogout():
    session.clear()
    return redirect("/adminlogin")

@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == "POST":
        if request.form.get("username") == "admin" and request.form.get("password") == "password":
            session['logged_in'] = True
            return redirect("/admin")
        else:
            return render_template("adminlogin.html", failed=True)
    return render_template("adminlogin.html")

class UserView(ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.image_file:
            return ''

        return Markup(
            '<img src="%s" style="height:50px; width:50px;">' %
            url_for('static',
                    filename='img/profilepic/'+model.image_file)
        )

    column_formatters = {
        'image_file': _list_thumbnail
    }
    
    form_extra_fields = {
        'image_file': form.ImageUploadField('Image', base_path = file_path, thumbnail_size=(100, 100, True))
    }

    column_exclude_list = ['password']
    form_excluded_columns = ['posts']

class PostView(ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.image_file:
            return ''

        return Markup(
            '<img src="%s" style="height:50px; width:50px;">' %
            url_for('static',
                    filename='img/profilepic/'+model.image_file)
        )
    def _list_thumbnail2(view, context, model, name):
        if not model.image_file2:
            return ''

        return Markup(
            '<img src="%s" style="height:50px; width:50px;">' %
            url_for('static',
                    filename='img/profilepic/'+model.image_file2)
        )
    def _list_thumbnail3(view, context, model, name):
        if not model.image_file3:
            return ''

        return Markup(
            '<img src="%s" style="height:50px; width:50px;">' %
            url_for('static',
                    filename='img/profilepic/'+model.image_file3)
        )
    def _list_thumbnail4(view, context, model, name):
        if not model.image_file4:
            return ''

        return Markup(
            '<img src="%s" style="height:50px; width:50px;">' %
            url_for('static',
                    filename='img/profilepic/'+model.image_file4)
        )
    column_formatters = {
        'image_file': _list_thumbnail,
        'image_file2': _list_thumbnail2,
        'image_file3': _list_thumbnail3,
        'image_file4': _list_thumbnail4
    }
    
    form_extra_fields = {
        'image_file': form.ImageUploadField('Image 1', base_path = file_path, thumbnail_size=(100, 100, True)),
        'image_file2': form.ImageUploadField('Image 2', base_path = file_path, thumbnail_size=(100, 100, True)),
        'image_file3': form.ImageUploadField('Image 3', base_path = file_path, thumbnail_size=(100, 100, True)),
        'image_file4': form.ImageUploadField('Image 4', base_path = file_path, thumbnail_size=(100, 100, True))

    }

class GalleryView(ModelView):
    form_choices = {
        'district': [
                        ("",'-- choose district --'),
                        ('Kasaragod','Kasaragod'), ('Kannur','Kannur'),
                        ('Wayanad','wayanad'), ('Kozhikode','Kozhikode'),
                        ('Malappuram','Malappuram'), ('Palakkad','Palakkad'),
                        ('Thrissur','Thrissur'), ('Ernakulam','Ernakulam'),
                        ('Idukki','Idukki'), ('Kottayam','Kottayam'),
                        ('Alappuzha','Alappuzha'), ('Pathanamthitta','Pathanamthitta'),
                        ('Kollam','Kollam'), ('Thiruvananthapuram','Thiruvananthapuram')
                    ]

    }
    def _list_thumbnail(view, context, model, name):
        if not model.image_file:
            return ''

        return Markup(
            '<img src="%s" style="height:50px; width:50px;">' %
            url_for('static',
                    filename='img/profilepic/'+model.image_file)
        )
        
    column_formatters = {
        'image_file': _list_thumbnail
    }
    
    form_extra_fields = {
        'image_file': form.ImageUploadField('Image', base_path = file_path, thumbnail_size=(100, 100, True))
    }

logout_link = MenuLink('Logout','/adminlogout','adminlogout')
admin.add_link(logout_link)
admin.add_view(UserView(User,db.session))
admin.add_view(PostView(Post,db.session))   
admin.add_view(GalleryView(Gallery,db.session))
admin.add_view(ModelView(Feedback,db.session))
# admin.add_link(MenuLink(name='Public Website', category=''))