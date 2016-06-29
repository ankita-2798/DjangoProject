from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from polls.models import Question,Choice
from django.utils import timezone
from django.contrib.auth import authenticate,login
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
		return render(request,'polls/detail.html/',{'question':p,'error_message':"You didn't select a choice."})
	else:
		selected_choice.votes+=1
		selected_choice.save()
	return HttpResponseRedirect(reverse('polls:results',args=(p.id,)))
def call_signup(request):
	return render(request,'polls/signup.html/')
def call_login(request):
	return render(request,'polls/login.html/')
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
def verify_user(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request,user)
			return HttpResponse("U r logged in.")
		else:
			return HttpResponse("The account has been disabled.")
	else:
		return HttpResponse("The username-password combination is incorrect.")
