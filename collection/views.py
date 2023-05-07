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
        card_quantities = get_user_card_collection_quantities(owner)

        # print("Card Quantities:", card_quantities)  # Debugging statement

        collection_progress = {}
        for collection in collections:
            collection_progress[collection] = get_collection_progress(owner, collection)
            for collection, data in collection_progress.items():
                if data['progress'] == 100:
                    reward = collection.reward.amount
                    messages.success(self.request, f'You have completed the {collection} collection and have been awarded {reward} DJOBA!')
                    collection_completed.send(sender=self.__class__, user=owner, collection=collection)

        context['collection_progress'] = collection_progress
        context['card_quantities'] = card_quantities
        return context


