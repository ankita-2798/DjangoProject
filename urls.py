from django.conf.urls import patterns,url
from polls import views
from django.contrib.auth.decorators import login_required
urlpatterns=patterns('',
					url(r'^$',views.IndexView.as_view(),name='index'),
					url(r'^(?P<pk>\d+)/$',views.DetailView.as_view(),name='detail'),
					url(r'^(?P<pk>\d+)/results/$',views.ResultsView.as_view(),name='results'),
					url(r'^(?P<question_id>\d+)/vote/$',views.vote,name='vote'),
					url(r'^signup/$', views.call_signup, name='call_signup'),
					url(r'^login/$', views.call_login, name='call_login'),
					url(r'^createuser/$', views.create_user, name='create_user'),
					url(r'^verifyuser/$', views.verify_user, name='verify_user'),
					url(r'^changepassword/$', views.call_changepassword, name='call_changepassword'),
					url(r'^savepassword/$', views.save_password, name='save_password'),
					url(r'^editprofile/$', views.call_editprofile, name='call_editprofile'),
					url(r'^saveprofile/$', views.save_profile, name='save_profile'),
)