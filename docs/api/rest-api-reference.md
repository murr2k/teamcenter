# Teamcenter REST API Reference

## Table of Contents
- [Overview](#overview)
- [Authentication](#authentication)
- [Base URLs](#base-urls)
- [Common Headers](#common-headers)
- [Response Formats](#response-formats)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [API Endpoints](#api-endpoints)
  - [Items](#items)
  - [BOMs](#boms)
  - [Workflows](#workflows)
  - [Documents](#documents)
  - [Queries](#queries)
  - [Changes](#changes)
  - [Users](#users)
  - [Projects](#projects)

## Overview

The Teamcenter REST API provides programmatic access to PLM data and operations. This reference covers all available endpoints, request/response formats, and usage examples.

### API Version
Current Version: `v1`

### Base URL Pattern
```
https://{hostname}/tc/restful/{version}/{endpoint}
```

## Authentication

### Login Endpoint
```http
POST /auth/login
Content-Type: application/json

{
  "username": "user@epiroc.com",
  "password": "password",
  "group": "Engineering",
  "role": "Designer"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresIn": 3600,
  "user": {
    "id": "user123",
    "name": "John Doe",
    "email": "user@epiroc.com",
    "group": "Engineering",
    "role": "Designer"
  }
}
```

### Token Usage
Include the token in all subsequent requests:
```http
Authorization: Bearer {token}
```

### Logout
```http
POST /auth/logout
Authorization: Bearer {token}
```

### Token Refresh
```http
POST /auth/refresh
Authorization: Bearer {token}
```

## Base URLs

### Production
```
https://teamcenter.epiroc.com/tc/restful/v1
```

### Staging
```
https://teamcenter-staging.epiroc.com/tc/restful/v1
```

### Development
```
https://teamcenter-dev.epiroc.com/tc/restful/v1
```

## Common Headers

### Request Headers
```http
Content-Type: application/json
Accept: application/json
Authorization: Bearer {token}
X-TC-Project-ID: {projectId}  # Optional: for project context
X-TC-Locale: en_US            # Optional: for localization
```

### Response Headers
```http
Content-Type: application/json
X-TC-Request-ID: {requestId}
X-TC-Response-Time: {ms}
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## Response Formats

### Success Response
```json
{
  "success": true,
  "data": {
    // Response data
  },
  "metadata": {
    "timestamp": "2025-01-15T10:30:00Z",
    "requestId": "req_123456",
    "version": "v1"
  }
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ITEM_NOT_FOUND",
    "message": "Item with ID 'ITEM123' not found",
    "details": {
      "itemId": "ITEM123",
      "searchPath": "/items"
    }
  },
  "metadata": {
    "timestamp": "2025-01-15T10:30:00Z",
    "requestId": "req_123456"
  }
}
```

### Pagination Response
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "pageSize": 50,
    "totalPages": 10,
    "totalCount": 500,
    "hasNext": true,
    "hasPrevious": false
  }
}
```

## Error Handling

### HTTP Status Codes

| Code | Description | Usage |
|------|-------------|-------|
| 200 | OK | Successful GET, PUT |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid request format |
| 401 | Unauthorized | Invalid or missing token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource already exists |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Maintenance mode |

### Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| `AUTH_FAILED` | Authentication failed | Check credentials |
| `TOKEN_EXPIRED` | Token has expired | Refresh token |
| `PERMISSION_DENIED` | Insufficient permissions | Check user role |
| `ITEM_NOT_FOUND` | Item does not exist | Verify item ID |
| `DUPLICATE_ITEM` | Item already exists | Use different ID |
| `INVALID_PROPERTY` | Invalid property value | Check property constraints |
| `WORKFLOW_ERROR` | Workflow operation failed | Check workflow state |
| `FILE_TOO_LARGE` | File exceeds size limit | Reduce file size |
| `RATE_LIMIT_EXCEEDED` | Too many requests | Wait and retry |

## Rate Limiting

### Limits
- **Default:** 1000 requests per hour
- **Authenticated:** 5000 requests per hour
- **Enterprise:** 10000 requests per hour

### Rate Limit Headers
```http
X-RateLimit-Limit: 5000
X-RateLimit-Remaining: 4999
X-RateLimit-Reset: 1640995200
```

### Handling Rate Limits
```python
import time

def handle_rate_limit(response):
    if response.status_code == 429:
        reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
        wait_time = max(reset_time - time.time(), 0)
        time.sleep(wait_time)
        return True
    return False
```

## API Endpoints

### Items

#### List Items
```http
GET /items?page=1&pageSize=50&type=EPR_Equipment&sort=created_desc
```

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `pageSize` (integer): Items per page (default: 50, max: 100)
- `type` (string): Filter by item type
- `sort` (string): Sort order (created_asc, created_desc, modified_asc, modified_desc, name_asc, name_desc)
- `search` (string): Search term
- `properties` (object): Filter by properties

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "itemId": "SCOOPTRAM-001",
      "name": "Scooptram ST1030",
      "type": "EPR_Equipment",
      "revision": "A",
      "status": "Released",
      "created": "2025-01-15T10:00:00Z",
      "modified": "2025-01-15T11:00:00Z",
      "properties": {
        "epr_equipment_type": "Underground Loader",
        "epr_capacity": "10 tonnes"
      }
    }
  ],
  "pagination": {
    "page": 1,
    "pageSize": 50,
    "totalPages": 5,
    "totalCount": 250
  }
}
```

#### Get Item
```http
GET /items/{itemId}
```

**Path Parameters:**
- `itemId` (string): Item identifier

**Response:**
```json
{
  "success": true,
  "data": {
    "itemId": "SCOOPTRAM-001",
    "name": "Scooptram ST1030",
    "description": "10-tonne battery-electric loader",
    "type": "EPR_Equipment",
    "revision": "A",
    "status": "Released",
    "created": "2025-01-15T10:00:00Z",
    "createdBy": "user123",
    "modified": "2025-01-15T11:00:00Z",
    "modifiedBy": "user456",
    "properties": {
      "epr_equipment_type": "Underground Loader",
      "epr_model": "ST1030",
      "epr_capacity": "10 tonnes",
      "epr_power_type": "Battery Electric",
      "epr_voltage": "650V DC"
    },
    "relations": {
      "documents": 5,
      "children": 12,
      "parents": 1
    }
  }
}
```

#### Create Item
```http
POST /items
Content-Type: application/json

{
  "itemId": "DRILL-RIG-002",
  "name": "Boomer M2 Face Drilling Rig",
  "description": "Twin-boom face drilling rig",
  "type": "EPR_Equipment",
  "properties": {
    "epr_equipment_type": "Drilling Rig",
    "epr_model": "Boomer M2",
    "epr_power_type": "Diesel-Electric"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "itemId": "DRILL-RIG-002",
    "revisionId": "A",
    "created": true,
    "url": "/items/DRILL-RIG-002"
  }
}
```

#### Update Item
```http
PUT /items/{itemId}
Content-Type: application/json

{
  "name": "Updated Equipment Name",
  "description": "Updated description",
  "properties": {
    "epr_status": "In Service",
    "epr_location": "Pitt Meadows"
  }
}
```

#### Delete Item
```http
DELETE /items/{itemId}
```

**Query Parameters:**
- `force` (boolean): Force delete even if item has relations

#### Get Item Revisions
```http
GET /items/{itemId}/revisions
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "revisionId": "A",
      "status": "Released",
      "created": "2025-01-01T10:00:00Z",
      "effectiveDate": "2025-01-01T00:00:00Z",
      "description": "Initial release"
    },
    {
      "revisionId": "B",
      "status": "In Work",
      "created": "2025-01-15T10:00:00Z",
      "effectiveDate": null,
      "description": "Battery upgrade"
    }
  ]
}
```

#### Create Item Revision
```http
POST /items/{itemId}/revisions
Content-Type: application/json

{
  "revisionId": "B",
  "description": "Battery system upgrade",
  "copyFrom": "A",
  "includeRelations": true
}
```

### BOMs

#### Get BOM Structure
```http
GET /bom/{itemId}/structure?levels=2&revision=A&includeProperties=true
```

**Query Parameters:**
- `levels` (integer): Levels to expand (-1 for all, default: 1)
- `revision` (string): Specific revision (default: latest)
- `includeProperties` (boolean): Include line properties
- `includeDocuments` (boolean): Include attached documents
- `effectiveDate` (string): Effective date for configuration

**Response:**
```json
{
  "success": true,
  "data": {
    "root": {
      "itemId": "SCOOPTRAM-001",
      "revision": "A",
      "name": "Scooptram ST1030"
    },
    "lines": [
      {
        "lineId": "line_001",
        "level": 1,
        "parentId": "SCOOPTRAM-001",
        "childId": "BATTERY-PACK-650V",
        "childName": "Battery Pack System",
        "quantity": 1,
        "uom": "each",
        "findNumber": "10",
        "properties": {
          "critical": true,
          "leadTime": "12 weeks"
        },
        "children": [
          {
            "lineId": "line_002",
            "level": 2,
            "parentId": "BATTERY-PACK-650V",
            "childId": "BATTERY-CELL-001",
            "childName": "Battery Cell",
            "quantity": 240,
            "uom": "each"
          }
        ]
      }
    ]
  }
}
```

#### Add BOM Line
```http
POST /bom/{itemId}/lines
Content-Type: application/json

{
  "childId": "HYDRAULIC-PUMP-001",
  "quantity": 2,
  "uom": "each",
  "findNumber": "20",
  "properties": {
    "critical": true,
    "supplier": "Bosch Rexroth"
  }
}
```

#### Update BOM Line
```http
PUT /bom/{itemId}/lines/{lineId}
Content-Type: application/json

{
  "quantity": 3,
  "properties": {
    "notes": "Quantity increased for redundancy"
  }
}
```

#### Delete BOM Line
```http
DELETE /bom/{itemId}/lines/{lineId}
```

#### Get Where Used
```http
GET /bom/{itemId}/where-used?levels=1&type=EPR_Equipment
```

**Response:**
```json
{
  "success": true,
  "data": {
    "item": {
      "itemId": "BATTERY-PACK-650V",
      "name": "Battery Pack System"
    },
    "parents": [
      {
        "itemId": "SCOOPTRAM-001",
        "name": "Scooptram ST1030",
        "quantity": 1,
        "revision": "A"
      },
      {
        "itemId": "LOADER-002",
        "name": "Scooptram ST14",
        "quantity": 2,
        "revision": "B"
      }
    ]
  }
}
```

#### Compare BOMs
```http
POST /bom/compare
Content-Type: application/json

{
  "source": {
    "itemId": "SCOOPTRAM-001",
    "revision": "A"
  },
  "target": {
    "itemId": "SCOOPTRAM-001",
    "revision": "B"
  },
  "options": {
    "includeProperties": true,
    "includeQuantityChanges": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "added": [
      {
        "childId": "SAFETY-SYSTEM-V2",
        "name": "Enhanced Safety System",
        "quantity": 1
      }
    ],
    "removed": [
      {
        "childId": "SAFETY-SYSTEM-V1",
        "name": "Basic Safety System",
        "quantity": 1
      }
    ],
    "modified": [
      {
        "childId": "BATTERY-PACK-650V",
        "changes": {
          "quantity": {
            "old": 1,
            "new": 2
          }
        }
      }
    ],
    "unchanged": 15
  }
}
```

### Workflows

#### List Workflows
```http
GET /workflows?status=active&assignedTo=me
```

**Query Parameters:**
- `status` (string): active, completed, cancelled
- `assignedTo` (string): User ID or "me"
- `processType` (string): Workflow process type
- `target` (string): Target item ID

#### Start Workflow
```http
POST /workflows/start
Content-Type: application/json

{
  "processTemplate": "EPR_ECN_Process",
  "name": "ECN for Battery Upgrade",
  "description": "Upgrade battery system to 800V",
  "targets": ["SCOOPTRAM-001"],
  "properties": {
    "priority": "High",
    "changeType": "Major",
    "implementationDate": "2025-02-01",
    "estimatedHours": 40
  },
  "participants": {
    "reviewers": ["user123", "user456"],
    "approvers": ["manager001"]
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "workflowId": "WF-2025-001",
    "processId": "process_123",
    "status": "Active",
    "currentTask": {
      "taskId": "task_001",
      "name": "Initial Review",
      "assignedTo": ["user123"]
    }
  }
}
```

#### Get Workflow Status
```http
GET /workflows/{workflowId}
```

#### Get My Tasks
```http
GET /workflows/my-tasks?status=pending&priority=high
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "taskId": "task_001",
      "workflowId": "WF-2025-001",
      "name": "Review ECN",
      "description": "Review and approve ECN for battery upgrade",
      "priority": "High",
      "dueDate": "2025-01-20T17:00:00Z",
      "status": "Pending",
      "targets": [
        {
          "itemId": "SCOOPTRAM-001",
          "name": "Scooptram ST1030"
        }
      ],
      "actions": ["Approve", "Reject", "Request Info"]
    }
  ]
}
```

#### Complete Task
```http
POST /workflows/tasks/{taskId}/complete
Content-Type: application/json

{
  "decision": "Approve",
  "comments": "Approved with minor modifications",
  "properties": {
    "reviewNotes": "Ensure proper testing before implementation"
  }
}
```

#### Reassign Task
```http
POST /workflows/tasks/{taskId}/reassign
Content-Type: application/json

{
  "assignTo": "user789",
  "reason": "Subject matter expert required"
}
```

### Documents

#### Upload Document
```http
POST /documents/upload
Content-Type: multipart/form-data

FormData:
- file: (binary)
- itemId: SCOOPTRAM-001
- datasetType: MSWord
- datasetName: "Technical Specification"
- relationType: IMAN_specification
```

**Response:**
```json
{
  "success": true,
  "data": {
    "datasetId": "DS-001",
    "fileName": "tech_spec.docx",
    "fileSize": 2048576,
    "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "uploadedAt": "2025-01-15T12:00:00Z"
  }
}
```

#### Download Document
```http
GET /documents/{datasetId}/download
```

**Response:** Binary file stream

#### Get Document Info
```http
GET /documents/{datasetId}
```

#### List Item Documents
```http
GET /items/{itemId}/documents?type=IMAN_specification
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "datasetId": "DS-001",
      "name": "Technical Specification",
      "type": "MSWord",
      "fileName": "tech_spec.docx",
      "fileSize": 2048576,
      "created": "2025-01-15T12:00:00Z",
      "version": "1.0",
      "relationType": "IMAN_specification"
    }
  ]
}
```

### Queries

#### Execute Saved Query
```http
POST /queries/execute
Content-Type: application/json

