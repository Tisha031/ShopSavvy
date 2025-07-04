from flask import Flask,render_template, url_for, request, redirect, session, flash,make_response
import pymysql
import os
from werkzeug.utils import secure_filename
from flask_session import Session
import random

from flask_mail import Mail, Message 
from xhtml2pdf import pisa
import io

app = Flask(__name__)
mail = Mail(app) # instantiate the mail class 
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB (adjust as needed)
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
    
    
    order_query = "SELECT COUNT(*) FROM order_tbl"
    cursor.execute(order_query)
    total_order = cursor.fetchone()[0]
    cursor.close()
    
    return render_template("admin/dashboard.html", total_cat=total_cat ,  total_prdct=total_prdct , total_supp=total_supp , total_user=total_user, total_disp=total_disp,total_order=total_order)

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
    return render_template("admin/viewproduct.html", msg=msg)

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
    return render_template("admin/viewstock_qty.html", see=category)  

 
@app.route("/admin/add_stock_post", methods=["POST"])
def add_stock_post():
    cursor = conn.cursor()

    btn = request.form['btn']                  # either "add" or "del"
    prod_id = request.form['product_id']       # product ID
    quantity = int(request.form['quantity'])   # quantity to add/remove

    # Fetch current product details
    cursor.execute("SELECT * FROM manage_prdct WHERE prdct_id = %s", (prod_id,))
    data = cursor.fetchone()

    if data:
        current_qty = data[6]  # Assuming qty is at index 7
        if btn == 'add':
            new_qty = current_qty + quantity
        else:  # 'del'
            new_qty = max(0, current_qty - quantity)  # avoid negative stock

        cursor.execute("UPDATE manage_prdct SET qty = %s WHERE prdct_id = %s", (new_qty, prod_id))
        conn.commit()

    cursor.close()
    return redirect(url_for('stock'))



@app.route("/admin/viewfeedback")
def viewfeedback():
    cursor = conn.cursor()
    sql = "SELECT * FROM feedback"
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.commit()
    return render_template("admin/viewfeedback.html", data=data)

@app.route("/admin/vieworderL")
def vieworderL():
    cursor = conn.cursor()
    sql = "SELECT a.* , b.*,  GROUP_CONCAT(c.prdct_name SEPARATOR ', ') AS products FROM order_details as a , order_tbl as b,manage_prdct as c WHERE a.detail_id=b.detail_id AND b.prdct_id=c.prdct_id GROUP BY b.date"
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.commit()
    return render_template("admin/vorderlist.html",data=data)



import io
import base64
from flask import render_template, make_response
from xhtml2pdf import pisa

@app.route('/download_pdf')
def download_pdf():
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    sql = """
        SELECT 
            a.name, a.mobile, a.address, a.city, a.state, a.pin_code,
            a.date, a.order_num, a.total_amt, a.total_qty, a.pymnt_method,
            GROUP_CONCAT(c.prdct_name SEPARATOR ', ') AS products
        FROM order_details AS a
        JOIN order_tbl AS b ON a.detail_id = b.detail_id
        JOIN manage_prdct AS c ON b.prdct_id = c.prdct_id
        GROUP BY a.detail_id;
    """
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()

    # Split the products for each row into list for template rendering
    for row in data:
        if row.get('products'):
            row['products'] = row['products'].split(', ')

    html = render_template('admin/vorderlist_pdf.html', data=data)

    # Ensure the HTML is encoded before passing to pisa
    result = io.BytesIO()
    pisa.CreatePDF(io.BytesIO(html.encode('utf-8')), dest=result)

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

from datetime import datetime
import base64, os
from PIL import Image
from io import BytesIO

