from flask import Flask,url_for,render_template,redirect,request,g
import sqlite3
from model import User

app=Flask(__name__)
app.config['DATABASE']='database.db'

def connect_db():
    """Connects to the specific database."""
    db = sqlite3.connect(app.config['DATABASE'])
    return db

def init_db():
    with app.app_context():
        db = connect_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def insert_user_to_db(user):
    sql_insert='insert into users (name, pwd, email, age, birthday, face) values (?, ?, ?, ?, ?, ?, ?)'
    args=[user.name,user.pwd,user.email,user.age,user.birthday,user.face]
    g.db.execute(sql_insert,args)
    g.db.commit()

def query_users_from_db():
    users=[]
    sql_select='SELECT * FROM users'
    args=[]
    cur=g.db.execute(sql_select,args)
    for item in cur.fetchall():
        print(item)
    return users

@app.before_request
def before_request():
    # print('before_request()')
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    # print('teardown_request(exception)')
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/',methods=['GET','POST'])
def user_login():
    users = query_users_from_db()
    for user in users:
        print(user.name,user.email)
    return render_template('user_login.html')

@app.route('/regist/',methods=['GET','POST'])
def user_regist():
    if request.method == 'POST':
        user=User()
        user.name=request.form.get('user_name')
        user.pwd = request.form.get('user_pwd')
        user.email = request.form.get('user_email')
        user.age = request.form.get('user_age')
        user.birthday = request.form.get('user_birthday')
        user.face = request.form.get('user_face')
        print(user.email)
        insert_user_to_db(user)

        return redirect(url_for('user_login',username=user.name))
    return render_template('user_regist.html')

if __name__ == '__main__':
    app.run()
