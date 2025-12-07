from django.shortcuts import render,redirect,reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tkinter.tix import IMAGE
from PIL import Image , ImageTk 
from django.contrib.auth.models import User

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def home_view(request):
    #  if request.user.is_authenticated:
    #      return HttpResponseRedirect('afterlogin')  
     return render(request,'medical/index.html')


def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

def aboutus_view(request):
    return render(request,'medical/aboutus.html')


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



def fruits(request):        
        return render(request, "customer/fruits.html")


def classification1(request):
	return render(request, 'customer/classification1.html')


def classification1(request):
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        up=upload
        fn = up
        print("uploaded:",up)
        
    
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        print("save ", file)
        file_url = fss.url(file)
        print("url:",file_url)
        
       
        imgpath = up
        
        fn = up
        IMAGE_SIZE = 64
        LEARN_RATE = 1.0e-4
        CH=3
        print(fn)
        if fn!="":

            #img = cv2.imread('C:/new/21C9588-Rice prediction/rice_web/rice_web/media/image.png',0)
            img = Image.open(fn)
            img = np.array(img.convert('L'))
            
            
            print(img)
            
            filename1 = 'media/grey.jpeg'
            cv2.imwrite(filename1, img)
            
        
            file_url1 = fss.url(filename1)
            print("url:",file_url1) 
             
        
            #convert into binary
            ret,binary = cv2.threshold(img,160,255,cv2.THRESH_BINARY)# 160 - threshold, 255 - value to assign, THRESH_BINARY_INV - Inverse binary
            #img.save('media/binary.jpeg')
            filename2 = 'media/binary.jpeg'
            
            cv2.imwrite(filename2, binary)
            # Model Architecture and Compilation
        
            model = load_model(r'C:\Users\COMPUTER\Downloads\100%finalcodeskin_disease_chatbot_system\skin_disease_chatbot_system\skin_model.h5')
                
            # adam = Adam(lr=LEARN_RATE, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0)
            # model.compile(optimizer=adam, loss='categorical_crossentropy', metrics=['accuracy'])
            
            img = Image.open(fn)
            img = img.resize((IMAGE_SIZE,IMAGE_SIZE))
            img = np.array(img)
            
            img = img.reshape(1,IMAGE_SIZE,IMAGE_SIZE,3)
            
            img = img.astype('float32')
            img = img / 255.0
            print('img shape:',img)
            prediction = model.predict(img)
            print(np.argmax(prediction))
            disease=np.argmax(prediction)
            print(disease)
            if disease == 0:
                Cd="Normal"
                ans=""

            elif disease == 1:
                Cd="Actinic keratosis"
                ans="Precaution- Wear Sunscreen,Avoid Sun Exposure During Peak Hours,Use Protective Clothing"
              
            elif disease == 2:
                Cd="Nevus"
                ans="Precaution-  Asymmetry: One half of the mole doesn’t match the other.Border: Edges are irregular, jagged, or blurred.Color: Uneven color or multiple shades (brown, black, red, white, or blue).Diameter: Larger than 6 mm (about the size of a pencil eraser).Evolving: Changes in size, shape, or color over time."
                
            elif disease == 3:
                Cd= "Melanoma"
                ans="Precaution- Avoid Direct Sunlight During Peak Hours. Use Broad-Spectrum Sunscreen"
                
           
            
           
                
                
            A=Cd
        
            
            
          
            return render(request, "customer/fruits.html", {"predictions1": A,"ans1":ans,'file_url': file_url})  

    else:
    
        return render(request, "customer/classification1.html") #
    #return render(request, "classification1.html")
     
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