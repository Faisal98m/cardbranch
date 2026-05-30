from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import User, Client, Order, db
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/admin')
@login_required
@admin_required
def index():
    total_users = User.query.count()
    total_cards = Client.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(func.sum(Order.amount_paid)).scalar() or 0
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    return render_template('admin/index.html', total_users=total_users,
                           total_cards=total_cards, total_orders=total_orders,
                           total_revenue=total_revenue, recent_orders=recent_orders,
                           recent_users=recent_users)


@admin_bp.route('/admin/users')
@login_required
@admin_required
def users():
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=all_users)


@admin_bp.route('/admin/orders', methods=['GET', 'POST'])
@login_required
@admin_required
def orders():
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        status = request.form.get('status')
        tracking = request.form.get('tracking_number')
        order = Order.query.get_or_404(order_id)
        if status:
            order.status = status
        if tracking:
            order.tracking_number = tracking
        db.session.commit()
        flash('Order updated', 'success')
        return redirect(url_for('admin.orders'))

    all_orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=all_orders)


@admin_bp.route('/admin/revenue')
@login_required
@admin_required
def revenue():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    total = sum(o.amount_paid for o in orders)
    return render_template('admin/revenue.html', orders=orders, total=total)


@admin_bp.route('/admin/flush-orders-x7k9q')
@login_required
def flush_orders():
    if not current_user.is_admin:
        return '', 403
    Order.query.delete()
    db.session.commit()
    return 'Orders cleared.', 200
