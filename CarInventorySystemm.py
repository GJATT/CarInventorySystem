import contextlib
from tkinter import*
from tkinter import ttk
import random
import time
import datetime
from tkinter import messagebox
import mysql.connector


class Car:
    def __init__(self,root):
        self.root=root
        self.root.title("Car Inventory System")
        self.root.geometry("1540x800+0+0")


        self.SaleID=StringVar()
        self.SalePrice=StringVar()
        self.CName=StringVar()
        self.LPN=StringVar()
        self.DOS=StringVar()

        lbltitle=Label(self.root,bd=20,relief=RIDGE,text="Car Inventory System",fg="Green",bg="white",font=("times new roman",50,"bold"))
        lbltitle.pack(side=TOP,fill=X)

        # ====================================DataFrame=====================================
        Dataframe=Frame(self.root,bd=20,relief=RIDGE)
        Dataframe.place(x=0,y=130,width=1530,height=400)

        DataFrameLeft=LabelFrame(Dataframe,bd=10,relief=RIDGE, padx=10,
                                 font=("times new roman",15,"bold"),text="Sale Information")
        DataFrameLeft.place(x=0,y=5,width=400,height=250)

        DataFrameRight=LabelFrame(Dataframe,bd=10,relief=RIDGE,padx=10,
                                 font=("times new roman",15,"bold"),text="Sale/Purchase Information")
        DataFrameRight.place(x=1010,y=5,width=460,height=250)

        # =========================== buttons frame ==========================


        Buttonframe=Frame(self.root,bd=20,relief=RIDGE)
        Buttonframe.place(x=0,y=530,width=1530,height=130)


        # =========================== Details Frame ==================================

        Detailsframe = Frame(self.root,bd=20,relief=RIDGE)
        Detailsframe.place(x=0,y=600,width=1530,height=190)

        # ============================== DataFrameLeft ===================================

        lblSaleID=Label(DataFrameLeft,text="SaleID:",font=("arial",12,"bold"),padx=2,pady=6)
        lblSaleID.grid(row=0,column=0,sticky=W)
        txtSaleID=Entry(DataFrameLeft,font=("arial",13,"bold"),textvariable=self.SaleID,width=25)
        txtSaleID.grid(row=0,column=1)

        lblSalePrice=Label(DataFrameLeft,font=("arial",12,"bold"),text="Price Of Sale:",padx=2)
        lblSalePrice.grid(row=1,column=0,sticky=W)
        txtSalePrice=Entry(DataFrameLeft,font=("arial",13,"bold"),textvariable=self.SalePrice,width=25)
        txtSalePrice.grid(row=1,column=1)

        lblCName=Label(DataFrameLeft,font=("arial",12,"bold"),text="Customer Name:",padx=2,pady=4)
        lblCName.grid(row=2,column=0,sticky=W)
        txtCName=Entry(DataFrameLeft,font=("arial",13,"bold"),textvariable=self.CName,width=25)
        txtCName.grid(row=2,column=1)

        lblLPN=Label(DataFrameLeft,font=("arial",12,"bold"),text="License Plate Number:",padx=2,pady=6)
        lblLPN.grid(row=3,column=0,sticky=W)
        txtLPN=Entry(DataFrameLeft,font=("arial",13,"bold"),textvariable=self.LPN,width=25)
        txtLPN.grid(row=3,column=1)

        lblDOS=Label(DataFrameLeft,font=("arial",12,"bold"),text="Date Of Sale:",padx=2,pady=6)
        lblDOS.grid(row=4,column=0,sticky=W)
        txtDOS=Entry(DataFrameLeft,font=("arial",13,"bold"),textvariable=self.DOS,width=25)
        txtDOS.grid(row=4,column=1)


        #=============================== DataFrameRight ======================================
        self.txtSaleOrPurchaseInformation=Text(DataFrameRight,font=("arial",12,"bold"),width=45,height=14,padx=2,pady=6)
        self.txtSaleOrPurchaseInformation.grid(row=0,column=0)


        #================================ Buttons ============================================
        btnSale=Button(Buttonframe,command=self.Sale,text="Sale",bg="yellow",fg="green",font=("arial",12,"bold"),width=30,height=2,padx=2,pady=6)
        btnSale.grid(row=0,column=0)


        btnSaleInfo=Button(Buttonframe,command=self.iSaleInfo,text="Sale Info",bg="yellow",fg="green",font=("arial",12,"bold"),width=30,height=2,padx=2,pady=6)
        btnSaleInfo.grid(row=0, column=1)

        btnUpdate=Button(Buttonframe,command=self.update_data,text="Update",bg="yellow",fg="green",font=("arial",12,"bold"),width=30,height=2,padx=2,pady=6)
        btnUpdate.grid(row=0, column=2)


        btnDelete=Button(Buttonframe,command=self.idelete,text="Delete",bg="yellow",fg="green",font=("arial",12,"bold"),width=30,height=2,padx=2,pady=6)
        btnDelete.grid(row=0, column=3)

        btnClear=Button(Buttonframe,command=self.clear,text="Clear",bg="yellow",fg="green",font=("arial",12,"bold"),width=30,height=2,padx=2,pady=6)
        btnClear.grid(row=0, column=4)

        btnExit=Button(Buttonframe,command=self.iExit,text="Exit",bg="yellow",fg="green",font=("arial",12,"bold"),width=30,height=2,padx=2,pady=6)
        btnExit.grid(row=0, column=5)


        #================================= Table ================================================
        #================================= Scroll Bar ===========================================
        scroll_x=ttk.Scrollbar(Detailsframe,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(Detailsframe,orient=VERTICAL)
        self.sale_table=ttk.Treeview(Detailsframe,column=("SaleID","SalePrice","CustomerName","LicensePlateNumber","DateOfSale"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x=ttk.Scrollbar(command=self.sale_table.xview)
        scroll_y=ttk.Scrollbar(command=self.sale_table.yview)

        self.sale_table.heading("SaleID",text="Sale ID")
        self.sale_table.heading("SalePrice",text="Sale Price")
        self.sale_table.heading("CustomerName",text="Customer Name")
        self.sale_table.heading("LicensePlateNumber",text="License Plate Number")
        self.sale_table.heading("DateOfSale",text="Date Of Sale")

        self.sale_table["show"]="headings"
        self.sale_table.pack(fill=BOTH,expand=1)
        self.sale_table.bind("<ButtonRelease-1>",self.get_cursor)

        self.fetch_data()

        #================================= Functionality Declaration ==========================================
    def Sale(self):
        print("sale button works")
        if self.SaleID.get()=="" or self.SalePrice.get()=="":
            messagebox.showerror("Error","All fields are required")
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password="Therock1998",database="CarInventorySystem")
            my_cursor=conn.cursor()
            my_cursor.execute("insert into Sale values(%s,%s,%s,%s,%s)", (
                                                                            self.SaleID.get(),
                                                                            self.SalePrice.get(),
                                                                            self.CName.get(),
                                                                            self.LPN.get(),
                                                                            self.DOS.get()
                ))
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Success","Record has been inserted")
    def update_data(self):
        print("Update button clicked")
        conn=mysql.connector.connect(host="localhost",username="root",password="Therock1998",database="CarInventorySystem")
        my_cursor = conn.cursor()
        my_cursor.execute(
            "UPDATE Sale SET SalePrice=%s, CustomerName=%s, LicensePlateNumber=%s, DateOfSale=%s WHERE SaleID=%s", (
                self.SalePrice.get(),
                self.CName.get(),
                self.LPN.get(),
                self.DOS.get(),
                self.SaleID.get(),
            ))



        conn.commit()
        self.fetch_data()
        conn.close()
        messagebox.showinfo("Success","Record has been updated")


    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="Therock1998",database="CarInventorySystem")
        my_cursor = conn.cursor()
        my_cursor.execute("select * from Sale")
        rows=my_cursor.fetchall()
        self.sale_table.delete(*self.sale_table.get_children())

        if len(rows)!=0:
            for i in rows:
                self.sale_table.insert("",END,values=i)
            conn.commit()
        conn.close()
    def get_cursor(self,event):
        cursor_row=self.sale_table.focus()
        content=self.sale_table.item(cursor_row)
        row=content["values"]
        self.SaleID.set(row[0])
        self.SalePrice.set(row[1])
        self.CName.set(row[2])
        self.LPN.set(row[3])
        self.DOS.set(row[4])

    def iSaleInfo(self):
        self.txtSaleOrPurchaseInformation.insert(END,"Sale ID:\t\t\t"+self.SaleID.get()+"\n")
        self.txtSaleOrPurchaseInformation.insert(END, "Sale Price:\t\t\t" + self.SalePrice.get() + "\n")
        self.txtSaleOrPurchaseInformation.insert(END, "Customer Name:\t\t\t" + self.CName.get() + "\n")
        self.txtSaleOrPurchaseInformation.insert(END, "License Plate Number:\t\t\t" + self.LPN.get() + "\n")
        self.txtSaleOrPurchaseInformation.insert(END, "Date Of Sale:\t\t\t" + self.DOS.get() + "\n")


    def idelete(self):
        conn=mysql.connector.connect(host="localhost",username="root",password="Therock1998",database="CarInventorySystem")
        my_cursor=conn.cursor()
        query="delete from Sale where SaleID=%s"
        value=(self.SaleID.get(),)
        my_cursor.execute(query,value)

        conn.commit()
        conn.close()

        self.fetch_data()
        messagebox.showinfo("Delete","Patient has been deleted successfully")


    def clear(self):
        self.SaleID.set("")
        self.SalePrice.set("")
        self.CName.set("")
        self.LPN.set("")
        self.DOS.set("")
        self.txtSaleOrPurchaseInformation.delete("1.0",END)

    def iExit(self):
        iExit=messagebox.askyesno("Car Inventory System","Confirm you want to exit")
        if iExit>0:
            root.destroy()
            return




if __name__ =="__main__":
    root=Tk()
    ob=Car(root)
    root.mainloop()
