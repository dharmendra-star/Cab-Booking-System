"""***************************************
MODULES USED IN THE PROJECT
***************************************"""
from tkinter import INSERT
import mysql.connector as co

from tabulate import tabulate
import pickle
import os
from datetime import date
import datetime
"""***************************************
FUNCTION TO GENERATE CAB ID
***************************************"""

# def gen_cid():
#     if not os.path.exists("cab.txt"):
#         with open("cab.txt", "w") as f:
#             f.write("1000")

#     with open("cab.txt", "r+") as f:
#         n = int(f.read())
#         n += 1
#         f.seek(0)
#         f.write(str(n))
#     return n




def gen_cid():
    try:
        inFile=open("cab.txt","r+")
        n=inFile.read()
        n=int(n)
        n+=1
        inFile.close()
        infile=open("cab.txt",'w')
        infile.write(str(n))
        infile.close()
        #this will generate cab id for each CAB
        return(n)
    except IOError:
        print("I/O error occured")
        
"""*********************************
Function to Add CAB
*********************************"""


import mysql.connector as co

def add_cab():
    try:
        con = co.connect(
            host="Developer",
            user="root",
            password="Dhar@#3839",
            database="cab_booking_db"
        )
        cur = con.cursor()

        regno = input("Enter registration number: ")
        cab_type = input("Enter cab type: ")
        cab_desc = input("Enter cab description: ")
        seats = int(input("Enter seats: "))
        owner = input("Enter owner name: ")
        driver = input("Enter driver name: ")
        address = input("Enter owner address: ")
        mobile = int(input("Enter mobile no: "))
        
        


        query = """
        INSERT INTO CAB_MASTER
        (reg_no, cab_type, cab_desc, seats,
        owner_name, driver_name, owner_address, mobile)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """
        
        data = (regno, cab_type, cab_desc, seats,
                owner, driver, address, mobile)

        cur.execute(query, data)
        con.commit()

        print("✅ Cab added successfully")
        print("🆔 Generated Cab ID:", cur.lastrowid)

        cur.close()
        con.close()

    except Exception as e:
        print("❌ Error in add_cab")
        print(e)


# def add_cab():
#     try:
#         mycon=co.connect(host="Developer",user="root",password="Dhar@#3839",database="cab_booking_db")
#         cursor=mycon.cursor()
#         cid=gen_cid()
#         regno=input("\n\nEnter registration number: ")
#         cab_type=input("\nEnter type of the CAB: ")
#         cab_desc=input('Enter cab description : ')
#         nos=int(input('Enter no. of seats : '))
#         owner=input("Enter Owner's Name: ")
#         driver=input("Enter driver's Name: ")
#         ownadd=input('Enter owner address: ')
#         mob=int(input('Enter Mobile no. : '))
        
#         query="insert into CAB_MASTER values ("+str(cid)+",'"+regno+"','"+cab_type+"','"+cab_desc+"',"+str(nos)+",'"+owner+"','"+driver+"','"+ownadd+"',"+str(mob)+")"
        
#         print(query)
#         cursor.execute("insert into CAB_MASTER values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(cid,regno,cab_type,cab_desc,nos,owner,driver,ownadd,mob))
#         mycon.commit()
#         mycon.close()
#         cursor.close()
#         print ("\n Cab added Successfully")
#         print ("\n\n YOUR CAB ID IS: ",cid)
#         print('Record has been saved in CAB_MASTER table')
#     except:
#         print('error in add_cab')
        
"""*************************************************
FUNCTION TO DISPLAY ALL CABS
*************************************************"""

def show_all_cab():
    try:
        mycon=co.connect(host="Developer",user="root",password="Dhar@#3839",database="cab_booking_db")
        cursor=mycon.cursor()
        strQry="select * from cab_master"
        cursor.execute(strQry)
        data = cursor.fetchall()
        if data == []:
            print("No records found")
        else:
            print("")
            h=["CAB ID","REG NO.","CAB TYPE","CAB DESC","NO OF SEATS","OWNER NAME","DRIVER NAME","OWNER ADDRESS","MOB NO"]
            #print(tabulate(data,headers=h,tablefmt='fancy_grid'))
            #print(tabulate(data,headers=h,tablefmt='textile'))
            print(tabulate(data,headers=h))
        mycon.close()
        cursor.close()
    except:
        print('error')
        

"""************************************************
FUNCTION TO SEARCH CAB
************************************************"""
 
