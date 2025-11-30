import json
import random
import requests
from datetime import datetime, timedelta

class MaterialPricingEngine:
    """Real-time material pricing and supplier integration engine"""
    
    def __init__(self):
        self.supplier_apis = self._initialize_supplier_apis()
        self.material_catalog = self._initialize_material_catalog()
        self.price_cache = {}
        self.last_price_update = {}
    
    def _initialize_supplier_apis(self):
        """Initialize supplier API configurations"""
        return {
            'graybar': {
                'base_url': 'https://api.graybar.com/v1',
                'api_key': 'demo_key',
                'products_endpoint': '/products/search',
                'availability_endpoint': '/inventory'
            },
            'wesco': {
                'base_url': 'https://api.wesco.com/v1',
                'api_key': 'demo_key',
                'products_endpoint': '/catalog/search',
                'pricing_endpoint': '/pricing/quote'
            },
            'schneider': {
                'base_url': 'https://api.se.com/v1',
                'api_key': 'demo_key',
                'products_endpoint': '/electrical/products',
                'pricing_endpoint': '/electrical/pricing'
            }
        }
    
    def _initialize_material_catalog(self):
        """Initialize electrical material specifications and typical items"""
        return {
            'cables': {
                'copper_thhn_12awg': {
                    'description': '12 AWG Copper THHN Building Wire',
                    'unit': 'ft',
                    'weight_per_unit': 0.089,  # lbs per foot
                    'typical_applications': 'General purpose branch circuits',
                    'nec_ampacity': 30
                },
                'copper_thhn_10awg': {
                    'description': '10 AWG Copper THHN Building Wire',
                    'unit': 'ft',
                    'weight_per_unit': 0.131,
                    'typical_applications': '30A branch circuits',
                    'nec_ampacity': 40
                },
                'copper_thhn_8awg': {
                    'description': '8 AWG Copper THHN Building Wire',
                    'unit': 'ft',
                    'weight_per_unit': 0.208,
                    'typical_applications': '40A branch circuits',
                    'nec_ampacity': 55
                },
                'copper_thhn_6awg': {
                    'description': '6 AWG Copper THHN Building Wire',
                    'unit': 'ft',
                    'weight_per_unit': 0.331,
                    'typical_applications': '65A branch circuits',
                    'nec_ampacity': 80
                }
            },
            'breakers': {
                'breaker_20a_1p': {
                    'description': '20A Single Pole Circuit Breaker',
                    'unit': 'each',
                    'manufacturer': 'Square D',
                    'voltage_rating': '120/240V',
                    'interrupt_capacity': '10kA'
                },
                'breaker_30a_1p': {
                    'description': '30A Single Pole Circuit Breaker',
                    'unit': 'each',
                    'manufacturer': 'Square D',
                    'voltage_rating': '120/240V',
                    'interrupt_capacity': '10kA'
                },
                'breaker_60a_3p': {
                    'description': '60A Three Phase Circuit Breaker',
                    'unit': 'each',
                    'manufacturer': 'Square D',
                    'voltage_rating': '480V',
                    'interrupt_capacity': '65kA'
                }
            },
            'transformers': {
                'transformer_25kva_480v_208v': {
                    'description': '25kVA Transformer 480V to 208V/120V',
                    'unit': 'each',
                    'manufacturer': 'Hammond',
                    'primary_voltage': '480V',
                    'secondary_voltage': '208Y/120V',
                    'efficiency': '0.95'
                },
                'transformer_50kva_480v_208v': {
                    'description': '50kVA Transformer 480V to 208V/120V',
                    'unit': 'each',
                    'manufacturer': 'Hammond',
                    'primary_voltage': '480V',
                    'secondary_voltage': '208Y/120V',
                    'efficiency': '0.96'
                }
            },
            'conduit': {
                'emt_1/2in': {
                    'description': '1/2" Electrical Metallic Tubing (EMT)',
                    'unit': 'ft',
                    'material': 'Steel',
                    'wall_thickness': '0.042"',
                    'weight_per_unit': 0.303  # lbs per foot
                },
                'emt_3/4in': {
                    'description': '3/4" Electrical Metallic Tubing (EMT)',
                    'unit': 'ft',
                    'material': 'Steel',
                    'wall_thickness': '0.049"',
                    'weight_per_unit': 0.445
                },
                'rigid_1in': {
                    'description': '1" Rigid Metal Conduit',
                    'unit': 'ft',
                    'material': 'Galvanized Steel',
                    'weight_per_unit': 1.04
                }
            },
            'panels': {
                'panel_200a_42circuits': {
                    'description': '200A Main Lug Panel 42 Circuits',
                    'unit': 'each',
                    'manufacturer': 'Square D',
                    'mains': '200A',
                    'circuits': 42,
                    'voltage': '120/240V'
                },
                'panel_400a_42circuits': {
                    'description': '400A Main Breaker Panel 42 Circuits',
                    'unit': 'each',
                    'manufacturer': 'Square D',
                    'mains': '400A',
                    'circuits': 42,
                    'voltage': '120/240V'
                }
            }
        }
    
    def get_price_estimate(self, material_type, quantity, specifications=None):
        """
        Get real-time price estimate for materials
        
        Args:
            material_type: Type of material (e.g., 'copper_thhn_12awg')
            quantity: Required quantity
            specifications: Additional specifications dict
        
        Returns:
            dict: Price estimate with supplier information
        """
        # Check cache first
        cache_key = f"{material_type}_{quantity}"
        if cache_key in self.price_cache:
            cache_time = self.last_price_update.get(cache_key)
            if cache_time and (datetime.now() - cache_time).seconds < 3600:  # 1 hour cache
                return self.price_cache[cache_key]
        
        # Get base material info
        material_info = self._get_material_info(material_type)
        if not material_info:
            return None
        
        # Get pricing from multiple suppliers
        supplier_prices = self._get_supplier_prices(material_type, quantity, specifications)
        
        # Calculate weighted average with supplier reliability
        best_price = min(supplier_prices, key=lambda x: x['unit_cost'])
        
        # Apply market volatility and regional factors
        adjusted_price = self._apply_market_adjustments(best_price, material_type)
        
        estimate = {
            'material_name': material_type,
            'description': material_info.get('description', ''),
            'category': self._get_material_category(material_type),
            'quantity': quantity,
            'unit': material_info.get('unit', 'each'),
            'unit_cost': adjusted_price['unit_cost'],
            'total_cost': adjusted_price['unit_cost'] * quantity,
            'supplier': adjusted_price['supplier'],
            'lead_time_days': adjusted_price['lead_time'],
            'availability': adjusted_price['availability'],
            'specifications': specifications or {},
            'unit_weight_lbs': material_info.get('weight_per_unit', 0),
            'total_weight_lbs': material_info.get('weight_per_unit', 0) * quantity,
            'market_data': {
                'price_trend': adjusted_price['trend'],
                'volatility': adjusted_price['volatility'],
                'last_updated': datetime.now().isoformat()
            },
            'alternative_options': supplier_prices[:3]  # Top 3 supplier options
        }
        
        # Cache the result
        self.price_cache[cache_key] = estimate
        self.last_price_update[cache_key] = datetime.now()
        
        return estimate
    
    def _get_supplier_prices(self, material_type, quantity, specifications):
        """Get pricing from multiple suppliers (simulated API calls)"""
        prices = []
        
        # Simulate API calls to different suppliers
        suppliers = ['graybar', 'wesco', 'schneider']
        
        for supplier in suppliers:
            try:
                # Simulate supplier pricing
                base_price = self._get_base_supplier_price(material_type, supplier)
                unit_cost = base_price * self._get_supplier_markup(supplier)
                
                # Apply quantity discounts
                if quantity > 1000:
                    unit_cost *= 0.95
                elif quantity > 500:
                    unit_cost *= 0.97
                
                prices.append({
                    'supplier': supplier.title(),
                    'unit_cost': round(unit_cost, 2),
                    'availability': 'In Stock' if random.random() > 0.2 else 'Backorder',
                    'lead_time': random.randint(1, 14),
                    'reliability_score': random.uniform(0.8, 0.98)
                })
                
            except Exception as e:
                print(f"Error getting price from {supplier}: {e}")
                continue
        
        return prices
    
    def _get_base_supplier_price(self, material_type, supplier):
        """Get base supplier price for material"""
        # Simulated base prices (in reality, would come from supplier APIs)
        base_prices = {
            'graybar': {
                'copper_thhn_12awg': 0.85,
                'copper_thhn_10awg': 1.35,
                'breaker_20a_1p': 45.00,
                'transformer_25kva_480v_208v': 1850.00,
                'emt_1/2in': 1.25
            },
            'wesco': {
                'copper_thhn_12awg': 0.82,
                'copper_thhn_10awg': 1.32,
                'breaker_20a_1p': 43.50,
                'transformer_25kva_480v_208v': 1825.00,
                'emt_1/2in': 1.28
            },
            'schneider': {
                'copper_thhn_12awg': 0.88,
                'copper_thhn_10awg': 1.38,
                'breaker_20a_1p': 46.50,
                'transformer_25kva_480v_208v': 1875.00,
                'emt_1/2in': 1.30
            }
        }
        
        return base_prices.get(supplier, {}).get(material_type, 1.00)
    
    def _get_supplier_markup(self, supplier):
        """Get supplier markup percentage"""
        markups = {
            'graybar': random.uniform(1.05, 1.12),
            'wesco': random.uniform(1.04, 1.10),
            'schneider': random.uniform(1.06, 1.15)
        }
        return markups.get(supplier, 1.10)
    
    def _apply_market_adjustments(self, supplier_price, material_type):
        """Apply market volatility and regional adjustments"""
        # Simulate market volatility based on material type
        volatility_factors = {
            'copper': (0.85, 1.25),  # High volatility
            'breaker': (0.95, 1.05),  # Low volatility
            'transformer': (0.90, 1.15),  # Medium volatility
            'emt': (0.85, 1.20)  # Medium-high volatility
        }
        
        material_category = self._get_material_category(material_type)
        volatility_range = volatility_factors.get(material_category, (0.95, 1.05))
        
        # Apply market trend
        trend_factor = random.uniform(*volatility_range)
        
        adjusted_price = {
            'unit_cost': round(supplier_price['unit_cost'] * trend_factor, 2),
            'supplier': supplier_price['supplier'],
            'lead_time': supplier_price['lead_time'],
            'availability': supplier_price['availability'],
            'trend': 'increasing' if trend_factor > 1.05 else 'decreasing' if trend_factor < 0.95 else 'stable',
            'volatility': round((volatility_range[1] - volatility_range[0]) / 2, 3)
        }
        
        return adjusted_price
    
    def _get_material_info(self, material_type):
        """Get material specifications from catalog"""
        for category, materials in self.material_catalog.items():
            if material_type in materials:
                return materials[material_type]
        return None
    
    def _get_material_category(self, material_type):
        """Determine material category from type"""
        for category in self.material_catalog:
            if material_type in self.material_catalog[category]:
                return category
        return 'other'
    
    def get_bulk_material_estimate(self, project_specs):
        """
        Get comprehensive material estimate for entire project
        
        Args:
            project_specs: Dict containing project electrical specifications
        
        Returns:
            dict: Complete material list with pricing
        """
        materials_needed = []
        total_cost = 0
        
        # Parse project specifications
        building_type = project_specs.get('building_type', 'commercial')
        voltage_level = project_specs.get('voltage_level', '480V')
        square_footage = project_specs.get('square_footage', 10000)
        num_circuits = project_specs.get('num_circuits', 100)
        
        # Calculate material quantities based on building specifications
        cable_quantities = self._calculate_cable_quantities(num_circuits, square_footage, building_type)
        for cable_type, cable_length in cable_quantities.items():
            estimate = self.get_price_estimate(cable_type, cable_length)
            if estimate:
                materials_needed.append(estimate)
                total_cost += estimate['total_cost']
        
        # Add breakers
        num_breakers_20a = int(num_circuits * 0.6)
        num_breakers_30a = int(num_circuits * 0.4)
        
        breaker_20a = self.get_price_estimate('breaker_20a_1p', num_breakers_20a)
        breaker_30a = self.get_price_estimate('breaker_30a_1p', num_breakers_30a)
        
        if breaker_20a:
            materials_needed.append(breaker_20a)
            total_cost += breaker_20a['total_cost']
        
        if breaker_30a:
            materials_needed.append(breaker_30a)
            total_cost += breaker_30a['total_cost']
        
        # Add transformer if needed
        if voltage_level in ['13800V', '23000V']:
            transformer_estimate = self.get_price_estimate('transformer_50kva_480v_208v', 1)
            if transformer_estimate:
                materials_needed.append(transformer_estimate)
                total_cost += transformer_estimate['total_cost']
        
        # Add conduit
        conduit_estimate = self.get_price_estimate('emt_1/2in', int(square_footage * 0.8))
        if conduit_estimate:
            materials_needed.append(conduit_estimate)
            total_cost += conduit_estimate['total_cost']
        
        return {
            'materials': materials_needed,
            'total_cost': round(total_cost, 2),
            'summary': {
                'total_items': len(materials_needed),
                'cost_per_sqft': round(total_cost / square_footage, 2) if square_footage > 0 else 0,
                'cost_per_circuit': round(total_cost / num_circuits, 2) if num_circuits > 0 else 0
            },
            'market_summary': self._get_market_summary(materials_needed)
        }
    
    def _calculate_cable_quantities(self, num_circuits, square_footage, building_type):
        """Calculate cable quantities based on project specifications"""
        # Base calculations per circuit type
        cable_quantities = {}
        
        # Circuit conductor requirements
        # Power circuits (20A): typically 12 AWG copper
        power_circuit_length = int(num_circuits * 75)  # 75 ft per circuit average
        cable_quantities['copper_thhn_12awg'] = power_circuit_length
        
        # Heavy circuits (30A): 10 AWG copper
        heavy_circuit_length = int(num_circuits * 0.4 * 100)  # 100 ft per heavy circuit
        cable_quantities['copper_thhn_10awg'] = heavy_circuit_length
        
        # Building type adjustments
        if building_type == 'industrial':
            cable_quantities['copper_thhn_12awg'] = int(cable_quantities['copper_thhn_12awg'] * 1.3)
            cable_quantities['copper_thhn_10awg'] = int(cable_quantities['copper_thhn_10awg'] * 1.3)
        elif building_type == 'residential':
            cable_quantities['copper_thhn_12awg'] = int(cable_quantities['copper_thhn_12awg'] * 0.7)
            cable_quantities['copper_thhn_10awg'] = int(cable_quantities['copper_thhn_10awg'] * 0.7)
        
        return cable_quantities
    
    def _get_market_summary(self, materials):
        """Generate market summary for material list"""
        if not materials:
            return {}
        
        # Aggregate trends by material type
        trends = {}
        total_volatility = 0
        
        for material in materials:
            trend = material.get('market_data', {}).get('price_trend', 'stable')
            volatility = material.get('market_data', {}).get('volatility', 0)
            
            if trend not in trends:
                trends[trend] = 0
            trends[trend] += 1
            total_volatility += volatility
        
        avg_volatility = total_volatility / len(materials) if materials else 0
        
        return {
            'overall_trend': max(trends, key=trends.get),
            'average_volatility': round(avg_volatility, 3),
            'material_count_by_trend': trends,
            'supplier_diversity': len(set(m.get('supplier', 'Unknown') for m in materials)),
            'recommendations': self._get_procurement_recommendations(materials)
        }
    
    def _get_procurement_recommendations(self, materials):
        """Generate procurement recommendations based on market data"""
        recommendations = []
        
        # Price trend analysis
        increasing_items = [m for m in materials if m.get('market_data', {}).get('price_trend') == 'increasing']
        if increasing_items:
            recommendations.append({
                'type': 'timing',
                'priority': 'high',
                'message': f'Consider expediting {len(increasing_items)} items with increasing prices',
                'items': [m['material_name'] for m in increasing_items[:3]]
            })
        
        # Supplier concentration analysis
        supplier_counts = {}
        for material in materials:
            supplier = material.get('supplier', 'Unknown')
            supplier_counts[supplier] = supplier_counts.get(supplier, 0) + 1
        
        max_supplier = max(supplier_counts, key=supplier_counts.get)
        concentration = supplier_counts[max_supplier] / len(materials)
        
        if concentration > 0.6:
            recommendations.append({
                'type': 'supplier_diversity',
                'priority': 'medium',
                'message': f'Consider diversifying from {max_supplier} (currently {concentration:.1%} of purchases)',
                'current_concentration': f'{concentration:.1%}'
            })
        
        # Lead time optimization
        long_lead_items = [m for m in materials if m.get('lead_time_days', 0) > 10]
        if long_lead_items:
            recommendations.append({
                'type': 'lead_time',
                'priority': 'high',
                'message': f'Place orders early for {len(long_lead_items)} long-lead items',
                'items': [m['material_name'] for m in long_lead_items[:3]]
            })
        
        return recommendations
    
    def update_real_time_prices(self):
        """Update prices from all supplier APIs"""
        print("Updating real-time prices from suppliers...")
        
        # In a real implementation, this would make actual API calls
        # For demo purposes, we'll simulate price updates
        updated_count = 0
        
        for cache_key in list(self.price_cache.keys()):
            # Simulate API call delay
            material_type = cache_key.split('_')[0]  # Simplified parsing
            
            # Get new price from suppliers
            new_prices = self._get_supplier_prices(material_type, 100, {})
            if new_prices:
                best_price = min(new_prices, key=lambda x: x['unit_cost'])
                adjusted_price = self._apply_market_adjustments(best_price, material_type)
                
                # Update cached item
                cached_item = self.price_cache[cache_key]
                cached_item['unit_cost'] = adjusted_price['unit_cost']
                cached_item['total_cost'] = cached_item['unit_cost'] * cached_item['quantity']
                cached_item['market_data']['last_updated'] = datetime.now().isoformat()
                cached_item['market_data']['price_trend'] = adjusted_price['trend']
                
                updated_count += 1
        
        print(f"Updated {updated_count} material prices")
        return updated_count