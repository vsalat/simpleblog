# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, Response, abort, flash, redirect, url_for
from pagination import Pagination
from blog import db,models,admin_form,blog
from sqlalchemy import desc
import datetime,os

admin = Blueprint('admin',__name__,url_prefix='/admin_page')

def make_new_filename(name):
    FileExtension = name.split('.')[-1]
    FileName = str(datetime.datetime.now().strftime("%H%M%S%f"))+'.'+FileExtension
    return FileName

@admin.errorhandler(404)
def page_not_found(e):
    return render_template('admin/404.html'), 404

def check_auth(username, password):
    #simple logging
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'admin'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

@admin.before_request
def checkadmin():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

@admin.route('/')
@admin.route('/posts')
@admin.route('/posts/<int:pg>')
def posts(pg=1):
    def url_for_other_page(page):
        args = request.view_args.copy()
        args['pg'] = page
        return url_for(request.endpoint, **args)
    blog.jinja_env.globals['url_for_other_page'] = url_for_other_page
    count = models.Posts.query.count()
    PER_PAGE=50
    posts = models.Posts.query.order_by(desc(models.Posts.id)).offset((pg-1)*PER_PAGE).limit(PER_PAGE).all()
    pagination = Pagination(pg, PER_PAGE, count)
    return render_template('admin/posts.html',pagination=pagination,posts = posts)




@admin.route('/posts/new',methods=['GET','POST'])
def new_post():
    form = admin_form.EditPost(request.form)
    if request.method == 'GET':
        return render_template('admin/new_post.html',form=form)
    if request.method == 'POST':
        post = models.Posts()
        post.published = form.published.data
        post.name = form.name.data
        post.content = form.content.data
        post.precontent = form.precontent.data
        imgurl = ''
        img = request.files[form.imgfield.name]
        if img:
            cur_date = str(datetime.datetime.now().strftime("%d%m%y"))
            directory = blog.config['STORAGE_FOLDER']+cur_date
            if not os.path.exists(directory):
                os.makedirs(directory)
            img_filename = make_new_filename(img.filename)
            img_file = open(directory+'/'+img_filename,'w').write(img.read())
            img_filename = '/storage/'+cur_date+'/'+img_filename
            post.img = img_filename
        db.session.add(post)
        tagslist = form.tags.data
        post.tags = []
        for i in range(len(tagslist)):
            if tagslist[:-1]==' ' or tagslist[:-1]==',':
                tagslist = tagslist[:-1]
        tagslist = tagslist.replace(" ,",",")
        tagslist = tagslist.replace(", ",",")
        if len(tagslist)>0:
            if tagslist[-1] == ',':
                tagslist = tagslist[:-1]
            tagslist = tagslist.split(',')
            for  item in tagslist:
                for i in range(len(item)):
                    if item[0] == ' ':
                        item = item[1:]
                    elif item[-1] == ' ':
                        item = item[:-1]
                    else:
                        break
                tag = models.Tags.query.filter_by(name=item).first()
                if tag:
                    post.tags.append(tag)
                else:
                    tag = models.Tags(item)
                    db.session.add(tag)
                    db.session.commit()
                    post.tags.append(tag)
        db.session.commit()
        flash('Запись добавлена','success')
        return redirect(url_for('admin.posts'))



@admin.route('/posts/edit/<int:id>', methods=['GET','POST'])
def edit_post(id):
    post = models.Posts.query.get(id)
    if post:
        form = admin_form.EditPost(request.form, obj=post)
        if request.method=='GET':
            form = admin_form.EditPost(request.form, obj=post)
            tags =''
            for tag in post.tags: tags+=tag.name+', '
            form.tags.data= tags
            return render_template('admin/edit_post.html',form=form,post=post)
        elif request.method == 'POST':
            tagslist = form.tags.data
            post.tags = []
            for i in range(len(tagslist)):
                if tagslist[:-1]==' ' or tagslist[:-1]==',':
                    tagslist = tagslist[:-1]
            tagslist = tagslist.replace(" ,",",")
            tagslist = tagslist.replace(", ",",")
            if len(tagslist)>0:
                if tagslist[-1] == ',':
                    tagslist = tagslist[:-1]
                tagslist = tagslist.split(',')
                for  item in tagslist:
                    for i in range(len(item)):
                        print item
                        if item[0] == ' ':
                            item = item[1:]
                        elif item[-1] == ' ':
                            item = item[:-1]
                        else:
                            break
                    tag = models.Tags.query.filter_by(name=item).first()
                    if tag:
                        post.tags.append(tag)
                    else:
                        tag = models.Tags(item)
                        db.session.add(tag)
                        db.session.commit()
                        post.tags.append(tag)
            post.name = form.name.data
            post.published = form.published.data
            post.content = form.content.data
            post.precontent = form.precontent.data
            imgurl = ''
            if form.img.data == '':
                img = request.files[form.imgfield.name]
                if img:
                    cur_date = str(datetime.datetime.now().strftime("%d%m%y"))
                    directory = blog.config['STORAGE_FOLDER']+cur_date
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    img_filename = make_new_filename(img.filename)
                    img_file = open(directory+'/'+img_filename,'w').write(img.read())
                    img_filename = '/storage/'+cur_date+'/'+img_filename
                    post.img = img_filename
                else:
                    post.img = ''
            db.session.commit()
            flash('Сохранено','success')
            return redirect(url_for('admin.edit_post',id=post.id))

    else:
        abort(404)

@admin.route('/ckeditor_images',methods=['GET','POST'])
def ckeditor_images():
    if request.method == 'POST':
        file = request.files['upload']
        cur_date = str(datetime.datetime.now().strftime("%d%m%y"))
        directory = blog.config['STORAGE_FOLDER']+cur_date
        if not os.path.exists(directory):
                os.makedirs(directory)
        FileExtension = file.filename.split('.')[-1]
        FileName = str(datetime.datetime.now().strftime("%H%M%S%f"))+'.'+FileExtension
        file.save(os.path.join(directory,FileName))
        http_path = '/storage/'+cur_date+'/'+FileName
        callback = request.args['CKEditorFuncNum']
        error = ''
        return '<script type="text/javascript">window.parent.CKEDITOR.tools.callFunction("'+callback+'",  "'+http_path+'", "'+error+'" );</script>'


@admin.route('/test',methods=['GET','POST'])
def test():
    form = admin_form.TestForm(request.form)
    if request.method == 'GET':
        return render_template('admin/test.html',form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            import transliterate
            flash(transliterate.translit(form.name.data,'ru',reversed=True),'success')
            return render_template('admin/test.html',form=form)
        else:
            flash('Проверьте правильность заполнения полей','danger')
            return render_template('admin/test.html',form=form)
