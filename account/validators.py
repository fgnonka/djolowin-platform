import re
import unicodedata

from confusable_homoglyphs import confusables
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from phonenumber_field.phonenumber import to_python
from phonenumbers.phonenumberutil import is_possible_number

from .error_codes import AccountErrorCode




def validate_confusables(value):
    """
    Validator which disallows 'dangerous' usernames likely to
    represent homograph attacks.
    A username is 'dangerous' if it is mixed-script (as defined by
    Unicode 'Script' property) and contains one or more characters
    appearing in the Unicode Visually Confusable Characters file.
    """
    if not isinstance(value, str):
        return
    if confusables.is_dangerous(value):
        raise ValidationError(CONFUSABLE, code="invalid")


def validate_possible_number(phone, country=None):
    phone_number = to_python(phone, country)
    if (
        phone_number
        and not is_possible_number(phone_number)
        or not phone_number.is_valid()
    ):
        raise ValidationError(
            "The phone number entered is not valid.", code=AccountErrorCode.INVALID
        )
    return phone_number


def validate_confusables_email(value):
    """
    Validator which disallows 'dangerous' email addresses likely to
    represent homograph attacks.
    An email address is 'dangerous' if either the local-part or the
    domain, considered on their own, are mixed-script and contain one
    or more characters appearing in the Unicode Visually Confusable
    Characters file.
    """
    if value.count("@") != 1:
        return
    local_part, domain = value.split("@")
    if confusables.is_dangerous(local_part) or confusables.is_dangerous(domain):
        raise ValidationError(CONFUSABLE_EMAIL, code="invalid")


CONFUSABLE = _("This name cannot be registered. Please choose a different name.")
CONFUSABLE_EMAIL = _(
    "This email address cannot be registered. Please supply a different email address."
)
DUPLICATE_EMAIL = _(
    "This email address is already in use. Please supply a different email address."
)
DUPLICATE_USERNAME = _("A user with that username already exists.")
FREE_EMAIL = _(
    "Registration using free email addresses is prohibited. Please supply a different email address."
)
RESERVED_NAME = _("This name is reserved and cannot be registered.")
TOS_REQUIRED = _("You must agree to the terms to register")

# WHATWG HTML5 spec, section 4.10.5.1.5.
HTML5_EMAIL_RE = (
    r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]"
    r"+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}"
    r"[a-zA-Z0-9])?(?:\.[a-zA-Z0-9]"
    r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
)

# Below we construct a large but non-exhaustive list of names which
# users probably should not be able to register with, due to various
# risks:
#
# * For a site which creates email addresses from username, important
#   common addresses must be reserved.
#
# * For a site which creates subdomains from usernames, important
#   common hostnames/domain names must be reserved.
#
# * For a site which uses the username to generate a URL to the user's
#   profile, common well-known filenames must be reserved.
#
# etc., etc.
#
# Credit for basic idea and most of the list to Geoffrey Thomas's blog
# post about names to reserve:
# https://ldpreload.com/blog/names-to-reserve

SPECIAL_HOSTNAMES = [
    # Hostnames with special/reserved meaning.
    "autoconfig",  # Thunderbird autoconfig
    "autodiscover",  # MS Outlook/Exchange autoconfig
    "broadcasthost",  # Network broadcast hostname
    "isatap",  # IPv6 tunnel autodiscovery
    "localdomain",  # Loopback
    "localhost",  # Loopback
    "wpad",  # Proxy autodiscovery
]

PROTOCOL_HOSTNAMES = [
    # Common protocol hostnames.
    "ftp",
    "imap",
    "mail",
    "news",
    "pop",
    "pop3",
    "smtp",
    "usenet",
    "uucp",
    "webmail",
    "www",
]

CA_ADDRESSES = [
    # Email addresses known used by certificate authorities during
    # verification.
    "admin",
    "administrator",
    "hostmaster",
    "djolowin",  # Our App
    "account",
    "info",
    "is",
    "it",
    "mis",
    "postmaster",
    "root",
    "ssladmin",
    "ssladministrator",
    "sslwebmaster",
    "sysadmin",
    "webmaster",
]

RFC_2142 = [
    # RFC-2142-defined names not already covered.
    "abuse",
    "marketing",
    "noc",
    "sales",
    "security",
    "support",
]

NOREPLY_ADDRESSES = [
    # Common no-reply email addresses.
    "mailer-daemon",
    "nobody",
    "noreply",
    "no-reply",
]


SENSITIVE_FILENAMES = [
    # Sensitive filenames.
    "clientaccesspolicy.xml",  # Silverlight cross-domain policy file.
    "crossdomain.xml",  # Flash cross-domain policy file.
    "favicon.ico",
    "humans.txt",
    "keybase.txt",  # Keybase ownership-verification URL.
    "robots.txt",
    ".htaccess",
    ".htpasswd",
]

