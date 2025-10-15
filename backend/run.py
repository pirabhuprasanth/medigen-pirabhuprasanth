# backend/run.py
from app import create_app
from app.models import db
import os

# Create app with environment-specific configuration
app = create_app()

if __name__ == '__main__':
    # Ensure database tables are created
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created successfully!")
        except Exception as e:
            print(f"❌ Error creating database tables: {e}")
    
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    debug = app.config.get('DEBUG', True)
    
    print(f"🚀 Starting MediCare API on port {port}")
    print(f"🔧 Debug mode: {'ON' if debug else 'OFF'}")
    print(f"🌐 API URL: http://localhost:{port}")
    print(f"📋 Health Check: http://localhost:{port}/")
    print(f"🔐 API Endpoints: http://localhost:{port}/api/")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )