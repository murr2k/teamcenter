# Teamcenter Automation Project

## 🤖 Automated PLM Operations for Mining Equipment

This subproject provides automation scripts, tools, and examples for integrating with Teamcenter PLM at Epiroc. Focus on mining equipment lifecycle automation, compliance management, and engineering workflows.

## 📁 Project Structure

```
automation/
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
├── config/
│   ├── settings.yaml                # Configuration settings
│   ├── credentials.env.example      # Credential template
│   └── endpoints.json               # API endpoint definitions
├── src/
│   ├── __init__.py
│   ├── client/                      # API client implementations
│   │   ├── rest_client.py           # REST API client
│   │   ├── soa_client.py            # SOA client wrapper
│   │   └── auth.py                  # Authentication handlers
│   ├── services/                    # Business logic services
│   │   ├── equipment.py             # Equipment management
│   │   ├── bom.py                   # BOM operations
│   │   ├── compliance.py            # Compliance automation
│   │   ├── workflow.py              # Workflow automation
│   │   └── reporting.py             # Report generation
│   └── utils/                       # Utility functions
│       ├── logger.py                # Logging configuration
│       ├── retry.py                 # Retry mechanisms
│       └── validators.py            # Data validators
├── scripts/                         # Standalone automation scripts
│   ├── daily_compliance_check.py
│   ├── bom_sync.py
│   ├── ecn_processor.py
│   └── batch_cad_import.py
├── templates/                       # Document templates
│   ├── ecn_template.json
│   ├── compliance_report.html
│   └── bom_comparison.xlsx
├── tests/                           # Test suite
│   ├── test_client.py
│   ├── test_services.py
│   └── fixtures/
└── examples/                        # Usage examples
    ├── create_equipment.py
    ├── manage_bom.py
    └── start_workflow.py
```

## 🚀 Quick Start

### Installation

1. **Clone the repository**
```bash
cd /home/murr2k/projects/teamcenter
```

2. **Set up Python environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r automation/requirements.txt
```

3. **Configure credentials**
```bash
cp automation/config/credentials.env.example automation/config/credentials.env
# Edit credentials.env with your Teamcenter credentials
```

4. **Test connection**
```bash
python automation/examples/test_connection.py
```

### Basic Usage

```python
from automation.src.client import TeamcenterClient
from automation.src.services import EquipmentService

# Initialize client
client = TeamcenterClient()
client.connect()

# Create equipment service
equipment_service = EquipmentService(client)

# Create new equipment
loader = equipment_service.create_equipment({
    "name": "Scooptram ST1030",
    "type": "Underground Loader",
    "power": "Battery Electric",
    "capacity": "10 tonnes"
})

print(f"Created equipment: {loader.item_id}")
```

## 📋 Available Scripts

### Daily Compliance Check
Automated compliance verification for all equipment:
```bash
python automation/scripts/daily_compliance_check.py --email-report
```

### BOM Synchronization
Sync BOMs between Teamcenter and ERP:
```bash
python automation/scripts/bom_sync.py --source teamcenter --target sap
```

### ECN Processing
Batch process engineering changes:
```bash
python automation/scripts/ecn_processor.py --priority high --auto-approve
```

### CAD Batch Import
Import multiple CAD files with metadata:
```bash
python automation/scripts/batch_cad_import.py --folder /cad/files --validate
```

## 🔧 Core Services

### Equipment Service
```python
from automation.src.services import EquipmentService

service = EquipmentService(client)

# Create equipment
equipment = service.create_equipment(data)

# Update properties
service.update_equipment(item_id, properties)

# Get compliance status
status = service.check_compliance(item_id)

# Generate reports
report = service.generate_equipment_report(item_id)
```

### BOM Service
```python
from automation.src.services import BOMService

bom_service = BOMService(client)

# Get BOM structure
structure = bom_service.get_structure(item_id)

# Add component
bom_service.add_component(parent_id, child_id, quantity)

# Compare BOMs
diff = bom_service.compare(item1_id, item2_id)

# Export to Excel
bom_service.export_to_excel(item_id, "output.xlsx")
```

### Workflow Service
```python
from automation.src.services import WorkflowService

workflow_service = WorkflowService(client)

# Start ECN workflow
workflow = workflow_service.start_ecn(item_id, change_description)

# Get pending tasks
tasks = workflow_service.get_my_tasks()

# Complete task
workflow_service.complete_task(task_id, decision="approve")
```

## 🔐 Security

### Credential Management
- Never commit credentials to version control
- Use environment variables or secure vaults
- Rotate API keys regularly
- Implement token refresh logic

### Example secure configuration:
```python
import os
from dotenv import load_dotenv

load_dotenv('automation/config/credentials.env')

config = {
    'base_url': os.getenv('TEAMCENTER_URL'),
    'username': os.getenv('TEAMCENTER_USER'),
    'password': os.getenv('TEAMCENTER_PASS'),
    'use_ssl': True,
    'verify_cert': True
}
```

## 📊 Monitoring & Logging

### Logging Configuration
```python
import logging
from automation.src.utils.logger import setup_logger

logger = setup_logger('automation', level=logging.INFO)
logger.info('Starting automation process')
```

### Performance Monitoring
```python
from automation.src.utils.monitor import PerformanceMonitor

monitor = PerformanceMonitor()
with monitor.track('api_call'):
    result = client.get_item(item_id)

print(monitor.get_metrics())
```

## 🧪 Testing

Run the test suite:
```bash
# All tests
pytest automation/tests/

# Specific test
pytest automation/tests/test_client.py::test_authentication

# With coverage
pytest --cov=automation automation/tests/
```

## 📚 API Documentation

Detailed API documentation is available in:
- [Teamcenter API Guide](../docs/api/teamcenter-api-guide.md)
- [REST API Reference](../docs/api/rest-api-reference.md)
- [SOA Examples](../docs/api/soa-examples.md)

## 🛠️ Development

### Adding New Services

1. Create service file in `src/services/`
2. Inherit from `BaseService`
3. Implement business logic
4. Add tests in `tests/`
5. Document in this README

### Contributing Guidelines

1. Follow PEP 8 for Python code
2. Add type hints to all functions
3. Write unit tests for new features
4. Update documentation
5. Use meaningful commit messages

## 📈 Roadmap

### Phase 1 (Current)
- ✅ Basic API client implementation
- ✅ Equipment management
- ✅ BOM operations
- ✅ Compliance checking

### Phase 2 (Q2 2025)
- [ ] Advanced workflow automation
- [ ] Machine learning for predictive maintenance
- [ ] Real-time monitoring dashboard
- [ ] Mobile app integration

### Phase 3 (Q3 2025)
- [ ] IoT sensor integration
- [ ] Automated report generation
- [ ] AI-powered change impact analysis
- [ ] Full ERP synchronization

## 🆘 Troubleshooting

### Common Issues

**Connection timeout:**
```python
# Increase timeout in config
client = TeamcenterClient(timeout=60)
```

**Authentication failure:**
```python
# Check credentials and try SSO
client.connect(use_sso=True)
```

**Rate limiting:**
```python
# Implement retry with backoff
from automation.src.utils.retry import retry_with_backoff

@retry_with_backoff(max_retries=3)
def api_call():
    return client.get_item(item_id)
```

## 📞 Support

- Internal Wiki: [Teamcenter Automation Guide]
- Slack Channel: #teamcenter-automation
- Email: plm-support@epiroc.com

## 📄 License

© 2025 Murray Kopit. All Rights Reserved.

This automation framework is proprietary and confidential. See [LICENSE](../LICENSE) for details.
