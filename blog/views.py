# -*- coding: utf-8 -*-
from blog import blog,db,models
from flask import render_template, request, url_for, abort, send_from_directory
from pagination import Pagination
from sqlalchemy import desc
from math import ceil

@blog.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@blog.route('/')
@blog.route('/page/<int:pg>')
def main(pg=1):
    def url_for_other_page(page):
        args = request.view_args.copy()
        args['pg'] = page
        return url_for(request.endpoint, **args)
    blog.jinja_env.globals['url_for_other_page'] = url_for_other_page
    count = models.Posts.query.filter_by(published=True).count()
    PER_PAGE=10
    posts = models.Posts.query.filter_by(published=True).order_by(desc(models.Posts.id)).offset((pg-1)*PER_PAGE).limit(PER_PAGE).all()
    pagination = Pagination(pg, PER_PAGE, count)
    breadcrumb = [{'active':True,'name':'Блог','href':'/'}]
    if pg > 1:
        breadcrumb[0]['active']=False
        breadcrumb.append({'active':True,'name':'Страница '+str(pg),'href':'/page/'+str(pg)})
    return render_template('blog.html',pagination=pagination,posts = posts)

@blog.route('/tags/<string:tagname>')
@blog.route('/tags/<string:tagname>/<int:pg>')
def showtag(tagname,pg=1):
    def url_for_other_page(page):
        args = request.view_args.copy()
        args['pg'] = page
        return url_for(request.endpoint, **args)
    blog.jinja_env.globals['url_for_other_page'] = url_for_other_page
    tag = models.Tags.query.filter_by(name=tagname).join(models.Posts.tags).filter(models.Posts.published).first()
    if tag:
        count = len(tag.posts)
        PER_PAGE = 10
        pagination = Pagination(pg, PER_PAGE, count)
        posts = tag.posts.filter(published=True)[(pg-1)*PER_PAGE:(pg-1)*PER_PAGE+PER_PAGE]
        breadcrumb = [{'active':False,'name':'Блог','href':'/'},{'active':True,'name':'Поиск по тегу "'+tag.name+'"','href':'/tags/'+tag.name}]
        if pg > 1:
            breadcrumb[1]['active']=False
            breadcrumb.append({'active':True,'name':'Страница '+str(pg),'href':'/tags/'+tag.name+'/'+str(pg)})
        return render_template('blog.html',pagination=pagination,posts=posts,name='Поиск по тегу "'+tag.name+'"',breadcrumb=breadcrumb)
    else:
        abort(404)


@blog.route('/post/<int:id>')
def post(id):
    post = models.Posts.query.filter_by(id=id,published=True).first()
    if post:
        breadcrumb=[{'active':False,'name':'Блог', 'href':'/'},{'active':True,'name':post.name,'url':'/post/'+str(id)}]
        return render_template('post.html',post=post, breadcrumb=breadcrumb)
    else:
        abort(404)


@blog.route('/storage/<path:path>')
def storage(path):
    return send_from_directory(blog.config['STORAGE_FOLDER'],path)

@blog.route('/search')
@blog.route('/search/<int:pg>')
def search(pg=1):
    def url_for_other_page(page):
        args = request.view_args.copy()
        args['pg'] = page
        return url_for(request.endpoint, **args)
    blog.jinja_env.globals['url_for_other_page'] = url_for_other_page
    count = len(models.Posts.query.filter_by(published=True).whoosh_search(request.args['srch-term'],or_=True,like=True).all())
    PER_PAGE = 10
    pagination = Pagination(pg, PER_PAGE, count)
    posts = models.Posts.query.filter_by(published=True).whoosh_search(request.args['srch-term'],or_=True,like=True).order_by(desc(models.Posts.id)).offset((pg-1)*PER_PAGE).limit(PER_PAGE).all()
    return render_template('search.html',pagination=pagination,posts=posts,name='Поиск:  "'+request.args['srch-term']+'"')
