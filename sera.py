from EmulatorGUI import GPIO
#import RPi.GPIO as GPIO
import time
import traceback
import sqlite3

con =sqlite3.connect("degerler.db");

cursor = con.cursor();

def Sıcaklıknormalguncelle():
    
    cursor.execute("SELECT * FROM sera ")
    data=cursor.fetchall()
    cursor.execute("UPDATE sera SET deger=30 WHERE isim='Sıcaklık'")
    cursor.execute("UPDATE sera SET Durum='Normal' WHERE isim='Sıcaklık'")
    print("SOn deger---")
    for i in data:
        print(i)
        con.commit()
def Sıcaklıkdikkatguncelle():
    
    cursor.execute("SELECT * FROM sera ")
    data=cursor.fetchall()
    cursor.execute("UPDATE sera SET deger=45 WHERE isim='Sıcaklık'")
    cursor.execute("UPDATE sera SET Durum='Dikkat' WHERE isim='Sıcaklık'")
    print("SOn deger---")
    for i in data:
        print(i)
        con.commit()
        
def Nemnormalguncelle():
    
    cursor.execute("SELECT * FROM sera ")
    data=cursor.fetchall()

    cursor.execute("UPDATE sera SET deger=50 WHERE isim='Nem'")
    cursor.execute("UPDATE sera SET Durum='Normal' WHERE isim='Nem'")
    print("SOn deger---")
    for i in data:
        print(i)
        con.commit()

def Nemdikkatguncelle():
    
    cursor.execute("SELECT * FROM sera")
    data=cursor.fetchall()
    cursor.execute("UPDATE sera SET deger=3 WHERE isim='Nem'")
    cursor.execute("UPDATE sera SET Durum='Dikkat' WHERE isim='Nem'")
    print("SOn deger---")
    for i in data:
        print(i)
        con.commit()
def Motordurguncelle():
    
    cursor.execute("SELECT * FROM sera ")
    data=cursor.fetchall()
    cursor.execute("UPDATE sera SET deger=0 WHERE isim='Motor'")
    cursor.execute("UPDATE sera SET Durum='Duruyor' WHERE isim='Motor'")
    print("SOn deger---")
    for i in data:
        print(i)
        con.commit()
def Motorcalısguncelle():
    
    cursor.execute("SELECT * FROM sera ")
    data=cursor.fetchall()
    cursor.execute("UPDATE sera SET deger=1 WHERE isim='Motor'")
    cursor.execute("UPDATE sera SET Durum='Calısıyor' WHERE isim='Motor'")
    print("SOn deger---")
    for i in data:
        print(i)
        con.commit()

def Sudurguncelle():
    
    cursor.execute("SELECT * FROM sera ")
    data=cursor.fetchall()
    cursor.execute("UPDATE sera SET deger=0 WHERE isim='Su Pompası'")
    cursor.execute("UPDATE sera SET Durum='Duruyor' WHERE isim='Su Pompası'")
    print("SOn deger---")
    for i in data:
        print(i)
        con.commit()
def Sucalısguncelle():
    
    cursor.execute("SELECT * FROM sera ")
    data=cursor.fetchall()
    cursor.execute("UPDATE sera SET deger=1 WHERE isim='Su Pompası'")
    cursor.execute("UPDATE sera SET Durum='Calısıyor' WHERE isim='Su Pompası'")
    print("SOn deger---")
    for i in data:
        print(i)
        con.commit()

def Main():
  
    try:
        GPIO.setmode(GPIO.BCM)

        GPIO.setwarnings(False)

        GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Su ver manuel
        GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Her Şeyi kapat
        GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Havalandırma motorunu aç manuel
        GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Sıcaklık 36 altı ve normal
        GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # Sıcaklık 36 ve üstü
        GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Nem normal
        GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Nem fazla

        GPIO.setup(4, GPIO.OUT, initial=GPIO.HIGH)  # Su verilme durumu
        GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH)  # Motor çalışma durumu
        GPIO.setup(9, GPIO.OUT, initial=GPIO.LOW)  # Sıcaklık Kontrolü altı
        GPIO.setup(19, GPIO.OUT, initial=GPIO.LOW)  # Nem kontrol
    
        while(True):
      
            if (GPIO.input(14) == True):

              print("Su Veriliyor..")
              GPIO.output(4,GPIO.LOW)
              Sucalısguncelle()
              time.sleep(7)
              print("NEm Normale döndü..")
              GPIO.output(19,GPIO.LOW)
              Nemnormalguncelle()
              time.sleep(5)
              GPIO.output(4,GPIO.HIGH)
              print("Su Kapatıldı..")
              Sudurguncelle()
              time.sleep(1)
        

            if (GPIO.input(18) == True):
              print("Motor Açık, Hava Üfleniyor..")
              GPIO.output(17,GPIO.LOW)
              Motorcalısguncelle()
              time.sleep(7)
              print("Sıcaklık Normale döndü..")
              Sıcaklıknormalguncelle()
              GPIO.output(9,GPIO.LOW)
              time.sleep(5)
              GPIO.output(17,GPIO.HIGH)
              print("Motor Kapatıldı..")
              Motordurguncelle()
              time.sleep(1)
          
              
            if (GPIO.input(15) == True):
              print("Motor ve Su Kapalı..")
              GPIO.output(17,GPIO.HIGH)
              GPIO.output(4,GPIO.HIGH)
              time.sleep(1)

            if (GPIO.input(25) == True):
              print("Sıcaklık 36 derece altı (Normal)..")
              GPIO.output(9,GPIO.LOW)
              Sıcaklıknormalguncelle()
              time.sleep(1)
              
            if (GPIO.input(8) == True):
              print("Sıcaklık 36 derece üstü DİKKAT!..")
              GPIO.output(9,GPIO.HIGH)
              Sıcaklıkdikkatguncelle()
              time.sleep(1)

            if (GPIO.input(16) == True):
              print("Nem (Normal)..")
              GPIO.output(19,GPIO.LOW)
              Nemnormalguncelle()
              time.sleep(1)
              
            if (GPIO.input(20) == True):
              print("Nem çok azaldı. Su veriniz.")
              GPIO.output(19,GPIO.HIGH)
              Nemdikkatguncelle()
              time.sleep(1)
              
        con.close()
    except Exception as ex:
        traceback.print_exc()
    finally:
        GPIO.cleanup()
Main()
