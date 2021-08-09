from tkinter import *
from tkinter import messagebox,Menu
import requests
import json
import sqlite3

pycrypto = Tk()
pycrypto.title("my crypto portle")
# pycrypto.iconbitmap('sym.ico')

con = sqlite3.connect('coin.db')
cursorObj = con.cursor()
cursorObj.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY , symbol TEXT, amount INTEGER, price REAL)")
con.commit()



def reset():
    for cell in pycrypto.winfo_children():
        cell.destroy()
         
        
    app_navigator()
    app_header()
    my_portfolio()

def app_navigator():
    def clear_all():
        cursorObj.execute('DELETE FROM coin')
        con.commit()
        
        messagebox.showinfo('portal notification','clear the nortal-add new iteam')
        reset()

    def close_portal():
        pycrypto.destroy()


    menu=Menu(pycrypto)
    file_item=Menu(menu)
    file_item.add_command(label='clear my portal',command=clear_all)
    file_item.add_command(label='close app',command=close_portal)
    menu.add_cascade(label='file',menu=file_item)
    pycrypto.config(menu=menu)

def my_portfolio():

    api_requests = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=200&convert=INR&CMC_PRO_API_KEY=80e5a3c1-fd89-420a-85c4-4ac99f6ff532")
    api = json.loads(api_requests.content)

    cursorObj.execute("SELECT * FROM coin")
    coins = cursorObj.fetchall()
    
    def font_color(amount):
        if amount>= 0:
            return "green"
        else:
            return "red"
     
    def insert_coin():
        cursorObj.execute("INSERT INTO coin(symbol,price,amount) VALUES(?,?,?) ",(symbol_txt.get(),price_txt.get(),amount_txt.get()))
        con.commit()
        messagebox.showinfo("portfollio notification","coin Added to portle Successfully")
        reset()

    def update_coin():
        cursorObj.execute("UPDATE coin SET symbol=?, price=?, amount=? WHERE id=?", (symbol_update.get(), price_update.get(), amount_update.get(),portid_update.get()))
        con.commit()
        messagebox.showinfo("portfollio notification","coin Update to portle Successfully")
        
        reset()

    def delete_coin():
        cursorObj.execute("DELETE FROM coin WHERE id=?", (portid_delete.get(),))
        con.commit()
        messagebox.showinfo("portfollio notification","coin Delete to portle Successfully")
        reset()

    total_pl = 0
    coin_row =1
    total_current_value = 0
    total_amount_paid = 0

    for i in range(0,200):
        for coin in coins:
            if api["data"][i]["symbol"] == coin[1]:
                total_paid = coin[2] * coin[3]
                current_value = coin[2] * api["data"][i]["quote"]["INR"]["price"]
                pl_percoin =  api["data"][i]["quote"]["INR"]["price"] - coin[3]
                total_pl_coin = pl_percoin * coin[2]

                total_pl = total_pl + total_pl_coin
                total_current_value = total_current_value + current_value 
                total_amount_paid = total_amount_paid + total_paid

                # print(api["data"][i]["name"] +"-"+ api["data"][i]["symbol"])
                # print("price - RS.{0:.2f}".format(api["data"][i]["quote"]["INR"]["price"]))
                # print("number of coin: ",coin["amount_owned"])
                # print("total amount paid:","RS.{0:.2f}".format(total_paid))
                # print("current value is:","RS.{0:.2f}".format(current_value))
                # print("P/L percoin:","RS.{0:.2f}".format(pl_percoin))
                # print("Total P/L with coin:","RS.{0:.2f}".format(total_pl_coin))
                # print("-----------")
  
  
                portfolio_id = Label(pycrypto, text=coin[0],bg="Bisque",fg="black", font="Lato 12 bold", padx="4",pady="5",borderwidth=3,relief="groove")
                portfolio_id.grid(row=coin_row , column=0,sticky=N+E+W+S)

                name = Label(pycrypto, text=api["data"][i]["symbol"],bg="Bisque",fg="black", font="Lato 12 bold", padx="4",pady="5",borderwidth=3,relief="groove")
                name.grid(row=coin_row , column=1,sticky=N+E+W+S)

                price = Label(pycrypto, text="RS.{0:.2f}".format(api["data"][i]["quote"]["INR"]["price"]),bg="Bisque",fg="black", font="Lato 12 bold", padx="4",pady="5",borderwidth=3,relief="groove")
                price.grid(row=coin_row , column=2,sticky=N+E+W+S)

                no_coin = Label(pycrypto, text=coin[2],bg="Bisque",fg="black", font="Lato 12 bold", padx="4",pady="5",borderwidth=3,relief="groove")
                no_coin.grid(row=coin_row , column=3,sticky=N+E+W+S)

                amount_paid = Label(pycrypto,text="RS.{0:.2f}".format(total_paid),bg="Bisque",fg="black", font="Lato 12 bold", padx="4",pady="5",borderwidth=3,relief="groove")
                amount_paid.grid(row=coin_row , column=4,sticky=N+E+W+S)
                

                current_val = Label(pycrypto, text="RS.{0:.2f}".format(current_value),bg="Bisque",fg="black", font="Lato 12 bold", padx="4",pady="5",borderwidth=3,relief="groove")
                current_val.grid(row=coin_row , column=5,sticky=N+E+W+S)

                pl_coin = Label(pycrypto, text="RS.{0:.2f}".format(pl_percoin),bg="Bisque",fg=font_color(float("{0:.2f}".format(pl_percoin))), font="Lato 12 bold", padx="4",pady="5",borderwidth=3,relief="groove")
                pl_coin.grid(row=coin_row , column=6,sticky=N+E+W+S)

                totalpl = Label(pycrypto, text="RS.{0:.2f}".format(total_pl_coin),bg="Bisque",fg=font_color(float("{0:.2f}".format(total_pl_coin))), font="Lato 12 bold", padx="4",pady="5",borderwidth=3,relief="groove")
                totalpl.grid(row=coin_row , column=7,sticky=N+E+W+S)

                

                coin_row = coin_row + 1
                

    #insert data    

    

    symbol_txt = Entry(pycrypto,borderwidth=3,relief="groove")        
    symbol_txt.grid(row=coin_row+1,column=1)

    price_txt = Entry(pycrypto,borderwidth=3,relief="groove")        
    price_txt.grid(row=coin_row+1,column=2)

    amount_txt = Entry(pycrypto,borderwidth=3,relief="groove")        
    amount_txt.grid(row=coin_row+1,column=3)

    add_coin = Button(pycrypto, text="Ad coin",bg="blue",fg="white",command=insert_coin, font="Lato 12 bold", padx="4",pady="5",borderwidth=3,relief="groove")
    add_coin.grid(row=coin_row+1, column=4,sticky=N+E+W+S)

    #update values
    portid_update = Entry(pycrypto,borderwidth=3,relief="groove")        
    portid_update.grid(row=coin_row+2,column=0)

    symbol_update = Entry(pycrypto,borderwidth=3,relief="groove")        
    symbol_update.grid(row=coin_row+2,column=1)

    price_update = Entry(pycrypto,borderwidth=3,relief="groove")        
    price_update.grid(row=coin_row+2,column=2)

    amount_update = Entry(pycrypto,borderwidth=3,relief="groove")        
    amount_update.grid(row=coin_row+2,column=3)

    update_coin_txt = Button(pycrypto, text="Update Coin",bg="blue",fg="white",command=update_coin, font="Lato 12 bold", padx="4",pady="5",borderwidth=3,relief="groove")
    update_coin_txt.grid(row=coin_row+2, column=4,sticky=N+E+W+S)


    #delete values
    portid_delete = Entry(pycrypto,borderwidth=3,relief="groove")        
    portid_delete.grid(row=coin_row+3,column=0)

    delete_coin_txt = Button(pycrypto, text="Delete Coin",bg="blue",fg="white",command=delete_coin, font="Lato 12 bold", padx="4",pady="5",borderwidth=3,relief="groove")
    delete_coin_txt.grid(row=coin_row+3, column=4,sticky=N+E+W+S)


    totalap = Label(pycrypto, text="RS.{0:.2f}".format(total_amount_paid),bg="Bisque",fg="black", font="Lato 12 bold", padx="4",pady="5",borderwidth=3,relief="groove")
    totalap.grid(row=coin_row , column=4,sticky=N+E+W+S)

    totalcv = Label(pycrypto, text="RS.{0:.2f}".format(total_current_value),bg="Bisque",fg="black", font="Lato 12 bold", padx="4",pady="5",borderwidth=3,relief="groove")
    totalcv.grid(row=coin_row , column=5,sticky=N+E+W+S)

    totalpl = Label(pycrypto, text="RS.{0:.2f}".format(total_pl),bg="Bisque",fg="black", font="Lato 12 bold", padx="4",pady="5",borderwidth=3,relief="groove")
    totalpl.grid(row=coin_row , column=7,sticky=N+E+W+S)

    # api = ""
    Refresh = Button(pycrypto, text="Refresh",bg="blue",fg="white",command=reset, font="Lato 12 bold", padx="4",pady="5",borderwidth=3,relief="groove")
    Refresh.grid(row=coin_row+1, column=7,sticky=N+E+W+S)