def search_cab():
    flag=0
    try:
        ano=int(input("Enter cab ID : "))
        mycon=co.connect(host="Developer",user="root",password="Dhar@#3839",database="cab_booking_db")
        cursor=mycon.cursor()
        strQry="select * from CAB_MASTER where cid="+str(ano)+""
        cursor.execute(strQry)
        data = cursor.fetchone()
        if data == None:
        
            print("cab ID does not exist")
        else:
            print("cab ID :",data[0])
            print("registration no. :",data[1])
            print("Cab type :",data[2])
            print("Cab Description :",data[3])
            print("no. of seats :",data[4])
            print("owner name :",data[5])
            print("driver name:",data[6])
            print("owner address:",data[7])
            print("mobile no. :",data[8])
        mycon.close()
        cursor.close()
    except Exception as e:
        print("Error:", e)

 
 
"""*****************************************
FUNCTION TO MODIFY RECORD
*****************************************"""
 
def modify_cab():
    print("1:Edit Registration number ")
    print("2:Edit Cab Type")
    print("3:Edit Cab Description")
    print("4:Edit Number Of Seat")
    print("5:Edit Owner's Name")
    print("6:Edit Driver's Name")
    print("7:Edit Owner's Address")
    print("8:Edit Mobile Number")
    print("9:Return")
    print("\t\t-------------------------------------------------")
    choice=int(input("enter your choice"))
    if choice==1:
        edit_regno()
    elif choice==2:
        edit_Ctype()
    elif choice==3:
        edit_Cdesc()
    elif choice==4:
        edit_nos()
    elif choice==5:
        edit_owner()
    elif choice==6:
        edit_driver()
    elif choice==7:
        edit_ownadd()
    elif choice==8:
        edit_mob()
    elif choice==9:
        return
    else:
        print("Error:invalid choice try again.....")
        conti="press any key to return to main menu"

def edit_regno():
    try:
        mycon=co.connect(host="Developer",user="root",password="Dhar@#3839",database="cab_booking_db")
        cursor=mycon.cursor()
        cabid=int(input('Enter cab id'))
        q="select * from cab_master where cid="+str(cabid)+""
        cursor.execute(q)
        data = cursor.fetchall()
        if data==[]:
            print("No record found")
        else:
            h=["CAB ID","REGISTRATION NO.","CAB TYPE","CAB DESCRIPTION","NUMBER OF SEATS","OWNER'S NAME","DRIVER'S NAME","OWNER'S ADDRESS","MOBILE NUMBER"]
            print(tabulate(data,headers=h))
            nm=input("enter new registration no.")
            st="update cab_master set regno='%s' where cid='%s'"%(nm,cabid)
            cursor.execute(st)
            mycon.commit()
            mycon.close()
            cursor.close()
            print('data updated successfully')
    except Exception as e:
        print("Error:", e)


def edit_Ctype():
    try:
        mycon=co.connect(host="Developer",user="root",password="Dhar@#3839",database="cab_booking_db")
        cursor=mycon.cursor()
        cabid=int(input('Enter cab id: '))
        q="select * from cab_master where cid="+str(cabid)+""
        cursor.execute(q)
        data = cursor.fetchall()
        if data==[]:
            print("No record found")
        else:
            h=["CAB ID","REGISTRATION NO.","CAB TYPE","CAB DESCRIPTION","NUMBER OF SEATS","OWNER'S NAME","DRIVER'S NAME","OWNER'S ADDRESS","MOBILE NUMBER"]
            print(tabulate(data,headers=h))
            nm=input("enter new cab type: ")
            st="update cab_master set cab_type='%s' where cid='%s'"%(nm,cabid)
            cursor.execute(st)
            mycon.commit()
            mycon.close()
            cursor.close()
            print('data updated successfully')
    except Exception as e:
        print("Error:", e)


def edit_Cdesc():
    try:
        mycon=co.connect(host="Developer",user="root",password="Dhar@#3839",database="cab_booking_db")
        cursor=mycon.cursor()
        cabid=int(input('Enter cab id'))
        q="select * from cab_master where cid="+str(cabid)+""
        cursor.execute(q)
        data = cursor.fetchall()
        if data==[]:
            print("No record found")
        else:
            h=["CAB ID","REGISTRATION NO.","CAB TYPE","CAB DESCRIPTION","NUMBER OF SEATS","OWNER'S NAME","DRIVER'S NAME","OWNER'S ADDRESS","MOBILE NUMBER"]
            print(tabulate(data,headers=h))
            nm=input("enter new cab description: ")
            st="update cab_master set cab_desc='%s' where cid='%s'"%(nm,cabid)
            cursor.execute(st)
            mycon.commit()
            mycon.close()
            cursor.close()
            print('data updated successfully')
    except Exception as e:
        print("Error:", e)


