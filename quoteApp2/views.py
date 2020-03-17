from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
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
        loggedinuser = User.objects.get(id = request.session['id'])
        context = {
            "loggedinuser" : User.objects.get(id = request.session['id']),
            "allQuotes": Quote.objects.exclude(favorite = loggedinuser),
            "favoriteQuotes": Quote.objects.filter(favorite = loggedinuser)
        }
    return render(request, "quotes.html", context)

def addQuote(request):
    errorsFromQuoteValidator = User.objects.quote_validator(request.POST)
    loggedinuser = User.objects.get(id=request.session["id"])
    if len(errorsFromQuoteValidator) > 0:
        for key, value in errorsFromQuoteValidator.items():
            messages.error(request, value)
        return redirect("/quotes")
    print(request.POST)
    print("addQuote is working!")
    new_quote = Quote.objects.create(poster = loggedinuser, quoter= request.POST['quoter'], message=request.POST['message'])
    return redirect ("/quotes")

def addFavorite(request, quote_id):
    quoteToAdd = Quote.objects.get(id=quote_id)
    loggedinuser = User.objects.get(id=request.session["id"])
    loggedinuser.favorite_quote.add(quoteToAdd)
    return redirect("/quotes")

def removeFavorite(request, quote_id):
    print("This is Running!")
    quoteToRemove = Quote.objects.get(id = quote_id)
    loggedinuser = User.objects.get(id=request.session["id"])
    loggedinuser.favorite_quote.remove(quoteToRemove)
    return redirect("/quotes")

def editQuote(request, quote_id):
    loggedinuser = User.objects.get(id=request.session["id"])
    quoteToEdit = Quote.objects.get(id=quote_id)
    print(request.POST)
    context = {
        "quote": quoteToEdit
    }
    return render(request, "edit.html", context)

def updateQuote(request, quote_id):
    errorsFromEditQuoteValidator = User.objects.edit_quote_validator(request.POST)
    loggedinuser = User.objects.get(id=request.session["id"])
    if len(errorsFromEditQuoteValidator) > 0:
        for key, value in errorsFromEditQuoteValidator.items():
            messages.error(request, value)
        return redirect("editQuote", quote_id=quote_id)
    quoteToEdit = Quote.objects.get(id=quote_id)
    quoteToEdit.quoter = request.POST['quoter']
    quoteToEdit.message = request.POST['message']
    quoteToEdit.save()
    return redirect("/quotes")

def userQuotes(request, user_id):
    count = Quote.objects.filter(poster=user_id).count()
    user = User.objects.get(id=user_id)
    messages = Quote.objects.filter(poster=user)
    allQuotes = Quote.objects.all()
    context = {
        "user": user,
        "count": count,
        "messages": messages
    }
    return render(request, "user.html", context)

def deleteQuote(request, quote_id):
    quoteToDelete = Quote.objects.get(id=quote_id)
    quoteToDelete.delete()
    return redirect("/quotes")

def Logout(request):
    request.session.clear()
    return redirect("/")

def Dashboard(request):
    return redirect("/quotes")
    

    
