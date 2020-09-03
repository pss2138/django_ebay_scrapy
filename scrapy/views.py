from django.shortcuts import render
from django.http import HttpResponse

from main.forms import SearchForm
from .ebay_scrapy import scrapy


def show_results(request):
    
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('search')
            form.save()
            table_recommendation, totalentries, table_shippingcost, table_category, table_price, table_duration, table_keyword, table_related, graph = scrapy(text)
            args = {"table_recommendation":table_recommendation, "totalentries": totalentries, "table_shippingcost": table_shippingcost, 
                    "table_category": table_category, "table_price": table_price, "table_duration": table_duration, 
                    "table_keyword": table_keyword, "table_related": table_related, "data": graph, "text":text}

            return render(request, "scrapy/results.html", args)
            

    form = SearchForm()
    return render(request, "scrapy/results.html", {"form": form})


