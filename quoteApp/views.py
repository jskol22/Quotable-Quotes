from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Quote
import bcrypt


def index(request): 
    return render(request, "index.html") 

def Register(request):
    print(request.POST)
    errorsFromModelsValidator = User.objects.registration_validator(request.POST)
    if len(errorsFromModelsValidator) > 0:
        for key, value in errorsFromModelsValidator.items():
            messages.error(request, value)
        return redirect ("/")
    else: 
        print(request.POST['password'])
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        print(hash1)
        user = User.objects.create(name= request.POST['name'], email= request.POST['email'], password= hash1.decode())
        request.session['id'] = user.id
    return redirect("/quotes")

def Login(request):
    errorsFromLoginValidator = User.objects.login_validator(request.POST)
    if len(errorsFromLoginValidator) > 0:
        for key, value in errorsFromLoginValidator.items():
            messages.error(request, value)
        return redirect("/")
    request.session['id'] = User.objects.filter(email= request.POST['email'])[0].id
    return redirect("/quotes")
def Quotes(request):
    if 'id' not in request.session:
        return redirect("/")
    else:
        context = {
            "loggedinuser" : User.objects.get(id = request.session['id']),
            "allQuotes": Quote.objects.all()
        }
    return render(request, "quotes.html", context)
def addQuote(request):
    errorsFromQuoteValidator = User.objects.quote_validator(request.POST)
    if len(errorsFromQuoteValidator) > 0:
        for key, value in errorsFromQuoteValidator.items():
            messages.error(request, value)
        return redirect("/quotes")
    print(request.POST)
    print("addQuote is working!")
    new_quote = Quote.objects.create(quoter= request.POST['quoter'], message=request.POST['message'])
    return redirect ("/quotes")

