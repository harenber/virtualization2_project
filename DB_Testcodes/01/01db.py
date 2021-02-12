# In this script we would be creating a db if it doesnt exit and inserting the values the user inputs through front end into the DB.


import sqlite3

connect_db=sqlite3.connect("Solver_data.db")
post=connect_db.cursor()
try:
    post.execute('''CREATE TABLE IF NOT EXISTS Input(
    Id integer primary key,
    t1 int,
    t2 int,
    m1 float,
    m2 float,
    m3 float,
    x1 double precision,
    x2 double precision,
    x3 double precision,
    y1 double precision,
    y2 double precision,
    y3 double precision,
    z1 double precision,
    z2 double precision,
    z3 double precision,
    vx1 double precision,
    vx2 double precision,
    vx3 double precision,
    vy1 double precision,
    vy2 double precision,
    vy3 double precision,
    vz1 double precision,
    vz2 double precision,
    vz3 double precision,
    h double precision,
    e double precision,
    s double precision
)''')
except sqlite3.OperationalError as e:
    print('sqlite error:', e.args[0])  # table already exists
else:
    print('table created')
    
##Add values got from user here
t1 =0
t2 =30
m1 =5
m2 =3
m3 =4
x1 =1
x2 =1
x3 =-2
y1 =-1
y2 =3
y3 =-1
z1 =0
z2 =0
z3 =0
vx1 =0
vx2 =0
vx3 =0
vy1 =0
vy2 =0
vy3 =0
vz1 =0
vz2 =0
vz3 =0
h =1
e =1e-9
s =0.9
Id=42.42

##insert these values into the DB

data_tuple=(Id,t1,t2,m1,m2,m3,x1,x2,x3,y1,y2,y3,z1,z2,z3,vx1,vx2,vx3,vy1,vy2,vy3,vz1,vz2,vz3,h,e,s)

try:
    post.execute('''INSERT INTO Input(Id,t1,t2,m1,m2,m3,x1,x2,x3,y1,y2,y3,z1,z2,z3,vx1,vx2,vx3,vy1,vy2,vy3,vz1,vz2,vz3,h,e,s) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',data_tuple)
except Exception as E:
    print('Error : ', E)
else:
    connect_db.commit()
    print('Data inserted')
    
    
# To check if the values have been inserted correctly.

#post.execute('''select * from Input''')
#print(post.fetchall())

connect_db.commit()
connect_db.close()
