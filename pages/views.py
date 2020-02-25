from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

# Create your views here.
class LandingView(View):
	def get(self,request,*args,**kwargs):
		context = {
			'title' : 'Welcome To Our Site'
		}
		return render(request,'pages/landing.html',context)