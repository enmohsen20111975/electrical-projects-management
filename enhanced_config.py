"""
Enhanced Configuration with Real Supplier API Integration
"""

import os
from datetime import timedelta

class BaseConfig:
    """Base configuration class"""
    
    # Basic Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Real Supplier API Configuration
    # Digi-Key API (https://developer.digikey.com/)
    DIGIKEY_CLIENT_ID = os.environ.get('DIGIKEY_CLIENT_ID', '')
    DIGIKEY_CLIENT_SECRET = os.environ.get('DIGIKEY_CLIENT_SECRET', '')
    DIGIKEY_BASE_URL = 'https://api.digikey.com/v1'
    
    # Mouser Electronics API (https://www.mouser.com/api-solutions/)
    MOUSER_API_KEY = os.environ.get('MOUSER_API_KEY', '')
    MOUSER_BASE_URL = 'https://api.mouser.com/api/v1'
    
    # UL Solutions Product iQ Database (https://productiq.ulprospector.com/)
    UL_API_KEY = os.environ.get('UL_API_KEY', '')
    UL_BASE_URL = 'https://productiq.ulprospector.com/api'
    
    # TrustedParts.com API (https://www.trustedparts.com/docs/trustedparts-api/)
    TRUSTEDPARTS_API_KEY = os.environ.get('TRUSTEDPARTS_API_KEY', '')
    TRUSTEDPARTS_BASE_URL = 'https://api.trustedparts.com/v1'
    
    # Win Source API (https://www.win-source.net/api-solution)
    WINSOURCE_API_KEY = os.environ.get('WINSOURCE_API_KEY', '')
    WINSOURCE_BASE_URL = 'https://api.win-source.net'
    
    # Sourcengine API (https://dev.sourcengine.com/)
    SOURCENGINE_API_KEY = os.environ.get('SOURCENGINE_API_KEY', '')
    SOURCENGINE_BASE_URL = 'https://api.sourcengine.com'
    
    # Luminovo API (https://luminovo.com/solutions/procurement)
    LUMINOVO_API_KEY = os.environ.get('LUMINOVO_API_KEY', '')
    LUMINOVO_BASE_URL = 'https://api.luminovo.com'
    
    # Real-time pricing update configuration
    PRICING_UPDATE_INTERVAL = 900  # 15 minutes
    CACHE_TIMEOUT = 300  # 5 minutes
    
    # NEC Standards Database Configuration
    NEC_BASE_URL = 'https://www.nfpa.org/codes-and-standards/all-codes-and-standards'
    NEC_VERSION = '2023'  # Current NEC version
    
    # Material compliance and certification
    UL_CERTIFICATION_CHECK = True
    CSA_CERTIFICATION_CHECK = True
    NEC_COMPLIANCE_VALIDATION = True
    
    # Electrical Standards Compliance
    ELECTRICAL_STANDARDS = {
        'NEC': {
            'version': '2023',
            'sections': {
                '310.60': 'Ampacities for Conductors Rated 0–2000 V',
                '430.52': 'Circuit Breaker Rating and Adjustment',
                '250.4': 'Grounding System Requirements',
                '440.14': 'Disconnecting Means',
                '310.16': 'Allowable Ampacities for Insulated Conductors'
            }
        },
        'UL': {
            'certification_required': True,
            'categories': ['UL 508A', 'UL 891', 'UL 1558']
        },
        'IEEE': {
            'standards': ['IEEE 141', 'IEEE 242', 'IEEE 1584']
        }
    }

class DevelopmentConfig(BaseConfig):
    """Development configuration with mock data for testing"""
    
    # Flask development settings
    DEBUG = True
    TESTING = False
    
    # Database - Using SQLite for development
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///electrical_construction_dev.db'
    
    # Use mock supplier data in development
    USE_MOCK_SUPPLIER_DATA = True
    MOCK_SUPPLIER_DELAY = 2  # seconds to simulate API calls
    
    # Logging
    LOG_LEVEL = 'DEBUG'
    
    # API rate limiting (disabled in development)
    API_RATE_LIMIT = False

class TestingConfig(BaseConfig):
    """Testing configuration"""
    
    # Flask testing settings
    DEBUG = False
    TESTING = True
    
    # In-memory database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Disable all external APIs in testing
    USE_MOCK_SUPPLIER_DATA = True
    
    # Fast testing
    PRICING_UPDATE_INTERVAL = 60  # 1 minute for testing
    CACHE_TIMEOUT = 30  # 30 seconds for testing

