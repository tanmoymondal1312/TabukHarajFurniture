def inbox_unread(request):
    """Unread counts for the dashboard sidebar badges (messages + orders)."""
    if not request.path.startswith("/dashboard"):
        return {}

    from pages.models import ContactMessage

    unread = ContactMessage.objects.filter(is_read=False)
    return {
        "inbox_unread": unread.filter(kind="message").count(),
        "orders_unread": unread.filter(kind="order").count(),
    }
