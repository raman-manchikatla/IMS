#Establish a connection to the SQL server
from flask import Flask, jsonify, request, render_template
import sqlite3
conn = sqlite3.connect('ims.db')
app = Flask(__name__)

def idgenerator(tab):
    conn = sqlite3.connect('ims.db')
    cn = conn.cursor()
    idval = ''
    if tab=='CUSTOMER':
        idval = 'CUSTOMER_ID'
    if tab=='PRODUCT':
        idval = 'PRODUCT_ID'
    if tab=='ORDERS':
        idval = 'ORDER_ID'
    if tab=='SUPPLIER':
        idval = 'SUPPLIER_ID'
    print(tab,idval)
    cn.execute(f"SELECT {idval} FROM {tab}")
    new = cn.fetchall()
    cud = str(new[len(new)-1][0])
    for i in range(len(str(cud))):
        if cud[i].isnumeric():
            f = i
            break
    myint = cud[f:]
    myint = int(myint)+1
    return idval[0:3]+str(myint)


@app.route('/')   #routing the homepage
def home():
    return render_template('index.html')

@app.route('/show-customers')
def customer_show():
    conn = sqlite3.connect('ims.db')
    cn = conn.cursor()
    cn.execute("select * from customer")
    data = []
    for i in cn.fetchall():
        customer = {}
        customer['customer_id']=i[0]
        customer['customer_name']=i[1]
        customer['customer_address']=i[2]
        customer['customer_email']=i[3]
        data.append(customer)

    return render_template('showcustomers.html',data = data)


@app.route('/show-products')
def product_show():
    conn = sqlite3.connect('ims.db')
    cn = conn.cursor()
    cn.execute("select * from product")
    data = []
    for i in cn.fetchall():
        product = {}
        product['product_id']=i[0]
        product['product_name']=i[1]
        product['price']=i[2]
        product['stock']=i[3]
        product['supplier_id']=i[4]
        data.append(product)

    return render_template('showproducts.html',data=data)


@app.route('/show-supplier')
def supplier_show():
    conn = sqlite3.connect('ims.db')
    cn = conn.cursor()
    cn.execute("select * from supplier")
    data = []
    for i in cn.fetchall():
        supplier = {}
        supplier['supplier_id']=i[0]
        supplier['supplier_name']=i[1]
        supplier['supplier_address']=i[2]
        supplier['supplier_email']=i[3]
        data.append(supplier)
    return render_template('showsupplier.html',data=data)


@app.route('/show-orders')
def orders_show():
    conn = sqlite3.connect('ims.db')
    cn = conn.cursor()
    cn.execute("select * from orders")
    data = []
    for i in cn.fetchall():
        orders = {}
        orders['order_id']=i[0]
        orders['product_id']=i[1]
        orders['customer_id']=i[2]
        orders['quantity']=i[3]
        data.append(orders)


    return render_template('showorders.html',data=data)

@app.route('/add-customer',methods = ['GET','POST'])
def customer_add():
    if request.method == 'POST':
        conn= sqlite3.connect('ims.db')
        cn = conn.cursor()
        customer_name = request.form.get("name")   #from the addcustomers html file ID = "name"
        customer_address = request.form.get("address")
        customer_email = request.form.get("email")
        ID = idgenerator('CUSTOMER')
        cn.execute(f"insert into customer(customer_id,customer_name,customer_address,customer_email) values ('{ID}','{customer_name}','{customer_address}','{customer_email}')")
        conn.commit()
        print('Data has been Inserted')
        return jsonify({'message':'successful'})
    else:
        return render_template('addcustomer.html')

@app.route('/update-customer',methods = ['GET','POST'])
def customer_update():
    if request.method == 'POST':
        conn = sqlite3.connect('ims.db')
        cn = conn.cursor()
        customer_id = request.form.get("customer_id")   #from the addcustomers html file ID = "name"
        change = request.form.get("old_value")
        new_value = request.form.get("new_value")
        cn.execute(f"update customer set {change} = '{new_value}' where customer_id = '{customer_id}'")
        conn.commit()
        print('Data has been updated')
        return jsonify({'message':'successful'})
    else:
        return render_template('updatecustomer.html')
    
@app.route('/delete-customer', methods=['GET', 'POST'])
def customer_delete():
    if request.method == 'POST':
        customer_id = request.form.get("customer_id")
        conn = sqlite3.connect('ims.db')
        cn = conn.cursor()

        try:
            cn.execute("DELETE FROM ORDERS WHERE CUSTOMER_ID = ?", (customer_id,))
            cn.execute("DELETE FROM CUSTOMER WHERE CUSTOMER_ID = ?", (customer_id,))
            conn.commit()
            return jsonify({'message': 'successful'})
        except Exception as e:
            pass
            return jsonify({'message': 'error', 'error_message': str(e)})
        finally:
            cn.close()

    else:
        return render_template('deletecustomer.html')

    
@app.route('/add-product',methods = ['GET','POST'])
def product_add():
    if request.method == 'POST':
        conn = sqlite3.connect('ims.db')
        cn = conn.cursor()
        product_name = request.form.get("product_name")
        stock = request.form.get("stock")
        price = request.form.get("price")
        supplier_id = request.form.get("supplier_id")
        ID = idgenerator('PRODUCT')
        cn.execute(f"insert into product(product_id,product_name,stock,price,supplier_id) values ('{ID}','{product_name}','{stock}','{price}','{supplier_id}')")
        conn.commit()
        print('Data has been Inserted')
        return jsonify({'message':'successful'})
    else:
        return render_template('addproduct.html')
    
