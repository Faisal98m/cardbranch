import resend
from flask import current_app


def send_order_confirmation(email, brand_name, quantity, amount_paid, tracking_url=''):
    api_key = current_app.config.get('RESEND_API_KEY')
    if not api_key:
        return

    resend.api_key = api_key

    params = {
        'from': 'CardBranch <orders@cardbranch.co.uk>',
        'to': [email],
        'subject': f'Order Confirmed - {brand_name}',
        'html': f'''
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h1 style="color: #c9a96e;">Order Confirmed</h1>
            <p>Thank you for your order from <strong>{brand_name}</strong>.</p>
            <p><strong>Quantity:</strong> {quantity}</p>
            <p><strong>Amount Paid:</strong> £{amount_paid:.2f}</p>
            <p>We'll notify you when your cards are dispatched.</p>
        </div>
        ''',
    }

    try:
        resend.Emails.send(params)
    except Exception:
        pass
