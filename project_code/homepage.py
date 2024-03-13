import streamlit as st
import os
import pandas as pd
from git import Repo
import mysql.connector
import json
import plotly.express as px
from dash import dcc, html,Dash,callback,Input,Output

#paste your State map json file
json_path1 =""
with open(json_path1, 'r') as f:
    india_map1 = json.load(f)

#paste your district map json file 
json_path2 =""
with open(json_path2, 'r') as g:
    india_map2=""
git_url="https://github.com/PhonePe/pulse.git"
des_path=""

#paste your mysql connection and database 
connection=mysql.connector.connect(host='localhost',username='root',password='berlin0',database='phonepe')
mycursor=connection.cursor()


#This function for cloning the data from git and store it in local
def git_clone(git_url,des_path):
   if os.path.exists(des_path):
      print('already exits')
   else:
      Repo.clone_from(git_url,des_path)
      print("sucess")

#This function capitalize the state name
def states(state):
     state=state.capitalize()
     return state

#This function check the district name and change it name according to map district name
def districts(district,state):
       if district=='marigaon':
          district='Morigaon'
          return district
       elif district=='purbi champaran':
          district='Purvi champaran'
          return district
       elif district=='pashchim champaran':
          district='Paschimi champaran'
          return district
       elif district=='west' and state=='Delhi':
          district='West delhi'
          return district   
       elif district=='north west' and state=='Delhi':
          district='North west delhi'
          return district   
       elif district=='north' and state=='Delhi':
          district='North delhi'
          return district   
       elif district=='east' and state=='Delhi':
          district='East delhi'
          return district          
       elif district=='south'and state=='Delhi':
          district='South delhi'
          return district   
       elif district=='central' and state=='Delhi':
          district='Central delhi'
          return district 
       elif district=='south west' and state=='Delhi':
          district='South west delhi'
          return district        
       elif district=='north east' and state=='Delhi':
          district='North east delhi'
          return district 
       elif district=='peddapalle':
          district='Peddapalli'
          return district  
       elif district=='koch bihar':
          district='Cooch behar'
          return district 
       elif district=='darjiling':
            district='Darjeeling'
            return district 
       elif district=='korea':
            district='Koriya'
            return district
       elif district=='pratapgarh' and state=="Uttar-pradesh":
            district='Pratapgarh-uttar'
            return district
       elif district=='aurangabad' and state=="Bihar":
            district='Aurangabad-bihar'
            return district
       elif district=='hamirpur' and state=="Uttar-pradesh":
            district='Hamirpur-uttar'
            return district

       elif district=='bilaspur' and state=="Chhattisgarh":
            district='Bilaspur-chhattisgarh'
            return district
       elif district=='balrampur' and state=="Chhattisgarh":
            district='Balrampur-chhattisgarh'
            return district
       else:
         district=district.capitalize()
         return district

#This function  collect the data from aggregated transaction and convert in proper dict and return agg_trans 
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
                st=states(x)
                agg_trans['S.no'].append(str(a))
                agg_trans['State'].append(st)
                agg_trans['Year'].append(str(y))
                agg_trans['Quater'].append(str(z.strip('.json')))
                agg_trans['Transaction_type'].append(Name)
                agg_trans['Transaction_count'].append(str(count))
                agg_trans['Transaction_amount'].append(str(amount))
   return agg_trans

#This function  collect the data from aggregated user and convert in proper dict and return agg_user 
def agg_user_data():
     agg_user_path=des_path+"/data/aggregated/user/country/india/state"
     agg_user={'S.no':[],'State':[],'Year':[],'Quater':[],'Registered_Users':[],'App_open':[]}
     state_list=os.listdir(agg_user_path)
     for x in state_list:
       state_path=agg_user_path+'/'+x   
       year_list=os.listdir(state_path)
       for y in year_list:
          year_path=state_path+'/'+y
          file_list=os.listdir(year_path)
          a=len(agg_user['S.no'])
          for z in file_list:
             file_path=year_path+"/"+z
             datas=open(file_path)    
             data=json.load(datas)

             opens=data['data']['aggregated']["appOpens"]
             users=data['data']['aggregated']["registeredUsers"]
             a=a+1
             st=states(x)
             agg_user['S.no'].append(str(a))
             agg_user['State'].append(st)
             agg_user['Year'].append(str(y))
             agg_user['Quater'].append(str(z.strip('.json')))
             agg_user['Registered_Users'].append(str(users))
             agg_user['App_open'].append(str(opens))
                

     return agg_user

