from django.urls import path 
from quoteApp2 import views 
urlpatterns = [ 
    path('', views.index), 
    path('register', views.Register),
    path('login', views.Login),
    path('quotes', views.Quotes),
    path('add_quote', views.addQuote),
    path('favorites/<quote_id>', views.addFavorite),
    path('removefavorites/<quote_id>', views.removeFavorite),
    path('user/<user_id>', views.userQuotes),
    path('logout', views.Logout),
    path('dashboard', views.Dashboard),
    path('quotes/<quote_id>', views.editQuote, name="editQuote"),
    path('edit/<quote_id>', views.updateQuote),
    path('delete/<quote_id>', views.deleteQuote),
] 