def edit_nos():
    try:
        mycon=co.connect(host="Developer",user="root",password="Dhar@#3839",database="cab_booking_db")
        cursor=mycon.cursor()
        cabid=int(input('Enter cab id'))
        q="select * from cab_master where cid="+str(cabid)+""
        cursor.execute(q)
        data = cursor.fetchall()
        if data==[]:
            print("No record found")
        else:
            h=["CAB ID","REGISTRATION NO.","CAB TYPE","CAB DESCRIPTION","NUMBER OF SEATS","OWNER'S NAME","DRIVER'S NAME","OWNER'S ADDRESS","MOBILE NUMBER"]
            print(tabulate(data,headers=h))
            nm=int(input("enter new no. of seats: "))
            st="update cab_master set nos='%s' where cid='%s'"%(nm,cabid)
            cursor.execute(st)
            mycon.commit()
            mycon.close()
            cursor.close()
            print('data updated successfully')
    except Exception as e:
        print("Error:", e)


def edit_owner():
    try:
        mycon=co.connect(host="Developer",user="root",password="Dhar@#3839",database="cab_booking_db")
        cursor=mycon.cursor()
        cabid=int(input('Enter cab id'))
        q="select * from cab_master where cid="+str(cabid)+""
        cursor.execute(q)
        data = cursor.fetchall()
        if data==[]:
            print("No record found")
        else:
            h=["CAB ID","REGISTRATION NO.","CAB TYPE","CAB DESCRIPTION","NUMBER OF SEATS","OWNER'S NAME","DRIVER'S NAME","OWNER'S ADDRESS","MOBILE NUMBER"]
            print(tabulate(data,headers=h))
            nm=input("enter new owner's name: ")
            st="update cab_master set owner='%s' where cid='%s'"%(nm,cabid)
            cursor.execute(st)
            mycon.commit()
            mycon.close()
            cursor.close()
            print('data updated successfully')
    except Exception as e:
        print("Error:", e)


def edit_driver():
    try:
        mycon=co.connect(host="Developer",user="root",password="Dhar@#3839",database="cab_booking_db")
        cursor=mycon.cursor()
        cabid=int(input('Enter cab id'))
        q="select * from cab_master where cid="+str(cabid)+""
        cursor.execute(q)
        data = cursor.fetchall()
        if data==[]:
            print("No record found")
        else:
            h=["CAB ID","REGISTRATION NO.","CAB TYPE","CAB DESCRIPTION","NUMBER OF SEATS","OWNER'S NAME","DRIVER'S NAME","OWNER'S ADDRESS","MOBILE NUMBER"]
            print(tabulate(data,headers=h))
            nm=input("enter new driver's name")
            st="update cab_master set driver='%s' where cid='%s'"%(nm,cabid)
            cursor.execute(st)
            mycon.commit()
            mycon.close()
            cursor.close()
            print('data updated successfully')
    except Exception as e:
        print("Error:", e)


def edit_ownadd():
    try:
        mycon=co.connect(host="Developer",user="root",password="Dhar@#3839",database="cab_booking_db")
        cursor=mycon.cursor()
        cabid=int(input('Enter cab id'))
        q="select * from cab_master where cid="+str(cabid)+""
        cursor.execute(q)
        data = cursor.fetchall()
        if data==[]:
            print("No record found")
        else:
            h=["CAB ID","REGISTRATION NO.","CAB TYPE","CAB DESCRIPTION","NUMBER OF SEATS","OWNER'S NAME","DRIVER'S NAME","OWNER'S ADDRESS","MOBILE NUMBER"]
            print(tabulate(data,headers=h))
            nm=input("enter new owner's address")
            st="update cab_master set ownadd='%s' where cid='%s'"%(nm,cabid)
            cursor.execute(st)
            mycon.commit()
            mycon.close()
            cursor.close()
            print('data updated successfully')
    except Exception as e:
        print("Error:", e)


