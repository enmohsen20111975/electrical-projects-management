import json
import random
import math
from datetime import datetime, timedelta

class AICostEstimator:
    """AI-powered cost estimation engine"""
    
    def __init__(self):
        self.material_cost_trends = self._initialize_material_trends()
        self.labor_rate_data = self._initialize_labor_rates()
        self.project_complexity_factors = self._initialize_complexity_factors()
    
    def _initialize_material_trends(self):
        """Initialize material cost trends (simulated real-time data)"""
        return {
            'copper': {'base_price': 4.50, 'volatility': 0.15, 'trend': 'increasing'},
            'aluminum': {'base_price': 2.20, 'volatility': 0.12, 'trend': 'stable'},
            'steel_conduit': {'base_price': 1.80, 'volatility': 0.20, 'trend': 'increasing'},
            'circuit_breakers': {'base_price': 250.00, 'volatility': 0.08, 'trend': 'stable'},
            'transformers': {'base_price': 5000.00, 'volatility': 0.10, 'trend': 'stable'},
            'labor_hours': {'base_rate': 85.00, 'volatility': 0.05, 'trend': 'increasing'}
        }
    
    def _initialize_labor_rates(self):
        """Initialize regional labor rates"""
        return {
            'electrical_supervision': 95.00,
            'master_electrician': 85.00,
            'journeyman_electrician': 65.00,
            'apprentice': 35.00,
            'helper': 25.00
        }
    
    def _initialize_complexity_factors(self):
        """Initialize project complexity cost factors"""
        return {
            'industrial': {'base_factor': 1.2, 'risk_multiplier': 1.15},
            'commercial': {'base_factor': 1.0, 'risk_multiplier': 1.1},
            'residential': {'base_factor': 0.8, 'risk_multiplier': 1.0},
            'utility_scale': {'base_factor': 1.5, 'risk_multiplier': 1.25}
        }
    
    def generate_estimate(self, project_data, historical_projects):
        """
        Generate AI-powered cost estimate for a project
        
        Args:
            project_data: Dict containing project specifications
            historical_projects: List of historical Project objects
        
        Returns:
            dict: Comprehensive cost estimate
        """
        # Extract project parameters
        project_type = project_data.get('type', 'commercial')
        voltage_level = project_data.get('voltage_level', '480V')
        complexity = project_data.get('complexity', 'medium')
        location = project_data.get('location', 'urban')
        timeline = project_data.get('timeline_months', 6)
        
        # Get base complexity factor
        complexity_data = self.project_complexity_factors.get(project_type, self.project_complexity_factors['commercial'])
        base_factor = complexity_data['base_factor']
        risk_multiplier = complexity_data['risk_multiplier']
        
        # Calculate material costs with AI prediction
        material_costs = self._predict_material_costs(project_data)
        
        # Calculate labor costs
        labor_costs = self._calculate_labor_costs(project_data, complexity)
        
        # Calculate specialized costs (permits, engineering, testing)
        specialized_costs = self._calculate_specialized_costs(project_data)
        
        # Apply AI-driven risk adjustments
        risk_adjustments = self._calculate_risk_adjustments(project_data, risk_multiplier)
        
        # Calculate total base cost
        total_base_cost = sum(material_costs.values()) + sum(labor_costs.values()) + sum(specialized_costs.values())
        
        # Apply final adjustments
        ai_adjustments = self._apply_ai_adjustments(total_base_cost, project_data, historical_projects)
        final_cost = total_base_cost + ai_adjustments['total_adjustment']
        
        return {
            'project_overview': {
                'type': project_type,
                'voltage_level': voltage_level,
                'complexity': complexity,
                'location': location,
                'timeline_months': timeline
            },
            'cost_breakdown': {
                'materials': {
                    'subtotal': sum(material_costs.values()),
                    'details': material_costs
                },
                'labor': {
                    'subtotal': sum(labor_costs.values()),
                    'details': labor_costs
                },
                'specialized': {
                    'subtotal': sum(specialized_costs.values()),
                    'details': specialized_costs
                },
                'risk_adjustments': {
                    'subtotal': sum(risk_adjustments.values()),
                    'details': risk_adjustments
                }
            },
            'ai_predictions': {
                'base_estimate': total_base_cost,
                'ai_adjustments': ai_adjustments,
                'final_estimate': final_cost,
                'confidence_interval': self._calculate_confidence_interval(final_cost, project_data),
                'accuracy_probability': self._calculate_accuracy_probability(project_data)
            },
            'market_insights': self._generate_market_insights(project_data),
            'risk_factors': self._identify_risk_factors(project_data),
            'optimization_recommendations': self._generate_optimization_recommendations(project_data, final_cost)
        }
    
    def _predict_material_costs(self, project_data):
        """Predict material costs using AI patterns"""
        materials = {}
        
        # Copper conductor prediction
        if project_data.get('copper_conductor_needed', True):
            copper_weight_lbs = project_data.get('copper_weight_lbs', 1000)
            copper_price = self.material_cost_trends['copper']['base_price']
            # Apply volatility and trend
            volatility_factor = 1 + random.uniform(-0.1, 0.1)
            materials['copper_conductor'] = round(copper_weight_lbs * copper_price * volatility_factor, 2)
        
        # Breakers and protective devices
        num_breakers = project_data.get('num_breakers', 20)
        breaker_unit_cost = self.material_cost_trends['circuit_breakers']['base_price']
        breaker_factor = 1 + random.uniform(-0.05, 0.15)
        materials['circuit_breakers'] = round(num_breakers * breaker_unit_cost * breaker_factor, 2)
        
        # Transformers
        num_transformers = project_data.get('num_transformers', 2)
        transformer_cost = self.material_cost_trends['transformers']['base_price']
        transformer_factor = 1 + random.uniform(-0.08, 0.08)
        materials['transformers'] = round(num_transformers * transformer_cost * transformer_factor, 2)
        
        # Conduit and raceway
        conduit_feet = project_data.get('conduit_feet', 5000)
        conduit_unit_cost = self.material_cost_trends['steel_conduit']['base_price']
        conduit_factor = 1 + random.uniform(-0.05, 0.20)
        materials['conduit_raceway'] = round(conduit_feet * conduit_unit_cost * conduit_factor, 2)
        
        # Add AI-predicted additional materials
        ai_materials = self._predict_additional_materials(project_data)
        materials.update(ai_materials)
        
        return materials
    
    def _calculate_labor_costs(self, project_data, complexity):
        """Calculate labor costs based on complexity and AI prediction"""
        labor_costs = {}
        
        # Base labor hours from project complexity
        complexity_hours = {
            'low': 2000,
            'medium': 5000,
            'high': 10000,
            'extreme': 20000
        }
        
        base_hours = complexity_hours.get(complexity, complexity_hours['medium'])
        
        # Apply AI adjustment based on historical patterns
        ai_efficiency_factor = random.uniform(0.9, 1.1)  # Simulated AI efficiency prediction
        adjusted_hours = base_hours * ai_efficiency_factor
        
        # Calculate costs by skill level
        labor_breakdown = {
            'electrical_supervision': 0.1,
            'master_electrician': 0.3,
            'journeyman_electrician': 0.4,
            'apprentice': 0.15,
            'helper': 0.05
        }
        
        for skill, percentage in labor_breakdown.items():
            hours = adjusted_hours * percentage
            rate = self.labor_rate_data[skill]
            # Apply regional and market factors
            regional_factor = 1 + random.uniform(-0.1, 0.2)
            cost = hours * rate * regional_factor
            labor_costs[skill] = round(cost, 2)
        
        return labor_costs
    
    def _calculate_specialized_costs(self, project_data):
        """Calculate specialized costs (permits, testing, engineering)"""
        specialized_costs = {}
        
        # Engineering design
        engineering_percent = random.uniform(0.08, 0.15)
        project_value = project_data.get('estimated_project_value', 100000)
        specialized_costs['engineering_design'] = round(project_value * engineering_percent, 2)
        
        # Permits and inspections
        permit_cost = project_data.get('permit_cost', 5000)
        inspection_cost = project_data.get('inspection_cost', 3000)
        specialized_costs['permits_inspections'] = round(permit_cost + inspection_cost, 2)
        
        # Testing and commissioning
        testing_cost = project_value * random.uniform(0.02, 0.05)
        specialized_costs['testing_commissioning'] = round(testing_cost, 2)
        
        # Project management
        pm_cost = project_value * random.uniform(0.05, 0.1)
        specialized_costs['project_management'] = round(pm_cost, 2)
        
        return specialized_costs
    
    def _calculate_risk_adjustments(self, project_data, risk_multiplier):
        """Calculate risk-based cost adjustments"""
        risk_adjustments = {}
        
        # Material price volatility
        materials_at_risk = project_data.get('materials_at_risk', 0.15)
        risk_adjustments['material_volatility'] = round(project_data.get('estimated_project_value', 100000) * materials_at_risk * 0.5, 2)
        
        # Schedule risk
        schedule_pressure = project_data.get('schedule_pressure', 0.1)
        risk_adjustments['schedule_risk'] = round(project_data.get('estimated_project_value', 100000) * schedule_pressure * 0.8, 2)
        
        # Technical complexity risk
        tech_risk = project_data.get('technical_complexity', 0.1)
        risk_adjustments['technical_risk'] = round(project_data.get('estimated_project_value', 100000) * tech_risk * 0.6, 2)
        
        # Apply overall risk multiplier
        risk_adjustments['contingency'] = round(sum(risk_adjustments.values()) * (risk_multiplier - 1), 2)
        
        return risk_adjustments
    
    def _apply_ai_adjustments(self, base_cost, project_data, historical_projects):
        """Apply AI-driven adjustments based on historical data"""
        adjustments = {}
        
        # Market timing adjustment
        current_month = datetime.now().month
        seasonal_factor = 1.0 + 0.1 * math.sin(2 * math.pi * current_month / 12)
        adjustments['seasonal_adjustment'] = round(base_cost * (seasonal_factor - 1), 2)
        
        # Historical performance factor
        if historical_projects:
            avg_performance = sum(p.progress for p in historical_projects) / len(historical_projects)
            performance_factor = avg_performance / 100
            adjustments['historical_performance'] = round(base_cost * (performance_factor - 1) * -0.1, 2)
        
        # Regional market adjustment
        regional_factor = project_data.get('regional_factor', 1.0)
        adjustments['regional_market'] = round(base_cost * (regional_factor - 1), 2)
        
        # Learning curve improvement
        learning_improvement = random.uniform(0.02, 0.08)  # 2-8% improvement
        adjustments['learning_curve'] = round(base_cost * -learning_improvement, 2)
        
        adjustments['total_adjustment'] = sum(adjustments.values())
        
        return adjustments
    
    def _calculate_confidence_interval(self, estimate, project_data):
        """Calculate confidence interval for the estimate"""
        # Base confidence on project clarity and data quality
        data_quality = project_data.get('data_quality_score', 0.7)  # 0-1 scale
        project_complexity = project_data.get('complexity_score', 0.5)
        
        # Higher complexity and lower data quality = wider confidence interval
        confidence_width = (1 - data_quality) * 0.3 + project_complexity * 0.2
        
        lower_bound = estimate * (1 - confidence_width)
        upper_bound = estimate * (1 + confidence_width)
        
        return {
            'lower_bound': round(lower_bound, 2),
            'upper_bound': round(upper_bound, 2),
            'width_percent': round(confidence_width * 100, 1)
        }
    
    def _calculate_accuracy_probability(self, project_data):
        """Calculate probability of estimate accuracy"""
        # Base accuracy factors
        completeness = project_data.get('specification_completeness', 0.8)
        historical_similarity = project_data.get('historical_similarity', 0.7)
        market_stability = project_data.get('market_stability', 0.6)
        
        # Calculate weighted accuracy probability
        accuracy = (completeness * 0.4 + historical_similarity * 0.3 + market_stability * 0.3)
        
        return round(accuracy * 100, 1)  # Return as percentage
    
    def _predict_additional_materials(self, project_data):
        """Predict additional materials not explicitly specified"""
        additional = {}
        
        # Hardware and fasteners (estimated at 2% of project value)
        project_value = project_data.get('estimated_project_value', 100000)
        additional['hardware_fasteners'] = round(project_value * 0.02, 2)
        
        # Cable accessories and terminations
        additional['cable_accessories'] = round(project_value * 0.01, 2)
        
        # Grounding materials
        additional['grounding_materials'] = round(project_value * 0.015, 2)
        
        return additional
    
    def _generate_market_insights(self, project_data):
        """Generate market insights for the project"""
        return {
            'material_market_trend': 'increasing' if random.random() > 0.5 else 'stable',
            'labor_market_trend': 'tight' if random.random() > 0.6 else 'adequate',
            'supply_chain_risk': 'low' if random.random() > 0.3 else 'medium',
            'recommended_purchase_timing': 'immediate' if random.random() > 0.4 else 'delayed',
            'key_suppliers': ['Graybar', 'WESCO', 'Schneider Electric', 'Siemens']
        }
    
    def _identify_risk_factors(self, project_data):
        """Identify key risk factors for the project"""
        risk_factors = []
        
        # Voltage level risk
        voltage = project_data.get('voltage_level', '480V')
        if 'kV' in voltage:
            risk_factors.append({
                'factor': 'High Voltage',
                'probability': 'medium',
                'impact': 'high',
                'mitigation': 'Specialized crews and equipment required'
            })
        
        # Timeline risk
        timeline = project_data.get('timeline_months', 6)
        if timeline < 6:
            risk_factors.append({
                'factor': 'Compressed Timeline',
                'probability': 'high',
                'impact': 'medium',
                'mitigation': 'Additional crews and overtime'
            })
        
        # Location risk
        if project_data.get('location') == 'rural':
            risk_factors.append({
                'factor': 'Remote Location',
                'probability': 'medium',
                'impact': 'medium',
                'mitigation': 'Increased mobilization costs and logistics planning'
            })
        
        return risk_factors
    
    def _generate_optimization_recommendations(self, project_data, estimate):
        """Generate cost optimization recommendations"""
        recommendations = []
        
        # Material optimization
        if estimate > project_data.get('budget_target', estimate * 1.2):
            recommendations.append({
                'category': 'Materials',
                'potential_savings': round(estimate * 0.05, 2),
                'recommendation': 'Consider aluminum conductors where code permits',
                'implementation': 'Replace copper with aluminum in non-critical circuits'
            })
        
        # Labor optimization
        recommendations.append({
            'category': 'Labor',
            'potential_savings': round(estimate * 0.03, 2),
            'recommendation': 'Optimize crew composition and scheduling',
            'implementation': 'Use more apprentices with increased supervision'
        })
        
        # Timeline optimization
        recommendations.append({
            'category': 'Schedule',
            'potential_savings': round(estimate * 0.02, 2),
            'recommendation': 'Parallel work activities where safe',
            'implementation': 'Coordinate with other trades for earlier access'
        })
        
        return recommendations
    
    def extract_drawing_data(self, file_path):
        """
        Simulate AI extraction of electrical symbols and components from drawings
        
        Args:
            file_path: Path to uploaded drawing file
        
        Returns:
            dict: Extracted electrical components and quantities
        """
        # Simulate AI analysis results
        extracted_data = {
            'symbols_detected': {
                'circuit_breakers': random.randint(15, 25),
                'transformers': random.randint(2, 5),
                'panelboards': random.randint(3, 8),
                'conduits': random.randint(50, 150),
                'junction_boxes': random.randint(10, 30)
            },
            'total_components': 0,
            'estimated_conductor_length': 0,
            'drawing_quality_score': round(random.uniform(0.7, 0.95), 2),
            'extraction_confidence': round(random.uniform(0.85, 0.98), 2)
        }
        
        extracted_data['total_components'] = sum(extracted_data['symbols_detected'].values())
        extracted_data['estimated_conductor_length'] = random.randint(2000, 8000)  # feet
        
        return extracted_data