@app.route('/add_to_bag', methods=['POST'])
def add_to_bag():
    user_id = session.get('user_id')
    prdct_id = request.form.get('prdct_id')
    custom_image_data = request.form.get('custom_image')

    if not user_id:
        return redirect(url_for('/user/Ulogin'))

    if not custom_image_data:
        return "No image received", 400

    try:
        header, encoded = custom_image_data.split(",", 1)
        image_data = base64.b64decode(encoded)
    except (ValueError, base64.binascii.Error):
        return "Invalid image data", 400

    # File saving setup
    filename = f"custom_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
    relative_path = f"static/custom/{filename}"
    full_path = os.path.join(relative_path)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # Convert and compress using Pillow
    try:
        image = Image.open(BytesIO(image_data))
        image = image.convert("RGB")
        image.save(full_path, format="PNG", quality=85)
    except Exception as e:
        return f"Error processing image: {e}", 500

    # Save to DB
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO add_to_bag(user_id, cust_id, qty, custom_image) VALUES (%s, %s, %s, %s)",
        (user_id, prdct_id, 1, relative_path)
    )
    conn.commit()
    cursor.close()

    return redirect(url_for('addTocartP'))

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
    msg='New Subcategory Added Successfully'
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
 
    return render_template("admin/viewsub_cat.html")


@app.route('/admin/delete_subcat/<int:subcat_id>')
def delete_subcat(subcat_id):
    cursor = conn.cursor()
    try:
        query = "DELETE FROM manage_subcat WHERE subcat_id  = %s"
        val = (subcat_id,)
        cursor.execute(query,val)
        conn.commit()
        msg='Delete Subcategory Successfully'
        return render_template("admin/viewsub_cat.html",msg=msg)
    finally:
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
        return render_template("admin/viewSupp.html",msg=msg)
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
    query = "SELECT * FROM manage_prdct ORDER BY prdct_id DESC LIMIT 4"
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
   
   
    query="INSERT INTO feedback(name,email,feed_cat,feed_des) VALUES (%s,%s,%s,%s)"
    val = (name,email,feed_cat,feed_des)
    
    cursor.execute(query,val)
    conn.commit()
    cursor.close()
    msg='feedback sent!'  
    return render_template("user/index.html", msg=msg)

