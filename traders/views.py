from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from .models import trader_collection, trades
from django.template import loader
from .form import TraderLogin
from tradeadmin.util import total_earning, total_loss
import pymongo


# Create your views here.


def login(request):
    context = {
        'form': TraderLogin()
    }

    if request.method == "POST":
        form = TraderLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            is_listed = trader_collection.find_one({'email': email})
            trader_name = is_listed['first_name']

            if is_listed:
                return redirect(reverse('trader_dashboard', args=[trader_name]))
            else:
                messages.info(request, "No email record found. Try Again!")

    template = loader.get_template('login.html')
    return HttpResponse(template.render(context, request))


def trader_dashboard(request, trader_name):
    trader = trader_collection.find_one({'first_name': trader_name }) 
    if trader:   
        trade_timeline = trades.find({'trader_id': trader['_id']}).limit(5).sort('timestamp', pymongo.ASCENDING)
        
        # get total earning
        fil_pr = {
            '$and': [
                {'trader_id': trader['_id']},
                {'status': 'profit'}
            ]
        }
        tt_en = trades.find(fil_pr)
        total_en = total_earning(tt_en)
        
        #  get total loss
        fil_ls = {
            '$and': [
                {'trader_id': trader['_id']},
                {'status': 'loss'}
            ]
        }
        tt_ls = trades.find(fil_ls)
        total_ls = total_loss(tt_ls)

        
        data_points = trades.find({'trader_id': trader['_id']}).sort('timestamp', pymongo.ASCENDING)
        timestamps = []
        profit_loss = []
        
        for x in data_points:
            timestamps.append(x['timestamp'].strftime('%H:%M'))
            profit_loss.append(x['balance'])

        context = {
            "details": trader,
            "total_earning": total_en,
            "total_loss": total_ls,
            "timelines": trade_timeline,
            'timestamps': timestamps,
            'profit_loss': profit_loss
        }

        template = loader.get_template('dashboard.html')
        return HttpResponse(template.render(context, request))
    else:
        return redirect('trader_login')
 
