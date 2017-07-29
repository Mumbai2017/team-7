from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from twilio.rest import TwilioRestClient
from models import Sakhi, Customer, Order, Distance
import re
import urllib2
import json
# Create your views here.

def hello_world(request):
	user_all = User.objects.all()
	if request.method == 'GET':
		print 'hello'
		sms_body = request.GET.get('Body')
		print sms_body
	#return HttpResponse('HI!')

def sms(request):
	if request.method == 'GET':
		print 'hello'
		sms_body  = request.GET.get('Body')
		print sms_body

def register_sakhi(request):
	if request.method == 'POST':
		name =  request.POST.get('name')
		password = request.POST.get('password')
		username = request.POST.get('email')
		phone = request.POST.get('mobile')
		user = User.objects.create_user(username=username,password=password,first_name=name)
		user.set_password(password)
		user.save()
		login(request,user)
		sakhi = Sakhi.objects.create(user=user,phone=phone)
		sakhi.save()
		redirect_url = '/getlocation/' + str(1) + '/' + str(sakhi.id) + '/'
		return HttpResponseRedirect(redirect_url)
	else:
		return render(request,'sakhi_register.html')
def register_user(request):
	if request.method == 'POST':
		name =  request.POST.get('name')
		password = request.POST.get('password')
		username = request.POST.get('email')
		phone = request.POST.get('mobile')	 
		user = User.objects.create_user(username=username,password=password,first_name=name)
		user.set_password(password)
		user.save()
		login(request,user)
		customer = Customer.objects.create(user=user,phone=phone)
		customer.save()
		redirect_url = '/getlocation/' + str(0) + '/' + str(customer.id) + '/'
		return HttpResponseRedirect(redirect_url)
	else:
		return render(request,'register_user.html')
def get_location(request,sakhi_user,id):
	if request.method == 'POST':
		if sakhi_user == str(1):
			lat = request.POST.get('glat')
			lng = request.POST.get('glng')
			sakhi = Sakhi.objects.get(id=id)
			sakhi.lat = lat
			sakhi.lng = lng
			sakhi.save()
			return HttpResponseRedirect('/sakhi_dashboard/')
		else:
			lat = request.POST.get('glat')
			lng = request.POST.get('glng')
			customer = Customer.objects.get(id=id)
			customer.lat = lat
			customer.lng = lng
			customer.save()
			return HttpResponseRedirect('/customer-order/')
	else:
		url_to_post = '/getlocation/' + str(sakhi_user) + '/' + str(id) + '/'
		return render(request,'get_location.html',{'url_to_post':url_to_post})


def recieve_sms(request):
	
	order_mari_regex = re.compile('\d+ order (\d\d?) mari')
	order_oat_regex = re.compile('\d+ order (\d\d?) oat')
	order_nachni_regex = re.compile('\d+ order (\d\d?) nachni')
	order_status_regex = re.compile('\d+ order (\d+) direction (\d)')

	if request.method == 'GET':
		sms_body  = request.GET.get('Body')
		sms_sender = request.GET.get('From')
		sms_id = request.GET.get('SmsSid')		
		
		if order_mari_regex.match(sms_body.strip()):	
			sakhi = Sakhi.objects.get(phone=sms_sender)
			quantity_search = re.search(order_mari_regex, sms_body.strip())
			quantity = quantity_search.group(1)
			new_mari = sakhi.mari+ int(quantity)
			sakhi.mari = new_mari
			sakhi.save()

		if order_oat_regex.match(sms_body.strip()):
			sakhi = Sakhi.objects.get(phone=sms_sender)
			quantity_search = re.search(order_oat_regex, sms_body.strip())
			quantity = quantity_search.group(1)
			new_oat = sakhi.oat+ int(quantity)
			sakhi.oat = new_oat
			sakhi.save()	

		if order_oat_regex.match(sms_body.strip()):
			sakhi = Sakhi.objects.get(phone=sms_sender)
			quantity_search = re.search(order_nachni_regex, sms_body.strip())
			quantity = quantity_search.group(1)
			new_nachni = sakhi.nachni+ int(quantity)
			sakhi.nachni = new_nachni
			sakhi.save()
		if order_status_regex.match(sms_body.strip()):
			order_parse = re.search(order_status_regex, sms_body.strip())
			order_id = order_parse.group(1)
			print order_id
			order_direction = order_parse.group(2)
			print order_direction
			order = Order.objects.get(id=order_id)
			order.order_direction = order_direction
			order.save()
			'''
			sakhi_id = order.placed_from
			sakhi = Sakhi.objects.get(id=sakhi_id)
			phone_number = sakhi.phone
			distance =  	
			'''
			#You can add sending direction sms later

