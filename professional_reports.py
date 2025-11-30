"""
Professional Electrical Engineering Report Generator
Generates comprehensive PDF reports for all electrical sizing calculations

Author: MiniMax Agent
Date: 2025-11-29
Version: 2.0
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus import Image as ReportLabImage
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from datetime import datetime
import json
from typing import Dict, List, Any, Optional
import os

class ElectricalEngineeringReportGenerator:
    """Generate professional electrical engineering reports"""
    
    def __init__(self, output_dir: str = "/workspace/reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Create styles
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for professional reports"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        # Heading style
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        
        # Subheading style
        self.subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceAfter=8,
            textColor=colors.darkgreen
        )
        
        # Body style
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_LEFT
        )
        
        # Code style
        self.code_style = ParagraphStyle(
            'CustomCode',
            parent=self.styles['Code'],
            fontSize=9,
            spaceAfter=6,
            backColor=colors.lightgrey,
            borderColor=colors.grey,
            borderWidth=1,
            borderPadding=5
        )
    
    def generate_cable_sizing_report(self, calculation_result: Dict, recommendations: Dict, project_info: Dict) -> str:
        """Generate comprehensive cable sizing report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cable_sizing_report_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        story = []
        
        # Title Page
        story.append(Paragraph("ELECTRICAL CABLE SIZING REPORT", self.title_style))
        story.append(Spacer(1, 20))
        
        # Project Information
        story.append(Paragraph("PROJECT INFORMATION", self.heading_style))
        project_table_data = [
            ['Project Name:', project_info.get('project_name', 'N/A')],
            ['Engineer:', project_info.get('engineer', 'N/A')],
            ['Date:', datetime.now().strftime('%Y-%m-%d %H:%M')],
            ['Report ID:', f"CBL-{timestamp}"],
            ['NEC Version:', '2023']
        ]
        
        project_table = Table(project_table_data, colWidths=[2*inch, 3*inch])
        project_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(project_table)
        story.append(Spacer(1, 30))
        
        # Calculation Summary
        story.append(Paragraph("CALCULATION SUMMARY", self.heading_style))
        
        calc_data = [
            ['Parameter', 'Value', 'Unit'],
            ['Load Current', f"{calculation_result.get('calculations', {}).get('load_current', 'N/A')}", 'Amps'],
            ['Voltage', f"{calculation_result.get('calculations', {}).get('voltage', 'N/A')}", 'Volts'],
            ['Distance', f"{calculation_result.get('calculations', {}).get('distance', 'N/A')}", 'Feet'],
            ['Ambient Temperature', f"{calculation_result.get('calculations', {}).get('ambient_temperature', 'N/A')}", '°C'],
            ['Installation Type', calculation_result.get('calculations', {}).get('installation_type', 'N/A'), ''],
            ['Recommended Cable Size', calculation_result.get('recommended_size', 'N/A'), ''],
            ['Voltage Drop', f"{calculation_result.get('calculations', {}).get('voltage_drop', {}).get('percent', 'N/A')}", '%'],
            ['NEC Compliance', 'YES' if calculation_result.get('nec_compliance') else 'NO', '']
        ]
        
        calc_table = Table(calc_data, colWidths=[2.5*inch, 1.5*inch, 1*inch])
        calc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey),
        ]))
        story.append(calc_table)
        story.append(Spacer(1, 30))
        
        # Detailed Calculations
        story.append(Paragraph("DETAILED CALCULATIONS", self.heading_style))
        story.append(Paragraph(f"<b>NEC Reference:</b> {calculation_result.get('nec_reference', 'N/A')}", self.body_style))
        story.append(Spacer(1, 12))
        
        # Cable ampacity calculations
        if 'calculations' in calculation_result:
            calc_details = calculation_result['calculations']
            
            story.append(Paragraph("Cable Ampacity Analysis", self.subheading_style))
            ampacity_data = [
                ['Base Ampacity', f"{calc_details.get('base_ampacity', 'N/A')} A"],
                ['Temperature Derating Factor', f"{calc_details.get('temperature_derating_factor', 'N/A')}"],
                ['Installation Derating Factor', f"{calc_details.get('installation_derating_factor', 'N/A')}"],
                ['Adjusted Ampacity', f"{calc_details.get('adjusted_ampacity', 'N/A')} A"],
                ['Required Ampacity', f"{calc_details.get('required_ampacity', 'N/A')} A"]
            ]
            
            ampacity_table = Table(ampacity_data, colWidths=[3*inch, 2*inch])
            ampacity_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            story.append(ampacity_table)
            story.append(Spacer(1, 20))
            
            # Voltage drop analysis
            if 'voltage_drop' in calc_details:
                story.append(Paragraph("Voltage Drop Analysis", self.subheading_style))
                vd_data = [
                    ['Voltage Drop', f"{calc_details['voltage_drop'].get('percent', 'N/A')} %"],
                    ['Maximum Allowable', '5.0 %'],
                    ['Result', 'PASS' if calc_details['voltage_drop'].get('percent', 100) <= 5.0 else 'FAIL']
                ]
                
                vd_table = Table(vd_data, colWidths=[3*inch, 2*inch, 1*inch])
                vd_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightgreen),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                story.append(vd_table)
        
        story.append(PageBreak())
        
        # Recommended Cable Products
        story.append(Paragraph("RECOMMENDED CABLE PRODUCTS", self.heading_style))
        
        # Cable manufacturer recommendations
        for manufacturer, cables in recommendations.items():
            if cables:
                story.append(Paragraph(f"{manufacturer.upper()} Cables", self.subheading_style))
                
                cable_data = [['Part Number', 'Description', 'Price', 'Availability']]
                for cable in cables[:3]:  # Top 3 recommendations
                    cable_data.append([
                        cable.get('part_number', 'N/A'),
                        cable.get('description', 'N/A')[:40] + '...',
                        f"${cable.get('price_estimate', 0):.2f}",
                        cable.get('availability', 'N/A')
                    ])
                
                cable_table = Table(cable_data, colWidths=[1.5*inch, 2.5*inch, 1*inch, 1*inch])
                cable_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                story.append(cable_table)
                story.append(Spacer(1, 15))
        
        # Installation Notes
        story.append(Paragraph("INSTALLATION NOTES", self.heading_style))
        installation_notes = [
            "• Verify local electrical codes and amendments to NEC 2023",
            "• Maintain proper conduit fill ratios per NEC Chapter 9",
            "• Ensure proper grounding and bonding per NEC Article 250",
            "• Use appropriate cable glands for cable entry/exit",
            "• Allow for proper cable pulling tension during installation",
            "• Document all calculations and as-built modifications"
        ]
        
        for note in installation_notes:
            story.append(Paragraph(note, self.body_style))
        
        story.append(Spacer(1, 20))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        story.append(Paragraph(f"Generated by Enhanced Electrical Engineering System v2.0 on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", footer_style))
        story.append(Paragraph("This report is for engineering reference only. Professional engineer review required for final design.", footer_style))
        
        # Build PDF
        doc.build(story)
        return filepath
    
    def generate_motor_sizing_report(self, calculation_result: Dict, recommendations: Dict, project_info: Dict) -> str:
        """Generate comprehensive motor sizing report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"motor_sizing_report_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        story = []
        
        # Title Page
        story.append(Paragraph("ELECTRICAL MOTOR SIZING REPORT", self.title_style))
        story.append(Spacer(1, 20))
        
        # Project Information
        story.append(Paragraph("PROJECT INFORMATION", self.heading_style))
        project_table_data = [
            ['Project Name:', project_info.get('project_name', 'N/A')],
            ['Engineer:', project_info.get('engineer', 'N/A')],
            ['Date:', datetime.now().strftime('%Y-%m-%d %H:%M')],
            ['Report ID:', f"MOT-{timestamp}"],
            ['Application:', calculation_result.get('calculations', {}).get('application', 'N/A')]
        ]
        
        project_table = Table(project_table_data, colWidths=[2*inch, 3*inch])
        project_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(project_table)
        story.append(Spacer(1, 30))
        
        # Motor Specification Summary
        story.append(Paragraph("MOTOR SPECIFICATION SUMMARY", self.heading_style))
        
        calc_data = [
            ['Parameter', 'Value', 'Unit'],
            ['Required Power', f"{calculation_result.get('calculations', {}).get('load_hp', 'N/A')}", 'HP'],
            ['Voltage', calculation_result.get('calculations', {}).get('voltage', 'N/A'), 'Volts'],
            ['Efficiency Class', calculation_result.get('calculations', {}).get('efficiency_class', 'N/A'), ''],
            ['Full Load Current (FLA)', f"{calculation_result.get('calculations', {}).get('full_load_current', 'N/A')}", 'Amps'],
            ['Locked Rotor Current (LRC)', f"{calculation_result.get('calculations', {}).get('locked_rotor_current', 'N/A')}", 'Amps'],
            ['Service Factor', f"{calculation_result.get('calculations', {}).get('service_factor', 'N/A')}", ''],
            ['NEMA Frame', calculation_result.get('calculations', {}).get('nema_frame', 'N/A'), ''],
            ['Annual Operating Cost', f"${calculation_result.get('calculations', {}).get('annual_operating_cost', 0):.2f}", 'USD']
        ]
        
        calc_table = Table(calc_data, colWidths=[2.5*inch, 1.5*inch, 1*inch])
        calc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey),
        ]))
        story.append(calc_table)
        story.append(Spacer(1, 30))
        
        # Energy Analysis
        if 'calculations' in calculation_result:
            calc_details = calculation_result['calculations']
            story.append(Paragraph("ENERGY CONSUMPTION ANALYSIS", self.heading_style))
            
            energy_data = [
                ['Parameter', 'Value', 'Unit'],
                ['Efficiency', f"{calc_details.get('efficiency_percent', 'N/A')}", '%'],
                ['Power Factor', f"{calc_details.get('power_factor', 'N/A')}", ''],
                ['Annual Energy Consumption', f"{calc_details.get('annual_energy_consumption', 0):,.0f}" if isinstance(calc_details.get('annual_energy_consumption', 0), (int, float)) else str(calc_details.get('annual_energy_consumption', 'N/A')), 'kWh'],
                ['Operating Hours/Year', f"{calc_details.get('operating_hours_per_year', 0):,.0f}" if isinstance(calc_details.get('operating_hours_per_year', 0), (int, float)) else str(calc_details.get('operating_hours_per_year', 'N/A')), 'Hours'],
                ['Energy Cost/kWh', '$0.12', 'USD'],
                ['Total Annual Cost', f"${calc_details.get('annual_operating_cost', 0):.2f}", 'USD']
            ]
            
            energy_table = Table(energy_data, colWidths=[2.5*inch, 1.5*inch, 1*inch])
            energy_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 1), (0, -1), colors.lightgreen),
            ]))
            story.append(energy_table)
            story.append(Spacer(1, 20))
        
        story.append(PageBreak())
        
        # Recommended Motors
        story.append(Paragraph("RECOMMENDED MOTOR PRODUCTS", self.heading_style))
        
        for manufacturer, motors in recommendations.items():
            if motors:
                story.append(Paragraph(f"{manufacturer.upper()} Motors", self.subheading_style))
                
                motor_data = [['Part Number', 'Model', 'Price', 'Efficiency', 'Availability']]
                for motor in motors[:3]:
                    motor_data.append([
                        motor.get('part_number', 'N/A'),
                        motor.get('product_line', 'N/A')[:25] + '...' if len(motor.get('product_line', '')) > 25 else motor.get('product_line', 'N/A'),
                        f"${motor.get('price_estimate', 0):.2f}",
                        f"{motor.get('specifications', {}).get('efficiency_percent', 'N/A')}%",
                        motor.get('availability', 'N/A')
                    ])
                
                motor_table = Table(motor_data, colWidths=[1.5*inch, 2*inch, 1*inch, 1*inch, 1.5*inch])
                motor_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                story.append(motor_table)
                story.append(Spacer(1, 15))
        
        # Installation Requirements
        story.append(Paragraph("INSTALLATION REQUIREMENTS", self.heading_style))
        installation_reqs = [
            "• Ensure proper motor mounting per manufacturer specifications",
            "• Provide adequate ventilation for cooling (minimum 3 feet clearance)",
            "• Install proper motor protection devices (overload relays, circuit breakers)",
            "• Verify power supply voltage and phase matches motor requirements",
            "• Implement proper grounding per NEC Article 250",
            "• Consider harmonic mitigation for VFD applications",
            "• Plan for maintenance access and shaft alignment"
        ]
        
        for req in installation_reqs:
            story.append(Paragraph(req, self.body_style))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        story.append(Spacer(1, 20))
        story.append(Paragraph(f"Generated by Enhanced Electrical Engineering System v2.0 on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", footer_style))
        story.append(Paragraph("This report is for engineering reference only. Professional engineer review required for final design.", footer_style))
        
        # Build PDF
        doc.build(story)
        return filepath
    
    def generate_circuit_breaker_report(self, calculation_result: Dict, recommendations: Dict, project_info: Dict) -> str:
        """Generate comprehensive circuit breaker sizing report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"breaker_sizing_report_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        story = []
        
        # Title Page
        story.append(Paragraph("CIRCUIT BREAKER SIZING REPORT", self.title_style))
        story.append(Spacer(1, 20))
        
        # Project Information
        story.append(Paragraph("PROJECT INFORMATION", self.heading_style))
        project_table_data = [
            ['Project Name:', project_info.get('project_name', 'N/A')],
            ['Engineer:', project_info.get('engineer', 'N/A')],
            ['Date:', datetime.now().strftime('%Y-%m-%d %H:%M')],
            ['Report ID:', f'CBR-{timestamp}'],
            ['Application:', calculation_result.get('calculations', {}).get('application', 'N/A')]
        ]
        
        project_table = Table(project_table_data, colWidths=[2*inch, 3*inch])
        project_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(project_table)
        story.append(Spacer(1, 30))
        
        # Circuit Protection Summary
        story.append(Paragraph("CIRCUIT PROTECTION SUMMARY", self.heading_style))
        
        calc_data = [
            ['Parameter', 'Value', 'Unit'],
            ['Continuous Load', f"{calculation_result.get('calculations', {}).get('continuous_load', 'N/A')}", 'Amps'],
            ['Recommended Breaker Size', f"{calculation_result.get('recommended_size', 'N/A')}", 'Amps'],
            ['Voltage', calculation_result.get('calculations', {}).get('voltage', 'N/A'), 'Volts'],
            ['Safety Factor', f"{calculation_result.get('calculations', {}).get('safety_factor', 'N/A')}", ''],
            ['Interrupting Capacity', calculation_result.get('calculations', {}).get('interrupting_capacity', 'N/A'), 'kA'],
            ['Ambient Temperature', f"{calculation_result.get('calculations', {}).get('ambient_temperature', 'N/A')}", '°C'],
            ['NEC Compliance', 'YES' if calculation_result.get('nec_compliance') else 'NO', '']
        ]
        
        calc_table = Table(calc_data, colWidths=[2.5*inch, 1.5*inch, 1*inch])
        calc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey),
        ]))
        story.append(calc_table)
        story.append(Spacer(1, 30))
        
        # Protection Analysis
        if 'calculations' in calculation_result:
            calc_details = calculation_result['calculations']
            story.append(Paragraph("PROTECTION ANALYSIS", self.heading_style))
            
            protection_data = [
                ['Parameter', 'Value', 'Standard'],
                ['Calculation Method', calc_details.get('calculation_method', 'N/A'), 'NEC 210.20, 430.52'],
                ['Continuous Load Factor', '125%', 'NEC 210.20(A)'],
                ['Total Load Current', f"{calc_details.get('total_load', 'N/A')}", 'Amps'],
                ['Required Wire Ampacity', f"{calc_details.get('wire_ampacity_required', 'N/A')}", 'Amps'],
                ['Short Circuit Capacity', calc_details.get('short_circuit_capacity', 'N/A'), 'Per utility'],
                ['Protection Rating', f"{calc_details.get('interrupting_capacity', 'N/A')}", 'kA']
            ]
            
            protection_table = Table(protection_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
            protection_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 1), (0, -1), colors.lightgreen),
            ]))
            story.append(protection_table)
            story.append(Spacer(1, 20))
        
        story.append(PageBreak())
        
        # Recommended Circuit Breakers
        story.append(Paragraph("RECOMMENDED CIRCUIT BREAKERS", self.heading_style))
        
        for manufacturer, breakers in recommendations.items():
            if breakers:
                story.append(Paragraph(f"{manufacturer.upper()} Circuit Breakers", self.subheading_style))
                
                breaker_data = [['Part Number', 'Product Line', 'Price', 'Interrupting Capacity', 'Availability']]
                for breaker in breakers[:3]:
                    breaker_data.append([
                        breaker.get('part_number', 'N/A'),
                        breaker.get('product_line', 'N/A')[:20] + '...' if len(breaker.get('product_line', '')) > 20 else breaker.get('product_line', 'N/A'),
                        f"${breaker.get('price_estimate', 0):.2f}",
                        breaker.get('specifications', {}).get('interruption_capacity', 'N/A'),
                        breaker.get('availability', 'N/A')
                    ])
                
                breaker_table = Table(breaker_data, colWidths=[1.5*inch, 2*inch, 1*inch, 1.5*inch, 1*inch])
                breaker_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                story.append(breaker_table)
                story.append(Spacer(1, 15))
        
        # Safety Considerations
        story.append(Paragraph("SAFETY CONSIDERATIONS", self.heading_style))
        safety_items = [
            "• Verify available fault current does not exceed breaker interrupting capacity",
            "• Ensure proper coordination with upstream and downstream protective devices",
            "• Consider ambient temperature effects on breaker ratings per manufacturer data",
            "• Install in appropriate enclosure rated for environmental conditions",
            "• Verify proper grounding and bonding of enclosure",
            "• Consider arc flash boundary calculations for personal protective equipment",
            "• Document all calculations and provide stamped engineering drawings"
        ]
        
        for item in safety_items:
            story.append(Paragraph(item, self.body_style))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        story.append(Spacer(1, 20))
        story.append(Paragraph(f"Generated by Enhanced Electrical Engineering System v2.0 on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", footer_style))
        story.append(Paragraph("This report is for engineering reference only. Professional engineer review required for final design.", footer_style))
        
        # Build PDF
        doc.build(story)
        return filepath

