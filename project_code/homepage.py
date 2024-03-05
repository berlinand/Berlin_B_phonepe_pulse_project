import streamlit as st
import os
import pandas as pd
from git import Repo
import mysql.connector
import json
import plotly.express as px
from dash import dcc, html,Dash

git_url="https://github.com/PhonePe/pulse.git"
des_path="D:/material/projects/MDE86/project_2_phonepe/data"

connection=mysql.connector.connect(host='localhost',username='root',password='berlin10',database='phonepe')
mycursor=connection.cursor()



def git_clone(git_url,des_path):
   if os.path.exists(des_path):
      print('already exits')
   else:
      Repo.clone_from(git_url,des_path)
      print("sucess")

def agg_trans_data():
   agg_trans_path=des_path+"/data/aggregated/transaction/country/india/state"
   agg_trans={'S.no':[],'State':[],'Year':[],'Quater':[],'Transaction_type':[],'Transaction_count':[],'Transaction_amount':[]}
   state_list=os.listdir(agg_trans_path)
   for x in state_list:
      state_path=agg_trans_path+'/'+x   
      year_list=os.listdir(state_path)
      for y in year_list:
         year_path=state_path+'/'+y
         file_list=os.listdir(year_path)
         for z in file_list:
            file_path=year_path+"/"+z
            datas=open(file_path)    
            data=json.load(datas)  
            if type(data['data']['transactionData'])==list:
              a=len(agg_trans['S.no'])
              for i in data['data']['transactionData']:
                Name=i['name']
                count=i['paymentInstruments'][0]['count']
                amount=i['paymentInstruments'][0]['amount']
                a=a+1
                agg_trans['S.no'].append(str(a))
                agg_trans['State'].append(x)
                agg_trans['Year'].append(str(y))
                agg_trans['Quater'].append(str(z.strip('.json')))
                agg_trans['Transaction_type'].append(Name)
                agg_trans['Transaction_count'].append(str(count))
                agg_trans['Transaction_amount'].append(str(amount))
   return agg_trans


def agg_user_data():
     agg_user_path=des_path+"/data/aggregated/user/country/india/state"
     agg_user={'S.no':[],'State':[],'Year':[],'Quater':[],'Device_brand':[],'Transaction_count':[],'Transaction_percentage':[]}
     state_list=os.listdir(agg_user_path)
     for x in state_list:
       state_path=agg_user_path+'/'+x   
       year_list=os.listdir(state_path)
       for y in year_list:
          year_path=state_path+'/'+y
          file_list=os.listdir(year_path)
          for z in file_list:
             file_path=year_path+"/"+z
             datas=open(file_path)    
             data=json.load(datas)
             if type(data['data']['usersByDevice'])==list:
               a=len(agg_user['S.no'])
               for i in data['data']['usersByDevice']:
                 Brand=i['brand']
                 count=i['count']
                 percent=i['percentage']
                 a=a+1
                 agg_user['S.no'].append(str(a))
                 agg_user['State'].append(x)
                 agg_user['Year'].append(str(y))
                 agg_user['Quater'].append(str(z.strip('.json')))
                 agg_user['Device_brand'].append(Brand)
                 agg_user['Transaction_count'].append(str(count))
                 agg_user['Transaction_percentage'].append(str(percent))

     return agg_user


def map_trans_data():
   map_trans_path=des_path+"/data/map/transaction/hover/country/india/state"
   map_trans={'S.no':[],'State':[],'Year':[],'Quater':[],'Transaction_District':[],'Transaction_count':[],'Transaction_amount':[]}
   state_list=os.listdir(map_trans_path)
   for x in state_list:
      state_path=map_trans_path+'/'+x   
      year_list=os.listdir(state_path)
      for y in year_list:
         year_path=state_path+'/'+y
         file_list=os.listdir(year_path)
         for z in file_list:
            file_path=year_path+"/"+z
            datas=open(file_path)    
            data=json.load(datas)  
            if type(data['data']['hoverDataList'])==list:
              a=len(map_trans['S.no'])
              for i in data['data']['hoverDataList']:
                Name=i['name']
                count=i['metric'][0]['count']
                amount=i['metric'][0]['amount']
                a=a+1
                map_trans['S.no'].append(str(a))
                map_trans['State'].append(x)
                map_trans['Year'].append(str(y))
                map_trans['Quater'].append(str(z.strip('.json')))
                map_trans['Transaction_District'].append(Name)
                map_trans['Transaction_count'].append(str(count))
                map_trans['Transaction_amount'].append(str(amount))
   return map_trans

