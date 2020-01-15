#coding:utf-8
import MySQLdb
import json
from flask import (Flask, abort, flash, g, redirect, render_template, request,
                   url_for,session)

#打开数据库
DATABASE = 'booker'
DB_HOST = '127.0.0.1'
USERNAME = 'root'
PASSWORD = '12345678'

#gdb = MySQLdb.connect("127.0.0.1", "root", "12345678", "booker", charset='utf8' )

#创建应用
app = Flask(__name__)
app.secret_key = b'ss*(^(*}/))'
#app.config.from_object(__name__)

def connect_db():
    db = MySQLdb.connect("127.0.0.1", "root", "12345678", "booker", charset='utf8' )
    return db

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(Exception):
    g.db.close()

@app.route('/')
def show_ent():
    cur = g.db.cursor()
    cur.execute("select * from entries")
    entries = [dict(title=row[1],cont=row[2]) for row in cur.fetchall()]
    #entries = json.dumps(entries, encoding="UTF-8", ensure_ascii=False)
    #str(entries).decode('unicode_escape')
    return render_template('show_entries.html',entries=entries)

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'haizhi' or request.form['password'] != 'haizhi':
            error = '账号或密码错误！'
            return render_template('login.html',error=error)
        else:
            session['logged_in'] = True
            flash('登录成功')
            return redirect(url_for('show_ent'))
    return render_template('login.html',error=error)

@app.route('/add',methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.cursor().execute('insert into entries (title,text) values (%s,%s)',(request.form['title'],request.form['text']))
    g.db.commit()
    flash('添加成功')
    return redirect(url_for('show_ent'))

@app.route('/loginout')
def logout():
    session.pop('logged_in',None)
    flash('登出成功')
    return redirect(url_for('show_ent'))

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
