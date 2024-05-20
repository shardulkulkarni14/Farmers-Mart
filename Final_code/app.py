import pyrebase
from firebase import firebase
from scapy.all import *
import random
import requests
import json
from instamojo_wrapper import Instamojo
config = {
	"apiKey": "AIzaSyAYeR8EbGT8o0mkcqpiL6s7PfcCrT2_naA",
    "authDomain": "sih2020-59356.firebaseapp.com",
    "databaseURL": "https://sih2020-59356.firebaseio.com",
    "projectId": "sih2020-59356",
    "storageBucket": "sih2020-59356.appspot.com",
    "messagingSenderId": "40198112981",
    "appId": "1:40198112981:web:8768d7a572404c1b7c845c",
    "measurementId": "G-2NW3KXNK42",
    "serviceAccount": "serviceAccount.json"
}



FBConn = firebase.FirebaseApplication('https://sih2020-59356.firebaseio.com')

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
from flask import *
import pandas as pd
app = Flask(__name__)
app.secret_key = "hello"
db = firebase.database()
@app.route('/', methods=["GET", "POST"])
def index():

	return render_template('index.html')

@app.route('/custregister',methods=["GET", "POST"])
def customer():
	if request.method == 'POST':
		if request.form['submit'] == 'submit':
			print("hello")
			names = request.form['names']
			number = request.form['number']
			email = request.form['email']
			address = request.form['address']
			password = request.form['pass']
			city = request.form['city']
			state = request.form['state']
			country = request.form['country']
			customer = "customer"
			data_to_upload = {
				'Name': names,
				'Phone Number': number,
				'Email id': email,
				'Address' : address,
				'Password': password,
				'type':customer,
				'Country' : country,
				'State' : state,
				'City' : city,
			}
			print(data_to_upload)
			result = FBConn.post('/user_data/', data_to_upload)
			print(result)
	return render_template('cust-index.html')

