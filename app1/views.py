from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Company, StockPrice
import yfinance as yf
from joblib import load
import pandas as pd
import numpy as np


fundModel=load('C:/Users/suyog/Downloads/FinalYearProject-main/FinalYearProject-main/FinalYearProject-main/savedModels/Fund.joblib')
bondsModel=load('C:/Users/suyog/Downloads/FinalYearProject-main/FinalYearProject-main/FinalYearProject-main/savedModels/Bonds.joblib')
fdModel=load('C:/Users/suyog/Downloads/FinalYearProject-main/FinalYearProject-main/FinalYearProject-main/savedModels/FD.joblib')
fidModel=load('C:/Users/suyog/Downloads/FinalYearProject-main/FinalYearProject-main/FinalYearProject-main/savedModels/FID.joblib')
goldModel=load('C:/Users/suyog/Downloads/FinalYearProject-main/FinalYearProject-main/FinalYearProject-main/savedModels/Gold.joblib')
realEstateModel=load('C:/Users/suyog/Downloads/FinalYearProject-main/FinalYearProject-main/FinalYearProject-main/savedModels/RealEstate.joblib')
stockModel=load('C:/Users/suyog/Downloads/FinalYearProject-main/FinalYearProject-main/FinalYearProject-main/savedModels/Stocks.joblib')

def fetch_stock_prices():
    companies = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Google': 'GOOGL',
        'Amazon': 'AMZN',
        'Tesla': 'TSLA'
    }

    for company_name, symbol in companies.items():
        stock = yf.Ticker(symbol)
        price = stock.history(period='1d')['Close'][0]
        
        company, created = Company.objects.get_or_create(name=company_name)
        StockPrice.objects.create(company=company, price=price)

def index(request):
    fetch_stock_prices()
    stock_prices = StockPrice.objects.all()
    return render(request, 'index.html', {'stock_prices': stock_prices})

def investTypes(request):
    return render(request, "investtypes.html")



@login_required
def home(request):
    return render(request, "home.html", {'username': request.user.username})

@login_required
def goal(request):
    global reason
    if request.method == 'POST':
        reason=float(request.POST.get('option'))
        
    return render(request, "goal.html", {'username': request.user.username})

@login_required
def imp(request):
    global year
    if request.method == 'POST':
        year= float(request.POST.get('option'))
        
    return render(request, "imp.html", {'username': request.user.username})

@login_required
def investTypes(request):
    return render(request, "investtypes.html",{'username': request.user.username})

@login_required
def recommend(request):
    global risk
    if request.method == 'POST':
        risk =float(request.POST.get('option'))
        input_data = np.array([[reason,year,risk]])
        fund_pred=fundModel.predict(input_data)
        bond_pred=bondsModel.predict(input_data)
        fd_pred=fdModel.predict(input_data)
        fid_pred=fidModel.predict(input_data)
        gold_pred=goldModel.predict(input_data)
        estate_pred=realEstateModel.predict(input_data)
        stock_pred=stockModel.predict(input_data)
        fd1=fund_pred[0]
        fd2=bond_pred[0]
        fd3=fd_pred[0]
        fd4=fid_pred[0]
        fd5=gold_pred[0]
        fd6=estate_pred[0]
        fd7=stock_pred[0]
        print(fd1)
        print(fd2)
        print(fd3)
        print(fd4)
        print(fd5)
        print(fd6)
        print(fd7)
    return render(request,"recommend.html",{'username': request.user.username,'fd1':fd1,'fd2':fd2,'fd3':fd3,'fd4':fd4,'fd5':fd5,'fd6':fd6,'fd7':fd7})

@login_required
def statergy(request):
    return render(request,"statergy.html",{'username': request.user.username})

@login_required
def page1(request):
    return render(request,"1.html",{'username':request.user.username})

@login_required
def page2(request):
    return render(request,"2.html",{'username':request.user.username})

@login_required
def page3(request):
    return render(request,"3.html",{'username':request.user.username})

@login_required
def page4(request):
    return render(request,"4.html",{'username':request.user.username})

@login_required
def page5(request):
    return render(request,"5.html",{'username':request.user.username})

def warning(request):
    return render(request,"warning.html")

def usernamewarning(request):
    data = {
        'message' : 'Username is alredy taken please try different.'
    }
    return render(request,"usernamewarning.html",data)

def landingpage(request):
    data = {
        'title' : 'Home Page',
        'image1' : 'Our product provides expert recommendations for your investment portfolio, saving you time and effort in researching and analyzing investment options.',
        'image2' : 'With our product, you can easily build a diversified portfolio that aligns with your financial goals. We take into account your risk tolerance, investment horizon, and financial objectives.',
        'image3' : 'Our expert recommendations help you make informed investment decisions to achieve your financial goals. Whether youre saving for retirement, buying a house, or funding your child education, weve got you covered.'
    }
    return render(request,"MainPage.html",data)

def user_login(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('password1')

        try:
            user = authenticate(request, username=uname, password=pass1)
            if user is not None:
                login(request, user)
                return render(request, "home.html", {'username': uname})
            else:
                return render(request,"alert.html")
        except IntegrityError as e:
            return HttpResponse(f"IntegrityError occurred: {str(e)}")
    return render(request,"login.html")

def user_logout(request):
    logout(request)
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email1 = request.POST.get('email1')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('cpassword1')

        try:
            if len(pass1) <= 8 or pass1 != pass2 or len(uname) <= 8:
                raise ValueError('Invalid input')

            user = User.objects.create_user(uname, email1, pass1)
            return redirect('login')

        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e) and 'username' in str(e):
                return redirect("usernamewarning")
                # return HttpResponse('Username already exists. Please choose a different username.')
            else:
                return HttpResponse('An error occurred during sign up.')

        except ValueError as e:
            return redirect('warning')

    return render(request, "signup.html")