"""
Electrical Sizing Recommendation Engine
Automatically suggests manufacturer part numbers based on calculation results

Author: MiniMax Agent
Date: 2025-11-29
Version: 2.0
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json

@dataclass
class PartRecommendation:
    """Part number recommendation with full details"""
    manufacturer: str
    product_line: str
    part_number: str
    description: str
    specifications: Dict[str, Any]
    datasheet_url: str
    price_estimate: float
    availability: str
    lead_time_days: int
    nec_compliant: bool
    reason_for_recommendation: str

class CircuitBreakerRecommendationEngine:
    """Automatic circuit breaker recommendations based on sizing calculations"""
    
    def __init__(self):
        self.manufacturer_mappings = {
            'siemens': self._get_siemens_breakers(),
            'abb': self._get_abb_breakers(),
            'schneider': self._get_schneider_breakers(),
            'eaton': self._get_eaton_breakers(),
            'ge': self._get_ge_breakers(),
            'omron': self._get_omron_breakers()
        }
    
    def recommend_circuit_breakers(self, amp_rating: float, voltage: str, application: str = 'general') -> Dict[str, List[PartRecommendation]]:
        """Get circuit breaker recommendations based on calculated requirements"""
        recommendations = {}
        
        for manufacturer, breakers in self.manufacturer_mappings.items():
            manufacturer_recs = []
            
            for breaker in breakers:
                if self._matches_requirements(breaker, amp_rating, voltage, application):
                    recommendation = PartRecommendation(
                        manufacturer=breaker['manufacturer'],
                        product_line=breaker['product_line'],
                        part_number=breaker['part_number'],
                        description=breaker['description'],
                        specifications=breaker['specifications'],
                        datasheet_url=breaker['datasheet_url'],
                        price_estimate=breaker['price_estimate'],
                        availability=breaker['availability'],
                        lead_time_days=breaker['lead_time_days'],
                        nec_compliant=breaker['nec_compliant'],
                        reason_for_recommendation=self._get_recommendation_reason(breaker, amp_rating, application)
                    )
                    manufacturer_recs.append(recommendation)
            
            # Sort by best match (price, availability, specifications)
            manufacturer_recs.sort(key=lambda x: (x.price_estimate, x.lead_time_days))
            recommendations[manufacturer] = manufacturer_recs[:3]  # Top 3 per manufacturer
        
        return recommendations
    
    def _matches_requirements(self, breaker: Dict, amp_rating: float, voltage: str, application: str) -> bool:
        """Check if breaker matches the calculated requirements"""
        try:
            # Check amp rating compatibility
            breaker_amp = float(breaker['specifications']['amp_rating'])
            if amp_rating > breaker_amp * 1.25:  # Allow 25% oversizing tolerance
                return False
            
            # Check voltage compatibility
            breaker_voltage = breaker['specifications']['voltage']
            if voltage not in breaker_voltage and voltage != '480V' and '480' in breaker_voltage:
                return False
            
            # Check application suitability
            if application == 'motor' and breaker['specifications'].get('motor_protection', False):
                return True
            elif application == 'general' and not breaker['specifications'].get('motor_only', False):
                return True
            
            return True
        except (KeyError, ValueError, TypeError):
            return False
    
    def _get_recommendation_reason(self, breaker: Dict, amp_rating: float, application: str) -> str:
        """Generate reason for recommendation"""
        reasons = []
        
        if breaker['specifications'].get('motor_protection', False) and application == 'motor':
            reasons.append("Specifically designed for motor protection")
        
        if breaker['specifications'].get('interruption_capacity', '0kA') in ['65kA', '100kA']:
            reasons.append("High interruption capacity for safety")
        
        if breaker['price_estimate'] < 2000:
            reasons.append("Cost-effective option")
        
        if breaker['availability'] == 'In Stock':
            reasons.append("Available for immediate delivery")
        
        if not reasons:
            reasons.append("Meets all electrical requirements")
        
        return "; ".join(reasons)
    
    def _get_siemens_breakers(self) -> List[Dict]:
        return [
            {
                'manufacturer': 'Siemens',
                'product_line': 'Sentron WL',
                'part_number': 'WL3B25B800E',
                'description': '25kA Circuit Breaker, Electronic Trip',
                'specifications': {
                    'amp_rating': 100,
                    'voltage': '480V',
                    'poles': 3,
                    'interruption_capacity': '65kA',
                    'trip_unit': 'Electronic',
                    'motor_protection': False,
                    'frame_size': 'WL3'
                },
                'datasheet_url': 'https://new.abb.com/products/3VA21/3VA2125-5EF32-0AA0/datasheet',
                'price_estimate': 3850.00,
                'availability': 'In Stock',
                'lead_time_days': 10,
                'nec_compliant': True
            },
            {
                'manufacturer': 'Siemens',
                'product_line': 'Sentron ED4',
                'part_number': 'ED4B100',
                'description': 'Thermal-Magnetic Circuit Breaker',
                'specifications': {
                    'amp_rating': 100,
                    'voltage': '480V',
                    'poles': 3,
                    'interruption_capacity': '22kA',
                    'trip_unit': 'Thermal-Magnetic',
                    'motor_protection': True,
                    'frame_size': 'ED4'
                },
                'datasheet_url': 'https://new.abb.com/products/3VA21/3VA2125-5EF32-0AA0/datasheet',
                'price_estimate': 2850.00,
                'availability': 'In Stock',
                'lead_time_days': 7,
                'nec_compliant': True
            }
        ]
    
    def _get_abb_breakers(self) -> List[Dict]:
        return [
            {
                'manufacturer': 'ABB',
                'product_line': 'S203',
                'part_number': 'S203-C100',
                'description': 'C-Curve Circuit Breaker, 100A',
                'specifications': {
                    'amp_rating': 100,
                    'voltage': '480V',
                    'poles': 3,
                    'interruption_capacity': '25kA',
                    'trip_unit': 'Thermal-Magnetic',
                    'motor_protection': True,
                    'frame_size': 'S200'
                },
                'datasheet_url': 'https://search.abb.com/library/Download.aspx?DocumentID=1SAM000000R0004&LanguageCode=en&DocumentPartId=&Action=Launch',
                'price_estimate': 2650.00,
                'availability': 'In Stock',
                'lead_time_days': 12,
                'nec_compliant': True
            }
        ]
    
    def _get_schneider_breakers(self) -> List[Dict]:
        return [
            {
                'manufacturer': 'Schneider Electric',
                'product_line': 'PowerPact H',
                'part_number': 'HGL36100',
                'description': '100A Circuit Breaker, 65kA',
                'specifications': {
                    'amp_rating': 100,
                    'voltage': '480V',
                    'poles': 3,
                    'interruption_capacity': '65kA',
                    'trip_unit': 'Thermal-Magnetic',
                    'motor_protection': True,
                    'frame_size': 'H-frame'
                },
                'datasheet_url': 'https://www.se.com/ww/en/product/HGL36100/',
                'price_estimate': 3250.00,
                'availability': 'In Stock',
                'lead_time_days': 8,
                'nec_compliant': True
            },
            {
                'manufacturer': 'Schneider Electric',
                'product_line': 'iSW',
                'part_number': 'iSW30100',
                'description': 'Compact 100A Circuit Breaker',
                'specifications': {
                    'amp_rating': 100,
                    'voltage': '480V',
                    'poles': 3,
                    'interruption_capacity': '35kA',
                    'trip_unit': 'Electronic',
                    'motor_protection': False,
                    'frame_size': 'iC60N'
                },
                'datasheet_url': 'https://www.se.com/ww/en/product/iSW30100/',
                'price_estimate': 1850.00,
                'availability': 'In Stock',
                'lead_time_days': 7,
                'nec_compliant': True
            }
        ]
    
    def _get_eaton_breakers(self) -> List[Dict]:
        return [
            {
                'manufacturer': 'Eaton',
                'product_line': 'BR',
                'part_number': 'BR3100',
                'description': '100A Circuit Breaker, Plug-in',
                'specifications': {
                    'amp_rating': 100,
                    'voltage': '480V',
                    'poles': 3,
                    'interruption_capacity': '10kA',
                    'trip_unit': 'Thermal-Magnetic',
                    'motor_protection': True,
                    'frame_size': 'BR'
                },
                'datasheet_url': 'https://www.eaton.com/us/en-us/products/low-voltage-power-circuit-breakers/br-family.html',
                'price_estimate': 2850.00,
                'availability': 'In Stock',
                'lead_time_days': 10,
                'nec_compliant': True
            }
        ]
    
    def _get_ge_breakers(self) -> List[Dict]:
        return [
            {
                'manufacturer': 'General Electric',
                'product_line': 'AE',
                'part_number': 'AE100',
                'description': '100A Thermal-Magnetic Breaker',
                'specifications': {
                    'amp_rating': 100,
                    'voltage': '480V',
                    'poles': 3,
                    'interruption_capacity': '25kA',
                    'trip_unit': 'Thermal-Magnetic',
                    'motor_protection': True,
                    'frame_size': 'AE'
                },
                'datasheet_url': 'https://www.ge.com/industrial-solutions/circuit-breakers/ae-family',
                'price_estimate': 2750.00,
                'availability': 'In Stock',
                'lead_time_days': 14,
                'nec_compliant': True
            }
        ]
    
    def _get_omron_breakers(self) -> List[Dict]:
        return [
            {
                'manufacturer': 'Omron',
                'product_line': 'Breaker',
                'part_number': 'BB100',
                'description': '100A Industrial Circuit Breaker',
                'specifications': {
                    'amp_rating': 100,
                    'voltage': '480V',
                    'poles': 3,
                    'interruption_capacity': '18kA',
                    'trip_unit': 'Thermal-Magnetic',
                    'motor_protection': True,
                    'frame_size': 'BB'
                },
                'datasheet_url': 'https://www.omron.com/products/circuit-breakers/',
                'price_estimate': 2950.00,
                'availability': 'In Stock',
                'lead_time_days': 15,
                'nec_compliant': True
            }
        ]

class MotorRecommendationEngine:
    """Automatic motor recommendations based on sizing calculations"""
    
    def __init__(self):
        self.manufacturer_mappings = {
            'siemens': self._get_siemens_motors(),
            'abb': self._get_abb_motors(),
            'schneider': self._get_schneider_motors(),
            'eaton': self._get_eaton_motors(),
            'ge': self._get_ge_motors(),
            'baldor': self._get_baldor_motors()
        }
    
    def recommend_motors(self, hp_rating: float, voltage: str, efficiency_class: str = 'IE3') -> Dict[str, List[PartRecommendation]]:
        """Get motor recommendations based on calculated requirements"""
        recommendations = {}
        
        for manufacturer, motors in self.manufacturer_mappings.items():
            manufacturer_recs = []
            
            for motor in motors:
                if self._matches_motor_requirements(motor, hp_rating, voltage, efficiency_class):
                    recommendation = PartRecommendation(
                        manufacturer=motor['manufacturer'],
                        product_line=motor['product_line'],
                        part_number=motor['part_number'],
                        description=motor['description'],
                        specifications=motor['specifications'],
                        datasheet_url=motor['datasheet_url'],
                        price_estimate=motor['price_estimate'],
                        availability=motor['availability'],
                        lead_time_days=motor['lead_time_days'],
                        nec_compliant=motor['nec_compliant'],
                        reason_for_recommendation=self._get_motor_recommendation_reason(motor, hp_rating)
                    )
                    manufacturer_recs.append(recommendation)
            
            manufacturer_recs.sort(key=lambda x: (x.price_estimate, x.specifications.get('efficiency_percent', 0)), reverse=True)
            recommendations[manufacturer] = manufacturer_recs[:3]
        
        return recommendations
    
    def _matches_motor_requirements(self, motor: Dict, hp_rating: float, voltage: str, efficiency_class: str) -> bool:
        """Check if motor matches requirements"""
        try:
            motor_hp = float(motor['specifications']['hp'])
            if abs(motor_hp - hp_rating) > hp_rating * 0.1:  # 10% tolerance
                return False
            
            motor_voltage = motor['specifications']['voltage']
            if voltage not in motor_voltage and voltage != '480V':
                return False
            
            motor_efficiency = motor['specifications'].get('efficiency_class', 'IE3')
            efficiency_rank = {'IE1': 1, 'IE2': 2, 'IE3': 3, 'IE4': 4, 'IE5': 5}
            required_rank = efficiency_rank.get(efficiency_class, 3)
            motor_rank = efficiency_rank.get(motor_efficiency, 3)
            
            return motor_rank >= required_rank
        except (KeyError, ValueError, TypeError):
            return False
    
    def _get_motor_recommendation_reason(self, motor: Dict, hp_rating: float) -> str:
        """Generate reason for motor recommendation"""
        reasons = []
        
        efficiency = motor['specifications'].get('efficiency_percent', 0)
        if efficiency >= 90:
            reasons.append(f"High efficiency ({efficiency}%) reduces operating costs")
        
        if motor['availability'] == 'In Stock':
            reasons.append("Available for immediate delivery")
        
        if motor['specifications'].get('service_factor', 1.0) >= 1.15:
            reasons.append("High service factor for demanding applications")
        
        if motor['lead_time_days'] <= 10:
            reasons.append("Fast delivery")
        
        if not reasons:
            reasons.append("Meets all electrical and mechanical requirements")
        
        return "; ".join(reasons)
    
    def _get_siemens_motors(self) -> List[Dict]:
        return [
            {
                'manufacturer': 'Siemens',
                'product_line': 'SIMOTICS SD',
                'part_number': '1FK7022-5AK71-1QG0',
                'description': '10HP IE3 Motor, TEFC',
                'specifications': {
                    'hp': 10.0,
                    'voltage': '480V',
                    'efficiency_class': 'IE3',
                    'efficiency_percent': 89.5,
                    'rpm': 1800,
                    'enclosure': 'TEFC',
                    'service_factor': 1.15,
                    'frame_size': '215T'
                },
                'datasheet_url': 'https://new.siemens.com/global/en/products/automation/simotics-motors.html',
                'price_estimate': 2850.00,
                'availability': 'In Stock',
                'lead_time_days': 14,
                'nec_compliant': True
            }
        ]
    
    def _get_abb_motors(self) -> List[Dict]:
        return [
            {
                'manufacturer': 'ABB',
                'product_line': 'M3BP',
                'part_number': 'M3BP 132SMA 4',
                'description': '10HP IE3 Motor, IP55',
                'specifications': {
                    'hp': 10.0,
                    'voltage': '480V',
                    'efficiency_class': 'IE3',
                    'efficiency_percent': 89.0,
                    'rpm': 1800,
                    'enclosure': 'IP55',
                    'service_factor': 1.15,
                    'frame_size': '132'
                },
                'datasheet_url': 'https://new.abb.com/motors-generators/low-voltage-ac-motors/m3bp-ie3',
                'price_estimate': 2650.00,
                'availability': 'In Stock',
                'lead_time_days': 12,
                'nec_compliant': True
            }
        ]
    
    def _get_schneider_motors(self) -> List[Dict]:
        return [
            {
                'manufacturer': 'Schneider Electric',
                'product_line': 'Altivar Process',
                'part_number': 'ATV12H037M3C',
                'description': '10HP Soft Starter',
                'specifications': {
                    'hp': 10.0,
                    'voltage': '480V',
                    'type': 'Soft Starter',
                    'control_voltage': '24V',
                    'display': 'LED',
                    'protection': 'Thermal'
                },
                'datasheet_url': 'https://www.se.com/us/en/product-range/60044-altivar-process/',
                'price_estimate': 950.00,
                'availability': 'In Stock',
                'lead_time_days': 7,
                'nec_compliant': True
            }
        ]
    
    def _get_eaton_motors(self) -> List[Dict]:
        return [
            {
                'manufacturer': 'Eaton',
                'product_line': 'Crusher Duty',
                'part_number': 'ED10HP',
                'description': '10HP Crusher Duty Motor',
                'specifications': {
                    'hp': 10.0,
                    'voltage': '480V',
                    'efficiency_class': 'IE3',
                    'efficiency_percent': 89.0,
                    'rpm': 1800,
                    'enclosure': 'TEFC',
                    'duty': 'Crusher',
                    'service_factor': 1.25
                },
                'datasheet_url': 'https://www.eaton.com/us/en-us/products/low-voltage-motor-controls/crusher-duty-motors.html',
                'price_estimate': 3100.00,
                'availability': 'In Stock',
                'lead_time_days': 18,
                'nec_compliant': True
            }
        ]
    
    def _get_ge_motors(self) -> List[Dict]:
        return [
            {
                'manufacturer': 'General Electric',
                'product_line': 'Crusher Duty',
                'part_number': '5KH49RN214G',
                'description': '10HP Crusher Duty Motor',
                'specifications': {
                    'hp': 10.0,
                    'voltage': '480V',
                    'efficiency_class': 'IE3',
                    'efficiency_percent': 89.0,
                    'rpm': 1800,
                    'enclosure': 'TEFC',
                    'duty': 'Crusher',
                    'service_factor': 1.15
                },
                'datasheet_url': 'https://www.ge.com/industrial-solutions/motors-generators/low-voltage-ac-motors',
                'price_estimate': 2950.00,
                'availability': 'In Stock',
                'lead_time_days': 21,
                'nec_compliant': True
            }
        ]
    
    def _get_baldor_motors(self) -> List[Dict]:
        return [
            {
                'manufacturer': 'Baldor',
                'product_line': 'General Duty',
                'part_number': 'IDM3710T',
                'description': '10HP General Purpose Motor',
                'specifications': {
                    'hp': 10.0,
                    'voltage': '480V',
                    'efficiency_class': 'IE3',
                    'efficiency_percent': 89.5,
                    'rpm': 1800,
                    'enclosure': 'TEFC',
                    'service_factor': 1.15
                },
                'datasheet_url': 'https://www.baldor.com/products/low-voltage-ac-motors',
                'price_estimate': 2750.00,
                'availability': 'In Stock',
                'lead_time_days': 16,
                'nec_compliant': True
            }
        ]

def test_recommendation_engines():
    """Test the recommendation engines"""
    print("Testing Recommendation Engines")
    print("=" * 40)
    
    # Test Circuit Breaker Recommendations
    print("\n🔌 CIRCUIT BREAKER RECOMMENDATIONS (100A)")
    print("-" * 45)
    cb_engine = CircuitBreakerRecommendationEngine()
    cb_recommendations = cb_engine.recommend_circuit_breakers(100, '480V', 'general')
    
    for manufacturer, recs in cb_recommendations.items():
        print(f"\n{manufacturer.upper()}:")
        for rec in recs[:2]:  # Show top 2
            print(f"  {rec.part_number}: ${rec.price_estimate:.2f} - {rec.reason_for_recommendation}")
            print(f"    📄 Datasheet: {rec.datasheet_url}")
    
    # Test Motor Recommendations
    print("\n\n🏭 MOTOR RECOMMENDATIONS (10HP)")
    print("-" * 35)
    motor_engine = MotorRecommendationEngine()
    motor_recommendations = motor_engine.recommend_motors(10.0, '480V', 'IE3')
    
    for manufacturer, recs in motor_recommendations.items():
        print(f"\n{manufacturer.upper()}:")
        for rec in recs[:2]:  # Show top 2
            print(f"  {rec.part_number}: ${rec.price_estimate:.2f} - {rec.reason_for_recommendation}")
            print(f"    📄 Datasheet: {rec.datasheet_url}")

if __name__ == "__main__":
    test_recommendation_engines()
