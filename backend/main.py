import os
import urllib.parse as up
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
from model import Review
load_dotenv()

up.uses_netloc.append("postgres")
url = up.urlparse(os.environ["DATABASE_URL"])
conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def get_prod(product_id:int):
    cur = conn.cursor()
    cur.execute('SELECT * FROM product WHERE product_id = %s', (product_id,))
    rows = cur.fetchall()
    returndat=[]
    for row in rows:
        data={
            'product_id':row[0],
            'name':row[1],
            'description':row[2],
            'price':row[3]
            }
        returndat.append(data)
    
    return returndat

def insert_prod(product_id:str, product_name:str,product_desc:str, product_price:float):
    cur = conn.cursor()
    # INSERT INTO product (product_id, name, description, price) VALUES ('P001', 'Smartphone', 'High-performance smartphone with advanced features', 59999.99);
    cur.execute('INSERT INTO product (product_id, name, description, price) VALUES (%s, %s, %s,%s)', (product_id, product_name,product_desc, product_price))
    conn.commit()

def get_customer(customer_id:int):
    cur = conn.cursor()
    cur.execute('SELECT * FROM customer WHERE customer_id = %s', (customer_id,))
    rows = cur.fetchall()
    return rows

def insert_customer(customer_id:str, customer_name:str,customer_email:str, customer_phone:str):
    cur = conn.cursor()
    
@app.route('/', methods=['GET'])
def index():
    return "hello"

@app.route('/getproduct', methods=['GET'])
def getproduct():
    product_id = request.args.get('product_id')
    return jsonify(get_prod(product_id))


def check_exists(userid:str):
    cur = conn.cursor()
    cur.execute("SELECT * FROM customer WHERE customer_id = %s", (userid,))
    rows = cur.fetchall()
    if len(rows)>0:
        return jsonify({"exists":'present'})
    else:
        return jsonify({"exists":'absent'})
    
@app.route('/userexists', methods=['GET'])
def userexists():
    userid=request.args.get('inputID')
    print(userid)
    h=(check_exists(userid))
    return h

@app.route('/userproducts', methods=['POST'])
def userproducts():
    userid=request.json['inputID']
    cur = conn.cursor()
    cur.execute("SELECT p.name,pu.purchase_id,p.price FROM product p JOIN purchase pu ON p.product_id = pu.product_id WHERE pu.customer_id = %s", (userid,))
    rows = cur.fetchall()
    returndat=[]
    i=1
    for row in rows:
        cur=conn.cursor()
        cur.execute("SELECT * FROM complaint WHERE purchase_id = %s", (row[1],))
        if len(cur.fetchall())>0:
            complaint=True
        else:
            complaint=False
        print(complaint)
        data={
            'serialNumber':i,
            'name':row[0],
            'pid':row[1],
            'price':str(row[2]),
            "complaint":complaint #purchase id there
            }
        
        i=i+1
        returndat.append(data)
    return jsonify(returndat)

@app.route('/addcomplaint', methods=['POST'])
def addcomplaint():
    purchase_id=request.json['inputID']
    description=request.json['complaint']

    #get the customer id from purchase table
    cursor = conn.cursor()
    query = "SELECT customer_id FROM purchase WHERE purchase_id = %s;"
    cursor.execute(query, (purchase_id,))
    result = cursor.fetchone()
    if result:
        customer_id = result[0]
        print(f"Customer ID for purchase ID {purchase_id} is {customer_id}")
        complaint_id = "CM"+purchase_id[2:]+ customer_id[1:] + datetime.now().strftime("%Y%m%d%H%M%S")
        opening_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        '''import model here to update the severity rating'''

        review = Review()
    
        severity_rating=review.predict(description)

        cur = conn.cursor()
        cur.execute("INSERT INTO complaint (complaint_id, customer_id, purchase_id,description, opening_date, closing_date, severity) VALUES (%s, %s, %s,%s, %s, NULL, %s)", (complaint_id, customer_id, purchase_id,description, opening_date,severity_rating))
        conn.commit()


        #insert in service table
        insert_query = """
        INSERT INTO Service (Complaint_ID, Purchase_ID, Customer_ID, Complaint_Status)
        VALUES (%s, %s, %s, %s);
        """
        cursor.execute(insert_query, (complaint_id, purchase_id, customer_id, "In progress"))

        # Step 4: Commit the transaction
        conn.commit()

        return jsonify({"status":"success"})

        #add entry to service table

    else:
        print(f"No customer found for purchase ID {purchase_id}")
        return jsonify({"status":"failed"})
    #make complaint id with purchase id+customerid+datetime

@app.route('/servicestatus', methods=['POST'])
def servicestatus():
    purchase_id=request.json['inputID']
    cursor = conn.cursor()
    query = """
    SELECT s.Purchase_ID, s.Complaint_ID,  c.Description,s.Complaint_Status, c.Severity
    FROM Service s
    JOIN Complaint c ON s.Complaint_ID = c.Complaint_ID
    WHERE s.Purchase_ID = %s;
    """

    # Execute the query
    cursor.execute(query, (purchase_id,))

    # Fetch all the rows
    rows = cursor.fetchall()
    returndat=[]
    i=1
    for row in rows:
        data={
            'serialNumber':i, #change this to a counter
            'purchase_id':row[0],
            'complaint_id':row[1],
            'description':row[2],
            'status':row[3],
            'severity':row[4]
            }
        returndat.append(data)
        i+=1
    print(returndat,"returndat")
    return jsonify(returndat)

@app.route('/Feedback', methods=['POST'])
def feedback():
    complaint_id=request.json['inputID']
    feedbackrating=request.json['rating']
    feedback=request.json['feedback']
    cursor = conn.cursor()
    query = """
    UPDATE Service
    SET Feedback = %s
    SET Feedback_Rating = %s
    WHERE Complaint_ID = %s;
    """
    # Execute the query
    cursor.execute(query, (feedback,int(feedbackrating),complaint_id))

    # Commit the transaction
    conn.commit()
    return jsonify({"status":"success"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')