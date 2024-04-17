# Bezi deyishiklikler etdim :)

# Secimler 1: (1) Girish et (2) Qeydiyyatdan kec (3)Shifremi unutdum

# Secimler 2: (1) Oyuna basla (2) Balansi yoxla (3) Balansi artir (4) Isitfadechini bazadan sil (5) Cixish et

# Error mesajlari: 
# Giris: login ve ya parol yalnishdir, 
# Qeydiyyat: Login bazada movcuddur, yeni login yaradin
# Shifremi unutdum: login ve ya cavab yalnishdir
# Oyuna bashla: 1.Balans yoxdursa oyuna baslamaq mumkun olmasin.   2.Balansin menfiye getmesinin qarshisin alin.
# Istifadecini bazadan sil: shifre yalnishdir.   (silinmeni tesdiqlemek uchun yeniden shifre isteyir)

# Qeyd:
# Oyuna basladiqda ne qeder mebleg merc qoyacaginizi secirsiniz, 
# Uduzduqda qoyulan mebleg balansdan cixir, qazandiqda ise mebleg yerde qalan balansa 2 qat elave olunur.


import sqlite3
import random

db = sqlite3.connect("casinodata.db")

sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS casinodata(
            
            login VARCHAR(15) NOT NULL UNIQUE,
            password VARCHAR(50) NOT NULL,
            cash INTEGER DEFAULT 0,
            secret_question VARCHAR(50) NOT NULL
)""")



choice1 = int(input("(1) Giris et  (2) Qeydiyyatdan kec (3) Shifremi unutdum: "))
if choice1 == 1:
    login = input("Login daxil edin: ")
    password = input("Shifre daxil edin: ")
    while True:
        sql.execute(f"SELECT * FROM casinodata WHERE login = '{login}' and password = '{password}' ")
        if sql.fetchone():
            choice2 = int(input("(1) Oyuna bashla  (2) Balansi yoxla (3) Balansi artir (4) Istifadecini bazadan sil (5) Chixish et: "))

            if choice2 == 1:
                sql.execute(f"SELECT cash FROM casinodata WHERE login = '{login}'")
                cash = int("".join(map(str, sql.fetchone())))
                if cash > 0:
                    bet = int(input("Oynamaq istediyiniz meblegi daxil edin:  "))
                    if bet <= cash:
                        guess = int(input("1-5 arasinda reqem texmin edin: "))
                        num = random.randint(1,5)
                        if guess == num:
                            sql.execute(f"UPDATE casinodata SET cash = cash + '{bet}' WHERE login = '{login}'" )
                            db.commit()
                            print(f"Tebrikler, {bet * 2} AZN qazandiniz ! ") 
                        else:
                            sql.execute(f"UPDATE casinodata SET cash = cash - '{bet}' WHERE login = '{login}'" )
                            db.commit()
                            print(f"Siz uduzdunuz {bet} AZN.  Qazanan reqem: {num}")
                    else:
                        sql.execute(f"SELECT cash FROM casinodata WHERE login = '{login}' and password = '{password}'")
                        print("Kifayet qeder balans yoxdur! Balans:", "".join(map(str, sql.fetchone())), "AZN")
                else:
                    print("Zehmet olmasa balansi artirin.")

            elif choice2 == 2:
                sql.execute(f"SELECT cash FROM casinodata WHERE login = '{login}' and password = '{password}'")
                print("Balans:", "".join(map(str, sql.fetchone())), "AZN")

            elif choice2 == 3:
                cashin = int(input("Meblegi daxil edin: "))
                sql.execute(f"UPDATE casinodata SET cash = cash + '{cashin}' WHERE login = '{login}'" )
                db.commit()

                sql.execute(f"SELECT cash FROM casinodata WHERE login = '{login}' and password = '{password}'")
                print("Balans:", "".join(map(str, sql.fetchone())), "AZN")

            elif choice2 == 4:
                password = input("Istifadecini silmek ucun shifreni tesdiq edin: ")
                sql.execute(f"SELECT password FROM casinodata WHERE login = '{login}' and password = '{password}' ")
                if sql.fetchone():
                    sql.execute(f"DELETE FROM casinodata WHERE login = '{login}' and password = '{password}'")
                    db.commit()
                    print("Istifadeci ugurla silindi! ")
                    break
                else:
                    print("Shifre yalnishdir!")
                    break

            elif choice2 == 5:
                break

            else:
                print("Yalnish secim!")

        else:
            print("Yalnis login ve ya parol!")
            break


    
elif choice1 == 2:
    while True:
        login = input("Login daxil edin: ")
        logincheck = sql.execute(f"SELECT COUNT(*) FROM casinodata WHERE login = '{login}'")
        logincheck = int("".join(map(str, sql.fetchone())))
        if logincheck == 0:
            password = input("Shifre daxil edin: ")
            secret_question = input("Ilk evcil heyvaninizin adi: ")
            sql.execute(f"INSERT INTO casinodata(login, password, secret_question) VALUES('{login}', '{password}', '{secret_question}')")
            db.commit()
            print("Qeydiyyatdan ugurla kecdiniz.")
            break
        else:
            print("Bu login bazada movcuddur, yeni bir login daxil edin! ")
            

elif choice1 == 3:
    login = input("Login daxil edin: ")
    secret_question = input("Ilk evcil heyvaninizin adi: ")
    sql.execute(f"SELECT * FROM casinodata WHERE login = '{login}' and secret_question = '{secret_question}'")
    if sql.fetchone():
        newpass = input("Yeni pin daxil edin: ")
        sql.execute(f"UPDATE casinodata SET password = '{newpass}' WHERE login = '{login}' and secret_question = '{secret_question}'")
        db.commit()
        print("Shifre ugurla yenilendi.")
    else:
        print("Login ve ya cavab yalnishdir!")


else:
    print("Yalnish secim! ")
