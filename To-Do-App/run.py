from app import create_app, db
import os

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✓ Database ready")
        
    is_production = os.environ.get('FLASK_ENV') == 'production'

    app.run(
        debug=not is_production,
        host='0.0.0.0'
    )