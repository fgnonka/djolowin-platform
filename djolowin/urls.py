from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from graphene_django.views import GraphQLView


urlpatterns = [
    path("", include("base.urls", namespace="base")),
    path("admin/", admin.site.urls),
    path("account/", include("account.urls", namespace="account")),
    path("auction/", include("auction.urls", namespace="auction")),
    path("bundle/", include("bundle.urls", namespace="bundle")),
    path("collection/", include("collection.urls", namespace="collection")),
    path("communication/", include("communication.urls", namespace="communication")),
    path("currency/", include("app_currency.urls", namespace="currency")),
    path("graphql/", GraphQLView.as_view(graphiql=True)),
    path("my-djolowin/", include("djolowin_profile.urls", namespace="djolowin_profile")),
    path("playercard/", include("playercard.urls", namespace="playercard")),
    path("social-auth/", include("social_django.urls", namespace="social")),
    path("transaction/", include("transaction.urls", namespace="transaction")),
    path("wallet/", include("wallet.urls", namespace="wallet")),
]

urlpatterns += staticfiles_urlpatterns()

