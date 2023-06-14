import sqlite3
conn = sqlite3.connect('ims.db')
cur = conn.cursor()
# cur.execute("CREATE TABLE CUSTOMER(CUSTOMER_ID VARCHAR(30), CUSTOMER_NAME VARCHAR(40), CUSTOMER_ADDRESS VARCHAR(30), CUSTOMER_EMAIL VARCHAR(40))")
# cur.execute('CREATE TABLE SUPPLIER(SUPPLIER_ID VARCHAR(30),SUPPLIER_NAME VARCHAR(40),SUPPLIER_ADDRESS VARCHAR(30),SUPPLIER_EMAIL VARCHAR(40))')
# cur.execute('CREATE TABLE PRODUCT(PRODUCT_ID VARCHAR(30),PRODUCT_NAME VARCHAR(40),STOCK INT,PRICE FLOAT,SUPPLIER_ID VARCHAR(30))')
# cur.execute('CREATE TABLE ORDERS(ORDER_ID VARCHAR(30),PRODUCT_ID VARCHAR(30),CUSTOMER_ID VARCHAR(30),QUANTITY INT)')
#cur.execute("insert into CUSTOMER values('cus1','raman','nzb','raman@gmail.com')")
cur.execute("insert into supplier values('SUP1','mithil','knr','mithil@gmail.com')")
conn.commit()

