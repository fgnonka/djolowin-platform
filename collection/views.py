from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView, DetailView

from .actions import has_user_completed_collection, get_collection_progress
from .models import Collection

class CollectionListView(LoginRequiredMixin, ListView):
    model = Collection
    template_name = 'djolowin/collection/collection_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collections = Collection.objects.all()
        owner = self.request.user
        user_cards = owner.playercards.all()
        
        collection_progress = {}
        for collection in collections:
            collection_progress[collection] = get_collection_progress(owner, collection)
            
        context['collection_progress'] = collection_progress
        return context

