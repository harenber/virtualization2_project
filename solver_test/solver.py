##--------------------solver-------------------------------------------##
import numpy as np
import sqlite3
import pandas as pd
import asyncio
import socket
import websockets





def f(t,y,m):
    yp = np.empty((18,))    #lazy init
    yp[0:9] = y[9:18] 
    #-------------- Calculating the forces
    yp[9:12] = -m[1]* (y[0:3]-y[3:6]) / np.linalg.norm(y[0:3]-y[3:6])**3 - m[2] * (y[0:3]-y[6:9]) / np.linalg.norm(y[0:3]-y[6:9]) ** 3
    yp[12:15] = -m[0]* (y[3:6]-y[0:3]) / np.linalg.norm(y[3:6]-y[0:3])**3 - m[2] * (y[3:6]-y[6:9]) / np.linalg.norm(y[3:6]-y[6:9]) ** 3
    yp[15:18] = -m[0]* (y[6:9]-y[0:3]) / np.linalg.norm(y[6:9]-y[0:3])**3 - m[1] * (y[6:9]-y[3:6]) / np.linalg.norm(y[6:9]-y[3:6]) ** 3
    return yp

def ODE45(f, tspan, h0, e, y0, s,m):
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
        k1 = h[i] * f(t[i], y[i],m)
        k2 = h[i] * f(t[i] + h[i] * 2/9, y[i] + k1 * 2/9,m)
        k3 = h[i] * f(t[i] + h[i] * 1/3, y[i] + k1 / 12 + k2 / 4,m)
        k4 = h[i] * f(t[i] + h[i] * 3/4, y[i] + k1 * 69/128 - k2 * 243/128 + k3 * 135/64,m)
        k5 = h[i] * f(t[i] + h[i], y[i] - k1 * 17/12 + k2 * 27/4 - k3 * 27/5 + k4 * 16/15,m)
        k6 = h[i] * f(t[i] + h[i] * 5/6, y[i] + k1 * 65/432 - k2 * 5/16 + k3 * 13/16 + k4 * 4/27 + k5 * 5/144,m)
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
connect_db=sqlite3.connect("Solver_data.db")
post=connect_db.cursor()





async def get_input_from_backend(websocket, path):
	#Id =  await websocket.recv()
	Id= await asyncio.wait_for(websocket.recv(), timeout=100.0)
	print(Id)
	



	#post.execute(''' Select * from Input where id= (SELECT * from sqlite_sequence where name ='Input')''')
	df = pd.read_sql_query('''Select * from Input  where Id= ?''', connect_db,params=(Id,))

	print(df)
	tspan = [df.loc[0,"t1"], df.loc[0,"t2"]]
	m = [df.loc[0,"m1"], df.loc[0,"m2"], df.loc[0,"m3"]]
	h0 = df.loc[0,"h"]
	y0=[df.loc[0,"x1"],df.loc[0,"y1"],df.loc[0,"z1"],df.loc[0,"x2"],df.loc[0,"y2"],df.loc[0,"z2"],df.loc[0,"x3"],df.loc[0,"y3"],df.loc[0,"z3"],df.loc[0,"vx1"],df.loc[0,"vy1"],df.loc[0,"vz1"],df.loc[0,"vx2"],df.loc[0,"vy2"],df.loc[0,"vz2"],df.loc[0,"vx3"],df.loc[0,"vy3"],df.loc[0,"vz3"]]
	e = df.loc[0,"e"] # Has to be greater than first step delta (huh??)
	s = df.loc[0,"s"]
	y, h = ODE45(f, tspan, h0, e, y0, s,m) # modifies t, y, h



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
	#connect_db.close()


HOST = socket.gethostbyname('solver')
PORT = 8002
start_server = websockets.serve(get_input_from_backend, HOST, PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()



