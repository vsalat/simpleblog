# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextAreaField, FileField, HiddenField, BooleanField
from wtforms_html5 import TextField, SearchField, URLField, EmailField, TelField, IntegerField,IntegerRangeField, DecimalField
from wtforms.validators import Required

###  http://stackoverflow.com/questions/11309779/wtforms-add-a-class-to-a-form-dynamically
###  https://wtforms.readthedocs.io/en/latest/widgets.html?highlight=class_#custom-widgets

# class FormDynamicClass(object):
#     def __init__(self, *args, **kwargs):
#         super(FormDynamicClass, self).__init__(*args, **kwargs)
#         self.error_class='has-warning'
#         self.success_class='has-success'
#     def __call__(self,field,**kwargs):
#         if field.errors:
#             c = kwargs.pop('class', '') or kwargs.pop('class_', '')
#             kwargs['class'] = u'%s %s' % (field.short_name, c)
#         elif: len(field.data) > 0:

#         return super(FormDynamicClass, self).__call__(field, **kwargs)


class EditPost(Form):
    name = TextField('name')
    content = TextAreaField('content')
    precontent = TextAreaField('precontent')
    imgfield = FileField('imgfield')
    img = HiddenField('img')
    tags = TextField('tags')
    published = BooleanField('published',default=False)

class TestForm(Form):
    name = TextField('Имя',validators=[Required()])