""""""


class JobStatus:
    """ Job status of different activities"""
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    DELETED = "deleted"

    CHOICES = (
        (PENDING, "Pending"),
        (SUCCESS, "Success"),
        (FAILED, "Failed"),
        (DELETED, "Deleted"),
    )


class TimePeriodType:
    """ Time period type for different activities"""
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"

    CHOICES = (
        (DAY, "Day"),
        (WEEK, "Week"),
        (MONTH, "Month"),
        (YEAR, "Year"),
    )


class EventDeliveryStatus:
    """ Event delivery status of different activities"""
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"

    CHOICES = (
        (PENDING, "Pending"),
        (SUCCESS, "Success"),
        (FAILED, "Failed"),
    )