{
  "queryName": "EPR_Equipment_By_Type",
  "parameters": {
    "equipment_type": "Underground Loader",
    "status": "Released"
  },
  "options": {
    "maxResults": 100,
    "includeProperties": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "queryName": "EPR_Equipment_By_Type",
    "executionTime": 250,
    "resultCount": 15,
    "results": [
      {
        "itemId": "SCOOPTRAM-001",
        "name": "Scooptram ST1030",
        "type": "EPR_Equipment",
        "properties": {
          "epr_equipment_type": "Underground Loader"
        }
      }
    ]
  }
}
```

#### List Available Queries
```http
GET /queries?category=Equipment
```

#### Full Text Search
```http
POST /search
Content-Type: application/json

{
  "query": "battery electric loader",
  "types": ["EPR_Equipment", "Document"],
  "filters": {
    "created": {
      "from": "2024-01-01",
      "to": "2025-01-31"
    },
    "status": ["Released", "In Work"]
  },
  "facets": ["type", "status", "equipment_type"],
  "page": 1,
  "pageSize": 20
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "query": "battery electric loader",
    "totalResults": 42,
    "results": [...],
    "facets": {
      "type": {
        "EPR_Equipment": 15,
        "Document": 27
      },
      "status": {
        "Released": 30,
        "In Work": 12
      }
    }
  }
}
```

### Changes

#### Create Engineering Change Request (ECR)
```http
POST /changes/ecr
Content-Type: application/json

