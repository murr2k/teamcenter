#!/usr/bin/env python3
"""
Example: Mining Equipment Automation for Epiroc
Demonstrates common automation tasks for Teamcenter PLM
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.client.rest_client import TeamcenterRESTClient
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EquipmentAutomation:
    """
    Automation examples for mining equipment management
    """
    
    def __init__(self, base_url: str, username: str, password: str):
        """Initialize automation client"""
        self.client = TeamcenterRESTClient(base_url, username, password)
    
    def create_scooptram_loader(self):
        """
        Example: Create a new Scooptram loader with full specifications
        """
        logger.info("Creating new Scooptram ST1030 loader...")
        
        # Equipment data for battery-electric loader
        loader_data = {
            'itemId': f'SCOOPTRAM-{datetime.now().strftime("%Y%m%d%H%M")}',
            'name': 'Scooptram ST1030 Battery-Electric Loader',
            'description': '10-tonne capacity underground loader with battery-electric drive',
            'type': 'EPR_MiningEquipment',
            'properties': {
                'epr_equipment_type': 'Underground Loader',
                'epr_model': 'ST1030',
                'epr_power_type': 'Battery Electric',
                'epr_capacity': '10 tonnes',
                'epr_battery_voltage': '650V DC',
                'epr_battery_capacity': '265 kWh',
                'epr_charging_time': '90 minutes',
                'epr_operating_time': '4-6 hours',
                'epr_tramming_speed': '20 km/h',
                'epr_width': '2495 mm',
                'epr_height': '2440 mm',
                'epr_length': '11215 mm',
                'epr_weight': '32000 kg',
                'epr_safety_features': 'ROPS/FOPS certified cabin, Emergency stop, Battery management system',
                'epr_certifications': 'CE, MSHA, CANMET',
                'epr_facility': 'Pitt Meadows',
                'epr_manufacture_date': datetime.now().strftime('%Y-%m-%d')
            }
        }
        
        # Create the equipment item
        loader = self.client.create_item(loader_data)
        logger.info(f"✓ Created loader: {loader['itemId']}")
        
        return loader
    
    def build_loader_bom(self, loader_id: str):
        """
        Example: Build BOM structure for loader
        """
        logger.info(f"Building BOM for loader {loader_id}...")
        
        # Define major components
        components = [
            {
                'itemId': 'BATTERY-PACK-650V',
                'name': 'Battery Pack System 650V',
                'quantity': 1,
                'critical': True
            },
            {
                'itemId': 'ELECTRIC-MOTOR-200KW',
                'name': 'Electric Drive Motor 200kW',
                'quantity': 2,
                'critical': True
            },
            {
                'itemId': 'HYDRAULIC-SYSTEM-ST1030',
                'name': 'Hydraulic System Assembly',
                'quantity': 1,
                'critical': True
            },
            {
                'itemId': 'CONTROL-SYSTEM-V3',
                'name': 'Epiroc Control System V3',
                'quantity': 1,
                'critical': True
            },
            {
                'itemId': 'BUCKET-10T',
                'name': '10-Tonne Bucket Assembly',
                'quantity': 1,
                'critical': False
            },
            {
                'itemId': 'CABIN-ROPS-FOPS',
                'name': 'ROPS/FOPS Certified Cabin',
                'quantity': 1,
                'critical': True
            },
            {
                'itemId': 'CHARGING-INTERFACE',
                'name': 'Fast Charging Interface',
                'quantity': 1,
                'critical': False
            }
        ]
        
        # Add each component to BOM
        for component in components:
            try:
                # First create the component if it doesn't exist
                comp_data = {
                    'itemId': component['itemId'],
                    'name': component['name'],
                    'type': 'EPR_Component'
                }
                
                try:
                    self.client.create_item(comp_data)
                    logger.info(f"  Created component: {component['itemId']}")
                except:
                    logger.info(f"  Component exists: {component['itemId']}")
                
                # Add to BOM
                bom_line = self.client.add_bom_line(
                    parent_id=loader_id,
                    child_id=component['itemId'],
                    quantity=component['quantity'],
                    properties={
                        'epr_critical_component': str(component['critical']),
                        'epr_position_number': str(components.index(component) + 1)
                    }
                )
                logger.info(f"  ✓ Added {component['name']} to BOM")
                
            except Exception as e:
                logger.error(f"  ✗ Failed to add {component['itemId']}: {e}")
        
        logger.info("BOM structure complete")
    
    def check_equipment_compliance(self, equipment_id: str):
        """
        Example: Check compliance status of equipment
        """
        logger.info(f"Checking compliance for {equipment_id}...")
        
        # Define required compliance documents
        required_docs = [
            'MSHA_Certification',
            'CE_Declaration',
            'Electrical_Safety_Test',
            'Battery_Safety_Report',
            'ROPS_FOPS_Certificate'
        ]
        
        # In real implementation, would query for attached documents
        # For demo, we'll simulate the check
        compliance_status = {
            'equipmentId': equipment_id,
            'compliant': True,
            'missing_documents': [],
            'expired_documents': [],
            'warnings': []
        }
        
        # Simulate checking each required document
        for doc_type in required_docs:
            # In real implementation, would check if document exists and is valid
            logger.info(f"  Checking {doc_type}...")
            
            # Simulate some missing docs for demo
            if doc_type in ['Electrical_Safety_Test', 'Battery_Safety_Report']:
                compliance_status['missing_documents'].append(doc_type)
                compliance_status['compliant'] = False
        
        # Generate compliance report
        if compliance_status['compliant']:
            logger.info("✓ Equipment is COMPLIANT")
        else:
            logger.warning("✗ Equipment is NON-COMPLIANT")
            logger.warning(f"  Missing: {compliance_status['missing_documents']}")
        
        return compliance_status
    
    def start_ecn_workflow(self, equipment_id: str, change_description: str):
        """
        Example: Start an Engineering Change Notice workflow
        """
        logger.info(f"Starting ECN workflow for {equipment_id}...")
        
        workflow_data = {
            'processName': 'EPR_ECN_Process',
            'targets': [equipment_id],
            'properties': {
                'change_description': change_description,
                'change_reason': 'Battery system upgrade',
                'impact_level': 'Medium',
                'safety_impact': 'Yes',
                'testing_required': 'Yes',
                'estimated_hours': '40',
                'implementation_date': '2025-02-01',
                'requester': 'Engineering Team',
                'priority': 'Normal'
            }
        }
        
        try:
            workflow = self.client.start_workflow(
                process_name=workflow_data['processName'],
                targets=workflow_data['targets'],
                properties=workflow_data['properties']
            )
            
            logger.info(f"✓ Started ECN workflow: {workflow.get('workflowId')}")
            logger.info(f"  Description: {change_description}")
            logger.info(f"  Priority: {workflow_data['properties']['priority']}")
            
            return workflow
            
        except Exception as e:
            logger.error(f"✗ Failed to start workflow: {e}")
            return None
    
    def generate_equipment_report(self, equipment_id: str):
        """
        Example: Generate comprehensive equipment report
        """
        logger.info(f"Generating report for {equipment_id}...")
        
        try:
            # Get equipment details
            equipment = self.client.get_item(equipment_id)
            
            # Get BOM structure
            bom = self.client.get_bom_structure(equipment_id, levels=2)
            
            # Get where-used information
            where_used = self.client.get_where_used(equipment_id)
            
            # Generate report
            report = {
                'timestamp': datetime.now().isoformat(),
                'equipment': {
                    'id': equipment_id,
                    'name': equipment.get('name'),
                    'type': equipment.get('properties', {}).get('epr_equipment_type'),
                    'model': equipment.get('properties', {}).get('epr_model'),
                    'power_type': equipment.get('properties', {}).get('epr_power_type'),
                    'facility': equipment.get('properties', {}).get('epr_facility')
                },
                'bom_summary': {
                    'total_components': len(bom.get('lines', [])),
                    'critical_components': sum(1 for line in bom.get('lines', []) 
                                              if line.get('properties', {}).get('epr_critical_component') == 'True')
                },
                'usage': {
                    'used_in_count': len(where_used),
                    'parent_assemblies': [parent.get('itemId') for parent in where_used]
                }
            }
            
            logger.info("✓ Report generated successfully")
            logger.info(f"  Equipment: {report['equipment']['name']}")
            logger.info(f"  Components: {report['bom_summary']['total_components']}")
            logger.info(f"  Used in: {report['usage']['used_in_count']} assemblies")
            
            return report
            
        except Exception as e:
            logger.error(f"✗ Failed to generate report: {e}")
            return None
    
    def run_full_demo(self):
        """
        Run complete demonstration of equipment automation
        """
        logger.info("=" * 60)
        logger.info("TEAMCENTER EQUIPMENT AUTOMATION DEMONSTRATION")
        logger.info("Epiroc - Pitt Meadows Facility")
        logger.info("=" * 60)
        
        try:
            # Step 1: Create new equipment
            logger.info("\n1. CREATING NEW EQUIPMENT")
            logger.info("-" * 40)
            loader = self.create_scooptram_loader()
            loader_id = loader['itemId']
            
            # Step 2: Build BOM structure
            logger.info("\n2. BUILDING BOM STRUCTURE")
            logger.info("-" * 40)
            self.build_loader_bom(loader_id)
            
            # Step 3: Check compliance
            logger.info("\n3. CHECKING COMPLIANCE")
            logger.info("-" * 40)
            compliance = self.check_equipment_compliance(loader_id)
            
            # Step 4: Start ECN if non-compliant
            if not compliance['compliant']:
                logger.info("\n4. STARTING ECN WORKFLOW")
                logger.info("-" * 40)
                self.start_ecn_workflow(
                    loader_id,
                    "Update compliance documentation and battery safety certification"
                )
            
            # Step 5: Generate report
            logger.info("\n5. GENERATING EQUIPMENT REPORT")
            logger.info("-" * 40)
            report = self.generate_equipment_report(loader_id)
            
            logger.info("\n" + "=" * 60)
            logger.info("DEMONSTRATION COMPLETE")
            logger.info(f"Created equipment: {loader_id}")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"Demo failed: {e}")
        
        finally:
            # Cleanup
            self.client.logout()


def main():
    """
    Main execution function
    """
    # Configuration
    BASE_URL = os.getenv('TEAMCENTER_URL', 'https://teamcenter.epiroc.com/tc')
    USERNAME = os.getenv('TEAMCENTER_USER', 'demo.user@epiroc.com')
    PASSWORD = os.getenv('TEAMCENTER_PASS', 'demo_password')
    
    # Note: In production, use proper credential management
    logger.warning("Using demo credentials. Set environment variables for real connection.")
    
    try:
        # Create automation instance
        automation = EquipmentAutomation(BASE_URL, USERNAME, PASSWORD)
        
        # Run demonstration
        automation.run_full_demo()
        
    except Exception as e:
        logger.error(f"Automation failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())