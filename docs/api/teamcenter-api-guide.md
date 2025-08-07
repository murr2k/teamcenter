# Teamcenter API Complete Guide

## Table of Contents
- [Overview](#overview)
- [API Architecture](#api-architecture)
- [Authentication](#authentication)
- [SOA Framework](#soa-framework)
- [REST APIs](#rest-apis)
- [ITK Programming](#itk-programming)
- [Code Examples](#code-examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

Teamcenter provides multiple API interfaces for integration, automation, and customization. This guide covers all available APIs and their practical applications for mining equipment industry automation.

### Available API Types

| API Type | Language Support | Use Case | Complexity |
|----------|-----------------|----------|------------|
| **SOA (Service-Oriented Architecture)** | Java, C#, C++, Python | Enterprise integrations | Medium |
| **REST API** | Any language | Web integrations, lightweight apps | Low |
| **ITK (Integration Toolkit)** | C/C++ | Server-side customization | High |
| **Active Workspace APIs** | JavaScript/TypeScript | UI customization | Medium |
| **RAC (Rich Client) APIs** | Java | Desktop client customization | High |

## API Architecture

### System Architecture
```
┌─────────────────────────────────────────────────────────┐
│                   Client Applications                    │
│  (Web Apps, Mobile, Desktop, IoT Devices, ERP Systems)  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                    API Gateway Layer                     │
│         (Authentication, Rate Limiting, Routing)         │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┬─────────────────────┐
        │                         │                      │
┌───────▼──────┐       ┌──────────▼────────┐   ┌────────▼────────┐
│   REST API   │       │   SOA Services    │   │   ITK Server    │
│   (Modern)   │       │   (Enterprise)    │   │  (Customization)│
└───────┬──────┘       └──────────┬────────┘   └────────┬────────┘
        │                         │                      │
        └─────────────┬───────────┴──────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│              Teamcenter Business Logic                   │
│     (Items, BOMs, Workflows, Documents, Changes)         │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                  Database Layer                          │
│            (Oracle / SQL Server)                         │
└──────────────────────────────────────────────────────────┘
```

## Authentication

### 1. Basic Authentication
```python
# Python example
import requests
from requests.auth import HTTPBasicAuth

base_url = "https://teamcenter.epiroc.com/tc"
auth = HTTPBasicAuth('username', 'password')

response = requests.get(f"{base_url}/restful/auth/login", auth=auth)
session_token = response.json()['token']
```

### 2. SSO (Single Sign-On)
```java
// Java SOA example
Connection connection = new Connection("https://teamcenter.epiroc.com/tc");
connection.setOption(Connection.OPT_USE_SSO, true);
SessionService sessionService = SessionService.getService(connection);
sessionService.loginSSO();
```

### 3. Token-Based Authentication
```javascript
// JavaScript REST API
const authToken = await fetch('https://teamcenter.epiroc.com/tc/restful/auth/token', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'user@epiroc.com',
        password: 'password',
        grant_type: 'password'
    })
});

const token = await authToken.json();
// Use token.access_token for subsequent requests
```

### 4. Certificate-Based Authentication
```python
# Python with client certificate
import requests

cert = ('/path/to/client.crt', '/path/to/client.key')
response = requests.get(
    'https://teamcenter.epiroc.com/tc/restful/api/items',
    cert=cert,
    verify='/path/to/ca-bundle.crt'
)
```

## SOA Framework

### Service Structure

The SOA framework provides these core services:

#### DataManagement Service
- Create, read, update, delete operations
- File upload/download
- Relationship management

#### Query Service
- Saved queries execution
- Dynamic queries
- Full-text search

#### Workflow Service
- Process initiation
- Task management
- Status tracking

#### Structure Service
- BOM operations
- Configuration management
- Effectivity handling

### Java SOA Example - Complete Item Creation
```java
import com.teamcenter.soa.client.Connection;
import com.teamcenter.soa.client.model.ModelObject;
import com.teamcenter.services.strong.core.DataManagementService;
import com.teamcenter.services.strong.core._2008_06.DataManagement.*;

public class TeamcenterItemCreator {
    
    private Connection connection;
    private DataManagementService dmService;
    
    public void connect() throws Exception {
        String serverUrl = "https://teamcenter.epiroc.com/tc";
        connection = new Connection(serverUrl);
        
        // Login
        SessionService sessionService = SessionService.getService(connection);
        sessionService.login("username", "password", "group", "role");
        
        // Get service
        dmService = DataManagementService.getService(connection);
    }
    
    public Item createMiningEquipmentItem() throws Exception {
        // Create item properties
        ItemProperties itemProps = new ItemProperties();
        itemProps.clientId = "CreateItem_" + System.currentTimeMillis();
        itemProps.itemId = "SCOOPTRAM-" + generateId();
        itemProps.revId = "A";
        itemProps.name = "Scooptram ST1030 Battery Loader";
        itemProps.type = "EPR_Equipment";  // Custom type for Epiroc equipment
        itemProps.description = "Battery-electric underground loader";
        
        // Set custom properties
        Map<String, String> properties = new HashMap<>();
        properties.put("epr_equipment_type", "Underground Loader");
        properties.put("epr_power_type", "Battery Electric");
        properties.put("epr_capacity", "10 tonnes");
        properties.put("epr_battery_voltage", "650V");
        itemProps.extendedAttributes = properties;
        
        // Create the item
        CreateResponse response = dmService.createItems(new ItemProperties[]{itemProps});
        
        if (response.serviceData.sizeOfPartialErrors() > 0) {
            throw new Exception("Error creating item: " + 
                response.serviceData.getPartialError(0).getMessage());
        }
        
        return response.output[0].item;
    }
    
    public void attachCADDocument(Item item, String cadFilePath) throws Exception {
        // Create dataset for CAD file
        DatasetProperties datasetProps = new DatasetProperties();
        datasetProps.clientId = "Dataset_" + System.currentTimeMillis();
        datasetProps.type = "UGMASTER";  // For NX CAD files
        datasetProps.name = item.get_item_id() + "_CAD";
        datasetProps.description = "CAD Model";
        
        CreateResponse response = dmService.createDatasets(
            new DatasetProperties[]{datasetProps}
        );
        
        Dataset dataset = response.output[0].dataset;
        
        // Upload file
        FileManagementUtility fmUtil = new FileManagementUtility(connection);
        fmUtil.uploadFile(dataset, cadFilePath);
        
        // Attach to item revision
        dmService.createRelations(new Relationship[]{
            new Relationship(item.get_latest_item_revision(), 
                            dataset, 
                            "IMAN_specification")
        });
    }
}
```

### C# SOA Example - BOM Management
```csharp
using Teamcenter.Soa.Client;
using Teamcenter.Soa.Client.Model.Strong;
using Teamcenter.Services.Strong.Core;
using Teamcenter.Services.Strong.Cad;

public class BOMManager
{
    private Connection connection;
    private StructureManagementService structureService;
    
    public async Task<BOMWindow> CreateBOMStructure()
    {
        // Connect to Teamcenter
        connection = new Connection("https://teamcenter.epiroc.com/tc");
        await connection.LoginAsync("username", "password");
        
        structureService = StructureManagementService.GetService(connection);
        
        // Create BOM window
        var bomWindow = await structureService.CreateBOMWindowAsync(
            topItemRevision,
            new CreateBOMWindowInfo
            {
                RevisionRule = "Latest Working",
                ActiveAssemblyArrangement = null,
                ConfigContext = null
            }
        );
        
        // Add components
        await AddBOMLine(bomWindow, "HYDRAULIC-PUMP-001", 1);
        await AddBOMLine(bomWindow, "BATTERY-PACK-650V", 2);
        await AddBOMLine(bomWindow, "CONTROL-SYSTEM-V2", 1);
        
        return bomWindow;
    }
    
    private async Task AddBOMLine(BOMWindow window, string componentId, int quantity)
    {
        var component = await FindItem(componentId);
        
        await structureService.AddBOMLineAsync(
            window.TopBOMLine,
            component.LatestItemRevision,
            quantity,
            new BOMLineProperties
            {
                SequenceNumber = GetNextSequence(),
                Quantity = quantity.ToString(),
                UnitOfMeasure = "each"
            }
        );
    }
}
```

## REST APIs

### REST API Structure

Base URL: `https://teamcenter.epiroc.com/tc/restful/`

### Common Endpoints

#### Items and Revisions
```http
GET /items                          # List all items
GET /items/{id}                     # Get specific item
POST /items                         # Create new item
PUT /items/{id}                     # Update item
DELETE /items/{id}                  # Delete item
GET /items/{id}/revisions           # Get item revisions
POST /items/{id}/revisions          # Create new revision
```

#### BOM Operations
```http
GET /bom/{id}/structure             # Get BOM structure
POST /bom/{id}/lines                # Add BOM line
PUT /bom/{id}/lines/{lineId}        # Update BOM line
DELETE /bom/{id}/lines/{lineId}     # Remove BOM line
GET /bom/{id}/where-used            # Where-used query
POST /bom/{id}/compare              # Compare BOMs
```

#### Workflow
```http
GET /workflows                      # List workflows
POST /workflows/start               # Start workflow
GET /workflows/{id}/tasks           # Get workflow tasks
POST /workflows/{id}/tasks/{taskId}/complete  # Complete task
```

#### Documents
```http
GET /documents                      # List documents
POST /documents/upload              # Upload document
GET /documents/{id}/download        # Download document
GET /documents/{id}/versions        # Get versions
```

### Python REST API Client
```python
import requests
import json
from typing import Dict, List, Optional
from datetime import datetime

class TeamcenterRESTClient:
    """
    Teamcenter REST API Client for Mining Equipment Automation
    """
    
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.token = None
        self.authenticate(username, password)
    
    def authenticate(self, username: str, password: str):
        """Authenticate and get session token"""
        auth_url = f"{self.base_url}/auth/login"
        response = self.session.post(
            auth_url,
            json={"username": username, "password": password}
        )
        response.raise_for_status()
        self.token = response.json()['token']
        self.session.headers.update({
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        })
    
    def create_equipment_item(self, equipment_data: Dict) -> Dict:
        """Create a new mining equipment item"""
        item_data = {
            "itemId": equipment_data.get('id', f"EQP-{datetime.now().strftime('%Y%m%d%H%M%S')}"),
            "name": equipment_data['name'],
            "description": equipment_data.get('description', ''),
            "type": "EPR_MiningEquipment",
            "properties": {
                "epr_equipment_type": equipment_data.get('type', 'Loader'),
                "epr_model": equipment_data.get('model', ''),
                "epr_serial_number": equipment_data.get('serial', ''),
                "epr_power_type": equipment_data.get('power', 'Electric'),
                "epr_capacity": equipment_data.get('capacity', ''),
                "epr_operating_voltage": equipment_data.get('voltage', ''),
                "epr_safety_rating": equipment_data.get('safety_rating', 'MSHA'),
                "epr_manufacture_date": equipment_data.get('mfg_date', ''),
                "epr_facility": "Pitt Meadows"
            }
        }
        
        response = self.session.post(
            f"{self.base_url}/items",
            json=item_data
        )
        response.raise_for_status()
        return response.json()
    
    def get_bom_structure(self, item_id: str, levels: int = -1) -> Dict:
        """Get BOM structure for equipment"""
        params = {
            "levels": levels,
            "includeProperties": True,
            "includeDocuments": True
        }
        response = self.session.get(
            f"{self.base_url}/bom/{item_id}/structure",
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    def add_component_to_bom(self, parent_id: str, component_id: str, 
                            quantity: int = 1, properties: Dict = None) -> Dict:
        """Add component to equipment BOM"""
        bom_line_data = {
            "parentId": parent_id,
            "componentId": component_id,
            "quantity": quantity,
            "properties": properties or {}
        }
        
        response = self.session.post(
            f"{self.base_url}/bom/{parent_id}/lines",
            json=bom_line_data
        )
        response.raise_for_status()
        return response.json()
    
    def start_ecn_workflow(self, item_id: str, change_description: str, 
                          impact_analysis: str) -> Dict:
        """Start Engineering Change Notice workflow"""
        workflow_data = {
            "processTemplate": "EPR_ECN_Process",
            "name": f"ECN for {item_id}",
            "description": change_description,
            "targets": [item_id],
            "properties": {
                "change_reason": change_description,
                "impact_analysis": impact_analysis,
                "priority": "Normal",
                "implementation_date": datetime.now().isoformat()
            }
        }
        
        response = self.session.post(
            f"{self.base_url}/workflows/start",
            json=workflow_data
        )
        response.raise_for_status()
        return response.json()
    
    def query_equipment_by_type(self, equipment_type: str) -> List[Dict]:
        """Query all equipment of specific type"""
        query_data = {
            "queryName": "EPR_Equipment_By_Type",
            "parameters": {
                "equipment_type": equipment_type
            },
            "maxResults": 100
        }
        
        response = self.session.post(
            f"{self.base_url}/query/execute",
            json=query_data
        )
        response.raise_for_status()
        return response.json()['results']
    
    def get_equipment_compliance_docs(self, item_id: str) -> List[Dict]:
        """Get all compliance documents for equipment"""
        response = self.session.get(
            f"{self.base_url}/items/{item_id}/relations",
            params={"relationType": "EPR_Compliance_Doc"}
        )
        response.raise_for_status()
        return response.json()['documents']
    
    def upload_cad_file(self, item_id: str, file_path: str, 
                       file_type: str = "NX") -> Dict:
        """Upload CAD file for equipment"""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {
                'itemId': item_id,
                'datasetType': file_type,
                'relation': 'IMAN_specification'
            }
            response = self.session.post(
                f"{self.base_url}/documents/upload",
                files=files,
                data=data
            )
        response.raise_for_status()
        return response.json()

# Example usage
if __name__ == "__main__":
    # Initialize client
    client = TeamcenterRESTClient(
        base_url="https://teamcenter.epiroc.com/tc/restful",
        username="your.name@epiroc.com",
        password="your_password"
    )
    
    # Create new equipment
    new_loader = client.create_equipment_item({
        "name": "Scooptram ST1030 Battery",
        "description": "10-tonne battery-electric loader",
        "type": "Underground Loader",
        "model": "ST1030",
        "power": "Battery Electric",
        "capacity": "10 tonnes",
        "voltage": "650V DC",
        "safety_rating": "MSHA/CE"
    })
    
    print(f"Created equipment: {new_loader['itemId']}")
    
    # Add components to BOM
    client.add_component_to_bom(
        parent_id=new_loader['itemId'],
        component_id="BATTERY-PACK-650V",
        quantity=2
    )
    
    # Query all loaders
    loaders = client.query_equipment_by_type("Underground Loader")
    print(f"Found {len(loaders)} loaders in system")
```

## ITK Programming

### ITK Overview
The Integration Toolkit (ITK) is the C/C++ API for server-side customization.

### ITK Program Structure
```c
#include <tc/tc.h>
#include <tc/emh.h>
#include <tccore/item.h>
#include <tccore/aom.h>
#include <tccore/aom_prop.h>

int create_mining_equipment_item()
{
    int status = ITK_ok;
    tag_t item_tag = NULLTAG;
    tag_t rev_tag = NULLTAG;
    tag_t type_tag = NULLTAG;
    char *item_id = "SCOOPTRAM-001";
    char *item_name = "Scooptram ST1030";
    char *item_type = "EPR_Equipment";
    
    // Initialize ITK
    ITK_initialize_text_services(0);
    
    // Login
    status = ITK_init_module("username", "password", "group");
    if (status != ITK_ok) {
        printf("Login failed\n");
        return status;
    }
    
    // Find item type
    status = TCTYPE_find_type(item_type, NULL, &type_tag);
    
    // Create item
    status = ITEM_create_item2(
        item_id,           // Item ID
        item_name,         // Name
        type_tag,          // Type
        "A",              // Rev ID
        &item_tag,        // Output item
        &rev_tag          // Output revision
    );
    
    if (status == ITK_ok) {
        // Set custom properties
        status = AOM_set_value_string(
            rev_tag,
            "epr_equipment_type",
            "Underground Loader"
        );
        
        status = AOM_set_value_string(
            rev_tag,
            "epr_power_type",
            "Battery Electric"
        );
        
        // Save
        status = AOM_save(rev_tag);
        
        printf("Created item: %s\n", item_id);
    }
    
    // Cleanup
    ITK_exit_module(TRUE);
    
    return status;
}

// Custom handler for equipment validation
int EPR_validate_equipment_handler(
    int *decision,
    va_list args)
{
    int status = ITK_ok;
    tag_t rev_tag = va_arg(args, tag_t);
    char *voltage_str = NULL;
    double voltage = 0.0;
    
    // Get voltage property
    status = AOM_ask_value_string(
        rev_tag,
        "epr_operating_voltage",
        &voltage_str
    );
    
    if (status == ITK_ok && voltage_str != NULL) {
        voltage = atof(voltage_str);
        
        // Validate voltage for safety
        if (voltage > 1000.0) {
            *decision = EPR_REJECT;
            EMH_store_error_s1(
                EMH_severity_error,
                EPR_VOLTAGE_TOO_HIGH,
                "Voltage exceeds 1000V safety limit"
            );
        } else {
            *decision = EPR_ACCEPT;
        }
        
        MEM_free(voltage_str);
    }
    
    return status;
}
```

## Code Examples

### Example 1: Automated BOM Comparison
```python
def compare_equipment_boms(client: TeamcenterRESTClient, 
                          item1_id: str, item2_id: str) -> Dict:
    """
    Compare BOMs of two equipment items to find differences
    Useful for variant management and change impact analysis
    """
    
    # Get both BOM structures
    bom1 = client.get_bom_structure(item1_id, levels=-1)
    bom2 = client.get_bom_structure(item2_id, levels=-1)
    
    # Create comparison maps
    bom1_map = {line['componentId']: line for line in bom1['lines']}
    bom2_map = {line['componentId']: line for line in bom2['lines']}
    
    comparison = {
        'added': [],
        'removed': [],
        'modified': [],
        'unchanged': []
    }
    
    # Find additions and modifications
    for comp_id, line2 in bom2_map.items():
        if comp_id not in bom1_map:
            comparison['added'].append(line2)
        else:
            line1 = bom1_map[comp_id]
            if line1['quantity'] != line2['quantity']:
                comparison['modified'].append({
                    'component': comp_id,
                    'old_quantity': line1['quantity'],
                    'new_quantity': line2['quantity']
                })
            else:
                comparison['unchanged'].append(comp_id)
    
    # Find removals
    for comp_id, line1 in bom1_map.items():
        if comp_id not in bom2_map:
            comparison['removed'].append(line1)
    
    return comparison
```

### Example 2: Compliance Document Automation
```python
import os
from datetime import datetime, timedelta

def automate_compliance_check(client: TeamcenterRESTClient, 
                             equipment_type: str = "Underground Loader"):
    """
    Automated compliance document checking for mining equipment
    Ensures all required safety documents are present and current
    """
    
    required_docs = {
        'MSHA_Certification': 365,  # Days valid
        'CE_Declaration': 730,
        'Electrical_Safety_Test': 180,
        'Pressure_Vessel_Cert': 365,
        'Battery_Safety_Report': 90
    }
    
    # Get all equipment of type
    equipment_list = client.query_equipment_by_type(equipment_type)
    
    compliance_report = []
    
    for equipment in equipment_list:
        item_id = equipment['itemId']
        docs = client.get_equipment_compliance_docs(item_id)
        
        doc_map = {doc['type']: doc for doc in docs}
        
        equipment_compliance = {
            'itemId': item_id,
            'name': equipment['name'],
            'compliant': True,
            'issues': []
        }
        
        for doc_type, validity_days in required_docs.items():
            if doc_type not in doc_map:
                equipment_compliance['compliant'] = False
                equipment_compliance['issues'].append(f"Missing {doc_type}")
            else:
                doc = doc_map[doc_type]
                doc_date = datetime.fromisoformat(doc['created_date'])
                expiry_date = doc_date + timedelta(days=validity_days)
                
                if expiry_date < datetime.now():
                    equipment_compliance['compliant'] = False
                    equipment_compliance['issues'].append(
                        f"{doc_type} expired on {expiry_date.strftime('%Y-%m-%d')}"
                    )
                elif expiry_date < datetime.now() + timedelta(days=30):
                    equipment_compliance['issues'].append(
                        f"{doc_type} expires soon ({expiry_date.strftime('%Y-%m-%d')})"
                    )
        
        compliance_report.append(equipment_compliance)
        
        # Auto-create workflow for non-compliant equipment
        if not equipment_compliance['compliant']:
            workflow = client.start_ecn_workflow(
                item_id=item_id,
                change_description="Compliance documentation update required",
                impact_analysis=f"Issues: {', '.join(equipment_compliance['issues'])}"
            )
            print(f"Started workflow {workflow['id']} for {item_id}")
    
    return compliance_report
```

### Example 3: CAD File Batch Processing
```java
public class CADBatchProcessor {
    
    public void processCADFiles(String folderPath) {
        File folder = new File(folderPath);
        File[] cadFiles = folder.listFiles((dir, name) -> 
            name.endsWith(".prt") || name.endsWith(".asm"));
        
        for (File cadFile : cadFiles) {
            try {
                // Extract part number from filename
                String partNumber = extractPartNumber(cadFile.getName());
                
                // Find or create item
                Item item = findOrCreateItem(partNumber);
                
                // Create dataset
                Dataset dataset = createCADDataset(item, cadFile);
                
                // Extract metadata
                extractAndSetMetadata(dataset, cadFile);
                
                // Generate derived files
                generateDerivedFiles(dataset);
                
                System.out.println("Processed: " + cadFile.getName());
                
            } catch (Exception e) {
                System.err.println("Error processing " + 
                    cadFile.getName() + ": " + e.getMessage());
            }
        }
    }
    
    private void generateDerivedFiles(Dataset dataset) throws Exception {
        // Generate PDF drawing
        VisualizationService vizService = 
            VisualizationService.getService(connection);
        
        vizService.generatePDF(dataset, new PDFOptions() {{
            setInclude3D(true);
            setIncludePMI(true);
            setPageSize("A1");
        }});
        
        // Generate STEP file for exchange
        TranslationService transService = 
            TranslationService.getService(connection);
        
        transService.translateToSTEP(dataset, new STEPOptions() {{
            setApplicationProtocol("AP214");
            setIncludeAssemblyStructure(true);
        }});
    }
}
```

## Best Practices

### 1. Connection Management
```python
class TeamcenterConnectionPool:
    """Connection pool for managing multiple API connections"""
    
    def __init__(self, max_connections: int = 5):
        self.pool = []
        self.max_connections = max_connections
        self.lock = threading.Lock()
    
    def get_connection(self):
        with self.lock:
            if self.pool:
                return self.pool.pop()
            elif len(self.active) < self.max_connections:
                return self.create_connection()
            else:
                # Wait for available connection
                time.sleep(0.1)
                return self.get_connection()
    
    def return_connection(self, conn):
        with self.lock:
            self.pool.append(conn)
```

### 2. Error Handling
```python
class TeamcenterAPIError(Exception):
    """Custom exception for Teamcenter API errors"""
    
    def __init__(self, message, error_code=None, details=None):
        super().__init__(message)
        self.error_code = error_code
        self.details = details

def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """Decorator for retrying failed API calls"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except TeamcenterAPIError as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(delay * (2 ** attempt))
                    print(f"Retry {attempt + 1} after error: {e}")
            return None
        return wrapper
    return decorator

@retry_on_failure(max_retries=3)
def critical_api_call():
    # Your API call here
    pass
```

### 3. Logging and Monitoring
```python
import logging
from datetime import datetime

class APILogger:
    def __init__(self, log_file: str = "teamcenter_api.log"):
        self.logger = logging.getLogger("TeamcenterAPI")
        self.logger.setLevel(logging.DEBUG)
        
        # File handler
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
    
    def log_api_call(self, method: str, endpoint: str, 
                     response_time: float, status_code: int):
        self.logger.info(
            f"API Call: {method} {endpoint} - "
            f"Status: {status_code} - Time: {response_time:.2f}s"
        )
```

### 4. Performance Optimization
```python
class BatchProcessor:
    """Process multiple items in batches for better performance"""
    
    def __init__(self, batch_size: int = 50):
        self.batch_size = batch_size
    
    def process_items(self, items: List, process_func):
        results = []
        for i in range(0, len(items), self.batch_size):
            batch = items[i:i + self.batch_size]
            batch_results = self.process_batch(batch, process_func)
            results.extend(batch_results)
        return results
    
    def process_batch(self, batch: List, process_func):
        # Use threading for parallel processing
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(process_func, item) 
                      for item in batch]
            return [f.result() for f in futures]
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Authentication Failures
```python
# Problem: Token expiration
# Solution: Implement token refresh
class TokenManager:
    def __init__(self):
        self.token = None
        self.expiry = None
    
    def get_valid_token(self):
        if not self.token or datetime.now() >= self.expiry:
            self.refresh_token()
        return self.token
    
    def refresh_token(self):
        # Refresh logic here
        pass
```

#### 2. Rate Limiting
```python
# Problem: API rate limits exceeded
# Solution: Implement rate limiting
from time import time, sleep

class RateLimiter:
    def __init__(self, calls_per_second: int = 10):
        self.calls_per_second = calls_per_second
        self.calls = []
    
    def wait_if_needed(self):
        now = time()
        self.calls = [c for c in self.calls if now - c < 1.0]
        
        if len(self.calls) >= self.calls_per_second:
            sleep_time = 1.0 - (now - self.calls[0])
            if sleep_time > 0:
                sleep(sleep_time)
        
        self.calls.append(time())
```

#### 3. Large Dataset Handling
```python
# Problem: Memory issues with large BOMs
# Solution: Use pagination and streaming
def stream_large_bom(client, item_id: str, page_size: int = 100):
    """Stream large BOM structures page by page"""
    offset = 0
    while True:
        page = client.get_bom_page(item_id, offset, page_size)
        if not page['lines']:
            break
        
        for line in page['lines']:
            yield line
        
        offset += page_size
```

#### 4. Connection Timeouts
```python
# Problem: Long-running operations timeout
# Solution: Implement async operations with status polling
async def async_operation_with_polling(client, operation_id: str):
    """Poll for operation completion"""
    max_attempts = 60
    poll_interval = 5
    
    for attempt in range(max_attempts):
        status = await client.check_operation_status(operation_id)
        
        if status['state'] == 'completed':
            return status['result']
        elif status['state'] == 'failed':
            raise TeamcenterAPIError(f"Operation failed: {status['error']}")
        
        await asyncio.sleep(poll_interval)
    
    raise TimeoutError(f"Operation {operation_id} timed out")
```

## Security Best Practices

### 1. Credential Management
```python
import os
from cryptography.fernet import Fernet

class SecureCredentials:
    """Secure credential storage and retrieval"""
    
    def __init__(self):
        # Use environment variable for encryption key
        key = os.environ.get('TEAMCENTER_ENCRYPTION_KEY')
        if not key:
            raise ValueError("Encryption key not found in environment")
        self.cipher = Fernet(key.encode())
    
    def store_credentials(self, username: str, password: str):
        """Encrypt and store credentials"""
        encrypted_user = self.cipher.encrypt(username.encode())
        encrypted_pass = self.cipher.encrypt(password.encode())
        
        # Store in secure location (e.g., keyring, vault)
        # This is a simplified example
        with open('.credentials', 'wb') as f:
            f.write(encrypted_user + b'\n' + encrypted_pass)
    
    def get_credentials(self):
        """Retrieve and decrypt credentials"""
        with open('.credentials', 'rb') as f:
            lines = f.read().split(b'\n')
            username = self.cipher.decrypt(lines[0]).decode()
            password = self.cipher.decrypt(lines[1]).decode()
        return username, password
```

### 2. API Key Rotation
```python
class APIKeyRotation:
    """Automated API key rotation"""
    
    def __init__(self, rotation_days: int = 30):
        self.rotation_days = rotation_days
        self.last_rotation = datetime.now()
    
    def check_rotation_needed(self):
        days_since_rotation = (datetime.now() - self.last_rotation).days
        return days_since_rotation >= self.rotation_days
    
    def rotate_key(self):
        # Generate new API key
        new_key = self.generate_new_key()
        
        # Update in Teamcenter
        self.update_teamcenter_key(new_key)
        
        # Update local storage
        self.store_new_key(new_key)
        
        self.last_rotation = datetime.now()
        return new_key
```

## Performance Metrics

### Monitoring API Performance
```python
class PerformanceMonitor:
    """Track API performance metrics"""
    
    def __init__(self):
        self.metrics = {
            'total_calls': 0,
            'total_time': 0,
            'errors': 0,
            'by_endpoint': {}
        }
    
    def record_call(self, endpoint: str, duration: float, 
                   success: bool = True):
        self.metrics['total_calls'] += 1
        self.metrics['total_time'] += duration
        
        if not success:
            self.metrics['errors'] += 1
        
        if endpoint not in self.metrics['by_endpoint']:
            self.metrics['by_endpoint'][endpoint] = {
                'calls': 0,
                'total_time': 0,
                'avg_time': 0
            }
        
        ep_metrics = self.metrics['by_endpoint'][endpoint]
        ep_metrics['calls'] += 1
        ep_metrics['total_time'] += duration
        ep_metrics['avg_time'] = ep_metrics['total_time'] / ep_metrics['calls']
    
    def get_report(self):
        return {
            'average_response_time': self.metrics['total_time'] / 
                                    max(self.metrics['total_calls'], 1),
            'error_rate': self.metrics['errors'] / 
                         max(self.metrics['total_calls'], 1),
            'total_calls': self.metrics['total_calls'],
            'by_endpoint': self.metrics['by_endpoint']
        }
```

---

## Next Steps

1. **Set up development environment** with necessary SDKs
2. **Obtain API credentials** from your Teamcenter administrator
3. **Start with REST API** for simple integrations
4. **Use SOA for complex operations** requiring transactions
5. **Implement ITK for server-side** customizations

## Resources

- [Siemens Teamcenter Developer Portal](https://docs.sw.siemens.com/teamcenter)
- [API Documentation](https://support.sw.siemens.com/api-docs)
- [Sample Code Repository](https://github.com/siemens/teamcenter-samples)
- [Community Forum](https://community.sw.siemens.com/teamcenter-developers)