def app_header():
    

    portfolio_id = Label(pycrypto, text="Portfolio ID",bg="GreenYellow",fg="black", font="Lato 12 bold", padx="4",pady="5",borderwidth=3, relief="groove")
    portfolio_id.grid(row=0 , column=0,sticky=N+E+W+S)

    name = Label(pycrypto, text="Coin Name",bg="GreenYellow",fg="black", font="Lato 12 bold", padx="4",pady="5",borderwidth=3, relief="groove")
    name.grid(row=0 , column=1,sticky=N+E+W+S)

    price = Label(pycrypto, text="Price",bg="GreenYellow",fg="black", font="Lato 12 bold", padx="4",pady="5",borderwidth=3, relief="groove")
    price.grid(row=0 , column=2,sticky=N+E+W+S)

    no_coin = Label(pycrypto, text="Coin Owned",bg="GreenYellow",fg="black", font="Lato 12 bold", padx="4",pady="5",borderwidth=3, relief="groove")
    no_coin.grid(row=0 , column=3,sticky=N+E+W+S)

    amount_paid = Label(pycrypto, text="Total Amount Paid",bg="GreenYellow",fg="black", font="Lato 12 bold", padx="4",pady="5",borderwidth=3, relief="groove")
    amount_paid.grid(row=0 , column=4,sticky=N+E+W+S)

    current_val = Label(pycrypto, text="Current Value",bg="GreenYellow",fg="black", font="Lato 12 bold", padx="4",pady="5",borderwidth=3, relief="groove")
    current_val.grid(row=0 , column=5,sticky=N+E+W+S)

    pl_coin = Label(pycrypto, text="P/L Per coin",bg="GreenYellow",fg="black", font="Lato 12 bold", padx="4",pady="5",borderwidth=3, relief="groove")
    pl_coin.grid(row=0 , column=6,sticky=N+E+W+S)

    total_pl = Label(pycrypto, text="Total P/L With Coin",bg="GreenYellow",fg="black", font="Lato 12 bold", padx="4",pady="5",borderwidth=3, relief="groove")
    total_pl.grid(row=0 , column=7,sticky=N+E+W+S)

app_navigator()
app_header()
my_portfolio()
pycrypto.mainloop()

cursorObj.close()
con.close()