def edit_mob():
    try:
        mycon=co.connect(host="Developer",user="root",password="Dhar@#3839",database="cab_booking_db")
        cursor=mycon.cursor()
        cabid=int(input('Enter cab id'))
        q="select * from cab_master where cid="+str(cabid)+""
        cursor.execute(q)
        data = cursor.fetchall()
        if data==[]:
            print("No record found")
        else:
            h=["CAB ID","REGISTRATION NO.","CAB TYPE","CAB DESCRIPTION","NUMBER OF SEATS","OWNER'S NAME","DRIVER'S NAME","OWNER'S ADDRESS","MOBILE NUMBER"]
            print(tabulate(data,headers=h))
            nm=int(input("enter new mobile no. : "))
            st="update cab_master set mob='%s' where cid='%s'"%(nm,cabid)
            cursor.execute(st)
            mycon.commit()
            mycon.close()
            cursor.close()
            print('data updated successfully')
    except Exception as e:
        print("Error:", e)


"""***************************************
FUNCTION TO DELETE CAB
***************************************"""
 
def delete_cab(n):
    try:
        mycon=co.connect(host="Developer",user="root",password="Dhar@#3839",database="cab_booking_db")
        cursor=mycon.cursor()
        q="select * from CAB_MASTER where cid="+str(n)+""
        cursor.execute(q)
        data = cursor.fetchall()
        if data==[]:
            
            print("No record found")
        else:
            h=["CAB ID","REGISTRATION NO.","CAB TYPE","CAB DESCRIPTION","NUMBER OF SEATS","OWNER'S NAME","DRIVER'S NAME","OWNER'S ADDRESS","MOBILE NUMBER"]
            print(tabulate(data,headers=h))
            c=input("Are you sure want to delete the account (Y/N) : ")
            if c=='Y' or c=='y':
                st="delete from CAB_MASTER where cid="+str(n)+""
                cursor.execute(st)
                mycon.commit()
                print('CAB Deleted successfully')
            mycon.close()
            cursor.close()
            
    except :
        print('error')

"""***************************************
FUNCTION TO GENERATE booking ID
***************************************"""
 
def gen_bid():
    try:
        inFile=open("book.txt","r+")
        n=inFile.read()
        n=int(n)
        n+=1
        inFile.close()
        infile=open("book.txt",'w')
        infile.write(str(n))
        infile.close()
        #this will generate book id for each booking
        return(n)
    except IOError:
        print("I/O error occured")
"""*********************************
Function to Add booking
*********************************"""

def add_booking():
    try:
        mycon=co.connect(host="Developer",user="root",password="Dhar@#3839",database="cab_booking_db")
        cursor=mycon.cursor()
        today=date.today()
        print("Date : ",today)
        print("*"*50)
        cid=int(input("Enter cab ID : "))
        q="select * from CAB_MASTER where cid="+str(cid)
        cursor.execute(q)
        data = cursor.fetchall()
        if data==[]:
            print("No record found")
        else:
            h=["CAB ID","REG. NO.","CAB TYPE","DESCRIPTION","SEATS","OWNER'S NAME","DRIVER'S NAME","ADDRESS","MOB. NUMBER"]
            print(tabulate(data,headers=h))
            bid=gen_bid()
            print(bid)
            cnm=input("Enter customer's Name: ")
            mob=input('Enter Mobile no. : ')
            source=input('Enter pickup location : ')
            dest=input('Enter drop location : ')
            amt=float(input("Enter Bill Amount : "))
            query="insert into BOOKINGS values ("
            query+=str(bid)+","+str(cid)+",'"+cnm+"','"+mob+"','"+source+"','"+dest+"',"+str(amt)+")"
            print(query)
            cursor.execute(query)
            mycon.commit()
            print ("\n Cab booked Successfully")
            print ("\n\n YOUR booking ID IS: ",bid)
            print('Record has been saved in bookings table')
        mycon.close()
        cursor.close()
    except:
        print('error in booking')
        print( "Booking Unsuccessful")
        

"""***************************************
FUNCTION TO DELETE booking
***************************************"""
def cancel_booking(n):
    try:
        mycon=co.connect(host="Developer",user="root",password="Dhar@#3839",database="cab_booking_db")
        cursor=mycon.cursor()
        q="select * from bookings where bid="+str(n)+""
        cursor.execute(q)
        data = cursor.fetchall()
        if data==[]:
            print("No record found")
        else:
            h=["BOOKING ID","CAB ID","CUSTOMER NAME","MOB NO.","PICKUP LOCATION","DROP LOCATION"]
            print(tabulate(data,headers=h))
            c=input("Are you sure want to delete the account (Y/N) : ")
            if c=='Y' or c=='y':
                st="delete from BOOKINGS where bid="+str(n)+""
                cursor.execute(st)
                mycon.commit()
                print('Booking Cancelled successfully')
            mycon.close()
            cursor.close()
            
    except :
        print('error')



        