def map_user_data():
     map_user_path=des_path+"/data/map/user/hover/country/india/state"
     map_user={'S.no':[],'State':[],'Year':[],'Quater':[],'Transaction_District':[],'Registered_user':[],'App_Opens':[]}
     state_list=os.listdir(map_user_path)
     for x in state_list:
       state_path=map_user_path+'/'+x   
       year_list=os.listdir(state_path)
       for y in year_list:
          year_path=state_path+'/'+y
          file_list=os.listdir(year_path)
          for z in file_list:
             file_path=year_path+"/"+z
             datas=open(file_path)    
             data=json.load(datas)
             a=len(map_user['S.no'])
             for i in data['data']['hoverData']:
                 count=data['data']['hoverData'][i]['registeredUsers']
                 app=data['data']['hoverData'][i]['appOpens']
                 a=a+1
                 map_user['S.no'].append(str(a))
                 map_user['State'].append(x)
                 map_user['Year'].append(str(y))
                 map_user['Quater'].append(str(z.strip('.json')))
                 map_user['Transaction_District'].append(i)
                 map_user['Registered_user'].append(str(count))
                 map_user['App_Opens'].append(str(app))
                 
     return map_user

def top_trans_data():
   top_trans_path=des_path+"/data/top/transaction/country/india/state"
   top_trans_district={'S.no':[],'State':[],'Year':[],'Quater':[],'Transaction_District':[],'Transaction_count':[],'Transaction_amount':[]}
   top_trans_pincode={'S.no':[],'State':[],'Year':[],'Quater':[],'Transaction_pincode':[],'Transaction_count':[],'Transaction_amount':[]}
   state_list=os.listdir(top_trans_path)
   for x in state_list:
      state_path=top_trans_path+'/'+x   
      year_list=os.listdir(state_path)
      for y in year_list:
         year_path=state_path+'/'+y
         file_list=os.listdir(year_path)
         for z in file_list:
            file_path=year_path+"/"+z
            datas=open(file_path)    
            data=json.load(datas)  
            if type(data['data']['districts'])==list:
              a=len(top_trans_district['S.no'])
              for i in data['data']['districts']:
                Name=i['entityName']
                count=i['metric']['count']
                amount=i['metric']['amount']
                a=a+1
                top_trans_district['S.no'].append(str(a))
                top_trans_district['State'].append(x)
                top_trans_district['Year'].append(str(y))
                top_trans_district['Quater'].append(str(z.strip('.json')))
                top_trans_district['Transaction_District'].append(Name)
                top_trans_district['Transaction_count'].append(str(count))
                top_trans_district['Transaction_amount'].append(str(amount))
                
            if type(data['data']['pincodes'])==list:
              a=len( top_trans_pincode['S.no'])
              for j in data['data']['pincodes']:
                Name=j['entityName']
                count=j['metric']['count']
                amount=j['metric']['amount']
                a=a+1
                top_trans_pincode['S.no'].append(str(a))
                top_trans_pincode['State'].append(x)
                top_trans_pincode['Year'].append(str(y))
                top_trans_pincode['Quater'].append(str(z.strip('.json')))
                top_trans_pincode['Transaction_pincode'].append(Name)
                top_trans_pincode['Transaction_count'].append(str(count))
                top_trans_pincode['Transaction_amount'].append(str(amount))

   return top_trans_district,top_trans_pincode

def top_user_data():
   top_user_path=des_path+"/data/top/user/country/india/state"
   top_user_district={'S.no':[],'State':[],'Year':[],'Quater':[],'Transaction_District':[],'Registered_user':[]}
   top_user_pincode={'S.no':[],'State':[],'Year':[],'Quater':[],'Transaction_pincode':[],'Registered_user':[]}
   state_list=os.listdir(top_user_path)
   for x in state_list:
      state_path=top_user_path+'/'+x   
      year_list=os.listdir(state_path)
      for y in year_list:
         year_path=state_path+'/'+y
         file_list=os.listdir(year_path)
         for z in file_list:
            file_path=year_path+"/"+z
            datas=open(file_path)    
            data=json.load(datas)  
            if type(data['data']['districts'])==list:
              a=len(top_user_district['S.no'])
              for i in data['data']['districts']:
                Name=i['name']
                user=i['registeredUsers']
                a=a+1
                top_user_district['S.no'].append(str(a))
                top_user_district['State'].append(x)
                top_user_district['Year'].append(str(y))
                top_user_district['Quater'].append(str(z.strip('.json')))
                top_user_district['Transaction_District'].append(Name)
                
                top_user_district['Registered_user'].append(str(user))
                
            if type(data['data']['pincodes'])==list:
              a=len(top_user_pincode['S.no'])
              for j in data['data']['pincodes']:
                Name=j['name']
                
                user=j['registeredUsers']
                a=a+1
                top_user_pincode['S.no'].append(str(a))
                top_user_pincode['State'].append(x)
                top_user_pincode['Year'].append(str(y))
                top_user_pincode['Quater'].append(str(z.strip('.json')))
                top_user_pincode['Transaction_pincode'].append(Name)
                
                top_user_pincode['Registered_user'].append(str(user))

   return top_user_district,top_user_pincode

