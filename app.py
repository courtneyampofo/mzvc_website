import os
from church_website import app, init_db

if __name__ == '__main__':
    # Ensure uploads directory exists
    os.makedirs('uploads', exist_ok=True)
    
    # Initialize database
    init_db()
    
    print("Church Website is running!")
    print("Default admin credentials: username: admin, password: admin123")
    print("Visit http://localhost:5000 to view the website")
    print("Admin dashboard: http://localhost:5000/admin")
    
    # For production deployment, don't run the app here
    # The hosting platform will handle this
    if os.environ.get('RENDER') or os.environ.get('HEROKU'):
        # Production environment - don't run locally
        pass
    else:
        # Development environment - run locally
        app.run(debug=True, host='0.0.0.0', port=5000)