def customer_order(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			user = request.user
			customer = Customer.objects.get(user=user)
			order_type = request.POST.get('type')
			mari = request.POST.get('mari')
			nachni = request.POST.get('nachni')
			oat = request.POST.get('oats')
			urgent_status = request.POST.get('delivery')
			if urgent_status == 'urgent':
				order = Order.objects.create(nachni=nachni,oat=oat,mari=mari,urgent=1,placed_by=customer.id,placed_from=-1)
			else:
				order = Order.objects.create(nachni=nachni,oat=oat,mari=mari,urgent=0,placed_by=customer.id,placed_from=-1)
			order.save()
			match_order_url = '/match_order/' + str(order.id) + '/'
			return HttpResponseRedirect(match_order_url) 
		else:
			return render(request,'customer_order.html')
def match_order(request,order_id):
	order = Order.objects.get(id=order_id)
	all_sakhis = Sakhi.objects.all()
	customer_id = Order.objects.get(id=order_id).placed_by
	customer = Customer.objects.get(id=customer_id)
	customer_lat = customer.lat
	customer_lng = customer.lng
	for sakhi in all_sakhis:
		sakhi_lat = sakhi.lat
		sakhi_lng = sakhi.lng
		sakhi_id = sakhi.id
		if Distance.objects.filter(sakhi_id = sakhi_id,customer_id=customer_id).exists():
			pass
		else:
			request_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins='+customer_lat+','+customer_lng+'&destinations='+sakhi_lat+','+sakhi_lng+'&key=AIzaSyDAwcnYHYw4He8TjQsxqKpEqIXNw08et4M'
			response = urllib2.urlopen(request_url).read()
			json_response = json.loads(response)
			print json_response
			distance = json_response['rows'][0]['elements'][0]['distance']['value']
			customer_addr = json_response['origin_addresses'][0]
			sakhi_addr = json_response['destination_addresses'][0]
			distance_obj = Distance.objects.create(sakhi_id=sakhi.id,customer_id=customer_id,distance=distance,customer_addr=customer_addr,sakhi_addr=sakhi_addr)
			distance_obj.save()
	distances = Distance.objects.filter(customer_id=customer_id).order_by('distance')
	sakhi_with_order = ''
	distance_obj_of_order = ''
	for distance in distances:
		sakhi = Sakhi.objects.get(id = distance.sakhi_id)
		if sakhi.mari >= order.mari and sakhi.nachni >= order.nachni and sakhi.oat >= order.oat: 
			order.placed_from = sakhi.id
			order.save()
			distance_obj_of_order = distance
			sakhi_with_order = sakhi
			break
	if order.placed_from == -1:
		return HttpResponseRedirect('SORRY FOUND NO Sakhi')
	else:
		message_to_send = 'You have an order for ' + str(order.nachni) + ' khaakhra to ' + str(distance_obj_of_order.customer_addr) + ' order id = ' + str(order.id) + ' 1 to deliver 2 to collect 3 to no '
		send_sms(sakhi_with_order.phone,message_to_send)
		order_status_url = '/order_status/'+str(order.id) +'/'
		return HttpResponseRedirect(order_status_url)
def send_sms(number,message):
	ACCOUNT_SID = "AC2deb88c500af87f3abf68e0977e3dd8d" 
	AUTH_TOKEN = "3d508103252df724e85bb633c0455851" 
 	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 	client.messages.create(
    to=number, 
    from_="+14154298601 ", 
    body=message,
	)

def order_status(request,order_id):
	order = Order.objects.get(id=order_id)
	sakhi_id = order.placed_from
	sakhi = Sakhi.objects.get(id=sakhi_id)
	customer_id = order.placed_by
	customer = Customer.objects.get(id=customer_id)
	distance = Distance.objects.get(customer_id=customer_id,sakhi_id=sakhi_id)
	status_of_order = ''
	order_direction = order.order_direction
	print order_direction
	if order_direction == -1:
		status_of_order = 'Order yet to be seen by the sakhi. Kindly be patient.'
	if order_direction == 1:
		status_of_order = 'Order approved. Sakhi will deliver it'
	if order_direction == 2:
		status_of_order = 'Order approved. Collect it from the sakhi'
	if order_direction == 3:
		status_of_order = 'Order redirected. We will reassign a new sakhi and notify you'
	if order_direction == 9:
		status_of_order = 'Order fullfilled. Thank you!'
	sakhi_addr = distance.sakhi_addr
	assigned_with = sakhi.user.first_name
	order_by = customer.user.first_name
	sakhi_phone = sakhi.phone
	customer_addr = distance.customer_addr
	customer_phone = customer.phone
	return render(request,'order_placed.html',{'status_of_order':status_of_order,'sakhi_addr':sakhi_addr,'assigned_with':assigned_with,'order_by':order_by,'sakhi_phone':sakhi_phone,'customer_addr':customer_addr,'customer_phone':customer_phone})

def sakhi_dashboard(request):
	if request.user.is_authenticated():
		user = request.user
		sakhi = Sakhi.objects.get(user=user)
		sakhi_id = sakhi.id
		orders = Order.objects.filter(placed_from=sakhi_id)
		oat = sakhi.oat
		nachni = sakhi.nachni
		mari = sakhi.mari
		return render(request,'sakhi_dashboard.html',{'mari':mari,'nachni':nachni,'oat':oat,'orders':orders})

def give_sakhi_directions(sakhi_id,distance_id):
	pass
def login_sakhi(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username,password=password)
		if user:
			login(request,user)
			return HttpResponseRedirect('/sakhi_dashboard/')
		else:
			return HttpResponse('invalid creds')
	else:
		return render(request,'login.html')

def order_complete(request,order_id):
	order = Order.objects.get(id=order_id)
	order.order_direction = 9
	order.save()
	return HttpResponseRedirect('/sakhi_dashboard/')

def gruh_dashboard_1(request):
	if request.user.is_authenticated():
		username = request.user.username
		if username == 'admin':
			orders = Order.objects.all()
			js_array = [0,0,0,0,0]
			for order in orders:
				if order.order_direction == -1:
					js_array[0]+=1
				elif order.order_direction == 1:
					js_array[1]+=1
				elif order.order_direction == 2:
					js_array[2]+=1
				elif order.order_direction == 3:
					js_array[3]+=1
				elif order.order_direction == 3:
					js_array[3]+=1
				else:
					js_array[4]+=1
			#return render(request,'chart_trial.html')
			return render(request,'gruh_dashboard_1.html',{'js_array':js_array})
def gruh_dashboard_2(request):
	if request.user.is_authenticated():
		username = request.user.username
		if username == 'admin':
			return render(request,'gruh_dashboard_2.html')
def gruh_dashboard_3(request):
	if request.user.is_authenticated():
		username = request.user.username
		if username == 'admin':
			sakhis = Sakhi.objects.all()
			orders = Order.objects.all()
			sakhi_dict = {}
			sakhi_name = []
			mari = []
			nachni = []
			oat = []  
			for order in orders:
				sakhi = Sakhi.objects.get(id=order.placed_by)
				sakhi_username = str(sakhi.user.username)
				print sakhi_username
				if sakhi_username in sakhi_dict:
					print type(sakhi_dict)
					sakhi_dict[sakhi_username][0]+=order.mari
					sakhi_dict[sakhi_username][1]+=order.nachni
					sakhi_dict[sakhi_username][2]+=order.oat
				else:
					sakhi_dict[sakhi_username] = [order.mari,order.nachni,order.oat]
				print len(sakhi_dict)
			for key in sakhi_dict:
				sakhi_name.append(key)
				mari.append(sakhi_dict[key][0])
				nachni.append(sakhi_dict[key][1])
				oat.append(sakhi_dict[key][2])
			print sakhi_name
			print mari
			print nachni
			print oat
			return render(request,'gruh_dashboard_3.html',{'sakhi_name':sakhi_name,'mari':mari,'nachni':nachni,'oat':oat})

	

'''
def get_sms(request):
	ACCOUNT_SID = "AC2deb88c500af87f3abf68e0977e3dd8d" 
	AUTH_TOKEN = "3d508103252df724e85bb633c0455851" 
 	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
 	messages = client.sms.messages.list()
 	print len(messages)
 	for message in messages:
 		if message.direction == 'inbound':
 			print message.body
 			print message.sid
 	return HttpResponse('HI!')
'''