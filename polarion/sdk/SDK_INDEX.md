# Polarion SDK Component Index

## 📚 API Categories

### 1. Core Platform APIs

#### Open Java API
**Package**: `com.polarion.platform`
**Purpose**: Core platform functionality and extensions
**Key Interfaces**:
- `IWorkItem` - Work item manipulation
- `IProject` - Project management
- `IUser` - User management
- `IModule` - Document/module handling
- `ITestRun` - Test execution

**Common Use Cases**:
```java
// Create custom work item
IWorkItem requirement = project.createWorkItem("requirement");
requirement.setTitle("Battery voltage monitoring");
requirement.setValue("priority", "critical");
requirement.save();
```

#### Rendering Java API
**Package**: `com.polarion.platform.rendering`
**Purpose**: Content rendering and transformation
**Key Classes**:
- `IRenderer` - Wiki to HTML rendering
- `IExporter` - Document export
- `IPDFGenerator` - PDF generation

### 2. Integration APIs

#### REST API
**Base URL**: `/polarion/rest/v1`
**Authentication**: OAuth 2.0, Basic Auth
**Key Endpoints**:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/projects` | GET | List projects |
| `/projects/{id}/workitems` | GET/POST | Manage work items |
| `/projects/{id}/testruns` | GET/POST | Test management |
| `/projects/{id}/documents` | GET/POST | Document operations |
| `/projects/{id}/plans` | GET | Planning data |

**Example Request**:
```bash
curl -X GET \
  https://polarion.server/rest/v1/projects/EPIROC/workitems \
  -H 'Authorization: Bearer {token}' \
  -H 'Accept: application/json'
```

#### Web Services API (SOAP)
**WSDL**: `/polarion/ws/services?wsdl`
**Key Services**:

1. **TrackerWebService**
   - `createWorkItem()`
   - `updateWorkItem()`
   - `queryWorkItems()`
   - `getWorkItemHistory()`

2. **TestManagementWebService**
   - `createTestRun()`
   - `executeTestCase()`
   - `getTestResults()`

3. **PlanningWebService**
   - `createPlan()`
   - `updatePlanItem()`
   - `calculateVelocity()`

### 3. Scripting APIs

#### JavaScript/Velocity Context
**Available Objects**:
- `$workItem` - Current work item
- `$project` - Current project
- `$user` - Current user
- `$trackerService` - Tracker operations
- `$securityService` - Security checks

**Example Workflow Script**:
```javascript
// Auto-assign safety-critical items
if (workItem.getType().getId() == "safetyrequirement") {
    var sil = workItem.getValue("safety_integrity_level");
    if (sil >= 3) {
        workItem.setAssignee("senior_safety_engineer");
        workItem.addComment("Auto-assigned due to SIL-" + sil);
    }
}
```

### 4. Extension Points

#### Custom Fields
**Location**: `/opt/polarion/extensions/custom-fields`
```xml
<field id="battery_chemistry">
    <type>enum</type>
    <values>
        <value>LiFePO4</value>
        <value>NMC</value>
        <value>LTO</value>
    </values>
    <required>true</required>
</field>
```

#### Custom Workflows
**Location**: `/opt/polarion/extensions/workflows`
```xml
<workflow id="safety_review">
    <state id="draft">
        <transition to="review">
            <condition>hasRole("engineer")</condition>
        </transition>
    </state>
    <state id="review">
        <transition to="approved">
            <condition>hasRole("safety_officer")</condition>
            <action>notifyStakeholders()</action>
        </transition>
    </state>
</workflow>
```

#### Custom Importers/Exporters
**Interface**: `com.polarion.platform.importer.IImporter`
```java
public class ReqIFImporter implements IImporter {
    @Override
    public void importData(InputStream data, IProject project) {
        // Parse ReqIF format
        // Create work items
        // Maintain traceability
    }
}
```

## 🔧 SDK Tools & Utilities

### Development Tools

#### 1. Polarion SDK Eclipse Plugin
- Syntax highlighting
- Code completion
- Debugging support
- Deployment tools

#### 2. Polarion CLI
```bash
# Deploy extension
polarion-cli deploy-extension my-extension.jar

# Run tests
polarion-cli test --project EPIROC

# Export data
polarion-cli export --format reqif --output requirements.xml
```

#### 3. SDK Maven Archetype
```bash
mvn archetype:generate \
  -DarchetypeGroupId=com.polarion \
  -DarchetypeArtifactId=polarion-extension \
  -DgroupId=com.epiroc \
  -DartifactId=epiroc-polarion-extensions