def sql_agg_trans(agg_trans_df):
    
   
    query1= "show tables like 'agg_trans'"
    mycursor.execute(query1)
    result1=mycursor.fetchall()
    if len(result1)==0:
       query2="""create table agg_trans(
          S_no int primary key,
          State varchar(255),
          Year int,
          Quater int,
          Transaction_type varchar(255),
          Transaction_count int,
          Transaction_amount decimal(40,12)
          )"""
       mycursor.execute(query2)
       
       query3="""insert into agg_trans(S_no,State,Year,Quater,Transaction_type,Transaction_count,Transaction_amount) values(%s,%s,%s,%s,%s,%s,%s)"""
       datas=[]
       for x in agg_trans_df.index:
         row=tuple(agg_trans_df.iloc[x])
         datas.append(row)

       mycursor.executemany(query3,datas)
       connection.commit()


def sql_agg_user(agg_user_df):
   
    query1= "show tables like 'agg_user'"
    mycursor.execute(query1)
    result1=mycursor.fetchall()
    if len(result1)==0:

       query2="""create table agg_user(
          S_no int primary key,
          State varchar(255),
          Year int,
          Quater int,
         Device_brand varchar(255),
          Transaction_count int,
          Transaction_percentage decimal(20,19)
          )"""
       mycursor.execute(query2)
       
       query3="""insert into agg_user(S_no,State,Year,Quater,Device_brand,Transaction_count,Transaction_percentage) values(%s,%s,%s,%s,%s,%s,%s)"""
       datas=[]
       for x in agg_user_df.index:
         row=tuple(agg_user_df.iloc[x])
         datas.append(row)

       mycursor.executemany(query3,datas)
       connection.commit()

def sql_map_trans(map_trans_df):
    
    
    query1= "show tables like 'map_trans'"
    mycursor.execute(query1)
    result1=mycursor.fetchall()
    if len(result1)==0:
       query2="""create table map_trans(
          S_no int primary key,
          State varchar(255),
          Year int,
          Quater int,
          Transaction_District varchar(255),
          Transaction_count int,
          Transaction_amount decimal(40,12)
          )"""
       mycursor.execute(query2)
       
       query3="""insert into map_trans(S_no,State,Year,Quater,Transaction_District,Transaction_count,Transaction_amount) values(%s,%s,%s,%s,%s,%s,%s)"""
       datas=[]
       for x in map_trans_df.index:
         row=tuple(map_trans_df.iloc[x])
         datas.append(row)

       mycursor.executemany(query3,datas)
       connection.commit()

def sql_map_user(map_user_df):
   
    
    query1= "show tables like 'map_user'"
    mycursor.execute(query1)
    result1=mycursor.fetchall()
    if len(result1)==0:

       query2="""create table map_user(
          S_no int primary key,
          State varchar(255),
          Year int,
          Quater int,
          Transaction_District varchar(255),
          Registered_user int,
          App_open int
          
          )"""
       mycursor.execute(query2)
       
       query3="""insert into map_user(S_no,State,Year,Quater,Transaction_District,Registered_user,App_open) values(%s,%s,%s,%s,%s,%s,%s)"""
       datas=[]
       for x in map_user_df.index:
         row=tuple(map_user_df.iloc[x])
         datas.append(row)

       mycursor.executemany(query3,datas)
       connection.commit()

