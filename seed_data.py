#!/usr/bin/env python3
"""
Sample data seeding script for Electrical PM Application
"""

import json
import random
from datetime import datetime, timedelta
from app import app
from models import db, Project, Material, HistoricalProject

def seed_projects():
    """Create sample projects"""
    projects = [
        {
            'name': 'Industrial Complex Phase 1',
            'description': 'New 50,000 sq ft manufacturing facility electrical installation',
            'type': 'industrial',
            'status': 'in_progress',
            'start_date': datetime.now() - timedelta(days=30),
            'end_date': datetime.now() + timedelta(days=90),
            'budget': 485000.00,
            'actual_cost': 145000.00,
            'progress': 30.0,
            'voltage_level': '480V',
            'square_footage': 50000,
            'num_circuits': 200
        },
        {
            'name': 'Downtown Office Tower',
            'description': 'Complete electrical system for 15-story office building',
            'type': 'commercial',
            'status': 'planning',
            'start_date': datetime.now() + timedelta(days=14),
            'end_date': datetime.now() + timedelta(days=365),
            'budget': 1250000.00,
            'actual_cost': 25000.00,
            'progress': 5.0,
            'voltage_level': '480V',
            'square_footage': 225000,
            'num_circuits': 800
        },
        {
            'name': 'Residential Subdivision Phase 2',
            'description': 'Electrical infrastructure for 45-home residential development',
            'type': 'residential',
            'status': 'completed',
            'start_date': datetime.now() - timedelta(days=180),
            'end_date': datetime.now() - timedelta(days=30),
            'budget': 285000.00,
            'actual_cost': 275000.00,
            'progress': 100.0,
            'voltage_level': '240V',
            'square_footage': 54000,
            'num_circuits': 135
        },
        {
            'name': 'Substation Upgrade Project',
            'description': '13.8kV to 480V distribution system upgrade',
            'type': 'utility_scale',
            'status': 'on_hold',
            'start_date': datetime.now() - timedelta(days=60),
            'end_date': datetime.now() + timedelta(days=120),
            'budget': 750000.00,
            'actual_cost': 95000.00,
            'progress': 15.0,
            'voltage_level': '13800V',
            'square_footage': 0,
            'num_circuits': 50
        },
        {
            'name': 'Shopping Center Renovation',
            'description': 'Electrical modernization for existing retail center',
            'type': 'commercial',
            'status': 'in_progress',
            'start_date': datetime.now() - timedelta(days=15),
            'end_date': datetime.now() + timedelta(days=45),
            'budget': 195000.00,
            'actual_cost': 65000.00,
            'progress': 35.0,
            'voltage_level': '480V',
            'square_footage': 75000,
            'num_circuits': 180
        }
    ]
    
    created_projects = []
    
    with app.app_context():
        for project_data in projects:
            project = Project(
                name=project_data['name'],
                description=project_data['description'],
                status=project_data['status'],
                start_date=project_data['start_date'],
                end_date=project_data['end_date'],
                budget=project_data['budget'],
                actual_cost=project_data['actual_cost'],
                progress=project_data['progress']
            )
            db.session.add(project)
            created_projects.append(project)
        
        db.session.commit()
        print(f"Created {len(created_projects)} sample projects")
    
    return created_projects

def seed_materials(projects):
    """Create sample material data"""
    materials_data = [
        {
            'project_id': 1,  # Industrial Complex
            'name': 'Copper THHN 12 AWG',
            'category': 'cables',
            'quantity': 2500.0,
            'unit_cost': 0.85,
            'total_cost': 2125.00,
            'supplier': 'Graybar',
            'specifications': {'voltage_rating': '600V', ' insulation': 'THHN'}
        },
        {
            'project_id': 1,
            'name': '20A Circuit Breakers',
            'category': 'breakers',
            'quantity': 45.0,
            'unit_cost': 45.00,
            'total_cost': 2025.00,
            'supplier': 'Square D',
            'specifications': {'interrupt_capacity': '10kA', 'voltage': '120/240V'}
        },
        {
            'project_id': 1,
            'name': 'EMT Conduit 1/2"',
            'category': 'conduit',
            'quantity': 1200.0,
            'unit_cost': 1.25,
            'total_cost': 1500.00,
            'supplier': 'WESCO',
            'specifications': {'material': 'Steel', 'wall_thickness': '0.042"'}
        },
        {
            'project_id': 2,  # Downtown Office Tower
            'name': '50kVA Transformer',
            'category': 'transformers',
            'quantity': 3.0,
            'unit_cost': 1850.00,
            'total_cost': 5550.00,
            'supplier': 'Schneider Electric',
            'specifications': {'primary_voltage': '480V', 'secondary_voltage': '208Y/120V'}
        },
        {
            'project_id': 2,
            'name': 'Copper THHN 10 AWG',
            'category': 'cables',
            'quantity': 8500.0,
            'unit_cost': 1.35,
            'total_cost': 11475.00,
            'supplier': 'Graybar',
            'specifications': {'voltage_rating': '600V', 'insulation': 'THHN'}
        },
        {
            'project_id': 3,  # Residential Subdivision
            'name': 'Copper THHN 12 AWG',
            'category': 'cables',
            'quantity': 3200.0,
            'unit_cost': 0.82,
            'total_cost': 2624.00,
            'supplier': 'WESCO',
            'specifications': {'voltage_rating': '600V', 'insulation': 'THHN'}
        },
        {
            'project_id': 3,
            'name': '200A Main Panel',
            'category': 'panels',
            'quantity': 15.0,
            'unit_cost': 285.00,
            'total_cost': 4275.00,
            'supplier': 'Square D',
            'specifications': {'mains': '200A', 'circuits': 42, 'voltage': '120/240V'}
        }
    ]
    
    with app.app_context():
        for material_data in materials_data:
            material = Material(
                project_id=material_data['project_id'],
                name=material_data['name'],
                category=material_data['category'],
                quantity=material_data['quantity'],
                unit_cost=material_data['unit_cost'],
                total_cost=material_data['total_cost'],
                supplier=material_data['supplier'],
                specifications=json.dumps(material_data['specifications'])
            )
            db.session.add(material)
        
        db.session.commit()
        print(f"Created {len(materials_data)} sample material records")

