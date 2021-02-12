import sqlite3
import pandas as pd


connect_db=sqlite3.connect("Solver_data.db")
post=connect_db.cursor()

Id=42.42
new_Id=str(Id).replace(".","_") 
#post.execute(''' Select * from Input where id= (SELECT * from sqlite_sequence where name ='Input')''')
df = pd.read_sql_query('''Select * from output'''+new_Id, connect_db)
print(df)
