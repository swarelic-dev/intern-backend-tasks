from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contact model with field-level phone validation.
    """
    class Meta:
        model = Contact
        fields = ['id', 'name', 'phone', 'email', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_phone(self, value):
        """
        Validate that the phone number contains exactly 10 numeric digits.
        """
        cleaned_value = value.strip()
        if not cleaned_value.isdigit() or len(cleaned_value) != 10:
            raise serializers.ValidationError("Phone number must be exactly 10 digits.")
        return cleaned_value
