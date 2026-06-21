# UI Codebase Audit - CardBranch Dashboard
# =========================================
# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
# Description: Complete inventory of templates, routes, CSS, and JavaScript


## 1. Template File Contents

### templates/layouts/base.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}CardBranch{% endblock %}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@300;400;500;600;700&family=Playfair+Display+SC:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">
    <style>
        :root {
            --bg-primary: #f0ebe4;
            --bg-secondary: #faf8f4;
            --bg-card: #faf8f4;
            --bg-elevated: #ffffff;
            --accent: #6b1f2a;
            --accent-hover: #7c2535;
            --accent-subtle: #f0dde0;
            --accent-border: #d4b0b5;
            --text-primary: #1a1714;
            --text-secondary: #8a7e72;
            --text-dim: #b0a496;
            --border: #d8d0c4;
            --border-light: #e8e2d8;
            --success: #3b6d11;
            --warning: #92600a;
            --danger: #ef4444;
            --radius: 8px;
            --radius-sm: 4px;
            --radius-lg: 8px;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html { overflow-x: hidden; }
        body { font-family: 'Inter', sans-serif; background: var(--bg-primary); color: var(--text-primary); min-height: 100vh; overflow-x: hidden; }
        h1, h2 { font-family: 'DM Serif Display', serif; font-weight: 400; }
        h1 { font-weight: 400; }
        h2 { font-weight: 400; }
        a { color: inherit; text-decoration: none; }
        a:hover { opacity: 0.8; }
        img { max-width: 100%; }
        input, textarea, select { font-family: 'Inter', sans-serif; background: #ffffff; border: 1px solid #d8d0c4; color: #1a1714; padding: 10px 14px; border-radius: var(--radius-sm); font-size: 14px; width: 100%; outline: none; transition: border-color 0.15s; }
        input:focus, textarea:focus, select:focus { border-color: #6b1f2a; }
        input::placeholder, textarea::placeholder { color: #b0a496; }
        label { font-size: 13px; font-weight: 500; color: var(--text-secondary); margin-bottom: 6px; display: block; }
        table { width: 100%; border-collapse: collapse; }
        th { font-size: 11px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.10em; text-align: left; padding: 12px 8px; border-bottom: 1px solid #d8d0c4; }
        td { padding: 12px 8px; font-size: 14px; color: var(--text-primary); border-bottom: 1px solid #d8d0c4; }
        tr:last-child td { border-bottom: none; }
        *:focus-visible { outline: 2px solid #6b1f2a; outline-offset: 2px; }
        .flash { padding: 12px 20px; margin-bottom: 16px; border-radius: 6px; font-size: 14px; }
        .flash.error { background: rgba(239, 68, 68, 0.08); color: var(--danger); border: 1px solid rgba(239, 68, 68, 0.3); }
        .flash.success { background: #eaf3de; color: var(--success); border: 1px solid #b8d89a; }
        .btn { display: inline-flex; align-items: center; justify-content: center; padding: 10px 24px; border-radius: var(--radius-sm); font-weight: 500; font-size: 14px; cursor: pointer; border: none; transition: all 0.15s; font-family: 'Inter', sans-serif; }
        .btn:hover { opacity: 0.9; }
        .btn-primary { background: #6b1f2a; color: #faf8f4; font-weight: 600; box-shadow: 0 2px 8px rgba(107,31,42,0.35); }
        .btn-primary:hover { background: #7c2535; }
        .btn-ghost { background: transparent; border: 1.5px solid #6b1f2a; color: #6b1f2a; font-weight: 500; }
        .btn-ghost:hover { background: #f0dde0; }
        .btn-ghost-danger { background: transparent; border: 1.5px solid var(--danger); color: var(--danger); }
        .btn-ghost-danger:hover { background: rgba(239, 68, 68, 0.08); }
        .btn-sm { padding: 7px 14px; font-size: 11px; }
        .status-pill { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; border: 1px solid transparent; }
        .status-pending { background: #fdf3e3; color: #92600a; border-color: #f0d090; }
        .status-sent_to_print { background: #f0dde0; color: #6b1f2a; border-color: #d4b0b5; }
        .status-dispatched { background: #f0dde0; color: #6b1f2a; border-color: #d4b0b5; }
        .status-delivered { background: #eaf3de; color: #3b6d11; border-color: #b8d89a; }
        .status-paid { background: #eaf3de; color: #3b6d11; border-color: #b8d89a; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
        @media (max-width: 768px) {
            .container { padding: 0 16px !important; }
            main { padding-left: 0 !important; padding-right: 0 !important; }
        }
        .page-title { font-size: 24px; font-weight: 400; color: var(--text-primary); margin-bottom: 24px; font-family: 'DM Serif Display', serif; }
        .section-label { font-family: 'Inter', sans-serif; font-weight: 700; font-size: 9px; text-transform: uppercase; letter-spacing: 0.10em; color: #b0a496; }
        .stat-value { font-family: 'DM Serif Display', serif; font-size: 24px; color: #6b1f2a; }
        .badge { display: inline-block; padding: 3px 8px; background: #f0dde0; border: 1px solid #d4b0b5; color: #6b1f2a; font-weight: 700; font-size: 9px; text-transform: uppercase; letter-spacing: 0.07em; border-radius: 4px; }
        .avatar { width: 34px; height: 34px; border-radius: 50%; background: #f0dde0; border: 1.5px solid #6b1f2a; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 700; color: #6b1f2a; flex-shrink: 0; }
        .avatar-img { width: 34px; height: 34px; border-radius: 50%; object-fit: cover; border: 1.5px solid #6b1f2a; }
        .card-stripe { border: 1px solid #d8d0c4; border-top: 4px solid #6b1f2a; border-radius: var(--radius-lg); box-shadow: 0 3px 12px rgba(107,31,42,0.08), 0 1px 3px rgba(0,0,0,0.04); background: var(--bg-card); }
        .card-stripe:hover { border-color: #6b1f2a; }
        .order-row { background: var(--bg-card); border: 1px solid #d8d0c4; border-radius: 6px; box-shadow: 0 1px 4px rgba(0,0,0,0.04); padding: 8px 10px; }
        .order-icon { display: inline-flex; align-items: center; justify-content: center; width: 28px; height: 28px; background: #f0dde0; color: #6b1f2a; border-radius: 5px; flex-shrink: 0; }
    </style>
    {% block extra_head %}{% endblock %}
</head>
<body>
<main>
    {% block content %}{% endblock %}
</main>
</body>
</html>

```
### templates/layouts/dashboard.html
```html
{% extends "layouts/base.html" %}
{% block title %}Dashboard - CardBranch{% endblock %}
{% block content %}
{% set current = request.endpoint %}

<header class="mobile-header">
  <span style="font-size:16px; font-weight:400; font-family:'DM Serif Display',serif; color:#faf8f4;">CardBranch</span>
</header>

<div style="display:flex; min-height:100vh;">
    <aside class="sidebar" style="width:240px; background:var(--bg-secondary); border-right:1px solid var(--border); display:flex; flex-direction:column; flex-shrink:0;">
        <div style="height:64px; display:flex; align-items:center; padding:0 20px; background:#6b1f2a;">
            <a href="{{ url_for('dashboard.index') }}" style="font-size:18px; font-weight:400; font-family:'DM Serif Display',serif; color:#faf8f4;">CardBranch</a>
        </div>
        <nav style="flex:1; padding:16px 12px; display:flex; flex-direction:column; gap:2px;">
            <a href="{{ url_for('dashboard.index') }}" class="sidebar-item">
                <span style="display:flex; align-items:center; gap:10px;">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
                    My Cards
                </span>
            </a>
            <a href="{{ url_for('dashboard.card_new') }}" class="sidebar-item">
                <span style="display:flex; align-items:center; gap:10px;">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><path d="M12 5v14M5 12h14"/></svg>
                    New Card
                </span>
            </a>
            <a href="{{ url_for('dashboard.orders') }}" class="sidebar-item">
                <span style="display:flex; align-items:center; gap:10px;">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
                    Orders
                </span>
            </a>
            <div style="border-top:1px solid var(--border); margin:12px 0; padding-top:12px;">
                <span class="section-label" style="padding:0 4px;">Admin</span>
            </div>
            <a href="{{ url_for('admin.index') }}" class="sidebar-item">
                <span style="display:flex; align-items:center; gap:10px;">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                    Overview
                </span>
                <span class="badge">Admin</span>
            </a>
        </nav>
        <div style="padding:16px 12px; border-top:1px solid var(--border);">
            <a href="{{ url_for('auth.logout') }}" class="sidebar-item">
                <span style="display:flex; align-items:center; gap:10px;">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
                    Sign out
                </span>
            </a>
        </div>
    </aside>
    <div class="main-content" style="flex:1; padding:32px; background:var(--bg-primary);">
        {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
        {% for category, message in messages %}
        <div class="flash {{ category }}">{{ message }}</div>
        {% endfor %}
        {% endif %}
        {% endwith %}
        {% block dashboard_content %}{% endblock %}
    </div>
</div>

<nav class="mobile-nav" aria-label="Mobile navigation">
  <a href="{{ url_for('dashboard.index') }}" class="mobile-nav-item {% if current == 'dashboard.index' %}active{% endif %}">
    <i class="ti ti-layout-grid" aria-hidden="true"></i>
    <span>My Cards</span>
  </a>
  <a href="{{ url_for('dashboard.card_new') }}" class="mobile-nav-item {% if current == 'dashboard.card_new' %}active{% endif %}">
    <i class="ti ti-plus" aria-hidden="true"></i>
    <span>New Card</span>
  </a>
  <a href="{{ url_for('dashboard.orders') }}" class="mobile-nav-item {% if current == 'dashboard.orders' %}active{% endif %}">
    <i class="ti ti-shopping-bag" aria-hidden="true"></i>
    <span>Orders</span>
  </a>
  {% if current_user.is_admin %}
  <a href="{{ url_for('admin.index') }}" class="mobile-nav-item {% if current == 'admin.index' %}active{% endif %}">
    <i class="ti ti-shield" aria-hidden="true"></i>
    <span>Admin</span>
  </a>
  {% endif %}
  <a href="{{ url_for('auth.logout') }}" class="mobile-nav-item">
    <i class="ti ti-logout" aria-hidden="true"></i>
    <span>Sign Out</span>
  </a>
</nav>

<style>
    .sidebar-item { display:flex; align-items:center; justify-content:space-between; padding:10px 16px; border-radius:var(--radius-sm); font-size:14px; color:#8a7e72; transition:all 0.15s; }
    .sidebar-item:hover { background:#f0dde0; color:#6b1f2a; }
    .mobile-nav { display:none; position:fixed; bottom:0; left:0; right:0; height:60px; background:#6b1f2a; flex-direction:row; align-items:center; justify-content:space-around; z-index:100; padding-bottom:env(safe-area-inset-bottom); }
    .mobile-nav-item { display:flex; flex-direction:column; align-items:center; gap:3px; color:rgba(250,248,244,0.55); text-decoration:none; font-size:11px; padding:8px 16px; font-family:'Inter',sans-serif; font-weight:400; }
    .mobile-nav-item i { font-size:20px; }
    .mobile-nav-item:hover, .mobile-nav-item.active { color:#faf8f4; font-weight:500; border-bottom:2px solid #faf8f4; margin-bottom:-2px; }
    .mobile-header { display:none; padding:14px 16px; background:#6b1f2a; position:sticky; top:0; width:100%; z-index:99; }
    @media (max-width: 768px) {
        .sidebar { display: none !important; }
        .main-content { margin-left: 0 !important; width: 100% !important; padding-bottom: 72px !important; }
        .mobile-nav { display:flex; }
        .mobile-header { display:flex; align-items:center; }
    }
</style>
{% endblock %}

```

### templates/layouts/admin.html
```html
{% extends "layouts/base.html" %}
{% block title %}Admin - CardBranch{% endblock %}
{% block content %}
<div style="display:flex; min-height:100vh;">
    <aside class="sidebar" style="width:240px; background:var(--bg-secondary); border-right:1px solid var(--border); display:flex; flex-direction:column; flex-shrink:0;">
        <div style="height:64px; display:flex; align-items:center; padding:0 20px; background:#6b1f2a;">
            <a href="{{ url_for('admin.index') }}" style="font-size:16px; font-weight:400; font-family:'DM Serif Display',serif; color:#faf8f4;">CardBranch Admin</a>
        </div>
        <nav style="flex:1; padding:16px 12px; display:flex; flex-direction:column; gap:2px;">
            <a href="{{ url_for('admin.index') }}" class="sidebar-item">
                <span style="display:flex; align-items:center; gap:10px;">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                    Overview
                </span>
            </a>
            <a href="{{ url_for('admin.users') }}" class="sidebar-item">
                <span style="display:flex; align-items:center; gap:10px;">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                    Users
                </span>
            </a>
            <a href="{{ url_for('admin.orders') }}" class="sidebar-item">
                <span style="display:flex; align-items:center; gap:10px;">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
                    Orders
                </span>
            </a>
            <a href="{{ url_for('admin.revenue') }}" class="sidebar-item">
                <span style="display:flex; align-items:center; gap:10px;">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
                    Revenue
                </span>
            </a>
            <div style="border-top:1px solid var(--border); margin:12px 0; padding-top:12px;"></div>
            <a href="{{ url_for('dashboard.index') }}" class="sidebar-item">
                <span style="display:flex; align-items:center; gap:10px;">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
                    Dashboard
                </span>
            </a>
        </nav>
        <div style="padding:16px 12px; border-top:1px solid var(--border);">
            <a href="{{ url_for('auth.logout') }}" class="sidebar-item">
                <span style="display:flex; align-items:center; gap:10px;">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
                    Sign out
                </span>
            </a>
        </div>
    </aside>
    <div class="main-content" style="flex:1; padding:32px; background:var(--bg-primary);">
        {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
        {% for category, message in messages %}
        <div class="flash {{ category }}">{{ message }}</div>
        {% endfor %}
        {% endif %}
        {% endwith %}
        {% block admin_content %}{% endblock %}
    </div>
</div>
<nav class="admin-mobile-nav" aria-label="Admin mobile navigation">
  <a href="{{ url_for('admin.index') }}" class="admin-mobile-nav-item">
    <i class="ti ti-shield" aria-hidden="true"></i>
    <span>Overview</span>
  </a>
  <a href="{{ url_for('admin.users') }}" class="admin-mobile-nav-item">
    <i class="ti ti-users" aria-hidden="true"></i>
    <span>Users</span>
  </a>
  <a href="{{ url_for('admin.orders') }}" class="admin-mobile-nav-item">
    <i class="ti ti-shopping-bag" aria-hidden="true"></i>
    <span>Orders</span>
  </a>
  <a href="{{ url_for('admin.revenue') }}" class="admin-mobile-nav-item">
    <i class="ti ti-currency-pound" aria-hidden="true"></i>
    <span>Revenue</span>
  </a>
  <a href="{{ url_for('dashboard.index') }}" class="admin-mobile-nav-item">
    <i class="ti ti-layout-grid" aria-hidden="true"></i>
    <span>Dashboard</span>
  </a>
</nav>
<style>
    .sidebar-item { display:flex; align-items:center; justify-content:space-between; padding:10px 16px; border-radius:var(--radius-sm); font-size:14px; color:#8a7e72; transition:all 0.15s; }
    .sidebar-item:hover { background:#f0dde0; color:#6b1f2a; }
    .admin-mobile-nav { display:none; position:fixed; bottom:0; left:0; right:0; height:60px; background:#6b1f2a; flex-direction:row; align-items:center; justify-content:space-around; z-index:100; padding-bottom:env(safe-area-inset-bottom); }
    .admin-mobile-nav-item { display:flex; flex-direction:column; align-items:center; gap:3px; color:rgba(250,248,244,0.55); text-decoration:none; font-size:10px; padding:8px 8px; font-family:'Inter',sans-serif; font-weight:400; }
    .admin-mobile-nav-item i { font-size:20px; }
    .admin-mobile-nav-item:hover, .admin-mobile-nav-item.active { color:#faf8f4; font-weight:500; }
    @media (max-width: 768px) {
        .sidebar { display: none !important; }
        .main-content { margin-left: 0 !important; width: 100% !important; padding: 16px !important; padding-bottom: 72px !important; box-sizing: border-box; }
        .admin-mobile-nav { display:flex; }
    }
</style>
{% endblock %}

```

### templates/public/index.html
```html
{% extends "layouts/base.html" %}
{% block title %}CardBranch - Premium Business Cards{% endblock %}
{% block content %}
<nav style="background:#6b1f2a; width:100%; margin:0; padding:0; height:64px; display:flex; align-items:center;">
    <div style="flex:1; display:flex; align-items:center; justify-content:space-between; max-width:1200px; margin:0 auto; padding:0 48px;">
        <span style="font-size:18px; font-weight:400; font-family:'DM Serif Display',serif; color:#faf8f4;">CardBranch</span>
        <div class="nav-buttons" style="display:flex; gap:12px; align-items:center;">
            <a href="{{ url_for('auth.login') }}" style="font-family:'Inter',sans-serif; font-size:12px; color:rgba(250,248,244,0.55); text-decoration:none; padding:6px 16px; border-radius:4px; border:1.5px solid rgba(250,248,244,0.3);">Sign In</a>
            <a href="{{ url_for('auth.register') }}" class="btn btn-primary" style="padding:8px 20px; font-size:13px;">Get Started</a>
        </div>
    </div>
</nav>

<section class="hero" style="padding:120px 24px 80px; text-align:center; background:#faf8f4; border-bottom:1px solid #d8d0c4;">
    <div style="max-width:680px; margin:0 auto;">
        <h1 style="font-size:48px; font-weight:400; line-height:1.2; color:var(--text-primary); margin-bottom:20px;">Your brand, one scan away</h1>
        <p style="font-size:18px; color:var(--text-secondary); max-width:520px; margin:0 auto 32px; line-height:1.6;">Create a digital business card with a hosted links page, QR code, and print-ready PDF. Order premium physical cards delivered to your door.</p>
        <div style="display:flex; gap:12px; justify-content:center; flex-wrap:wrap;">
            <a href="{{ url_for('auth.register') }}" class="btn btn-primary" style="padding:12px 28px; font-size:15px;">Create your card</a>
            <a href="#example" class="btn btn-ghost" style="padding:12px 28px; font-size:15px;">See example</a>
        </div>
    </div>
</section>

<section id="example" style="padding:80px 24px; border-top:1px solid var(--border); background:#faf8f4;">
  <div style="max-width:1100px; margin:0 auto;">

    <div style="text-align:center; margin-bottom:64px;">
      <p style="font-size:11px; letter-spacing:0.12em; color:var(--text-secondary); text-transform:uppercase; margin-bottom:8px; font-family:'Inter',sans-serif;">See what you get</p>
      <h2 style="font-size:32px; font-weight:400; color:var(--text-primary); font-family:'DM Serif Display',serif; margin:0;">Everything in one place</h2>
    </div>

    <!-- ROW 1: Card mockup left, text right -->
    <div class="example-row" style="display:grid; grid-template-columns:1fr 1fr; gap:64px; align-items:center; margin-bottom:80px;">
      <div style="background:var(--bg-secondary); border:1px solid var(--border); border-radius:16px; padding:28px; display:flex; flex-direction:column; gap:10px;">
        <div style="font-size:10px; color:var(--text-dim); letter-spacing:0.1em; font-family:'Inter',sans-serif;">FRONT</div>
        <div style="background:#ffffff; border:0.5px solid var(--border-light); border-radius:8px; padding:14px 16px; position:relative; overflow:hidden; height:80px; display:flex; align-items:center; justify-content:space-between; box-sizing:border-box;">
          <div style="position:absolute; bottom:0; left:0; right:0; height:2px; background:#6b1f2a;"></div>
          <div>
            <div style="font-size:14px; font-weight:600; color:#1a1714; margin-bottom:3px;">Da Workforce</div>
            <div style="font-size:9px; color:#8a7e72;">Delivering Drivers to You</div>
          </div>
          <div style="width:38px; height:38px; background:var(--bg-secondary); border-radius:4px; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg viewBox="0 0 36 36" width="30" height="30" opacity="0.5">
              <rect x="2" y="2" width="10" height="10" rx="1" fill="none" stroke="#1a1714" stroke-width="1.5"/>
              <rect x="4" y="4" width="6" height="6" rx="0.5" fill="#1a1714" opacity="0.6"/>
              <rect x="24" y="2" width="10" height="10" rx="1" fill="none" stroke="#1a1714" stroke-width="1.5"/>
              <rect x="26" y="4" width="6" height="6" rx="0.5" fill="#1a1714" opacity="0.6"/>
              <rect x="2" y="24" width="10" height="10" rx="1" fill="none" stroke="#1a1714" stroke-width="1.5"/>
              <rect x="4" y="26" width="6" height="6" rx="0.5" fill="#1a1714" opacity="0.6"/>
              <rect x="16" y="16" width="18" height="2" fill="#1a1714" opacity="0.3"/>
              <rect x="16" y="20" width="14" height="2" fill="#1a1714" opacity="0.3"/>
              <rect x="16" y="24" width="18" height="2" fill="#1a1714" opacity="0.3"/>
              <rect x="16" y="28" width="10" height="2" fill="#1a1714" opacity="0.3"/>
            </svg>
          </div>
        </div>
        <div style="font-size:10px; color:var(--text-dim); letter-spacing:0.1em; margin-top:8px; font-family:'Inter',sans-serif;">BACK</div>
        <div style="background:#ffffff; border:0.5px solid var(--border-light); border-radius:8px; padding:14px 16px; position:relative; overflow:hidden; height:80px; display:flex; align-items:center; justify-content:space-between; box-sizing:border-box;">
          <div style="position:absolute; top:0; left:0; right:0; height:2px; background:#6b1f2a;"></div>
          <div>
            <div style="font-size:10px; font-weight:600; color:#6b1f2a; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:4px;">Da Workforce</div>
            <div style="font-size:9px; color:#8a7e72; margin-bottom:3px;">Delivering Drivers to You</div>
            <div style="font-size:8px; color:#b0a496;">cardbranch.co.uk/c/da-workforce</div>
          </div>
          <div style="width:46px; height:46px; background:var(--bg-secondary); border-radius:4px; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg viewBox="0 0 36 36" width="38" height="38" opacity="0.5">
              <rect x="2" y="2" width="10" height="10" rx="1" fill="none" stroke="#1a1714" stroke-width="1.5"/>
              <rect x="4" y="4" width="6" height="6" rx="0.5" fill="#1a1714" opacity="0.6"/>
              <rect x="24" y="2" width="10" height="10" rx="1" fill="none" stroke="#1a1714" stroke-width="1.5"/>
              <rect x="26" y="4" width="6" height="6" rx="0.5" fill="#1a1714" opacity="0.6"/>
              <rect x="2" y="24" width="10" height="10" rx="1" fill="none" stroke="#1a1714" stroke-width="1.5"/>
              <rect x="4" y="26" width="6" height="6" rx="0.5" fill="#1a1714" opacity="0.6"/>
              <rect x="16" y="16" width="18" height="2" fill="#1a1714" opacity="0.3"/>
              <rect x="16" y="20" width="14" height="2" fill="#1a1714" opacity="0.3"/>
              <rect x="16" y="24" width="18" height="2" fill="#1a1714" opacity="0.3"/>
            </svg>
          </div>
        </div>
        <p style="font-size:10px; color:var(--text-dim); text-align:center; margin:6px 0 0; font-family:'Inter',sans-serif;">85 Ã— 55mm Â· Print ready</p>
      </div>
      <div>
        <div style="font-size:11px; font-weight:500; color:#6b1f2a; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:12px; font-family:'Inter',sans-serif;">01 â€” Your business card</div>
        <h3 style="font-size:24px; font-weight:400; color:var(--text-primary); margin:0 0 14px; font-family:'DM Serif Display',serif;">A print-ready card, designed for you</h3>
        <p style="font-size:15px; color:var(--text-secondary); line-height:1.7; margin:0 0 20px; font-family:'Inter',sans-serif;">Get a professional 85Ã—55mm business card PDF instantly. Take it to any print shop in the world, or let us handle it â€” 1000 cards printed and delivered to your door.</p>
        <div style="display:flex; flex-direction:column; gap:10px;">
          <div style="display:flex; align-items:center; gap:10px; font-size:14px; color:var(--text-secondary); font-family:'Inter',sans-serif;">
            <svg viewBox="0 0 24 24" fill="none" stroke="#6b1f2a" stroke-width="2" width="16" height="16"><polyline points="20 6 9 17 4 12"/></svg> Front and back design included
          </div>
          <div style="display:flex; align-items:center; gap:10px; font-size:14px; color:var(--text-secondary); font-family:'Inter',sans-serif;">
            <svg viewBox="0 0 24 24" fill="none" stroke="#6b1f2a" stroke-width="2" width="16" height="16"><polyline points="20 6 9 17 4 12"/></svg> QR code embedded on card
          </div>
          <div style="display:flex; align-items:center; gap:10px; font-size:14px; color:var(--text-secondary); font-family:'Inter',sans-serif;">
            <svg viewBox="0 0 24 24" fill="none" stroke="#6b1f2a" stroke-width="2" width="16" height="16"><polyline points="20 6 9 17 4 12"/></svg> Download PDF instantly
          </div>
        </div>
      </div>
    </div>

    <!-- ROW 2: Text left, phone right -->
    <div class="example-row example-row-reverse" style="display:grid; grid-template-columns:1fr 1fr; gap:64px; align-items:center; margin-bottom:80px;">
      <div>
        <div style="font-size:11px; font-weight:500; color:#6b1f2a; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:12px; font-family:'Inter',sans-serif;">02 â€” Your links page</div>
        <h3 style="font-size:24px; font-weight:400; color:var(--text-primary); margin:0 0 14px; font-family:'DM Serif Display',serif;">One scan, all your links</h3>
        <p style="font-size:15px; color:var(--text-secondary); line-height:1.7; margin:0 0 20px; font-family:'Inter',sans-serif;">When someone scans your card, they land on your hosted links page. All your social profiles, website, and contact details â€” one tap away.</p>
        <div style="display:flex; flex-direction:column; gap:10px;">
          <div style="display:flex; align-items:center; gap:10px; font-size:14px; color:var(--text-secondary); font-family:'Inter',sans-serif;">
            <svg viewBox="0 0 24 24" fill="none" stroke="#6b1f2a" stroke-width="2" width="16" height="16"><polyline points="20 6 9 17 4 12"/></svg> Hosted at cardbranch.co.uk/c/your-brand
          </div>
          <div style="display:flex; align-items:center; gap:10px; font-size:14px; color:var(--text-secondary); font-family:'Inter',sans-serif;">
            <svg viewBox="0 0 24 24" fill="none" stroke="#6b1f2a" stroke-width="2" width="16" height="16"><polyline points="20 6 9 17 4 12"/></svg> Add Instagram, LinkedIn, website and more
          </div>
          <div style="display:flex; align-items:center; gap:10px; font-size:14px; color:var(--text-secondary); font-family:'Inter',sans-serif;">
            <svg viewBox="0 0 24 24" fill="none" stroke="#6b1f2a" stroke-width="2" width="16" height="16"><polyline points="20 6 9 17 4 12"/></svg> Update links any time, card stays the same
          </div>
        </div>
        <a href="/c/da-workforce" target="_blank" rel="noopener noreferrer" style="display:inline-flex; align-items:center; gap:6px; margin-top:20px; font-size:13px; color:#6b1f2a; text-decoration:none; font-family:'Inter',sans-serif;">See a live example <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg></a>
      </div>
      <div style="display:flex; justify-content:center;">
        <div style="width:200px; background:#faf8f4; border:1.5px solid var(--border); border-radius:28px; padding:18px 14px; box-sizing:border-box;">
          <div style="width:44px; height:5px; background:var(--border); border-radius:3px; margin:0 auto 18px;"></div>
          <div style="display:flex; flex-direction:column; align-items:center; gap:6px; margin-bottom:16px;">
            <div style="width:38px; height:38px; border-radius:50%; background:#f0dde0; border:1px solid #d4b0b5; display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:600; color:#6b1f2a; font-family:'Inter',sans-serif;">D</div>
            <div style="font-size:12px; font-weight:600; color:#1a1714; font-family:'Inter',sans-serif;">Da Workforce</div>
            <div style="font-size:9px; color:#8a7e72; text-transform:uppercase; letter-spacing:0.08em; font-family:'Inter',sans-serif;">Delivering Drivers to You</div>
          </div>
          <div style="display:flex; flex-direction:column; gap:6px;">
            <div style="background:#f0ebe4; border:0.5px solid var(--border); border-radius:8px; padding:9px 11px; display:flex; align-items:center; justify-content:space-between;">
              <span style="font-size:11px; color:#8a7e72; font-family:'Inter',sans-serif;">Instagram</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="#8a7e72" stroke-width="2" width="11" height="11"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </div>
            <div style="background:#f0ebe4; border:0.5px solid var(--border); border-radius:8px; padding:9px 11px; display:flex; align-items:center; justify-content:space-between;">
              <span style="font-size:11px; color:#8a7e72; font-family:'Inter',sans-serif;">LinkedIn</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="#8a7e72" stroke-width="2" width="11" height="11"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </div>
            <div style="background:#f0ebe4; border:0.5px solid var(--border); border-radius:8px; padding:9px 11px; display:flex; align-items:center; justify-content:space-between;">
              <span style="font-size:11px; color:#8a7e72; font-family:'Inter',sans-serif;">Website</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="#8a7e72" stroke-width="2" width="11" height="11"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </div>
          </div>
          <div style="width:32px; height:32px; border-radius:50%; background:var(--border); margin:14px auto 0;"></div>
        </div>
      </div>
    </div>

    <!-- ROW 3: QR left, text right -->
    <div class="example-row" style="display:grid; grid-template-columns:1fr 1fr; gap:64px; align-items:center;">
      <div style="background:var(--bg-secondary); border:1px solid var(--border); border-radius:16px; padding:40px; display:flex; flex-direction:column; align-items:center; gap:20px;">
        <svg viewBox="0 0 120 120" width="130" height="130">
          <rect x="4" y="4" width="34" height="34" rx="3" fill="none" stroke="#1a1714" stroke-width="2.5"/>
          <rect x="12" y="12" width="18" height="18" rx="1" fill="#1a1714" opacity="0.8"/>
          <rect x="82" y="4" width="34" height="34" rx="3" fill="none" stroke="#1a1714" stroke-width="2.5"/>
          <rect x="90" y="12" width="18" height="18" rx="1" fill="#1a1714" opacity="0.8"/>
          <rect x="4" y="82" width="34" height="34" rx="3" fill="none" stroke="#1a1714" stroke-width="2.5"/>
          <rect x="12" y="90" width="18" height="18" rx="1" fill="#1a1714" opacity="0.8"/>
          <rect x="46" y="4" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="56" y="4" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="66" y="4" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="46" y="14" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="66" y="14" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="56" y="24" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="46" y="34" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="4" y="46" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="14" y="46" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="24" y="56" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="46" y="46" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="56" y="56" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="66" y="46" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="76" y="56" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="86" y="46" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="96" y="46" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="106" y="56" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="46" y="66" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="76" y="66" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="86" y="76" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="46" y="76" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="56" y="86" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="66" y="96" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="96" y="86" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="46" y="96" width="6" height="6" fill="#1a1714" opacity="0.6"/>
          <rect x="106" y="96" width="6" height="6" fill="#1a1714" opacity="0.6"/>
        </svg>
        <div style="text-align:center;">
          <div style="font-size:12px; font-weight:500; color:#1a1714; font-family:'Inter',sans-serif;">Da Workforce</div>
          <div style="font-size:11px; color:#8a7e72; font-family:'Inter',sans-serif;">cardbranch.co.uk/c/da-workforce</div>
        </div>
        <div style="display:inline-flex; align-items:center; gap:6px; font-size:12px; color:#6b1f2a; border:0.5px solid #d4b0b5; background:#f0dde0; border-radius:6px; padding:7px 16px; font-family:'Inter',sans-serif;">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg> Download PNG
        </div>
      </div>
      <div>
        <div style="font-size:11px; font-weight:500; color:#6b1f2a; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:12px; font-family:'Inter',sans-serif;">03 â€” Your QR code</div>
        <h3 style="font-size:24px; font-weight:400; color:var(--text-primary); margin:0 0 14px; font-family:'DM Serif Display',serif;">Share anywhere, instantly</h3>
        <p style="font-size:15px; color:var(--text-secondary); line-height:1.7; margin:0 0 20px; font-family:'Inter',sans-serif;">Your QR code links directly to your links page. Put it on your card, email signature, or website. Download it as a PNG and use it wherever you need.</p>
        <div style="display:flex; flex-direction:column; gap:10px;">
          <div style="display:flex; align-items:center; gap:10px; font-size:14px; color:var(--text-secondary); font-family:'Inter',sans-serif;">
            <svg viewBox="0 0 24 24" fill="none" stroke="#6b1f2a" stroke-width="2" width="16" height="16"><polyline points="20 6 9 17 4 12"/></svg> Unique to your brand
          </div>
          <div style="display:flex; align-items:center; gap:10px; font-size:14px; color:var(--text-secondary); font-family:'Inter',sans-serif;">
            <svg viewBox="0 0 24 24" fill="none" stroke="#6b1f2a" stroke-width="2" width="16" height="16"><polyline points="20 6 9 17 4 12"/></svg> Works with any camera app
          </div>
          <div style="display:flex; align-items:center; gap:10px; font-size:14px; color:var(--text-secondary); font-family:'Inter',sans-serif;">
            <svg viewBox="0 0 24 24" fill="none" stroke="#6b1f2a" stroke-width="2" width="16" height="16"><polyline points="20 6 9 17 4 12"/></svg> Download as PNG, use anywhere
          </div>
        </div>
      </div>
    </div>

  </div>
</section>

<section style="padding:80px 24px 120px; border-top:1px solid var(--border);">
    <div style="max-width:1200px; margin:0 auto; text-align:center;">
        <h2 style="font-size:24px; font-weight:400; color:var(--text-primary); margin-bottom:48px;">Simple pricing</h2>
        <div class="pricing-grid" style="display:grid; grid-template-columns:repeat(3,1fr); gap:24px; max-width:900px; margin:0 auto;">
            <div class="card-stripe" style="padding:32px;">
                <h3 style="font-size:14px; font-weight:600; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:16px;">Basic</h3>
                <p style="font-size:36px; font-weight:600; color:var(--text-primary); margin-bottom:4px;">Â£49</p>
                <p style="font-size:13px; color:var(--text-dim); margin-bottom:24px;">one-time</p>
                <ul style="list-style:none; text-align:left; color:var(--text-secondary); font-size:14px; display:flex; flex-direction:column; gap:12px;">
                    <li style="display:flex; align-items:center; gap:8px;"><svg viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" width="16" height="16"><polyline points="20 6 9 17 4 12"/></svg>Hosted links page</li>
                    <li style="display:flex; align-items:center; gap:8px;"><svg viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" width="16" height="16"><polyline points="20 6 9 17 4 12"/></svg>QR code</li>
                    <li style="display:flex; align-items:center; gap:8px;"><svg viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" width="16" height="16"><polyline points="20 6 9 17 4 12"/></svg>Print-ready PDF</li>
                    <li style="display:flex; align-items:center; gap:8px;"><svg viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" width="16" height="16"><polyline points="20 6 9 17 4 12"/></svg>50 cards printed</li>
                </ul>
                <a href="{{ url_for('auth.register') }}" class="btn btn-ghost" style="width:100%; margin-top:24px;">Get started</a>
            </div>
            <div class="card-stripe" style="padding:32px; position:relative;">
                <div style="position:absolute; top:-12px; left:50%; transform:translateX(-50%); background:var(--accent); color:#faf8f4; font-size:11px; font-weight:700; padding:4px 14px; border-radius:20px; text-transform:uppercase; letter-spacing:0.07em;">Most popular</div>
                <h3 style="font-size:14px; font-weight:600; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:16px;">Standard</h3>
                <p style="font-size:36px; font-weight:600; color:var(--text-primary); margin-bottom:4px;">Â£85</p>
                <p style="font-size:13px; color:var(--text-dim); margin-bottom:24px;">one-time</p>
                <ul style="list-style:none; text-align:left; color:var(--text-secondary); font-size:14px; display:flex; flex-direction:column; gap:12px;">
                    <li style="display:flex; align-items:center; gap:8px;"><svg viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" width="16" height="16"><polyline points="20 6 9 17 4 12"/></svg>Everything in Basic</li>
                    <li style="display:flex; align-items:center; gap:8px;"><svg viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" width="16" height="16"><polyline points="20 6 9 17 4 12"/></svg>1000 cards printed</li>
                    <li style="display:flex; align-items:center; gap:8px;"><svg viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" width="16" height="16"><polyline points="20 6 9 17 4 12"/></svg>Delivered to your door</li>
                    <li style="display:flex; align-items:center; gap:8px;"><svg viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" width="16" height="16"><polyline points="20 6 9 17 4 12"/></svg>Reprint any time</li>
                </ul>
                <a href="{{ url_for('auth.register') }}" class="btn btn-primary" style="width:100%; margin-top:24px;">Get started</a>
            </div>
            <div class="card-stripe" style="padding:32px;">
                <h3 style="font-size:14px; font-weight:600; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:16px;">Premium</h3>
                <p style="font-size:36px; font-weight:600; color:var(--text-primary); margin-bottom:4px;">Â£120</p>
                <p style="font-size:13px; color:var(--text-dim); margin-bottom:24px;">one-time</p>
                <ul style="list-style:none; text-align:left; color:var(--text-secondary); font-size:14px; display:flex; flex-direction:column; gap:12px;">
                    <li style="display:flex; align-items:center; gap:8px;"><svg viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" width="16" height="16"><polyline points="20 6 9 17 4 12"/></svg>Everything in Standard</li>
                    <li style="display:flex; align-items:center; gap:8px;"><svg viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" width="16" height="16"><polyline points="20 6 9 17 4 12"/></svg>2000 cards printed</li>
                    <li style="display:flex; align-items:center; gap:8px;"><svg viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" width="16" height="16"><polyline points="20 6 9 17 4 12"/></svg>Priority delivery</li>
                    <li style="display:flex; align-items:center; gap:8px;"><svg viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" width="16" height="16"><polyline points="20 6 9 17 4 12"/></svg>Dedicated support</li>
                </ul>
                <a href="{{ url_for('auth.register') }}" class="btn btn-ghost" style="width:100%; margin-top:24px;">Get started</a>
            </div>
        </div>
    </div>
</section>

<style>
    html { scroll-behavior: smooth; }
    @media (max-width: 768px) {
        .hero { padding: 80px 24px 48px; }
        .hero h1 { font-size: 32px; }
        .features-grid { grid-template-columns: 1fr !important; }
        .pricing-grid { grid-template-columns: 1fr !important; }
        .example-row { grid-template-columns: 1fr !important; gap: 32px !important; }
    .example-row > :first-child { order: 2; }
    .example-row > :last-child { order: 1; }
    .example-row-reverse > :first-child { order: 1; }
    .example-row-reverse > :last-child { order: 2; }
        nav > div { padding: 0 16px !important; }
    }
    @media (max-width: 600px) {
        nav .nav-buttons { gap: 8px !important; }
        nav .nav-buttons a, nav .nav-buttons button {
            padding: 6px 12px !important;
            font-size: 12px !important;
        }
    }
</style>
{% endblock %}

```

### templates/public/links.html
```html
{% extends "layouts/base.html" %}
{% block title %}{{ client.brand_name }} - CardBranch{% endblock %}
{% block content %}

{% set colour_map = {
    'oxblood': '#6b1f2a',
    'navy':    '#1a2744',
    'forest':  '#1a3d2b',
    'slate':   '#2d3748',
    'charcoal':'#1a1714',
    'linen':   '#f0ebe4',
    'sage':    '#e8ede8',
    'blush':   '#f5ece8'
} %}
{% set light_styles = ['linen', 'sage', 'blush'] %}
{% set card_bg = colour_map.get(client.card_style, '#6b1f2a') %}
{% set is_light = client.card_style in light_styles %}
{% set text_primary = '#1a1714' if is_light else '#faf8f4' %}
{% set text_secondary = '#4a3f3a' if is_light else '#c8b8b0' %}
{% set text_dim = '#7a6a62' if is_light else '#8a7a72' %}
{% set icon_bg = 'rgba(0,0,0,0.08)' if is_light else 'rgba(255,255,255,0.12)' %}
{% set icon_colour = '#4a3f3a' if is_light else '#e8d8d0' %}
{% set btn_border = 'rgba(0,0,0,0.15)' if is_light else 'rgba(255,255,255,0.15)' %}
{% set btn_hover_bg = 'rgba(0,0,0,0.06)' if is_light else 'rgba(255,255,255,0.08)' %}
{% set divider_colour = 'rgba(0,0,0,0.15)' if is_light else 'rgba(255,255,255,0.2)' %}
{% set brand_accent = '#6b1f2a' if is_light else '#c9a96e' %}

<div style="min-height:100vh; background:{{ card_bg }}; display:flex; flex-direction:column; align-items:center; padding:48px 20px;">
    <div style="text-align:center; max-width:480px; width:100%;">
        {% if client.logo_filename %}
        <img src="{{ r2_url }}/{{ client.logo_filename }}"
             alt="{{ client.brand_name }}"
             style="width:80px; height:80px; border-radius:50%; object-fit:cover; margin-bottom:16px; border:2px solid {{ divider_colour }};">
        {% endif %}

        <h1 style="font-size:22px; font-weight:400; color:{{ text_primary }}; margin-bottom:4px;">
            {{ client.brand_name }}
        </h1>

        {% if client.tagline %}
        <p style="color:{{ text_secondary }}; font-size:13px; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:24px;">{{ client.tagline }}</p>
        {% endif %}

        <div style="width:40px; height:1px; background:{{ divider_colour }}; margin:0 auto 28px;"></div>

        <div style="display:flex; flex-direction:column; gap:12px;">
            {% for link in links %}
            <a href="{{ link.url }}" target="_blank" rel="noopener noreferrer"
               class="links-btn"
               style="display:flex; align-items:center; gap:12px; padding:14px 20px; border-radius:8px; border:1px solid {{ btn_border }}; color:{{ text_primary }}; font-size:13px; font-weight:500; text-decoration:none; transition:all 0.15s; background:transparent;">
                <span style="width:32px; height:32px; border-radius:50%; background:{{ icon_bg }}; display:flex; align-items:center; justify-content:center; color:{{ icon_colour }}; flex-shrink:0;">
                    {% if link.platform|lower == 'instagram' %}
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>
                    {% elif link.platform|lower == 'tiktok' %}
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M9 12a4 4 0 1 0 4 4V4a5 5 0 0 0 5 5"/></svg>
                    {% elif link.platform|lower == 'linkedin' %}
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><rect x="2" y="2" width="20" height="20" rx="4"/><line x1="8" y1="11" x2="8" y2="16"/><line x1="8" y1="8" x2="8" y2="8.5"/><path d="M12 16v-5m0 0a3 3 0 0 1 6 0v5"/></svg>
                    {% elif link.platform|lower == 'website' %}
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
                    {% else %}
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
                    {% endif %}
                </span>
                <span style="flex:1; text-align:left;">{{ link.platform }}</span>
                <span style="color:{{ text_dim }}; font-size:12px;">&rarr;</span>
            </a>
            {% endfor %}
        </div>

        <p style="margin-top:48px; color:{{ text_dim }}; font-size:12px;">Powered by <span style="color:{{ brand_accent }};">CardBranch</span></p>
    </div>
</div>

<style>
    .links-btn:hover,
    .links-btn:focus-visible {
        background: {{ btn_hover_bg }} !important;
    }
</style>
{% endblock %}

```

### templates/auth/login.html
```html
{% extends "layouts/base.html" %}
{% block title %}Sign In - CardBranch{% endblock %}
{% block content %}
<div style="min-height:100vh; display:flex; align-items:flex-start; justify-content:center; padding:80px 20px 20px;">
    <div class="card-stripe" style="padding:32px; width:100%; max-width:400px;">
        <div style="text-align:center; margin-bottom:28px;">
            <h1 style="font-size:22px; font-weight:400; color:var(--text-primary);">Welcome back</h1>
            <p style="color:var(--text-secondary); font-size:14px; margin-top:4px;">Sign in to your account</p>
        </div>
        <form method="POST">
            {{ form.hidden_tag() }}
            <div style="margin-bottom:16px;">
                <label>{{ form.email.label }}</label>
                {{ form.email(placeholder="you@example.com") }}
                {% for error in form.email.errors %}<span style="color:var(--danger); font-size:12px;">{{ error }}</span>{% endfor %}
            </div>
            <div style="margin-bottom:24px;">
                <label>{{ form.password.label }}</label>
                {{ form.password(placeholder="â€¢â€¢â€¢â€¢â€¢â€¢â€¢â€¢") }}
                {% for error in form.password.errors %}<span style="color:var(--danger); font-size:12px;">{{ error }}</span>{% endfor %}
            </div>
            {{ form.submit(class="btn btn-primary", style="width:100%; height:44px;") }}
        </form>
        <p style="text-align:center; margin-top:20px; color:var(--text-secondary); font-size:13px;">
            Don't have an account? <a href="{{ url_for('auth.register') }}" style="color:#6b1f2a;">Register</a>
        </p>
    </div>
</div>
{% endblock %}

```

### templates/auth/register.html
```html
{% extends "layouts/base.html" %}
{% block title %}Register - CardBranch{% endblock %}
{% block content %}
<div style="min-height:100vh; display:flex; align-items:flex-start; justify-content:center; padding:80px 20px 20px;">
    <div class="card-stripe" style="padding:32px; width:100%; max-width:400px;">
        <div style="text-align:center; margin-bottom:28px;">
            <h1 style="font-size:22px; font-weight:400; color:var(--text-primary);">Create account</h1>
            <p style="color:var(--text-secondary); font-size:14px; margin-top:4px;">Get started with CardBranch</p>
        </div>
        <form method="POST">
            {{ form.hidden_tag() }}
            <div style="margin-bottom:16px;">
                <label>{{ form.email.label }}</label>
                {{ form.email(placeholder="you@example.com") }}
                {% for error in form.email.errors %}<span style="color:var(--danger); font-size:12px;">{{ error }}</span>{% endfor %}
            </div>
            <div style="margin-bottom:16px;">
                <label>{{ form.password.label }}</label>
                {{ form.password(placeholder="â€¢â€¢â€¢â€¢â€¢â€¢â€¢â€¢") }}
                {% for error in form.password.errors %}<span style="color:var(--danger); font-size:12px;">{{ error }}</span>{% endfor %}
            </div>
            <div style="margin-bottom:24px;">
                <label>{{ form.confirm_password.label }}</label>
                {{ form.confirm_password(placeholder="â€¢â€¢â€¢â€¢â€¢â€¢â€¢â€¢") }}
                {% for error in form.confirm_password.errors %}<span style="color:var(--danger); font-size:12px;">{{ error }}</span>{% endfor %}
            </div>
            {{ form.submit(class="btn btn-primary", style="width:100%; height:44px;") }}
        </form>
        <p style="text-align:center; margin-top:20px; color:var(--text-secondary); font-size:13px;">
            Already have an account? <a href="{{ url_for('auth.login') }}" style="color:#6b1f2a;">Sign In</a>
        </p>
    </div>
</div>
{% endblock %}

```

### templates/dashboard/index.html
```html
{% extends "layouts/dashboard.html" %}
{% block dashboard_content %}
<div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:24px;">
    <h2 class="page-title" style="margin-bottom:0;">My Cards</h2>
    <a href="{{ url_for('dashboard.card_new') }}" class="btn btn-primary btn-sm">+ New Card</a>
</div>

{% if clients %}
<div style="display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:20px;">
    {% for client in clients %}
    <div class="card-item card-stripe" style="padding:24px;">
        <div style="display:flex; align-items:flex-start; justify-content:space-between; margin-bottom:12px;">
            <h3 style="font-size:16px; font-weight:600; color:var(--text-primary);">{{ client.brand_name }}</h3>
        </div>
        {% if client.tagline %}<p style="color:var(--text-secondary); font-size:13px; margin-bottom:8px;">{{ client.tagline }}</p>{% endif %}
        <p style="color:var(--text-dim); font-size:12px; margin-bottom:16px; font-family:monospace;">cardbranch.co.uk/c/{{ client.slug }}</p>
        <div style="display:flex; gap:8px;">
            <a href="{{ url_for('dashboard.card_view', id=client.id) }}" class="btn btn-ghost btn-sm">View</a>
            <a href="{{ url_for('dashboard.card_edit', id=client.id) }}" class="btn btn-ghost btn-sm">Edit</a>
            <form method="POST" action="{{ url_for('dashboard.card_delete', id=client.id) }}" style="display:inline;" onsubmit="return confirm('Delete this card? This cannot be undone.');">
                <button type="submit" class="btn btn-ghost btn-sm">Delete</button>
            </form>
        </div>
    </div>
    {% endfor %}
</div>
{% else %}
<div class="card-stripe" style="text-align:center; padding:64px 20px;">
    <p style="color:var(--text-secondary); font-size:15px; margin-bottom:16px;">You haven't created any cards yet.</p>
    <a href="{{ url_for('dashboard.card_new') }}" class="btn btn-primary">Create Your First Card</a>
</div>
{% endif %}
<style>
    .card-item:hover,
    .card-item:focus-visible {
        border-color: #6b1f2a !important;
    }
</style>
{% endblock %}

```

### templates/dashboard/card_new.html
```html
{% extends "layouts/dashboard.html" %}
{% block dashboard_content %}

<h2 class="page-title" style="margin-bottom:24px;">Create New Card</h2>

<div class="card-new-layout">

  <!-- LEFT: Form -->
  <div class="card-stripe" style="padding:32px;">
    <form method="POST" enctype="multipart/form-data" id="card-form">
      {{ form.hidden_tag() }}

      <div style="margin-bottom:20px;">
        <label>{{ form.brand_name.label }}</label>
        {{ form.brand_name(placeholder="e.g. Da Workforce", id="brand-input") }}
        {% for error in form.brand_name.errors %}<span style="color:var(--danger); font-size:12px;">{{ error }}</span>{% endfor %}
      </div>

      <div style="margin-bottom:20px;">
        <label>{{ form.tagline.label }} <span style="font-size:11px; color:var(--text-dim); font-weight:400;">(optional)</span></label>
        {{ form.tagline(placeholder="Your tagline or motto", id="tagline-input") }}
      </div>

      <div style="margin-bottom:20px;">
        <label>{{ form.logo.label }} <span style="font-size:11px; color:var(--text-dim); font-weight:400;">(optional)</span></label>
        {{ form.logo }}
        {% for error in form.logo.errors %}<span style="color:var(--danger); font-size:12px;">{{ error }}</span>{% endfor %}
      </div>

      <div style="margin-bottom:20px;">
        <label>Links</label>
        <div id="links-container">
          <div class="link-row" style="display:flex; gap:8px; margin-bottom:8px;">
            <input type="text" name="platform_0" placeholder="Platform (e.g. Instagram)" style="flex:1;" required>
            <input type="url" name="url_0" placeholder="https://..." style="flex:2;" required>
          </div>
        </div>
        <button type="button" onclick="addLink()" class="btn btn-ghost btn-sm" style="margin-top:8px;">+ Add Link</button>
      </div>

      <!-- Colour picker -->
      <div style="margin-bottom:24px;">
        <label style="display:block; margin-bottom:12px;">Card colour</label>
        <input type="hidden" name="card_style" id="card-style-input" value="oxblood">

        <p class="card-new-swatch-label">Dark</p>
        <div class="card-new-swatches">
          <div class="card-new-swatch-wrap" data-style="oxblood" data-bg="#6b1f2a" data-text="#faf8f4">
            <div class="card-new-swatch selected" style="background:#6b1f2a;"></div>
            <span class="card-new-swatch-name">Oxblood</span>
          </div>
          <div class="card-new-swatch-wrap" data-style="navy" data-bg="#1a2744" data-text="#faf8f4">
            <div class="card-new-swatch" style="background:#1a2744;"></div>
            <span class="card-new-swatch-name">Navy</span>
          </div>
          <div class="card-new-swatch-wrap" data-style="forest" data-bg="#1a3d2b" data-text="#faf8f4">
            <div class="card-new-swatch" style="background:#1a3d2b;"></div>
            <span class="card-new-swatch-name">Forest</span>
          </div>
          <div class="card-new-swatch-wrap" data-style="slate" data-bg="#2d3748" data-text="#faf8f4">
            <div class="card-new-swatch" style="background:#2d3748;"></div>
            <span class="card-new-swatch-name">Slate</span>
          </div>
          <div class="card-new-swatch-wrap" data-style="charcoal" data-bg="#1a1714" data-text="#faf8f4">
            <div class="card-new-swatch" style="background:#1a1714; border:1px solid #3a3734;"></div>
            <span class="card-new-swatch-name">Charcoal</span>
          </div>
        </div>

        <div style="border-top:1px solid var(--border); margin:14px 0;"></div>

        <p class="card-new-swatch-label">Light</p>
        <div class="card-new-swatches">
          <div class="card-new-swatch-wrap" data-style="linen" data-bg="#f0ebe4" data-text="#1a1714">
            <div class="card-new-swatch" style="background:#f0ebe4; border:1.5px solid #c8bfb4;"></div>
            <span class="card-new-swatch-name">Linen</span>
          </div>
          <div class="card-new-swatch-wrap" data-style="sage" data-bg="#e8ede8" data-text="#1a1714">
            <div class="card-new-swatch" style="background:#e8ede8; border:1.5px solid #b8c8b8;"></div>
            <span class="card-new-swatch-name">Sage</span>
          </div>
          <div class="card-new-swatch-wrap" data-style="blush" data-bg="#f5ece8" data-text="#1a1714">
            <div class="card-new-swatch" style="background:#f5ece8; border:1.5px solid #d8c0b8;"></div>
            <span class="card-new-swatch-name">Blush</span>
          </div>
        </div>
      </div>

      <input type="hidden" name="links" id="links-json" value="[]">
      <div style="display:flex; gap:8px; padding-top:8px;">
        {{ form.submit(class="btn btn-primary") }}
        <a href="{{ url_for('dashboard.index') }}" class="btn btn-ghost">Cancel</a>
      </div>
    </form>
  </div>

  <!-- RIGHT: Live preview -->
  <div class="card-new-preview">
    <p class="card-new-preview-title">Live preview</p>

    <div style="display:flex; flex-direction:column; gap:16px; flex:1;">
      <div style="flex:1; display:flex; flex-direction:column;">
        <p class="card-new-face-label">FRONT</p>
        <div class="card-new-face" id="preview-front" style="background:#6b1f2a; box-shadow:0 6px 20px rgba(107,31,42,0.35); flex:1; aspect-ratio:unset;">
          <div class="card-new-logo-box" id="preview-logo" style="width:34px; height:34px; font-size:15px; color:#faf8f4; border:1.5px solid rgba(250,248,244,0.4);">D</div>
          <div class="card-new-brand" id="preview-brand" style="color:#faf8f4;">Your Brand</div>
          <div class="card-new-divider" id="preview-divider" style="width:22px; background:rgba(250,248,244,0.35); display:none;"></div>
          <div class="card-new-tag" id="preview-tag" style="color:rgba(250,248,244,0.6); display:none;"></div>
        </div>
      </div>
      <div style="flex:1; display:flex; flex-direction:column;">
        <p class="card-new-face-label">BACK</p>
        <div class="card-new-face" style="background:#faf8f4; border:1.5px solid #d8d0c4; box-shadow:0 4px 12px rgba(0,0,0,0.08); flex:1; aspect-ratio:unset;">
          <svg viewBox="0 0 56 56" width="64" height="64">
            <rect x="2" y="2" width="16" height="16" rx="1.5" fill="none" stroke="#1a1714" stroke-width="2"/>
            <rect x="5" y="5" width="10" height="10" rx="0.5" fill="#1a1714"/>
            <rect x="38" y="2" width="16" height="16" rx="1.5" fill="none" stroke="#1a1714" stroke-width="2"/>
            <rect x="41" y="5" width="10" height="10" rx="0.5" fill="#1a1714"/>
            <rect x="2" y="38" width="16" height="16" rx="1.5" fill="none" stroke="#1a1714" stroke-width="2"/>
            <rect x="5" y="41" width="10" height="10" rx="0.5" fill="#1a1714"/>
            <rect x="22" y="2" width="4" height="4" fill="#1a1714" opacity="0.7"/>
            <rect x="28" y="2" width="4" height="4" fill="#1a1714" opacity="0.7"/>
            <rect x="22" y="8" width="4" height="4" fill="#1a1714" opacity="0.7"/>
            <rect x="28" y="14" width="4" height="4" fill="#1a1714" opacity="0.7"/>
            <rect x="22" y="22" width="4" height="4" fill="#1a1714" opacity="0.7"/>
            <rect x="30" y="22" width="4" height="4" fill="#1a1714" opacity="0.7"/>
            <rect x="38" y="22" width="4" height="4" fill="#1a1714" opacity="0.7"/>
            <rect x="22" y="30" width="4" height="4" fill="#1a1714" opacity="0.7"/>
            <rect x="30" y="30" width="4" height="4" fill="#1a1714" opacity="0.7"/>
            <rect x="46" y="30" width="4" height="4" fill="#1a1714" opacity="0.7"/>
            <rect x="22" y="38" width="4" height="4" fill="#1a1714" opacity="0.7"/>
            <rect x="30" y="46" width="4" height="4" fill="#1a1714" opacity="0.7"/>
            <rect x="38" y="38" width="4" height="4" fill="#1a1714" opacity="0.7"/>
            <rect x="46" y="46" width="4" height="4" fill="#1a1714" opacity="0.7"/>
            <rect x="2" y="22" width="4" height="4" fill="#1a1714" opacity="0.7"/>
            <rect x="10" y="30" width="4" height="4" fill="#1a1714" opacity="0.7"/>
            <rect x="16" y="22" width="4" height="4" fill="#1a1714" opacity="0.7"/>
            <rect x="38" y="46" width="16" height="3" fill="#1a1714" opacity="0.4"/>
            <rect x="38" y="51" width="10" height="3" fill="#1a1714" opacity="0.4"/>
          </svg>
        </div>
      </div>
    </div>
    <p style="font-size:10px; color:var(--text-dim); text-align:center; margin-top:10px;">85 Ã— 55mm Â· Print ready</p>
  </div>

</div>

<style>
.card-new-layout {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: 28px;
  align-items: stretch;
}
.card-new-preview {
  position: sticky;
  top: 24px;
  display: flex;
  flex-direction: column;
  gap: 0;
  padding: 24px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
}
.card-new-preview-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 12px;
}
.card-new-face-label {
  font-size: 10px;
  letter-spacing: 0.12em;
  color: var(--text-dim);
  margin-bottom: 6px;
  font-weight: 600;
}
.card-new-face {
  border-radius: 10px;
  overflow: hidden;
  width: 100%;
  aspect-ratio: 1.75 / 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 7px;
  padding: 16px;
  transition: background 0.2s;
  box-sizing: border-box;
}
.card-new-logo-box {
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Playfair Display SC', Georgia, serif;
  transition: all 0.2s;
}
.card-new-brand {
  font-family: 'Playfair Display SC', Georgia, serif;
  font-size: 14px;
  font-weight: 700;
  transition: color 0.2s;
  text-align: center;
}
.card-new-divider {
  height: 1px;
  transition: background 0.2s;
}
.card-new-tag {
  font-family: 'Playfair Display SC', Georgia, serif;
  font-size: 6.5px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  transition: color 0.2s;
  text-align: center;
}
.card-new-swatches {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 4px;
}
.card-new-swatch-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  cursor: pointer;
}
.card-new-swatch {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  border: 2px solid transparent;
  transition: transform 0.1s;
}
.card-new-swatch:hover { transform: scale(1.1); }
.card-new-swatch.selected {
  border-color: #6b1f2a;
  box-shadow: 0 0 0 3px rgba(107,31,42,0.2);
}
.card-new-swatch-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin: 0 0 10px;
}
.card-new-swatch-name {
  font-size: 9px;
  color: var(--text-secondary);
  font-weight: 500;
}
@media (max-width: 768px) {
  .card-new-layout { grid-template-columns: 1fr !important; }
  .card-new-preview { position: static; margin-top: 8px; }
}
</style>

<script>
let linkCount = 1;
let currentBg = '#6b1f2a';
let isLight = false;

function addLink() {
  const container = document.getElementById('links-container');
  const row = document.createElement('div');
  row.className = 'link-row';
  row.style.cssText = 'display:flex; gap:8px; margin-bottom:8px;';
  row.innerHTML = `
    <input type="text" name="platform_${linkCount}" placeholder="Platform" style="flex:1;" required>
    <input type="url" name="url_${linkCount}" placeholder="https://..." style="flex:2;" required>
  `;
  container.appendChild(row);
  linkCount++;
}

document.getElementById('card-form').addEventListener('submit', function() {
  const links = [];
  document.querySelectorAll('.link-row').forEach(row => {
    const platform = row.querySelector('input[type="text"]').value;
    const url = row.querySelector('input[type="url"]').value;
    if (platform && url) links.push({ platform, url });
  });
  document.getElementById('links-json').value = JSON.stringify(links);
});

function updatePreview() {
  const brand = document.getElementById('brand-input').value.trim() || 'Your Brand';
  const tag = document.getElementById('tagline-input').value.trim();
  const initial = brand[0].toUpperCase();
  const logoEl = document.getElementById('preview-logo');
  const brandEl = document.getElementById('preview-brand');
  const dividerEl = document.getElementById('preview-divider');
  const tagEl = document.getElementById('preview-tag');
  const frontEl = document.getElementById('preview-front');

  logoEl.textContent = initial;
  brandEl.textContent = brand;

  if (tag) {
    dividerEl.style.display = 'block';
    tagEl.style.display = 'block';
    tagEl.textContent = tag;
    logoEl.style.width = '34px';
    logoEl.style.height = '34px';
    logoEl.style.fontSize = '15px';
    brandEl.style.fontSize = '14px';
  } else {
    dividerEl.style.display = 'none';
    tagEl.style.display = 'none';
    logoEl.style.width = '46px';
    logoEl.style.height = '46px';
    logoEl.style.fontSize = '22px';
    brandEl.style.fontSize = '9px';
  }

  if (isLight) {
    logoEl.style.color = '#1a1714';
    logoEl.style.borderColor = 'rgba(26,23,20,0.35)';
    brandEl.style.color = '#1a1714';
    tagEl.style.color = 'rgba(26,23,20,0.55)';
    dividerEl.style.background = 'rgba(26,23,20,0.25)';
    frontEl.style.boxShadow = '0 4px 16px rgba(0,0,0,0.1)';
    frontEl.style.border = '1.5px solid #d8d0c4';
  } else {
    logoEl.style.color = '#faf8f4';
    logoEl.style.borderColor = 'rgba(250,248,244,0.4)';
    brandEl.style.color = '#faf8f4';
    tagEl.style.color = 'rgba(250,248,244,0.6)';
    dividerEl.style.background = 'rgba(250,248,244,0.35)';
    frontEl.style.boxShadow = '0 6px 20px ' + currentBg + '66';
    frontEl.style.border = 'none';
  }
}

document.querySelectorAll('.card-new-swatch-wrap').forEach(wrap => {
  wrap.addEventListener('click', () => {
    document.querySelectorAll('.card-new-swatch').forEach(s => s.classList.remove('selected'));
    wrap.querySelector('.card-new-swatch').classList.add('selected');
    currentBg = wrap.dataset.bg;
    isLight = wrap.dataset.text === '#1a1714';
    document.getElementById('preview-front').style.background = currentBg;
    document.getElementById('card-style-input').value = wrap.dataset.style;
    updatePreview();
  });
});

document.getElementById('brand-input').addEventListener('input', updatePreview);
document.getElementById('tagline-input').addEventListener('input', updatePreview);

currentBg = '#6b1f2a';
isLight = false;
document.getElementById('preview-front').style.background = currentBg;
updatePreview();
</script>

{% endblock %}

```

### templates/dashboard/card_view.html
```html
{% extends "layouts/dashboard.html" %}
{% block dashboard_content %}

{% set colour_map = {
    'oxblood': '#6b1f2a',
    'navy':    '#1a2744',
    'forest':  '#1a3d2b',
    'slate':   '#2d3748',
    'charcoal':'#1a1714',
    'linen':   '#f0ebe4',
    'sage':    '#e8ede8',
    'blush':   '#f5ece8'
} %}
{% set light_styles = ['linen', 'sage', 'blush'] %}
{% set card_bg = colour_map.get(client.card_style, '#6b1f2a') %}
{% set is_light = client.card_style in light_styles %}
{% set card_text = '#1a1714' if is_light else '#faf8f4' %}

{% if request.args.get('order') == 'success' %}
<div style="background:#f0fdf4; border:1.5px solid #86efac; border-radius:10px; padding:14px 18px; margin-bottom:20px; display:flex; align-items:center; gap:12px;">
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
  <div>
    <p style="margin:0; font-size:14px; font-weight:600; color:#15803d;">Payment successful</p>
    <p style="margin:4px 0 0; font-size:13px; color:#166534;">Your QR code and PDF are now ready to download.</p>
  </div>
</div>
{% endif %}
<a href="{{ url_for('dashboard.index') }}" style="font-size:13px; color:var(--text-secondary); display:inline-flex; align-items:center; gap:6px; margin-bottom:16px; text-decoration:none;">
  &larr; My Cards
</a>

<div style="margin-bottom:24px;">
  <h1 style="font-size:24px; font-weight:400; color:var(--text-primary); margin:0 0 4px;">{{ client.brand_name }}</h1>
  {% if client.tagline %}<p style="font-size:14px; color:var(--text-secondary); margin:0;">{{ client.tagline }}</p>{% endif %}
</div>

<div class="card-view-grid">

  <!-- COL 1: BUSINESS CARD -->
  <div class="cv-col">
    <div class="section-header" style="margin-top:0;">
      <div class="section-accent"></div>
      <span class="section-label">BUSINESS CARD</span>
    </div>
    <div class="cv-panel">
      <div class="cv-panel-body" style="display:flex; flex-direction:column; gap:10px;">
        <div>
          <div class="card-lbl">Front</div>
        <div class="card-front" style="background: {{ card_bg }}; width:100%; aspect-ratio:85/55; border-radius:8px; display:flex; align-items:center; justify-content:center; overflow:hidden;">
          <div class="card-inner">
            {% if client.tagline %}
            <div class="logo-box" style="border-color: {{ card_text }}44;">
              {% if client.logo_filename %}
              <img src="{{ r2_url }}/{{ client.logo_filename }}"
                   style="width:100%; height:100%; object-fit:contain; border-radius:3px;"
                   alt="{{ client.brand_name }}">
              {% else %}
              <span class="logo-initial" style="color: {{ card_text }};">{{ client.brand_name[0] }}</span>
              {% endif %}
            </div>
            <div class="preview-name" style="color: {{ card_text }};">{{ client.brand_name }}</div>
            <div class="preview-divider" style="background: {{ card_text }}55;"></div>
            <div class="preview-tagline" style="color: {{ card_text }}99;">{{ client.tagline }}</div>
            {% else %}
            <div class="logo-box logo-box-lg" style="border-color: {{ card_text }}44;">
              {% if client.logo_filename %}
              <img src="{{ r2_url }}/{{ client.logo_filename }}"
                   style="width:100%; height:100%; object-fit:contain; border-radius:4px;"
                   alt="{{ client.brand_name }}">
              {% else %}
              <span class="logo-initial logo-initial-lg" style="color: {{ card_text }};">{{ client.brand_name[0] }}</span>
              {% endif %}
            </div>
            <div class="preview-name-sm" style="color: {{ card_text }}99;">{{ client.brand_name|upper }}</div>
            {% endif %}
          </div>
        </div>
        </div>

        <div>
          <div class="card-lbl">Back</div>
        <div style="width:100%; position:relative; padding-bottom:64.7%; border-radius:8px; overflow:hidden; background:#f0ebe4;">
          <div style="position:absolute; inset:0; display:flex; align-items:center; justify-content:center;">
            <div style="width:38%; aspect-ratio:1; border-radius:3px; overflow:hidden; background:#e0d8d0; display:flex; align-items:center; justify-content:center; padding:4px; box-sizing:border-box;">
              <img src="{{ r2_url }}/generated/{{ client.slug }}/qr.png"
                   style="width:100%; height:100%; display:block; object-fit:contain;"
                   alt="QR Code"
                   onerror="this.style.display='none'">
            </div>
          </div>
        </div>
        </div>
      </div>
      <div class="cv-panel-footer" style="border-top:none; padding-top:6px;">
        <p style="text-align:center; font-size:9px; color:var(--text-dim); margin:0;">85 &times; 55mm &middot; Print ready</p>
      </div>
    </div>
  </div>

  <!-- COL 2: LINKS PAGE -->
  <div class="cv-col">
    <div class="section-header">
      <div class="section-accent"></div>
      <span class="section-label">LINKS PAGE</span>
    </div>
    <div class="cv-panel">
      <div class="cv-panel-body">
        <div style="display:flex; flex-direction:column; align-items:center; gap:5px; padding:10px 0 8px;">
          {% if client.logo_filename %}
          <img src="{{ r2_url }}/{{ client.logo_filename }}"
               style="width:36px; height:36px; border-radius:50%; object-fit:cover; border:1px solid var(--border);"
               alt="{{ client.brand_name }}">
          {% else %}
          <div style="width:36px; height:36px; border-radius:50%; background:#6b1f2a; display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:600; color:#faf8f4;">
            {{ client.brand_name[0] }}
          </div>
          {% endif %}
          <div style="font-size:12px; font-weight:500; color:var(--text-primary);">{{ client.brand_name }}</div>
          {% if client.tagline %}
          <div style="font-size:9px; color:var(--text-dim); text-transform:uppercase; letter-spacing:0.1em; text-align:center;">{{ client.tagline }}</div>
          {% endif %}
        </div>

        <div style="height:0.5px; background:var(--border-light); margin:6px 0 8px;"></div>

        {% for link in links %}
        <a href="{{ link.url }}" class="link-pill" target="_blank" rel="noopener noreferrer">
          <span style="display:flex; align-items:center; gap:6px; font-size:11px; color:var(--text-secondary);">
            {% if link.platform|lower == 'instagram' %}<i class="ti ti-brand-instagram" aria-hidden="true"></i>
            {% elif link.platform|lower == 'tiktok' %}<i class="ti ti-brand-tiktok" aria-hidden="true"></i>
            {% elif link.platform|lower == 'linkedin' %}<i class="ti ti-brand-linkedin" aria-hidden="true"></i>
            {% elif link.platform|lower == 'website' %}<i class="ti ti-world" aria-hidden="true"></i>
            {% else %}<i class="ti ti-link" aria-hidden="true"></i>
            {% endif %}
            {{ link.platform }}
          </span>
          <i class="ti ti-arrow-right" aria-hidden="true" style="font-size:11px; color:var(--text-dim);"></i>
        </a>
        {% endfor %}
      </div>

      <div class="cv-panel-footer">
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px;">
          <a href="{{ url_for('public.card_links', slug=client.slug) }}" class="btn-ghost" target="_blank" rel="noopener noreferrer">
            <i class="ti ti-eye" aria-hidden="true"></i> Preview
          </a>
          <button class="btn-ghost" onclick="navigator.clipboard.writeText('{{ request.host_url }}c/{{ client.slug }}')" style="font-family:inherit; cursor:pointer;">
            <i class="ti ti-copy" aria-hidden="true"></i> Copy link
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- COL 3: YOUR CARD -->
  <div class="cv-col">
    <div class="section-header">
      <div class="section-accent"></div>
      <span class="section-label">YOUR CARD</span>
    </div>
    <div class="cv-panel">
      <div class="cv-panel-body">
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
          <div style="font-size:10px; color:var(--text-dim); text-transform:uppercase; letter-spacing:0.06em;">Live links page</div>
          <div class="live-badge"><div class="live-dot"></div>Live</div>
        </div>
        <div class="url-row">
          <a href="{{ url_for('public.card_links', slug=client.slug) }}"
             style="font-size:11px; color:var(--text-secondary); text-decoration:none; flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;"
             target="_blank">cardbranch.co.uk/c/{{ client.slug }}</a>
          <button onclick="navigator.clipboard.writeText('{{ request.host_url }}c/{{ client.slug }}')"
                  style="background:none; border:none; cursor:pointer; color:var(--text-dim); font-family:inherit; padding:0;">
            <i class="ti ti-copy" aria-hidden="true" style="font-size:13px;"></i>
          </button>
        </div>

        <div class="meta-grid">
          <div class="meta-cell">
            <div class="meta-label">CREATED</div>
            <div class="meta-value">{{ client.created_at.strftime('%d %b') }}</div>
          </div>
          <div class="meta-cell">
            <div class="meta-label">LINKS</div>
            <div class="meta-value">{{ links|length }}</div>
          </div>
          <div class="meta-cell">
            <div class="meta-label">SLUG</div>
            <div class="meta-value" style="font-size:9px; word-break:break-all;">{{ client.slug }}</div>
          </div>
        </div>
      </div>

      <div class="cv-panel-footer">
        <a href="{{ url_for('checkout.order', id=client.id) }}" class="btn-primary">
          <i class="ti ti-shopping-cart" aria-hidden="true"></i> Order cards
        </a>
        <p style="text-align:center; font-size:10px; color:var(--text-dim); margin:0;">Printed &amp; delivered to your door</p>
        <a href="{{ url_for('dashboard.download_pdf', id=client.id) }}" class="btn-ghost">
          <i class="ti ti-download" aria-hidden="true"></i> Download PDF
        </a>
        <a href="{{ url_for('dashboard.download_qr', id=client.id) }}" class="btn-ghost">
          <i class="ti ti-qrcode" aria-hidden="true"></i> Download QR
        </a>
        <a href="{{ url_for('dashboard.card_edit', id=client.id) }}" class="btn-ghost">
          <i class="ti ti-edit" aria-hidden="true"></i> Edit card
        </a>
        <form method="POST" action="{{ url_for('dashboard.card_delete', id=client.id) }}"
              onsubmit="return confirm('Delete this card? This cannot be undone.');">
          <button type="submit" class="btn-ghost btn-danger" style="font-family:inherit; cursor:pointer; width:100%;">
            <i class="ti ti-trash" aria-hidden="true"></i> Delete card
          </button>
        </form>
      </div>
    </div>
  </div>

</div>

<style>
.card-view-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 20px;
  align-items: start;
}
.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 10px;
}
@media (max-width: 768px) {
  .card-view-grid { grid-template-columns: 1fr !important; }
}
.cv-col { display: flex; flex-direction: column; }
.cv-panel {
  background: var(--bg-secondary);
  border: 0.5px solid rgba(107,31,42,0.2);
  border-radius: 12px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  flex: 1;
}
.cv-panel-body { flex: 1; }
.cv-panel-footer {
  margin-top: auto;
  padding-top: 12px;
  border-top: 0.5px solid var(--border-light);
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.card-lbl {
  font-size: 9px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-dim);
  margin-bottom: 5px;
}
.card-front {
  width: 100%;
  aspect-ratio: 85 / 55;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.card-inner {
  width: 88%;
  height: 84%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.logo-box {
  width: 20%;
  aspect-ratio: 1;
  border: 1px solid;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  margin-bottom: 9%;
  flex-shrink: 0;
}
.logo-box-lg {
  width: 30%;
  margin-bottom: 6%;
}
.logo-initial {
  font-size: 11px;
  font-weight: 700;
  font-family: 'Playfair Display SC', Georgia, serif;
}
.logo-initial-lg {
  font-size: 16px;
}
.preview-name {
  font-size: 9px;
  font-weight: 700;
  font-family: 'Playfair Display SC', Georgia, serif;
  text-align: center;
  margin-bottom: 5%;
}
.preview-name-sm {
  font-size: 7px;
  letter-spacing: 0.12em;
  font-family: 'Playfair Display SC', Georgia, serif;
  text-align: center;
}
.preview-divider {
  width: 28px;
  height: 1px;
  margin-bottom: 5%;
}
.preview-tagline {
  font-size: 5.5px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  text-align: center;
  font-family: 'Playfair Display SC', Georgia, serif;
}
.btn-primary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  width: 100%;
  padding: 9px 0;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  background: #6b1f2a;
  border: none;
  color: #faf8f4;
  text-decoration: none;
  cursor: pointer;
}
.btn-ghost {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  width: 100%;
  padding: 9px 0;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  background: transparent;
  border: 0.5px solid var(--border);
  color: var(--text-secondary);
  text-decoration: none;
  cursor: pointer;
}
.btn-danger {
  color: #a03030 !important;
  border-color: rgba(160,48,48,0.25) !important;
}
.link-pill {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 10px;
  border-radius: 8px;
  border: 0.5px solid var(--border-light);
  background: var(--bg-elevated);
  margin-bottom: 6px;
  text-decoration: none;
}
.live-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 10px;
  color: #2d6a3f;
  background: #eaf3de;
  border-radius: 20px;
  padding: 2px 8px;
}
.live-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #639922;
  flex-shrink: 0;
}
.url-row {
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--bg-elevated);
  border: 0.5px solid var(--border-light);
  border-radius: 8px;
  padding: 8px 10px;
  margin-bottom: 10px;
}
.meta-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1px;
  background: var(--border-light);
  border-radius: 8px;
  overflow: hidden;
}
.meta-cell {
  background: var(--bg-elevated);
  padding: 8px 6px;
  text-align: center;
}
.meta-label {
  font-size: 9px;
  color: var(--text-dim);
  letter-spacing: 0.06em;
  margin-bottom: 2px;
}
.meta-value {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
}
</style>
{% endblock %}

```

### templates/dashboard/card_edit.html
```html
{% extends "layouts/dashboard.html" %}
{% block dashboard_content %}

{% set colour_map = {
    'oxblood': {'bg_hex': '#6b1f2a', 'light': False},
    'navy':    {'bg_hex': '#1a2744', 'light': False},
    'forest':  {'bg_hex': '#1a3d2b', 'light': False},
    'slate':   {'bg_hex': '#2d3748', 'light': False},
    'charcoal':{'bg_hex': '#1a1714', 'light': False},
    'linen':   {'bg_hex': '#f0ebe4', 'light': True},
    'sage':    {'bg_hex': '#e8ede8', 'light': True},
    'blush':   {'bg_hex': '#f5ece8', 'light': True},
} %}

<style>
.card-new-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 32px;
    align-items: start;
    max-width: 960px;
}
@media (max-width: 768px) {
    .card-new-grid {
        grid-template-columns: 1fr;
    }
    .card-new-preview-col {
        order: -1;
    }
}
.card-new-preview-wrap {
    position: sticky;
    top: 24px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}
.card-new-preview-card {
    width: 100%;
    aspect-ratio: 85 / 55;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
    transition: background 0.3s ease;
}
.card-new-swatches {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 8px;
}
.card-new-swatch-wrap {
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
}
.card-new-swatch {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    border: 2px solid transparent;
    transition: border-color 0.15s, transform 0.15s;
}
.card-new-swatch.selected {
    border-color: var(--accent);
    transform: scale(1.15);
}
.card-new-swatch-label {
    font-size: 10px;
    color: var(--text-dim);
    text-transform: capitalize;
}
.card-preview-inner {
    width: 92%;
    height: 88%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0;
    position: relative;
}
.card-preview-logo-box {
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    flex-shrink: 0;
    transition: border-color 0.3s;
}
.card-preview-name {
    font-family: 'Playfair Display SC', serif;
    font-weight: 700;
    text-align: center;
    transition: color 0.3s;
    line-height: 1.1;
}
.card-preview-divider {
    width: 40px;
    height: 1px;
    transition: background 0.3s;
}
.card-preview-tagline {
    font-family: 'Playfair Display SC', serif;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    text-align: center;
    transition: color 0.3s;
}
.card-back-preview {
    width: 100%;
    aspect-ratio: 85 / 55;
    border-radius: 8px;
    background: #f0ebe4;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}
.card-back-qr-placeholder {
    width: 38%;
    aspect-ratio: 1;
    background: #e0d8d0;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>

<h2 class="page-title">Edit {{ client.brand_name }}</h2>

<div class="card-new-grid">
    <!-- FORM COLUMN -->
    <div>
        <div class="card-stripe" style="padding: 28px;">
            <form method="POST" enctype="multipart/form-data">
                {{ form.hidden_tag() }}

                <div style="margin-bottom: 20px;">
                    <label>{{ form.brand_name.label }}</label>
                    {{ form.brand_name(id="input-brand", value=client.brand_name) }}
                    {% for error in form.brand_name.errors %}
                    <span style="color:var(--danger); font-size:12px;">{{ error }}</span>
                    {% endfor %}
                </div>

                <div style="margin-bottom: 20px;">
                    <label>{{ form.tagline.label }}</label>
                    {{ form.tagline(id="input-tagline", value=client.tagline) }}
                </div>

                <div style="margin-bottom: 20px;">
                    <label>{{ form.logo.label }}</label>
                    {{ form.logo }}
                    {% if client.logo_filename %}
                    <p style="color:var(--text-dim); font-size:12px; margin-top:4px;">Current logo on file</p>
                    {% endif %}
                </div>

                <div style="margin-bottom: 20px;">
                    <label style="display:block; margin-bottom:8px;">Card Colour</label>
                    <div class="card-new-swatches">
                        <div style="width:100%; font-size:11px; color:var(--text-dim); margin-bottom:4px; text-transform:uppercase; letter-spacing:0.08em;">Dark</div>
                        {% for style, cfg in colour_map.items() %}
                        {% if not cfg.light %}
                        <div class="card-new-swatch-wrap" data-style="{{ style }}" onclick="selectColour('{{ style }}', '{{ cfg.bg_hex }}', false)">
                            <div class="card-new-swatch {% if client.card_style == style %}selected{% endif %}" style="background:{{ cfg.bg_hex }};"></div>
                            <span class="card-new-swatch-label">{{ style }}</span>
                        </div>
                        {% endif %}
                        {% endfor %}
                        <div style="width:100%; font-size:11px; color:var(--text-dim); margin-top:8px; margin-bottom:4px; text-transform:uppercase; letter-spacing:0.08em;">Light</div>
                        {% for style, cfg in colour_map.items() %}
                        {% if cfg.light %}
                        <div class="card-new-swatch-wrap" data-style="{{ style }}" onclick="selectColour('{{ style }}', '{{ cfg.bg_hex }}', true)">
                            <div class="card-new-swatch {% if client.card_style == style %}selected{% endif %}" style="background:{{ cfg.bg_hex }};"></div>
                            <span class="card-new-swatch-label">{{ style }}</span>
                        </div>
                        {% endif %}
                        {% endfor %}
                    </div>
                    <input type="hidden" name="card_style" id="card-style-input" value="{{ client.card_style }}">
                </div>

                <div style="margin-bottom: 20px;">
                    <label>Links</label>
                    <div id="links-container">
                        {% for link in links %}
                        <div class="link-row" style="display:flex; gap:8px; margin-bottom:8px;">
                            <input type="text" name="platform_{{ loop.index0 }}" value="{{ link.platform }}" placeholder="Platform" style="flex:1;" required>
                            <input type="url" name="url_{{ loop.index0 }}" value="{{ link.url }}" placeholder="https://..." style="flex:2;" required>
                        </div>
                        {% endfor %}
                    </div>
                    <button type="button" onclick="addLink()" class="btn btn-ghost btn-sm" style="margin-top:8px;">+ Add Link</button>
                </div>

                <input type="hidden" name="links" id="links-json" value="">
                <div style="display:flex; gap:8px; padding-top:8px;">
                    {{ form.submit(class="btn btn-primary") }}
                    <a href="{{ url_for('dashboard.card_view', id=client.id) }}" class="btn btn-ghost">Cancel</a>
                </div>
            </form>
        </div>
    </div>

    <!-- PREVIEW COLUMN -->
    <div class="card-new-preview-col">
        <div class="card-new-preview-wrap">
            <p style="font-size:11px; text-transform:uppercase; letter-spacing:0.1em; color:var(--text-dim); margin-bottom:4px;">Preview</p>

            <!-- Front -->
            <div class="card-new-preview-card" id="preview-front"
                 style="background: {{ colour_map[client.card_style]['bg_hex'] }};">
                <div class="card-preview-inner" id="preview-inner">
                    <!-- JS renders content here -->
                </div>
            </div>

            <!-- Back -->
            <div class="card-back-preview">
                <div class="card-back-qr-placeholder">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#b0a090" stroke-width="1.5"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="3" height="3"/></svg>
                </div>
            </div>

            <p style="font-size:11px; color:var(--text-dim); text-align:center;">Front &amp; back preview</p>
        </div>
    </div>
</div>

<script>
let currentBg = '{{ colour_map[client.card_style]["bg_hex"] }}';
let isLight = {{ 'true' if colour_map[client.card_style]['light'] else 'false' }};
let linkCount = {{ links|length }};

function selectColour(style, hex, light) {
    currentBg = hex;
    isLight = light;
    document.getElementById('card-style-input').value = style;
    document.getElementById('preview-front').style.background = hex;
    document.querySelectorAll('.card-new-swatch').forEach(s => s.classList.remove('selected'));
    const wrap = document.querySelector(`.card-new-swatch-wrap[data-style="${style}"]`);
    if (wrap) wrap.querySelector('.card-new-swatch').classList.add('selected');
    updatePreview();
}

function updatePreview() {
    const brand = document.getElementById('input-brand').value.trim() || '{{ client.brand_name }}';
    const tagline = document.getElementById('input-tagline').value.trim();
    const textColour = isLight ? '#1a1714' : '#faf8f4';
    const inner = document.getElementById('preview-inner');

    if (tagline) {
        // A1 layout
        inner.innerHTML = `
            <div style="display:flex; flex-direction:column; align-items:center; gap:0; width:100%;">
                <div class="card-preview-logo-box"
                     style="width:22%; aspect-ratio:1; border:1px solid ${textColour}44; background:${currentBg}; margin-bottom:6%;">
                    <span style="font-family:'Playfair Display SC',serif; font-weight:700; font-size:clamp(10px,2.5vw,16px); color:${textColour};">
                        ${brand.charAt(0).toUpperCase()}
                    </span>
                </div>
                <div class="card-preview-name" style="font-size:clamp(11px,2vw,15px); color:${textColour}; margin-bottom:4%;">${brand}</div>
                <div class="card-preview-divider" style="background:${textColour}66; margin-bottom:4%;"></div>
                <div class="card-preview-tagline" style="font-size:clamp(7px,1.2vw,9px); color:${textColour}aa;">${tagline.toUpperCase()}</div>
            </div>`;
    } else {
        // A3 layout
        inner.innerHTML = `
            <div style="display:flex; flex-direction:column; align-items:center; gap:0; width:100%;">
                <div class="card-preview-logo-box"
                     style="width:32%; aspect-ratio:1; border:1px solid ${textColour}44; background:${currentBg}; margin-bottom:5%;">
                    <span style="font-family:'Playfair Display SC',serif; font-weight:700; font-size:clamp(12px,3vw,20px); color:${textColour};">
                        ${brand.charAt(0).toUpperCase()}
                    </span>
                </div>
                <div style="font-family:'Playfair Display SC',serif; font-size:clamp(8px,1.4vw,10px); letter-spacing:0.12em; text-transform:uppercase; color:${textColour}aa;">${brand.toUpperCase()}</div>
            </div>`;
    }
}

document.getElementById('input-brand').addEventListener('input', updatePreview);
document.getElementById('input-tagline').addEventListener('input', updatePreview);

function addLink() {
    const container = document.getElementById('links-container');
    const row = document.createElement('div');
    row.className = 'link-row';
    row.style.cssText = 'display:flex; gap:8px; margin-bottom:8px;';
    row.innerHTML = `
        <input type="text" name="platform_${linkCount}" placeholder="Platform" style="flex:1;" required>
        <input type="url" name="url_${linkCount}" placeholder="https://..." style="flex:2;" required>
    `;
    container.appendChild(row);
    linkCount++;
}

document.querySelector('form').addEventListener('submit', function() {
    const links = [];
    document.querySelectorAll('.link-row').forEach(row => {
        const platform = row.querySelector('input[type="text"]').value;
        const url = row.querySelector('input[type="url"]').value;
        if (platform && url) links.push({platform, url});
    });
    document.getElementById('links-json').value = JSON.stringify(links);
});

// Init preview on load
updatePreview();
</script>
{% endblock %}

```

### templates/dashboard/card_order.html
```html
{% extends "layouts/dashboard.html" %}
{% block dashboard_content %}

<style>
  .order-header {
    margin-bottom: 32px;
  }
  .order-header h2 {
    font-family: 'DM Serif Display', serif;
    font-size: 28px;
    color: var(--text-primary);
    margin: 0 0 8px 0;
  }
  .order-header p {
    color: var(--text-secondary);
    font-size: 15px;
    margin: 0;
  }
  .tiers-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 40px;
  }
  .tier-card {
    background: var(--bg-card);
    border: 1.5px solid var(--border);
    border-radius: 12px;
    padding: 28px 24px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    transition: border-color 0.15s;
  }
  .tier-card.recommended {
    border-color: var(--accent);
  }
  .tier-badge {
    display: inline-block;
    background: var(--accent);
    color: #fff;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 4px;
  }
  .tier-name {
    font-family: 'DM Serif Display', serif;
    font-size: 22px;
    color: var(--text-primary);
    margin: 0;
  }
  .tier-price {
    font-size: 36px;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1;
  }
  .tier-price span {
    font-size: 15px;
    font-weight: 400;
    color: var(--text-secondary);
  }
  .tier-description {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
    line-height: 1.5;
  }
  .tier-includes {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex: 1;
  }
  .tier-includes li {
    font-size: 14px;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .tier-includes li::before {
    content: '';
    display: inline-block;
    width: 16px;
    height: 16px;
    background: var(--accent);
    mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='20 6 9 17 4 12'/%3E%3C/svg%3E");
    mask-size: contain;
    mask-repeat: no-repeat;
    flex-shrink: 0;
  }
  .tier-btn {
    display: block;
    width: 100%;
    padding: 12px;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 600;
    text-align: center;
    cursor: pointer;
    border: none;
    background: var(--accent);
    color: #fff;
    text-decoration: none;
    transition: opacity 0.15s;
  }
  .tier-btn:hover {
    opacity: 0.88;
  }
  .tier-btn.ghost {
    background: transparent;
    border: 1.5px solid var(--border);
    color: var(--text-primary);
  }
  .tier-btn.ghost:hover {
    border-color: var(--accent);
    color: var(--accent);
  }
  .order-back {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    color: var(--text-secondary);
    font-size: 14px;
    text-decoration: none;
    margin-bottom: 24px;
  }
  .order-back:hover {
    color: var(--text-primary);
  }
  @media (max-width: 768px) {
    .tiers-grid {
      grid-template-columns: 1fr;
    }
    .tier-price {
      font-size: 30px;
    }
  }
</style>

<a href="{{ url_for('dashboard.card_view', id=client.id) }}" class="order-back">
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
  Back to card
</a>

<div class="order-header">
  <h2>Get your card</h2>
  <p>Choose a plan for <strong>{{ client.brand_name }}</strong>. One-time payment â€” no subscription.</p>
</div>

<div class="tiers-grid">
  {% for tier in tiers %}
  <div class="tier-card {% if tier.key == 'standard' %}recommended{% endif %}">
    {% if tier.key == 'standard' %}
    <span class="tier-badge">Most popular</span>
    {% else %}
    <span style="display:block; height:22px;"></span>
    {% endif %}
    <p class="tier-name">{{ tier.name }}</p>
    <div class="tier-price">{{ tier.price }} <span>one-time</span></div>
    <p class="tier-description">{{ tier.description }}</p>
    <ul class="tier-includes">
      {% for item in tier.includes %}
      <li>{{ item }}</li>
      {% endfor %}
    </ul>
    <a href="{{ url_for('dashboard.card_checkout', id=client.id, tier=tier.key) }}" class="tier-btn {% if tier.key != 'standard' %}ghost{% endif %}">
      Get {{ tier.name }}
    </a>
  </div>
  {% endfor %}
</div>

{% endblock %}

```

### templates/dashboard/orders.html
```html
{% extends "layouts/dashboard.html" %}
{% block dashboard_content %}
<h2 class="page-title">Order History</h2>

{% if orders %}
<div class="card-stripe" style="overflow:hidden; padding:0;">
    <div style="overflow-x:auto;">
        <table>
            <thead>
                <tr>
                    <th>Order</th>
                    <th>Brand</th>
                    <th>Qty</th>
                    <th>Amount</th>
                    <th>Status</th>
                    <th>Tracking</th>
                    <th>Date</th>
                </tr>
            </thead>
            <tbody>
                {% for order in orders %}
                <tr>
                    <td style="font-weight:500;">#{{ order.id }}</td>
                    <td>{{ order.client.brand_name }}</td>
                    <td>{{ order.quantity }}</td>
                    <td>Â£{{ "%.2f"|format(order.amount_paid) }}</td>
                    <td><span class="status-pill status-{{ order.status }}">{{ order.status.replace('_', ' ') }}</span></td>
                    <td style="color:var(--text-secondary);">{{ order.tracking_number or '-' }}</td>
                    <td style="color:var(--text-secondary);">{{ order.created_at.strftime('%d %b %Y') }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% else %}
<div class="card-stripe" style="text-align:center; padding:64px 20px;">
    <p style="color:var(--text-secondary); font-size:15px;">No orders yet. Create a card to get started.</p>
</div>
{% endif %}
{% endblock %}

```

### templates/admin/index.html
```html
{% extends "layouts/admin.html" %}
{% block admin_content %}
<h2 class="page-title">Admin Overview</h2>

<div style="display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:16px; margin-bottom:32px;">
    <div class="card-stripe" style="padding:24px;">
        <p class="section-label" style="margin-bottom:8px;">Total Users</p>
        <p class="stat-value">{{ total_users }}</p>
    </div>
    <div class="card-stripe" style="padding:24px;">
        <p class="section-label" style="margin-bottom:8px;">Total Cards</p>
        <p class="stat-value">{{ total_cards }}</p>
    </div>
    <div class="card-stripe" style="padding:24px;">
        <p class="section-label" style="margin-bottom:8px;">Total Orders</p>
        <p class="stat-value">{{ total_orders }}</p>
    </div>
    <div class="card-stripe" style="padding:24px;">
        <p class="section-label" style="margin-bottom:8px;">Total Revenue</p>
        <p class="stat-value">Â£{{ "%.2f"|format(total_revenue) }}</p>
    </div>
</div>

<div style="display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:20px;">
    <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-lg); padding:24px;">
        <h3 class="section-label" style="margin-bottom:16px;">Recent Orders</h3>
        {% if recent_orders %}
        <ul style="list-style:none;">
            {% for order in recent_orders %}
            <li style="padding:10px 0; border-bottom:1px solid var(--border); display:flex; justify-content:space-between;">
                <span style="font-size:14px;">#{{ order.id }} - {{ order.client.brand_name if order.client else 'N/A' }}</span>
                <span style="color:var(--text-secondary); font-size:13px;">Â£{{ "%.2f"|format(order.amount_paid) }}</span>
            </li>
            {% endfor %}
        </ul>
        {% else %}
        <p style="color:var(--text-dim);">No orders yet.</p>
        {% endif %}
    </div>
    <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-lg); padding:24px;">
        <h3 class="section-label" style="margin-bottom:16px;">Recent Users</h3>
        {% if recent_users %}
        <ul style="list-style:none;">
            {% for user in recent_users %}
            <li style="padding:10px 0; border-bottom:1px solid var(--border); display:flex; justify-content:space-between;">
                <span style="font-size:14px;">{{ user.email }}</span>
                <span style="color:var(--text-secondary); font-size:13px;">{{ user.created_at.strftime('%d %b %Y') }}</span>
            </li>
            {% endfor %}
        </ul>
        {% else %}
        <p style="color:var(--text-dim);">No users yet.</p>
        {% endif %}
    </div>
</div>
{% endblock %}

```

### templates/admin/users.html
```html
{% extends "layouts/admin.html" %}
{% block admin_content %}
<h2 class="page-title">Users</h2>

<div class="card-stripe" style="padding:0;">
    <div style="overflow-x:auto;">
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Email</th>
                    <th>Admin</th>
                    <th>Cards</th>
                    <th>Joined</th>
                </tr>
            </thead>
            <tbody>
                {% for user in users %}
                <tr>
                    <td style="font-weight:500;">{{ user.id }}</td>
                    <td>{{ user.email }}</td>
                    <td>{% if user.is_admin %}<span class="badge">Admin</span>{% else %}<span style="color:var(--text-dim); font-size:13px;">No</span>{% endif %}</td>
                    <td>{{ user.clients.count() }}</td>
                    <td style="color:var(--text-secondary);">{{ user.created_at.strftime('%d %b %Y') }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}

```

### templates/admin/orders.html
```html
{% extends "layouts/admin.html" %}
{% block admin_content %}
<h2 class="page-title">All Orders</h2>

<div class="card-stripe" style="padding:0;">
    <div style="overflow-x:auto;">
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>User</th>
                    <th>Brand</th>
                    <th>Tier</th>
                    <th>Qty</th>
                    <th>Amount</th>
                    <th>Status</th>
                    <th>Tracking</th>
                    <th>Date</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for order in orders %}
                <tr>
                    <td style="font-weight:500;">{{ order.id }}</td>
                    <td>{{ order.user.email }}</td>
                    <td>{{ order.client.brand_name if order.client else 'N/A' }}</td>
                    <td style="text-transform:capitalize;">{{ order.tier }}</td>
                    <td>{{ order.quantity }}</td>
                    <td>Â£{{ "%.2f"|format(order.amount_paid) }}</td>
                    <td><span class="status-pill status-{{ order.status }}">{{ order.status.replace('_', ' ') }}</span></td>
                    <td style="color:var(--text-secondary);">{{ order.tracking_number or '-' }}</td>
                    <td style="color:var(--text-secondary);">{{ order.created_at.strftime('%d %b %Y') }}</td>
                    <td>
                        <div style="display:flex; gap:6px; align-items:flex-start; flex-wrap:wrap;">
                            <button class="btn btn-ghost btn-sm" onclick="document.getElementById('addr-{{ order.id }}').style.display=document.getElementById('addr-{{ order.id }}').style.display=='none'?'table-row':'none'">Address</button>
                            <form method="POST" style="display:flex; gap:6px; align-items:center; flex-wrap:wrap;">
                                <input type="hidden" name="order_id" value="{{ order.id }}">
                                <select name="status" style="width:auto; padding:6px 8px; font-size:12px;">
                                    <option value="paid" {% if order.status == 'paid' %}selected{% endif %}>Paid</option>
                                    <option value="pending" {% if order.status == 'pending' %}selected{% endif %}>Pending</option>
                                    <option value="sent_to_print" {% if order.status == 'sent_to_print' %}selected{% endif %}>Sent to Print</option>
                                    <option value="dispatched" {% if order.status == 'dispatched' %}selected{% endif %}>Dispatched</option>
                                    <option value="delivered" {% if order.status == 'delivered' %}selected{% endif %}>Delivered</option>
                                </select>
                                <input type="text" name="tracking_number" placeholder="Tracking #" value="{{ order.tracking_number }}" style="width:100px; padding:6px 8px; font-size:12px;">
                                <button type="submit" class="btn btn-ghost btn-sm">Update</button>
                            </form>
                        </div>
                    </td>
                </tr>
                <tr id="addr-{{ order.id }}" style="display:none;">
                    <td colspan="10" style="background:var(--bg-card); color:var(--text-secondary); font-size:13px; padding:10px 16px;">
                        <strong style="color:var(--text-primary);">{{ order.delivery_name }}</strong><br>
                        {{ order.delivery_line1 }}<br>
                        {% if order.delivery_line2 %}{{ order.delivery_line2 }}<br>{% endif %}
                        {{ order.delivery_city }}<br>
                        {{ order.delivery_postcode }}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>


{% endblock %}

```

### templates/admin/revenue.html
```html
{% extends "layouts/admin.html" %}
{% block admin_content %}
<h2 class="page-title">Revenue</h2>

<div class="card-stripe" style="padding:24px; margin-bottom:24px;">
    <p class="section-label" style="margin-bottom:8px;">Total Revenue</p>
    <p class="stat-value" style="font-size:26px;">Â£{{ "%.2f"|format(total) }}</p>
</div>

<div class="card-stripe" style="padding:0;">
    <div style="overflow-x:auto;">
        <table>
            <thead>
                <tr>
                    <th>Order</th>
                    <th>User</th>
                    <th>Brand</th>
                    <th>Qty</th>
                    <th>Amount</th>
                    <th>Date</th>
                </tr>
            </thead>
            <tbody>
                {% for order in orders %}
                <tr>
                    <td style="font-weight:500;">{{ order.id }}</td>
                    <td>{{ order.user.email }}</td>
                    <td>{{ order.client.brand_name if order.client else 'N/A' }}</td>
                    <td>{{ order.quantity }}</td>
                    <td>Â£{{ "%.2f"|format(order.amount_paid) }}</td>
                    <td style="color:var(--text-secondary);">{{ order.created_at.strftime('%d %b %Y') }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}

```

## 2. Standalone CSS Files

NO standalone CSS files exist. All CSS is defined inline in `<style>` blocks within the template files themselves. The primary `<style>` block lives in `templates/layouts/base.html` with additional per-template style blocks in each child template.

## 3. CSS Custom Properties Defined in `:root`

**File:** `templates/layouts/base.html` (lines 12-32)

| Variable | Value |
|---|---|
| `--bg-primary` | #f0ebe4 |
| `--bg-secondary` | #faf8f4 |
| `--bg-card` | #faf8f4 |
| `--bg-elevated` | #ffffff |
| `--accent` | #6b1f2a |
| `--accent-hover` | #7c2535 |
| `--accent-subtle` | #f0dde0 |
| `--accent-border` | #d4b0b5 |
| `--text-primary` | #1a1714 |
| `--text-secondary` | #8a7e72 |
| `--text-dim` | #b0a496 |
| `--border` | #d8d0c4 |
| `--border-light` | #e8e2d8 |
| `--success` | #3b6d11 |
| `--warning` | #92600a |
| `--danger` | #ef4444 |
| `--radius` | 8px |
| `--radius-sm` | 4px |
| `--radius-lg` | 8px |

## 4. Route File Contents

### app/dashboard/routes.py
```python
import json
import os
import stripe
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, abort
from flask_login import login_required, current_user
from app.models import Client, Link, Order, db
from app.dashboard.forms import CardForm, LinkForm
from app.services.generator import unique_slug, save_logo, generate_assets
from app.services.email import send_order_confirmation

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def index():
    clients = Client.query.filter_by(user_id=current_user.id).order_by(Client.created_at.desc()).all()
    return render_template('dashboard/index.html', clients=clients)


@dashboard_bp.route('/card/new', methods=['GET', 'POST'])
@login_required
def card_new():
    form = CardForm()
    if form.validate_on_submit():
        brand_name = form.brand_name.data.strip()
        tagline = form.tagline.data.strip() if form.tagline.data else ''
        slug = unique_slug(brand_name)

        logo_filename = ''
        if form.logo.data:
            logo_filename = save_logo(form.logo.data)

        card_style = request.form.get('card_style', 'oxblood')

        client = Client(
            user_id=current_user.id,
            brand_name=brand_name,
            tagline=tagline,
            slug=slug,
            logo_filename=logo_filename,
            card_style=card_style,
        )
        db.session.add(client)
        db.session.flush()

        links_data = json.loads(request.form.get('links', '[]'))
        for i, link_data in enumerate(links_data):
            link = Link(
                client_id=client.id,
                platform=link_data.get('platform', 'custom'),
                url=link_data.get('url', ''),
                display_order=i,
            )
            db.session.add(link)

        db.session.commit()

        site_url = current_app.config['SITE_URL']
        generate_assets(slug, brand_name, tagline, site_url, logo_filename=logo_filename, card_style=card_style)

        flash('Card created successfully!', 'success')
        return redirect(url_for('dashboard.card_view', id=client.id))

    return render_template('dashboard/card_new.html', form=form)


@dashboard_bp.route('/card/<int:id>')
@login_required
def card_view(id):
    client = Client.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    links = Link.query.filter_by(client_id=client.id).order_by(Link.display_order).all()
    return render_template('dashboard/card_view.html', client=client, links=links)


@dashboard_bp.route('/card/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def card_edit(id):
    client = Client.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = CardForm(obj=client)

    if form.validate_on_submit():
        brand_name = form.brand_name.data.strip()
        client.brand_name = brand_name
        client.tagline = form.tagline.data.strip() if form.tagline.data else ''
        client.card_style = request.form.get('card_style', client.card_style)

        if form.logo.data:
            client.logo_filename = save_logo(form.logo.data)

        Link.query.filter_by(client_id=client.id).delete()

        links_data = json.loads(request.form.get('links', '[]'))
        for i, link_data in enumerate(links_data):
            link = Link(
                client_id=client.id,
                platform=link_data.get('platform', 'custom'),
                url=link_data.get('url', ''),
                display_order=i,
            )
            db.session.add(link)

        db.session.commit()

        site_url = current_app.config['SITE_URL']
        generate_assets(client.slug, brand_name, client.tagline, site_url, logo_filename=client.logo_filename, card_style=client.card_style)

        flash('Card updated successfully!', 'success')
        return redirect(url_for('dashboard.card_view', id=client.id))

    links = Link.query.filter_by(client_id=client.id).order_by(Link.display_order).all()
    colour_map = {
        'oxblood': {'bg_hex': '#6b1f2a', 'light': False},
        'navy':    {'bg_hex': '#1a2744', 'light': False},
        'forest':  {'bg_hex': '#1a3d2b', 'light': False},
        'slate':   {'bg_hex': '#2d3748', 'light': False},
        'charcoal':{'bg_hex': '#1a1714', 'light': False},
        'linen':   {'bg_hex': '#f0ebe4', 'light': True},
        'sage':    {'bg_hex': '#e8ede8', 'light': True},
        'blush':   {'bg_hex': '#f5ece8', 'light': True},
    }
    return render_template('dashboard/card_edit.html', form=form, client=client, links=links, colour_map=colour_map)


@dashboard_bp.route('/card/<int:id>/delete', methods=['POST'])
@login_required
def card_delete(id):
    client = Client.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    order_count = Order.query.filter_by(client_id=client.id).count()
    if order_count > 0:
        flash('This card has existing orders and cannot be deleted.', 'error')
        return redirect(url_for('dashboard.card_view', id=client.id))
    db.session.delete(client)
    db.session.commit()
    flash('Card deleted.', 'success')
    return redirect(url_for('dashboard.index'))


@dashboard_bp.route('/card/<int:id>/order')
@login_required
def card_order(id):
    client = Client.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    tiers = [
        {
            'key': 'digital',
            'name': 'Digital',
            'price': 'Â£19',
            'description': 'QR code + print-ready PDF. No physical cards.',
            'includes': ['Hosted links page', 'QR code download', 'Print-ready PDF (85Ã—55mm)'],
            'quantity': None,
        },
        {
            'key': 'standard',
            'name': 'Standard',
            'price': 'Â£59',
            'description': '250 printed cards delivered to your door.',
            'includes': ['Everything in Digital', '250 printed cards', 'Matt laminate finish', 'Delivered in 5â€“7 days'],
            'quantity': 250,
        },
        {
            'key': 'premium',
            'name': 'Premium',
            'price': 'Â£85',
            'description': '500 printed cards delivered to your door.',
            'includes': ['Everything in Digital', '500 printed cards', 'Matt laminate finish', 'Delivered in 5â€“7 days'],
            'quantity': 500,
        },
    ]
    return render_template('dashboard/card_order.html', client=client, tiers=tiers)


@dashboard_bp.route('/card/<int:id>/checkout/<tier>')
@login_required
def card_checkout(id, tier):
    client = Client.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    price_map = {
        'digital':  os.environ['STRIPE_PRICE_DIGITAL'],
        'standard': os.environ['STRIPE_PRICE_STANDARD'],
        'premium':  os.environ['STRIPE_PRICE_PREMIUM'],
    }

    if tier not in price_map:
        flash('Invalid tier selected.', 'error')
        return redirect(url_for('dashboard.card_order', id=client.id))

    stripe.api_key = os.environ['STRIPE_SECRET_KEY']

    site_url = current_app.config['SITE_URL'].rstrip('/')

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_map[tier],
            'quantity': 1,
        }],
        mode='payment',
        success_url=f"{site_url}/card/{client.id}?order=success",
        cancel_url=f"{site_url}/card/{client.id}/order",
        metadata={
            'client_id': str(client.id),
            'user_id': str(current_user.id),
            'tier': tier,
        },
        billing_address_collection='required',
    )

    return redirect(session.url, code=303)


@dashboard_bp.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    stripe.api_key = os.environ['STRIPE_SECRET_KEY']
    webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET', '')
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature', '')

    if webhook_secret:
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        except stripe.error.SignatureVerificationError:
            abort(400)
    else:
        import json as _json
        event = _json.loads(payload)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        meta = session.get('metadata', {})
        client_id = int(meta.get('client_id', 0))
        user_id = int(meta.get('user_id', 0))
        tier = meta.get('tier', 'digital')

        quantity_map = {
            'digital': 0,
            'standard': 250,
            'premium': 500,
        }
        amount_map = {
            'digital': 19.00,
            'standard': 59.00,
            'premium': 85.00,
        }

        existing = Order.query.filter_by(
            stripe_session_id=session['id']
        ).first()

        if not existing:
            order = Order(
                user_id=user_id,
                client_id=client_id,
                tier=tier,
                quantity=quantity_map.get(tier, 0),
                amount_paid=amount_map.get(tier, 0),
                stripe_session_id=session['id'],
                stripe_payment_id=session.get('payment_intent', ''),
                status='paid',
            )
            db.session.add(order)
            db.session.commit()

    return '', 200


@dashboard_bp.route('/orders')
@login_required
def orders():
    all_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('dashboard/orders.html', orders=all_orders)


@dashboard_bp.route('/card/<int:id>/download/pdf')
@login_required
def download_pdf(id):
    import os
    client = Client.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    has_paid = Order.query.filter_by(
        client_id=client.id,
        user_id=current_user.id
    ).filter(Order.status != 'pending').first()
    if not has_paid:
        flash('Purchase a plan to download your PDF.', 'info')
        return redirect(url_for('dashboard.card_order', id=client.id))
    public_url = os.environ['R2_PUBLIC_URL'].rstrip('/')
    return redirect(f"{public_url}/generated/{client.slug}/card.pdf")


@dashboard_bp.route('/card/<int:id>/download/qr')
@login_required
def download_qr(id):
    import os
    client = Client.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    has_paid = Order.query.filter_by(
        client_id=client.id,
        user_id=current_user.id
    ).filter(Order.status != 'pending').first()
    if not has_paid:
        flash('Purchase a plan to download your QR code.', 'info')
        return redirect(url_for('dashboard.card_order', id=client.id))
    public_url = os.environ['R2_PUBLIC_URL'].rstrip('/')
    return redirect(f"{public_url}/generated/{client.slug}/qr.png")

```

### app/public/routes.py
```python
from flask import Blueprint, render_template, abort
from app.models import Client

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def index():
    return render_template('public/index.html')


@public_bp.route('/c/<slug>')
def card_links(slug):
    client = Client.query.filter_by(slug=slug).first_or_404()
    links = client.links.order_by('display_order').all()
    return render_template('public/links.html', client=client, links=links)

```

### app/admin/routes.py
```python
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
        from app.services.email import send_status_update
        send_status_update(order, order.client, order.user)
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



```

### app/auth/routes.py
```python
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db
from app.auth.forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard.index'))
        flash('Invalid email or password', 'error')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('auth/register.html', form=form)

        user = User(email=email)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('dashboard.index'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.index'))

```

## 5. Route Table

| METHOD | Route | Endpoint Name | Template Rendered |
|--------|-------|---------------|-------------------|
| GET | / | public.index | public/index.html |
| GET | /c/<slug> | public.card_links | public/links.html |
| GET, POST | /login | auth.login | auth/login.html |
| GET, POST | /register | auth.register | auth/register.html |
| GET | /logout | auth.logout | redirect -> public.index |
| GET | /dashboard | dashboard.index | dashboard/index.html |
| GET, POST | /card/new | dashboard.card_new | dashboard/card_new.html |
| GET | /card/<int:id> | dashboard.card_view | dashboard/card_view.html |
| GET, POST | /card/<int:id>/edit | dashboard.card_edit | dashboard/card_edit.html |
| POST | /card/<int:id>/delete | dashboard.card_delete | redirect -> dashboard.index |
| GET | /card/<int:id>/order | dashboard.card_order | dashboard/card_order.html |
| GET | /card/<int:id>/checkout/<tier> | dashboard.card_checkout | redirect -> Stripe |
| POST | /webhook/stripe | dashboard.stripe_webhook | none (200 empty) |
| GET | /orders | dashboard.orders | dashboard/orders.html |
| GET | /card/<int:id>/download/pdf | dashboard.download_pdf | redirect -> R2 PDF |
| GET | /card/<int:id>/download/qr | dashboard.download_qr | redirect -> R2 QR |
| GET | /admin | admin.index | admin/index.html |
| GET | /admin/users | admin.users | admin/users.html |
| GET, POST | /admin/orders | admin.orders | admin/orders.html |
| GET | /admin/revenue | admin.revenue | admin/revenue.html |

## 6. Template Inheritance (Layout Extension)

ALL templates extend a layout; none are standalone. The inheritance chain:

| Template | Extends |
|---|---|
| `templates/layouts/base.html` | — (root layout) |
| `templates/layouts/dashboard.html` | `layouts/base.html` |
| `templates/layouts/admin.html` | `layouts/base.html` |
| `templates/public/index.html` | `layouts/base.html` |
| `templates/public/links.html` | `layouts/base.html` |
| `templates/auth/login.html` | `layouts/base.html` |
| `templates/auth/register.html` | `layouts/base.html` |
| `templates/dashboard/index.html` | `layouts/dashboard.html` |
| `templates/dashboard/card_new.html` | `layouts/dashboard.html` |
| `templates/dashboard/card_view.html` | `layouts/dashboard.html` |
| `templates/dashboard/card_edit.html` | `layouts/dashboard.html` |
| `templates/dashboard/card_order.html` | `layouts/dashboard.html` |
| `templates/dashboard/orders.html` | `layouts/dashboard.html` |
| `templates/admin/index.html` | `layouts/admin.html` |
| `templates/admin/users.html` | `layouts/admin.html` |
| `templates/admin/orders.html` | `layouts/admin.html` |
| `templates/admin/revenue.html` | `layouts/admin.html` |

## 7. Inline JavaScript Summary

Three templates contain inline JavaScript:

### `dashboard/card_new.html`

- **Live preview**: On `#brand-input` / `#tagline-input` input events, `updatePreview()` updates the card front preview (brand name, initial letter, tagline, divider visibility, text/logo colours) in real time.
- **Colour swatches**: Clicking a `.card-new-swatch-wrap` updates `currentBg`, `isLight`, sets the hidden `#card-style-input`, and calls `updatePreview()`. Light vs dark determines text colour and box-shadow style.
- **Add/remove link rows**: `addLink()` dynamically appends a `.link-row` div with platform and URL fields, incrementing `linkCount`.
- **Form submit**: On `#card-form` submit, iterates all `.link-row` elements, collects `{platform, url}` pairs, serializes to JSON, and writes to hidden `#links-json` input.
- **Initialization**: On page load, sets `currentBg`, `isLight`, applies background to `#preview-front`, and calls `updatePreview()`.

### `dashboard/card_edit.html`

- **Live preview**: On `#input-brand` / `#input-tagline` input events, `updatePreview()` dynamically renders the card front inner HTML (A1 layout with tagline or A3 layout without), adjusting logo size, divider, text colour, and font sizes.
- **Colour swatches**: `selectColour(style, hex, light)` updates `currentBg`, `isLight`, sets `#card-style-input`, updates `#preview-front` background, toggles `.selected` class on swatches, and calls `updatePreview()`.
- **Add link rows**: Same `addLink()` pattern as `card_new.html`.
- **Form submit**: Serializes link rows into JSON hidden input before POST.
- **Initialization**: Reads Jinja-rendered `currentBg` / `isLight` from template variables and calls `updatePreview()` on load.

### `admin/orders.html`

- **Toggle address**: Each order row has an inline `onclick` handler toggling `display:none/table-row` on the corresponding `#addr-{{ order.id }}` hidden row, revealing delivery address details.

