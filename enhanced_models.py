"""
Enhanced Database Models for Real-World Electrical Construction Management
Addresses industry pain points with supplier integration, NEC compliance, and real-time data
"""

from datetime import datetime, timedelta
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import json

# Initialize Flask-SQLAlchemy
db = SQLAlchemy()

class ProjectStatus(Enum):
    """Project status enumeration"""
    PLANNING = "planning"
    DESIGN = "design"
    BIDDING = "bidding"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"

class Priority(Enum):
    """Project priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ComplianceStatus(Enum):
    """NEC compliance status"""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PENDING_REVIEW = "pending_review"
    REQUIRES_CORRECTION = "requires_correction"

class SupplierIntegrationStatus(Enum):
    """Supplier integration status"""
    INTEGRATED = "integrated"
    NOT_INTEGRATED = "not_integrated"
    PENDING_SETUP = "pending_setup"
    ERROR = "error"

class ElectricalComponent(db.Model):
    """Enhanced electrical component model with real supplier data"""
    __tablename__ = 'electrical_components'
    
    id = Column(Integer, primary_key=True)
    
    # Basic component information
    manufacturer = Column(String(100), nullable=False)
    part_number = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=False)
    category = Column(String(50))  # breaker, switch, wire, etc.
    
    # Electrical specifications
    voltage_rating = Column(String(50))  # e.g., "120V", "480V"
    current_rating = Column(String(50))  # e.g., "100A", "20A"
    power_rating = Column(String(50))    # e.g., "5kW"
    impedance = Column(String(50))       # for transformers, motors
    
    # Physical specifications
    dimensions = Column(String(100))     # e.g., "6\" x 4\" x 2\""
    weight_lbs = Column(Float)
    mounting_type = Column(String(50))   # surface, flush, din rail
    enclosure_rating = Column(String(20)) # NEMA ratings
    
    # Pricing and availability (real-time data)
    base_price = Column(Float, default=0.0)
    current_price = Column(Float, default=0.0)
    currency = Column(String(3), default='USD')
    stock_quantity = Column(Integer, default=0)
    minimum_order_quantity = Column(Integer, default=1)
    lead_time_days = Column(Integer, default=7)
    
    # Supplier information
    supplier_id = Column(String(50))
    supplier_name = Column(String(100))
    supplier_sku = Column(String(100))
    supplier_url = Column(String(500))
    
    # Certification and compliance
    ul_certified = Column(Boolean, default=False)
    csa_certified = Column(Boolean, default=False)
    ce_marked = Column(Boolean, default=False)
    nec_compliant = Column(Boolean, default=False)
    compliance_notes = Column(Text)
    certification_number = Column(String(100))
    certification_expiry = Column(DateTime)
    
    # Datasheet and documentation
    datasheet_url = Column(String(500))
    installation_guide_url = Column(String(500))
    manufacturer_url = Column(String(500))
    
    # Status and metadata
    active = Column(Boolean, default=True)
    last_updated = Column(DateTime, default=func.now(), onupdate=func.now())
    data_source = Column(String(50))  # digikey, mouser, manual, etc.
    data_quality_score = Column(Float, default=0.0)  # 0-1 confidence score
    
    # NEC-specific data
    nec_section_references = Column(JSON)  # List of applicable NEC sections
    ampacity_rating = Column(Float)
    temperature_rating = Column(String(20))  # 75C, 90C, etc.
    conductor_material = Column(String(20))  # copper, aluminum
    
    # Relationships
    bom_items = relationship("BOMItem", back_populates="component")
    quotations = relationship("SupplierQuotation", back_populates="component")
    
    def __repr__(self):
        return f"<ElectricalComponent {self.manufacturer} {self.part_number}>"
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'manufacturer': self.manufacturer,
            'part_number': self.part_number,
            'description': self.description,
            'category': self.category,
            'voltage_rating': self.voltage_rating,
            'current_rating': self.current_rating,
            'price': self.current_price,
            'currency': self.currency,
            'stock_quantity': self.stock_quantity,
            'supplier_name': self.supplier_name,
            'ul_certified': self.ul_certified,
            'nec_compliant': self.nec_compliant,
            'datasheet_url': self.datasheet_url,
            'compliance_status': self.get_compliance_status(),
            'availability_status': self.get_availability_status()
        }
    
    def get_compliance_status(self):
        """Determine overall compliance status"""
        if not self.ul_certified and not self.csa_certified:
            return "UNSAFE - Not certified"
        elif not self.nec_compliant:
            return "NON_COMPLIANT"
        else:
            return "COMPLIANT"
    
    def get_availability_status(self):
        """Determine availability status"""
        if self.stock_quantity > 10:
            return "In Stock"
        elif self.stock_quantity > 0:
            return "Limited Stock"
        elif self.lead_time_days <= 7:
            return "Available - 1 Week"
        else:
            return "Special Order - Extended Lead Time"
    
    def get_price_confidence(self):
        """Get confidence level for pricing data"""
        # Higher confidence if data is recent and from multiple sources
        days_old = (datetime.now() - self.last_updated).days
        if days_old <= 1:
            return 0.95
        elif days_old <= 7:
            return 0.85
        elif days_old <= 30:
            return 0.75
        else:
            return 0.50
    
    def calculate_total_cost(self, quantity: int = 1, include_shipping: bool = True):
        """Calculate total cost including shipping and taxes"""
        base_cost = self.current_price * max(quantity, self.minimum_order_quantity)
        
        if include_shipping:
            # Estimate shipping cost (this would be more sophisticated in reality)
            shipping_cost = min(base_cost * 0.05, 100.0)  # 5% or $100 max
        else:
            shipping_cost = 0
        
        tax_rate = 0.08875  # 8.875% typical sales tax
        tax_cost = (base_cost + shipping_cost) * tax_rate
        
        return {
            'base_cost': base_cost,
            'shipping_cost': shipping_cost,
            'tax_cost': tax_cost,
            'total_cost': base_cost + shipping_cost + tax_cost,
            'confidence': self.get_price_confidence()
        }

class BOMItem(db.Model):
    """Bill of Materials item with enhanced tracking"""
    __tablename__ = 'bom_items'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    component_id = Column(Integer, ForeignKey('electrical_components.id'), nullable=False)
    
    # BOM specific information
    quantity_required = Column(Integer, nullable=False, default=1)
    quantity_allocated = Column(Integer, default=0)
    unit_cost = Column(Float, default=0.0)
    total_cost = Column(Float, default=0.0)
    
    # Status tracking
    status = Column(String(20), default='planned')  # planned, ordered, delivered, installed
    priority = Column(SQLEnum(Priority), default=Priority.MEDIUM)
    
    # Scheduling information
    required_date = Column(DateTime)
    order_date = Column(DateTime)
    delivery_date = Column(DateTime)
    installation_date = Column(DateTime)
    
    # Change tracking
    original_quantity = Column(Integer)
    change_reason = Column(Text)
    last_modified = Column(DateTime, default=func.now(), onupdate=func.now())
    modified_by = Column(String(100))
    
    # Relationships
    project = relationship("Project", back_populates="bom_items")
    component = relationship("ElectricalComponent", back_populates="bom_items")
    change_requests = relationship("ChangeRequest", back_populates="bom_item")
    
    def __repr__(self):
        return f"<BOMItem {self.component.part_number} x{self.quantity_required}>"
    
    def get_status_info(self):
        """Get detailed status information"""
        status_info = {
            'status': self.status,
            'quantity_required': self.quantity_required,
            'quantity_allocated': self.quantity_allocated,
            'allocation_percentage': (self.quantity_allocated / self.quantity_required * 100) if self.quantity_required > 0 else 0
        }
        
        # Add timeline information
        if self.required_date:
            days_until_required = (self.required_date - datetime.now()).days
            status_info['days_until_required'] = days_until_required
            status_info['is_overdue'] = days_until_required < 0
        
        return status_info
    
    def calculate_total_cost(self):
        """Calculate total cost for this BOM item"""
        if self.component:
            self.unit_cost = self.component.current_price
            self.total_cost = self.unit_cost * self.quantity_required
        return self.total_cost

class SupplierQuotation(db.Model):
    """Real-time supplier quotations"""
    __tablename__ = 'supplier_quotations'
    
    id = Column(Integer, primary_key=True)
    component_id = Column(Integer, ForeignKey('electrical_components.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    
    # Supplier information
    supplier_name = Column(String(100), nullable=False)
    supplier_code = Column(String(20))  # DK, MO, MS, etc.
    
    # Quotation details
    quote_id = Column(String(50), nullable=False)
    part_number = Column(String(100), nullable=False)
    unit_price = Column(Float, nullable=False)
    currency = Column(String(3), default='USD')
    quantity_quoted = Column(Integer, default=1)
    
    # Terms and availability
    minimum_quantity = Column(Integer, default=1)
    lead_time_days = Column(Integer, default=7)
    availability = Column(String(50))  # In Stock, Back Order, Discontinued
    valid_until = Column(DateTime)
    
    # Contact information
    contact_person = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100))
    website = Column(String(200))
    
    # Additional information
    shipping_cost = Column(Float, default=0.0)
    notes = Column(Text)
    quote_conditions = Column(JSON)  # Special terms, bulk discounts, etc.
    
    # Metadata
    created_date = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    data_source = Column(String(50))  # API, manual, email
    
    # Relationships
    component = relationship("ElectricalComponent", back_populates="quotations")
    project = relationship("Project", back_populates="supplier_quotations")
    
    def __repr__(self):
        return f"<SupplierQuotation {self.supplier_name} {self.part_number}>"
    
    def get_quote_age_days(self):
        """Get age of quotation in days"""
        return (datetime.now() - self.created_date).days
    
    def is_quote_valid(self):
        """Check if quote is still valid"""
        if self.valid_until:
            return datetime.now() < self.valid_until
        # Default to 30 days if no expiration specified
        return self.get_quote_age_days() <= 30
    
    def get_total_cost(self, quantity: int = 1):
        """Calculate total cost for specified quantity"""
        effective_quantity = max(quantity, self.minimum_quantity)
        subtotal = self.unit_price * effective_quantity
        
        return {
            'unit_price': self.unit_price,
            'quantity': effective_quantity,
            'subtotal': subtotal,
            'shipping': self.shipping_cost,
            'total': subtotal + self.shipping_cost,
            'currency': self.currency,
            'is_valid': self.is_quote_valid()
        }

class NECComplianceRecord(db.Model):
    """NEC compliance tracking for projects and components"""
    __tablename__ = 'nec_compliance_records'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    component_id = Column(Integer, ForeignKey('electrical_components.id'))
    bom_item_id = Column(Integer, ForeignKey('bom_items.id'))
    
    # Compliance information
    nec_section = Column(String(50), nullable=False)  # e.g., "310.60", "430.52"
    requirement_description = Column(Text, nullable=False)
    compliance_status = Column(SQLEnum(ComplianceStatus), nullable=False)
    
    # Detailed assessment
    findings = Column(Text)
    recommendations = Column(Text)
    corrective_actions = Column(Text)
    risk_level = Column(String(20))  # Low, Medium, High, Critical
    
    # Review information
    reviewed_by = Column(String(100))
    review_date = Column(DateTime, default=func.now())
    next_review_date = Column(DateTime)
    
    # Approval workflow
    approved_by = Column(String(100))
    approval_date = Column(DateTime)
    approval_conditions = Column(Text)
    
    # Relationships
    project = relationship("Project", back_populates="compliance_records")
    component = relationship("ElectricalComponent")
    bom_item = relationship("BOMItem")
    
    def __repr__(self):
        return f"<NECComplianceRecord {self.nec_section} - {self.compliance_status}>"
    
    def get_risk_priority(self):
        """Get priority based on risk level and status"""
        if self.compliance_status == ComplianceStatus.NON_COMPLIANT:
            if self.risk_level == 'Critical':
                return 1
            elif self.risk_level == 'High':
                return 2
            else:
                return 3
        elif self.compliance_status == ComplianceStatus.REQUIRES_CORRECTION:
            return 4
        elif self.compliance_status == ComplianceStatus.PENDING_REVIEW:
            return 5
        else:
            return 6

class ChangeRequest(db.Model):
    """Change request tracking for BOM items"""
    __tablename__ = 'change_requests'
    
    id = Column(Integer, primary_key=True)
    bom_item_id = Column(Integer, ForeignKey('bom_items.id'), nullable=False)
    
    # Change details
    change_type = Column(String(50))  # quantity, component, schedule, specification
    requested_by = Column(String(100), nullable=False)
    requested_date = Column(DateTime, default=func.now())
    
    # Change description
    description = Column(Text, nullable=False)
    reason = Column(Text)
    justification = Column(Text)
    
    # Impact assessment
    cost_impact = Column(Float, default=0.0)
    schedule_impact_days = Column(Integer, default=0)
    risk_assessment = Column(Text)
    
    # Approval workflow
    status = Column(String(20), default='pending')  # pending, approved, rejected, implemented
    requested_by_role = Column(String(50))  # engineer, contractor, client, etc.
    
    # Approval information
    reviewed_by = Column(String(100))
    review_date = Column(DateTime)
    review_comments = Column(Text)
    
    # Implementation tracking
    implemented_date = Column(DateTime)
    implemented_by = Column(String(100))
    actual_cost_impact = Column(Float, default=0.0)
    actual_schedule_impact = Column(Integer, default=0)
    
    # Relationships
    bom_item = relationship("BOMItem", back_populates="change_requests")
    
    def __repr__(self):
        return f"<ChangeRequest {self.change_type} for BOM Item {self.bom_item_id}>"
    
    def get_approval_priority(self):
        """Get approval priority based on impact and urgency"""
        if abs(self.cost_impact) > 10000 or abs(self.schedule_impact_days) > 14:
            return "High"
        elif abs(self.cost_impact) > 1000 or abs(self.schedule_impact_days) > 7:
            return "Medium"
        else:
            return "Low"

class SupplierIntegrationLog(db.Model):
    """Log of supplier integration activities"""
    __tablename__ = 'supplier_integration_logs'
    
    id = Column(Integer, primary_key=True)
    supplier_name = Column(String(100), nullable=False)
    integration_type = Column(String(50))  # API, manual, file upload
    
    # Activity details
    activity_type = Column(String(50))  # search, quote, order, sync
    status = Column(String(20))  # success, error, warning
    message = Column(Text)
    
    # Request/response data
    request_data = Column(JSON)
    response_data = Column(JSON)
    error_details = Column(Text)
    
    # Performance metrics
    response_time_ms = Column(Integer)
    records_processed = Column(Integer, default=0)
    records_successful = Column(Integer, default=0)
    records_failed = Column(Integer, default=0)
    
    # Metadata
    timestamp = Column(DateTime, default=func.now())
    user_id = Column(String(100))
    session_id = Column(String(100))
    
    def __repr__(self):
        return f"<SupplierIntegrationLog {self.supplier_name} {self.activity_type} - {self.status}>"

# Enhanced Project model with real-world fields
class Project(db.Model):
    """Enhanced project model with industry pain point solutions"""
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    
    # Basic project information
    name = Column(String(200), nullable=False)
    description = Column(Text)
    project_number = Column(String(50), unique=True, index=True)
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.PLANNING)
    priority = Column(SQLEnum(Priority), default=Priority.MEDIUM)
    
    # Location and client information
    client_name = Column(String(100))
    client_contact = Column(String(100))
    project_location = Column(String(200))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(50))
    zip_code = Column(String(20))
    
    # Project timeline
    start_date = Column(DateTime)
    estimated_completion = Column(DateTime)
    actual_completion = Column(DateTime)
    last_update = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Financial information
    estimated_cost = Column(Float, default=0.0)
    actual_cost = Column(Float, default=0.0)
    budget_variance = Column(Float, default=0.0)
    contingency_percentage = Column(Float, default=10.0)
    
    # Team information
    project_manager = Column(String(100))
    lead_engineer = Column(String(100))
    electrical_engineer = Column(String(100))
    foreman = Column(String(100))
    
    # Risk and compliance
    risk_level = Column(String(20))  # Low, Medium, High
    nec_revision = Column(String(10))  # e.g., "2020", "2023"
    permit_status = Column(String(50))
    inspection_status = Column(String(50))
    
    # BIM and CAD integration
    bim_model_url = Column(String(500))
    cad_drawing_url = Column(String(500))
    revision_number = Column(String(20), default="R0")
    
    # Progress tracking
    progress_percentage = Column(Float, default=0.0)
    milestone_completion = Column(JSON)  # Dict of milestones
    issues_logged = Column(Integer, default=0)
    
    # Integration status
    supplier_integration_status = Column(SQLEnum(SupplierIntegrationStatus), default=SupplierIntegrationStatus.NOT_INTEGRATED)
    nec_compliance_status = Column(SQLEnum(ComplianceStatus), default=ComplianceStatus.PENDING_REVIEW)
    
    # Relationships
    bom_items = relationship("BOMItem", back_populates="project", cascade="all, delete-orphan")
    supplier_quotations = relationship("SupplierQuotation", back_populates="project")
    compliance_records = relationship("NECComplianceRecord", back_populates="project")
    
    def __repr__(self):
        return f"<Project {self.name} ({self.status})>"
    
    def get_bom_summary(self):
        """Get BOM summary statistics"""
        if not self.bom_items:
            return {
                'total_items': 0,
                'total_cost': 0.0,
                'approved_items': 0,
                'pending_items': 0,
                'overdue_items': 0
            }
        
        total_items = len(self.bom_items)
        total_cost = sum(item.total_cost for item in self.bom_items)
        approved_items = sum(1 for item in self.bom_items if item.status == 'installed')
        pending_items = sum(1 for item in self.bom_items if item.status in ['planned', 'ordered'])
        
        overdue_items = 0
        if any(item.required_date for item in self.bom_items):
            overdue_items = sum(1 for item in self.bom_items 
                              if item.required_date and 
                              item.required_date < datetime.now() and 
                              item.status != 'installed')
        
        return {
            'total_items': total_items,
            'total_cost': total_cost,
            'approved_items': approved_items,
            'pending_items': pending_items,
            'overdue_items': overdue_items,
            'completion_percentage': (approved_items / total_items * 100) if total_items > 0 else 0
        }
    
    def get_supplier_summary(self):
        """Get supplier summary from quotations"""
        if not self.supplier_quotations:
            return {
                'total_quotes': 0,
                'active_suppliers': 0,
                'best_price_total': 0.0,
                'average_lead_time': 0
            }
        
        active_quotes = [q for q in self.supplier_quotations if q.is_active and q.is_quote_valid()]
        total_quotes = len(active_quotes)
        
        if total_quotes == 0:
            return {
                'total_quotes': 0,
                'active_suppliers': 0,
                'best_price_total': 0.0,
                'average_lead_time': 0
            }
        
        suppliers = set(q.supplier_name for q in active_quotes)
        best_price_total = sum(min(q.unit_price for q in active_quotes 
                                 if q.part_number == item.component.part_number) 
                             for item in self.bom_items if item.component)
        
        avg_lead_time = sum(q.lead_time_days for q in active_quotes) / total_quotes
        
        return {
            'total_quotes': total_quotes,
            'active_suppliers': len(suppliers),
            'best_price_total': best_price_total,
            'average_lead_time': round(avg_lead_time, 1)
        }
    
    def get_compliance_summary(self):
        """Get NEC compliance summary"""
        if not self.compliance_records:
            return {
                'total_checks': 0,
                'compliant_count': 0,
                'non_compliant_count': 0,
                'pending_count': 0,
                'critical_issues': 0
            }
        
        total_checks = len(self.compliance_records)
        compliant_count = sum(1 for rec in self.compliance_records 
                            if rec.compliance_status == ComplianceStatus.COMPLIANT)
        non_compliant_count = sum(1 for rec in self.compliance_records 
                                if rec.compliance_status == ComplianceStatus.NON_COMPLIANT)
        pending_count = sum(1 for rec in self.compliance_records 
                          if rec.compliance_status == ComplianceStatus.PENDING_REVIEW)
        critical_issues = sum(1 for rec in self.compliance_records 
                            if rec.risk_level == 'Critical' and 
                            rec.compliance_status == ComplianceStatus.NON_COMPLIANT)
        
        return {
            'total_checks': total_checks,
            'compliant_count': compliant_count,
            'non_compliant_count': non_compliant_count,
            'pending_count': pending_count,
            'critical_issues': critical_issues,
            'compliance_percentage': (compliant_count / total_checks * 100) if total_checks > 0 else 0
        }
    
    def get_performance_metrics(self):
        """Get project performance metrics"""
        bom_summary = self.get_bom_summary()
        supplier_summary = self.get_supplier_summary()
        compliance_summary = self.get_compliance_summary()
        
        # Calculate overall health score (0-100)
        bom_score = bom_summary['completion_percentage']
        supplier_score = min(100, (supplier_summary['total_quotes'] / max(1, len(self.bom_items))) * 100)
        compliance_score = compliance_summary['compliance_percentage']
        
        overall_score = (bom_score * 0.4 + supplier_score * 0.3 + compliance_score * 0.3)
        
        return {
            'overall_health_score': round(overall_score, 1),
            'bom_completion': bom_summary['completion_percentage'],
            'supplier_coverage': supplier_score,
            'compliance_score': compliance_score,
            'estimated_vs_actual_variance': self.budget_variance,
            'timeline_status': self.get_timeline_status()
        }
    
    def get_timeline_status(self):
        """Get project timeline status"""
        if not self.start_date or not self.estimated_completion:
            return "Not Scheduled"
        
        now = datetime.now()
        
        if self.actual_completion:
            return "Completed"
        
        if now > self.estimated_completion:
            return "Behind Schedule"
        
        # Calculate progress based on time elapsed vs total time
        total_duration = (self.estimated_completion - self.start_date).days
        elapsed_duration = (now - self.start_date).days
        
        if total_duration <= 0:
            return "Invalid Schedule"
        
        expected_progress = min(100, (elapsed_duration / total_duration) * 100)
        
        if self.progress_percentage < expected_progress - 10:
            return "Behind Schedule"
        elif self.progress_percentage < expected_progress - 5:
            return "At Risk"
        elif abs(self.progress_percentage - expected_progress) <= 5:
            return "On Schedule"
        else:
            return "Ahead of Schedule"
    
    def to_dict(self):
        """Convert project to dictionary with all summary data"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'project_number': self.project_number,
            'status': self.status.value,
            'priority': self.priority.value,
            'client_name': self.client_name,
            'location': self.project_location,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'estimated_completion': self.estimated_completion.isoformat() if self.estimated_completion else None,
            'actual_completion': self.actual_completion.isoformat() if self.actual_completion else None,
            'estimated_cost': self.estimated_cost,
            'actual_cost': self.actual_cost,
            'progress_percentage': self.progress_percentage,
            'project_manager': self.project_manager,
            'lead_engineer': self.lead_engineer,
            'nec_revision': self.nec_revision,
            'risk_level': self.risk_level,
            'permit_status': self.permit_status,
            'inspection_status': self.inspection_status,
            'bom_summary': self.get_bom_summary(),
            'supplier_summary': self.get_supplier_summary(),
            'compliance_summary': self.get_compliance_summary(),
            'performance_metrics': self.get_performance_metrics(),
            'timeline_status': self.get_timeline_status(),
            'last_update': self.last_update.isoformat() if self.last_update else None
        }