{
  "title": "Battery System Upgrade",
  "description": "Upgrade from 650V to 800V battery system",
  "priority": "High",
  "category": "Design Change",
  "affectedItems": ["SCOOPTRAM-001", "BATTERY-PACK-650V"],
  "justification": "Improved performance and charging time",
  "impactAnalysis": {
    "safety": "Medium",
    "cost": "High",
    "schedule": "Low"
  }
}
```

#### Create Engineering Change Notice (ECN)
```http
POST /changes/ecn
Content-Type: application/json

{
  "ecrId": "ECR-2025-001",
  "title": "ECN: Battery System Upgrade",
  "implementationDate": "2025-03-01",
  "dispositions": [
    {
      "itemId": "BATTERY-PACK-650V",
      "action": "Revise",
      "newRevision": "B"
    }
  ]
}
```

#### Get Change Status
```http
GET /changes/{changeId}/status
```

### Users

#### Get Current User
```http
GET /users/me
```

**Response:**
```json
{
  "success": true,
  "data": {
    "userId": "user123",
    "username": "john.doe@epiroc.com",
    "name": "John Doe",
    "email": "john.doe@epiroc.com",
    "group": "Engineering",
    "role": "Designer",
    "permissions": [
      "create_item",
      "modify_item",
      "release_item",
      "create_ecn"
    ],
    "preferences": {
      "locale": "en_US",
      "timezone": "America/Vancouver",
      "defaultProject": "PROJ-001"
    }
  }
}
```

#### Search Users
```http
GET /users/search?q=john&group=Engineering
```

### Projects

#### List Projects
```http
GET /projects?status=active&member=me
```

#### Get Project Details
```http
GET /projects/{projectId}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "projectId": "PROJ-001",
    "name": "Scooptram Electrification",
    "description": "Convert diesel loaders to battery-electric",
    "status": "Active",
    "startDate": "2024-01-01",
    "endDate": "2025-12-31",
    "manager": "user456",
    "members": [
      {
        "userId": "user123",
        "role": "Engineer"
      }
    ],
    "statistics": {
      "items": 150,
      "documents": 450,
      "workflows": 25
    }
  }
}
```

## Webhook Support

### Register Webhook
```http
POST /webhooks
Content-Type: application/json

