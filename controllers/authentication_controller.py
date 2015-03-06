import bottle, authentication_repository, user_repository, user
from bottle import get, view, post, error, route
from role_type import Role_Type

import seeded_data

@get('/')
@view('login')
def get_login():
	currentUser = auth_repo.get_logged_in_user()
	if currentUser is not None:
		return render_dashboard_by_role(currentUser)

	if (user_repo.get_users() is None):
		seeded_data.seed_all_data()

	return

@post('/login')
def login():
	email = bottle.request.forms.get('email')
	password = bottle.request.forms.get('password')
	users = user_repo.get_users()

	# user = filter(u.email == email and u.password == password for u in users)
	user = next((u for u in users if u.email == email and u.password == password), None)

	if user is None:
		return bottle.template('login', {'email':email, 'password':'', 'error':'Invalid username and/or password.'})

	auth_repo.login(user)
	return render_dashboard_by_role(user)

@get('/signup')
@view('signUp')
def get_signup():
	currentUser = auth_repo.get_logged_in_user()
	if (currentUser is not None):
		return render_dashboard_by_role(currentUser)

	return

@post('/signup')
def signup():
	fullName = bottle.request.forms.get('fullName')
	email = bottle.request.forms.get('email')
	password = bottle.request.forms.get('password')
	passwordCheck = bottle.request.forms.get('passwordCheck')
	users = user_repo.get_users()

	if any(u.email == email for u in users):
		return bottle.template('signUp', {'fullName':fullName, 'email':email, 'password':password, 'passwordCheck':passwordCheck, 'error':'E-mail already exists.'})

	if password != passwordCheck:
		return bottle.template('signUp', {'fullName':fullName, 'email':email, 'password':password, 'passwordCheck':passwordCheck, 'error':'Passwords do not match.'})

	newUser = user.User(email, password, fullName)
	users.append(newUser)
	user_repo.seed_users(users)
	
	auth_repo.login(newUser)
	return render_dashboard_by_role(newUser)

@get('/logout')
def logout():
	auth_repo.logout()
	return bottle.redirect('/')

def render_dashboard_by_role(user):
	if user.role == Role_Type.recruit:
		return bottle.template('dashboard_recruit', {'user':user})

	if user.role == Role_Type.recruiter:
		return bottle.template('dashboard_recruiter', {'user':user})

	if user.role == Role_Type.school:
		return bottle.template('dashboard_school', {'user':user})

	if user.role == Role_Type.admin:
		return bottle.template('dashboard_admin', {'user':user})	

	return bottle.template('dashboard_basic', {'user':user})

auth_repo = authentication_repository.Authentication_Repository()
user_repo = user_repository.User_Repository()