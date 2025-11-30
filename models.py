from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Project(db.Model):
    """Main project model"""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='planning')  # planning, in_progress, completed, on_hold
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    budget = db.Column(db.Float, default=0.0)
    actual_cost = db.Column(db.Float, default=0.0)
    progress = db.Column(db.Float, default=0.0)  # 0.0 to 100.0
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    calculations = db.relationship('ElectricalCalculation', backref='project', lazy=True, cascade='all, delete-orphan')
    materials = db.relationship('Material', backref='project', lazy=True, cascade='all, delete-orphan')
    risk_assessments = db.relationship('RiskAssessment', backref='project', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'budget': self.budget,
            'actual_cost': self.actual_cost,
            'progress': self.progress,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ElectricalCalculation(db.Model):
    """Electrical engineering calculations"""
    __tablename__ = 'electrical_calculations'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    calculation_type = db.Column(db.String(100), nullable=False)  # load_flow, voltage_drop, fault_current, cable_sizing
    input_parameters = db.Column(db.Text)  # JSON string
    results = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'calculation_type': self.calculation_type,
            'input_parameters': json.loads(self.input_parameters) if self.input_parameters else {},
            'results': json.loads(self.results) if self.results else {},
            'created_at': self.created_at.isoformat()
        }

class Material(db.Model):
    """Material specifications and pricing"""
    __tablename__ = 'materials'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))  # cables, breakers, transformers, conduit, etc.
    quantity = db.Column(db.Float, nullable=False)
    unit_cost = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    supplier = db.Column(db.String(255))
    specifications = db.Column(db.Text)  # JSON string
    status = db.Column(db.String(50), default='quoted')  # quoted, ordered, delivered, installed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'name': self.name,
            'category': self.category,
            'quantity': self.quantity,
            'unit_cost': self.unit_cost,
            'total_cost': self.total_cost,
            'supplier': self.supplier,
            'specifications': json.loads(self.specifications) if self.specifications else {},
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

class RiskAssessment(db.Model):
    """Project risk assessments and mitigation strategies"""
    __tablename__ = 'risk_assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    overall_risk_score = db.Column(db.Float, nullable=False)  # 0.0 to 1.0
    risk_factors = db.Column(db.Text)  # JSON string
    mitigation_strategies = db.Column(db.Text)  # JSON string
    assessment_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'overall_risk_score': self.overall_risk_score,
            'risk_factors': json.loads(self.risk_factors) if self.risk_factors else {},
            'mitigation_strategies': json.loads(self.mitigation_strategies) if self.mitigation_strategies else [],
            'assessment_date': self.assessment_date.isoformat()
        }

class HistoricalProject(db.Model):
    """Historical project data for AI training"""
    __tablename__ = 'historical_projects'
    
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(255), nullable=False)
    project_type = db.Column(db.String(100))  # commercial, industrial, residential
    electrical_scope = db.Column(db.Text)  # JSON string describing electrical scope
    actual_cost = db.Column(db.Float)
    final_duration = db.Column(db.Integer)  # days
    success_factors = db.Column(db.Text)  # JSON string
    challenges = db.Column(db.Text)  # JSON string
    completed_date = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_name': self.project_name,
            'project_type': self.project_type,
            'electrical_scope': json.loads(self.electrical_scope) if self.electrical_scope else {},
            'actual_cost': self.actual_cost,
            'final_duration': self.final_duration,
            'success_factors': json.loads(self.success_factors) if self.success_factors else [],
            'challenges': json.loads(self.challenges) if self.challenges else [],
            'completed_date': self.completed_date.isoformat() if self.completed_date else None
        }