{
  "url": "https://your-app.com/webhook",
  "events": ["item.created", "item.released", "workflow.completed"],
  "secret": "your-webhook-secret"
}
```

### Webhook Events
- `item.created` - New item created
- `item.updated` - Item properties updated
- `item.released` - Item released
- `item.deleted` - Item deleted
- `bom.updated` - BOM structure changed
- `workflow.started` - Workflow initiated
- `workflow.task.assigned` - Task assigned
- `workflow.completed` - Workflow completed
- `document.uploaded` - Document uploaded

### Webhook Payload
```json
{
  "event": "item.released",
  "timestamp": "2025-01-15T14:30:00Z",
  "data": {
    "itemId": "SCOOPTRAM-001",
    "revision": "A",
    "releasedBy": "user123"
  },
  "signature": "sha256=..."
}
```

## SDK Examples

### Python
```python
import requests

class TeamcenterAPI:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.session = requests.Session()
        self.authenticate(username, password)
    
    def authenticate(self, username, password):
        response = self.session.post(
            f"{self.base_url}/auth/login",
            json={"username": username, "password": password}
        )
        token = response.json()["token"]
        self.session.headers["Authorization"] = f"Bearer {token}"
    
    def get_item(self, item_id):
        response = self.session.get(f"{self.base_url}/items/{item_id}")
        return response.json()
