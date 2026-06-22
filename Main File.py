from tkinter import Tk,Label,Frame,Entry,Button,messagebox,simpledialog,filedialog
from tkinter.ttk import Combobox
import random
import mygenerator
import dbhandler
import mailhandler
import time
import sqlite3
from PIL import Image,ImageTk
import shutil
import os
import re



def update_time():
    t=time.strftime("%A,%d-%m-%Y ⏰%r")
    lbl_dt.configure(text=t)
    lbl_dt.after(1000,update_time)


def customer_screen():    
    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.74)
    

    def logout_click():
        frm.destroy()
        main_screen()


    def viewdetails_screen():
        ifrm=Frame(root,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.32,relwidth=.70,relheight=.54)

        lbl_ftitle=Label(ifrm,text="This is view details screen",
                   font=('arial',15,'bold'),bg="white",fg='purple')
        lbl_ftitle.pack() 

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query="select * from users where acn=?"
        curobj.execute(query,(user_acn,))
        row=curobj.fetchone()
        conobj.close()
        details=f"""  
        Name={row[1]}
        
        ACN   ={row[0]}

        Bal   ={row[7]}

        open date={row[9]}
        """
        lbl_details=Label(ifrm,text=details,
                          font=('arial',15,'bold'),bg='white',fg='black')
        lbl_details.place(x=150,y=50)
       


    def updatedetails_screen():
        ifrm=Frame(root,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.32,relwidth=.70,relheight=.54)


        def up_details():
            name=e_name.get()
            pwd=e_pass.get()
            email=e_email.get()
            mob=e_mob.get()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='update users set name=?,pass=?,email=?,mob=? where acn=?'
            curobj.execute(query,(name,pwd,email,mob,user_acn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo('Update','Details Updated')
            customer_screen()




        lbl_ftitle=Label(ifrm,text="This is updatedetails screen",
                   font=('arial',15,'bold'),bg="white",fg='purple')
        lbl_ftitle.pack() 

        lbl_name=Label(ifrm,text="Name",
                   font=('arial',15,'bold'),bg="white")
        lbl_name.place(relx=.19,rely=.2)

        e_name=Entry(ifrm,font=('arial',15,'bold'),bd=4)
        e_name.place(relx=.19,rely=.28)
        

        lbl_email=Label(ifrm,text="Email",
                   font=('arial',15,'bold'),bg="white")
        lbl_email.place(relx=.19,rely=.38)

        e_email=Entry(ifrm,font=('arial',15,'bold',),bd=4)
        e_email.place(relx=.19,rely=.46)


        lbl_mob=Label(ifrm,text="Mob",
                   font=('arial',15,'bold'),bg="white")
        lbl_mob.place(relx=.6,rely=.38)

        e_mob=Entry(ifrm,font=('arial',15,'bold',),bd=4)
        e_mob.place(relx=.6,rely=.46)


        lbl_pass=Label(ifrm,text="Pass",
                   font=('arial',15,'bold'),bg="white")
        lbl_pass.place(relx=.6,rely=.2)

        e_pass=Entry(ifrm,font=('arial',15,'bold',),bd=4)
        e_pass.place(relx=.6,rely=.28)

        up_btn=Button(ifrm,command=up_details,text="Update Details",bd=5,
                    font=('arial',15,'bold'),bg='pink',fg='Blue',width=14)
        up_btn.place(relx=.40,rely=.7)

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select name,pass,email,mob from users where acn=?'
        curobj.execute(query,(user_acn,))
        tup=curobj.fetchone()
        conobj.close()

        e_name.insert(0,tup[0])
        e_pass.insert(0,tup[1])
        e_email.insert(0,tup[2])
        e_mob.insert(0,tup[3])



    def deposit_screen():
        ifrm=Frame(root,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.32,relwidth=.70,relheight=.54)

        lbl_ftitle=Label(ifrm,text="This is deposit screen",
                   font=('arial',15,'bold'),bg="white",fg='purple')
        lbl_ftitle.pack() 

        amt=simpledialog.askfloat('Deposit Amount',"Enter Account")
        if amt==None:
            return
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='update users set bal=bal+? where acn=?'
        curobj.execute(query,(amt,user_acn))
        conobj.commit()
        conobj.close()
        messagebox.showinfo('Deposit','Amount Deposited')


    def withdraw_screen():
        ifrm=Frame(root,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.32,relwidth=.70,relheight=.54)

        lbl_ftitle=Label(ifrm,text="This is withdraw screen",
                   font=('arial',15,'bold'),bg="white",fg='purple')
        lbl_ftitle.pack() 

        amt=simpledialog.askfloat('Deposit Amount',"Enter Account")
        if amt==None:
            return
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select bal from users where acn=?'
        curobj.execute(query,(user_acn,))
        bal=curobj.fetchone()[0]
        conobj.close()

        if amt>bal:
            messagebox.showerror('withraw','insufficient Bal')
            return
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='update users set bal=bal-? where acn=?'
        curobj.execute(query,(amt,user_acn))
        conobj.commit()
        conobj.close()
        messagebox.showinfo('Withdraw','Amount Withdrawn')


    def transfer_screen():
        ifrm=Frame(root,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.32,relwidth=.70,relheight=.54)

        lbl_ftitle=Label(ifrm,text="This is transfer screen",
                   font=('arial',15,'bold'),bg="white",fg='purple')
        lbl_ftitle.pack()
         
        to_acn=simpledialog.askfloat('Transfer Amount',"Enter TO ACN")
        if to_acn==None:
            return

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from users where acn=?'
        curobj.execute(query,(to_acn,))
        row=curobj.fetchone()
        conobj.close()
        if row==None:
            messagebox.showerror('Transfer Amount',"To ACN does not exist")
            return

        
        amt=simpledialog.askfloat('Deposit Amount',"Enter Amount")
        if amt==None:
            return
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select bal from users where acn=?'
        curobj.execute(query,(user_acn,))
        bal=curobj.fetchone()[0]
        conobj.close()

        if amt>bal:
            messagebox.showerror('Transfer Amount','Insufficient Bal')
            return
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query1='update users set bal=bal-? where acn=?'
        query2='update users set bal=bal+? where acn=?' 
        curobj.execute(query1,(amt,user_acn))
        curobj.execute(query2,(amt,to_acn))
        conobj.commit()
        conobj.close()
        messagebox.showinfo('Transfer Amount',f'{amt} Amount Transfered to ACN {to_acn} from ACN {user_acn}')



    def dp():
        filepath=filedialog.askopenfilename(filetypes=[('Image Files','*.jpg *.png *.jpeg')])
        shutil.copy(filepath,f'{user_acn}.jpg')
        img=Image.open(f'{user_acn}.jpg').resize((150,120))
        imgtk=ImageTk.PhotoImage(img,master=root)

        dp_lbl=Label(frm,image=imgtk)
        dp_lbl.image=imgtk
        dp_lbl.place(relx=0,rely=.05)


    logout_btn=Button(frm,text="Logout",bd=5,
                    font=('arial',14,'bold'),bg='pink',command=logout_click)
    logout_btn.place(relx=.93,rely=0)
    conobj=sqlite3.connect(database='bank.sqlite')
    curobj=conobj.cursor()
    query='select name from users where acn=?'
    curobj.execute(query,user_acn,)
    name=curobj.fetchone()[0]
    conobj.close()

    

    lbl_wel=Label(frm,text=f"Welcome,{name}",
                   font=('arial',15,'bold'),bg="powder blue")
    lbl_wel.place(relx=0,rely=0)

    if os.path.exists(f'{user_acn}.jpg'):
        filepath=f'{user_acn}.jpg'
    else:
        filepath='default.jpg'   
    imgc=Image.open(filepath).resize((150,120))
    imgctk=ImageTk.PhotoImage(imgc,master=root)
    dp_lbl=Label(frm,image=imgctk)
    dp_lbl.image=imgctk
    dp_lbl.place(relx=0,rely=.05)


    updatedp_btn=Button(frm,command=dp,text="Update DP",bd=5,
                    font=('arial',10,'bold'),bg='white',fg='purple',width=10)
    updatedp_btn.place(relx=.02,rely=.30)





    view_btn=Button(frm,text="View Details",bd=5,
                    font=('arial',14,'bold'),bg='blue',fg='white',width=15,command=viewdetails_screen)
    view_btn.place(relx=0,rely=.38)


    update_btn=Button(frm,text="Update Details",bd=5,
                    font=('arial',14,'bold'),bg='green',fg='white',width=15,command=updatedetails_screen)
    update_btn.place(relx=0,rely=.48)


    deposit_btn=Button(frm,text="Deposit Simulation",bd=5,
                    font=('arial',14,'bold'),bg='red',fg='white',width=15,command=deposit_screen)
    deposit_btn.place(relx=0,rely=.58)
    

    withdraw_btn=Button(frm,text="Withdraw",bd=5,
                    font=('arial',14,'bold'),bg='purple',fg='white',width=15,command=withdraw_screen)
    withdraw_btn.place(relx=0,rely=.68)


    Transfer_btn=Button(frm,text="Transfer",bd=5,
                    font=('arial',14,'bold'),bg='orange',fg='white',width=15,command=transfer_screen)
    Transfer_btn.place(relx=0,rely=.78)






    
def admin_screen():
    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.74)
    

    def logout_click():
        frm.destroy()
        main_screen()




    def openacn_screen():
        ifrm=Frame(root,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.09,rely=.32,relwidth=.84,relheight=.54)


        def reset():
                e_name.delete(0,'end')
                e_mob.delete(0,'end')
                e_email.delete(0,'end')
                e_adhar.delete(0,'end')
                e_age.delete(0,'end')

        def create_acn():
            name=e_name.get() 
            email=e_email.get()
            adhar=e_adhar.get()
            mob=e_mob.get()
            age=e_age.get()
            gender=cb_gender.get()
               
            
            if len(name)==0:
                messagebox.showerror('Open Account','Name is required')
                return 
            if len(email)==0:
                messagebox.showerror('Open Account','email is required')
                return 
            match=re.fullmatch(r'[a-zA-Z0-9_.$]+@[a-zA-Z0-9]+\.[a-zA-Z]+',email)
            if match==None:
                messagebox.showerror('Open Account','Invalid Email')
                return
            if len(adhar)==0:
                messagebox.showerror('Open Account','Adhar is required')
                return
            if adhar.isdigit() is not True:
                messagebox.showerror('Open Account','Adhar  should be in digit')
                return
            if len(adhar)!=12:
                messagebox.showinfo('OPen Account','adhar no. should be exactly 12 digit')
                return
            

            if len(mob)==0:
                messagebox.showerror('Open Account','mob no is required')
                return
            if mob.isdigit() is not True:
                messagebox.showerror('Open Account','mob no should be in digit')
                return
            if len(mob)<10:
                messagebox.showerror('OPen Account','Mob no should not less than 10 digit')
                return
            if len(age)==0:
                messagebox.showerror('Open Account','Age is required')
                return  
            if age.isdigit() is not True:
                messagebox.showerror('Open Account','age should be in digit')
                return     
            
            bal=0
            opendate=time.strftime("%A,%b %d %Y %r")
            pwd=mygenerator.generate_password()


            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='insert into users values(null,?,?,?,?,?,?,?,?,?)'
            curobj.execute(query,(name,pwd,email,mob,adhar,age,bal,gender,opendate))
            conobj.commit()
            conobj.close()

            
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query="select max(acn) from users"
            curobj.execute(query)
            acn=curobj.fetchone()[0]
            conobj.close()

            mailhandler.send_openacn_email(email,name,acn,pwd)
            messagebox.showinfo("Create Account","Credentials are sent to email")
        
        
        
        lbl_ftitle=Label(ifrm,text="This is open account screen",
                   font=('arial',15,'bold'),bg="white",fg='purple')
        lbl_ftitle.pack() 

        lbl_name=Label(ifrm,text="Name",
                   font=('arial',15,'bold'),bg="white")
        lbl_name.place(relx=.19,rely=.2)

        e_name=Entry(ifrm,font=('arial',15,'bold'),bd=4)
        e_name.place(relx=.19,rely=.28)
        

        lbl_email=Label(ifrm,text="Email",
                   font=('arial',15,'bold'),bg="white")
        lbl_email.place(relx=.19,rely=.38)

        e_email=Entry(ifrm,font=('arial',15,'bold',),bd=4)
        e_email.place(relx=.19,rely=.46)


        lbl_mob=Label(ifrm,text="Mob",
                   font=('arial',15,'bold'),bg="white")
        lbl_mob.place(relx=.19,rely=.56)

        e_mob=Entry(ifrm,font=('arial',15,'bold',),bd=4)
        e_mob.place(relx=.19,rely=.64)


        lbl_adhar=Label(ifrm,text="Adhar",
                   font=('arial',15,'bold'),bg="white")
        lbl_adhar.place(relx=.6,rely=.2)

        e_adhar=Entry(ifrm,font=('arial',15,'bold',),bd=4)
        e_adhar.place(relx=.6,rely=.28)


        lbl_age=Label(ifrm,text="Age",
                   font=('arial',15,'bold'),bg="white")
        lbl_age.place(relx=.6,rely=.38)

        e_age=Entry(ifrm,font=('arial',15,'bold',),bd=4)
        e_age.place(relx=.6,rely=.46)


        lbl_gender=Label(ifrm,text="Gender",
                   font=('arial',15,'bold'),bg="white")
        lbl_gender.place(relx=.6,rely=.56)

        cb_gender=Combobox(ifrm,font=('arial',15,'bold',),values=['Male','Female'])
        cb_gender.current(0)
        cb_gender.config(state='readonly')
        cb_gender.place(relx=.6,rely=.64)


        submit_btn=Button(ifrm,text='Submit',bd=5,
                     font=('arial',15,'bold'),bg='pink',command=create_acn)
        submit_btn.place(relx=.4,rely=.8)

        reset_btn=Button(ifrm,command=reset,text='Reset',bd=5,font=('arial',15,'bold'),bg="pink")
        reset_btn.place(relx=.5,rely=.8,relwidth=.09)


    def viewacn_screen():
        ifrm=Frame(root,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.09,rely=.32,relwidth=.84,relheight=.54)

        def reset():
            e_Acn.delete(0,'end')


        def search():
            acn=int(e_Acn.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query="select name,bal,opendate,email,adhar from users where acn=?"

            curobj.execute(query,(acn,))
            row=curobj.fetchone()
            conobj.close()
            if row==None:
                messagebox.showerror("Search","Account does not exist")
            else:
                #messagebox.showinfo('search',row)
                details=f'Name={row[0]}\nBal={row[1]}\nOpendate={row[2]}\nEmail={row[3]}\nAdhar={row[4]}\n'     
                messagebox.showinfo('search',details)




        lbl_ftitle=Label(ifrm,text="This is view account screen",
                   font=('arial',15,'bold'),bg="white",fg='purple')
        lbl_ftitle.pack() 


        lbl_Acn=Label(ifrm,text="ACN",
                   font=('arial',15,'bold'),bg="white")
        lbl_Acn.place(relx=.25,rely=.2)

        e_Acn=Entry(ifrm,font=('arial',15,'bold',),bd=4)
        e_Acn.place(relx=.38,rely=.2)


        search_btn=Button(ifrm,command=search,text='Search',bd=5,
                     font=('arial',14  ),bg='pink')
        search_btn.place(relx=.7,rely=.18)

        reset_btn=Button(ifrm,command=reset,text='Reset',bd=5,font=('arial',15),bg="pink")
        reset_btn.place(relx=.8,rely=.178)

           

    def closeacn_screen():
        ifrm=Frame(root,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.09,rely=.32,relwidth=.84,relheight=.54)

        def reset():
            e_Acn.delete(0,'end')

        def close():
            acn=int(e_Acn.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query="select name,email from users where acn=?"
            curobj.execute(query,(acn,))
            row=curobj.fetchone()
            conobj.close()

            
            
            if row==None:
                messagebox.showerror('close account does not exist')
            else:
                gen_otp=random.randint(1000,9999)
                mailhandler.send_closeacn_email(row[1],row[0],gen_otp)
                user_otp=simpledialog.askinteger('Close Account',"Enter OTP")
                if user_otp==gen_otp:
                    conobj=sqlite3.connect(database='bank.sqlite') 
                    curobj=conobj.cursor()
                    query="delete from users where acn=?"
                    curobj.execute(query,(acn,))
                    conobj.commit()
                    conobj.close()
                    messagebox.showinfo('Account Closed')
                else:
                    messagebox.showerror('Close Account','Invalid OTP')

            
            
            

        lbl_ftitle=Label(ifrm,text="This is close account screen",
                   font=('arial',15,'bold'),bg="white",fg='purple')
        lbl_ftitle.pack()  


        lbl_Acn=Label(ifrm,text="ACN",
                   font=('arial',15,'bold'),bg="white")
        lbl_Acn.place(relx=.25,rely=.2)

        e_Acn=Entry(ifrm,font=('arial',15,'bold',),bd=4)
        e_Acn.place(relx=.38,rely=.2)


        close_btn=Button(ifrm,command=close,text='Close',bd=5,
                     font=('arial',14 ),bg='pink')
        close_btn.place(relx=.7,rely=.18)

        reset_btn=Button(ifrm,command=reset,text='Reset',bd=5,font=('arial',14),bg="pink")
        reset_btn.place(relx=.8,rely=.178)
    



    logout_btn=Button(frm,text="Logout",bd=5,
                    font=('arial',14,'bold'),bg='pink',command=logout_click)
    logout_btn.place(relx=.93,rely=0)
    

    lbl_wel=Label(frm,text="Welcome Admin",
                   font=('arial',15,'bold'),bg="powder blue")
    lbl_wel.place(relx=0,rely=0)


    openacn_btn=Button(frm,text="Open Account",bd=5,
                    font=('arial',14,'bold'),bg='blue',fg='white',command=openacn_screen)
    openacn_btn.place(relx=.15,rely=.06)



    viewacn_btn=Button(frm,text="View Account",bd=5,
                    font=('arial',14,'bold'),bg='green',fg='white',command=viewacn_screen)
    viewacn_btn.place(relx=.45,rely=.06)


    closeacn_btn=Button(frm,text="Close Account",bd=5,
                    font=('arial',14,'bold'),bg='red',fg='white',command=closeacn_screen)
    closeacn_btn.place(relx=.75,rely=.06)

    
    



def fp_screen():
    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.74)


    def back_click():
        frm.destroy()
        main_screen()

    def reset():
        e_acn.delete(0,'end')
        e_email.delete(0,'end')
            

    def fp_otp():
        user_acn=e_acn.get()
        user_email=e_email.get()

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query="select name,pass from users where acn=? and email=?"
        curobj.execute(query,(user_acn,user_email))
        tup=curobj.fetchone()
        conobj.close()
        
        
        if tup==None:
            messagebox.showerror("Forgot Password",'ACN does not exist')
            return
        gen_otp=random.randint(1000,9999)
        mailhandler.send_fpotp_email(user_email,tup[0],gen_otp)
        user_otp=simpledialog.askinteger('Forgot Password','OTP')
        if user_otp==None:
            return
        if gen_otp==user_otp:
            messagebox.showinfo('Forgote Password',f"Your pass={tup[1]}")
    
    back_btn=Button(frm,text="Back",bd=5,
                    font=('arial',15,'bold'),bg='pink',command=main_screen)
    back_btn.place(relx=0,rely=0)

    lbl_acn=Label(frm,text="User ACN",
                   font=('arial',12,'bold'),bg="powder blue")
    lbl_acn.place(relx=.35,rely=.2)

    e_acn=Entry(frm,font=('arial',12,'bold',),bd=4)
    e_acn.place(relx=.5,rely=.2)

    lbl_email=Label(frm,text="User Email",
                   font=('arial',12,'bold'),bg="powder blue")
    lbl_email.place(relx=.35,rely=.3)

    e_email=Entry(frm,font=('arial',12,'bold',),bd=4)
    e_email.place(relx=.5,rely=.3)


    otp_btn=Button(frm,command=fp_otp,text="Validate & Send OTP",bd=5,
                    font=('arial',14,'bold'),bg='pink')
    otp_btn.place(relx=.40,rely=.5)

    reset_btn=Button(frm,command=reset,text='Reset',bd=5,font=('arial',15,'bold'),bg="pink")
    reset_btn.place(relx=.60,rely=.5)




def main_screen():
    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.74)


    def fp_click():
        frm.destroy()
        fp_screen()


    def reset():
        e_acn.delete(0,'end')
        e_pass.delete(0,'end')
        e_captcha.delete(0,'end')
        cb_user.current(2)

    
    def login_click():
        global user_acn
        user_type=cb_user.get()
        user_acn=e_acn.get()
        user_pass=e_pass.get()
        user_captcha=e_captcha.get()
        if user_type=='Admin'and user_acn=='0' and user_pass=='Admin' and user_captcha==captcha.replace(' ',''):
            frm.destroy()
            admin_screen()
        elif user_type=='Customer' and user_captcha==captcha.replace(' ',''):
            
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query="select * from users where acn=? and pass=?"
            curobj.execute(query,(user_acn,user_pass))
            row=curobj.fetchone()
            conobj.close()

            if row==None:
                messagebox.showerror('Login','Invalid ACN/Pass')
                
            else:
                frm.destroy()
                customer_screen()
        else:
            messagebox.showerror('User Type',"Invalid credentials")                


    lbl_user=Label(frm,text="User Type",
                   font=('arial',12,'bold'),bg="powder blue")
    lbl_user.place(relx=.35,rely=.1)

    cb_user=Combobox(frm,values=["Customer","Admin","         ----Select----"],
                     font=('arial',12,'bold'))
    cb_user.current(2)
    cb_user.config(state='readonly')
    cb_user.place(relx=.5,rely=.1)


    lbl_acn=Label(frm,text="User ACN",
                   font=('arial',12,'bold'),bg="powder blue")
    lbl_acn.place(relx=.35,rely=.2)

    e_acn=Entry(frm,font=('arial',12,'bold',),bd=4)
    e_acn.place(relx=.5,rely=.2)


    lbl_pass=Label(frm,text="User Pass",
                   font=('arial',12,'bold'),bg="powder blue")
    lbl_pass.place(relx=.35,rely=.3)

    e_pass=Entry(frm,font=('arial',12,'bold',),bd=4,show='*')
    e_pass.place(relx=.5,rely=.3)

    captcha=mygenerator.generate_captcha()
    lbl_show_cap=Label(frm,text=captcha,
                       font=('comic sans',15,'bold'),bg='white',fg='purple',width=8)
    lbl_show_cap.place(relx=.52,rely=.4)

    def refresh_captcha():
        nonlocal captcha
        captcha=mygenerator.generate_captcha()
        lbl_show_cap.configure(text=captcha)
    
    ref_btn=Button(frm,text='🔄️refresh',bd=5,font=('arial',10),command=refresh_captcha)
    ref_btn.place(relx=.62,rely=.4)

    lbl_captcha=Label(frm,text="User Captcha",
                   font=('arial',12,'bold'),bg="powder blue")
    lbl_captcha.place(relx=.35,rely=.5)

    e_captcha=Entry(frm,font=('arial',12,'bold',),bd=4)
    e_captcha.place(relx=.5,rely=.5)

    login_btn=Button(frm,text='Login',bd=5,
                     font=('arial',15,'bold'),bg='pink',command=login_click)
    login_btn.place(relx=.5,rely=.6)

    reset_btn=Button(frm,command=reset,text='Reset',bd=5,font=('arial',15,'bold'),bg="pink")
    reset_btn.place(relx=.58,rely=.6)

    fp_btn=Button(frm,text='Forget Password',bd=4,font=('arial',15,'bold'),
                  bg="pink",width=18,command=fp_click)
    fp_btn.place(relx=.48,rely=.72)



root=Tk()
root.state('zoomed')
root.configure(bg='pink')
root.resizable(width=False,height=False)


lbl_title=Label(root,text='Banking Stimulation',
                font=('arial',30,'bold','underline'),
                bg='pink',fg="black")

lbl_title.pack()



lbl_dt=Label(root,text=time.strftime("%A,%d-%m-%Y ⏰%r"),
              font=('arial',10,'bold'),bg='pink',fg='blue')

lbl_dt.pack(pady=20)
update_time()

img=Image.open('logo.jpg').resize((250,150))
imgtk=ImageTk.PhotoImage(img,master=root)


lbl_logo=Label(root,image=imgtk)
lbl_logo.place(relx=0,rely=0)

img1=Image.open('bank.jpg').resize((250,150))
imgtk1=ImageTk.PhotoImage(img1,master=root)


lbl_logo1=Label(root,image=imgtk1)
lbl_logo1.place(relx=.8,rely=0)

lbl_footer=Label(root,text='Developed by:Abhiyogyta@..',
                font=('arial',15,'bold'),
                bg='pink',fg="blue")
lbl_footer.pack(side='bottom',pady=10)

main_screen()




root.mainloop()