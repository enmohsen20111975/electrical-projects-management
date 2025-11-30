#!/usr/bin/env python3
"""
Final Database Initialization Script for Enhanced Electrical Construction PM
Creates all tables and initial data with correct field names
"""

import sys
import os
from datetime import datetime

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from enhanced_models import db, Project, BOMItem, ChangeRequest, ElectricalComponent, NECComplianceRecord, SupplierQuotation
    from enhanced_config import BaseConfig
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

def init_database():
    """Initialize the database with all tables"""
    print("=" * 60)
    print("Enhanced Electrical Construction PM - Database Initialization")
    print("=" * 60)
    
    try:
        # Configure Flask app with database
        from flask import Flask
        app = Flask(__name__)
        app.config.from_object(BaseConfig)
        
        # Set up the database URI
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///enhanced_electrical_pm.db')
        
        with app.app_context():
            # Initialize database
            print("[INFO] Creating database tables...")
            db.init_app(app)
            
            # Create all tables
            db.create_all()
            
            print("[SUCCESS] Database tables created successfully!")
            
            # Create initial test data
            print("[INFO] Creating initial test data...")
            create_sample_data()
            
            print("[SUCCESS] Database initialization completed!")
            
    except Exception as e:
        print(f"[ERROR] Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def create_sample_data():
    """Create sample data for testing"""
    
    # Create sample electrical components first
    components = [
        ElectricalComponent(
            manufacturer="Schneider Electric",
            part_number="CH42MB2800",
            description="Main Service Panel 800A, 42 Circuit",
            category="panels",
            voltage_rating="480V",
            current_rating="800A",
            dimensions="36\" x 16\" x 6\"",
            enclosure_rating="NEMA 1",
            base_price=2850.00,
            current_price=2850.00,
            stock_quantity=5,
            lead_time_days=14,
            supplier_id="se001",
            supplier_name="Schneider Electric",
            supplier_sku="CH42MB2800",
            ul_certified=True,
            nec_compliant=True,
            datasheet_url="https://www.se.com/datasheet/ch42mb2800",
            data_source="manual"
        ),
        ElectricalComponent(
            manufacturer="Square D",
            part_number="QA120020",
            description="Circuit Breaker 20A, 1-Pole, 120V",
            category="circuit_breakers",
            voltage_rating="120V",
            current_rating="20A",
            dimensions="1\" x 3\" x 2.5\"",
            mounting_type="din_rail",
            base_price=45.00,
            current_price=45.00,
            stock_quantity=50,
            lead_time_days=7,
            supplier_id="sd001",
            supplier_name="Square D",
            supplier_sku="QA120020",
            ul_certified=True,
            nec_compliant=True,
            datasheet_url="https://www.squared.com/datasheet/qa120020",
            data_source="manual"
        ),
        ElectricalComponent(
            manufacturer="Southwire",
            part_number="EMT-1-10",
            description="Conduit EMT 1 inch, 10 ft length",
            category="conduit",
            voltage_rating="600V",
            current_rating="N/A",
            dimensions="10 ft length",
            base_price=2.50,
            current_price=2.50,
            stock_quantity=1000,
            lead_time_days=3,
            supplier_id="sw001",
            supplier_name="Southwire",
            supplier_sku="EMT-1-10",
            ul_certified=True,
            nec_compliant=True,
            datasheet_url="https://www.southwire.com/datasheet/emt-1-10",
            data_source="manual"
        )
    ]
    
    for component in components:
        db.session.add(component)
    
    db.session.commit()
    print(f"[INFO] Created {len(components)} sample electrical components")
    
    # Create sample project
    sample_project = Project(
        name="Office Building Electrical System",
        description="Complete electrical infrastructure for 5-story office building",
        project_number="ELEC-2025-001",
        status="planning",
        priority="high",
        client_name="ABC Corporation",
        client_contact="John Doe, PE",
        project_location="Downtown Business District",
        address="123 Main Street",
        city="Metro City",
        state="CA",
        zip_code="90210",
        start_date=datetime(2025, 1, 15),
        estimated_completion=datetime(2025, 6, 30),
        estimated_cost=250000.00,
        square_footage=25000,
        occupancy_type="Business Group B",
        service_voltage="480V/277V",
        main_panel_rating=800,
        estimated_load=600
    )
    
    db.session.add(sample_project)
    db.session.commit()
    
    print(f"[INFO] Created sample project: {sample_project.name} (ID: {sample_project.id})")
    
    # Create sample BOM items
    bom_items = []
    for i, component in enumerate(components):
        bom_item = BOMItem(
            project_id=sample_project.id,
            component_id=component.id,
            quantity_required=1 if i == 0 else (24 if i == 1 else 500),
            unit_cost=component.current_price,
            total_cost=component.current_price * (1 if i == 0 else (24 if i == 1 else 500)),
            status="planned",
            priority="high" if i == 0 else "medium",
            required_date=datetime(2025, 2, 1) if i == 0 else datetime(2025, 1, 20),
            modified_by="System Admin"
        )
        bom_items.append(bom_item)
        db.session.add(bom_item)
    
    db.session.commit()
    
    print(f"[INFO] Created {len(bom_items)} sample BOM items")
    
    # Create sample NEC compliance record
    nec_compliance = NECComplianceRecord(
        project_id=sample_project.id,
        nec_version="2023",
        compliance_status="pending_review",
        section_310_60_compliant=True,
        section_430_52_compliant=True,
        section_250_4_compliant=True,
        section_440_14_compliant=True,
        compliance_score=0.95,
        last_checked=datetime.now(),
        checked_by="Automated System",
        notes="All major NEC sections compliant. Minor adjustments needed for conduit fill calculations."
    )
    
    db.session.add(nec_compliance)
    db.session.commit()
    
    print(f"[INFO] Created sample NEC compliance record (Score: {nec_compliance.compliance_score})")

if __name__ == "__main__":
    success = init_database()
    if success:
        print("\n" + "=" * 60)
        print("✅ Database initialization completed successfully!")
        print("You can now run the enhanced application with:")
        print("python enhanced_app.py")
        print("Access the application at: http://localhost:5000")
        print("=" * 60)
    else:
        print("\n❌ Database initialization failed. Please check the error messages above.")
        sys.exit(1)