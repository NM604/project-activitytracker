from . import db
import datetime
from flask import Flask, g, flash, Blueprint, render_template, request, redirect, url_for, session
from flask_session import Session
from datetime import date

bp = Blueprint('plan', 'plan', url_prefix = '')



@bp.route('/')
def dashboard():
  if not session.get("username"):
    return redirect(url_for("plan.login"))
  username = session.get("username")
  conn = db.get_db()
  cursor = conn.cursor()
  cursor.execute("""select id from users where username = %s;""", (username,))
  user = cursor.fetchone()
  if not user:
    return redirect(url_for("plan.login"))
  return render_template("dashboard.html")
  
  

@bp.route('/login', methods=['POST', 'GET'])  
def login():
  conn = db.get_db()
  cursor = conn.cursor()
  status = None
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    cursor.execute("""select id from users where username = %s;""", (username,))
    user = cursor.fetchone()
    if not user:
      status = "User does not exist"
      return render_template('login.html', status = status)
    cursor.execute("""select password from users where username = %s;""", (username,))
    pw = cursor.fetchone()
    if pw[0] != password:
      status = 'Incorrect password'
    else:
      cursor.execute("""select id from users where username = %s;""", (username,))
      user = cursor.fetchone()
      userid = user[0]
      session["username"] = username
      session["userid"] = userid
      return redirect(url_for("plan.dashboard"))
  if status is not None:
    return render_template('login.html', status = status)
  else:
    return render_template('login.html')
    
    
    
    
@bp.route('/logout')
def logout():
  session["username"] = None
  session["userid"] = None
  session["password"] = None
  return redirect("/", 302)   
  
  
   
    
@bp.route('/create')
def create():
  return render_template('create.html')
  
  
  
  
@bp.route('/createuser', methods=['POST'])
def createuser():
  status = None
  username = request.form['username']
  password = request.form['password']
  conn = db.get_db()
  cur = conn.cursor()
  cur.execute("""select username from users where username = %s;""", (username,))
  n = cur.fetchone()
  if n is not None:
    flash('Username already exists')
    return redirect(url_for("plan.create"), 302)
  cur.execute("""insert into users (username, password) values (%s, %s);""", (username, password))
  conn.commit()
  return redirect('/', 302)





@bp.route('/calender')
def calender():

  conn = db.get_db()
  cursor = conn.cursor()
  oid = session.get("userid")
  fday = request.args.get("d",1)
  if int(fday)<10:
    r = str(fday)
    fday = '0'+r
  fmonth = request.args.get("m",1)
  if int(fmonth)<10:
    x = str(fmonth)
    fmonth = '0'+x
  fyear = request.args.get("y",1)
  ffdate = str(fyear)+'-'+fmonth+'-'+fday
  
  current_time = datetime.datetime.now() 
  year = current_time.year
  month = current_time.month
  day = current_time.day
  current = date.today()
  today = current.strftime("%A")
  fdate = current.strftime("%B %d")
  m = current.strftime("%m")
  
  cursor.execute("""select name from tasks where oid = %s and deadline = %s order by deadline;""", (oid, ffdate))
  listtasks = cursor.fetchall()
  
  return render_template('calender.html', year=year,month=month,day=day,today=today,fdate=fdate, m=m, listtasks=listtasks, fday=fday, fmonth=fmonth, fyear=fyear)
  
  


@bp.route('/thisday')
def thisday():
  p = []
  d = datetime.datetime.now().strftime("%Y-%m-%d")
  conn = db.get_db()
  cursor = conn.cursor()
  this_day = request.args.get("d",1)
  this_month = request.args.get("m",1)
  this_year = request.args.get("y",1)
  user_id = session.get("userid")    
  this_date = str(this_year)+'-'+this_month+'-'+this_day
  cursor.execute("""select id, name, description, shopping from tasks where oid = %s and deadline = %s;""", (user_id, this_date))
  info = cursor.fetchall()
  cursor.execute("""select item, qty, tid from shoppinglist where deadline = %s;""", (this_date,))
  listshopping = cursor.fetchall()
  return render_template('thisday.html', info=info, listshopping=listshopping)
  
  
  
  
@bp.route('/addtask')
def add_task():
  return render_template('add_task.html')


 
