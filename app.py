from flask import Flask,render_template, url_for, request, redirect, session, flash,make_response
import pymysql
import os
from werkzeug.utils import secure_filename
from flask_session import Session
import random

from flask_mail import Mail, Message 



app = Flask(__name__)
mail = Mail(app) # instantiate the mail class 
# configuration of mail 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'shopsavvy0310@gmail.com'
app.config['MAIL_PASSWORD'] = 'kkln orvh wodz ggys'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) 
   
app.secret_key = 'your_secret_key'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
 
UPLOAD_FOLDER='static/upload/'

Session(app)

conn = pymysql.connect(host = 'localhost', user = 'root', password = '', db = 'trumart_db')

def generateotp():
    import random
    suu=random.randint(100,999)
    return suu
    

# ADMIN ------------------------>>

@app.route("/admin")
def login():
    return render_template("admin/login.html")

@app.route('/logout')
def logout():
    session.clear() 
    return redirect('/')

def check_session():
    admin_id = int(session.get('Admin_id') or 0)
    if admin_id == 0:
        return redirect('/admin') 
    return None

@app.route("/admin/dashboard")
def dashboard():
    redirect_result = check_session()
    if redirect_result:
        return redirect_result
    cursor = conn.cursor()
    
    cat_query = "SELECT COUNT(*) FROM manage_cat"
    cursor.execute(cat_query)
    total_cat = cursor.fetchone()[0]
    
    prdct_query = "SELECT COUNT(*) FROM manage_prdct"
    cursor.execute(prdct_query)
    total_prdct = cursor.fetchone()[0]
    
    supp_query = "SELECT COUNT(*) FROM supplier_reg"
    cursor.execute(supp_query)
    total_supp = cursor.fetchone()[0]
    
    user_query = "SELECT COUNT(*) FROM user_reg"
    cursor.execute(user_query)
    total_user = cursor.fetchone()[0]
    
    disp_query = "SELECT COUNT(*) FROM manage_disp"
    cursor.execute(disp_query)
    total_disp = cursor.fetchone()[0]
    cursor.close()
    
    return render_template("admin/dashboard.html", total_cat=total_cat ,  total_prdct=total_prdct , total_supp=total_supp , total_user=total_user, total_disp=total_disp)

@app.route("/admin/addcategory")
def addcategory():
    redirect_result = check_session()
    if redirect_result:
        return redirect_result
    return render_template("admin/addcategory.html")

@app.route("/admin/viewcategory")
def viewcategory():
    redirect_result = check_session()
    if redirect_result:
        return redirect_result
    cursor = conn.cursor()
    query = "SELECT * FROM manage_cat"
    cursor.execute(query)
    acount = cursor.fetchall()
    cursor.close()
    return render_template("admin/viewcategory.html",acc=acount)

@app.route("/admin/addproduct")
def addproduct():
    redirect_result = check_session()
    if redirect_result:
        return redirect_result
    cursor = conn.cursor()
    query = "SELECT * from manage_cat"
    cursor.execute(query)
    category = cursor.fetchall()
    query = "SELECT * from manage_subcat"
    cursor.execute(query)
    subcategory = cursor.fetchall()
    cursor.close()
    return render_template("admin/addproduct.html", cat=category,subcat = subcategory)

@app.route("/admin/viewproduct")
def viewproduct():
    redirect_result = check_session()
    if redirect_result:
        return redirect_result
    cursor = conn.cursor()
    query = "SELECT a. *, b.*,c.subcat_name FROM manage_cat as a, manage_prdct as b,manage_subcat as c  WHERE a.cat_id = b.cat_id AND b.subcat_id = c.subcat_id"
    cursor.execute(query)
    summ = cursor.fetchall()
    cursor.close()
    return render_template("admin/viewproduct.html", sho=summ)


@app.route("/admin/add_cat_process",methods=["POST"])
def add_cat_process():
    cursor= conn.cursor()
    cat_name=request.form['cat_name']
    description=request.form['description']
    query="INSERT INTO manage_cat(cat_name,description) VALUES (%s,%s)"
    val=(cat_name,description)
    cursor.execute(query,val)
    conn.commit()
    cursor.close()
    msg='New Category Added Successfully'
    return render_template("admin/addcategory.html", msg=msg)

@app.route("/admin/add_prdct_process",methods=["POST"])
def add_prdct_process():
    cursor = conn.cursor()
    cat_id = request.form['cat_id']
    subcat_id = request.form['subcat_id']
    prdct_name = request.form['prdct_name']
    description = request.form['description']
    price=request.form['price']
    p_image=request.files['p_image']
    filename = secure_filename(p_image.filename)
    p_image.save(os.path.join(UPLOAD_FOLDER,filename))
    path = os.path.join(UPLOAD_FOLDER,filename)
    # p_status = request.form['p_status']
    query="INSERT INTO manage_prdct(cat_id,subcat_id,prdct_name,description,price,p_image) VALUES (%s,%s,%s,%s,%s,%s)"
    val = (cat_id,subcat_id, prdct_name,description,price,path)
    cursor.execute(query,val)
    conn.commit()
    cursor.close()
    msg='New Product Added Successfully'
    
    return render_template("admin/addproduct.html", msg=msg)

@app.route("/admin/admin_login", methods=['POST'])
def admin_login():
    cursor = conn.cursor()
    Email = request.form['Email']
    Password = request.form['Password']
    query="SELECT * from admin_login WHERE Email=%s and Password=%s"
    val=(Email,Password)
    cursor.execute(query,val)
    account=cursor.fetchone()
    cursor.close()
 
    if account:
        session['Admin_id'] = account[0]
        session['Email'] = account[1]
        
        
        msg="Login Successfully"
        return redirect(url_for('dashboard', msg=msg))

    else : 
      msg="Invalid credentials"
      return render_template("admin/login.html", msg=msg) 

@app.route("/admin/edit_cat/<int:cat_id>")
def edit_cat(cat_id):
    cursor = conn.cursor()
    query = "SELECT * FROM manage_cat WHERE cat_id = %s"
    cursor.execute(query, (cat_id,))
    category = cursor.fetchall()
    cursor.close()
    return render_template("admin/edit_cat.html", category=category)