#This function  collect the data from map transaction and convert in proper dict and return map_trans 
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
                Name=Name.removesuffix(' district')
                
                count=i['metric'][0]['count']
                amount=i['metric'][0]['amount']
                a=a+1
                st=states(x)
                name=districts(Name,st)
                
                map_trans['S.no'].append(str(a))
                map_trans['State'].append(st)
                map_trans['Year'].append(str(y))
                map_trans['Quater'].append(str(z.strip('.json')))
                map_trans['Transaction_District'].append(name)
                map_trans['Transaction_count'].append(str(count))
                map_trans['Transaction_amount'].append(str(amount))
   return map_trans

#This function  collect the data from map user and convert in proper dict and return map_user
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
                 st=states(x)
                 i=i.removesuffix(" district")
                 name=districts(i,st)
                
                 map_user['S.no'].append(str(a))
                 map_user['State'].append(st)
                 map_user['Year'].append(str(y))
                 map_user['Quater'].append(str(z.strip('.json')))
                 map_user['Transaction_District'].append(name)
                 map_user['Registered_user'].append(str(count))
                 map_user['App_Opens'].append(str(app))
                 
     return map_user

#This function  collect the data from top transaction and convert in proper dict and return top_trans_district,top_trans_pincode
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
                st=states(x)
                name=districts(Name,st)
                top_trans_district['S.no'].append(str(a))
                top_trans_district['State'].append(st)
                top_trans_district['Year'].append(str(y))
                top_trans_district['Quater'].append(str(z.strip('.json')))
                top_trans_district['Transaction_District'].append(name)
                top_trans_district['Transaction_count'].append(str(count))
                top_trans_district['Transaction_amount'].append(str(amount))
                
            if type(data['data']['pincodes'])==list:
              a=len( top_trans_pincode['S.no'])
              for j in data['data']['pincodes']:
                Name=j['entityName']
                count=j['metric']['count']
                amount=j['metric']['amount']
                a=a+1
                st=states(x)
                top_trans_pincode['S.no'].append(str(a))
                top_trans_pincode['State'].append(st)
                top_trans_pincode['Year'].append(str(y))
                top_trans_pincode['Quater'].append(str(z.strip('.json')))
                top_trans_pincode['Transaction_pincode'].append(Name)
                top_trans_pincode['Transaction_count'].append(str(count))
                top_trans_pincode['Transaction_amount'].append(str(amount))

   return top_trans_district,top_trans_pincode

#This function  collect the data from top user and convert in proper dict and return top_user_district,top_user_pincode
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
                st=states(x)
                name=districts(Name,st)
                top_user_district['S.no'].append(str(a))
                top_user_district['State'].append(st)
                top_user_district['Year'].append(str(y))
                top_user_district['Quater'].append(str(z.strip('.json')))
                top_user_district['Transaction_District'].append(name)
                
                top_user_district['Registered_user'].append(str(user))
                
            if type(data['data']['pincodes'])==list:
              a=len(top_user_pincode['S.no'])
              for j in data['data']['pincodes']:
                Name=j['name']
                
                user=j['registeredUsers']
                a=a+1
                st=states(x)
                top_user_pincode['S.no'].append(str(a))
                top_user_pincode['State'].append(st)
                top_user_pincode['Year'].append(str(y))
                top_user_pincode['Quater'].append(str(z.strip('.json')))
                top_user_pincode['Transaction_pincode'].append(Name)
                
                top_user_pincode['Registered_user'].append(str(user))

   return top_user_district,top_user_pincode

#This function  store the data in mysql from agg_trans_df
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

