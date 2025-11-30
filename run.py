#!/usr/bin/env python3
"""
Startup script for Electrical Construction PM Application
"""

import os
import sys
from app import app, db

def initialize_database():
    """Initialize the database with tables"""
    print("Initializing database...")
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")

def run_development_server():
    """Run the development server"""
    print("Starting Electrical PM Application...")
    print("Access the application at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    try:
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'flask', 'flask_cors', 'flask_sqlalchemy', 
        'numpy', 'pandas', 'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using:")
        print(f"pip install {' '.join(missing_packages)}")
        print("Or run: pip install -r requirements.txt")
        return False
    
    return True

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = ['uploads', 'static', 'models']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Directory created/verified: {directory}")

def main():
    """Main function to start the application"""
    print("=" * 60)
    print("ELECTRICAL CONSTRUCTION PROJECT MANAGEMENT")
    print("AI-Powered Cost Estimation & Material Management")
    print("=" * 60)
    print()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create necessary directories
    create_directories()
    
    # Initialize database
    initialize_database()
    
    print()
    print("Application ready!")
    print("Features available:")
    print("• Project creation and management")
    print("• Electrical calculations (load flow, voltage drop, fault current)")
    print("• AI-powered cost estimation")
    print("• Real-time material pricing")
    print("• Risk assessment and project tracking")
    print()
    
    # Start the server
    run_development_server()

if __name__ == '__main__':
    main()