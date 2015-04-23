import os
from flask import Flask, session, render_template, redirect,\
Response, url_for, request, jsonify

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from model import Base, Category, Item, FUser

import jinja2 

from flask_wtf.csrf import CsrfProtect

from datetime import datetime

from flask.ext.login import LoginManager, UserMixin,\
 login_user, logout_user, current_user

from dicttoxml import dicttoxml

import json

from FacebookSignUp import FacebookSignUp

from upload_image import upload_image

app = Flask(__name__)

# Run Flask_WTF's CRSFProtect
CsrfProtect(app)
WTF_CSRF_SECRET_KEY = "uuuuuuuuuuuuuuu"

# This secret is used for Flask's session
app.secret_key= "uuuuuuuuuuuuuuu"

# Initialize and connect database by SQLAlchemy
CURRENT_PATH = os.getcwd()
engine = create_engine('postgresql://catalog:cataword@localhost/catalog')
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# initialize the Login Manager of Flask-Login
LoginManager = LoginManager(app)


# Login session
@LoginManager.user_loader
def load_user(id):
	"""Load user in User by id"""
	return session.query(FUser).get(int(id))

@app.route('/logout')
def logout():
	"""Logout and redirect to home page"""
	logout_user()
	return redirect("/")

@app.route('/login')
def oauthAuthorize():
	"""Pass parameter to facebook authorize page, and pass the feedback
	to callback function. Parameter and URLs are store in FacebookSignUp.py"""
	if not current_user.is_anonymous():
		return redirect("/")
	gofacebook=FacebookSignUp()
	return gofacebook.authorize()

@app.route('/callback')
def oauthCallback():
	"""Handle the data send back by facebook."""
	# Check if login alwaydy, if yes, redirect to home page
	if not current_user.is_anonymous():
		return redirect("/")

	oauth=FacebookSignUp()
	social_id, email=oauth.callback()
	# If face book send nothing back, redirect to home page
	if social_id is None:
		flash("Authentication failed.")
		return redirect("/")

	# Check if the user already signup in our database
	try:
		user = session.query(FUser).filter_by(social_id=str(social_id)).one()
	except:
		user = None
	# If user is not in database, put it in
	if not user:
		user = FUser(social_id=str(social_id), email=email)
		session.add(user)
		session.commit()
	# Get the user login
	login_user(user, True)
	return redirect("/")


# Initialize template environment
env = jinja2.Environment(loader=jinja2.PackageLoader('catalog', 'templates'))


@app.route('/', methods=['GET', 'POST'])
def showAll():
	"""This page will show all items, order by adding time"""
	login_already = current_user.is_authenticated()
	i = session.query(Item).order_by(desc(Item.create_time)).all()
	c = session.query(Category).all()
	return render_template("home.html", c=c, items=i, login_already=login_already)


def vacant_input(*disable_variable):
	"""This function is created to check if there is any empty imput 
	for page /add and /edit.
	Args:
		*disable_varialbe(str): input the form name, and function will skip it.
	"""
	var = ["name", "discription", "photo", "category"]
	for v in disable_variable:
		var.remove(v)
	error = {}
	def add_error(var):
		for i in var:
			if i!="photo":
				if not request.form[i]:
					error[i] = True
			else:
				if not request.files[i]:
					error[i] = True
		return error


@app.route('/add', methods=['GET', 'POST'])
def newItem():
	"""This page will be for adding a new item."""
	error=None
	login_already=current_user.is_authenticated()
	#   This function will return to homepage if it found user is not login. 
	#  	There are same setting in pages below which are able to edit the database. 
	if login_already:
		if request.method == "POST":
			error = vacant_input()
			if not error:
				"""go on input database if no empty imput. If there any, 
				   reload and labels of the empty form will turn red."""
				time_now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				""" Get currunt time and insert to create_time. 
				 	This will use for index items display order"""
				i = Item(create_time=time_now, 
						 name=request.form['name'], 
						 discription=request.form['discription'], 
						 category=request.form['category'])
				session.add(i)
				session.flush()
				i.photo=upload_image(i.id)
				session.commit()
				return redirect("/")
			c = session.query(Category).all()
			return render_template("add.html", c=c, login_already=login_already, error=error)
		c = session.query(Category).all()
		return render_template("add.html", c=c, login_already=login_already, error=error)
	else:
		return redirect("/")