@app.route("/admin/edit_cat_process",methods=["POST"])
def edit_cat_process():
    cursor= conn.cursor()
    cat_id=request.form['cat_id']
    cat_name=request.form['cat_name']
    description=request.form['description']
    query = "UPDATE manage_cat SET cat_name=%s, description=%s WHERE cat_id=%s"
    val=(cat_name,description,cat_id)
    cursor.execute(query,val)
    conn.commit()
    cursor.close()
    msg='Update Category'
    return redirect(url_for('viewcategory', msg=msg))

@app.route("/admin/edit_prdct/<int:prdct_id>")
def edit_prdct(prdct_id):
    
    cursor = conn.cursor()
    query = "SELECT * from manage_cat"
    cursor.execute(query)
    category = cursor.fetchall()
    cursor.close()
     
    cursor = conn.cursor()
    query = "SELECT a. *, b.* FROM manage_cat as a, manage_prdct as b WHERE a.cat_id = b.cat_id and b.prdct_id = %s"
    cursor.execute(query,(prdct_id,))
    prdct = cursor.fetchone()
  
    cursor.close()
    return render_template("admin/edit_prdct.html", i=prdct,category=category)

@app.route("/admin/edit_prdct_process",methods=["POST"])
def edit_prdct_process():
    cursor = conn.cursor()
    prdct_id = request.form['prdct_id']
    cat_id = request.form['cat_id']
    prdct_name = request.form['prdct_name']
    description = request.form['description']
    price=request.form['price']
    image = request.files['p_image']
    if image and image.filename:
        filename = secure_filename(image.filename)
        image.save(os.path.join(UPLOAD_FOLDER,filename))
        path = os.path.join(UPLOAD_FOLDER,filename)
        query = "UPDATE manage_prdct SET cat_id=%s, prdct_name=%s, description=%s, price=%s, p_image=%s WHERE prdct_id=%s"
        val = (cat_id,prdct_name,description,price,path,prdct_id)
    else:
            query = "UPDATE manage_prdct SET cat_id=%s, prdct_name=%s, description=%s, price=%s WHERE prdct_id=%s"
            val = (cat_id,prdct_name,description,price,prdct_id)
        
    cursor.execute(query,val)
    conn.commit()
    cursor.close()
    msg = 'Update Product'
    return redirect(url_for('viewproduct', msg=msg))

@app.route("/admin/adddispatcher")
def adddispatcher():
    redirect_result = check_session()
    if redirect_result:
        return redirect_result
    cursor = conn.cursor()
    query = "SELECT * FROM manage_disp"
    cursor.execute(query)
    tak = cursor.fetchall()
    cursor.close()
    return render_template("admin/adddispatcher.html",acc=tak)

@app.route("/admin/add_dis_process", methods=["POST"])
def add_dis_process():
    cursor= conn.cursor()
    
    name = request.form['name']
    mobile = request.form['mobile']
    email = request.form['email']
    password = request.form['password']
    
    query = "INSERT INTO manage_disp (name,mobile,email,password) VALUES (%s,%s,%s,%s)"
    val = (name,mobile,email,password)
    cursor.execute(query,val)
    tis = cursor.fetchone()
    conn.commit()
    cursor.close()
    
    # if tis:
    #     msg="This Email is already registered!"
    #     cursor.close()
    #     return render_template("admin/adddispatcher.html", msg=msg)
    return redirect(url_for('adddispatcher'))
    
@app.route("/admin/block/<int:disp_id>")
def block(disp_id):       
    cursor= conn.cursor()
    query="UPDATE manage_disp SET status = 1 WHERE disp_id  = %s"
    val=(disp_id)
    cursor.execute(query,val)
    conn.commit()
    cursor.close()
    msg1='Dispatcher Block Successfully'
    return redirect(url_for('adddispatcher'))


@app.route("/admin/unblock/<int:disp_id>")
def unblock(disp_id):       
    cursor= conn.cursor()
    query="UPDATE manage_disp SET status = 0 WHERE disp_id  = %s"
    val=(disp_id)
    cursor.execute(query,val)
    conn.commit()
    cursor.close()
    msg1='Dispatcher Unblock Successfully'
    return redirect(url_for('adddispatcher'))

@app.route('/admin/delete_category/<int:cat_id>')
def delete_category(cat_id):
    cursor = conn.cursor()
    try:
        query = "DELETE FROM manage_cat WHERE cat_id  = %s"
        val = (cat_id)
        cursor.execute(query,val)
        conn.commit()
        msg='Category Deleted successfully!'
        return redirect(url_for('viewcategory'))
    finally:
        cursor.close()
        
@app.route('/admin/delete_product/<int:prdct_id>')
def delete_product(prdct_id):
    cursor = conn.cursor()
    try:
        query = "DELETE FROM manage_prdct WHERE prdct_id  = %s"
        val = (prdct_id)
        cursor.execute(query,val)
        conn.commit()
        msg='Product Deleted successfully!'
        return redirect(url_for('viewproduct'))
    finally:
        cursor.close()
        
@app.route('/admin/delete_dispatcher/<int:disp_id>')
def delete_dispatcher(disp_id):
    cursor = conn.cursor()
    try:
        query = "DELETE FROM manage_disp WHERE disp_id  = %s"
        val = (disp_id)
        cursor.execute(query,val)
        conn.commit()
        msg='Dispatcher Deleted successfully!'
        return redirect(url_for('adddispatcher'))
    finally:
        cursor.close()
        
@app.route("/admin/viewSupp")
def viewSupp():
    redirect_result = check_session()
    if redirect_result:
        return redirect_result
    cursor = conn.cursor()
    query = "SELECT * FROM supplier_reg"
    cursor.execute(query)
    why = cursor.fetchall()
    cursor.close()
    return render_template("admin/viewSupp.html",mee=why)

