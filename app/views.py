from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from twilio.rest import TwilioRestClient

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
		print username
		user = User.objects.create_user(username=username,password=password,first_name=name)
		user.set_password(password)
		user.save()
		return HttpResponseRedirect('/admin')
	else:
		return render(request,'sakhi_register.html')

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