@app.route('/catalog/<category>/items', methods=['GET', 'POST'])
def showcategoryItem(category):
	"""This page will be for showing all items in the category"""
	login_already=current_user.is_authenticated()
	# Get all items in the selected category 
	i = session.query(Item).filter_by(category=category).order_by(desc(Item.create_time)).all()
	c = session.query(Category).all()
	return render_template("home.html", c=c, items=i, login_already=login_already)

@app.route('/item/<item>', methods=['GET', 'POST'])
def showItem(item):
	"""This page will be for showing the selected item"""
	login_already=current_user.is_authenticated()
	i = session.query(Item).filter_by(id=item).one()
	c = session.query(Category).all()
	return render_template("item.html", c=c, item=i, login_already=login_already)

@app.route('/<item>/edit', methods=['GET', 'POST'])
def editItem(item):
	"""This page will be for editing the selected item"""
	error=None
	login_already=current_user.is_authenticated()
	if login_already:
		i = session.query(Item).filter_by(id=item).one()
		if request.method == "POST":
			"""Update the infomation of the item. Item's id is used for index the url.
			   And it won't change."""
			error=vacant_input("photo")
			# Check if there is any empty input except photo.
			if not error:
				# go on input database if no empty imput. If there any, 
				# reload and labels of the empty form will turn red.
				i.name= request.form['name']
				i.discription= request.form['discription']
				i.category= request.form['category']
				if request.files['photo']:
					i.photo=upload_image(i.id)
					# the photo file will not be change if no file upload.
				session.add(i)
				session.commit()
				return redirect("/item/%s" %item)
			c = session.query(Category).all()
			return render_template("add.html", c=c, login_already=login_already, error=error)
		i=session.query(Item).filter_by(id=item).one()
		c=session.query(Category).all()
		return render_template("edit.html", c=c, item=i, login_already=login_already, error=error)
	else:
		return redirect("/")

@app.route('/<item>/delete', methods=['GET','POST'])
def deleteItem(item):
	"""This page will be for deleting the selected item"""
	login_already=current_user.is_authenticated()
	if login_already:
		if request.method == "POST":
			# This post request is submited automatically in delete.html for csrf protection.
			if request.form['delete_it'] == "yes":
				i = session.query(Item).filter_by(id=item).one()
				session.delete(i)
				session.commit()
				return redirect("/")
		return render_template("delete.html")
	else:
		return redirect("/")

@app.route('/newcategory', methods=['GET', 'POST'])
def newCategory():
	"""This page will be for create a new category"""
	login_already=current_user.is_authenticated()
	if login_already:
		if request.method=='POST':
			i = Category(name=request.form['name'])
			session.add(i)
			session.commit()
			return redirect("/")
		c=session.query(Category).all()
		return render_template("newcategory.html", c=c, login_already=login_already)
	else:
		return redirect("/")

# the JSON session 

@app.route('/JSON')
def categoryItemJSON():
	"""This page will be for showing all items in the category in JSON"""
	c = session.query(Category).all()
	return jsonify(Caregory=[i.serialize for i in c])

@app.route('/item/<item>/JSON')
def showItemJSON(item):
	"""This page will be for showing the selected item in JSON"""
	i = session.query(Item).filter_by(id=item).one()
	return jsonify(i.serialize)

@app.route('/catalog/<category>/items/JSON')
def showCategoryItemJSON(category):
	"""This page will be for showing all items in the category in JSON"""
	i = session.query(Item).filter_by(category=category).order_by(desc(Item.create_time)).all()
	return jsonify(Category=[item.serialize for item in i])

# the XML session

@app.route('/XML', methods=['GET', 'POST'])
def categoryItemXML():
	"""This page will be for showing all items in the category in XML"""
	c = session.query(Category).all()
	data = {}
	for i in c:
		data[i.name] = i.serialize
	xml = dicttoxml(data)
	return xml

@app.route('/catalog/<category>/items/XML')
def showCategoryItemXML(category):
	"""This page will be for showing all items in the category in XML"""
	i = session.query(Item).filter_by(category=category).\
	order_by(desc(Item.create_time)).all()
	data = {}
	for item in i:
		data[item.name] = item.serialize
	xml = dicttoxml(data)
	return xml

@app.route('/item/<item>/XML')
def showItemXML(item):
	"""This page will be for showing the selected item in XML"""
	i = session.query(Item).filter_by(id=item).one()
	xml = dicttoxml(i.serialize)
	return xml



# run the app by "python catalog.py". False debug before put it online.
if __name__ == "__main__":
    app.run(debug=True)
