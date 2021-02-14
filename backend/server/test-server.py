import asyncio
import websockets
import socket
import json
import math
import sqlite3
import time
import pandas as pd

async def save_to_db(data):
	connect_db=sqlite3.connect("Solver_data.db")
	post=connect_db.cursor()
	try:
		post.execute('''CREATE TABLE IF NOT EXISTS Input(
		Id Float Primary key,		t1 int,		t2 int,
		m1 float,		m2 float,		m3 float,
		x1 double precision,		x2 double precision,		x3 double precision,
		y1 double precision,		y2 double precision,		y3 double precision,
		z1 double precision,		z2 double precision,		z3 double precision,
		vx1 double precision,		vx2 double precision,		vx3 double precision,
		vy1 double precision,		vy2 double precision,		vy3 double precision,
		vz1 double precision,		vz2 double precision,		vz3 double precision,
		h double precision,		e double precision,		s double precision
	)''')
	except sqlite3.OperationalError as e:
		print('sqlite error:', e.args[0])  # table already exists
	else:
		print('table created')

	t1, t2 = data['time'][0], data['time'][1]
	m1, m2, m3 = data['b1']['mass'], data['b2']['mass'], data['b3']['mass']
	x1, x2, x3 = data['b1']['position'][0], data['b2']['position'][0], data['b3']['position'][0]
	y1, y2, y3 = data['b1']['position'][1], data['b2']['position'][1], data['b3']['position'][1]
	z1, z2, z3 = data['b1']['position'][2], data['b2']['position'][2], data['b3']['position'][2]
	vx1, vx2, vx3 = data['b1']['velocity'][0], data['b2']['velocity'][0], data['b3']['velocity'][0]
	vy1, vy2, vy3 = data['b1']['velocity'][1], data['b2']['velocity'][1], data['b3']['velocity'][1]
	vz1, vz2, vz3 = data['b1']['velocity'][2], data['b2']['velocity'][2], data['b3']['velocity'][2]
	Id, e, h ,s = time.time(), data['epsilon'], 0.1, 0.9

	#print(data)


	data_tuple=(Id,t1,t2,m1,m2,m3,x1,x2,x3,y1,y2,y3,z1,z2,z3,vx1,vx2,vx3,vy1,vy2,vy3,vz1,vz2,vz3,h,e,s)

	try:
		post.execute('''INSERT INTO Input(Id,t1,t2,m1,m2,m3,x1,x2,x3,y1,y2,y3,z1,z2,z3,vx1,vx2,vx3,vy1,vy2,vy3,vz1,vz2,vz3,h,e,s) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',data_tuple)
	except Exception as E:
		print('Error : ', E)
	else:
		connect_db.commit()
		print('Data inserted')
		return Id




async def send_id_to_solver(Id):
	HOST = socket.gethostbyname('solver')
	PORT = 8002  
	uri = "ws://"+str(HOST)+":"+str(PORT)
	async with websockets.connect(uri) as websocket:
		await websocket.send(Id)


async def backend_service(websocket, path):
	initial = await websocket.recv()

	data = json.loads(initial)
	#print(data)
	Id=await save_to_db(data)
	await asyncio.sleep(1/60)
	await asyncio.sleep(1/60)
	await send_id_to_solver(str(Id))



	connect_db=sqlite3.connect("Solver_data.db")
	post=connect_db.cursor()
	
	
	new_Id=str(Id).replace(".","_") 
	#post.execute(''' Select * from Input where id= (SELECT * from sqlite_sequence where name ='Input')''')
	df=pd.read_sql_query('''Select y1,y2,y3,y4,y5,y6,y7,y8,y9 from output'''+new_Id, connect_db)
	b1=pd.read_sql_query('''Select y1,y2,y3 from output'''+new_Id, connect_db)
	b2=pd.read_sql_query('''Select y4,y5,y6 from output'''+new_Id, connect_db)
	b3=pd.read_sql_query('''Select y7,y8,y9 from output'''+new_Id, connect_db)


	b1=json.loads(b1.to_json(orient="split"))
	b2=json.loads(b2.to_json(orient="split"))
	b3=json.loads(b3.to_json(orient="split"))
	
	print(b1['data'][0])
	
	for i in range(0,len(b1['data'])):
		data = {
		        "b1": {"x": b1['data'][i][0], "y": b1['data'][i][1], "z": b1['data'][i][2]},
		        "b2": {"x": b2['data'][i][0], "y": b2['data'][i][1], "z": b2['data'][i][2]},
		        "b3": {"x": b3['data'][i][0], "y": b3['data'][i][1], "z": b3['data'][i][2]}
		    }
		await websocket.send(json.dumps(data))
		await asyncio.sleep(1/30)



HOST = socket.gethostbyname('project_server')
PORT = 8001
print(HOST)
#print(PORT)

start_server = websockets.serve(backend_service, HOST, PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
