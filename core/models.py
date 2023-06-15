import datetime
from typing import Any, TypeVar

import pytz
from django.contrib.postgres.indexes import GinIndex
from django.db import models, transaction
from django.db.models import F, Q, JSONField, Max

from . import JobStatus, EventDeliveryStatus

# Create your models here.


class ModelWithMetadata(models.Model):
    """An abstract model to add metadata to models."""

    metadata = JSONField(default=dict, blank=True)
    private_metadata = JSONField(default=dict, blank=True)

    class Meta:
        indexes = [
            GinIndex(fields=["private_metadata"], name="private_metadata_gin"),
            GinIndex(fields=["metadata"], name="metadata_gin"),
        ]
        abstract = True

    def get_value_from_private_metadata(self, key: str, default: Any = None) -> Any:
        return self.private_metadata.get(key, default)

    def store_value_in_private_metadata(self, items: dict):
        if not self.private_metadata:
            self.private_metadata = {}
        self.private_metadata.update(items)

    def clear_private_metadata(self):
        self.private_metadata = {}

    def delete_value_from_private_metadata(self, key: str):
        if key in self.private_metadata:
            del self.private_metadata[key]

    def get_value_from_metadata(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)

    def store_value_in_metadata(self, items: dict):
        if not self.metadata:
            self.metadata = {}
        self.metadata.update(items)

    def clear_metadata(self):
        self.metadata = {}

    def delete_value_from_metadata(self, key: str):
        if key in self.metadata:
            del self.metadata[key]


class Job(models.Model):
    status = models.CharField(
        max_length=50, choices=JobStatus.CHOICES, default=JobStatus.PENDING
    )
    message = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class EventPayload(models.Model):
    payload = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class EventDelivery(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=255,
        choices=EventDeliveryStatus.CHOICES,
        default=EventDeliveryStatus.PENDING,
    )
    event_type = models.CharField(max_length=255)
    payload = models.ForeignKey(
        EventPayload, related_name="deliveries", null=True, on_delete=models.CASCADE
    )
    # webhook = models.ForeignKey("webhook.Webhook", on_delete=models.CASCADE)

    class Meta:
        ordering = ("-created_at",)