# Example of how to use these models with real data
def seed_enhanced_sample_data():
    """Create sample data for demonstration"""
    from app import db
    
    # Sample components with real-world characteristics
    components = [
        {
            'manufacturer': 'Schneider Electric',
            'part_number': 'QO-1100',
            'description': 'QO Circuit Breaker 100A 120/240V',
            'category': 'circuit_breaker',
            'voltage_rating': '240V',
            'current_rating': '100A',
            'base_price': 145.50,
            'current_price': 147.25,
            'stock_quantity': 25,
            'ul_certified': True,
            'nec_compliant': True,
            'supplier_name': 'Digi-Key',
            'nec_section_references': ['310.60', '430.52'],
            'ampacity_rating': 100.0,
            'temperature_rating': '75C',
            'conductor_material': 'Copper',
            'data_source': 'api',
            'data_quality_score': 0.95
        },
        {
            'manufacturer': 'Siemens',
            'part_number': 'EDD-53',
            'description': '3-Pole Switch 50A 480V',
            'category': 'disconnect_switch',
            'voltage_rating': '480V',
            'current_rating': '50A',
            'base_price': 89.25,
            'current_price': 91.75,
            'stock_quantity': 15,
            'ul_certified': True,
            'nec_compliant': True,
            'supplier_name': 'Mouser',
            'nec_section_references': ['430.107', '440.14'],
            'ampacity_rating': 50.0,
            'temperature_rating': '75C',
            'conductor_material': 'Copper',
            'data_source': 'api',
            'data_quality_score': 0.92
        }
    ]
    
    # Create sample projects
    projects = [
        {
            'name': 'Downtown Office Complex - Phase 1',
            'description': 'Electrical installation for 12-story office building',
            'project_number': 'DOC-2024-001',
            'client_name': 'Metro Development Corp',
            'project_location': 'Downtown Financial District',
            'status': ProjectStatus.IN_PROGRESS,
            'priority': Priority.HIGH,
            'estimated_cost': 850000.0,
            'actual_cost': 125000.0,
            'progress_percentage': 35.0,
            'project_manager': 'John Smith, PE',
            'lead_engineer': 'Sarah Johnson, PE',
            'nec_revision': '2023',
            'risk_level': 'Medium',
            'permit_status': 'Approved',
            'inspection_status': 'Scheduled',
            'start_date': datetime.now() - timedelta(days=45),
            'estimated_completion': datetime.now() + timedelta(days=120)
        },
        {
            'name': 'Industrial Manufacturing Facility',
            'description': 'Heavy industrial electrical installation with 480V service',
            'project_number': 'IMF-2024-002',
            'client_name': 'Advanced Manufacturing Inc',
            'project_location': 'Industrial Park West',
            'status': ProjectStatus.PLANNING,
            'priority': Priority.CRITICAL,
            'estimated_cost': 1250000.0,
            'actual_cost': 0.0,
            'progress_percentage': 5.0,
            'project_manager': 'Mike Wilson, PE',
            'lead_engineer': 'Lisa Chen, PE',
            'nec_revision': '2023',
            'risk_level': 'High',
            'permit_status': 'Under Review',
            'inspection_status': 'Not Scheduled',
            'start_date': datetime.now() + timedelta(days=30),
            'estimated_completion': datetime.now() + timedelta(days=240)
        }
    ]
    
    return components, projects

if __name__ == "__main__":
    # Example usage
    from app import app, db
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Seed sample data
        components_data, projects_data = seed_enhanced_sample_data()
        
        # Create components
        for comp_data in components_data:
            component = ElectricalComponent(**comp_data)
            db.session.add(component)
        
        # Create projects
        for proj_data in projects_data:
            project = Project(**proj_data)
            db.session.add(project)
        
        db.session.commit()
        print("Enhanced database with real-world data created successfully!")