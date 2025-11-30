"""
Enhanced Flask Application for Electrical Construction Project Management
Addresses real industry pain points with real-time data integration and NEC compliance
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional
import logging
from functools import wraps

# Import our custom modules
from enhanced_models import *
from supplier_integration import ElectricalComponentsDatabase, create_components_database
from ai_engine import ElectricalCalculator
from config import config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config[os.getenv('FLASK_ENV', 'development')])

# Initialize extensions
db.init_app(app)
CORS(app)

# Initialize components database
components_db = create_components_database(app.config)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# INDUSTRY PAIN POINT SOLUTIONS - API ROUTES
# ============================================================================

@app.route('/')
def dashboard():
    """Main dashboard with real-time project overview"""
    try:
        projects = Project.query.all()
        
        # Calculate dashboard metrics
        total_projects = len(projects)
        active_projects = len([p for p in projects if p.status in [ProjectStatus.IN_PROGRESS, ProjectStatus.DESIGN]])
        completed_projects = len([p for p in projects if p.status == ProjectStatus.COMPLETED])
        high_priority_projects = len([p for p in projects if p.priority == Priority.CRITICAL])
        
        # Calculate financial metrics
        total_estimated_cost = sum(p.estimated_cost for p in projects)
        total_actual_cost = sum(p.actual_cost for p in projects)
        
        # Calculate compliance metrics
        compliance_issues = 0
        nec_violations = 0
        
        for project in projects:
            for compliance in project.compliance_records:
                if compliance.compliance_status in [ComplianceStatus.NON_COMPLIANT, ComplianceStatus.REQUIRES_CORRECTION]:
                    compliance_issues += 1
                    if compliance.risk_level == 'Critical':
                        nec_violations += 1
        
        # Get recent supplier integration activities
        recent_activities = SupplierIntegrationLog.query.filter(
            SupplierIntegrationLog.timestamp >= datetime.now() - timedelta(days=7)
        ).order_by(SupplierIntegrationLog.timestamp.desc()).limit(10).all()
        
        # Get projects with BOM data
        projects_with_bom = []
        for project in projects:
            bom_summary = project.get_bom_summary()
            supplier_summary = project.get_supplier_summary()
            compliance_summary = project.get_compliance_summary()
            
            projects_with_bom.append({
                'project': project,
                'bom_summary': bom_summary,
                'supplier_summary': supplier_summary,
                'compliance_summary': compliance_summary,
                'performance_metrics': project.get_performance_metrics()
            })
        
        dashboard_data = {
            'projects': projects_with_bom,
            'metrics': {
                'total_projects': total_projects,
                'active_projects': active_projects,
                'completed_projects': completed_projects,
                'high_priority_projects': high_priority_projects,
                'total_estimated_cost': total_estimated_cost,
                'total_actual_cost': total_actual_cost,
                'budget_variance': total_actual_cost - total_estimated_cost,
                'compliance_issues': compliance_issues,
                'nec_violations': nec_violations
            },
            'recent_activities': recent_activities,
            'last_updated': datetime.now().isoformat()
        }
        
        return render_template('enhanced_dashboard.html', dashboard_data=dashboard_data)
    
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        return render_template('error.html', error=str(e))

@app.route('/api/projects', methods=['GET', 'POST'])
def api_projects():
    """Handle project CRUD operations"""
    if request.method == 'GET':
        try:
            projects = Project.query.all()
            return jsonify({
                'success': True,
                'projects': [project.to_dict() for project in projects],
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['name', 'client_name', 'project_location']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
            
            # Create new project
            project = Project(
                name=data['name'],
                description=data.get('description', ''),
                client_name=data['client_name'],
                project_location=data['project_location'],
                priority=Priority(data.get('priority', 'medium').lower()),
                estimated_cost=data.get('estimated_cost', 0.0),
                project_manager=data.get('project_manager', ''),
                lead_engineer=data.get('lead_engineer', ''),
                nec_revision=data.get('nec_revision', '2023'),
                start_date=datetime.fromisoformat(data['start_date']) if data.get('start_date') else None,
                estimated_completion=datetime.fromisoformat(data['estimated_completion']) if data.get('estimated_completion') else None
            )
            
            db.session.add(project)
            db.session.commit()
            
            # Log supplier integration setup
            if project.supplier_integration_status == SupplierIntegrationStatus.INTEGRATED:
                integration_log = SupplierIntegrationLog(
                    supplier_name='System',
                    integration_type='system',
                    activity_type='project_creation',
                    status='success',
                    message=f'Project {project.name} created with supplier integration enabled',
                    project_id=project.id
                )
                db.session.add(integration_log)
                db.session.commit()
            
            return jsonify({
                'success': True,
                'project': project.to_dict(),
                'message': 'Project created successfully'
            })
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Project creation error: {e}")
            return jsonify({'success': False, 'error': str(e)})

@app.route('/api/projects/<int:project_id>', methods=['GET', 'PUT', 'DELETE'])
def api_project_detail(project_id):
    """Handle single project operations"""
    project = Project.query.get_or_404(project_id)
    
    if request.method == 'GET':
        try:
            project_data = project.to_dict()
            project_data['bom_items'] = [{
                'id': item.id,
                'component': item.component.to_dict() if item.component else None,
                'quantity_required': item.quantity_required,
                'quantity_allocated': item.quantity_allocated,
                'unit_cost': item.unit_cost,
                'total_cost': item.total_cost,
                'status': item.status,
                'priority': item.priority.value,
                'required_date': item.required_date.isoformat() if item.required_date else None,
                'status_info': item.get_status_info()
            } for item in project.bom_items]
            
            project_data['supplier_quotations'] = [{
                'id': quote.id,
                'supplier_name': quote.supplier_name,
                'part_number': quote.part_number,
                'unit_price': quote.unit_price,
                'quantity_quoted': quote.quantity_quoted,
                'availability': quote.availability,
                'lead_time_days': quote.lead_time_days,
                'created_date': quote.created_date.isoformat(),
                'is_valid': quote.is_quote_valid(),
                'quote_age_days': quote.get_quote_age_days(),
                'total_cost': quote.get_total_cost(quote.quantity_quoted)
            } for quote in project.supplier_quotations]
            
            project_data['compliance_records'] = [{
                'id': record.id,
                'nec_section': record.nec_section,
                'requirement_description': record.requirement_description,
                'compliance_status': record.compliance_status.value,
                'findings': record.findings,
                'recommendations': record.recommendations,
                'risk_level': record.risk_level,
                'reviewed_by': record.reviewed_by,
                'review_date': record.review_date.isoformat(),
                'get_risk_priority': record.get_risk_priority()
            } for record in project.compliance_records]
            
            return jsonify({
                'success': True,
                'project': project_data
            })
            
        except Exception as e:
            logger.error(f"Project detail error: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            
            # Update project fields
            if 'name' in data:
                project.name = data['name']
            if 'description' in data:
                project.description = data['description']
            if 'status' in data:
                project.status = ProjectStatus(data['status'])
            if 'priority' in data:
                project.priority = Priority(data['priority'])
            if 'estimated_cost' in data:
                project.estimated_cost = data['estimated_cost']
            if 'actual_cost' in data:
                project.actual_cost = data['actual_cost']
                project.budget_variance = data['actual_cost'] - project.estimated_cost
            if 'progress_percentage' in data:
                project.progress_percentage = data['progress_percentage']
            
            # Update timeline
            if 'start_date' in data and data['start_date']:
                project.start_date = datetime.fromisoformat(data['start_date'])
            if 'estimated_completion' in data and data['estimated_completion']:
                project.estimated_completion = datetime.fromisoformat(data['estimated_completion'])
            
            project.last_update = datetime.now()
            db.session.commit()
            
            return jsonify({
                'success': True,
                'project': project.to_dict(),
                'message': 'Project updated successfully'
            })
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Project update error: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    elif request.method == 'DELETE':
        try:
            db.session.delete(project)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Project deleted successfully'})
        except Exception as e:
            db.session.rollback()
            logger.error(f"Project deletion error: {e}")
            return jsonify({'success': False, 'error': str(e)})

@app.route('/api/suppliers/search', methods=['POST'])
def api_supplier_search():
    """Real-time component search across all suppliers"""
    try:
        data = request.get_json()
        part_number = data.get('part_number', '').strip()
        manufacturer = data.get('manufacturer', '').strip()
        
        if not part_number:
            return jsonify({'success': False, 'error': 'Part number is required'}), 400
        
        # Search across all suppliers
        components = components_db.search_component_comprehensive(part_number, manufacturer)
        
        if not components:
            return jsonify({
                'success': False, 
                'error': 'Component not found',
                'part_number': part_number,
                'suggestions': get_component_suggestions(part_number)
            })
        
        # Enhance with compliance data
        enhanced_components = []
        for component in components:
            compliance_data = components_db.verify_certifications(component)
            
            component_data = {
                'id': component.part_number,  # Use part_number as ID for demo
                'manufacturer': component.manufacturer,
                'part_number': component.part_number,
                'description': component.description,
                'category': component.category,
                'voltage_rating': component.voltage_rating,
                'current_rating': component.current_rating,
                'price': component.price_usd,
                'currency': 'USD',
                'stock_quantity': component.stock_available,
                'supplier_name': component.supplier_id,
                'supplier_sku': component.part_number,
                'lead_time_days': component.lead_time_days,
                'ul_certified': component.ul_certified,
                'nec_compliant': component.nec_compliant,
                'datasheet_url': component.datasheet_url,
                'compliance_status': compliance_data,
                'availability_status': component.get_availability_status() if hasattr(component, 'get_availability_status') else 'Available',
                'total_cost_calculation': component.calculate_total_cost(1) if hasattr(component, 'calculate_total_cost') else {
                    'base_cost': component.price_usd,
                    'shipping_cost': component.price_usd * 0.05,
                    'tax_cost': component.price_usd * 0.08875,
                    'total_cost': component.price_usd * 1.13875,
                    'confidence': 0.85
                }
            }
            enhanced_components.append(component_data)
        
        # Log the search activity
        integration_log = SupplierIntegrationLog(
            supplier_name='Multi-Source',
            integration_type='search',
            activity_type='component_search',
            status='success',
            message=f'Searched for {part_number}, found {len(enhanced_components)} results',
            records_processed=len(enhanced_components),
            records_successful=len(enhanced_components)
        )
        db.session.add(integration_log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'components': enhanced_components,
            'search_criteria': {
                'part_number': part_number,
                'manufacturer': manufacturer
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Supplier search error: {e}")
        return jsonify({'success': False, 'error': str(e)})

def get_component_suggestions(part_number):
    """Get suggestions for similar part numbers"""
    # This would typically search a database of component descriptions
    # For now, return some generic suggestions
    suggestions = []
    
    # Common electrical components
    common_parts = ['CB1', 'SW1', 'TB1', 'MCB1', 'CONT1', 'RELAY1']
    suggestions = [part for part in common_parts if part_number.lower() in part.lower()]
    
    return suggestions[:3]  # Return top 3 suggestions

@app.route('/api/suppliers/quote', methods=['POST'])
def api_supplier_quote():
    """Get real-time pricing from multiple suppliers"""
    try:
        data = request.get_json()
        parts_list = data.get('parts', [])
        project_id = data.get('project_id')
        
        if not parts_list:
            return jsonify({'success': False, 'error': 'No parts specified'}), 400
        
        # Get quotes from all suppliers
        quotes = components_db.get_best_pricing(parts_list)
        
        if not quotes:
            return jsonify({'success': False, 'error': 'No quotes available'}), 404
        
        # Process and enhance quotes
        enhanced_quotes = []
        total_estimated_cost = 0
        
        for quote in quotes:
            quote_data = {
                'id': quote.quote_id,
                'supplier_name': quote.supplier_name,
                'part_number': quote.part_number,
                'unit_price': quote.unit_price,
                'quantity_quoted': quote.quantity_quoted,
                'minimum_quantity': quote.minimum_quantity,
                'availability': quote.availability,
                'lead_time_days': quote.lead_time_days,
                'currency': quote.currency,
                'is_valid': quote.is_quote_valid(),
                'quote_age_days': quote.get_quote_age_days(),
                'total_cost': quote.get_total_cost(quote.quantity_quoted),
                'cost_breakdown': quote.get_total_cost(quote.quantity_quoted)
            }
            enhanced_quotes.append(quote_data)
            total_estimated_cost += quote.total_cost if hasattr(quote, 'total_cost') else quote.unit_price
        
        # Group by part number for comparison
        parts_quotes = {}
        for quote in enhanced_quotes:
            part_number = quote['part_number']
            if part_number not in parts_quotes:
                parts_quotes[part_number] = []
            parts_quotes[part_number].append(quote)
        
        # Find best prices for each part
        best_quotes = []
        for part_number, part_quotes in parts_quotes.items():
            best_quote = min(part_quotes, key=lambda x: x['unit_price'])
            best_quotes.append(best_quote)
        
        # Log the quoting activity
        integration_log = SupplierIntegrationLog(
            supplier_name='Multi-Source',
            integration_type='quotation',
            activity_type='bulk_quote',
            status='success',
            message=f'Generated {len(quotes)} quotes for {len(parts_list)} parts',
            records_processed=len(quotes),
            records_successful=len(quotes),
            project_id=project_id
        )
        db.session.add(integration_log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'quotes': enhanced_quotes,
            'parts_summary': {
                'total_parts': len(parts_list),
                'total_quotes': len(quotes),
                'total_suppliers': len(set(q['supplier_name'] for q in enhanced_quotes)),
                'estimated_total_cost': total_estimated_cost
            },
            'best_quotes': best_quotes,
            'parts_quotes': parts_quotes,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Supplier quote error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/components', methods=['GET'])
def api_components():
    """List components with filtering and search"""
    try:
        # Get query parameters
        search = request.args.get('search', '').strip()
        category = request.args.get('category', '').strip()
        manufacturer = request.args.get('manufacturer', '').strip()
        ul_certified = request.args.get('ul_certified', '').strip()
        nec_compliant = request.args.get('nec_compliant', '').strip()
        
        # Build query
        query = ElectricalComponent.query
        
        if search:
            query = query.filter(
                db.or_(
                    ElectricalComponent.description.ilike(f'%{search}%'),
                    ElectricalComponent.part_number.ilike(f'%{search}%'),
                    ElectricalComponent.manufacturer.ilike(f'%{search}%')
                )
            )
        
        if category:
            query = query.filter(ElectricalComponent.category == category)
        
        if manufacturer:
            query = query.filter(ElectricalComponent.manufacturer.ilike(f'%{manufacturer}%'))
        
        if ul_certified:
            query = query.filter(ElectricalComponent.ul_certified == (ul_certified.lower() == 'true'))
        
        if nec_compliant:
            query = query.filter(ElectricalComponent.nec_compliant == (nec_compliant.lower() == 'true'))
        
        components = query.limit(100).all()
        
        return jsonify({
            'success': True,
            'components': [component.to_dict() for component in components],
            'total_count': len(components),
            'filters_applied': {
                'search': search,
                'category': category,
                'manufacturer': manufacturer,
                'ul_certified': ul_certified,
                'nec_compliant': nec_compliant
            }
        })
        
    except Exception as e:
        logger.error(f"Components list error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/bom/create', methods=['POST'])
def api_bom_create():
    """Create Bill of Materials from supplier search results"""
    try:
        data = request.get_json()
        project_id = data.get('project_id')
        components = data.get('components', [])
        
        if not project_id or not components:
            return jsonify({'success': False, 'error': 'Project ID and components are required'}), 400
        
        project = Project.query.get_or_404(project_id)
        created_items = []
        
        for comp_data in components:
            part_number = comp_data.get('part_number')
            quantity = comp_data.get('quantity', 1)
            
            # Check if component exists
            component = ElectricalComponent.query.filter_by(part_number=part_number).first()
            
            if not component:
                # Create new component from supplier data
                component = ElectricalComponent(
                    manufacturer=comp_data.get('manufacturer', ''),
                    part_number=part_number,
                    description=comp_data.get('description', ''),
                    category=comp_data.get('category', ''),
                    voltage_rating=comp_data.get('voltage_rating', ''),
                    current_rating=comp_data.get('current_rating', ''),
                    current_price=comp_data.get('price', 0.0),
                    stock_quantity=comp_data.get('stock_quantity', 0),
                    ul_certified=comp_data.get('ul_certified', False),
                    nec_compliant=comp_data.get('nec_compliant', False),
                    supplier_name=comp_data.get('supplier_name', ''),
                    datasheet_url=comp_data.get('datasheet_url', ''),
                    data_source='supplier_integration',
                    data_quality_score=0.85
                )
                db.session.add(component)
                db.session.flush()  # Get the ID
            
            # Create BOM item
            bom_item = BOMItem(
                project_id=project.id,
                component_id=component.id,
                quantity_required=quantity,
                unit_cost=component.current_price,
                total_cost=component.current_price * quantity,
                status='planned',
                priority=Priority.MEDIUM
            )
            
            db.session.add(bom_item)
            created_items.append({
                'id': bom_item.id,
                'part_number': component.part_number,
                'description': component.description,
                'quantity': quantity,
                'unit_cost': bom_item.unit_cost,
                'total_cost': bom_item.total_cost
            })
        
        db.session.commit()
        
        # Update project BOM summary
        bom_summary = project.get_bom_summary()
        
        return jsonify({
            'success': True,
            'message': f'Created {len(created_items)} BOM items',
            'bom_items': created_items,
            'project_bom_summary': bom_summary
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"BOM creation error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/compliance/check', methods=['POST'])
def api_compliance_check():
    """Perform NEC compliance check on project BOM"""
    try:
        data = request.get_json()
        project_id = data.get('project_id')
        
        if not project_id:
            return jsonify({'success': False, 'error': 'Project ID is required'}), 400
        
        project = Project.query.get_or_404(project_id)
        
        # Check compliance for all BOM items
        compliance_results = []
        critical_issues = 0
        
        for bom_item in project.bom_items:
            if bom_item.component:
                # Perform compliance check
                compliance_data = components_db.verify_certifications(bom_item.component)
                
                compliance_record = NECComplianceRecord(
                    project_id=project.id,
                    component_id=bom_item.component.id,
                    bom_item_id=bom_item.id,
                    nec_section=', '.join(bom_item.component.nec_section_references or []),
                    requirement_description=f"Component selection and installation per NEC requirements",
                    compliance_status=ComplianceStatus.COMPLIANT if compliance_data['nec_compliant'] else ComplianceStatus.NON_COMPLIANT,
                    findings=compliance_data.get('nec_issues', []),
                    recommendations=compliance_data.get('nec_warnings', []),
                    risk_level='High' if not compliance_data['nec_compliant'] else 'Low',
                    reviewed_by='Automated System',
                    review_date=datetime.now()
                )
                
                if compliance_record.risk_level == 'Critical':
                    critical_issues += 1
                
                db.session.add(compliance_record)
                compliance_results.append({
                    'component': bom_item.component.part_number,
                    'compliance_status': compliance_record.compliance_status.value,
                    'risk_level': compliance_record.risk_level,
                    'issues': compliance_record.findings
                })
        
        # Update project compliance status
        if critical_issues > 0:
            project.nec_compliance_status = ComplianceStatus.NON_COMPLIANT
        elif len(compliance_results) == 0:
            project.nec_compliance_status = ComplianceStatus.PENDING_REVIEW
        else:
            project.nec_compliance_status = ComplianceStatus.COMPLIANT
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'compliance_results': compliance_results,
            'summary': {
                'total_components_checked': len(compliance_results),
                'compliant': len([r for r in compliance_results if r['compliance_status'] == 'compliant']),
                'non_compliant': len([r for r in compliance_results if r['compliance_status'] == 'non_compliant']),
                'critical_issues': critical_issues,
                'overall_status': project.nec_compliance_status.value
            }
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Compliance check error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/reports/bom/<int:project_id>', methods=['GET'])
def api_bom_report(project_id):
    """Generate comprehensive BOM report"""
    try:
        project = Project.query.get_or_404(project_id)
        
        # Generate BOM components list
        components = []
        for bom_item in project.bom_items:
            if bom_item.component:
                components.append(bom_item.component)
        
        # Generate comprehensive report
        if components:
            report = components_db.generate_bom_report(components)
        else:
            report = {
                'summary': {
                    'total_parts': 0,
                    'total_cost': 0.0,
                    'ul_certified_count': 0,
                    'nec_compliant_count': 0,
                    'unique_manufacturers': 0
                },
                'components': [],
                'certification_summary': {
                    'ul_certified': [],
                    'non_ul_certified': [],
                    'nec_issues': []
                },
                'cost_analysis': {
                    'by_manufacturer': {},
                    'by_supplier': {}
                }
            }
        
        # Add project-specific information
        report['project_info'] = {
            'name': project.name,
            'project_number': project.project_number,
            'client_name': project.client_name,
            'location': project.project_location,
            'nec_revision': project.nec_revision,
            'review_date': datetime.now().isoformat(),
            'reviewed_by': 'Automated System'
        }
        
        # Add project performance metrics
        report['performance_metrics'] = project.get_performance_metrics()
        
        return jsonify({
            'success': True,
            'report': report
        })
        
    except Exception as e:
        logger.error(f"BOM report error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/integration/status', methods=['GET'])
def api_integration_status():
    """Get supplier integration status and recent activity"""
    try:
        # Get recent integration logs
        recent_logs = SupplierIntegrationLog.query.filter(
            SupplierIntegrationLog.timestamp >= datetime.now() - timedelta(days=7)
        ).order_by(SupplierIntegrationLog.timestamp.desc()).limit(20).all()
        
        # Calculate integration statistics
        total_activities = len(recent_logs)
        successful_activities = len([log for log in recent_logs if log.status == 'success'])
        error_activities = len([log for log in recent_logs if log.status == 'error'])
        
        # Get supplier summary
        suppliers = db.session.query(SupplierQuotation.supplier_name).distinct().all()
        active_suppliers = [supplier[0] for supplier in suppliers]
        
        # Get active quotations
        active_quotes = SupplierQuotation.query.filter_by(is_active=True).all()
        valid_quotes = [quote for quote in active_quotes if quote.is_quote_valid()]
        
        return jsonify({
            'success': True,
            'integration_status': {
                'total_activities': total_activities,
                'successful_activities': successful_activities,
                'error_activities': error_activities,
                'success_rate': (successful_activities / total_activities * 100) if total_activities > 0 else 0,
                'active_suppliers': len(active_suppliers),
                'active_quotes': len(active_quotes),
                'valid_quotes': len(valid_quotes)
            },
            'suppliers': active_suppliers,
            'recent_activities': [{
                'supplier_name': log.supplier_name,
                'activity_type': log.activity_type,
                'status': log.status,
                'message': log.message,
                'timestamp': log.timestamp.isoformat(),
                'records_processed': log.records_processed,
                'response_time_ms': log.response_time_ms
            } for log in recent_logs]
        })
        
    except Exception as e:
        logger.error(f"Integration status error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/calculate/voltage-drop', methods=['POST'])
def api_calculate_voltage_drop():
    """Calculate voltage drop"""
    try:
        data = request.get_json()
        result = ElectricalCalculator.calculate_voltage_drop(
            voltage=float(data.get('voltage', 120)),
            current=float(data.get('current', 10)),
            distance_ft=float(data.get('distance_ft', 100)),
            conductor_size=str(data.get('conductor_size', '12')),
            conductor_material=data.get('conductor_material', 'copper')
        )
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/calculate/fault-current', methods=['POST'])
def api_calculate_fault_current():
    """Calculate fault current"""
    try:
        data = request.get_json()
        result = ElectricalCalculator.calculate_fault_current(
            source_voltage=float(data.get('source_voltage', 480)),
            source_mva=float(data.get('source_mva', 500)),
            transformer_kva=float(data.get('transformer_kva', 75)),
            transformer_impedance_percent=float(data.get('transformer_impedance', 2.5))
        )
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/calculate/cable-sizing', methods=['POST'])
def api_calculate_cable_sizing():
    """Calculate cable sizing"""
    try:
        data = request.get_json()
        result = ElectricalCalculator.calculate_cable_sizing(
            current_amps=float(data.get('current_amps', 20)),
            voltage=float(data.get('voltage', 120)),
            ambient_temp_c=float(data.get('ambient_temp', 30)),
            num_conductors=int(data.get('num_conductors', 3))
        )
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/calculate/breaker-sizing', methods=['POST'])
def api_calculate_breaker_sizing():
    """Calculate breaker sizing"""
    try:
        data = request.get_json()
        result = ElectricalCalculator.calculate_breaker_sizing(
            load_amps=float(data.get('load_amps', 20)),
            load_type=data.get('load_type', 'continuous')
        )
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/calculate/motor-startup', methods=['POST'])
def api_calculate_motor_startup():
    """Calculate motor startup characteristics"""
    try:
        data = request.get_json()
        result = ElectricalCalculator.calculate_motor_startup(
            motor_hp=float(data.get('motor_hp', 10)),
            voltage=float(data.get('voltage', 480)),
            method=data.get('method', 'dol')
        )
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ============================================================================
# INDUSTRY PAIN POINT SOLUTIONS - TEMPLATES AND UI
# ============================================================================

@app.route('/dashboard/enhanced')
def enhanced_dashboard():
    """Enhanced dashboard with real-time supplier integration"""
    return render_template('enhanced_dashboard.html')

@app.route('/projects/<int:project_id>/bom')
def project_bom(project_id):
    """Project BOM management with real supplier integration"""
    project = Project.query.get_or_404(project_id)
    return render_template('project_bom.html', project=project)

@app.route('/suppliers/search')
def supplier_search():
    """Real-time component search interface"""
    return render_template('supplier_search.html')

@app.route('/compliance/check')
def compliance_check():
    """NEC compliance checking interface"""
    projects = Project.query.all()
    return render_template('compliance_check.html', projects=projects)

@app.route('/reports')
def reports():
    """Comprehensive reporting interface"""
    return render_template('reports.html')

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error='Resource not found'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', error='Internal server error'), 500

# ============================================================================
# APPLICATION STARTUP
# ============================================================================

def init_database():
    """Initialize database with tables and sample data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if we need to seed data
        if Project.query.count() == 0:
            logger.info("Seeding database with sample data...")
            components_data, projects_data = seed_enhanced_sample_data()
            
            # Create components
            for comp_data in components_data:
                component = ElectricalComponent(**comp_data)
                db.session.add(component)
            
            # Create projects
            for proj_data in projects_data:
                project = Project(**proj_data)
                db.session.add(project)
            
            # Create sample BOM items
            components = ElectricalComponent.query.all()
            project = Project.query.first()
            
            if components and project:
                bom_items = [
                    BOMItem(project_id=project.id, component_id=components[0].id, quantity_required=12, unit_cost=components[0].current_price),
                    BOMItem(project_id=project.id, component_id=components[1].id, quantity_required=6, unit_cost=components[1].current_price)
                ]
                
                for item in bom_items:
                    item.total_cost = item.unit_cost * item.quantity_required
                    db.session.add(item)
            
            db.session.commit()
            logger.info("Database seeded successfully")
        
        logger.info("Database initialization complete")

if __name__ == '__main__':
    # Initialize database
    init_database()
    
    # Start the application
    app.run(
        host=app.config.get('HOST', '0.0.0.0'),
        port=app.config.get('PORT', 5000),
        debug=app.config.get('DEBUG', False)
    )