```

## 📦 Pre-built Extensions

### Available in SDK

1. **Git Integration**
   - Commit linking
   - Branch tracking
   - Merge request integration

2. **Jenkins Plugin**
   - Build triggering
   - Test result import
   - Deployment tracking

3. **JIRA Connector**
   - Issue synchronization
   - Status mapping
   - Comment sync

4. **Email Notifications**
   - Custom templates
   - Conditional sending
   - Digest options

5. **Custom Reports**
   - Traceability matrix
   - Test coverage
   - Compliance dashboard

## 🏗️ Architecture Patterns

### Extension Architecture
```
polarion-extensions/
├── core/
│   ├── work-items/      # Custom work item types
│   ├── workflows/        # Workflow definitions
│   └── fields/          # Custom fields
├── integration/
│   ├── rest/            # REST endpoints
│   ├── soap/            # SOAP services
│   └── webhooks/        # Event handlers
├── ui/
│   ├── widgets/         # UI widgets
│   ├── forms/           # Custom forms
│   └── pages/           # Custom pages
└── jobs/
    ├── scheduled/       # Cron jobs
    └── triggered/       # Event-driven jobs
```

### Data Flow Pattern
```
External System → REST/SOAP API → Polarion Core → Database
                                         ↓
                            Notifications → Users/Systems
```

## 🔍 Common Integration Scenarios

### 1. Teamcenter Integration
```java
// Sync requirements from Teamcenter
public class TeamcenterSync {
    public void syncRequirements() {
        // 1. Connect to Teamcenter
        TeamcenterClient tc = new TeamcenterClient();
        
        // 2. Query requirements
        List<Requirement> tcReqs = tc.getRequirements();
        
        // 3. Create/update in Polarion
        for (Requirement req : tcReqs) {
            IWorkItem polarionReq = findOrCreate(req.getId());
            polarionReq.setValue("tc_id", req.getId());
            polarionReq.setValue("description", req.getText());
            polarionReq.save();
        }
    }
}
```

### 2. Test Automation Integration
```python
# Import test results from pytest
import requests

def upload_test_results(project_id, test_run_id, results):
    url = f"https://polarion/rest/v1/projects/{project_id}/testruns/{test_run_id}/results"
    
    for test in results:
        payload = {
            "testCaseId": test.id,
            "status": "passed" if test.passed else "failed",
            "duration": test.duration,
            "comment": test.output
        }
        
        response = requests.post(url, json=payload, headers=auth_headers)
```

### 3. Compliance Reporting
```sql
-- Query for compliance dashboard
SELECT 
    wi.c_id as requirement_id,
    wi.c_title as requirement_text,
    wi.c_status as status,
    cf.safety_level as sil_level,
    cf.standard as compliance_standard,
    tr.passed_count,
    tr.failed_count
FROM 
    workitem wi
    JOIN custom_fields cf ON wi.c_uri = cf.work_item_uri
    LEFT JOIN test_results tr ON wi.c_id = tr.requirement_id
WHERE 
    wi.c_type = 'safetyrequirement'
    AND wi.project_id = 'EPIROC'
```

## 📈 Performance Optimization

### Best Practices

1. **Batch Operations**
```java
// Good: Batch save
transaction.begin();
for (IWorkItem item : items) {
    item.setValue("status", "reviewed");
}
transaction.commit(); // Single save

// Bad: Individual saves
for (IWorkItem item : items) {
    item.setValue("status", "reviewed");
    item.save(); // Multiple saves
}
```

2. **Caching**
```java
// Cache frequently accessed data
private static final Map<String, IUser> userCache = new HashMap<>();

public IUser getUser(String id) {
    return userCache.computeIfAbsent(id, k -> loadUser(k));
}
```

3. **Async Processing**
```java
// Use async for non-critical operations
CompletableFuture.runAsync(() -> {
    sendNotifications(workItem);
    updateMetrics(workItem);
});
```

## 🚨 Common Pitfalls

1. **Transaction Management**: Always use transactions for bulk operations
2. **Memory Leaks**: Close resources and clear caches
3. **API Limits**: Respect rate limits (100 requests/minute)
4. **Permission Checks**: Always verify user permissions
5. **Data Validation**: Validate before saving to avoid corruption

---
*SDK Index - Your guide to extending Polarion for embedded systems PLM*