@app.route('/farmer',  methods= ["GET", "POST"])
def farm():
	if request.method == 'POST':
		if request.form['submit'] == 'submit':
			Fname = request.form['Fname']
			Lname = request.form['Lname']
			Soil_type = request.form.get('soiltype')
			Country = request.form['Country']
			State = request.form['State']
			City = request.form['City']
			Pincode = request.form['Pincode']
			Pnumber = request.form['Pnumber']
			Age = request.form['Age']
			gender = request.form.get('gender')
			Addfarm = request.form['Addfarm']
			Landholding = request.form['Landholding']
			Area = request.form.get('Area')
			Passw = request.form['Passw']
			agriculture = request.form.getlist('agri')
			animal = request.form.getlist('animal')
			flowers = request.form.getlist('flowers')
			spices = request.form.getlist('spices')
			fruits = request.form.getlist('fruits')
			farmer = "farmer"
			data_to_upload = {
				'Name' : Fname+" "+Lname,
				'Country' : Country,
				'State' : State,
				'City' : City,
				'Pincode' : Pincode,
				'Phone Number' : Pnumber,
				'Age' : Age,
				'Gender' : gender,
				'Addfarm' : Addfarm,
				'Landholding': Landholding,
				'Area' : Area,
				'Password' : Passw,
				'crop' : agriculture,
				'animal' : animal,
				'fruits' : fruits,
				'flowers' : flowers,
				'spices' : spices,
				'type':farmer,
				'soil':Soil_type,
				'score':'4'
			}
			total_score = []
			for i in agriculture:
				total_score.append(i)
			for j in animal:
				total_score.append(j)
			for m in flowers:
				total_score.append(m)
			for k in fruits:
				total_score.append(k)
			for l in spices:
				total_score.append(l)

			print(total_score)
			score_value=[]
			for i in range(len(total_score)):
				score_value.append('3')

			# score_crop = dict(zip(total_score,score_value))
			df = pd.DataFrame(list(zip(total_score,score_value)), 
               columns =['crop', 'score'])
			print(df)
			crop_soil = FBConn.get('/crop_soil/',None)
			cost_crop = FBConn.get('/crop_cost/',None)
			cost=""
			for ind in df.index:
				

				for i in crop_soil:
					crops = crop_soil[i]['Crop']
					soils = crop_soil[i]['Soil']
					for i in cost_crop:
						if df.iloc[ind]['crop'] == cost_crop[i]['Crop Name']:
							cost = cost_crop[i]['Cost']
					if crops == df.iloc[ind]['crop']:
						if Soil_type == soils:
							score_update = int(df.iloc[ind]['score'])
							df.at[ind,'score']= '4'
							

				data_to = {
					'Crop' : df.iloc[ind]['crop'],
					'Score' : df.iloc[ind]['score'],
					'Cost'  : cost
				}
				print(data_to)
				total_sc = FBConn.post('/'+Pnumber+'/', data_to)
			result = FBConn.post('/user_data/', data_to_upload)
			print(result)
	return render_template('reg-farm-index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
	result = FBConn.get('/user_data/',None)
	print(result)
	if request.method == 'POST':
		if request.form['submit'] == 'submit':
			email1 = request.form['email']
			session["user"] = email1
			password1 = request.form['pass']
			# cust = request.form.get('cust')
			print("hello")
			for i in result:
				a = result[i]['Phone Number']
				b = result[i]['Password']
				if email1 == a and password1 == result[i]['Password']:
					c = result[i]['type']
					if c == "farmer":
						return redirect(url_for('farmerfeed'))
					elif c == "customer":
						return redirect(url_for('customerfeed'))
	return render_template('login-index.html')

@app.route('/user', methods=["GET", "POST"])
def user():
	result = FBConn.get('/user_data/',None)
	user_name =""
	if "user" in session:
		email_id = session["user"]
		for i in result:
			a = result[i]['Phone Number']
			if a ==email_id:
				name = result[i]['Name']
				address = result[i]['Address']
		print(email_id)

	transaction_data = FBConn.get('/transaction_data/',None)
	for i in transaction_data:
			if transaction_data[i]['Customer name'] == name:
				packing_id = transaction_data[i]['Packing-ID'] 
				print(packing_id,email_id)
				temp = random.randint(25,35)
				from datetime import datetime

				now = datetime.now()

				current_time = now.strftime("%H%M%S")
				time= int(current_time)
	return render_template('user-data.html',packing_id=str(packing_id),email_id=str(7875),temp=str(temp),time=str(time))

@app.route('/setpage', methods = ['GET', 'POST'])
def setpage():
	return render_template('setpage.html')


@app.route('/getpage',methods=['GET','POST'])
def getpage():
	return render_template('getpage.html')

@app.route('/farmerprofile',methods=['GET','POST'])
def farmprofile():
	date_rice=[]
	crop_d = "Rose"
	price_rice=[]
	graph_crop = FBConn.get('/graph_crop/',None)
	name_crop = []
	datee = []
	sold = []
	website = []

	for i in graph_crop:
		if graph_crop[i]['Crop_name'] ==crop_d:
			name_crop.append(graph_crop[i]['Crop_name'])
			datee.append(graph_crop[i]['Date'])
			sold.append(int(graph_crop[i]['Sold']))
			website.append(int(graph_crop[i]['Website_price']))
	result = FBConn.get('/user_data/',None)
	cost_crop = FBConn.get('/crop_cost/',None)
	user_name =""
	name =""
	address=""
	phone=""
	if "user" in session:
		email_id = session["user"]
		print(email_id)
		for i in result:
			a = result[i]['Phone Number']
			if a ==email_id:
				name = result[i]['Name']
				address = result[i]['Addfarm']
		phone = "+91 "+email_id
		
	data_pic = FBConn.get('/'+email_id+'/',None)
	crop_score=[]
	crop_produced=[]
	costt=[]

	data_user = FBConn.get('/user_data/',None)
	transaction_data = FBConn.get('/transaction_data/',None)
	crop_cost = FBConn.get('/crop_cost/',None)
	data_review = FBConn.get('/review_data/',None)

	for i,a in data_review.items():
		if a['flag'] == 1:
			if 	name == a['Farmer name']:
				purchased_crop = a['Crop_Name']
				rating = a['Rating']
				for j in crop_cost:
					if purchased_crop == crop_cost[j]['Crop Name']:
						price_crop = crop_cost[j]['Cost']
						dataa = FBConn.get('/'+email_id+'/',None)
						
						for y,k in dataa.items():
							if purchased_crop == k['Crop']:
								price_ratio = float(k['Cost'])/float(price_crop)
								score_ratio = float(rating)/5
								old_score = float(k['Score'])/5
								total = price_ratio+score_ratio+old_score
								tt = (total*5.0)/3.0
								tt1 = round(tt,1)
								print(tt1) 
								datta = {
								'Score':tt1
								}
								
								db.child('/'+email_id+'/').child(y).update(datta)
				daa={
				'flag':2
				}
				db.child('/review_data/').child(i).update(daa)			

	for i in data_pic:
		crop_produced.append(data_pic[i]['Crop'])
		
	crop_produced.sort()
	for i in range(len(crop_produced)):
		for j in data_pic: 
			if crop_produced[i] == data_pic[j]['Crop']:
				crop_score.append(data_pic[j]['Score'])
				costt.append(data_pic[j]['Cost'])
	storage = firebase.storage()
	files = storage.list_files()
	print(files)
	img_list=[]
	f=[]
	for file in files:
		img_list.append(storage.child(file.name).get_url(None))
	
	for i in range(len(img_list)):
		a = img_list[i]
		b = a.split("%2F")
		c = b[1]
		d = c.split(".jpg") 
		
		for j in range(len(crop_produced)):
			e = crop_produced[j]
			if d[0] == e.lower():
				print(d[0])
				f.append(a)
	
	if request.method == 'POST':
		if request.form['submit'] == 'submit':
			crop_predict = request.form.get('cropname')
			crop_predicts = str(crop_predict)
			
			rice = FBConn.get('/'+crop_predicts+'/',None)
			for i in rice:
				date_rice.append(rice[i]['Date'])
				price_rice.append(rice[i]['Price'])
		elif request.form['submit'] == 'update':
			return redirect(url_for('updateorder'))
		elif request.form['submit'] == 'upload_lease':
			Area = request.form.get('dist')
			Land_Location = request.form['land_location']
			Land_area = request.form['area_land']
			workers = request.form['workers']
			Soil = request.form.get('type_soil')
			crop = request.form.getlist('vehicle1')
			experience = request.form['experience']
			data = {
			'Farmer Name':name,
			'Land location':Land_Location,
			'Land area':Land_area+" "+Area,
			'Workers':workers,
			'Type_Soil':Soil,
			'Crop':crop,
			'Experience':experience
			}
			FBConn.post('/lease/', data)
		elif request.form['submit'] =='crop_price':
			print("HE::P")
			name_crop = []
			datee = []
			sold = []
			website = []
			crop_d = request.form.get('cropnames')	

			graph_crop = FBConn.get('/graph_crop/',None)
			for i in graph_crop:
				print(crop_d,graph_crop[i]['Crop_name'])
				if graph_crop[i]['Crop_name'] ==crop_d:

					name_crop.append(graph_crop[i]['Crop_name'])
					datee.append(graph_crop[i]['Date'])
					sold.append(int(graph_crop[i]['Sold']))
					website.append(int(graph_crop[i]['Website_price']))
					print(name_crop)
	else: 
		rice = FBConn.get('/rice/',None)
		for i in rice:
			date_rice.append(rice[i]['Date'])
			price_rice.append(rice[i]['Price'])

	

	
	return render_template('fprofile.html',crop_d=crop_d,name=name,address=address,phone=phone,date_rice=date_rice,price_rice=price_rice,ricee=zip(date_rice,price_rice),total_score=zip(crop_produced,crop_score,f,costt),graph_crop=zip(name_crop,datee,sold,website))


@app.route('/farmerfeed',methods=['GET','POST'])
def farmerfeed():
	return render_template('ffeed.html')


@app.route('/customerprofile',methods=['GET','POST'])
def customerprofile():
	result = FBConn.get('/user_data/',None)
	user_name =""
	name =""
	address=""
	phone=""
	if "user" in session:
		email_id = session["user"]
		print(email_id)
		for i in result:
			a = result[i]['Phone Number']
			if a ==email_id:
				name = result[i]['Name']
				address = result[i]['Address']
		phone = "+91 "+a
	return render_template('cprofile.html',name=name,address=address,phone=phone)


@app.route('/cfeed',methods=['GET','POST'])
def customerfeed():
	result = FBConn.get('/crop_score/',None)
	print(result)
	farmer_name=[]
	farmer_crop=[]
	farmer_score=[]
	data_crop=[]
	user_data = FBConn.get('/user_data/',None)
	email_id=""
	crop_name=[]
	price=[]
	phone_number=[]
	if "user" in session:
		email_id = session["user"]
		print(email_id)
	for i in user_data:
		if email_id == user_data[i]['Phone Number']:	
			name = user_data[i]['Name']
			emails = user_data[i]['Email id']
	for j in user_data:
		phones = user_data[j]['Phone Number']
		types = user_data[j]['type']
		if types == "farmer":

			phone_number.append(phones)
			

	for i in range(len(phone_number)):
		ph = FBConn.get('/'+phone_number[i]+'/',None)
		for j in ph:
			ph_crop = ph[j]['Crop']
			costss = ph[j]['Cost']
			
			for k in result:
				
				if ph_crop == result[k]['Crop Name']:
					
					farmer_name.append(result[k]['Name'])
					farmer_crop.append(result[k]['Crop Name'])
					farmer_score.append(result[k]['Score'])
					price.append(costss)
					
	# for i in result:
	# 	# for j in phone_number:
	# 	# 	phone_data = phone_number[j]
			
	# 	farmer_name.append(result[i]['Name'])
	# 	farmer_crop.append(result[i]['Crop Name'])
	# 	farmer_score.append(result[i]['Score'])
	# print(farmer_score)
	total_scores=list(zip(farmer_name,farmer_crop,farmer_score,price))
	df = pd.DataFrame(total_scores, columns = ['Famer Name', 'Farmer crop','Farmer_score','Price'])
	print(pd.to_numeric(df['Farmer_score']))
	data = pd.read_csv('Score.csv')
	pd.to_numeric(data['Farmer_score'])
	a =  data.iloc[data.groupby(['Farmer crop'], sort=False)['Farmer_score'].idxmax()][['Farmer crop', 'Famer Name', 'Farmer_score','Price']]
	b=a.values.tolist()
	dataaa=[]
	if request.method == 'POST':
		if request.form['Buy Now'] == 'Buy Now':
			farmername = request.form['farmername']
			cropname = request.form['cropname']
			cropscore = request.form['cropscore']
			price = request.form['price']
			from instamojo_wrapper import Instamojo
			data_to_upload = {
				'Customer name' : name,
				'Farmer Name' : farmername,
				'Crop Purchased' : cropname,
				'Crop_Score' : cropscore,
				'Price' : price,
				'Packing-ID':"FM"+str(random.randint(10000,1000000))
				}
			API_KEY = '3200b0a8745e5566455b40363dba2aa6'
			AUTH_TOKEN = '4e327bece751601e5a0e5b3d63a15990'
			api = Instamojo(api_key=API_KEY,auth_token=AUTH_TOKEN)
			response = api.payment_request_create(
				amount=price,
				buyer_name=name,
				purpose='Buying the '+cropname,
				send_email=True,
				email=emails,
				phone=email_id,
				redirect_url="http://www.example.com/handle_redirect.py")
			print(response['payment_request']['longurl'])
			result = FBConn.post('/transaction_data/', data_to_upload)
			return redirect(response['payment_request']['longurl'])
		elif request.form['Buy Now'] == 'msg':
			def send_sms(number, message):
				url = 'https://www.fast2sms.com/dev/bulk'
				params = {
				'authorization': 'zDXSyjGALP4KpY8OUvWunIx76rVsaw2dfcCNlEkTJRhomF31HeEcSoO92nf6i4LDFPTe1lkrRGNqCbuU',
				'sender_id': 'SMSIND',
				'message': message,
				'language': 'english',
				'route': 'p',
				'numbers': number
				}
				response = requests.get(url, params=params)
				dic = response.json()
				print(dic)
				return dic.get('return')  # comes back with a json object with return id 

				
			crop_name = request.form.get('cropname')
			quantity = request.form['quantity']
			place = request.form['place']
			unit = request.form.get('unit')
			messages = "Hello farmers Customer named "+name+" wanted "+crop_name+" with quantity "+quantity+"/"+unit+" in city "+place
			print(messages)
			send_sms("9766318407",messages)
		elif request.form['Buy Now'] == 'rcropname':
			rcrop = request.form.get('rcropnames')
			data_crop=[]
			user_dataa = FBConn.get('/user_data/', None)
			phone_number=[]
			names=[]
			for i in user_dataa:
				if user_dataa[i]['type'] == "farmer":
					phone_number.append(user_dataa[i]['Phone Number'])
					names.append(user_dataa[i]['Name'])
			data_zip = zip(names,phone_number)
			print(data_zip)
			dataaa=[]

			for i,y in data_zip:
				ph = FBConn.get('/'+y+'/', None)
				for j in ph:
					print(rcrop,ph[j]['Crop'])
					if rcrop == ph[j]['Crop']:

						data_crop.append(ph[j])
						dataaa.append(i)
			print(data_crop)
			print(zip(data_crop,dataaa))
	return render_template('cfeed.html',total_score=b,data_crops=zip(data_crop,dataaa))

@app.route('/cart',methods=['GET','POST'])
def cart():
	user_data = FBConn.get('/user_data/',None)
	email_id=""
	crop_name=[]
	price=[]
	name_user = ""

	if "user" in session:
		email_id = session["user"]
		print(email_id)
	for i in user_data:
		if email_id == user_data[i]['Phone Number']:
			name_user = user_data[i]['Name']
			address = user_data[i]['Address']
			amount = 600
			promocode = "076439"
	return render_template('shopCart.html',name_user=name_user,address=address,amount=amount,promocode=promocode)

@app.route('/updateorder',methods=['GET','POST'])
def updateorder():
	user_data = FBConn.get('/user_data/',None)
	email_id=""
	crop_name=[]
	price=[]
	if "user" in session:
		email_id = session["user"]
		print(email_id)
	data_pic = FBConn.get('/'+email_id+'/',None)
	for i in data_pic:
		crop_name.append(data_pic[i]['Crop'])
		price.append(data_pic[i]['Cost'])
	db = firebase.database()
	if request.method == 'POST':
		if request.form['submit'] == 'submit':
			print("hello")
			price = request.form['price']
			cropname = request.form['crop_name']
			print(cropname)
			for x,y in data_pic.items():
				print(y['Crop'])
				if cropname == y['Crop']:
					print(x)
					data = {
						'Crop':cropname,
						'Cost':price
					}
					print(x)
					db.child('/'+email_id+'/').child(x).update(data)
			return redirect(url_for('updateorder'))

	return render_template('update_order.html',data_crop=zip(crop_name,price))


@app.route('/track',methods=['GET','POST'])
def track():
	user_data = FBConn.get('/user_data/',None)
	email_id=""
	crop_name=[]
	price=[]
	if "user" in session:
		email_id = session["user"]
		print(email_id)
	for i in user_data:
		if email_id == user_data[i]['Phone Number']:
			cust_name = user_data[i]['Name']
	transaction_data = FBConn.get('/transaction_data/',None)
	farmer_name=[]
	price=[]
	crop_name=[]
	packing_id=[]
	print(email_id)
	temp = random.randint(25,35)
	from datetime import datetime
	data_long = FBConn.get('/data_long/',None)
	data_lo = []
	data_longg = ""
	for i in data_long:
		data_lo.append(data_long[i]['City']+","+str(data_long[i]['Latitude']) +","+str(data_long[i]['Longitude']))
		print(data_lo)
	data_longg = random.choice(data_lo)
	print(data_longg)
	now = datetime.now()

	current_time = now.strftime("%H%M%S")
	time= int(current_time)
	for i in transaction_data:
		
		if cust_name == transaction_data[i]['Customer name']:
			farmer_name.append(transaction_data[i]['Farmer Name'])
			price.append(transaction_data[i]['Price'])
			packing_id.append(transaction_data[i]['Packing-ID'])
			crop_name.append(transaction_data[i]['Crop Purchased'])
			print("hello")
	# if request.method == 'POST':
	# 	if request.form['submit'] == 'submit':
	# 		print("hello")
			# return redirect(url_for('setpage'))
	return render_template('track.html',total_details=zip(farmer_name,price,crop_name,packing_id),email_id=email_id,temp=temp,time=time,data_longg=data_longg)

@app.route('/review',methods=['GET','POST'])
def review():
	user_data = FBConn.get('/user_data/',None)
	email_id=""
	crop_name=[]
	price=[]
	if "user" in session:
		email_id = session["user"]
		print(email_id)
	for i in user_data:
		if email_id == user_data[i]['Phone Number']:
			cust_name = user_data[i]['Name']
	transaction_data = FBConn.get('/transaction_data/',None)
	farmer_name=[]
	price=[]
	crop_name=[]
	packing_id=[]
	print(email_id)
	for i in transaction_data:
		
		if cust_name == transaction_data[i]['Customer name']:
			farmer_name.append(transaction_data[i]['Farmer Name'])
			crop_name.append(transaction_data[i]['Crop Purchased'])
			print("hello")
	if request.method == 'POST':
		if request.form['submit'] == 'submit':
			farmername = request.form['farmers_name']
			cropname = request.form['crop']
			rating = request.form['rating']
			review = request.form['review']
			data_to_upload = {
				'Farmer name': farmername,
				'Customer_name': cust_name,
				'Crop_Name': cropname,
				'Rating' : rating,
				'Review': review,
				'flag':1
			}
			print(data_to_upload)
			result = FBConn.post('/review_data/', data_to_upload)
	return render_template('review.html',total_details=zip(farmer_name,crop_name))

@app.route('/lease',methods=['GET','POST'])
def lease():
	lease = FBConn.get('/lease/',None)
	crop_data = []
	Farmer_name=[]
	Land_area=[]
	Land_Location=[]
	type_soil=[]
	workers=[]
	experience=[]
	a= ""
	for i in lease:
		Farmer_name.append(lease[i]['Farmer Name'])
		Land_area.append(lease[i]['Land area'])
		Land_Location.append(lease[i]['Land location'])
		type_soil.append(lease[i]['Type_Soil'])
		workers.append(lease[i]['Workers'])
		experience.append(lease[i]['Experience'])
		crop_data.append(lease[i]['Crop'])
		# for j in range(len(crop_data)):
		# 	for k in range(len(crop_data)):
		# 		print(crop_data[j][k])
		# 		a = a + crop_data[j][k]+","
		# 		print(a)
	print(Farmer_name,Land_area,Land_Location,type_soil,workers,experience)
	return render_template('lease.html',lease_datas=zip(Farmer_name,Land_area,Land_Location,type_soil,workers,experience,crop_data))


@app.route('/market',methods=['GET','POST'])
def market():
	return render_template('market.html')

@app.route('/shop',methods=['GET','POST'])
def shop():
	return render_template('shop.html')
if __name__ == '__main__':
	app.run(debug=True)