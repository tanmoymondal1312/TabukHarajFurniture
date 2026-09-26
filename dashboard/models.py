from django.db import models


class VisitorLog(models.Model):
    DEVICE_DESKTOP = "desktop"
    DEVICE_MOBILE = "mobile"
    DEVICE_TABLET = "tablet"
    DEVICE_CHOICES = (
        (DEVICE_DESKTOP, "Desktop"),
        (DEVICE_MOBILE, "Mobile"),
        (DEVICE_TABLET, "Tablet"),
    )

    path = models.CharField("Page", max_length=300, db_index=True)
    visitor_key = models.CharField("Visitor", max_length=40, db_index=True)
    referrer = models.CharField("Referrer", max_length=200, blank=True)
    device = models.CharField(
        "Device", max_length=10, choices=DEVICE_CHOICES, default=DEVICE_DESKTOP
    )
    created_at = models.DateTimeField("Time", db_index=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Visitor log"
        verbose_name_plural = "Visitor logs"
        indexes = [models.Index(fields=["created_at", "path"])]

    def __str__(self):
        return f"{self.path} — {self.created_at:%Y-%m-%d %H:%M}"

    @property
    def short_key(self):
        return f"v-{self.visitor_key[:8]}"