def sql_top_trans(top_trans_dis_df,top_trans_pin_df):
    
    query1= "show tables like 'top_trans_district'"
    mycursor.execute(query1)
    result1=mycursor.fetchall()
    if len(result1)==0:
       query2="""create table top_trans_district(
          S_no int primary key,
          State varchar(255),
          Year int,
          Quater int,
          Transaction_District varchar(255),
          Transaction_count int,
          Transaction_amount decimal(40,12)
          )"""
       mycursor.execute(query2)
       
       query3="""insert into top_trans_district(S_no,State,Year,Quater,Transaction_District,Transaction_count,Transaction_amount) 
               values(%s,%s,%s,%s,%s,%s,%s)"""
       datas=[]
       for x in top_trans_dis_df.index:
         row=tuple(top_trans_dis_df.iloc[x])
         datas.append(row)

       mycursor.executemany(query3,datas)
       connection.commit()


   
    query4= "show tables like 'top_trans_pincode'"
    mycursor.execute(query4)
    result1=mycursor.fetchall()
    if len(result1)==0:
       query5="""create table top_trans_pincode(
          S_no int primary key,
          State varchar(255),
          Year int,
          Quater int,
          Transaction_pincode varchar(255),
          Transaction_count int,
          Transaction_amount decimal(40,12)
          )"""
       mycursor.execute(query5)
       
       query6="""insert into top_trans_pincode(S_no,State,Year,Quater,Transaction_pincode,Transaction_count,Transaction_amount) 
               values(%s,%s,%s,%s,%s,%s,%s)"""
       datas1=[]
       for y in top_trans_pin_df.index:
         row=tuple(top_trans_pin_df.iloc[y])
         datas1.append(row)

       mycursor.executemany(query6,datas1)
       connection.commit()

def sql_top_user(top_user_dis_df,top_user_pin_df): 
   
    query1= "show tables like 'top_user_district'"
    mycursor.execute(query1)
    result1=mycursor.fetchall()
    if len(result1)==0:
       query2="""create table top_user_district(
          S_no int primary key,
          State varchar(255),
          Year int,
          Quater int,
          Transaction_District varchar(255),
          Registered_user int
          
          )"""
       mycursor.execute(query2)
       
       query3="""insert into top_user_district(S_no,State,Year,Quater,Transaction_District,Registered_user) 
               values(%s,%s,%s,%s,%s,%s)"""
       datas=[]
       for x in  top_user_dis_df.index:
         row=tuple( top_user_dis_df.iloc[x])
         datas.append(row)

       mycursor.executemany(query3,datas)
       connection.commit()



    
    query4= "show tables like 'top_user_pincode'"
    mycursor.execute(query4)
    result1=mycursor.fetchall()
    if len(result1)==0:
       query5="""create table top_user_pincode(
          S_no int primary key,
          State varchar(255),
          Year int,
          Quater int,
          Transaction_pincode varchar(255),
          Registered_user int
          
          )"""
       mycursor.execute(query5)
       
       query6="""insert into top_user_pincode(S_no,State,Year,Quater,Transaction_pincode,Registered_user) 
               values(%s,%s,%s,%s,%s,%s)"""
       datas1=[]
       for y in top_user_pin_df.index:
         row=tuple(top_user_pin_df.iloc[y])
         datas1.append(row)

       mycursor.executemany(query6,datas1)
       connection.commit()


def map1():
   fig=px.scatter_mapbox()

#------------------------------------------------------
git_clone(git_url,des_path)

agg_trans=agg_trans_data()
agg_trans_df=pd.DataFrame(agg_trans)

agg_user=agg_user_data()
agg_user_df=pd.DataFrame(agg_user)

map_trans=map_trans_data()
map_trans_df=pd.DataFrame(map_trans)
map_user=map_user_data()
map_user_df=pd.DataFrame(map_user)

top_trans_district,top_trans_pincode=top_trans_data()
top_trans_dis_df=pd.DataFrame(top_trans_district)
top_trans_pin_df=pd.DataFrame(top_trans_pincode)


top_user_district,top_user_pincode=top_user_data()
top_user_dis_df=pd.DataFrame(top_user_district)
top_user_pin_df=pd.DataFrame(top_user_pincode)

sql_agg_trans(agg_trans_df)
sql_agg_user(agg_user_df)
sql_map_trans(map_trans_df)
sql_map_user(map_user_df)
sql_top_trans(top_trans_dis_df,top_trans_pin_df)
sql_top_user(top_user_dis_df,top_user_pin_df)

st.title(":violet[Phonepe] :red[Pulse]")
st.header("Data Visualization Exploration")
map1(agg_trans_df)
