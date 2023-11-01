from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from .models import trader_collection, trades
from .form import NewTrader
from .util import total_earning, total_loss, simulate_trading
import threading, pymongo

# Create your views here.

thread = threading.Thread(target=simulate_trading)
thread.daemon = True
thread.start()


def trader_list(request):
    traders = trader_collection.find()
    context = {
        "traders": traders
    }
    
    template = loader.get_template('traders.html')
    return HttpResponse(template.render(context, request))


def add_new_trader(request):
    template = loader.get_template('add-traders.html')
    context = {
        "form": NewTrader()
    }

    if request.method == "POST":
        form = NewTrader(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            stock = int(form.cleaned_data['stock'])

            record = {
                "first_name": firstname,
                "last_name": lastname,
                "email": email,
                "stock_value": stock
            }

            trader_collection.insert_one(record)
            
            messages.success(request, 'New Record created!')
        else:
            messages.warning(request, 'Invalid Record details')

    return HttpResponse(template.render(context, request))


def trader_analytics(request, trader_name):
    trader = trader_collection.find_one({'first_name': trader_name })   
    if trader: 
        trade_timeline = trades.find({'trader_id': trader['_id']}).limit(5)
        
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

        template = loader.get_template('trader_analytics.html')

        return HttpResponse(template.render(context, request))
    else:
        return redirect('traders')


