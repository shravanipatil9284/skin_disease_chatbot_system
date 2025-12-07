from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from customer.chat import get_response,bot_name
import speech_recognition as sr
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from googletrans import Translator
from translate import Translator as trans
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from gtts import gTTS
import os
import numpy as np
from tensorflow.keras.models import load_model
from tkinter.tix import IMAGE
from PIL import Image , ImageTk 

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class eng(TemplateView):
    template_name = "customer/eng.html"

    def get(self, request):
        context = {
            "chat_history": [
                {"sender": "bot", "text": "Hi, how can I assist you?"}
            ]
        }
        return render(request, self.template_name, context)

    def post(self, request):
        if request.method == 'POST':
            user_message = request.POST.get('input', False)
            bot_response = get_response(user_message)
            if bot_response is None:
                bot_response = "I'm sorry, I don't understand your question. Please contact this number: 9828798798"
            
            # Get chat history from session or initialize if not present
            chat_history = request.session.get('chat_history', [])
            
            # Append new messages to the chat history
            chat_history.append({"sender": "user", "text": user_message})
            chat_history.append({"sender": "bot", "text": bot_response})
            
            # Save updated chat history back to the session
            request.session['chat_history'] = chat_history
            
            context = {"chat_history": chat_history}
        return render(request, self.template_name, context)

@login_required(login_url='customerlogin')
def customer_dashboard_view(request):
    

    dict={
        'customer':models.Customer.objects.get(user_id=request.user.id),
       
    }
    if request.method == 'POST':
        user = request.POST.get('input',False)
        context1={"user":user,"bot":get_response(user)}
			
		
    return render(request,'customer/customer_dashboard.html',context=dict)



from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


#Develop by Haseeb Asghar
#https://www.linkedin.com/in/infohaseeb/
#https://github.com/infohaseeb

def LoginUser(request):
    if request.user.username=="":
        return render(request,"customer/login.html")
    else:
        return HttpResponseRedirect("/homepage")

@login_required(login_url="/loginuser/")
def HomePage(request):
    return render(request, "medical/home.html")

def clicklogin(request):
    if request.method!="POST":
        return HttpResponse("<h1> Methoid not allowed<h1>")
    else:
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        
        user=authenticate(username=username,password=password)
        if user!=None:
            login(request,user)
            return HttpResponseRedirect('/homepage')
        else:
            messages.error(request, "Invalid Login")
            return HttpResponseRedirect('/loginuser')

def LogoutUser(request):
    logout(request)
    request.user=None
    return HttpResponseRedirect("/loginuser")       




def RegisterUser(request):
    if request.user==None or request.user =="" or request.user.username=="":
        return render(request,"customer/register.html")
    else:
        return HttpResponseRedirect("/homepage")        


def ClickRegister(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
            User.objects.create_user(username, email, password)
            messages.success(request, "User Created Successfully")
            return HttpResponseRedirect('/register_user')
        else:
            messages.error(request, "Email or Username Already Exist")
            return HttpResponseRedirect('/register_user')