@app.route("/user/customization")
def customization():
    cursor = conn.cursor()
    sql = "SELECT * FROM customization WHERE cust_id = 2"
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    return render_template("user/customization.html", data=results)




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
    cart_query = """
        SELECT a.cart_id, a.user_id, a.prdct_id, a.qty,
            b.prdct_name, b.p_image, b.price, NULL AS custom_image
        FROM add_to_cart AS a
        JOIN manage_prdct AS b ON a.prdct_id = b.prdct_id
        WHERE a.user_id = %s
        """
    cursor.execute(cart_query, (user_id,))
    cart_items = cursor.fetchall()

    # 2. Custom product cart
    custom_query = """
        SELECT a.bag_id, a.user_id, a.cust_id, a.qty,
            b.prdct_name, a.custom_image, b.price, b.img
        FROM add_to_bag AS a
        JOIN customization AS b ON a.cust_id = b.cust_id
        WHERE a.user_id = %s
    """
    cursor.execute(custom_query, (user_id,))
    custom_items = cursor.fetchall()

    all_items = cart_items + custom_items

        # 4. Calculate total and GST
    total = 0
    for item in all_items:
            try:
                total += item[3] * item[6]
            except TypeError:
                pass  # Skip items with invalid data

    gst = total * 5 /100
    gsttotal = total + gst

    cursor.close()

    
    # 3. Combine all items
    return render_template("user/checkout.html", detail=detail, cart=all_items ,total=total,gst=gst,gsttotal=gsttotal )

        # @app.route("/user/placeorder", methods=["POST"])
        # def placeorder():
        #     cursor = conn.cursor()
        #     user_id = session.get('user_id')

        #     if not user_id:
        #         return "User not logged in", 401

        #     # Get form data
        #     name = request.form['name']
        #     mobile = request.form['mobile']
        #     u_email = request.form['u_email']
        #     address = request.form['address']
        #     country = request.form['country']
        #     state = request.form['state']
        #     city = request.form['city']
        #     pin_code = request.form['pin_code']
        #     pymnt_method = request.form['pymnt_method']

        #     # Get all products
        #     cursor.execute("SELECT * FROM manage_prdct")
        #     prod = cursor.fetchall()

        #     # Get cart items
        #     cursor.execute("SELECT * FROM add_to_cart WHERE user_id = %s", (user_id,))
        #     cart_items = cursor.fetchall()

        #     if not cart_items:
        #         return "Cart is empty", 400

        #     # Insert order details
        #     cursor.execute("""
        #         INSERT INTO order_details(user_id, name, mobile, u_email, address, country, state, city, pin_code, pymnt_method)
        #         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        #     """, (user_id, name, mobile, u_email, address, country, state, city, pin_code, pymnt_method))
        #     conn.commit()
        #     detail_id = cursor.lastrowid

        #     # Generate common order info
        #     order_date = datetime.now().strftime("%Y-%m-%d")
        #     order_num = "ORD" + str(random.randint(10000, 99999))

        #     # Insert into order_tbl
        #     for item in cart_items:
        #         prdct_id = item[2]
        #         qty = item[3]

        #         price = next((p[3] for p in prod if p[0] == prdct_id), 0)
        #         total_amt = price * qty

        #         cursor.execute("""
        #             INSERT INTO order_tbl(detail_id, user_id, prdct_id, qty, total_amt, order_num, date)
        #             VALUES (%s, %s, %s, %s, %s, %s, %s)
        #         """, (detail_id, user_id, prdct_id, qty, total_amt, order_num, order_date))

        #     conn.commit()

        #     # Delete from cart after successful order
        #     cursor.execute("DELETE FROM add_to_cart WHERE user_id = %s", (user_id,))
        #     conn.commit()

        #     # Fetch order data to show / email
        #     cursor.execute("""
        #         SELECT 
        #             a.detail_id, a.user_id, a.name, a.u_email, a.mobile, a.address, a.country, a.state, a.city, a.pin_code,
        #             a.pymnt_method, b.order_id, b.order_num, b.date, b.prdct_id, b.qty, b.total_amt,
        #             c.prdct_name
        #         FROM order_details AS a
        #         JOIN order_tbl AS b ON a.detail_id = b.detail_id
        #         JOIN manage_prdct AS c ON b.prdct_id = c.prdct_id
        #         WHERE a.user_id = %s AND b.user_id = %s
        #     """, (user_id, user_id))
        #     order_data = cursor.fetchall()
        #     cursor.close()

        #     if not order_data:
        #         return "No orders found", 404

        #     total_amount = sum(item[16] for item in order_data)
        #     user_name = order_data[0][2]

        #     # Generate PDF
        #     pdf_io = generate_pdf('user/bill.html', {'data': order_data, 'total_amount': total_amount})
        #     if not pdf_io:
        #         return "Failed to generate PDF", 500

        #     # Send invoice email
        #     msg = Message(
        #         subject='Your SHOP SAVVY Order Invoice',
        #         sender='shopsavvy0310@gmail.com',
        #         recipients=[u_email]
        #     )
        #     msg.body = f"Dear {user_name},\n\nThank you for your purchase. Please find your invoice attached.\n\n- ShopSavvy"
        #     msg.attach("invoice.pdf", "application/pdf", pdf_io.read())
        #     mail.send(msg)

        #     return redirect('/')


def generate_pdf(template_name, context):
    html = render_template(template_name, **context)
    pdf_io = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf_io)
    if pisa_status.err:
        return None
    pdf_io.seek(0)
    return pdf_io

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
        cursor = conn.cursor()

        # Get cart items
        query_cart = """
            SELECT a.cart_id, a.user_id, a.prdct_id, a.qty, 
                b.prdct_name, b.p_image, b.price, NULL AS custom_image
            FROM add_to_cart AS a
            JOIN manage_prdct AS b ON a.prdct_id = b.prdct_id
            WHERE a.user_id = %s;
        """
        cursor.execute(query_cart, (user_id,))
        cart_items = cursor.fetchall()

        # Get custom products
        query_custom = """
            SELECT a.bag_id, a.user_id, a.cust_id, a.qty, 
                b.prdct_name, a.custom_image, b.price, b.img
            FROM add_to_bag AS a
            JOIN customization AS b ON a.cust_id = b.cust_id
            WHERE a.user_id = %s;
        """
        cursor.execute(query_custom, (user_id,))
        custom_items = cursor.fetchall()

        all_items = cart_items + custom_items

        # Calculate total and GST
        total = 0
        for item in all_items:
            try:
                total += item[3] * item[6]
            except TypeError:
                pass  

        gst = total * 5 /100
        gsttotal = total + gst

        cursor.close()
        

                
        return render_template("user/addTocart.html",cart=all_items,total=total,gsttotal=gsttotal,gst=gst)
    else:
        flash('please Login First','error')
        return redirect(url_for('Ulogin'))

