from django.shortcuts import render
from dal import autocomplete
from .models import Stock
from .forms import StockForm
# Create your views here.

def stocks(request):
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