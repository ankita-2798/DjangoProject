from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from polls.models import Question,Choice
from django.utils import timezone
from django.contrib.auth import authenticate,login,logout
from mysite import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
class IndexView(generic.ListView):
	template_name='polls/index.html'
	context_object_name='latest_question_list'
	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
class DetailView(generic.DetailView):
	model=Question
	template_name='polls/detail.html'
	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now())
class ResultsView(generic.DetailView):
	model=Question
	template_name='polls/results.html'
@login_required
def vote(request,question_id):
	p=get_object_or_404(Question,pk=question_id)
	try:
		selected_choice=p.choice_set.get(pk=request.POST['choice'])
	except(KeyError,Choice.DoesNotExist):
		return render(request,'polls/detail.html/',{'question':p,'message':"You didn't select a choice."})
	else:
		selected_choice.votes+=1
		selected_choice.save()
	return HttpResponseRedirect(reverse('polls:results',args=(p.id,)))
def call_signup(request):
	return render(request,'polls/signup.html/')
def create_user(request):
	username=request.POST['username']
	firstname=request.POST['firstname']
	lastname=request.POST['lastname']
	email=request.POST['email']
	password=request.POST['password']
	user=User.objects.create_user(username, email, password)
	user.first_name=firstname
	user.last_name=lastname
	user.save()
	return HttpResponseRedirect(reverse('polls:index'))
def call_login(request):
	return render(request,'polls/login.html/')
def verify_user(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request,user)
			return HttpResponseRedirect(reverse('polls:index'))
		else:
			return render(request,'polls/login.html/',{'message':'The account has been disabled.'})
	else:
		return render(request,'polls/login.html/',{'message':'The username-password combination is incorrect.'})
@login_required
def call_changepassword(request):
	return render(request,'polls/changepassword.html/')
@login_required
def save_password(request):
	my_user=request.user
	username=request.user.username
	oldpassword=request.POST['oldpassword']
	password1=request.POST['password1']
	password2=request.POST['password2']
	test_user= authenticate(username=username, password=oldpassword)
	if test_user is None:
		return render(request,'polls/changepassword.html/',{'message':'The existing password is incorrect.'})
	else:
		if password1!=password2:
			return render(request,'polls/changepassword.html/',{'message':'The entered passwords did not match.'})
		else:
			if password1:
				my_user.set_password(password1)
				my_user.save()
				return render(request,'polls/changepassword.html/',{'message':'The password has been successfully changed.'})
			else:
				return render(request,'polls/changepassword.html/',{'message':'Null passwords not accepted.'})
@login_required
def call_editprofile(request):
	return render(request,'polls/editprofile.html')
@login_required
def save_profile(request):
	email=request.POST['email']
	firstname=request.POST['firstname']
	lastname=request.POST['lastname']
	user=request.user
	if email:
		user.email=email
	if firstname:
		user.first_name=firstname
	if lastname:
		user.last_name=lastname
	user.save()
	return render(request,'polls/editprofile.html/',{'message':'The changes for non-null fields have been successfully made.'})
def log_out(request):
	logout(request)
	return HttpResponseRedirect(reverse('polls:call_login'))
	
	
	

	
