import resend
from flask import current_app


def send_order_confirmation(order, client, user):
    api_key = current_app.config.get('RESEND_API_KEY')
    if not api_key:
        return

    resend.api_key = api_key

    address_line2 = f"<p>{order.delivery_line2}</p>" if order.delivery_line2 else ""

    params = {
        'from': 'CardBranch <orders@cardbranch.co.uk>',
        'to': [user.email],
        'subject': f'Order Confirmed — {client.brand_name}',
        'html': f'''
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #333;">
            <h1 style="color: #c9a96e;">Order Confirmed</h1>
            <p>Thanks for your order. Here's a summary:</p>
            <table style="width:100%; border-collapse:collapse; margin: 16px 0;">
                <tr><td style="padding:8px 0; color:#666;">Brand</td><td><strong>{client.brand_name}</strong></td></tr>
                <tr><td style="padding:8px 0; color:#666;">Tier</td><td>{order.tier.capitalize()}</td></tr>
                <tr><td style="padding:8px 0; color:#666;">Quantity</td><td>{order.quantity} cards</td></tr>
                <tr><td style="padding:8px 0; color:#666;">Amount paid</td><td>£{order.amount_paid:.2f}</td></tr>
            </table>
            <h3 style="color:#c9a96e;">Delivery address</h3>
            <p>{order.delivery_name}</p>
            <p>{order.delivery_line1}</p>
            {address_line2}
            <p>{order.delivery_city}</p>
            <p>{order.delivery_postcode}</p>
            <p style="margin-top:24px; color:#666;">We'll be in touch when your cards are on their way.</p>
        </div>
        ''',
    }

    try:
        resend.Emails.send(params)
    except Exception:
        pass


def send_admin_notification(order, client, user):
    api_key = current_app.config.get('RESEND_API_KEY')
    if not api_key:
        return

    resend.api_key = api_key

    import os
    r2_url = os.environ.get('R2_PUBLIC_URL', '').rstrip('/')
    pdf_url = f"{r2_url}/generated/{client.slug}/card.pdf"
    address_line2 = f"<p>{order.delivery_line2}</p>" if order.delivery_line2 else ""

    params = {
        'from': 'CardBranch <orders@cardbranch.co.uk>',
        'to': ['admin@cardbranch.co.uk'],
        'subject': f'New Order #{order.id} — {client.brand_name} ({order.tier.capitalize()})',
        'html': f'''
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #333;">
            <h1 style="color: #c9a96e;">New Order Received</h1>
            <table style="width:100%; border-collapse:collapse; margin: 16px 0;">
                <tr><td style="padding:8px 0; color:#666;">Order ID</td><td><strong>#{order.id}</strong></td></tr>
                <tr><td style="padding:8px 0; color:#666;">Customer</td><td>{user.email}</td></tr>
                <tr><td style="padding:8px 0; color:#666;">Brand</td><td>{client.brand_name}</td></tr>
                <tr><td style="padding:8px 0; color:#666;">Tier</td><td>{order.tier.capitalize()}</td></tr>
                <tr><td style="padding:8px 0; color:#666;">Quantity</td><td>{order.quantity} cards</td></tr>
                <tr><td style="padding:8px 0; color:#666;">Amount paid</td><td>£{order.amount_paid:.2f}</td></tr>
            </table>
            <h3 style="color:#c9a96e;">Delivery address</h3>
            <p>{order.delivery_name}</p>
            <p>{order.delivery_line1}</p>
            {address_line2}
            <p>{order.delivery_city}</p>
            <p>{order.delivery_postcode}</p>
            <h3 style="color:#c9a96e;">Card PDF</h3>
            <p><a href="{pdf_url}" style="color:#c9a96e;">{pdf_url}</a></p>
            <p style="color:#666; font-size:13px;">Log into Solopress, upload the PDF above, enter the delivery address, and place the order. Then update the order status in the admin panel.</p>
        </div>
        ''',
    }

    try:
        resend.Emails.send(params)
    except Exception:
        pass


def send_status_update(order, client, user):
    api_key = current_app.config.get('RESEND_API_KEY')
    if not api_key:
        return

    resend.api_key = api_key

    tracking_row = ""
    if order.tracking_number:
        tracking_row = f"<tr><td style='padding:8px 0; color:#666;'>Tracking</td><td><strong>{order.tracking_number}</strong></td></tr>"

    params = {
        'from': 'CardBranch <orders@cardbranch.co.uk>',
        'to': [user.email],
        'subject': f'Your order has been updated — {client.brand_name}',
        'html': f'''
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #333;">
            <h1 style="color: #c9a96e;">Order Update</h1>
            <p>Your order for <strong>{client.brand_name}</strong> has been updated.</p>
            <table style="width:100%; border-collapse:collapse; margin: 16px 0;">
                <tr><td style="padding:8px 0; color:#666;">Order ID</td><td><strong>#{order.id}</strong></td></tr>
                <tr><td style="padding:8px 0; color:#666;">Status</td><td><strong>{order.status.capitalize()}</strong></td></tr>
                <tr><td style="padding:8px 0; color:#666;">Order date</td><td>{order.created_at.strftime("%d %b %Y")}</td></tr>
                {tracking_row}
            </table>
            <p style="margin-top:24px; color:#666;">If you have any questions, reply to this email.</p>
        </div>
        ''',
    }

    try:
        resend.Emails.send(params)
    except Exception:
        pass