def seed_historical_projects():
    """Create historical project data for AI training"""
    historical_data = [
        {
            'project_name': 'Tech Campus Phase 1',
            'project_type': 'commercial',
            'electrical_scope': {
                'voltage_levels': ['480V', '208V'],
                'total_load_kva': 500,
                'num_panels': 25,
                'num_circuits': 400,
                'cable_miles': 2.5,
                'transformers': 4
            },
            'actual_cost': 950000.00,
            'final_duration': 180,
            'success_factors': ['Early material procurement', 'Experienced crew', 'Good weather'],
            'challenges': ['Permit delays', 'Spec changes', 'Coordination issues']
        },
        {
            'project_name': 'Manufacturing Plant',
            'project_type': 'industrial',
            'electrical_scope': {
                'voltage_levels': ['480V', '240V'],
                'total_load_kva': 1200,
                'num_panels': 45,
                'num_circuits': 650,
                'cable_miles': 4.2,
                'transformers': 8
            },
            'actual_cost': 1850000.00,
            'final_duration': 270,
            'success_factors': ['Detailed planning', 'Quality materials', 'Strong PM'],
            'challenges': ['Heavy load requirements', 'Tight schedule', 'Coordination complexity']
        },
        {
            'project_name': 'Luxury Condominiums',
            'project_type': 'residential',
            'electrical_scope': {
                'voltage_levels': ['240V', '120V'],
                'total_load_kva': 200,
                'num_panels': 60,
                'num_circuits': 240,
                'cable_miles': 1.8,
                'transformers': 2
            },
            'actual_cost': 425000.00,
            'final_duration': 120,
            'success_factors': ['Standard design', 'Experienced crew', 'Good access'],
            'challenges': ['Quality requirements', 'Inspection delays', 'Coordination with finishes']
        },
        {
            'project_name': 'Distribution Substation',
            'project_type': 'utility_scale',
            'electrical_scope': {
                'voltage_levels': ['13800V', '480V'],
                'total_load_kva': 5000,
                'num_panels': 15,
                'num_circuits': 85,
                'cable_miles': 0.5,
                'transformers': 6
            },
            'actual_cost': 2850000.00,
            'final_duration': 365,
            'success_factors': ['Expert crew', 'Quality equipment', 'Detailed engineering'],
            'challenges': ['High voltage safety', 'Specialized equipment', 'Testing requirements']
        }
    ]
    
    with app.app_context():
        for hist_data in historical_data:
            historical_project = HistoricalProject(
                project_name=hist_data['project_name'],
                project_type=hist_data['project_type'],
                electrical_scope=json.dumps(hist_data['electrical_scope']),
                actual_cost=hist_data['actual_cost'],
                final_duration=hist_data['final_duration'],
                success_factors=json.dumps(hist_data['success_factors']),
                challenges=json.dumps(hist_data['challenges']),
                completed_date=datetime.now() - timedelta(days=random.randint(30, 365))
            )
            db.session.add(historical_project)
        
        db.session.commit()
        print(f"Created {len(historical_data)} historical project records for AI training")

def main():
    """Main seeding function"""
    print("Seeding Electrical PM Application with sample data...")
    print("=" * 60)
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Seed data
        projects = seed_projects()
        seed_materials(projects)
        seed_historical_projects()
        
        print("=" * 60)
        print("Sample data seeding completed!")
        print("\nYou can now:")
        print("1. Run 'python run.py' to start the application")
        print("2. Access http://localhost:5000 to view the dashboard")
        print("3. Explore projects, calculations, and material estimates")
        print("\nSample projects include:")
        print("• Industrial Complex Phase 1 (30% complete)")
        print("• Downtown Office Tower (Planning)")
        print("• Residential Subdivision Phase 2 (Completed)")
        print("• Substation Upgrade Project (On Hold)")
        print("• Shopping Center Renovation (35% complete)")

if __name__ == '__main__':
    main()