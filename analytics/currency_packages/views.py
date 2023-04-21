from django.shortcuts import render
from app_currency.models import CurrencyPackage


def most_popular_currency_packages(request):
    packages = CurrencyPackage.objects.order_by("-usage_count")[:10]
    context = {"packages": packages}
    return render(request, "popular_currency_packages.html", context)


def total_currency_package_purchases(request, package_id):
    package = CurrencyPackage.objects.get(id=package_id)
    purchases = package.purchases.all()
    context = {"package": package, "purchases": purchases}
    return render(request, "currency_package_purchases.html", context)