```

### JavaScript
```javascript
class TeamcenterAPI {
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
    this.token = null;
  }
  
  async authenticate(username, password) {
    const response = await fetch(`${this.baseUrl}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    this.token = data.token;
  }
  
  async getItem(itemId) {
    const response = await fetch(`${this.baseUrl}/items/${itemId}`, {
      headers: { 'Authorization': `Bearer ${this.token}` }
    });
    return response.json();
  }
}
```

### cURL Examples
```bash
# Login
curl -X POST https://teamcenter.epiroc.com/tc/restful/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user@epiroc.com","password":"password"}'

# Get Item
curl -X GET https://teamcenter.epiroc.com/tc/restful/v1/items/SCOOPTRAM-001 \
  -H "Authorization: Bearer {token}"

# Create Item
curl -X POST https://teamcenter.epiroc.com/tc/restful/v1/items \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"itemId":"TEST-001","name":"Test Item","type":"Item"}'
```

## Best Practices

### 1. Pagination
Always use pagination for list operations:
```python
def get_all_items(api, item_type):
    items = []
    page = 1
    while True:
        response = api.get(f"/items?type={item_type}&page={page}&pageSize=100")
        data = response.json()
        items.extend(data["data"])
        if not data["pagination"]["hasNext"]:
            break
        page += 1
    return items
```

### 2. Error Handling
Implement comprehensive error handling:
```python
def safe_api_call(func):
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            if response.status_code == 429:
                # Handle rate limiting
                time.sleep(60)
                return func(*args, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API call failed: {e}")
            raise
    return wrapper
```

### 3. Bulk Operations
Use bulk endpoints when available:
```python
# Instead of multiple single creates
for item in items:
    api.create_item(item)  # Bad

# Use bulk create
api.create_items_bulk(items)  # Good
```

### 4. Caching
Implement caching for frequently accessed data:
```python
from functools import lru_cache
import time

@lru_cache(maxsize=100)
def get_item_cached(item_id, cache_time=300):
    timestamp = int(time.time() / cache_time)
    return api.get_item(item_id)
```

### 5. Async Operations
Use async operations for better performance:
```python
import asyncio
import aiohttp

async def fetch_items_async(item_ids):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_item(session, item_id) for item_id in item_ids]
        return await asyncio.gather(*tasks)
```

## Migration Guide

### From SOAP to REST
```python
# Old SOAP approach
from zeep import Client
client = Client('https://teamcenter.epiroc.com/tc/services?wsdl')
result = client.service.getItem(itemId='ITEM-001')

# New REST approach
import requests
response = requests.get(
    'https://teamcenter.epiroc.com/tc/restful/v1/items/ITEM-001',
    headers={'Authorization': f'Bearer {token}'}
)
result = response.json()
```

## Support

### Documentation
- API Explorer: https://teamcenter.epiroc.com/tc/api-explorer
- OpenAPI Spec: https://teamcenter.epiroc.com/tc/restful/v1/openapi.json
- Postman Collection: https://teamcenter.epiroc.com/tc/restful/v1/postman.json

### Contact
- API Support: api-support@epiroc.com
- Developer Forum: https://developer.epiroc.com/forum

---

© 2025 Murray Kopit. All Rights Reserved.