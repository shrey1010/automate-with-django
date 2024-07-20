from django.shortcuts import render,redirect,get_object_or_404
from dal import autocomplete
from .models import Stock,StockData
from .forms import StockForm
from .utils import scrap_stock_data
from django.contrib import messages
# Create your views here.

def stocks(request):
    
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            stock_id = request.POST.get("stock")
            stock = Stock.objects.get(id=stock_id)
            symbol = stock.symbol
            exchange = stock.exchange
            stock_response = scrap_stock_data(symbol=symbol, exchange=exchange)
            
            if stock_response == None:
                messages.error(request,f"Could Not fetch data for {symbol}")
                return redirect('stocks')
            
            try:
                stock_data = StockData.objects.get(stock=stock)
                
            except StockData.DoesNotExist:
                stock_data = StockData(stock=stock)

            stock_data.current_price = stock_response["current_price"]
            stock_data.price_changed = stock_response["price_change"]
            stock_data.percentage_changed = stock_response["percentage_change"]
            stock_data.previous_close = stock_response["previous_close"]
            stock_data.week_52_high = stock_response["week_52_high"]
            stock_data.week_52_low = stock_response["week_52_low"]
            stock_data.market_cap = stock_response["market_cap"]
            stock_data.pe_ratio = stock_response["pe_ratio"]
            stock_data.avg_volume = stock_response["avg_volume"]
            stock_data.save()
            return redirect("stock_detail",stock_data.id)
            
        else:
            context={
            "form": form,
            }
            return render(request, "stockanalysis/stocks.html",context=context)
            
    else:
        form = StockForm()
        context = {
            "form": form,
        }
        return render(request, "stockanalysis/stocks.html",context=context)

class StockAutocomplete(autocomplete.Select2QuerySetView):
     def get_queryset(self):
        if not self.request.user.is_authenticated:
             return Stock.objects.none()
        
        qs = Stock.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
            
        return qs
    
def stock_detail(request, stock_id):
    stock_data = get_object_or_404(StockData, pk=stock_id)
    context = {
        "stock_data":stock_data,
    }
    
    return render(request, "stockanalysis/stock_detail.html",context=context)