@app.route('/add-orders',methods=['GET','POST'])
def orders_add():
    if request.method == 'POST':
         conn = sqlite3.connect('ims.db')
         cn = conn.cursor()
         product_id=request.form.get('product_id')
         customer_id=request.form.get('customer_id')
         quantity=request.form.get('quantity')
         ID = idgenerator('ORDERS')
         cn.execute(f"insert into orders(order_id,product_id,customer_id,quantity)values('{ID}','{product_id}','{customer_id}','{quantity}')")
         conn.commit()
         print('Data has been inserted')
         return jsonify({'message':'sucessful'})
    else:
        return render_template('addorders.html')
    
@app.route('/add-supplier',methods=['GET','POST'])
def supplier_add():
    if request.method == 'POST':
         conn = sqlite3.connect('ims.db')
         cn = conn.cursor()
         supplier_name=request.form.get('supplier_name')
         supplier_address=request.form.get('supplier_address')
         supplier_email=request.form.get('supplier_email')
         ID = idgenerator('SUPPLIER')
         cn.execute(f"insert into supplier(supplier_id,supplier_name,supplier_address,supplier_email)values('{ID}','{supplier_name}','{supplier_address}','{supplier_email}')")
         conn.commit()
         print('data has been inserted')
         return jsonify({'message':'sucessful'})
    else:
        return render_template('addsupplier.html')
    
@app.route('/update-product',methods=['GET','POST'])
def product_update():
    if request.method == 'POST':
         conn = sqlite3.connect('ims.db')
         cn = conn.cursor()
         product_id=request.form.get("product_id")
         change=request.form.get("change")
         new_value=request.form.get("new_value")
         cn.execute(f"update product set {change}='{new_value}' where product_id = '{product_id}'")
         conn.commit()
         print('data has been updated')
         return jsonify({'message':'sucessful'})
    else:
         return render_template('updateproduct.html')
    
@app.route('/update-orders',methods=['GET','POST'])
def orders_update():
    if request.method == 'POST':
         conn = sqlite3.connect('ims.db')
         cn = conn.cursor()
         order_id=request.form.get("order_id")
         change=request.form.get("change")
         new_value=request.form.get("new_value")
         cn.execute(f"update orders set {change}='{new_value}' where order_id = '{order_id}'")
         conn.commit()
         print('data has been updated')
         return jsonify({'message':'sucessful'})
    else:
         return render_template('updateorders.html')
    
@app.route('/update-supplier',methods=['GET','POST'])
def supplier_update():
    if request.method == 'POST':
         conn = sqlite3.connect('ims.db')
         cn = conn.cursor()
         supplier_id=request.form.get("supplier_id")
         change=request.form.get("change")
         new_value=request.form.get("new_value")
         cn.execute(f"update supplier set {change}='{new_value}' where supplier_id = '{supplier_id}'")
         conn.commit()
         print('data has been updated')
         return jsonify({'message':'sucessful'})
    else:
         return render_template('updatesupplier.html')
    
@app.route('/delete-product', methods=['GET', 'POST'])
def product_delete():
    if request.method == 'POST':
        product_id = request.form.get("product_id")
        conn = sqlite3.connect('ims.db')
        cn = conn.cursor()

        try:
            cn.execute("DELETE FROM ORDERS WHERE product_id = ?", product_id)
            cn.execute("DELETE FROM product WHERE product_id = ?", product_id)  # Updated column name
            conn.commit()
            return jsonify({'message': 'successful'})
        except Exception as e:
            conn.rollback()
            return jsonify({'message': 'error', 'error_message': str(e)})
        finally:
            cn.close()
    else:
        return render_template('deleteproduct.html')
    
@app.route('/delete-orders', methods=['GET', 'POST'])
def orders_delete():
    if request.method == 'POST':
        order_id = request.form.get("order_id")
        conn = sqlite3.connect('ims.db')
        cn = conn.cursor()

        try:
            cn.execute("DELETE FROM ORDERS WHERE order_ID = ?", order_id)
            conn.commit()
            return jsonify({'message': 'successful'})
        except Exception as e:
            conn.rollback()
            return jsonify({'message': 'error', 'error_message': str(e)})
        finally:
            cn.close()
    else:
        return render_template('deleteorders.html')
    
@app.route('/delete-supplier', methods=['GET', 'POST'])
def supplier_delete():
    if request.method == 'POST':
        supplier_id = request.form.get("supplier_id")
        conn = sqlite3.connect('ims.db')
        cn = conn.cursor()

        try:
            # Delete related records in PRODUCT table first
            cn.execute("DELETE FROM PRODUCT WHERE supplier_id = ?", supplier_id)
            conn.commit()

            # Delete the supplier
            cn.execute("DELETE FROM supplier WHERE supplier_id = ?", supplier_id)
            conn.commit()

            return jsonify({'message': 'successful'})
        except Exception as e:
            conn.rollback()
            return jsonify({'message': 'error', 'error_message': str(e)})
        finally:
            cn.close()

    else:
        return render_template('deletesupplier.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = False)
