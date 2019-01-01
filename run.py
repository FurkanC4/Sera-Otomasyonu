from flask import Flask, render_template, request
import sqlite3 as sql
import time
import traceback
import sqlite3

app = Flask(__name__)

@app.route('/my-link/')
def my_link():
   con =sqlite3.connect("degerler.db");
   cur = con.cursor()
   cur.execute("UPDATE sera SET Durum='Kapalı' WHERE isim='Motor'")
   cur.execute("UPDATE sera SET deger='0' WHERE isim='Motor'")
   cur.execute("UPDATE sera SET Durum='Kapalı' WHERE isim='Sıcaklık'")
   cur.execute("UPDATE sera SET deger='0' WHERE isim='Sıcaklık'")
   cur.execute("UPDATE sera SET Durum='Kapalı' WHERE isim='Nem'")
   cur.execute("UPDATE sera SET deger='0' WHERE isim='Nem'")
   cur.execute("UPDATE sera SET Durum='Kapalı' WHERE isim='Su Pompası'")
   cur.execute("UPDATE sera SET deger='0' WHERE isim='Su Pompası'")

   con.commit()
   return "Başarılı Elektrik Kesildi !"

@app.route('/my-link2/')
def my_link2():
   con =sqlite3.connect("degerler.db");
   
   cur = con.cursor()
   cur.execute("UPDATE sera SET Durum='Calısıyor' WHERE isim='Motor'")
   cur.execute("UPDATE sera SET Deger='1' WHERE isim='Motor'")

   con.commit()
   return "Motorunuz Çalışıyor Emulatörden Görebilirsiniz !"


@app.route('/')
def home():
   return render_template('home.html')

@app.route('/enternew')
def new_student():
   return render_template('bos.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         isim = request.form['isim']
         Durum = request.form['Durum']
         deger = request.form['deger']
    
         with sql.connect("degerler.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO sera (isim,Durum,deger)  VALUES (?,?,?,?)",(isim,Durum,deger) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sql.connect("degerler.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from sera")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

if __name__ == '__main__':
   app.run(debug = True)