class ElectricalCalculator:
    """Standard Electrical Engineering Calculations"""
    
    @staticmethod
    def calculate_voltage_drop(voltage, current, distance_ft, conductor_size, conductor_material='copper', conduit_type='steel'):
        """
        Calculate voltage drop based on NEC Chapter 9 Table 8 & 9
        Formula: VD = 2 * K * L * I / CM (Approx) or Exact: VD = I * (R cos(theta) + X sin(theta)) * L
        Using simplified effective Z for standard power factor 0.85
        """
        # Simplified impedance values (Ohms/1000ft) for 0.85 PF
        # Source: NEC Chapter 9 Table 9 (Effective Z at 0.85 PF)
        impedance_table = {
            '14': 3.1, '12': 2.0, '10': 1.2, '8': 0.78, '6': 0.49,
            '4': 0.31, '2': 0.19, '1/0': 0.12, '2/0': 0.10, '3/0': 0.083, '4/0': 0.067
        }
        
        z = impedance_table.get(conductor_size, 0.1) # Default to low Z if not found
        if conductor_material == 'aluminum':
            z *= 1.6
            
        # VD = I * Z * (L/1000)
        vd = current * z * (distance_ft / 1000.0)
        vd_percent = (vd / voltage) * 100
        
        return {
            'voltage_drop_volts': round(vd, 2),
            'voltage_drop_percent': round(vd_percent, 2),
            'acceptable': vd_percent <= 3.0 # NEC recommendation for branch circuits
        }

    @staticmethod
    def calculate_fault_current(source_voltage, source_mva, transformer_kva, transformer_impedance_percent, conductor_impedance=0):
        """
        Calculate Available Fault Current (Point-to-Point)
        """
        # 1. Calculate Transformer Full Load Amps
        # I_FLA = kVA * 1000 / (Voltage * 1.732)
        i_fla = (transformer_kva * 1000) / (source_voltage * 1.732)
        
        # 2. Calculate Multiplier
        multiplier = 100 / transformer_impedance_percent
        
        # 3. Calculate SCA at Transformer Secondary
        sca_transformer = i_fla * multiplier
        
        # If conductor impedance is provided, reduce fault current (simplified)
        # In reality, would add Z_source + Z_transformer + Z_cable
        final_sca = sca_transformer # Placeholder for full point-to-point
        
        return {
            'available_fault_current_amps': round(final_sca, 0),
            'transformer_fla': round(i_fla, 1)
        }

    @staticmethod
    def calculate_cable_sizing(current_amps, voltage, ambient_temp_c=30, num_conductors=3):
        """
        Size cable based on NEC 310.15
        """
        # Simplified Ampacity Table (75C column, Copper)
        ampacity_table = {
            '14': 20, '12': 25, '10': 35, '8': 50, '6': 65,
            '4': 85, '2': 115, '1/0': 150, '2/0': 175, '3/0': 200, '4/0': 230
        }
        
        # Temperature Correction (30C base)
        temp_correction = 1.0
        if ambient_temp_c > 30:
            temp_correction = 0.9 # Simplified
            
        # Fill Adjustment
        fill_adjustment = 1.0
        if num_conductors > 3:
            fill_adjustment = 0.8
            
        required_ampacity = current_amps * 1.25 # Continuous load
        
        selected_size = "Unknown"
        rated_ampacity = 0
        
        for size, ampacity in ampacity_table.items():
            derated_ampacity = ampacity * temp_correction * fill_adjustment
            if derated_ampacity >= required_ampacity:
                selected_size = size
                rated_ampacity = derated_ampacity
                break
                
        return {
            'recommended_size': selected_size,
            'rated_ampacity': round(rated_ampacity, 1),
            'required_ampacity': round(required_ampacity, 1)
        }

    @staticmethod
    def calculate_breaker_sizing(load_amps, load_type='continuous'):
        """
        Size circuit breaker based on NEC 240
        """
        factor = 1.25 if load_type == 'continuous' else 1.0
        required_rating = load_amps * factor
        
        standard_sizes = [15, 20, 30, 40, 50, 60, 70, 80, 90, 100, 125, 150, 175, 200, 225, 250]
        
        selected_size = next((size for size in standard_sizes if size >= required_rating), 250)
        
        return {
            'recommended_trip_rating': selected_size,
            'minimum_rating': round(required_rating, 1)
        }

    @staticmethod
    def calculate_motor_startup(motor_hp, voltage, method='dol'):
        """
        Analyze motor startup characteristics
        """
        # Estimate FLA from HP (NEC Table 430.250 approx)
        # 460V 3-phase approx
        fla_map = {
            5: 7.6, 7.5: 11, 10: 14, 15: 21, 20: 27, 25: 34, 30: 40, 40: 52, 50: 65, 75: 96, 100: 124
        }
        fla = fla_map.get(motor_hp, motor_hp * 1.2) # Fallback
        
        # Locked Rotor Current (Code Letter G approx 6x FLA)
        lrc = fla * 6.0
        
        if method == 'soft_start':
            lrc *= 0.4
        elif method == 'vfd':
            lrc = fla * 1.1
            
        return {
            'full_load_amps': fla,
            'locked_rotor_amps': round(lrc, 1),
            'startup_method': method
        }

    @staticmethod
    def calculate_contactor_sizing(motor_hp, voltage):
        """
        Size NEMA/IEC contactor
        """
        # NEMA Sizes
        if voltage >= 440:
            if motor_hp <= 10: size = 1
            elif motor_hp <= 25: size = 2
            elif motor_hp <= 50: size = 3
            elif motor_hp <= 100: size = 4
            else: size = 5
        else:
            size = 1 # Default
            
        return {
            'nema_size': size,
            'voltage': voltage,
            'max_hp': motor_hp
        }