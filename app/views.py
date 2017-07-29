from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from twilio.rest import TwilioRestClient
from models import Sakhi, Customer, Order
import re
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
			return HttpResponseRedirect('/admin')
		else:
			lat = request.POST.get('glat')
			lng = request.POST.get('glng')
			customer = Customer.objects.get(id=id)
			customer.lat = lat
			customer.lng = lng
			customer.save()
			return HttpResponseRedirect('/admin')
	else:
		url_to_post = '/getlocation/' + str(sakhi_user) + '/' + str(id) + '/'
		return render(request,'get_location.html',{'url_to_post':url_to_post})


def recieve_sms(request):
	
	order_mari_regex = re.compile('\d+ order (\d\d?) mari')
	order_oat_regex = re.compile('\d+ order (\d\d?) oat')
	order_nachni_regex = re.compile('\d+ order (\d\d?) nachni')


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
			print mari
			print oat
			print nachni
			if urgent_status == 'urgent':
				order = Order.objects.create(nachni=nachni,oat=oat,mari=mari,urgent=1,placed_by=customer.id,placed_from=-1)
			else:
				order = Order.objects.create(nachni=nachni,oat=oat,mari=mari,urgent=0,placed_by=customer.id,placed_from=-1)

		else:
			return render(request,'customer_order.html')


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
