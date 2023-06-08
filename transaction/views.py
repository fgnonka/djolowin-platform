from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Transaction
# Create your views here.

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'djolowin/transaction/transaction_history.html'
    context_object_name = 'transactions'
    paginate_by = 10

    def get_queryset(self):
        return Transaction.objects.filter(buyer=self.request.user).order_by('-timestamp')