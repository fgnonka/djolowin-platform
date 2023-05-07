from enum import Enum


class AppCurrencyErrorCode(Enum):
    """This class is used to define the error codes for the app_currency app."""
    PARTIAL_PAYMENT_NOT_ALLOWED = "partial_payment_not_allowed"
    INVALID_CURRENCY = "invalid_currency"
    INVALID_AMOUNT = "invalid_amount"
    INVALID_PAYMENT_METHOD = "invalid_payment_method"
    INVALID_PAYMENT_GATEWAY = "invalid_payment_gateway"
    PAYMENT_ERROR = "payment_error"
    NOT_FOUND = "not_found"
    REQUIRED = "required"
    UNIQUE = "unique"
    GRAPHQL_ERROR = "graphql_error"
    OUT_OF_SCOPE_USER = "out_of_scope_user"
    OUT_OF_SCOPE_GROUP = "out_of_scope_group"
    OUT_OF_SCOPE_PERMISSION = "out_of_scope_permission"
    BALANCE_NOT_ENOUGH = "balance_not_enough"
    INVALID_WALLET = "invalid_wallet"
    INVALID_TRANSACTION = "invalid_transaction"