"""*************************************************
FUNCTION TO DISPLAY ALL bookings
*************************************************"""

def show_all_bookings():
    try:
        mycon=co.connect(host="Developer",user="root",password="Dhar@#3839",database="cab_booking_db")
        cursor=mycon.cursor()
        strQry="select * from bookings"
        cursor.execute(strQry)
        data = cursor.fetchall()
        if data == []:
            print("No records found")
        else:
            print("")
            h=["BOOKING ID","CAB ID","CUSTOMER NAME","MOB NO.","PICKUP LOCATION","DROP LOCATION","Bill"]
            #print(tabulate(data,headers=h,tablefmt='fancy_grid'))
            #print(tabulate(data,headers=h,tablefmt='textile'))
            print(tabulate(data,headers=h))
        mycon.close()
        cursor.close()
    except:
        print('error')
#**************************************************
# FUNCTION TO GENERATE BILL
#***************************************************

def bill_generate(n):
    try:
        mycon=co.connect(host="Developer",user="root",password="Dhar@#3839",database="cab_booking_db")
        cursor=mycon.cursor()
        q="select * from Bookings where BID="+str(n)
        cursor.execute(q)
        data = cursor.fetchone()
        if data==None:
            print("No record found")
            print( "\n\n Booking number not exist")
        else:
            print("...............................................")
            print("\nBILL DETAILS\n")
            print("...............................................")
            print("Booking Id :",data[0])
            print("Cab Id :",data[1])
            print("Customer Name :",data[2])
            print("Mob number :",data[3])
            print("Pickup Location :",data[4])
            print("Destination Location :",data[5])
            print("You must pay :",data[6])
            print("***********************************************")
            print(".............END OF Bill.................")
            print("***********************************************")
        mycon.close()
        cursor.close()
    except:
        print( "\n\n Booking Id not exist")
        print( "Error in bill_generate function")
        
"""****************************************************************************
                        INTRODUCTORY FUNCTION
*****************************************************************************"""
 
def intro():
    print ("CAB BOOKING SYSTEM")
    print ("PRESENTED BY : DHARMENDRA KUMAR SINGH")
    print ("COLLAGE  : GOVERNMENT POLYTECHNIC JAGANNNATHPUR, WEST SINGHBHUM, (JHARKHAND)")
    print ("BRANCH : COMPUTER SCIENCE AND ENGINEERING")
    print ("SEMESTER : 3TH SEMESTER")
    print ("YEAR : 2RD YEAR")
    input("Press Enter key to continue.............!")

#**************************************************************
# CAB MENU FUNCTION
#***********************************************************""" 
def cab_menu():
    while True:
        print (60*"=")
        print ("CAB MENU")
        print ("1. Add New Cab")
        print ("2. Modify Existing Cab")
        print ("3. Delete Cab")
        print ("4. View All Cab")
        print ("5. Search Cab")
        print ("6. Exit")
        
        
        try:
            ch=int(input("Enter Your Choice(1~6): "))
            if ch==1:
                add_cab()
                
            elif ch==2:
                modify_cab()
        
            elif ch==3:
                n=int(input("Enter CAB ID : "))
                delete_cab(n)
        
            elif ch==4:
                show_all_cab()
        
            elif ch==5:
                search_cab()
        
            elif ch==6:
                break
                
            else:
                print("Input correct choice...(1-6)")
        
        except NameError:
            print ("Input correct choice...(1-6)")
#"""""""***************************************************************************
                        #THE MAIN FUNCTION OF PROGRAM
#*****************************************************************************""""""

intro()


while True:
    print(50*"=")
    print( "\tMAIN MENU:")
    print(50*"=")
    print( "1. Cab Master Menu")
    print( "2. Cab Booking")
    print( "3. Cancel Booking")
    print( "4. Show All Booking")
    print( "5. Search Booking")
    print( "6. Exit")
    try:
        ch=int(input("Enter Your Choice(1~6): "))
        if ch==1:
            cab_menu()
        elif ch==2:
            add_booking()
        elif ch==3:
            cancel_booking()
        elif ch==4:
            show_all_bookings()
        elif ch==5:
            num=int(input("\n\nEnter Booking Number: "))
            bill_generate(num)
        elif ch==6:
            break
        else:
            print( "Input correcr choice...(1-6)")
    except NameError:
        print( "Input correct choice...(1-6)")


#*******************************************************************
input("\n\n\n\n\nTHANK YOU\n\n VISIT AGAIN \n\n Press any key to exit...")
 