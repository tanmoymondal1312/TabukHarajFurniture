def inbox_unread(request):
    """Unread contact-message count for the dashboard sidebar badge."""
    if not request.path.startswith("/dashboard"):
        return {}

    from pages.models import ContactMessage

    return {"inbox_unread": ContactMessage.objects.filter(is_read=False).count()}
