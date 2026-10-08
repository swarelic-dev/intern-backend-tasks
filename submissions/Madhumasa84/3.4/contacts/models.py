from django.db import models


class Contact(models.Model):
    """
    Contact model representing a contact record in the system.
    """
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return f"{self.name} ({self.phone})"
