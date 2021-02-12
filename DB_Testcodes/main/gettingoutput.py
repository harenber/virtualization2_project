import sqlite3
import pandas as pd
import json


connect_db=sqlite3.connect("Solver_data.db")
post=connect_db.cursor()

Id=42.42
new_Id=str(Id).replace(".","_") 
#post.execute(''' Select * from Input where id= (SELECT * from sqlite_sequence where name ='Input')''')
df=pd.read_sql_query('''Select y1,y2,y3,y4,y5,y6,y7,y8,y9 from output'''+new_Id, connect_db)
b1=pd.read_sql_query('''Select y1,y2,y3 from output'''+new_Id, connect_db)
b2=pd.read_sql_query('''Select y4,y5,y6 from output'''+new_Id, connect_db)
b3=pd.read_sql_query('''Select y7,y8,y9 from output'''+new_Id, connect_db)

print(b1)
print(b2)
print(b3)


#data = {
            #"b1": {"x": b1x, "y": b1y, "z": b1z},
            #"b2": {"x": b2x, "y": b2y, "z": b2z},
            #"b3": {"x": b3x, "y": b3y, "z": b3z}
        #}
    