class ProductionConfig(BaseConfig):
    """Production configuration with real supplier integrations"""
    
    # Flask production settings
    DEBUG = False
    TESTING = False
    
    # Production database (PostgreSQL recommended)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://username:password@localhost/electrical_construction'
    
    # Use real supplier APIs in production
    USE_MOCK_SUPPLIER_DATA = False
    
    # Real API rate limiting
    API_RATE_LIMIT = True
    RATE_LIMIT_PER_MINUTE = 100
    
    # Enhanced security
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', 'change-this-salt')
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Production logging
    LOG_LEVEL = 'INFO'
    
    # Real-time data
    PRICING_UPDATE_INTERVAL = 900  # 15 minutes
    CACHE_TIMEOUT = 300  # 5 minutes
    
    # SSL and security headers
    SSL_REDIRECT = True

class StagingConfig(ProductionConfig):
    """Staging configuration (similar to production but with more logging)"""
    
    # More detailed logging for staging
    LOG_LEVEL = 'DEBUG'
    SQLALCHEMY_ECHO = True
    
    # Allow some mock data for testing
    USE_MOCK_SUPPLIER_DATA = False  # Use real APIs
    ALLOW_MOCK_FALLBACK = True  # Fallback to mock if API fails
    
    # Staging-specific settings
    MAIL_DEBUG = True
    CACHE_TIMEOUT = 180  # 3 minutes

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    
    'default': DevelopmentConfig
}

# API Configuration Helper
def get_supplier_config():
    """Get supplier configuration for external integrations"""
    return {
        'digikey': {
            'enabled': bool(BaseConfig.DIGIKEY_CLIENT_ID and BaseConfig.DIGIKEY_CLIENT_SECRET),
            'client_id': BaseConfig.DIGIKEY_CLIENT_ID,
            'client_secret': BaseConfig.DIGIKEY_CLIENT_SECRET,
            'base_url': BaseConfig.DIGIKEY_BASE_URL,
            'rate_limit': 1000,  # requests per hour
            'features': ['pricing', 'availability', 'ordering', 'product_data']
        },
        'mouser': {
            'enabled': bool(BaseConfig.MOUSER_API_KEY),
            'api_key': BaseConfig.MOUSER_API_KEY,
            'base_url': BaseConfig.MOUSER_BASE_URL,
            'rate_limit': 500,  # requests per hour
            'features': ['pricing', 'availability', 'product_data']
        },
        'ul_certifications': {
            'enabled': bool(BaseConfig.UL_API_KEY),
            'api_key': BaseConfig.UL_API_KEY,
            'base_url': BaseConfig.UL_BASE_URL,
            'rate_limit': 200,  # requests per hour
            'features': ['certification_verification', 'compliance_data']
        },
        'trustedparts': {
            'enabled': bool(BaseConfig.TRUSTEDPARTS_API_KEY),
            'api_key': BaseConfig.TRUSTEDPARTS_API_KEY,
            'base_url': BaseConfig.TRUSTEDPARTS_BASE_URL,
            'rate_limit': 300,  # requests per hour
            'features': ['multi_supplier_search', 'price_comparison']
        },
        'winsource': {
            'enabled': bool(BaseConfig.WINSOURCE_API_KEY),
            'api_key': BaseConfig.WINSOURCE_API_KEY,
            'base_url': BaseConfig.WINSOURCE_BASE_URL,
            'rate_limit': 250,  # requests per hour
            'features': ['pricing', 'availability', 'global_supply']
        },
        'sourcengine': {
            'enabled': bool(BaseConfig.SOURCENGINE_API_KEY),
            'api_key': BaseConfig.SOURCENGINE_API_KEY,
            'base_url': BaseConfig.SOURCENGINE_BASE_URL,
            'rate_limit': 400,  # requests per hour
            'features': ['supplier_matching', 'rfq_automation']
        },
        'luminovo': {
            'enabled': bool(BaseConfig.LUMINOVO_API_KEY),
            'api_key': BaseConfig.LUMINOVO_API_KEY,
            'base_url': BaseConfig.LUMINOVO_BASE_URL,
            'rate_limit': 200,  # requests per hour
            'features': ['procurement_automation', 'supply_chain_optimization']
        }
    }

