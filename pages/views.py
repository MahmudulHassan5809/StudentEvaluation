from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

# Create your views here.
class LandingView(View):
	def get(self,request,*args,**kwargs):
		context = {
			'title' : 'Welcome To Our ISU Student Evaluation'
		}
		return render(request,'pages/landing.html',context)




class AboutUsView(View):
    def get(self,request,*args,**kwargs):
        context = {
            'title' : 'About ISU Student Evaluation'
        }
        return render(request,'pages/about_us.html',context)