#This function  store the data in mysql from agg_user_df
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
          Registered_Users int,
          App_open bigint 
          )"""
       mycursor.execute(query2)
       
       query3="""insert into agg_user(S_no,State,Year,Quater,Registered_Users,App_open) values(%s,%s,%s,%s,%s,%s)"""
       datas=[]
       for x in agg_user_df.index:
         row=tuple(agg_user_df.iloc[x])
         datas.append(row)

       mycursor.executemany(query3,datas)
       connection.commit()

#This function  store the data in mysql from map_trans_df
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

#This function  store the data in mysql from map_user_df
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

#This function  store the data in mysql from top_trans_dis_df,top_trans_pin_df
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

#This function  store the data in mysql from top_user_dis_df,top_user_pin_df
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

#This function gives map state data according to user
def map1_data(use,year,Quater):
 
   quater=int(Quater[1:2])
   if use=='Transactions':   
        
        query7=   f"""select State,sum(Transaction_count) ,sum(Transaction_amount) ,
                sum(Transaction_amount)/sum(Transaction_count)  
                from agg_trans where Year={year} and Quater={quater} group by State
          """ 
        mycursor.execute(query7)
        result=mycursor.fetchall()
        df1=pd.DataFrame(result,columns=['State','All Transactions','Total Payment Value','AVG Transaction Value'])


   elif use=='Users':
      mycursor.execute(
       f"select State,Registered_Users,App_open from agg_user where Year={year} and Quater={quater} " )
      result=mycursor.fetchall()
      df1=pd.DataFrame(result,columns=['State','Registered Users','App opens'])
      df1['App opens']=df1['App opens'].replace(0,'Unavailable')     

   
   return df1

#This function gives map district data according to user
def map2_data(use,year,Quater):
 
   quater=int(Quater[1:2])
   if use=='Transactions':   
        
        query7=  f"""select State,Transaction_District,Transaction_count,Transaction_amount,
    (Transaction_amount/Transaction_count) from map_trans where Year={year} and Quater={quater}"""
        
        mycursor.execute(query7)
        result=mycursor.fetchall()
        df2=pd.DataFrame(result,columns=['State','District','All Transactions','Total Payment Value',"Avg. Transaction Value"])
        

   elif use=='Users':
      mycursor.execute(
       f"select State,Transaction_District,Registered_User,App_open from map_user where Year={year} and Quater={quater} " )
      result=mycursor.fetchall()
      df2=pd.DataFrame(result,columns=['State','District','Registered Users','App opens'])
      df2['App opens']=df2['App opens'].replace(0,'Unavailable')    


   return df2

#This function gives chart data according to user
def map_userli(us_tr,year,qu):
      df_data=map2_data(us_tr,year,qu)
      map_usli=list(df_data.columns)
      if "S.no" in map_usli or "Year" in map_usli and "Quater" in map_usli:
        map_usli.remove("Year")
        map_usli.remove("Quater")
      return map_usli

#This function gives chart data according to user
def map_transli(us_tr,year,qu):
   df_data=map2_data(us_tr,year,qu)
   map_trli=list(df_data.columns)
   if "S.no" in map_trli or "Year" in map_trli and "Quater" in map_trli:
     map_trli.remove("Year")
     map_trli.remove("Quater")
   return map_trli
#This function gives chart data according to user
def map_useli(us_tr,year,qu):
    map_usli=map_userli(us_tr,year,qu)
    if "State" in map_usli and "District" in map_usli: 
     map_usli.remove("State")
     map_usli.remove("District")
    return map_usli  
#This function gives chart data according to user
def map_transli1(us_tr,year,qu):
     map_trli=map_transli(us_tr,year,qu)
     if "State" in map_trli and "District" in map_trli: 
       map_trli.remove("State")
       map_trli.remove("District")
     return map_trli

#This function gives state map
def map1(use,year,Quater,select2):
   df1=map1_data(use,year,Quater)
   if use=='Transactions': 
        if select2=='District':
           select2='State'
        fig=px.choropleth(
                   df1,
                geojson=india_map1,
               featureidkey='properties.st_nm',
               locations="State",
                color=select2,
               color_continuous_scale='Reds',
                 hover_data=['State','All Transactions','Total Payment Value','AVG Transaction Value']  )
    
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(title_text='India State Map', hoverlabel=dict(bgcolor="white", font_size=16, font_family="Rockwell"))
        st.plotly_chart(fig, theme="streamlit", use_container_width=True,height=1780)

   elif use=='Users': 
      if select2=='District':
           select2='State'      
      fig=px.choropleth(
                   df1,
                geojson=india_map1,
               featureidkey='properties.st_nm',
               locations="State",
                color=select2,
               color_continuous_scale='Reds',
                 hover_data=['State','Registered Users','App opens']  )
    
      fig.update_geos(fitbounds="locations", visible=False)
      fig.update_layout(title_text='India State Map', hoverlabel=dict(bgcolor="white", font_size=16, font_family="Rockwell"))
      st.plotly_chart(fig, theme="streamlit", use_container_width=True,height=1780)  

#This function gives District map according to user
def map2(use,year,Quater,select2): 

   df2=map2_data(use,year,Quater) 
   if use=='Transactions':
       
        fig=px.choropleth(
                   df2,
                geojson=india_map2,
               featureidkey='properties.district',
               locations="District",
                color=select2,
               color_continuous_scale='Reds',
                 hover_data=['State','District','All Transactions','Total Payment Value',"Avg. Transaction Value"] )
    
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(title_text='India District Map', hoverlabel=dict(bgcolor="white", font_size=16, font_family="Rockwell"))
        st.plotly_chart(fig, theme="streamlit", use_container_width=True,height=1780)


   elif use=='Users':
      fig=px.choropleth(
                   df2,
                geojson=india_map2,
               featureidkey='properties.district',
               locations="District",
                color=select2,
               color_continuous_scale='Reds',
                 hover_data=['State','District','Registered Users','App opens']  )
    
      fig.update_geos(fitbounds="locations", visible=False)
      fig.update_layout(title_text='India District Map', hoverlabel=dict(bgcolor="white", font_size=16, font_family="Rockwell"))
      st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
#This function gives state, district map chart according to user
def map3(use,year,Quater,select1,select2,select3):
        
 
   if use=='Transactions':
     df1=map1_data(use,year,Quater)
     st_ate=df1[df1['State']==select1]
     st.write(f"State  :red[{ select1}]")    
     st.write(f"All Transactions  :red[{st_ate.iloc[0,1]}]")  
     st.write(f"Total Payment Value  :red[{st_ate.iloc[0,2]}]") 
     st.write(f"Avg. Transaction Value  :red[{st_ate.iloc[0,3]}]")

     df2=map2_data(use,year,Quater) 
     dis=df2[df2['State']==select1]
     df2=map2_data(use,year,Quater)
     fig=px.choropleth(
                  dis,
                geojson=india_map2,
               featureidkey='properties.district',
               locations="District",
                color=select2,
               color_continuous_scale='Reds',
                 hover_data=['State','District','All Transactions','Total Payment Value',"Avg. Transaction Value"] )
    
     fig.update_geos(fitbounds="locations", visible=False)
     fig.update_layout(title_text='State District Map', hoverlabel=dict(bgcolor="white", font_size=16, font_family="Rockwell"))
     st.plotly_chart(fig, theme="streamlit", use_container_width=True,height=1780)
     
     if select4=='Pie chart':
       fig1=px.pie(
          dis,
          names='District',
          values=select3,
          title="Pie chart"
           )
       fig1.update_traces(textposition='inside', textinfo='percent+label',textfont_size=16)
       fig1.update_layout(hoverlabel_font_size=20,hoverlabel_font_family='Arial')
       st.plotly_chart(fig1, theme="streamlit", use_container_width=True,height=1780)
     elif select4=="Scatter plots chart":
       fig1=px.scatter(
          dis,
          x='District',
          y=select3,
          title="Scatter plots chart"
           )
       
       fig1.update_layout(hoverlabel_font_size=20,hoverlabel_font_family='Arial')
       st.plotly_chart(fig1, theme="streamlit", use_container_width=True,height=1780)   

     elif select4=="Line chart":   
       fig1=px.line(
          dis,
          x='District',
          y=select3,
          title="Line chart"
           )
       
       fig1.update_layout(hoverlabel_font_size=20,hoverlabel_font_family='Arial')
       st.plotly_chart(fig1, theme="streamlit", use_container_width=True,height=1780)  
        
     elif select4=="Bar chart":   
       fig1=px.bar(
          dis,
          x='District',
          y=select3,
          title="Bar chart"
           )
       
       fig1.update_layout(hoverlabel_font_size=20,hoverlabel_font_family='Arial')
       st.plotly_chart(fig1, theme="streamlit", use_container_width=True,height=1780)   

   elif use=='Users':
     df1=map1_data(use,year,Quater)
     st_ate=df1[df1['State']==select1]
     st.write(f"State  :red[{ select1}]")    
     st.write(f"Registered Users  :red[{st_ate.iloc[0,1]}]")  
     st.write(f"App opens  :red[{st_ate.iloc[0,2]}]") 
    

     df2=map2_data(use,year,Quater) 
     dis=df2[df2['State']==select1]
     df2=map2_data(use,year,Quater)
     fig=px.choropleth(
                   dis,
                geojson=india_map2,
               featureidkey='properties.district',
               locations="District",
                color=select2,
               color_continuous_scale='Reds',
                 hover_data=['State','District','Registered Users','App opens']  )
    
     fig.update_geos(fitbounds="locations", visible=False)
     fig.update_layout(title_text='State District Map', hoverlabel=dict(bgcolor="white", font_size=16, font_family="Rockwell"))
     st.plotly_chart(fig, theme="streamlit", use_container_width=True)
     if select4=='Pie chart':
       fig1=px.pie(
          dis,
          names='District',
          values=select3,
          title="Pie chart"
           )
       fig1.update_traces(textposition='inside', textinfo='percent+label',textfont_size=16)
       fig1.update_layout(hoverlabel_font_size=20,hoverlabel_font_family='Arial')
       st.plotly_chart(fig1, theme="streamlit", use_container_width=True,height=1780)

     elif select4=="Scatter plots chart":
       fig1=px.scatter(
          dis,
          x='District',
          y=select3,
          title="Scatter plots chart"
        )
       fig1.update_layout(hoverlabel_font_size=20,hoverlabel_font_family='Arial')
       st.plotly_chart(fig1, theme="streamlit", use_container_width=True,height=1780) 

     elif select4=="Line chart":   
       fig1=px.line(
          dis,
          x='District',
          y=select3,
          title="Line chart"
           )
       
       fig1.update_layout(hoverlabel_font_size=20,hoverlabel_font_family='Arial')
       st.plotly_chart(fig1, theme="streamlit", use_container_width=True,height=1780)   

     elif select4=="Bar chart":   
       fig1=px.bar(
          dis,
          x='District',
          y=select3,
          title="Bar chart"
           )
       
       fig1.update_layout(hoverlabel_font_size=20,hoverlabel_font_family='Arial')
       st.plotly_chart(fig1, theme="streamlit", use_container_width=True,height=1780)

#This function display charts according to user
def charts(dis,select4,staordis,value):
     if select4=='Pie chart':
       fig1=px.pie(
          dis,
          names=staordis,
          values=value,
          title="Pie chart"
           )
       fig1.update_traces(textposition='inside', textinfo='percent+label',textfont_size=16)
       fig1.update_layout(hoverlabel_font_size=20,hoverlabel_font_family='Arial')
       st.plotly_chart(fig1, theme="streamlit", use_container_width=True,height=1780)
     elif select4=="Scatter plots chart":
       fig1=px.scatter(
          dis,
          x=staordis,
          y=value,
          title="Scatter plots chart"
           )
       
       fig1.update_layout(hoverlabel_font_size=20,hoverlabel_font_family='Arial')
       st.plotly_chart(fig1, theme="streamlit", use_container_width=True,height=1780)   

     elif select4=="Line chart":   
       fig1=px.line(
          dis,
          x=staordis,
          y=value,
          title="Line chart"
           )
       
       fig1.update_layout(hoverlabel_font_size=20,hoverlabel_font_family='Arial')
       st.plotly_chart(fig1, theme="streamlit", use_container_width=True,height=1780)  
        
     elif select4=="Bar chart":   
       fig1=px.bar(
          dis,
          x=staordis,
          y=value,
          title="Bar chart"
           )
       
       fig1.update_layout(hoverlabel_font_size=20,hoverlabel_font_family='Arial')
       st.plotly_chart(fig1, theme="streamlit", use_container_width=True,height=1780)   

#This function gives facts about phonepe pulse  
def question(ques,year,Quater,select4):
   quater=int(Quater[1:2])
   if ques=="What are the top ten transaction amount districts?":
      query=f"""select Transaction_District,State,Transaction_amount
       from top_trans_district  
       where Year={year} and Quater={quater} order by Transaction_amount desc limit 10 """    
      mycursor.execute(query)
      result=mycursor.fetchall()
      qdf=pd.DataFrame(result,columns=['District','State','Total Transaction Amount'])
      st.write(qdf)
      staordis='District'
      value='Total Transaction Amount'
      charts(qdf,select4,staordis,value)

   elif ques=="What are the top ten districts by average transaction amount?":
      query=f"""select Transaction_District,State,
    (Transaction_amount/Transaction_count) as avgam from top_trans_district 
    where Year={year} and Quater={quater} order by avgam desc limit 10 """          
      mycursor.execute(query)
      result=mycursor.fetchall()
      qdf=pd.DataFrame(result,columns=['District','State','AVG Transaction Amount'])
      st.write(qdf)
      staordis='District'
      value='AVG Transaction Amount'
      charts(qdf,select4,staordis,value) 

   elif ques=="What are the top ten transaction counts by district?":
      query=f"""select Transaction_District,State,
     Transaction_count from top_trans_district 
    where Year={year} and Quater={quater} order by Transaction_count desc limit 10 """          
      mycursor.execute(query)
      result=mycursor.fetchall()
      qdf=pd.DataFrame(result,columns=['District','State','Transaction count'])
      st.write(qdf)
      staordis='District'
      value='Transaction count'
      charts(qdf,select4,staordis,value) 

   elif ques=="What are the top ten transaction amount pincode ?":
      query=f"""select Transaction_pincode,State,Transaction_amount
       from top_trans_pincode  
       where Year={year} and Quater={quater} order by Transaction_amount desc limit 10 """    
      mycursor.execute(query)
      result=mycursor.fetchall()
      qdf=pd.DataFrame(result,columns=['Transaction pincode','State','Total Transaction Amount'])
      st.write(qdf)
      staordis='Transaction pincode'
      value='Total Transaction Amount'
      charts(qdf,select4,staordis,value)

   elif ques=="What are the top ten pincode by average transaction amount?":
      query=f"""select Transaction_pincode,State,
    (Transaction_amount/Transaction_count) as avgam from top_trans_pincode  
    where Year={year} and Quater={quater} order by avgam desc limit 10 """          
      mycursor.execute(query)
      result=mycursor.fetchall()
      qdf=pd.DataFrame(result,columns=['Transaction pincode','State','AVG Transaction Amount'])
      st.write(qdf)
      staordis='Transaction pincode'
      value='AVG Transaction Amount'
      charts(qdf,select4,staordis,value) 
   
   elif ques=="What are the top ten transaction counts by pincode ?":
      query=f"""select Transaction_pincode,State,
     Transaction_count from top_trans_pincode 
    where Year={year} and Quater={quater} order by Transaction_count desc limit 10 """          
      mycursor.execute(query)
      result=mycursor.fetchall()
      qdf=pd.DataFrame(result,columns=['Transaction pincode','State','Transaction count'])
      st.write(qdf)
      staordis='Transaction pincode'
      value='Transaction count'
      charts(qdf,select4,staordis,value) 

   elif ques=="What are the top ten districts by registered users?":
      query=f"""select Transaction_District,State,Registered_user
       from top_user_district 
       where Year={year} and Quater={quater} order by Registered_user desc limit 10 """    
      mycursor.execute(query)
      result=mycursor.fetchall()
      qdf=pd.DataFrame(result,columns=['District','State','Registered user'])
      st.write(qdf)
      staordis='District'
      value='Registered user'
      charts(qdf,select4,staordis,value)

   elif ques=="What are the top ten pincode by registered users?":
      query=f"""select Transaction_pincode,State,Registered_user
       from top_user_pincode
       where Year={year} and Quater={quater} order by Registered_user desc limit 10 """    
      mycursor.execute(query)
      result=mycursor.fetchall()
      qdf=pd.DataFrame(result,columns=['Transaction_pincode','State','Registered user'])
      st.write(qdf)
      staordis='Transaction_pincode'
      value='Registered user'
      charts(qdf,select4,staordis,value)

   elif ques=="What are the top ten transaction amount State?":
      query=f"""select State,sum(Transaction_amount) as sam
       from top_trans_district
       where Year={year} and Quater={quater} group by State order by sam desc limit 10 """    
      mycursor.execute(query)
      result=mycursor.fetchall()
      qdf=pd.DataFrame(result,columns=['State','Total Transaction Amount'])
      st.write(qdf)
      staordis='State'
      value='Total Transaction Amount'
      charts(qdf,select4,staordis,value)
   
   elif ques=="What are the top ten State by average transaction amount?":
      query=f""" select State,
    (Transaction_amount/Transaction_count) as avgam ,Transaction_type from agg_trans 
    where Year={year} and Quater={quater} order by avgam desc limit 10 """          
      mycursor.execute(query)
      result=mycursor.fetchall()
      qdf=pd.DataFrame(result,columns=['State','AVG Transaction Amount','Transaction Type'])
      st.write(qdf)
      staordis='State'
      value='AVG Transaction Amount'
      charts(qdf,select4,staordis,value) 

   elif ques=="What are the top ten transaction counts by State?":
      query=f"""select State,
     Transaction_count,Transaction_type from agg_trans 
    where Year={year} and Quater={quater} order by Transaction_count desc limit 10 """          
      mycursor.execute(query)
      result=mycursor.fetchall()
      qdf=pd.DataFrame(result,columns=['State','Transaction count','Transaction Type'])
      st.write(qdf)
      staordis='State'
      value='Transaction count'
      charts(qdf,select4,staordis,value) 
  
   elif ques=="What are the different categories of transactions by amount?":
      query=f"""select Transaction_type,sum(Transaction_amount) as tam from agg_trans 
    where Year={year} and Quater={quater} group by Transaction_type order by tam desc """          
      mycursor.execute(query)
      result=mycursor.fetchall()
      qdf=pd.DataFrame(result,columns=['Transaction Type','Total Transaction amount'])
      st.write(qdf)
      staordis='Transaction Type'
      value='Total Transaction amount'
      charts(qdf,select4,staordis,value) 

   elif ques=="What are the different categories of transactions by count?":
      query=f"""select Transaction_type,sum(Transaction_count) as tam from agg_trans 
    where Year={year} and Quater={quater} group by Transaction_type order by tam desc """          
      mycursor.execute(query)
      result=mycursor.fetchall()
      qdf=pd.DataFrame(result,columns=['Transaction Type','Total Transaction count'])
      st.write(qdf)
      staordis='Transaction Type'
      value='Total Transaction count'
      charts(qdf,select4,staordis,value) 

   elif ques=="What are the Total transaction amount, Average transaction amount, and Total transaction count?":
      query=f"""select sum(Transaction_amount) as sam,(sum(Transaction_amount)/sum(Transaction_count))as samco,sum(Transaction_count) as sco
       from agg_trans
       where Year={year} and Quater={quater}"""    
      mycursor.execute(query)
      result=mycursor.fetchall()
      qdf=pd.DataFrame(result,columns=['Total Transaction Amount','AVG Transaction Amount','Total Transaction count'])
      st.warning(f"Total Transaction Amount {':'} :red[{qdf.iloc[0,0]}]")   
      st.warning(f"AVG Transaction Amount {':'} :red[{qdf.iloc[0,1]}]") 
      st.warning(f"Total Transaction count {':'} :red[{qdf.iloc[0,2]}]")   

   elif ques=="What are the Total Registered PhonePe users, Total App open ?":
      query=f"""select sum(Registered_Users) as sam,sum(App_open) as sco
       from agg_user
       where Year={year} and Quater={quater}"""    
      mycursor.execute(query)
      result=mycursor.fetchall()
      qdf=pd.DataFrame(result,columns=['Total Registered PhonePe users','Total App open '])
      st.warning(f"Total Registered PhonePe users {':'} :red[{qdf.iloc[0,0]}]")   
      st.warning(f"Total App open {':'} :red[{qdf.iloc[0,1]}]") 
      
#---------------------------------------------------------------------------------------
git_clone(git_url,des_path)

agg_trans=agg_trans_data()
agg_trans_df=pd.DataFrame(agg_trans)
stk=agg_trans_df['State'].unique()
li=list(stk)
li.insert(0,"select a state from below")

agg_user=agg_user_data()
agg_user_df=pd.DataFrame(agg_user)

map_trans=map_trans_data()
map_trans_df=pd.DataFrame(map_trans)


map_user=map_user_data()
map_user_df=pd.DataFrame(map_user)
map_usli=list(map_user_df.columns)
map_usli.remove("S.no")

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
co1,co2,co3=st.columns(3)
us_tr=co1.selectbox(label='select one',options=['Users','Transactions'])
year=co2.selectbox(label='select one',options=[2018,2019,2020,2021,2022,2023])
qu=co3.selectbox(label='select one',options=['Q1 (Jan-Mar)','Q2 (Apr-Jun)','Q3 (Jul-Sep)','Q4 (Oct-Dec)'])
co4,co5=st.columns(2)
co6,co7,co8,co9=st.columns(4)
states_map=co4.checkbox(label="India State Map")
districts_map=co5.checkbox(label="India District Map")
select1= co6.selectbox(label="select a state",options=li,placeholder="select a state")   



if us_tr=='Users':
   map_usli= map_userli(us_tr,year,qu)
   select2=co7.selectbox(label="select a value",options=map_usli) 
   
   
elif us_tr=='Transactions' :
  map_trli=map_transli(us_tr,year,qu)
  select2=co7.selectbox(label="select a value",options=map_trli)  

if  us_tr=='Users':
   map_usli1=map_useli(us_tr,year,qu)
   select3=co9.selectbox(label="select a Chart value",options=map_usli1)

elif us_tr=='Transactions':
   map_tranli1=map_transli1(us_tr,year,qu)
   select3=co9.selectbox(label="select a Chart value",options=map_tranli1)
   

select4=co8.selectbox(label="chart",options=["Pie chart",'Scatter plots chart','Line chart',"Bar chart"])   

if states_map==True:
  map1(us_tr,year,qu,select2)
if districts_map==True:
  map2(us_tr,year,qu,select2)
if select1 != "select a state from below":
  map3(us_tr,year,qu,select1,select2,select3)

st.subheader(":violet[Phonepe pulse Facts]")

questli=["select a Fact from below","What are the Total transaction amount, Average transaction amount, and Total transaction count?",
         "What are the Total Registered PhonePe users, Total App open ?",
         "What are the top ten transaction amount districts?","What are the top ten districts by average transaction amount?",
         "What are the top ten transaction counts by district?","What are the top ten transaction amount pincode ?",
         "What are the top ten pincode by average transaction amount?","What are the top ten transaction counts by pincode ?",
         "What are the top ten districts by registered users?","What are the top ten pincode by registered users?",
         "What are the top ten transaction amount State?","What are the top ten State by average transaction amount?",
         "What are the top ten transaction counts by State?","What are the different categories of transactions by amount?",
         "What are the different categories of transactions by count?",      

         ]
select5=st.selectbox(label="select a Question",options=questli)
   
question(select5,year,qu,select4)
