import os
from app import create_app, db

app = create_app(os.environ.get('FLASK_CONFIG'))

with app.app_context():
    os.makedirs(os.path.join(app.static_folder, 'generated'), exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, 'uploads'), exist_ok=True)

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5001
    app.run(debug=True, host='0.0.0.0', port=port)