OTHER_SENSITIVE_NAMES = [
    # Other names which could be problems depending on URL/subdomain
    # structure.
    "0",
    "100",
    "101",
    "102",
    "1xx",
    "200",
    "201",
    "202",
    "203",
    "204",
    "205",
    "206",
    "207",
    "226",
    "2xx",
    "300",
    "301",
    "302",
    "303",
    "304",
    "305",
    "307",
    "308",
    "3xx",
    "400",
    "401",
    "402",
    "403",
    "404",
    "405",
    "406",
    "407",
    "408",
    "409",
    "410",
    "411",
    "412",
    "413",
    "414",
    "415",
    "416",
    "417",
    "418",
    "422",
    "423",
    "424",
    "426",
    "428",
    "429",
    "431",
    "451",
    "4xx",
    "500",
    "501",
    "502",
    "503",
    "504",
    "505",
    "506",
    "507",
    "511",
    "5xx",
    "7xx",
    "account",
    "accounts",
    "activate",
    "activities",
    "activity",
    "ad",
    "add",
    "address",
    "adm",
    "admin",
    "administration",
    "administrator",
    "ads",
    "advertising",
    "affiliate",
    "affiliates",
    "all",
    "analysis",
    "analytics",
    "anon",
    "anonymous",
    "api",
    "app",
    "apps",
    "archive",
    "archives",
    "asset",
    "auth",
    "authentication",
    "autoconfig",
    "avatar",
    "auth",
    "authorize",
    "backup",
    "bank",
    "beta",
    "billing",
    "bin",
    "blog",
    "blogs",
    "board",
    "bot",
    "bots",
    "broadcasthost",
    "bug",
    "bugs",
    "buy",
    "cache",
    "call",
    "cancel",
    "captcha",
    "career",
    "careers",
    "cart",
    "categories",
    "category",
    "cgi",
    "cgi-bin",
    "changelog",
    "chat",
    "check",
    "checking",
    "checkout",
    "client",
    "clients",
    "code",
    "comment",
    "comments",
    "communities",
    "community",
    "company",
    "config",
    "configuration",
    "connect",
    "contact",
    "contact-us",
    "contact_us",
    "contactus",
    "contribute",
    "corp",
    "create",
    "crypt",
    "css",
    "copyright",
    "dashboard",
    "data",
    "db",
    "default",
    "delete",
    "demo",
    "destroy",
    "dev",
    "devel",
    "developer",
    "developers",
    "die",
    "dir",
    "directory",
    "dist",
    "dns",
    "doc",
    "docker",
    "docs",
    "documentation",
    "download",
    "downloads",
    "edit",
    "editor",
    "email",
    "employment",
    "empty",
    "end",
    "enterprise",
    "entries",
    "entry",
    "error",
    "errors",
    "eval",
    "event",
    "exit",
    "explore",
    "export",
    "faq",
    "favorite",
    "favorites",
    "fbi",
    "feature",
    "features",
    "feed",
    "feedback",
    "feeds",
    "file",
    "files",
    "firewall",
    "first",
    "follow",
    "followers",
    "following",
    "forgot",
    "forgot-password",
    "forgot_password",
    "forgotpassword",
    "form",
    "forum",
    "forums",
    "free",
    "friend",
    "friends",
    "ftp",
    "get",
    "gift",
    "gifts",
    "gist",
    "git",
    "graph",
    "group",
    "groups",
    "guest",
    "guests",
    "help",
    "home",
    "homepage",
    "hooks",
    "host",
    "hosting",
    "hostmaster",
    "hostname",
    "howto",
    "html",
    "http",
    "httpd",
    "https",
    "i",
    "id",
    "image",
    "images",
    "imap",
    "img",
    "index",
    "info",
    "information",
    "inquiry",
    "intranet",
    "invitations",
    "invite",
    "ip",
    "irc",
    "is",
    "isatap",
    "issue",
    "issues",
    "it",
    "item",
    "items",
    "java",
    "javascript",
    "job",
    "jobs",
    "join",
    "js",
    "json",
    "keys",
    "keyserver",
    "knowledgebase",
    "language",
    "languages",
    "last",
    "legal",
    "license",
    "link",
    "links",
    "list",
    "lists",
    "local",
    "localdomain",
    "localhost",
    "log",
    "log-in",
    "log-out",
    "log_in",
    "log_out",
    "login",
    "logout",
    "logs",
    "m",
    "mail",
    "mail1",
    "mail2",
    "mail3",
    "mail4",
    "mail5",
    "mailer",
    "mailer-daemon",
    "mailing",
    "maintenance",
    "manager",
    "manual",
    "map",
    "maps",
    "marketing",
    "master",
    "me",
    "media",
    "member",
    "members",
    "message",
    "messages",
    "mis",
    "mob",
    "mobile",
    "movie",
    "movies",
    "msg",
    "music",
    "mx",
    "my",
    "name",
    "named",
    "names",
    "namespace",
    "namespaces",
    "nan",
    "navi",
    "navigation",
    "net",
    "network",
    "new",
    "news",
    "newsletter",
    "nick",
    "nickname",
    "noc",
    "notes",
    "notification",
    "notifications",
    "notify",
    "ns",
    "ns1",
    "ns10",
    "ns2",
    "ns3",
    "ns4",
    "ns5",
    "ns6",
    "ns7",
    "ns8",
    "ns9",
    "null",
    "oauth",
    "pay",
    "payment",
    "payments",
    "plans",
    "portfolio",
    "preferences",
    "pricing",
    "privacy",
    "profile",
    "register",
    "secure",
    "settings",
    "signin",
    "signup",
    "ssl",
    "status",
    "store",
    "subscribe",
    "terms",
    "tos",
    "user",
    "users",
    "weblog",
    "work",
]

DEFAULT_RESERVED_NAMES = (
    SPECIAL_HOSTNAMES
    + PROTOCOL_HOSTNAMES
    + CA_ADDRESSES
    + RFC_2142
    + NOREPLY_ADDRESSES
    + SENSITIVE_FILENAMES
    + OTHER_SENSITIVE_NAMES
)