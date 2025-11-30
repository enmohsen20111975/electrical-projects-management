#!/usr/bin/env python3
"""
Database Initialization Script for AI-Powered Electrical Construction Calculator
Creates all tables and initial data using the correct enhanced models
"""

import sys
import os
from datetime import datetime, timedelta
import logging

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def init_database():
    """Initialize the database with all tables"""
    print("=" * 50)
    print("AI-Powered Electrical Construction Calculator - Database Initialization")
    print("=" * 50)
    
    try:
        # Import app and db from the main application
        from app import app, db
        from enhanced_models import Project, BOMItem, ElectricalComponent, NECComplianceRecord, ProjectStatus, Priority, ComplianceStatus
        
        with app.app_context():
            # Initialize database
            logger.info(f"Using Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
            logger.info("Creating database tables...")
            db.create_all()
            logger.info("Database tables created successfully!")
            
            # Check if data already exists
            if Project.query.first():
                logger.info("Data already exists. Skipping sample data creation.")
                return True
            
            # Create initial test data
            logger.info("Creating initial test data...")
            create_sample_data(db, Project, BOMItem, ElectricalComponent, NECComplianceRecord, ProjectStatus, Priority, ComplianceStatus)
            
            logger.info("Database initialization completed!")
            
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False
    
    return True

def create_sample_data(db, Project, BOMItem, ElectricalComponent, NECComplianceRecord, ProjectStatus, Priority, ComplianceStatus):
    """Create sample data for testing"""
    
    # Create sample project
    sample_project = Project(
        name="Office Building Electrical System",
        description="Complete electrical infrastructure for 5-story office building",
        status=ProjectStatus.PLANNING,
        priority=Priority.HIGH,
        estimated_cost=250000.00,
        start_date=datetime(2025, 1, 15),
        estimated_completion=datetime(2025, 6, 30),
        project_location="Downtown Business District",
        client_name="ABC Corporation",
        electrical_engineer="John Smith, PE",
        nec_revision="2023",
        risk_level="Medium"
    )
    
    db.session.add(sample_project)
    db.session.commit()
    
    logger.info(f"Created sample project: {sample_project.name} (ID: {sample_project.id})")
    
    # Create sample component
    component = ElectricalComponent(
        manufacturer="Schneider Electric",
        part_number="CH42MB2800",
        description="Main Service Panel 800A, 42 Circuit",
        category="Panels",
        voltage_rating="240V",
        current_rating="800A",
        current_price=2850.00,
        stock_quantity=5,
        ul_certified=True,
        nec_compliant=True,
        supplier_name="Schneider Electric",
        data_source="manual"
    )
    
    db.session.add(component)
    db.session.commit()
    
    # Create BOM Item
    bom_item = BOMItem(
        project_id=sample_project.id,
        component_id=component.id,
        quantity_required=1,
        unit_cost=2850.00,
        total_cost=2850.00,
        status='planned',
        priority=Priority.HIGH,
        required_date=datetime(2025, 2, 1)
    )
    
    db.session.add(bom_item)
    db.session.commit()
    
    logger.info(f"Created sample BOM item for project {sample_project.id}")
    
    # Create NEC Compliance Record
    nec_record = NECComplianceRecord(
        project_id=sample_project.id,
        component_id=component.id,
        bom_item_id=bom_item.id,
        nec_section="408.36",
        requirement_description="Overcurrent protection for panelboards",
        compliance_status=ComplianceStatus.COMPLIANT,
        findings="Main breaker provided within panelboard",
        risk_level="Low",
        reviewed_by="Automated System"
    )
    
    db.session.add(nec_record)
    db.session.commit()
    
    logger.info("Created sample NEC compliance record")

if __name__ == "__main__":
    success = init_database()
    if success:
        print("\n" + "=" * 50)
        print("Database initialization completed successfully!")
        print("You can now run the application with:")
        print("python app.py")
        print("=" * 50)
    else:
        print("\nDatabase initialization failed. Please check the error messages above.")
        sys.exit(1)