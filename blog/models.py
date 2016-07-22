from blog import db,blog
import flask.ext.whooshalchemyplus as whooshalchemy
import datetime

relationship_table=db.Table('relationship_table',                            
	db.Column('post_id', db.Integer,db.ForeignKey('posts.id'), nullable=False),
	db.Column('tags_id',db.Integer,db.ForeignKey('tags.id'),nullable=False),
	db.PrimaryKeyConstraint('post_id', 'tags_id') )
 
class Posts(db.Model):
	__searchable__ = ['content','precontent','name']
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255),nullable=False)
	content = db.Column(db.Text)
	precontent = db.Column(db.Text)
	img = db.Column(db.String(40))
	published = db.Column(db.Boolean,default=False)
	add_date = db.Column(db.DateTime)
	tags=db.relationship('Tags', secondary=relationship_table, backref='posts')  
	def __init__(self):
		self.add_date = datetime.datetime.now()
 
class Tags(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	name=db.Column(db.String, unique=True, nullable=False)
	def __init__(self,name):
		self.name = name

whooshalchemy.whoosh_index(blog, Posts)