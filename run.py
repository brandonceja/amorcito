from flask import Flask
from flask import render_template, request
import pyodbc
from datetime import date, datetime

server = "127.0.0.1"
username = "python"
password = "SFpJZhYSiLinBBf0Kq9N"



app = Flask(__name__)



@app.route("/")
def index():
    cnxn = pyodbc.connect(r'Driver=SQL Server;Server=.\SQLEXPRESS;Database=ContribucionInterbancaria;Trusted_Connection=yes;UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()

    cursor.execute("SELECT B.idBanco,B.nombreBanco,D.compraActual,D.ventaActual FROM Bancos B LEFT JOIN dolarBancos D ON B.idBanco = D.idBanco")

    bancos = []

    while 1:
        row = cursor.fetchone()
        if not row:
            break
        bancos.append(row)
    cnxn.close()

    return render_template("index.html", data_bancos=bancos)

@app.route("/bancos/<int:id_banco>", methods=["GET", "POST"])
def banco(id_banco):

    banco = []

    if request.method == "POST":
        cactual = request.form['cactual']
        vactual = request.form['vactual']
        c24h = request.form['c24']
        v24h = request.form['v24']
        c48h = request.form['c48']
        v48h = request.form['v48']

        cnxn = pyodbc.connect(r'Driver=SQL Server;Server=.\SQLEXPRESS;Database=ContribucionInterbancaria;Trusted_Connection=yes;UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        
        cursor.execute("EXEC ManageBancos 'UPDATE',NULL,"+str(id_banco)+",3,"+vactual+","+cactual+","+c24h+","+v24h+","+c48h+","+v48h+",'"+current_time+"',1")
        cnxn.commit()

        cnxn.close()


    cnxn = pyodbc.connect(r'Driver=SQL Server;Server=.\SQLEXPRESS;Database=ContribucionInterbancaria;Trusted_Connection=yes;UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()

    cursor.execute("SELECT * FROM Bancos B LEFT JOIN dolarBancos D ON B.idBanco = D.idBanco WHERE B.idBanco ="+str(id_banco))
            

    while 1:
        row = cursor.fetchone()
        if not row:
            break
        banco.append(row)
    cnxn.close()

    return render_template("banco.html", data_banco=banco)