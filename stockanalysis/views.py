from django.shortcuts import render
from dal import autocomplete
from .models import Stock
from .forms import StockForm
from .utils import scrap_stock_data
# Create your views here.

def stocks(request):
    
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            stock_id = request.POST.get("stock")
            stock = Stock.objects.get(id=stock_id)
            symbol = stock.symbol
            exchange = stock.exchange
            stock_data = scrap_stock_data(symbol=symbol, exchange=exchange)
            print(stock_data)
            
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