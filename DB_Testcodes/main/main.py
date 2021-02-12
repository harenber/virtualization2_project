# In this script we would be creating a db if it doesnt exit and inserting the values the user inputs through front end into the DB.
import numpy as np
import sqlite3
import pandas as pd

connect_db=sqlite3.connect("Solver_data.db")
post=connect_db.cursor()
try:
    post.execute('''CREATE TABLE IF NOT EXISTS Input(
    Id Float Primary key,
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




##...................................................................................................................................................##
##--------------------solver-------------------------------------------##
##--------------------solver-------------------------------------------##
def f(t,y):
    yp = np.empty((18,))    #lazy init
    yp[0:9] = y[9:18] 
    #-------------- Calculating the forces
    yp[9:12] = -m[1]* (y[0:3]-y[3:6]) / np.linalg.norm(y[0:3]-y[3:6])**3 - m[2] * (y[0:3]-y[6:9]) / np.linalg.norm(y[0:3]-y[6:9]) ** 3
    yp[12:15] = -m[0]* (y[3:6]-y[0:3]) / np.linalg.norm(y[3:6]-y[0:3])**3 - m[2] * (y[3:6]-y[6:9]) / np.linalg.norm(y[3:6]-y[6:9]) ** 3
    yp[15:18] = -m[0]* (y[6:9]-y[0:3]) / np.linalg.norm(y[6:9]-y[0:3])**3 - m[1] * (y[6:9]-y[3:6]) / np.linalg.norm(y[6:9]-y[3:6]) ** 3
    return yp

def ODE45(f, tspan, h0, e, y, s):
    # h: Step Size Array, init by user
    # y: Solution array of arrays, init by user
    # s: Safety Factor
    # e: Maximum Error
    t = np.array([tspan[0]], dtype=float)
    h = np.array([h0], dtype=float)
    y = np.array([y0], dtype=float)
    i = 0
    #----------------------Implementing RK4 and RK5
    while t[-1] < tspan[1]:
        k1, k2, k3, k4, k5, k6, y5, y6 = (np.empty((18,)) for _ in range(8))
        k1 = h[i] * f(t[i], y[i])
        k2 = h[i] * f(t[i] + h[i] * 2/9, y[i] + k1 * 2/9)
        k3 = h[i] * f(t[i] + h[i] * 1/3, y[i] + k1 / 12 + k2 / 4)
        k4 = h[i] * f(t[i] + h[i] * 3/4, y[i] + k1 * 69/128 - k2 * 243/128 + k3 * 135/64)
        k5 = h[i] * f(t[i] + h[i], y[i] - k1 * 17/12 + k2 * 27/4 - k3 * 27/5 + k4 * 16/15)
        k6 = h[i] * f(t[i] + h[i] * 5/6, y[i] + k1 * 65/432 - k2 * 5/16 + k3 * 13/16 + k4 * 4/27 + k5 * 5/144)
        y5 = y[i] + k1 / 9 + k3 * 9/20 + k4 * 16/45 + k5 / 12
        y6 = y[i] + k1 * 47/450 + k3 * 12/25 + k4 * 32/225 + k5 /30 + k6 * 6/25
        
        #--------------------------Adapting step size
        delta = (y6 - y5)/y6
        delta[np.isnan(delta)] = 0
        delta = np.max(np.abs(delta))       #    Relative error with respect to RK5
        hh =  h[i] * s * (e/delta)**0.2
        if delta > e:
            h[i] = hh
            continue
        h = np.append(h, hh)
        t = np.append(t, t[i] + h[i])
        y = np.vstack([y, y5])
        i = i + 1
    return y, h

#--------------------------Inputs
Id=42.42
#post.execute(''' Select * from Input where id= (SELECT * from sqlite_sequence where name ='Input')''')
df = pd.read_sql_query('''Select * from Input  where Id= ?''', connect_db,params=(Id,))

print(df)
tspan = [df.loc[0,"t1"], df.loc[0,"t2"]]
m = [df.loc[0,"m1"], df.loc[0,"m2"], df.loc[0,"m3"]]
h0 = df.loc[0,"h"]
y0=[df.loc[0,"x1"],df.loc[0,"y1"],df.loc[0,"z1"],df.loc[0,"x2"],df.loc[0,"y2"],df.loc[0,"z2"],df.loc[0,"x3"],df.loc[0,"y3"],df.loc[0,"z3"],df.loc[0,"vx1"],df.loc[0,"vy1"],df.loc[0,"vz1"],df.loc[0,"vx2"],df.loc[0,"vy2"],df.loc[0,"vz2"],df.loc[0,"vx3"],df.loc[0,"vy3"],df.loc[0,"vz3"]]
e = df.loc[0,"e"] # Has to be greater than first step delta (huh??)
s = df.loc[0,"s"]
y, h = ODE45(f, tspan, h0, e, y0, s) # modifies t, y, h



##----------------------------------------solver-end----------------------##

#inserting data to DB:

new_Id=str(Id).replace(".","_")
#post.execute('''Drop table IF EXISTS Output'''+new_Id)

try:
    post.execute(''' CREATE TABLE Output'''+ new_Id+'''(
    y1 double precision,
    y2 double precision,
    y3 double precision,
    y4 double precision,
    y5 double precision,
    y6 double precision,
    y7 double precision,
    y8 double precision,
    y9 double precision,
    y10 double precision,
    y11 double precision,
    y12 double precision,
    y13 double precision,
    y14 double precision,
    y15 double precision,
    y16 double precision,
    y17 double precision,
    y18 double precision
)''')
except sqlite3.OperationalError as e:
    print('sqlite error:', e.args[0])  # table already exists
else:
    print('table created')
    
#inserting Data into DB:        
try:
    for row in y:
        post.execute('''INSERT INTO Output'''+new_Id+'''(y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12,y13,y14,y15,y16,y17,y18) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',row)
except Exception as E:
    print('Error : ', E)
else:
    connect_db.commit()
    print('Data inserted')
#..............................................................................................................................................
connect_db.commit()
connect_db.close()