@app.route("/admin/blockunblock1",methods=["POST"])
def blockunblock1():
    id = request.form['id']
    cursor = conn.cursor()
    query = f"SELECT * from supplier_reg WHERE supp_id = {id}"
    cursor.execute(query)
    data = cursor.fetchone()
    if data[8] == 0:
        query = f"UPDATE supplier_reg SET s_status = 1 WHERE supp_id = {id}"
    else:
        query = f"UPDATE supplier_reg SET s_status = 0 WHERE supp_id = {id}"
        
    cursor.execute(query)
    conn.commit()
    return redirect('viewSupp')

@app.route("/admin/viewuser")
def viewuser():
    cursor = conn.cursor()
    query = "SELECT * from user_reg"
    cursor.execute(query)
    user = cursor.fetchall()
    cursor.close()
    return render_template("admin/viewuser.html", yee=user)

@app.route("/admin/blockunblock",methods=["POST"])
def blockunblock():
    id = request.form['id']
    cursor = conn.cursor()
    query = f"SELECT * from user_reg WHERE user_id = {id}"
    cursor.execute(query)
    data = cursor.fetchone()
    if data[8] == 0:
        query = f"UPDATE user_reg SET status = 1 WHERE user_id = {id}"
    else:
        query = f"UPDATE user_reg SET status = 0 WHERE user_id = {id}"
        
    cursor.execute(query)
    conn.commit()
    return redirect('viewuser')

@app.route("/admin/viewOrders")
def viewOrder():
    return render_template("admin/viewOrder.html")

@app.route("/admin/myyaccount")
def myyaccount():
    return render_template("admin/myyaccount.html")

@app.route('/editprofile')
def editprofile():
    admin_email = session['Admin_id']
    cursor = conn.cursor()
    cat_query  = "SELECT * FROM Admin_login where Admin_id = %s"
    val = (admin_email)
    cursor.execute(cat_query,val)
    account = cursor.fetchall()
    cursor.close()
    return render_template("admin/editprofile.html",account=account)

@app.route("/admin/update_pass",methods=["POST"])
def update_pass():
    cursor= conn.cursor()
    Email = request.form["Email"]
    Password=request.form["Password"]
    Admin_id = request.form["Admin_id"]
    
    query = "UPDATE admin_login SET Password = %s where Admin_id = %s"
    
    val=(Password,Admin_id)
    cursor.execute(query,val)
    conn.commit()
    cursor.close()
    return render_template("/admin/login.html")

@app.route("/admin/Supp")
def Supp():
    return render_template("admin/addSupp.html")

@app.route("/admin/addSupp", methods=["POST"])
def addSupp():
    cursor= conn.cursor()   
    supp_name = request.form['supp_name']
    supp_bussName = request.form['supp_bussName']
    address = request.form['address']
    email_id = request.form['email_id']
    pwd = request.form['pwd']
    contact_no = request.form['contact_no']
    profile_img = request.files['profile_img']
    filename = secure_filename(profile_img.filename)
    profile_img.save(os.path.join(UPLOAD_FOLDER,filename))
    path = os.path.join(UPLOAD_FOLDER,filename)
    Supp = "INSERT INTO supplier_reg(supp_name,supp_bussName,address,email_id,pwd,contact_no,profile_img) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    val = (supp_name,supp_bussName,address,email_id,pwd,contact_no,path)
    cursor.execute(Supp,val)
    conn.commit()
    cursor.close()
    return render_template("admin/addSupp.html")


@app.route("/admin/stock")
def stock():   
    cursor = conn.cursor()
    query = "SELECT * from manage_prdct"
    cursor.execute(query)
    category = cursor.fetchall()
    cursor.close()
    return render_template("admin/viewstock_qty.html", see=category )  

 
@app.route("/admin/add_stock_post",methods=["POST"])
def add_stock_post():
    cursor = conn.cursor()
    btn = request.form['btn']
    prod_id = request.form['product_id']
    quantity = int(request.form['quantity'])
    sql = "SELECT * FROM manage_prdct WHERE prdct_id = %s"
    val = (prod_id)
    cursor.execute(sql,val)
    data = cursor.fetchone()
    if btn == 'add':
        quantity_add =quantity + data[7]
        sql = "UPDATE manage_prdct SET qty = %s WHERE prdct_id = %s"
        val = (quantity_add,prod_id)       
    else:
        quantity_rm = data[7] - quantity
        sql = "UPDATE manage_prdct SET qty = %s WHERE prdct_id = %s"
        val = (quantity_rm,prod_id)
    cursor.execute(sql,val)
    conn.commit()
    return redirect(url_for('stock'))


@app.route("/admin/viewfeedback")
def viewfeedback():
    return render_template("admin/viewfeedback.html")

@app.route("/admin/vieworderL")
def vieworderL():
    cursor = conn.cursor()
    sql = "SELECT a.* , b.*,c.prdct_name FROM order_details as a , order_tbl as b,manage_prdct as c WHERE a.detail_id=b.detail_id AND b.prdct_id=c.prdct_id"
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.commit()
    return render_template("admin/vorderlist.html",data=data)


