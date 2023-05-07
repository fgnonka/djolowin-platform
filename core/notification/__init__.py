from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.sites.models import Site

from core.utils import build_absolute_uri

LOGO_URL = "images/djolowin_logo.png"


def get_site_context():
    """ Returns a dictionary of the site context."""
    site: Site = Site.objects.get_current()
    site_context = {
        "domain": site.domain,
        "site_name": site.name,
        "logo_url": build_absolute_uri(staticfiles_storage.url(LOGO_URL)),
    }
    return site_context
