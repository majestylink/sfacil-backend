STATUS_CHOICES = (
    ('pending', 'pending'),
    ('processing', 'processing'),
    ('success', 'success'),
    ('error', 'error'),
    ('cancelled', 'cancelled')
)

TYPE_CHOICES = (
    ('deposit', 'deposit'),
    ('payment', 'payment'),
    ('withdrawal', 'withdrawal'),
    ('transfer', 'transfer')
)

NOTIFICATION_TYPE = (
    ('Low Stock Alert', 'Low Stock Alert'),
    ('New Order Placed', 'New Order Placed'),
    ('Product Transaction', 'Product Transaction'),
    ('Raw Material Transaction', 'Raw Material Transaction'),
    ('General Notification', 'General Notification')
)
