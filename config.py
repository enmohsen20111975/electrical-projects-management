"""
Configuration settings for Electrical PM Application
"""

import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///electrical_pm.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Application Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # File Upload Configuration
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'dwg', 'dxf', 'png', 'jpg', 'jpeg'}
    
    # Cache Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Material Pricing Configuration
    MATERIAL_PRICE_CACHE_TIMEOUT = 3600  # 1 hour
    SUPPLIER_API_TIMEOUT = 30  # seconds
    
    # Calculation Engine Configuration
    MAX_CALCULATION_DISTANCE = 10000  # feet
    VOLTAGE_LEVELS = {
        '120V': 120,
        '208V': 208,
        '240V': 240,
        '480V': 480,
        '600V': 600,
        '2400V': 2400,
        '4160V': 4160,
        '13800V': 13800,
        '23000V': 23000
    }
    
    # AI Engine Configuration
    AI_CONFIDENCE_THRESHOLD = 0.7
    HISTORICAL_DATA_RETENTION_DAYS = 365
    RISK_ASSESSMENT_UPDATE_INTERVAL = 24  # hours
    
    # Business Logic Configuration
    NEC_VOLTAGE_DROP_LIMIT = 3.0  # percent for branch circuits
    CONTINUOUS_LOAD_FACTOR = 1.25  # 125%
    COPPER_RESISTANCE_BASE = 0.19  # ohms per 1000 ft for #2 AWG
    
    # Standard transformer sizes (kVA)
    STANDARD_TRANSFORMER_SIZES = [15, 25, 37.5, 50, 75, 100, 150, 200, 250, 300, 500, 750, 1000]
    
    # Wire ampacity tables (simplified)
    AMPACITY_COPPER_THHN = {
        '12': 30, '10': 40, '8': 55, '6': 80, '4': 105,
        '2': 140, '1/0': 170, '2/0': 195, '3/0': 225, '4/0': 260
    }
    
    AMPACITY_ALUMINUM_THHN = {
        '12': 25, '10': 35, '8': 50, '6': 65, '4': 85,
        '2': 115, '1/0': 135, '2/0': 155, '3/0': 180, '4/0': 205
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///electrical_pm_dev.db'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///electrical_pm_prod.db'
    
    # Security settings for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # File upload security
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8MB for production
    
    # AI configuration for production
    AI_CONFIDENCE_THRESHOLD = 0.8
    MATERIAL_PRICE_CACHE_TIMEOUT = 1800  # 30 minutes for faster updates

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Business Rules Configuration
BUSINESS_RULES = {
    'project_types': ['commercial', 'industrial', 'residential', 'utility_scale'],
    'project_statuses': ['planning', 'in_progress', 'completed', 'on_hold'],
    'calculation_types': ['load_flow', 'voltage_drop', 'fault_current', 'cable_sizing', 'transformer_sizing'],
    'material_categories': ['cables', 'breakers', 'transformers', 'conduit', 'panels'],
    'suppliers': ['graybar', 'wesco', 'schneider', 'siemens', 'eaton'],
    'risk_levels': ['low', 'medium', 'high'],
    'priority_levels': ['low', 'medium', 'high', 'critical']
}

# Material Catalog Configuration
MATERIAL_CATALOG = {
    'cables': {
        'copper_thhn_12awg': {
            'description': '12 AWG Copper THHN Building Wire',
            'unit': 'ft',
            'weight_per_unit': 0.089,
            'nec_ampacity': 30,
            'applications': ['General purpose branch circuits', '15-20A circuits']
        },
        'copper_thhn_10awg': {
            'description': '10 AWG Copper THHN Building Wire',
            'unit': 'ft',
            'weight_per_unit': 0.131,
            'nec_ampacity': 40,
            'applications': ['30A branch circuits', 'Heavy loads']
        }
    },
    'breakers': {
        'breaker_20a_1p': {
            'description': '20A Single Pole Circuit Breaker',
            'unit': 'each',
            'manufacturer': 'Square D',
            'voltage_rating': '120/240V',
            'interrupt_capacity': '10kA'
        }
    }
}

# Labor Rate Configuration by Region
LABOR_RATES = {
    'national_average': {
        'electrical_supervision': 95.00,
        'master_electrician': 85.00,
        'journeyman_electrician': 65.00,
        'apprentice': 35.00,
        'helper': 25.00
    },
    'high_cost_regions': {
        'electrical_supervision': 110.00,
        'master_electrician': 95.00,
        'journeyman_electrician': 75.00,
        'apprentice': 42.00,
        'helper': 30.00
    },
    'low_cost_regions': {
        'electrical_supervision': 80.00,
        'master_electrician': 70.00,
        'journeyman_electrician': 55.00,
        'apprentice': 28.00,
        'helper': 22.00
    }
}

# Risk Assessment Weights
RISK_WEIGHTS = {
    'material_cost_volatility': 0.25,
    'schedule_compression': 0.20,
    'technical_complexity': 0.25,
    'weather_impact': 0.15,
    'permit_delays': 0.15
}

# AI Model Configuration
AI_CONFIG = {
    'confidence_threshold': 0.7,
    'learning_rate': 0.001,
    'batch_size': 32,
    'epochs': 100,
    'validation_split': 0.2,
    'early_stopping_patience': 10,
    'model_save_path': 'models/',
    'historical_data_minimum': 50  # Minimum projects for reliable predictions
}

# API Rate Limits
API_LIMITS = {
    'material_pricing': 100,  # requests per hour
    'calculations': 1000,     # requests per hour
    'file_uploads': 50        # requests per hour
}