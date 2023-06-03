from django.contrib import admin
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
    path("playercard/", include("playercard.urls", namespace="playercard")),
    path("transaction/", include("transaction.urls", namespace="transaction")),
    path("wallet/", include("wallet.urls", namespace="wallet")),
    path("social-auth/", include("social_django.urls", namespace="social")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
