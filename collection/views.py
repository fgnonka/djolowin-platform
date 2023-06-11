from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView, DetailView

from .actions import get_collection_progress, get_user_card_collection_quantities
from .models import Collection
from .signals import collection_completed

class CollectionListView(LoginRequiredMixin, ListView):
    model = Collection
    template_name = 'djolowin/collection/collection_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collections = Collection.objects.all()
        owner = self.request.user
        cards_count = {}
        for collection in collections:
            cards_count[collection.id] = get_user_card_collection_quantities(owner, collection)
        print(cards_count)
        context['collections'] = collections
        context['cards_count'] = cards_count
        return context


class CollectionDetailView(LoginRequiredMixin, DetailView):
    model = Collection
    template_name = 'djolowin/collection/collection_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection = self.get_object()
        owner = self.request.user
        collection_progress = get_collection_progress(owner, collection)
        print(collection)
        context['collection_progress'] = collection_progress
        context['cards_count'] = get_user_card_collection_quantities(owner, collection)
        # context['collec']
        return context



