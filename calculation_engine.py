import math
import json

class ElectricalCalculations:
    """Electrical engineering calculation engine"""
    
    def __init__(self):
        # Standard electrical constants
        self.VOLTAGE_STANDARDS = {
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
        
        # Cable resistance and reactance (per 1000 ft)
        self.CABLE_DATA = {
            'copper_awg': {
                '12': {'resistance': 1.93, 'reactance': 0.066},
                '10': {'resistance': 1.21, 'reactance': 0.064},
                '8': {'resistance': 0.76, 'reactance': 0.061},
                '6': {'resistance': 0.48, 'reactance': 0.059},
                '4': {'resistance': 0.30, 'reactance': 0.058},
                '2': {'resistance': 0.19, 'reactance': 0.056},
                '1/0': {'resistance': 0.12, 'reactance': 0.054},
                '2/0': {'resistance': 0.095, 'reactance': 0.053},
                '3/0': {'resistance': 0.075, 'reactance': 0.051},
                '4/0': {'resistance': 0.060, 'reactance': 0.050}
            }
        }
        
        # NEC conductor ampacity table (simplified)
        self.AMPACITY_TABLE = {
            'copper_thhn': {
                '12': 30, '10': 40, '8': 55, '6': 80, '4': 105,
                '2': 140, '1/0': 170, '2/0': 195, '3/0': 225, '4/0': 260
            },
            'aluminum_thhn': {
                '12': 25, '10': 35, '8': 50, '6': 65, '4': 85,
                '2': 115, '1/0': 135, '2/0': 155, '3/0': 180, '4/0': 205
            }
        }
    
    def calculate_load_flow(self, voltage, current, power_factor=0.8, distance=100):
        """
        Calculate load flow analysis
        
        Args:
            voltage: System voltage in volts
            current: Load current in amps
            power_factor: Power factor (0.0 to 1.0)
            distance: Cable distance in feet
        
        Returns:
            dict: Load flow results
        """
        # Calculate apparent power
        real_power = voltage * current * power_factor / 1000  # kW
        reactive_power = voltage * current * math.sin(math.acos(power_factor)) / 1000  # kVAR
        apparent_power = voltage * current / 1000  # kVA
        
        # Calculate voltage drop
        voltage_drop = self.calculate_voltage_drop(voltage, current, power_factor, distance)
        voltage_regulation = (voltage_drop / voltage) * 100
        
        # Calculate efficiency
        copper_losses = self.calculate_copper_losses(current, distance)
        efficiency = (real_power / (real_power + copper_losses / 1000)) * 100
        
        return {
            'input_values': {
                'voltage': voltage,
                'current': current,
                'power_factor': power_factor,
                'distance': distance
            },
            'load_analysis': {
                'real_power_kw': round(real_power, 2),
                'reactive_power_kvar': round(reactive_power, 2),
                'apparent_power_kva': round(apparent_power, 2),
                'power_factor': power_factor
            },
            'system_performance': {
                'voltage_drop_percent': round(voltage_regulation, 2),
                'efficiency_percent': round(efficiency, 2),
                'copper_losses_watts': round(copper_losses, 2)
            },
            'recommendations': self._get_load_flow_recommendations(voltage_regulation, efficiency)
        }
    
    def calculate_voltage_drop(self, voltage, current, power_factor, distance):
        """
        Calculate voltage drop in conductor
        
        Args:
            voltage: System voltage
            current: Load current in amps
            power_factor: Power factor
            distance: Distance in feet
        
        Returns:
            float: Voltage drop in volts
        """
        # Simplified voltage drop calculation
        # Vd = I * R * L / 1000 (for single phase)
        # where R is resistance per 1000 ft
        
        # Assume typical copper conductor for calculation
        resistance = 0.1  # ohms per 1000 ft (typical for #2 AWG)
        
        # Adjust for power factor (power factor affects reactive component)
        effective_resistance = resistance * (1 + (1 - power_factor))
        
        voltage_drop = (current * effective_resistance * distance) / 1000
        
        return voltage_drop
    
    def calculate_copper_losses(self, current, distance):
        """
        Calculate copper (I²R) losses
        
        Args:
            current: Current in amps
            distance: Distance in feet
        
        Returns:
            float: Power loss in watts
        """
        # I²R losses
        # Assume #2 AWG conductor (R = 0.19 ohms per 1000 ft)
        resistance = 0.19
        actual_resistance = (resistance * distance) / 1000
        copper_losses = (current ** 2) * actual_resistance
        
        return copper_losses
    
    def calculate_fault_current(self, voltage, impedance_percent=5.0, base_mva=10):
        """
        Calculate fault current based on system impedance
        
        Args:
            voltage: System voltage
            impedance_percent: Impedance percentage
            base_mva: Base MVA for calculation
        
        Returns:
            dict: Fault current analysis
        """
        # Fault current calculation
        # If = V / (Z * sqrt(3)) for three-phase
        base_current = (base_mva * 1000) / (math.sqrt(3) * voltage)
        fault_current = base_current / (impedance_percent / 100)
        
        # Calculate symmetrical RMS current
        symmetrical_current = fault_current
        
        # Calculate asymmetrical current (peak)
        asymmetrical_current = fault_current * 1.8  # Peak multiplier
        
        return {
            'system_parameters': {
                'voltage': voltage,
                'impedance_percent': impedance_percent,
                'base_mva': base_mva
            },
            'fault_analysis': {
                'symmetrical_current_amps': round(symmetrical_current, 0),
                'asymmetrical_current_amps': round(asymmetrical_current, 0),
                'base_current_amps': round(base_current, 0)
            },
            'coordination_requirements': {
                'min_breaker_rating': round(symmetrical_current * 1.25, 0),
                'recommended_breaker_rating': round(symmetrical_current * 1.5, 0)
            }
        }
    
    def size_conductor(self, current_amps, voltage, distance, conductor_type='copper_thhn'):
        """
        Size conductor based on ampacity and voltage drop requirements
        
        Args:
            current_amps: Design current in amps
            voltage: System voltage
            distance: Cable distance in feet
            conductor_type: Type of conductor ('copper_thhn', 'aluminum_thhn')
        
        Returns:
            dict: Conductor sizing results
        """
        # Start with ampacity requirement
        required_ampacity = current_amps * 1.25  # 125% of continuous load
        
        # Find suitable conductor size
        ampacity_table = self.AMPACITY_TABLE.get(conductor_type, self.AMPACITY_TABLE['copper_thhn'])
        
        suitable_sizes = []
        for size, ampacity in ampacity_table.items():
            if ampacity >= required_ampacity:
                suitable_sizes.append({
                    'size': size,
                    'ampacity': ampacity,
                    'ampacity_margin': ampacity - required_ampacity
                })
        
        if not suitable_sizes:
            # Use largest available conductor
            max_size = max(ampacity_table.keys())
            suitable_sizes.append({
                'size': max_size,
                'ampacity': ampacity_table[max_size],
                'ampacity_margin': ampacity_table[max_size] - required_ampacity
            })
        
        # Calculate voltage drop for each suitable size
        voltage_drops = []
        for conductor in suitable_sizes:
            # Get resistance for this conductor size
            resistance = self.CABLE_DATA['copper_awg'].get(conductor['size'], {'resistance': 0.2})['resistance']
            
            # Calculate voltage drop
            voltage_drop = (current_amps * resistance * distance) / 1000
            voltage_drop_percent = (voltage_drop / voltage) * 100
            
            voltage_drops.append({
                'size': conductor['size'],
                'voltage_drop_volts': round(voltage_drop, 2),
                'voltage_drop_percent': round(voltage_drop_percent, 2),
                'voltage_drop_pass': voltage_drop_percent <= 3.0  # NEC 3% limit for branch circuits
            })
        
        # Find best conductor size
        best_conductor = None
        for vd in voltage_drops:
            if vd['voltage_drop_pass']:
                best_conductor = vd
                break
        
        if not best_conductor:
            # If no conductor meets voltage drop requirement, use largest
            best_conductor = voltage_drops[-1]
        
        return {
            'requirements': {
                'design_current_amps': current_amps,
                'required_ampacity_amps': round(required_ampacity, 1),
                'distance_feet': distance,
                'voltage': voltage,
                'conductor_type': conductor_type
            },
            'sized_conductor': best_conductor,
            'alternative_options': voltage_drops[:3],  # Top 3 options
            'nec_compliance': {
                'ampacity_compliance': best_conductor['size'] in [s['size'] for s in suitable_sizes[:3]],
                'voltage_drop_compliance': best_conductor['voltage_drop_pass']
            }
        }
    
    def transformer_sizing(self, load_kva, voltage_primary, voltage_secondary, efficiency=0.95):
        """
        Calculate transformer sizing requirements
        
        Args:
            load_kva: Connected load in kVA
            voltage_primary: Primary voltage
            voltage_secondary: Secondary voltage
            efficiency: Transformer efficiency
        
        Returns:
            dict: Transformer sizing results
        """
        # Account for transformer efficiency
        transformer_rating = load_kva / efficiency
        
        # Round up to standard transformer sizes
        standard_sizes = [15, 25, 37.5, 50, 75, 100, 150, 200, 250, 300, 500, 750, 1000]
        
        recommended_size = min(size for size in standard_sizes if size >= transformer_rating)
        
        # Calculate full load currents
        primary_current = (recommended_size * 1000) / (math.sqrt(3) * voltage_primary)
        secondary_current = (recommended_size * 1000) / (math.sqrt(3) * voltage_secondary)
        
        return {
            'load_requirements': {
                'connected_load_kva': load_kva,
                'efficiency': efficiency,
                'required_transformer_kva': round(transformer_rating, 1)
            },
            'transformer_specification': {
                'recommended_rating_kva': recommended_size,
                'primary_voltage': voltage_primary,
                'secondary_voltage': voltage_secondary,
                'primary_current_amps': round(primary_current, 1),
                'secondary_current_amps': round(secondary_current, 1)
            },
            'utilization': {
                'kva_utilization_percent': round((load_kva / recommended_size) * 100, 1),
                'capacity_margin_percent': round(((recommended_size - transformer_rating) / recommended_size) * 100, 1)
            }
        }
    
    def _get_load_flow_recommendations(self, voltage_regulation, efficiency):
        """Generate recommendations based on load flow results"""
        recommendations = []
        
        if voltage_regulation > 5.0:
            recommendations.append({
                'type': 'voltage_regulation',
                'severity': 'high' if voltage_regulation > 8.0 else 'medium',
                'message': f'Voltage regulation of {voltage_regulation}% exceeds recommended 5% limit',
                'action': 'Consider larger conductor size or shorter distance'
            })
        
        if efficiency < 90:
            recommendations.append({
                'type': 'efficiency',
                'severity': 'medium',
                'message': f'System efficiency of {efficiency}% is below optimal',
                'action': 'Consider conductor upgrade or power factor correction'
            })
        
        return recommendations