# Industry-specific configuration
def get_industry_config():
    """Get industry-specific configuration for electrical construction"""
    return {
        'electrical_standards': {
            'nec_2023': {
                'enabled': True,
                'required_compliance': True,
                'auto_validation': True,
                'sections_to_check': [
                    '310.60', '430.52', '250.4', '440.14', '310.16',
                    '210.20', '430.32', '250.122', '310.15'
                ]
            },
            'ul_standards': {
                'ul_508a': {'required': True, 'auto_verify': True},
                'ul_891': {'required': True, 'auto_verify': True},
                'ul_1558': {'required': True, 'auto_verify': True}
            },
            'ieee_standards': {
                'ieee_141': {'reference': True, 'compliance_check': False},
                'ieee_242': {'reference': True, 'compliance_check': False},
                'ieee_1584': {'arc_flash': True, 'required': True}
            }
        },
        'component_categories': {
            'circuit_breakers': {
                'required_certifications': ['UL 508A'],
                'nec_sections': ['430.52', '240.6'],
                'voltage_ratings': ['120V', '240V', '480V', '600V'],
                'current_ratings': ['15A', '20A', '30A', '50A', '100A', '200A', '400A']
            },
            'disconnect_switches': {
                'required_certifications': ['UL 98'],
                'nec_sections': ['440.14', '430.107'],
                'voltage_ratings': ['240V', '480V', '600V'],
                'current_ratings': ['30A', '60A', '100A', '200A', '400A', '600A']
            },
            'terminal_blocks': {
                'required_certifications': ['UL 1059'],
                'nec_sections': ['110.14', '312.6'],
                'voltage_ratings': ['300V', '600V'],
                'current_ratings': ['10A', '20A', '30A', '60A', '100A']
            },
            'wiring_devices': {
                'required_certifications': ['UL 498'],
                'nec_sections': ['210.7', '250.146'],
                'types': ['receptacles', 'switches', 'wall_plates']
            }
        },
        'bom_optimization': {
            'supplier_consolidation': True,
            'volume_discounts': True,
            'lead_time_optimization': True,
            'risk_assessment': True,
            'alternative_parts': True
        },
        'real_time_features': {
            'price_monitoring': True,
            'availability_tracking': True,
            'lead_time_updates': True,
            'supplier_performance': True,
            'market_price_trends': True
        }
    }

# Problem-specific solutions configuration
def get_pain_point_solutions():
    """Get configuration for addressing industry pain points"""
    return {
        'procurement_automation': {
            'enabled': True,
            'real_time_pricing': True,
            'supplier_integration': True,
            'automated_quoting': True,
            'purchase_order_generation': True,
            'inventory_tracking': True
        },
        'nec_compliance': {
            'enabled': True,
            'auto_validation': True,
            'code_section_mapping': True,
            'risk_assessment': True,
            'corrective_action_suggestions': True,
            'compliance_reporting': True
        },
        'bim_integration': {
            'enabled': True,
            'model_validation': True,
            'clash_detection': True,
            'quantity_extraction': True,
            'cost_estimation': True,
            'change_management': True
        },
        'project_management': {
            'timeline_optimization': True,
            'resource_allocation': True,
            'risk_management': True,
            'change_control': True,
            'progress_tracking': True,
            'quality_assurance': True
        },
        'data_accuracy': {
            'real_time_updates': True,
            'multi_source_validation': True,
            'quality_scoring': True,
            'version_control': True,
            'audit_trail': True,
            'error_detection': True
        }
    }

# Export configuration
__all__ = ['config', 'BaseConfig', 'DevelopmentConfig', 'TestingConfig', 
           'ProductionConfig', 'StagingConfig', 'get_supplier_config',
           'get_industry_config', 'get_pain_point_solutions']

if __name__ == "__main__":
    # Example usage
    import os
    os.environ['FLASK_ENV'] = 'development'
    
    from enhanced_config import get_supplier_config, get_industry_config, get_pain_point_solutions
    
    # Print configuration
    suppliers = get_supplier_config()
    print("Supplier Configuration:")
    for name, config in suppliers.items():
        print(f"  {name}: {'Enabled' if config['enabled'] else 'Disabled'}")
    
    industry = get_industry_config()
    print("\nIndustry Configuration:")
    print(f"  NEC 2023: {'Enabled' if industry['electrical_standards']['nec_2023']['enabled'] else 'Disabled'}")
    print(f"  UL Standards: {len([k for k, v in industry['electrical_standards']['ul_standards'].items() if v['required']])} required")
    
    solutions = get_pain_point_solutions()
    print("\nPain Point Solutions:")
    for solution, config in solutions.items():
        print(f"  {solution}: {'Enabled' if config['enabled'] else 'Disabled'}")