@bp.route('/addtaskdetails', methods=['POST', 'GET'])
def add_taskdetails():
  if request.method == 'POST':
    name = request.form['name']
    description = request.form['description']
    deadline = request.form['deadline']
    shopping_status = request.form.get('shopping_status')
    oid = session.get("userid")
    d = datetime.datetime.now().strftime("%Y-%m-%d")
    conn = db.get_db()
    cursor = conn.cursor()
    
    if shopping_status is None:
      cursor.execute("""insert into tasks (name, description, deadline, oid, shopping) values (%s, %s, %s, %s, %s);""", (name, description, deadline, oid, 'n'))
      conn.commit()
    
    
    
    if shopping_status is not None:
      cursor.execute("""insert into tasks (name, description, deadline, oid, shopping) values (%s, %s, %s, %s, %s);""", (name, description, deadline, oid, 'y'))
      conn.commit()
      cursor.execute("""select id from tasks where name = %s;""",(name,))
      taskid = cursor.fetchone()
      tid = taskid[0]
      session["tid"] = tid
      session["deadline"] = deadline
      conn.commit()
      shop = shopping_status
      return redirect(url_for("plan.shopping",shop=shop))
    return redirect(url_for("plan.calender"))
    
    
    
    
    
@bp.route('/shopping')
def shopping():
  return render_template('shopping.html')    
  
  
  
  
    
@bp.route('/additems', methods=['POST', 'GET'])
def add_items():  
  
  if request.method == 'POST':
    conn = db.get_db()
    cursor = conn.cursor()
    tid = session.get("tid")
    deadline = session.get("deadline")
    itemname = request.form['itemname']
    itemquant = request.form['itemquant']
    cursor.execute("""insert into shoppinglist (item, qty, tid, deadline) values (%s, %s, %s, %s);""", (itemname, itemquant, tid, deadline))
    conn.commit()
  
    shstatus = request.form.get('shstatus')
    
    if shstatus is not None:
      session["tid"] = None
      session["deadline"] = None
      conn.commit()
      return redirect(url_for("plan.calender"))    
    conn.commit()
    return redirect(url_for("plan.shopping"))
    
    
    
    
    
    
@bp.route('/deletetask')
def deletetask():
  name = request.args.get("name",1)
  conn = db.get_db()
  cursor = conn.cursor()
  cursor.execute("""select shopping from tasks where name = %s;""",(name,))
  shoppingstatus = cursor.fetchone()
  shop_status = shoppingstatus[0]
  
  cursor.execute("""select deadline from tasks where name = %s;""",(name,))
  dtime = cursor.fetchone()
  deadline = dtime[0]
  deadlinetime = deadline.strftime("%Y-%m-%d")
  l = deadlinetime.split("-")
  
  if shop_status == 'y':
    cursor.execute("""select id from tasks where name = %s;""",(name,))
    t = cursor.fetchone()
    tasksid = t[0]
    cursor.execute("""delete from shoppinglist where tid = %s;""",(tasksid,))
  cursor.execute("""delete from tasks where name = %s;""",(name,))
  conn.commit()
  return redirect(url_for("plan.thisday", d=l[2], m=l[1], y=l[0]))
    
    
    
    



@bp.route('/deleteitem')
def deleteitem():
  name = request.args.get("name",1)
  item = request.args.get("item",1)
  conn = db.get_db()
  cursor = conn.cursor()
  cursor.execute("""select shopping from tasks where name = %s;""",(name,))
  shoppingstatus = cursor.fetchone()
  shop_status = shoppingstatus[0]
  
  cursor.execute("""select deadline from tasks where name = %s;""",(name,))
  dtime = cursor.fetchone()
  deadline = dtime[0]
  deadlinetime = deadline.strftime("%Y-%m-%d")
  l = deadlinetime.split("-")
  
  if shop_status == 'y':
    cursor.execute("""select id from tasks where name = %s;""",(name,))
    t = cursor.fetchone()
    tasksid = t[0]
    cursor.execute("""delete from shoppinglist where tid = %s and item = %s;""",(tasksid,item))
  conn.commit()
  return redirect(url_for("plan.thisday", d=l[2], m=l[1], y=l[0]))


    
    
    
    
    
@bp.route('/update')
def update():
  conn = db.get_db()
  cursor = conn.cursor()
  dtime = datetime.datetime.now().strftime("%Y-%m-%d")
  cursor.execute("""select name from tasks where deadline = %s;""",(d,))
  taskn = cursor.fetchone()
  taskname = taskn[0]
  cursor.execute("""select shopping from tasks where name = %s;""",(taskname,))
  shoppingstatus = cursor.fetchone()
  shop_status = shoppingstatus[0]
  if shop_status == 'y':
    cursor.execute("""select id from tasks where name = %s;""",(taskname,))
    t = cursor.fetchone()
    tasksid = t[0]
    cursor.execute("""delete from shoppinglist where tid = %s;""",(tasksid,))
  cursor.execute("""delete from tasks where name = %s;""",(taskname,))
  conn.commit()
  return redirect(url_for("plan.calender"))

  
