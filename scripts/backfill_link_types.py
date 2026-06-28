from app import create_app, db
from app.models import Link

app = create_app()

with app.app_context():
    links = Link.query.all()
    mapping = {
        'website': 'website',
        'instagram': 'instagram',
    }
    updated = 0
    for link in links:
        normalized = (link.platform or '').strip().lower()
        new_type = mapping.get(normalized, 'custom')
        if link.link_type != new_type:
            link.link_type = new_type
            updated += 1
    db.session.commit()
    print(f"Updated {updated} of {len(links)} links.")
