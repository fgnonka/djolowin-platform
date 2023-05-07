from wallet.models import UserWallet
from collection.models import CompletedCollection
from collection.signals import collection_completed


def release_reward(user, collection, **kwargs):
    completed_collection = CompletedCollection.objects.get_or_create(
        user=user, collection=collection, reward=collection.reward
    )
    if not completed_collection.reward_received:
        # Establish the amount of reward to give based on the collection
        reward_amount = collection.reward.amount
        # Query the user's wallet and add the reward to it'
        wallet = UserWallet.objects.get(user=user)
        wallet.balance += reward_amount
        wallet.save()
        
        completed_collection.reward_received = True
        completed_collection.save()


collection_completed.connect(release_reward)