@app.route("/user/atcqty", methods=['POST'])
def atcqty():
    cursor = conn.cursor()
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

@app.route('/user/delete_wish/<int:prdct_id>')
def delete_wish(prdct_id): 
    cursor = conn.cursor()
    query = "DELETE FROM wishlist WHERE prdct_id  = %s"
    cursor.execute(query, (prdct_id,))
    conn.commit()
    cursor.close()
    return redirect(url_for("wishlistt"))
        


@app.route("/user/my_account")
def my_account():
    u_email = session['user_id']
    cursor = conn.cursor()
    cat_query  = "SELECT * FROM user_reg where user_id = %s"
    val = (u_email)
    cursor.execute(cat_query,val)
    acont = cursor.fetchone()
    sql = "SELECT a.* , b.*, GROUP_CONCAT(c.prdct_name SEPARATOR ', ') AS products FROM order_details as a , order_tbl as b,manage_prdct as c WHERE a.detail_id=b.detail_id AND b.prdct_id=c.prdct_id AND a.user_id=%s GROUP BY b.date;"
    val=(acont[0])
    cursor.execute(sql,val)
    order=cursor.fetchall()
    cursor.close()
    return render_template("user/my_account.html",acont=acont,order=order)




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
    try:
        delete_cart_query = "DELETE FROM add_to_cart WHERE cart_id = %s"
        cursor.execute(delete_cart_query, (prdct_id,))

        if cursor.rowcount == 0:
            delete_bag_query = "DELETE FROM add_to_bag WHERE bag_id = %s"
            cursor.execute(delete_bag_query, (prdct_id,))
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
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
    cat_query  = "SELECT * FROM manage_subcat where cat_id = 14"
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
    email = data.get('email')  # Match frontend key
    mobile = data.get('mobile')
    address = data.get('address')
    country = data.get('country')
    state = data.get('state')
    city = data.get('city')
    pincode = data.get('pincode')
    amt = data.get('amt')
    user_id = session.get('user_id')
    pymnt_method = data.get('pymnt_method', 'Cash')  # default to Cash
    order_number = str(random.randint(100000, 999999))
    
    cursor.execute("SELECT * FROM user_reg WHERE user_id = %s",(user_id,))
    userdata = cursor.fetchone()

    # Fetch cart items
    cursor.execute("SELECT * FROM add_to_cart WHERE user_id = %s", (user_id,))
    cart_items = cursor.fetchall()

    order_id = None

    
    # Insert user details only once
    cursor.execute("""
        INSERT INTO order_details(user_id, name, u_email, mobile, address, country, state, city, pin_code, pymnt_method)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, ( user_id, name, email, mobile, address, country, state, city, pincode, pymnt_method))
    order_id = cursor.lastrowid
    for idx, item in enumerate(cart_items):
        product_id = item[2]
        quantity = item[3]

        cursor.execute("""
            INSERT INTO order_tbl(detail_id,order_num, user_id, prdct_id, qty, pymnt_method, total_amt)
            VALUES (%s,%s, %s, %s, %s, %s, %s)
        """, (order_id,order_number, user_id, product_id, quantity, pymnt_method, amt))

        
            

    # Clear cart after order
    cursor.execute("DELETE FROM add_to_cart WHERE user_id = %s", (user_id,))
    conn.commit()
    
    cursor.execute("""
        SELECT 
        o.order_num, 
        MAX(o.date) AS date, 
        SUM(o.total_amt) AS total_amt, 
        o.pymnt_method, 
        d.name, 
        d.mobile, 
        d.address, 
        d.city, 
        d.state, 
        d.pin_code, 
        GROUP_CONCAT(p.prdct_name SEPARATOR ', ') AS products, 
        SUM(o.qty) AS total_qty
    FROM order_tbl o
    JOIN order_details d ON o.detail_id = d.detail_id
    JOIN manage_prdct p ON p.prdct_id = o.prdct_id
    WHERE o.user_id = %s
    GROUP BY 
        o.order_num, 
        o.pymnt_method, 
        d.name, 
        d.mobile, 
        d.address, 
        d.city, 
        d.state, 
        d.pin_code
    ORDER BY date DESC
    LIMIT 1;
    """, (user_id,))

    latest_order = cursor.fetchone()

    # Convert the tuple to a dictionary to make it easier to access in the template
    latest_order_dict = {
        'order_num': latest_order[0],
        'date': latest_order[1],
        'total_amt': latest_order[2],
        'pymnt_method': latest_order[3],
        'name': latest_order[4],
        'mobile': latest_order[5],
        'address': latest_order[6],
        'city': latest_order[7],
        'state': latest_order[8],
        'pin_code': latest_order[9],
        'products': latest_order[10],  # ← Changed this
        'total_qty': latest_order[11]
    }


    # Generate the PDF, passing the order data and total amount
    pdf_io = generate_pdf('user/bill.html', {'data': [latest_order_dict], 'total_amount': latest_order[2]})
    if not pdf_io:
                return "Failed to generate PDF", 500

            # Send invoice email
    msg = Message(
                subject='Your SHOP SAVVY Order Invoice',
                sender='shopsavvy0310@gmail.com',
                recipients=[email]
            )
    msg.body = f"Dear {userdata[1]},\n\nThank you for your purchase. Please find your invoice attached.\n\n- ShopSavvy"
    msg.attach("invoice.pdf", "application/pdf", pdf_io.read())
    mail.send(msg)    

    
    cursor.close()

    return redirect(url_for("addTocartP"))

# USER --------------------------------------------->>>
@app.route("/user/viewbill", methods=['POST'])
def viewbill():
    cursor = conn.cursor()
    user_id = session['user_id']
    date = request.form["date"]
    
    cursor.execute("""
    SELECT 
    o.order_num, 
    MAX(o.date) AS date, 
    SUM(o.total_amt) AS total_amt, 
    MAX(o.pymnt_method) AS pymnt_method, 
    MAX(d.name) AS name, 
    MAX(d.mobile) AS mobile, 
    MAX(d.address) AS address, 
    MAX(d.city) AS city, 
    MAX(d.state) AS state, 
    MAX(d.pin_code) AS pin_code, 
    GROUP_CONCAT(p.prdct_name SEPARATOR ', ') AS products, 
    SUM(o.qty) AS total_qty
FROM order_tbl o
JOIN order_details d ON o.detail_id = d.detail_id
JOIN manage_prdct p ON p.prdct_id = o.prdct_id
WHERE o.user_id = %s AND o.date = %s
GROUP BY o.order_num
ORDER BY date DESC
LIMIT 1;

""", (user_id, date))  # 'date' = full datetime string from form

    latest_order = cursor.fetchone()

    if latest_order is None:
        cursor.close()
        return render_template("user/bill.html", data=[latest_order_dict])

    latest_order_dict = {
        'order_num': latest_order[0],
        'date': latest_order[1],
        'total_amt': latest_order[2],
        'pymnt_method': latest_order[3],
        'name': latest_order[4],
        'mobile': latest_order[5],
        'address': latest_order[6],
        'city': latest_order[7],
        'state': latest_order[8],
        'pin_code': latest_order[9],
        'products': latest_order[10].split(', '),  # optional: list format
        'total_qty': latest_order[11]
    }

    cursor.close()
    return render_template("user/bill.html", data=[latest_order_dict])

# SUPPLIER ------------------------------------------------->>
def check_sup():
    id = session.get('supp_id')
    if not id:
        return redirect('/supplier')
    return None

@app.route('/sdashboard')
def sdashboard():
    check=check_sup()
    if check:
        return check
    cursor = conn.cursor()
    prdct_query = "SELECT COUNT(*) FROM manage_prdct"
    cursor.execute(prdct_query)
    tl_prdct = cursor.fetchone()[0]
    
    
    
    user_query = "SELECT COUNT(*) FROM user_reg"
    cursor.execute(user_query)
    tl_user = cursor.fetchone()[0]
    
    disp_query = "SELECT COUNT(*) FROM manage_disp"
    cursor.execute(disp_query)
    tl_disp = cursor.fetchone()[0]
    
    
    order_query = "SELECT COUNT(*) FROM order_tbl"
    cursor.execute(order_query)
    tl_order = cursor.fetchone()[0]
    cursor.close()
    
    return render_template("supplier/sdashboard.html",  tl_prdct=tl_prdct , tl_user=tl_user, tl_disp=tl_disp,tl_order=tl_order)


@app.route("/supplier")
def slogin():
    return render_template("supplier/slogin.html")

@app.route("/supplier/Slogin", methods=["POST"])
def Slogin():
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
        session['profile_img'] = account[6]
        
        
        flash("Login Successfully")
        return redirect(url_for('sdashboard'))
    else:
        flash("Invalid Login")
        return redirect(url_for('slogin'))
        
   
    
@app.route('/supplier/Slogout')
def Slogout():
    session.pop('supp_id',None)
    session.pop('email_id',None)
    session.pop('supp_name',None)
    return redirect(url_for('slogin'))

@app.route("/supplier/sforgot")
def sforgot():
    return render_template("supplier/sforgot.html")

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

@app.route('/supplier/sdelete_category/<int:cat_id>')
def sdelete_category(cat_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM manage_cat WHERE cat_id = %s", (cat_id,))
    conn.commit()
    cursor.close()
    flash("Category deleted successfully.", "success")
    return redirect(url_for('viewcateg'))

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
    query = "SELECT a. *, b.*,c.subcat_name FROM manage_cat as a, manage_prdct as b,manage_subcat as c  WHERE a.cat_id = b.cat_id AND b.subcat_id = c.subcat_id"
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

@app.route("/supplier/vieworder")
def vieworder():
    cursor = conn.cursor()
    query = "SELECT a.* , b.*,  GROUP_CONCAT(c.prdct_name SEPARATOR ', ') AS products FROM order_details as a , order_tbl as b,manage_prdct as c WHERE a.detail_id=b.detail_id AND b.prdct_id=c.prdct_id GROUP BY b.date"
    cursor.execute(query)
    voo = cursor.fetchall()
    query = "SELECT * FROM manage_disp WHERE status = 0"
    cursor.execute(query)
    disp = cursor.fetchall()
    cursor.close()
    return render_template("supplier/vorder.html", cho=voo,disp=disp)

@app.route("/supplier/transfer",methods=['POST'])
def transfer():
    cursor=conn.cursor()
    disp_id = request.form['disp_id']
    id = request.form['id']
    sql = "UPDATE order_details SET disp_id = %s WHERE detail_id = %s"
    val = (disp_id,id)
    cursor.execute(sql,val)
    conn.commit()
    cursor.close()
    return redirect(url_for('vieworder'))


@app.route('/supplier/Vorderstatus')
def Vorderstatus():
    cursor = conn.cursor()
    query = "SELECT a.* , b.*,  GROUP_CONCAT(c.prdct_name SEPARATOR ', ') AS products FROM order_details as a , order_tbl as b,manage_prdct as c WHERE a.detail_id=b.detail_id AND b.prdct_id=c.prdct_id GROUP BY b.date"
    cursor.execute(query)
    voo = cursor.fetchall()
    query = "SELECT * FROM manage_disp WHERE status = 0"
    cursor.execute(query)
    disp = cursor.fetchall()
    cursor.close()
    return render_template("supplier/Vorderstatus.html",cho=voo)



@app.route("/supplier/Sprofile")
def Sprofile():     
    return render_template("supplier/sprofile.html")


@app.route('/supplier/subcat')
def subcat():
    cursor = conn.cursor()
    sql = "SELECT * FROM manage_cat"
    cursor.execute(sql)
    cursor.close()
    data = cursor.fetchall()
    return render_template("supplier/Asubcat.html",data=data)
@app.route("/supplier/Asubcat", methods=["POST"])
def Asubcat():
    try:
        cursor = conn.cursor()
        cat_id = request.form['cat_id']
        supp_id = request.form['supp_id']
        subcat_name = request.form['subcat_name']
        supp_desc = request.form['supp_desc']

        # Handle image upload
        img = request.files['img']
        filename = secure_filename(img.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        img.save(save_path)
        relative_path = os.path.join('static/uploads', filename)  # for frontend use

        # Insert into database
        query = "INSERT INTO manage_subcat (cat_id, supp_id, subcat_name, img, supp_desc) VALUES (%s, %s, %s, %s, %s)"
        val = (cat_id, supp_id, subcat_name, relative_path, supp_desc)
        cursor.execute(query, val)
        conn.commit()
        msg = 'New Subcategory Added Successfully'
    except Exception as e:
        conn.rollback()
        msg = f'Error occurred: {str(e)}'
    finally:
        cursor.close()
    
    return redirect(url_for('Asubcat', msg=msg))


@app.route('/supplier/ViSubcat')
def ViSubcat():
    cursor = conn.cursor()
    sql = "SELECT a.*, b.cat_name FROM manage_subcat as a, manage_cat as b WHERE a.cat_id=b.cat_id"
    cursor.execute(sql)
    cursor.close()
    doo = cursor.fetchall()
    return render_template("supplier/Vsubcat.html",doo=doo)



@app.route("/supplier/seditcat/<int:cat_id>")
def seditcat(cat_id):
    cursor = conn.cursor()
    query = "SELECT * FROM manage_cat WHERE cat_id = %s"
    cursor.execute(query, (cat_id,))
    category = cursor.fetchall()
    cursor.close()
    return render_template("supplier/seditcat.html", category=category)

@app.route("/supplier/editcat_process",methods=["POST"])
def editcat_process():
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
    return redirect(url_for('viewcateg', msg=msg))


# SUPPLIER ------------------------------------------------->>



#DISPATCHER ------------------------------------------------->>
@app.route("/dispatcher")
def dislogin():
    return render_template("dispatcher/dlogin.html")

@app.route("/disdashboard")
def disdashboard():
    cursor = conn.cursor()

    user_query = "SELECT COUNT(*) FROM user_reg"
    cursor.execute(user_query)
    t0l_user = cursor.fetchone()[0]
    
    order_query = "SELECT COUNT(*) FROM order_tbl"
    cursor.execute(order_query)
    t0l_order = cursor.fetchone()[0]
    cursor.close()
    
    return render_template("dispatcher/disdashboard.html",   t0l_user=t0l_user, t0l_order=t0l_order)

    

@app.route("/Dlogin", methods=["POST"])
def Dlogin():
    cursor = conn.cursor()
    email = request.form['email']
    password = request.form['password']
    query="SELECT * from manage_disp WHERE email=%s and password=%s"
    val=(email,password)
    cursor.execute(query,val)
    account=cursor.fetchone()
    cursor.close()
 
    if account:
        session['disp_id'] = account[0]
        session['email'] = account[3]
        session['name'] = account[1]        
        flash("Login Successfully")
        return redirect(url_for('disdashboard'))
    else:
        flash("Invalid Login")
        return redirect(url_for('dlogin'))
        
   
    
@app.route('/dispatcher/dlogout')
def dlogout():
    session.pop('disp_id',None)
    session.pop('email',None)
    session.pop('name',None)
    return render_template("dispatcher/dlogin.html")


@app.route("/dispatcher/dprofile")
def dprofile():     
    return render_template("dispatcher/dprofile.html")

@app.route("/dispatcher/dvieworder")
def dvieworder():     
    cursor = conn.cursor()
    sql = "SELECT a.* , b.*, GROUP_CONCAT(c.prdct_name SEPARATOR ', ') AS products FROM order_details as a , order_tbl as b,manage_prdct as c WHERE a.detail_id=b.detail_id AND b.prdct_id=c.prdct_id GROUP BY b.date"
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.commit()
    return render_template("dispatcher/dvieworder.html" ,data=data)

@app.route("/orderstatus", methods=['POST'])
def orderstatus():
    try:
        cursor = conn.cursor()
        id = request.form['id']
        status = int(request.form['status'])
        if status == 0:
            sql = "UPDATE order_details SET status=1 WHERE detail_id = %s"
        else: 
            sql = "UPDATE order_details SET status=0 WHERE detail_id = %s"
        cursor.execute(sql, (id,))
        conn.commit()
    except Exception as e:
        print(f"Error updating order status: {e}")
        # Optional: flash message or redirect to error page
    return redirect('/dispatcher/dvieworder')

    

@app.route("/dispatcher/dviewcust")
def dviewcust():  
    cursor = conn.cursor()
    sql = "SELECT * FROM user_reg"   
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template("dispatcher/dviewcust.html",data=data)


# DISPATCHER ------------------------------------------------->>


if __name__ =='__main__':    
    app.run(debug=True)