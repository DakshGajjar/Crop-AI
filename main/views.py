from django.shortcuts import render
from django.contrib import messages
from .utils import crop_recommend,crop_disease_detetct,crop_yield,crop_pest_identify
from main.models import imginput,pestimg
from datetime import datetime
#import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

#Home-Page
def home(request):
    """
    The home page of the application. It is the landing page for the user. 
    """

    return render(request,'home.html')

#About-Page
def about(request):
    """
    Render the about page.
    @param request - the request object
    @returns the rendered about page
    """

    return render(request,'about.html')

#Help-Page
def help(request):
    """
    Render the help page.
    @param request - the request object
    @returns the rendered help page
    """

    return render(request,'help.html')

#Crop Recommendation Page
def croprec(request):
    """
     this function takes the input from the user and returns the crop recommendations 
    """

    if request.method=='POST':
        n = request.POST.get('nitrogen')
        p = request.POST.get('phosphorus')
        k = request.POST.get('potassium')
        ph = request.POST.get('ph')
        rf = request.POST.get('rainfall')
        t = request.POST.get('temp')
        h = request.POST.get('hum')
        if n and p and k and ph and rf and t and h:
            if int(n)<120 and int(p)<140 and int(k)<200 and int(ph)<15 and int(rf) < 350 and int(rf) > 15 and int(t) < 45 and int(t) > 5 and int(h) < 100 and int(h) > 8:
                messages.success(request,'Success!!!')
                context = crop_recommend(n,p,k,ph,rf,t,h)
                return render(request,'croprec.html',context)
        messages.warning(request,'Error!! try again with appropriate input')
    return render(request,'croprec.html')

#Crop Disease Detection Page
def cropdis(request):
    """
    this function is used to take the image and detect the crop disease.
    @param request - the request object
    @return the html page with the image and the disease
    """

    try:
        context = {}
        if request.method == 'POST':
            img = request.FILES.get('imgupload')
            obj = imginput(img=img)
            obj.save()
            p = obj.img.path
            lis = crop_disease_detetct(p)
            context['image'] = obj
            context['cls'] = lis[2].upper()
            context['title'] = f'Detected Disease - {lis[2]}'
            context['info'] = lis[0]
            context['control'] = lis[1]
            messages.success(request,'Success!!!')
    except:
        messages.warning(request,'Error!! try again with appropriate input')
    return render(request,'cropdis.html',context)

#Crop Yield Page
def cropyield(request):
    """
    The function to calculate the crop yield resources.
    @param crop - the crop name
    @param qn - the quantity in quintals
    @returns the crop yield resources
    """

    context = {}
    l = ['Paddy','Jowar','Bajara','Maize','Cotton','Groundnut','Soyabean','Wheat','Barley','Gram']
    if request.method == 'POST':
        c = request.POST.get('cn')
        qn = request.POST.get('qn')
        if c and qn:
            if int(qn)<1000:
                crop =  l[int(c)-1]
                p,w,gd = crop_yield(crop,int(qn))
                w = w.replace('-','to')
                gd = gd.replace('-',' to ')
                messages.success(request,'Success!!!')
                context = {'cr':f'Crop - {l[int(c)-1]}','qn':f'Quantity - {qn} Quintals','pr':f'Price - {p} Rs.','wt':f'Water - {w} mm' , 'gd':f'Time - {gd}'}
            else:
                messages.warning(request,'Error!! try again with appropriate input')
    return render(request,'cropyield.html',context)

#Crop Pest Identification Page
def pests(request):
    """
    This function is used to upload an image and classify it. It will return the insect name,
    the classification, and the control.
    @param request - the request object
    @returns the context dictionary
    """

    #try:
    context = {}
    if request.method == 'POST':
        img = request.FILES.get('pest')
        obj = pestimg(pimg=img)
        obj.save()
        p = obj.pimg.path
        lis = crop_pest_identify(p)
        context['image'] = obj
        context['cls'] = lis[0].upper()
        context['title'] = f'Insect Name - {lis[0]}'
        context['info'] = lis[1]
        context['ctrl'] = lis[2]
        messages.success(request,'Success!!!')
    #except:
        #messages.warning(request,'Error!! try again with appropriate input')
    return render(request,'crop_pest.html',context)