from xhtml2pdf import pisa
import io
@app.route('/download_pdf')
def download_pdf():
    cursor = conn.cursor()
    sql = """
        SELECT a.*, b.*, c.prdct_name
        FROM order_details AS a, order_tbl AS b, manage_prdct AS c
        WHERE a.detail_id = b.detail_id AND b.prdct_id = c.prdct_id
    """
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.commit()

    html = render_template('admin/vorderlist_pdf.html', data=data)
    result = io.BytesIO()
    pisa.CreatePDF(io.StringIO(html), dest=result)

    response = make_response(result.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=orderlist.pdf'
    return response


@app.route("/admin/vorderH")
def vorderH():
    return render_template("admin/vorderhistory.html")

@app.route("/admin/viewship")
def viewship():
    return render_template("admin/shippingL.html")

@app.route("/user/custom",methods=["POST"])
def custom():
    cursor = conn.cursor()
    
    prdct_name = request.form['prdct_name']
    price = request.form['price']
    description = request.form['description']
    qty = request.form['qty']
    img=request.files['img']
    filename = secure_filename(img.filename)
    img.save(os.path.join(UPLOAD_FOLDER,filename))
    path = os.path.join(UPLOAD_FOLDER,filename)
   
    query="INSERT INTO customization(prdct_name,price,description,qty,img) VALUES (%s,%s,%s,%s,%s)"
    val = (prdct_name,price,description,qty,path)
    
    cursor.execute(query,val)
    conn.commit()
    cursor.close()
    msg='feedback sent!'  
    return render_template("admin/shippingL.html", msg=msg)






@app.route("/admin/addsubcat")
def addsubcat():
    cursor = conn.cursor()
    query = "SELECT * from manage_cat"
    cursor.execute(query)
    category = cursor.fetchall()
    cursor.close()
    return render_template("admin/addsub_cat.html", cat=category)



@app.route("/admin/addsubcatprocess",methods=["POST"])
def addsubcatprocess():
    cursor = conn.cursor()    
    subcat_name = request.form['subcat_name']
    cat_id = request.form['cat_id']
    supp_desc=request.form['supp_desc'] 
    img=request.files['img']
    filename = secure_filename(img.filename)
    img.save(os.path.join(UPLOAD_FOLDER,filename))
    path = os.path.join(UPLOAD_FOLDER,filename)
 
    query="INSERT INTO manage_subcat(subcat_name, cat_id, supp_desc, img) VALUES (%s, %s,%s,%s)"
    val = (subcat_name,cat_id, supp_desc, path)
    cursor.execute(query,val)
    conn.commit()
    cursor.close()
    msg='New Sub Category Added Successfully'
    
    return render_template("admin/addsub_cat.html", msg=msg)

@app.route("/admin/Vsubcat")
def Vsubcat():
    redirect_result = check_session()
    if redirect_result:
        return redirect_result
    cursor = conn.cursor()
    query = "SELECT a.*, b.cat_name FROM manage_subcat as a, manage_cat as b WHERE a.cat_id=b.cat_id"
    cursor.execute(query)
    me = cursor.fetchall()
    cursor.close()
    return render_template("admin/viewsub_cat.html", why=me)

@app.route("/admin/edit_subcat/<int:subcat_id>")
def edit_subcat(subcat_id):
    
    cursor = conn.cursor()
    query = "SELECT * from manage_cat"
    cursor.execute(query)
    cat = cursor.fetchall()
    cursor.close()
     
    cursor = conn.cursor()
    query = "SELECT a.*,b.* FROM `manage_subcat`as a, `manage_cat`as b WHERE a.cat_id=b.cat_id AND subcat_id =%s;"
    cursor.execute(query,(subcat_id,))
    h = cursor.fetchone()
    print (h)
  
    cursor.close()
    return render_template("admin/edit_subcat.html", h=h, cat=cat)

@app.route("/admin/edit_subcat_process",methods=["POST"])
def edit_subcat_process():
    cursor = conn.cursor()
    subcat_name = request.form['subcat_name']
    cat_id = request.form['cat_id']
    prdct_id = request.form['prdct_id']
    supp_desc = request.form['supp_desc'] 
    image=request.files['img']
    if image and image.filename:
        filename = secure_filename(image.filename)
        image.save(os.path.join(UPLOAD_FOLDER,filename))
        path = os.path.join(UPLOAD_FOLDER,filename)
        query = "UPDATE manage_subcat SET cat_id=%s, subcat_name=%s, supp_desc=%s, img=%s WHERE subcat_id=%s"
        val = (cat_id,subcat_name,supp_desc,path,prdct_id)
    else:
            query = "UPDATE manage_subcat SET cat_id=%s, subcat_name=%s, supp_desc=%s WHERE subcat_id=%s"
            val = (cat_id,subcat_name,supp_desc,prdct_id)
        
    cursor.execute(query,val)
    conn.commit()
    cursor.close()
    msg = 'UPDATE SUBCATEGORY'
    return redirect(url_for('Vsubcat'))

@app.route('/admin/delete_subcat/<int:prdct_id>')
def delete_subcat(prdct_id):
    cursor = conn.cursor()
    try:
        query = "DELETE FROM manage_subcat WHERE cat_id  = %s"
        val = (prdct_id)
        cursor.execute(query,val)
        conn.commit()
        msg='Subcategory Deleted successfully!'
        return redirect(url_for('viewsub_cat', msg=msg))
    finally:
        cursor.close()
        cursor.close()
        
@app.route('/admin/delete_supplier/<int:supp_id>')
def delete_supplier(supp_id):
    cursor = conn.cursor()
    try:
        query = "DELETE FROM supplier_reg WHERE supp_id  = %s"
        val = (supp_id)
        cursor.execute(query,val)
        conn.commit()
        msg='Supplier Deleted successfully!'
        return redirect(url_for('viewSupp'))
    finally:
        cursor.close()

# @app.route("/admin/Jlogin", methods=["POST"])
# def Jlogin():
#     cursor = conn.cursor()
    
#     Email = request.form['Email']
#     query="SELECT * from admin_login WHERE Admin_id=%s and Email=%s"
#     val=(Admin_id,Email)
#     cursor.execute(query,val)
#     account=cursor.fetchone()
#     cursor.close()
 
#     if account:
#         session['Admin_id'] = account[0]
#         session['Email'] = account[1]
#         msg="Login Successfully"
#         return render_template("admin/dashboard.html", msg=msg)
           
#     else : 
#       msg="Invalid credentials"
#       return render_template("admin/login.html", msg=msg)

# ADMIN ------------------------------>>



# USER --------------------------------------------->>>

@app.route("/")
def index():
    
    cursor = conn.cursor()
    query = "SELECT * FROM manage_cat"
    cursor.execute(query)
    cat = cursor.fetchall()
    query = "SELECT * FROM manage_prdct ORDER BY prdct_id DESC LIMIT 5"
    cursor.execute(query)
    prod = cursor.fetchall()
    query = "SELECT * FROM manage_subcat WHERE cat_id=12 LIMIT 6"
    cursor.execute(query)
    subcat = cursor.fetchall()
    query = "SELECT * FROM manage_subcat WHERE cat_id=13 LIMIT 6"
    cursor.execute(query)
    women = cursor.fetchall()
    query = "SELECT * FROM manage_subcat WHERE cat_id=14 LIMIT 6"
    cursor.execute(query)
    kid = cursor.fetchall()
    cursor.close()   
    return render_template("user/index.html",cat=cat,prod=prod,subcat=subcat,women=women,kid=kid)

@app.route("/user/contact")
def contact():
    return render_template("user/contact.html")

@app.route("/user/feedback",methods=["POST"])
def feedback():
    cursor = conn.cursor()
    
    name = request.form['name']
    email = request.form['email']
    feed_cat = request.form['feed_cat']
    feed_des = request.form['feed_des']
    img=request.files['img']
    filename = secure_filename(img.filename)
    img.save(os.path.join(UPLOAD_FOLDER,filename))
    path = os.path.join(UPLOAD_FOLDER,filename)
   
    query="INSERT INTO feedback(name,email,feed_cat,feed_des,img) VALUES (%s,%s,%s,%s,%s)"
    val = (name,email,feed_cat,feed_des,path)
    
    cursor.execute(query,val)
    conn.commit()
    cursor.close()
    msg='feedback sent!'  
    return render_template("user/index.html", msg=msg)

@app.route("/user/customization")
def customization():
    cursor = conn.cursor()
    sql = "SELECT * FROM  customization WHERE cust_id = 1"

    cursor.execute(sql)
    data = cursor.fetchone()
    cursor.close()   
    return render_template("user/customization.html",t=data)



@app.route("/user/Ulogin")
def Ulogin():
    return render_template("user/Ulogin.html")

@app.route("/user/forgot")
def forgot():
    return render_template("user/forgot.html")

@app.route("/user/chngepass",methods=['POST'])
def chngepass():
    cursor = conn.cursor()
    email = request.form['u_email']
    sql = "SELECT * FROM user_reg WHERE u_email = %s"
    val = (email)
    cursor.execute(sql,val)
    data = cursor.fetchone()
    cursor.close()   
    if data:
        otp = generateotp()
        msg = Message(subject='Password OTP Verification', sender='shopsavvy0310@gmail.com', recipients=[email])
        msg.body = f"Your OTP is : {otp}"
        mail.send(msg)
        return render_template("user/verifiedOtp.html",otp=otp,email=email)
    else:
        msg="Enter Valid Email Address"
        return render_template("user/forgot.html",msg=msg)

@app.route("/user/OTP",methods=['POST'])
def OTP():
    otp = request.form['otp']
    email = request.form['email']
    otpcode = request.form['otpcode']
    if otp==otpcode:
        return render_template("user/updatePassword.html",otp=otp,email=email)
    else:
        flash("Enter Valid OTP")
        return render_template("user/verifiedOtp.html",otp=otp,email=email)

@app.route("/user/updatePassword",methods=['POST'])
def updatePassword():
    cursor=conn.cursor()
    newpass = request.form['newpass']
    email = request.form['u_email']
    matchpass = request.form['matchpass']
    if newpass==matchpass:
        sql = "SELECT * FROM user_reg WHERE u_email=%s"
        val = (email)
        cursor.execute(sql,val)
        data = cursor.fetchone()
        if data[6]==newpass:
            msg = "Don't Enter old password"   
            return render_template("user/updatePassword.html",email=email,msg=msg)

        sql = "UPDATE user_reg SET password=%s WHERE u_email=%s"
        val=(newpass,email)
        cursor.execute(sql,val)
        conn.commit()
        return redirect('Ulogin')
    else:
        msg = "Password doesn't match"
        return render_template("user/updatePassword.html",email=email,msg=msg)

@app.route("/user/sign")
def sign():
    return render_template("user/signup.html")

@app.route("/user/signup",methods=["POST"])
def signup():
    cursor = conn.cursor()
    name = request.form['name']
    mobile = request.form['mobile']
    u_email = request.form['u_email']
    password = request.form['password']
    dob = request.form['dob']
    gender = request.form['gender']
    address = request.form['address']
    query="INSERT INTO user_reg(name,mobile,u_email,password,dob,gender,address) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    val = (name,mobile,u_email,password,dob,gender,address)
    cursor.execute(query,val)
    conn.commit()
    
    return redirect('Ulogin')

@app.route("/user/Ulogin", methods=["POST"])
def user_login():
    cursor = conn.cursor()
    u_email = request.form['u_email']
    Password = request.form['password']
    query="SELECT * from user_reg WHERE u_email=%s and password=%s and status=0"
    val=(u_email,Password)
    cursor.execute(query,val)
    account=cursor.fetchone()
    cursor.close()
 
    if account:
        session['user_id'] = account[0]
        session['u_email'] = account[1]
        session['name'] = account[2]
        
        flash("Login Successfully")
        return render_template("user/index.html")
    else : 
        flash("Invalid credentials")
        return redirect(url_for('Ulogin'))
  
  
@app.route('/user/checkoutdetail')
def checkoutdetail():
    u_email = session['user_id']
    cursor = conn.cursor()
    cat_query  = "SELECT * FROM user_reg where user_id = %s"
    val = (u_email)
    cursor.execute(cat_query,val)
    detail = cursor.fetchone()
    user_id = detail[0]
    cat_query  = "SELECT a.*, b.* FROM add_to_cart as a, manage_prdct as b WHERE a.user_id = %s AND a.prdct_id = b.prdct_id"
    val = (user_id)
    cursor.execute(cat_query,val)
    cart = cursor.fetchall()
    cursor.close()
    total=0
    for i in cart:
        total+=i[3]*i[8]
    cursor.close()
    gst=total*18/100
    gsttotal=gst+total
        
    return render_template("user/checkout.html", detail=detail, cart=cart ,total=total,gst=gst,gsttotal=gsttotal )

@app.route("/user/placeorder",methods=["POST"])
def placeorder():
    cursor = conn.cursor()
    user_id = session.get('user_id')
    
    name = request.form['name']
    mobile = request.form['mobile']
    u_email = request.form['u_email']
    
    address = request.form['address']
    country = request.form['country']
    state = request.form['state']
    city = request.form['city']
    pin_code = request.form['pin_code']
    pymnt_method = request.form['pymnt_method']
    
    query = "SELECT * FROM manage_prdct"
    cursor.execute(query)
    prod = cursor.fetchall()
    
    # Fetch all cart items
    query = "SELECT * FROM add_to_cart WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    cart_items = cursor.fetchall()

    order_id = None
    amt=0

    
    query="INSERT INTO order_details(user_id,name,mobile,u_email,address,country,state,city,pin_code,pymnt_method) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (user_id,name,mobile,u_email,address,country,state,city,pin_code,pymnt_method)
    cursor.execute(query,val)
    conn.commit()
    detail_id = cursor.lastrowid

    
    for idx, item in enumerate(cart_items):
        proid = item[2]
        cust_id = item[1]
        qty = item[3]
        for j in cart_items:
            for i in prod:
                if j[2]==i[0]:
                    amt+=i[3]*j[3]
        # Insert into order_tbl
        order_number = str(random.randint(100000, 999999))

        query = """
            INSERT INTO order_tbl(detail_id,order_num, user_id, prdct_id, qty,pymnt_method,total_amt)
            VALUES (%s,%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (detail_id,order_number, user_id, proid, qty,pymnt_method,amt))
        
        # Capture order_id from first insert
        if idx == 0:
            order_id = cursor.lastrowid
    
    
    
    query="DELETE FROM add_to_cart WHERE user_id=%s"
    val = (user_id,)
    cursor.execute(query,val)
    conn.commit()
    sql = "SELECT * FROM user_reg WHERE user_id = %s"
    val=(user_id)
    cursor.execute(sql,val)
    data = cursor.fetchone()
    
    
    
    
    email = session.get('u_email')
    msg = Message(subject='Your SHOP SAVVY Order ', sender='shopsavvy0310@gmail.com', recipients=[email])
    msg.body = f"""Dear {data[2]},
        Thank You For Your Recent Purchase
    """
    mail.send(msg)
    
    return redirect(url_for('addTocartP'))

@app.route('/user/Ulogout')
def Ulogout():
    session.pop('user_id',None)
    session.pop('u_email',None)
    session.pop('name',None)
    return redirect(url_for('Ulogin'))

  
@app.route("/user/product_list")
def product_list():
    cursor = conn.cursor()
    query = "SELECT a.*, b.* FROM manage_cat as a, manage_prdct as b where a.cat_id = b.cat_id"
    cursor.execute(query)
    summ = cursor.fetchall()
    cursor.close()
    return render_template("user/product_list.html", sho=summ)

@app.route("/user/product_cat/<int:cat_id>")
def product_cat(cat_id):
    cursor = conn.cursor()
    query = "SELECT * FROM manage_prdct WHERE cat_id = %s"
    cursor.execute(query, (cat_id,))
    category = cursor.fetchall()
    cursor.close()
    return render_template("user/product_cat.html", category=category)

@app.route("/user/product_detail/<int:prdct_id>")
def product_detail(prdct_id):
    cursor = conn.cursor()
    query = "SELECT * FROM manage_prdct where prdct_id = %s"
    cursor.execute(query, (prdct_id,))
    p_detail = cursor.fetchone()
    cat_id = p_detail[8]
    query = "SELECT * FROM manage_prdct where subcat_id = %s"
    cursor.execute(query,(cat_id,))
    rec = cursor.fetchall()
    cursor.close()
    return render_template("user/product_detail.html", t=p_detail,rec=rec)


@app.route("/user/addTocart/<int:prdct_id>")
def addTocart(prdct_id):
    if 'user_id' in session:
        cursor = conn.cursor()
        Prdct_id = prdct_id
        
        user_id = session.get('user_id')
        qty = 1
        query = "SELECT * FROM add_to_cart WHERE prdct_id = %s AND user_id=%s"
        val = (prdct_id,user_id)
        cursor.execute(query,val)
        account = cursor.fetchall()
        if account:
            # msg=""
            flash('Product already in a cart','error')
            return redirect(url_for('product_list'))
        else:
            query="INSERT INTO add_to_cart(prdct_id,user_id,qty) VALUES (%s,%s,%s)"
            val = (Prdct_id,user_id,qty)
            cursor.execute(query,val)
            conn.commit()
            cursor.close()
            flash('Product add to cart','success')
            return redirect(url_for("addTocartP"))
    else:
        flash('please Login First','error')
        return redirect(url_for('Ulogin'))
    
@app.route("/user/addTocartP")
def addTocartP():
    if 'user_id' in session:
        cursor = conn.cursor()
        user_id = session.get('user_id')
        query = f"SELECT a.cart_id, a.user_id, a.prdct_id, a.qty, b.prdct_name, b.p_image, b.price FROM add_to_cart AS a JOIN manage_prdct AS b ON a.prdct_id = b.prdct_id WHERE a.user_id = {user_id};"
        cursor.execute(query)
        cart = cursor.fetchall()
        total=0
        for i in cart:
            total+=i[3]*i[6]
        cursor.close()
        gst=total*18/100
        gsttotal=gst+total
        
        return render_template("user/addTocart.html", cart=cart,total=total,gsttotal=gsttotal,gst=gst)
    else:
        flash('please Login First','error')
        return redirect(url_for('Ulogin'))

@app.route("/user/atcqty", methods=['POST'])
def atcqty():
    cursor = conn.cursor()
    
    btn = request.form['btn']  # Get action (add/min)
    cart_id = request.form['id']  # Get cart ID
    qty = int(request.form['qty'])  # Convert qty to an integer

    # Calculate new quantity
    if btn == "add":
        new_qty = qty + 1
    elif btn == "min":
        new_qty = max(1, qty - 1)  # Prevent quantity from going below 1

    # Update quantity in database
    sql = "UPDATE add_to_cart SET qty = %s WHERE cart_id = %s"
    cursor.execute(sql, (new_qty, cart_id))
    
    conn.commit()
    cursor.close()

    return redirect(url_for("addTocartP"))  # Redirect back to cart page

    
@app.route("/user/wishlistt")
def wishlistt():
    cursor = conn.cursor()
    sql="SELECT a.*,b.* FROM manage_prdct as a , wishlist as b WHERE a.prdct_id=b.prdct_id"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    return render_template("user/wishlist.html",data=data)


@app.route("/user/wishlist/<int:prdct_id>")
def wishlist(prdct_id):
    
    if 'user_id' in session:
        cursor = conn.cursor()
        
        user_id = session.get('user_id')
        qty = 1
        query = "SELECT * FROM wishlist WHERE prdct_id = %s AND user_id=%s"
        val = (prdct_id,user_id)
        cursor.execute(query,val)
        account = cursor.fetchall()
        if account:
            # msg=""
            flash('Product already in a wishlist','error')
            return redirect(url_for('product_list'))
    
        cursor = conn.cursor()
        user_id = session.get('user_id')
        qty=1
        sql="INSERT INTO wishlist (prdct_id, user_id, qty) VALUES (%s,%s,%s)"
        val=(prdct_id,user_id,qty)
        cursor.execute(sql,val)
        conn.commit()
        cursor.close()
        return redirect(url_for("wishlistt"))
    else:
        return redirect(url_for("Ulogin"))

        


@app.route("/user/my_account")
def my_account():
    u_email = session['user_id']
    cursor = conn.cursor()
    cat_query  = "SELECT * FROM user_reg where user_id = %s"
    val = (u_email)
    cursor.execute(cat_query,val)
    acont = cursor.fetchone()
    cursor.close()
    return render_template("user/my_account.html",acont=acont)




@app.route("/user/update_pdetail",methods=["POST"])
def update_pdetail():
    cursor= conn.cursor()
    name = request.form["name"]
    mobile = request.form["mobile"]
    address = request.form["address"]
    user_id = request.form["user_id"]
    
    query = "UPDATE user_reg SET name = %s, mobile = %s, address = %s WHERE user_id = %s"
    
    val=(name,mobile,address,user_id)
    cursor.execute(query,val)
    conn.commit()
    cursor.close()
    return redirect("my_account")

@app.route('/user/delete_prdct/<int:prdct_id>')
def delete_prdct(prdct_id): 
    cursor = conn.cursor()
    query = "DELETE FROM add_to_cart WHERE cart_id  = %s"
    cursor.execute(query, (prdct_id,))
    conn.commit()
    cursor.close()
    return redirect(url_for("addTocartP"))


@app.route("/user/men")
def men():   
    cursor = conn.cursor()
    cat_query  = "SELECT * FROM manage_subcat where cat_id = 12"
    cursor.execute(cat_query)
    men = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template("user/men.html",men=men)
        
@app.route("/user/menlist<int:id>")
def men_list(id):   
    cursor = conn.cursor()
    cat_query  = "SELECT a.*, b.* FROM manage_cat as a, manage_prdct as b WHERE a.cat_id = b.cat_id AND b.cat_id = 12 AND b.subcat_id = %s"
    val=(id,)
    cursor.execute(cat_query,val)
    men = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template("user/product_list.html",sho=men)

@app.route("/user/women")
def women():
    cursor = conn.cursor()
    cat_query  = "SELECT * FROM manage_subcat where cat_id = 13"
    cursor.execute(cat_query)
    women = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template("user/women.html",women=women)

@app.route("/user/womenlist<int:id>")
def women_list(id):   
    cursor = conn.cursor()
    cat_query  = "SELECT a.*, b.* FROM manage_cat as a, manage_prdct as b WHERE a.cat_id = b.cat_id AND b.cat_id = 13 AND b.subcat_id = %s"
    val=(id,)
    cursor.execute(cat_query,val)
    women = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template("user/product_list.html",sho=women)


@app.route("/user/kids")
def kids():
    cursor = conn.cursor()
    cat_query  = "SELECT * FROM manage_prdct where cat_id = 14"
    cursor.execute(cat_query)
    kid = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template("user/kids.html",kid=kid)


@app.route("/user/kidlist<int:id>")
def kid_list(id):   
    cursor = conn.cursor()
    cat_query  = "SELECT a.*, b.* FROM manage_cat as a, manage_prdct as b WHERE a.cat_id = b.cat_id AND b.cat_id = 14 AND b.subcat_id = %s"
    val=(id,)
    cursor.execute(cat_query,val)
    kid = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template("user/product_list.html",sho=kid)

# @app.route("/user/chkout")
# def chkout():
#     cursor = conn.cursor()
#     data = request.get_json()
#     name = data.get('name')
#     email = data.get('email')
#     address = data.get('address')
#     country = data.get('country')
#     state = data.get('state')
#     city = data.get('city')
#     pincode = data.get('pincode')
#     amt = data.get('amt')
#     user_id = session.get('user_id')
#     pymnt_method = session.get('pymnt_method')
#     order_number = str(random.randint(100000, 999999))

#     query = "SELECT * FROM add_to_cart WHERE  user_id = %s"
#     val = (user_id)
#     cursor.execute(query,val) 
#     account = cursor.fetchall()
#     for x in account:
#         proid=x[2]
#         cust_id=x[1]
#         qty=x[3]
#         query = "INSERT INTO order_tbl(order_num,user_id,prdct_id,qty,total_amt,pymnt_method) VALUES (%s,%s,%s,%s,%s,%s)"
#         cursor.execute(query, ( 
#                 order_number, user_id, proid, qty, amt, pymnt_method))
        
#         Wuery = "INSERT INTO order_details(user_id,name,email,address,country,state,city,pincode,pymnt_method) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#         cursor.execute(Wuery, (
#             cust_id,name,email,address,country,state,city,pincode,pymnt_method))
        
#     conn.commit()
#     cursor.close()
    
#     return render_template("user/Ulogin.html")


@app.route("/user/chkout", methods=["POST"])
def chkout():
    cursor = conn.cursor()
    data = request.get_json()
    
    name = data.get('name')
    u_email = data.get('u_email')
    mobile = data.get('mobile')
    address = data.get('address')
    country = data.get('country')
    state = data.get('state')
    city = data.get('city')
    pincode = data.get('pincode')
    amt = data.get('amt')
    print(name,u_email)
    user_id = session.get('user_id')
    pymnt_method = "Online"
    order_number = str(random.randint(100000, 999999))

    # Fetch all cart items
    query = "SELECT * FROM add_to_cart WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    cart_items = cursor.fetchall()

    order_id = None

    for idx, item in enumerate(cart_items):
        proid = item[2]
        cust_id = item[1]
        qty = item[3]
        
        # Insert into order_tbl
        query = """
            INSERT INTO order_tbl(order_num, user_id, prdct_id, qty,pymnt_method,total_amt)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            order_number, user_id, proid, qty,pymnt_method,amt))
        
        # Capture order_id from first insert
        if idx == 0:
            order_id = cursor.lastrowid

    # Insert user info once
    query = """
        INSERT INTO order_details(order_id,user_id, name, u_email, mobile, address, country, state, city, pincode, pymnt_method)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        order_id,user_id, name, u_email, mobile, address, country, state, city, pincode, pymnt_method))

    conn.commit()
    query="DELETE FROM add_to_cart WHERE user_id=%s"
    val = (user_id,)
    cursor.execute(query,val)
    conn.commit()
    
    cursor.close()

    print("Inserted order_id:", order_id)  # Optional debug

    return render_template("user/Ulogin.html")

# USER --------------------------------------------->>>



# SUPPLIER ------------------------------------------------->>

@app.route("/supplier/Slogin")
def Slogin():
    return render_template("supplier/slogin.html")

@app.route("/supplier/Slogin", methods=["POST"])
def supplier_login():
    cursor = conn.cursor()
    email_id = request.form['email_id']
    Pwd = request.form['pwd']
    query="SELECT * from supplier_reg WHERE email_id=%s and pwd=%s"
    val=(email_id,Pwd)
    cursor.execute(query,val)
    account=cursor.fetchone()
    cursor.close()
 
    if account:
        session['supp_id'] = account[0]
        session['email_id'] = account[4]
        session['supp_name'] = account[1]
        
        msg="Login Successfully"
        return render_template("supplier/sdashboard.html", msg=msg)
    else : 
      msg="Invalid credentials"
      return render_template("supplier/slogin.html", msg=msg)
    
@app.route('/supplier/Slogout')
def Slogout():
    session.pop('supp_id',None)
    session.pop('email_id',None)
    session.pop('supp_name',None)
    return redirect(url_for('login'))

@app.route("/supplier")
def supplier():
    return render_template("supplier/sdashboard.html")

@app.route("/supplier/addcateg")
def addcateg():
   return render_template("supplier/addcateg.html")

@app.route("/supplier/add_cat",methods=["POST"])
def add_cat():
    cursor= conn.cursor()
    cat_name=request.form['cat_name']
    description=request.form['description']
    supp_id = session['supp_id']
    query="INSERT INTO manage_cat(cat_name,description,supp_id) VALUES (%s,%s,%s)"
    val=(cat_name,description,supp_id)
    cursor.execute(query,val)
    conn.commit()
    cursor.close()
    return render_template("supplier/addcateg.html")

@app.route("/supplier/viewcateg")
def viewcateg():
    cursor = conn.cursor()
    query = "SELECT * from manage_cat"
    cursor.execute(query)
    categ = cursor.fetchall()
    cursor.close()
    return render_template("supplier/viewcateg.html", see=categ)

@app.route("/supplier/addprdct",methods=["POST"])
def addprdct():
    cursor = conn.cursor()
    cat_id = request.form['cat_id']
    prdct_name = request.form['prdct_name']
    description = request.form['description']
    price=request.form['price']
    p_image=request.files['p_image']
    filename = secure_filename(p_image.filename)
    p_image.save(os.path.join(UPLOAD_FOLDER,filename))
    path = os.path.join(UPLOAD_FOLDER,filename)
    p_status = request.form['p_status']
    query="INSERT INTO manage_prdct(cat_id,prdct_name,description,price,p_image,p_status) VALUES (%s,%s,%s,%s,%s,%s)"
    val = (cat_id,prdct_name,description,price,path,p_status)
    cursor.execute(query,val)
    conn.commit()
    cursor.close()
    msg='New Product Added Successfully'
    return redirect ('supprdct')

@app.route('/supplier/addprdct')
def supprdct():
    return render_template("supplier/addprdct.html")

@app.route("/supplier/viewprdct")
def viewprdct():
    cursor = conn.cursor()
    query = "SELECT * from manage_prdct"
    cursor.execute(query)
    product = cursor.fetchall()
    cursor.close()
    return render_template("supplier/viewprdct.html", lol=product)

@app.route("/supplier/vdispatcher")
def vdispatcher():
    cursor = conn.cursor()
    query = "SELECT * FROM manage_disp"
    cursor.execute(query)
    voo = cursor.fetchall()
    cursor.close()
    return render_template("supplier/viewdispatcher.html", loo=voo)

@app.route("/supplier/viewcustomer")
def viewcustomer():
    cursor = conn.cursor()
    query = "SELECT * FROM user_reg"
    cursor.execute(query)
    voo = cursor.fetchall()
    cursor.close()
    return render_template("supplier/vcustomer.html", choo=voo)

@app.route("/supplier/Sprofile")
def Sprofile():     
    return render_template("supplier/sprofile.html")


# SUPPLIER ------------------------------------------------->>



# DISPATCHER ------------------------------------------------->>

@app.route("/dispatcher")
def dispatcher():
    return render_template("dispatcher/disdashboard.html")

# DISPATCHER ------------------------------------------------->>
@app.route('/user/success',methods=['POST'])
def success():
    global oid
    cursor = conn.cursor()
    oid = request.form['oid']    
    print(oid)
    cust_id = session['r_id']
    query = "SELECT * FROM cart WHERE  c_id = %s"
    val = (cust_id)
    cursor.execute(query,val) 
    account = cursor.fetchall()
    for x in account:
        proid=x[1]
        cust_id=x[2]
        qty=x[3]
        oid=oid
        query = "INSERT INTO delivery(c_id,prod_id,m_trans,qty) VALUES (%s,%s,%s,%s)"
        val = (cust_id,proid,oid,qty)
        cursor.execute(query,val)  
        conn.commit()
    

    variable = cust_id    
    query = "delete from cart  WHERE c_id = %s "
    val = (variable)
    cursor.execute(query,val) 
    conn.commit() 
    cursor.close()
    st="0"
    return st


if __name__ =='__main__':
    app.run(debug=True)