def test_report_generation():
    """Test the report generation system"""
    print("Testing Professional Report Generation")
    print("=" * 40)
    
    # Test data
    test_calculation = {
        'recommended_size': '6 AWG',
        'nec_compliance': True,
        'nec_reference': 'NEC 310.60, NEC 210.19',
        'calculations': {
            'load_current': 30,
            'voltage': 208,
            'distance': 150,
            'ambient_temperature': 40,
            'base_ampacity': 55,
            'temperature_derating_factor': 0.94,
            'installation_derating_factor': 0.8,
            'adjusted_ampacity': 41.4,
            'required_ampacity': 37.5,
            'voltage_drop': {'percent': 2.13}
        }
    }
    
    test_project_info = {
        'project_name': 'Industrial Motor Control Panel',
        'engineer': 'John Smith, PE'
    }
    
    test_recommendations = {
        'siemens': [{'part_number': '1FK7022-5AK71-1QG0', 'description': '10HP Motor', 'price_estimate': 2850.00, 'availability': 'In Stock'}],
        'abb': [{'part_number': 'M3BP 132SMA 4', 'description': '10HP Motor', 'price_estimate': 2650.00, 'availability': 'In Stock'}]
    }
    
    # Generate reports
    generator = ElectricalEngineeringReportGenerator()
    
    print("📄 Generating Cable Sizing Report...")
    cable_report = generator.generate_cable_sizing_report(test_calculation, test_recommendations, test_project_info)
    print(f"✅ Cable report generated: {cable_report}")
    
    print("📄 Generating Motor Sizing Report...")
    motor_report = generator.generate_motor_sizing_report(test_calculation, test_recommendations, test_project_info)
    print(f"✅ Motor report generated: {motor_report}")
    
    print("📄 Generating Circuit Breaker Report...")
    breaker_report = generator.generate_circuit_breaker_report(test_calculation, test_recommendations, test_project_info)
    print(f"✅ Breaker report generated: {breaker_report}")
    
    print("\n🎉 All professional reports generated successfully!")

if __name__ == "__main__":
    test_report_generation()
