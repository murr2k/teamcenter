# Teamcenter SOA (Service-Oriented Architecture) Examples

## Table of Contents
- [Overview](#overview)
- [Setup and Configuration](#setup-and-configuration)
- [Java Examples](#java-examples)
- [C# Examples](#c-examples)
- [Python with SOAP](#python-with-soap)
- [Advanced Scenarios](#advanced-scenarios)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

Teamcenter's Service-Oriented Architecture (SOA) provides enterprise-grade web services for complex PLM operations. SOA is ideal for:

- **Transactional operations** requiring ACID compliance
- **Complex business logic** with multiple dependent operations
- **Enterprise integrations** with ERP/MES systems
- **Batch processing** of large datasets
- **Custom business rule enforcement**

### SOA vs REST API

| Feature | SOA | REST API |
|---------|-----|----------|
| Protocol | SOAP/XML | HTTP/JSON |
| Performance | Heavy but robust | Lightweight and fast |
| Transaction Support | Full ACID | Limited |
| Complexity | High | Low |
| Use Case | Enterprise integration | Web/Mobile apps |

## Setup and Configuration

### Java Setup

#### Maven Dependencies
```xml
<dependencies>
    <!-- Teamcenter SOA Client -->
    <dependency>
        <groupId>com.teamcenter</groupId>
        <artifactId>soa-client</artifactId>
        <version>13.3.0</version>
    </dependency>
    
    <!-- Teamcenter Services -->
    <dependency>
        <groupId>com.teamcenter</groupId>
        <artifactId>soa-client-java</artifactId>
        <version>13.3.0</version>
    </dependency>
    
    <!-- Required Libraries -->
    <dependency>
        <groupId>org.apache.axis2</groupId>
        <artifactId>axis2</artifactId>
        <version>1.7.9</version>
    </dependency>
    
    <dependency>
        <groupId>commons-logging</groupId>
        <artifactId>commons-logging</artifactId>
        <version>1.2</version>
    </dependency>
</dependencies>
```

#### Connection Configuration
```java
import com.teamcenter.soa.client.Connection;
import com.teamcenter.soa.client.model.ErrorStack;
import com.teamcenter.soa.common.ObjectPropertyPolicy;

public class TeamcenterConnection {
    private static final String SERVER_URL = "https://teamcenter.epiroc.com/tc";
    private Connection connection;
    
    public void connect(String username, String password) {
        // Create connection
        connection = new Connection(SERVER_URL);
        
        // Set connection options
        connection.setOption(Connection.OPT_USE_COMPRESSION, true);
        connection.setOption(Connection.OPT_CACHE_MODEL_OBJECTS, true);
        
        // Set property policy
        ObjectPropertyPolicy policy = new ObjectPropertyPolicy();
        policy.addType("Item", new String[]{"item_id", "object_name", "object_desc"});
        policy.addType("ItemRevision", new String[]{"item_revision_id", "release_status_list"});
        connection.setObjectPropertyPolicy(policy);
        
        // Login
        SessionService sessionService = SessionService.getService(connection);
        LoginResponse response = sessionService.login(username, password, "", "", "");
        
        if (response.serviceData.sizeOfPartialErrors() > 0) {
            throw new Exception("Login failed: " + 
                response.serviceData.getPartialError(0).getMessage());
        }
    }
}
```

### C# Setup

#### NuGet Packages
```xml
<PackageReference Include="Teamcenter.Soa.Client" Version="13.3.0" />
<PackageReference Include="Teamcenter.Soa.Common" Version="13.3.0" />
<PackageReference Include="Newtonsoft.Json" Version="13.0.1" />
```

#### Connection Configuration
```csharp
using Teamcenter.Soa.Client;
using Teamcenter.Soa.Client.Model;
using Teamcenter.Services.Core;

public class TeamcenterConnection
{
    private const string ServerUrl = "https://teamcenter.epiroc.com/tc";
    private Connection connection;
    
    public async Task ConnectAsync(string username, string password)
    {
        // Create connection
        connection = new Connection(ServerUrl);
        
        // Configure connection
        connection.SetOption(Connection.Options.UseCompression, true);
        connection.SetOption(Connection.Options.CacheModelObjects, true);
        
        // Set up SSL if needed
        ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;
        
        // Login
        var sessionService = SessionService.GetService(connection);
        var response = await sessionService.LoginAsync(username, password, "", "", "");
        
        if (response.ServiceData.PartialErrors.Length > 0)
        {
            throw new Exception($"Login failed: {response.ServiceData.PartialErrors[0].Message}");
        }
    }
}
```

## Java Examples

### Complete Equipment Management System
```java
package com.epiroc.teamcenter.equipment;

import com.teamcenter.soa.client.Connection;
import com.teamcenter.soa.client.model.ModelObject;
import com.teamcenter.soa.client.model.strong.*;
import com.teamcenter.services.strong.core.*;
import com.teamcenter.services.strong.cad.*;
import com.teamcenter.services.strong.query.*;
import java.util.*;

public class EquipmentManager {
    
    private Connection connection;
    private DataManagementService dmService;
    private StructureManagementService structureService;
    private WorkflowService workflowService;
    private QueryService queryService;
    
    public EquipmentManager(Connection connection) {
        this.connection = connection;
        this.dmService = DataManagementService.getService(connection);
        this.structureService = StructureManagementService.getService(connection);
        this.workflowService = WorkflowService.getService(connection);
        this.queryService = QueryService.getService(connection);
    }
    
    /**
     * Create a new mining equipment item with full properties
     */
    public Item createMiningEquipment(String itemId, String name, 
                                     EquipmentType type, Map<String, String> properties) 
                                     throws ServiceException {
        
        // Create item properties
        ItemProperties itemProps = new ItemProperties();
        itemProps.clientId = "create_" + System.currentTimeMillis();
        itemProps.itemId = itemId;
        itemProps.revId = "A";
        itemProps.name = name;
        itemProps.description = properties.get("description");
        itemProps.type = "EPR_MiningEquipment";
        
        // Add extended attributes
        Map<String, VecStruct> extendedData = new HashMap<>();
        
        // Equipment specific properties
        extendedData.put("epr_equipment_type", 
            createVecStruct(type.toString()));
        extendedData.put("epr_model", 
            createVecStruct(properties.get("model")));
        extendedData.put("epr_power_type", 
            createVecStruct(properties.get("powerType")));
        extendedData.put("epr_capacity", 
            createVecStruct(properties.get("capacity")));
        extendedData.put("epr_operating_voltage", 
            createVecStruct(properties.get("voltage")));
        extendedData.put("epr_safety_certification", 
            createVecStruct(properties.get("certification")));
        extendedData.put("epr_manufacture_date", 
            createVecStruct(new Date()));
        extendedData.put("epr_facility", 
            createVecStruct("Pitt Meadows"));
        
        itemProps.extendedData = extendedData;
        
        // Create the item
        CreateItemsResponse response = dmService.createItems(
            new ItemProperties[]{itemProps}, 
            null,  // No custom baseline
            ""     // No relation type
        );
        
        // Check for errors
        if (response.serviceData.sizeOfPartialErrors() > 0) {
            throw new ServiceException(
                "Failed to create equipment: " + 
                response.serviceData.getPartialError(0).getMessage()
            );
        }
        
        Item createdItem = response.output[0].item;
        
        // Set additional properties on the revision
        ItemRevision revision = response.output[0].itemRev;
        setRevisionProperties(revision, properties);
        
        // Attach initial documents if provided
        if (properties.containsKey("specificationPath")) {
            attachDocument(revision, properties.get("specificationPath"), 
                         "IMAN_specification");
        }
        
        return createdItem;
    }
    
    /**
     * Build complete BOM structure for equipment
     */
    public void buildEquipmentBOM(Item parentItem, List<BOMComponent> components) 
                                  throws ServiceException {
        
        // Get latest revision
        ItemRevision parentRev = getLatestRevision(parentItem);
        
        // Create BOM view revision
        PSBOMViewRevision bomViewRev = createBOMViewRevision(parentRev);
        
        // Create BOM window
        CreateBOMWindowsInfo bomInfo = new CreateBOMWindowsInfo();
        bomInfo.itemRev = parentRev;
        
        CreateBOMWindowsResponse windowResponse = 
            structureService.createBOMWindows(new CreateBOMWindowsInfo[]{bomInfo});
        
        BOMWindow bomWindow = windowResponse.output[0].bomWindow;
        BOMLine topLine = windowResponse.output[0].bomLine;
        
        // Add components
        for (BOMComponent component : components) {
            addComponentToBOM(bomWindow, topLine, component);
        }
        
        // Save and close
        structureService.saveBOMWindow(bomWindow);
        structureService.closeBOMWindows(new BOMWindow[]{bomWindow});
    }
    
    /**
     * Add component to BOM with full properties
     */
    private void addComponentToBOM(BOMWindow window, BOMLine parentLine, 
                                  BOMComponent component) throws ServiceException {
        
        // Find or create component item
        Item componentItem = findOrCreateItem(component.itemId, component.name);
        ItemRevision componentRev = getLatestRevision(componentItem);
        
        // Create BOM line
        AddOrUpdateChildrenToParentLineInfo addInfo = 
            new AddOrUpdateChildrenToParentLineInfo();
        addInfo.parentLine = parentLine;
        
        ItemLineInfo lineInfo = new ItemLineInfo();
        lineInfo.itemRev = componentRev;
        
        // Set BOM line properties
        Map<String, String> lineProps = new HashMap<>();
        lineProps.put("bl_quantity", String.valueOf(component.quantity));
        lineProps.put("bl_sequence_no", component.findNumber);
        lineProps.put("bl_uom", component.uom);
        
        // Add custom properties
        if (component.isCritical) {
            lineProps.put("epr_critical_component", "true");
            lineProps.put("epr_failure_impact", component.failureImpact);
        }
        
        lineInfo.lineProperties = lineProps;
        addInfo.itemsToAdd = new ItemLineInfo[]{lineInfo};
        
        // Add to BOM
        AddOrUpdateChildrenToParentLineResponse response = 
            structureService.addOrUpdateChildrenToParentLine(
                new AddOrUpdateChildrenToParentLineInfo[]{addInfo}
            );
        
        if (response.serviceData.sizeOfPartialErrors() > 0) {
            throw new ServiceException(
                "Failed to add component " + component.itemId + ": " + 
                response.serviceData.getPartialError(0).getMessage()
            );
        }
        
        // Recursively add sub-components
        if (component.children != null && !component.children.isEmpty()) {
            BOMLine newLine = response.output[0].newBOMLines[0];
            for (BOMComponent child : component.children) {
                addComponentToBOM(window, newLine, child);
            }
        }
    }
    
    /**
     * Execute complex engineering change process
     */
    public String startEngineeringChange(Item targetItem, 
                                        ChangeRequest changeRequest) 
                                        throws ServiceException {
        
        // Create Problem Report
        ProblemReport pr = createProblemReport(changeRequest);
        
        // Create Engineering Change Request
        ECR ecr = createECR(pr, targetItem, changeRequest);
        
        // Perform impact analysis
        ImpactAnalysis impact = performImpactAnalysis(targetItem, changeRequest);
        
        // Create Engineering Change Notice
        ECN ecn = createECN(ecr, impact, changeRequest);
        
        // Start approval workflow
        WorkflowProcess workflow = startECNWorkflow(ecn, changeRequest);
        
        return workflow.getUid();
    }
    
    /**
     * Perform comprehensive impact analysis
     */
    private ImpactAnalysis performImpactAnalysis(Item item, 
                                                ChangeRequest request) 
                                                throws ServiceException {
        
        ImpactAnalysis analysis = new ImpactAnalysis();
        
        // Find where-used
        WhereUsedResponse whereUsed = structureService.whereUsed(
            new ModelObject[]{item},
            1,  // levels
            new WhereUsedConfigParameters()
        );
        
        analysis.affectedParents = Arrays.asList(whereUsed.output[0].parents);
        
        // Check for released items
        for (ModelObject parent : analysis.affectedParents) {
            if (isReleased(parent)) {
                analysis.hasReleasedParents = true;
                analysis.releasedItems.add(parent);
            }
        }
        
        // Estimate cost impact
        if (request.changeType == ChangeType.MAJOR) {
            analysis.estimatedCost = calculateMajorChangeCost(item);
            analysis.estimatedHours = 120;
        } else {
            analysis.estimatedCost = calculateMinorChangeCost(item);
            analysis.estimatedHours = 40;
        }
        
        // Check compliance impact
        analysis.complianceImpact = checkComplianceImpact(item, request);
        
        return analysis;
    }
    
    /**
     * Advanced query for equipment
     */
    public List<Item> findEquipmentBySpecs(EquipmentType type, 
                                          Map<String, String> specifications) 
                                          throws ServiceException {
        
        // Build query criteria
        QueryInput queryInput = new QueryInput();
        queryInput.query = getQuery("EPR_Equipment_Search");
        queryInput.maxNumToReturn = 100;
        queryInput.limitList = new ModelObject[0];
        queryInput.entries = new String[specifications.size() + 1];
        queryInput.values = new String[specifications.size() + 1];
        
        // Add equipment type
        queryInput.entries[0] = "Equipment Type";
        queryInput.values[0] = type.toString();
        
        // Add specifications
        int index = 1;
        for (Map.Entry<String, String> spec : specifications.entrySet()) {
            queryInput.entries[index] = spec.getKey();
            queryInput.values[index] = spec.getValue();
            index++;
        }
        
        // Execute query
        SavedQueriesResponse response = queryService.executeSavedQueries(
            new QueryInput[]{queryInput}
        );
        
        if (response.serviceData.sizeOfPartialErrors() > 0) {
            throw new ServiceException(
                "Query failed: " + 
                response.serviceData.getPartialError(0).getMessage()
            );
        }
        
        // Extract items
        List<Item> items = new ArrayList<>();
        for (ModelObject obj : response.arrayOfResults[0]) {
            if (obj instanceof Item) {
                items.add((Item) obj);
            }
        }
        
        return items;
    }
    
    /**
     * Batch update equipment properties
     */
    public void batchUpdateEquipment(List<Item> items, 
                                    Map<String, String> updates) 
                                    throws ServiceException {
        
        // Begin transaction
        TransactionService txService = TransactionService.getService(connection);
        txService.beginTransaction();
        
        try {
            for (Item item : items) {
                // Get latest revision
                ItemRevision revision = getLatestRevision(item);
                
                // Prepare property updates
                PropertyNameValue[] props = 
                    new PropertyNameValue[updates.size()];
                
                int i = 0;
                for (Map.Entry<String, String> entry : updates.entrySet()) {
                    PropertyNameValue prop = new PropertyNameValue();
                    prop.name = entry.getKey();
                    prop.values = new String[]{entry.getValue()};
                    props[i++] = prop;
                }
                
                // Update properties
                dmService.setProperties(
                    new ModelObject[]{revision}, 
                    props
                );
            }
            
            // Commit transaction
            txService.commitTransaction();
            
        } catch (Exception e) {
            // Rollback on error
            txService.rollbackTransaction();
            throw new ServiceException("Batch update failed: " + e.getMessage());
        }
    }
    
    // Helper classes
    public static class BOMComponent {
        public String itemId;
        public String name;
        public int quantity;
        public String findNumber;
        public String uom = "each";
        public boolean isCritical;
        public String failureImpact;
        public List<BOMComponent> children;
    }
    
    public static class ChangeRequest {
        public String title;
        public String description;
        public ChangeType changeType;
        public String justification;
        public Map<String, String> impacts;
        public List<String> reviewers;
        public List<String> approvers;
    }
    
    public static class ImpactAnalysis {
        public List<ModelObject> affectedParents = new ArrayList<>();
        public List<ModelObject> releasedItems = new ArrayList<>();
        public boolean hasReleasedParents = false;
        public double estimatedCost;
        public int estimatedHours;
        public ComplianceImpact complianceImpact;
    }
    
    public enum EquipmentType {
        UNDERGROUND_LOADER,
        SURFACE_DRILL_RIG,
        ROCK_BREAKER,
        BOLTING_RIG
    }
    
    public enum ChangeType {
        MINOR, MAJOR, CRITICAL
    }
    
    public enum ComplianceImpact {
        NONE, LOW, MEDIUM, HIGH
    }
}
```

## C# Examples

### Complete Mining Equipment Integration
```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Linq;
using Teamcenter.Soa.Client;
using Teamcenter.Soa.Client.Model;
using Teamcenter.Soa.Client.Model.Strong;
using Teamcenter.Services.Strong.Core;
using Teamcenter.Services.Strong.Cad;
using Teamcenter.Services.Strong.Workflow;

namespace Epiroc.Teamcenter.Integration
{
    public class MiningEquipmentService
    {
        private readonly Connection connection;
        private readonly DataManagementService dmService;
        private readonly StructureManagementService structureService;
        private readonly WorkflowService workflowService;
        
        public MiningEquipmentService(Connection connection)
        {
            this.connection = connection;
            this.dmService = DataManagementService.GetService(connection);
            this.structureService = StructureManagementService.GetService(connection);
            this.workflowService = WorkflowService.GetService(connection);
        }
        
        /// <summary>
        /// Create battery-electric loader with full specifications
        /// </summary>
        public async Task<Item> CreateBatteryLoaderAsync(LoaderSpecification spec)
        {
            // Prepare item creation
            var itemProps = new ItemProperties
            {
                ClientId = $"create_{DateTime.Now.Ticks}",
                ItemId = spec.ItemId,
                RevId = "A",
                Name = spec.Name,
                Description = spec.Description,
                Type = "EPR_BatteryLoader"
            };
            
            // Add battery-specific properties
            var extendedData = new Dictionary<string, VecStruct>
            {
                ["epr_model"] = CreateVecStruct(spec.Model),
                ["epr_battery_type"] = CreateVecStruct("Lithium-Ion"),
                ["epr_battery_voltage"] = CreateVecStruct($"{spec.BatteryVoltage}V"),
                ["epr_battery_capacity"] = CreateVecStruct($"{spec.BatteryCapacity} kWh"),
                ["epr_charging_time"] = CreateVecStruct($"{spec.ChargingTime} minutes"),
                ["epr_operating_time"] = CreateVecStruct($"{spec.OperatingHours} hours"),
                ["epr_regenerative_braking"] = CreateVecStruct(spec.HasRegenerativeBraking),
                ["epr_fast_charging"] = CreateVecStruct(spec.SupportsFastCharging),
                ["epr_battery_management_system"] = CreateVecStruct("Advanced BMS v3.0"),
                ["epr_thermal_management"] = CreateVecStruct(spec.ThermalManagement),
                ["epr_safety_features"] = CreateVecStruct(string.Join(", ", spec.SafetyFeatures))
            };
            
            itemProps.ExtendedData = extendedData;
            
            // Create item
            var response = await dmService.CreateItemsAsync(
                new[] { itemProps },
                null,
                string.Empty
            );
            
            if (response.ServiceData.PartialErrors.Length > 0)
            {
                throw new Exception($"Failed to create loader: {response.ServiceData.PartialErrors[0].Message}");
            }
            
            var item = response.Output[0].Item;
            var revision = response.Output[0].ItemRev;
            
            // Set additional revision properties
            await SetBatterySpecificPropertiesAsync(revision, spec);
            
            // Create battery system BOM
            await CreateBatterySystemBOMAsync(item, spec.BatteryConfiguration);
            
            // Attach compliance documents
            await AttachComplianceDocumentsAsync(revision, spec.ComplianceDocuments);
            
            return item;
        }
        
        /// <summary>
        /// Create complete battery system BOM structure
        /// </summary>
        private async Task CreateBatterySystemBOMAsync(Item loader, 
                                                       BatteryConfiguration config)
        {
            var components = new List<BOMLineCreation>();
            
            // Battery modules
            for (int i = 0; i < config.ModuleCount; i++)
            {
                components.Add(new BOMLineCreation
                {
                    ItemId = $"BATTERY-MODULE-{config.ModuleType}",
                    Name = $"Battery Module {config.ModuleVoltage}V {config.ModuleCapacity}Ah",
                    Quantity = 1,
                    FindNumber = $"{(i + 1) * 10}",
                    Properties = new Dictionary<string, string>
                    {
                        ["epr_module_position"] = $"Position {i + 1}",
                        ["epr_module_serial"] = $"MOD-{DateTime.Now:yyyyMMdd}-{i:000}",
                        ["epr_critical_component"] = "true",
                        ["epr_replacement_interval"] = "5 years"
                    }
                });
            }
            
            // Battery Management System
            components.Add(new BOMLineCreation
            {
                ItemId = "BMS-ADVANCED-V3",
                Name = "Battery Management System V3",
                Quantity = 1,
                FindNumber = "100",
                Properties = new Dictionary<string, string>
                {
                    ["epr_software_version"] = "3.2.1",
                    ["epr_can_bus_compatible"] = "true",
                    ["epr_remote_monitoring"] = "enabled"
                }
            });
            
            // Thermal Management System
            components.Add(new BOMLineCreation
            {
                ItemId = "THERMAL-MGMT-LIQUID",
                Name = "Liquid Cooling System",
                Quantity = 1,
                FindNumber = "200",
                Properties = new Dictionary<string, string>
                {
                    ["epr_cooling_capacity"] = "15 kW",
                    ["epr_coolant_type"] = "Glycol-Water 50/50",
                    ["epr_pump_redundancy"] = "Dual"
                }
            });
            
            // Power Distribution Unit
            components.Add(new BOMLineCreation
            {
                ItemId = "PDU-HIGH-VOLTAGE",
                Name = "High Voltage Power Distribution Unit",
                Quantity = 1,
                FindNumber = "300",
                Properties = new Dictionary<string, string>
                {
                    ["epr_max_voltage"] = "800V DC",
                    ["epr_max_current"] = "500A",
                    ["epr_safety_rating"] = "IP67"
                }
            });
            
            await AddComponentsToBOMAsync(loader, components);
        }
        
        /// <summary>
        /// Perform comprehensive compliance check
        /// </summary>
        public async Task<ComplianceReport> CheckEquipmentComplianceAsync(string itemId)
        {
            var report = new ComplianceReport
            {
                ItemId = itemId,
                CheckDate = DateTime.Now,
                ComplianceStatus = ComplianceStatus.Compliant
            };
            
            // Get item and its documents
            var item = await GetItemAsync(itemId);
            var documents = await GetItemDocumentsAsync(item);
            
            // Define required compliance documents for battery equipment
            var requiredDocs = new Dictionary<string, ComplianceRequirement>
            {
                ["MSHA_Certification"] = new ComplianceRequirement
                {
                    DocumentType = "MSHA_CERT",
                    ValidityDays = 365,
                    IsCritical = true,
                    RegulatoryBody = "Mine Safety and Health Administration"
                },
                ["Battery_UN38.3"] = new ComplianceRequirement
                {
                    DocumentType = "UN38_3_TEST",
                    ValidityDays = 730,
                    IsCritical = true,
                    RegulatoryBody = "United Nations"
                },
                ["CE_Declaration"] = new ComplianceRequirement
                {
                    DocumentType = "CE_DOC",
                    ValidityDays = 1095,
                    IsCritical = true,
                    RegulatoryBody = "European Union"
                },
                ["UL_Certification"] = new ComplianceRequirement
                {
                    DocumentType = "UL_CERT",
                    ValidityDays = 365,
                    IsCritical = false,
                    RegulatoryBody = "Underwriters Laboratories"
                },
                ["Battery_MSDS"] = new ComplianceRequirement
                {
                    DocumentType = "MSDS",
                    ValidityDays = 365,
                    IsCritical = true,
                    RegulatoryBody = "OSHA"
                },
                ["Thermal_Runaway_Test"] = new ComplianceRequirement
                {
                    DocumentType = "THERMAL_TEST",
                    ValidityDays = 730,
                    IsCritical = true,
                    RegulatoryBody = "Internal"
                }
            };
            
            // Check each requirement
            foreach (var requirement in requiredDocs)
            {
                var checkResult = new ComplianceCheck
                {
                    RequirementName = requirement.Key,
                    RequiredType = requirement.Value.DocumentType,
                    IsCritical = requirement.Value.IsCritical,
                    RegulatoryBody = requirement.Value.RegulatoryBody
                };
                
                // Find matching document
                var doc = documents.FirstOrDefault(d => 
                    d.Type == requirement.Value.DocumentType);
                
                if (doc == null)
                {
                    checkResult.Status = DocumentStatus.Missing;
                    checkResult.Message = $"{requirement.Key} not found";
                    
                    if (requirement.Value.IsCritical)
                    {
                        report.ComplianceStatus = ComplianceStatus.NonCompliant;
                        report.CriticalIssues.Add(checkResult.Message);
                    }
                }
                else
                {
                    // Check validity
                    var age = (DateTime.Now - doc.CreatedDate).Days;
                    
                    if (age > requirement.Value.ValidityDays)
                    {
                        checkResult.Status = DocumentStatus.Expired;
                        checkResult.Message = $"{requirement.Key} expired on {doc.CreatedDate.AddDays(requirement.Value.ValidityDays):yyyy-MM-dd}";
                        checkResult.ExpiryDate = doc.CreatedDate.AddDays(requirement.Value.ValidityDays);
                        
                        if (requirement.Value.IsCritical)
                        {
                            report.ComplianceStatus = ComplianceStatus.NonCompliant;
                            report.CriticalIssues.Add(checkResult.Message);
                        }
                    }
                    else if (age > requirement.Value.ValidityDays - 30)
                    {
                        checkResult.Status = DocumentStatus.ExpiringSoon;
                        checkResult.Message = $"{requirement.Key} expires in {requirement.Value.ValidityDays - age} days";
                        checkResult.ExpiryDate = doc.CreatedDate.AddDays(requirement.Value.ValidityDays);
                        
                        if (report.ComplianceStatus == ComplianceStatus.Compliant)
                        {
                            report.ComplianceStatus = ComplianceStatus.Warning;
                        }
                        report.Warnings.Add(checkResult.Message);
                    }
                    else
                    {
                        checkResult.Status = DocumentStatus.Valid;
                        checkResult.Message = "Valid";
                        checkResult.ValidUntil = doc.CreatedDate.AddDays(requirement.Value.ValidityDays);
                    }
                    
                    checkResult.DocumentId = doc.Id;
                    checkResult.LastUpdated = doc.ModifiedDate;
                }
                
                report.Checks.Add(checkResult);
            }
            
            // Generate recommendations
            if (report.ComplianceStatus != ComplianceStatus.Compliant)
            {
                report.Recommendations = GenerateComplianceRecommendations(report);
            }
            
            return report;
        }
        
        /// <summary>
        /// Smart workflow orchestration for ECN
        /// </summary>
        public async Task<WorkflowOrchestration> OrchestrateECNWorkflowAsync(
            ECNRequest request)
        {
            var orchestration = new WorkflowOrchestration
            {
                RequestId = Guid.NewGuid().ToString(),
                StartTime = DateTime.Now
            };
            
            // Phase 1: Impact Analysis
            var impactPhase = new WorkflowPhase { Name = "Impact Analysis" };
            
            var impactAnalysis = await PerformImpactAnalysisAsync(request.TargetItems);
            impactPhase.Results["AffectedItems"] = impactAnalysis.AffectedItems.Count;
            impactPhase.Results["EstimatedCost"] = impactAnalysis.EstimatedCost;
            impactPhase.Results["ComplianceImpact"] = impactAnalysis.ComplianceImpact;
            
            orchestration.Phases.Add(impactPhase);
            
            // Phase 2: Automated Approvals
            var approvalPhase = new WorkflowPhase { Name = "Automated Approvals" };
            
            // Auto-approve minor changes
            if (impactAnalysis.ChangeLevel == ChangeLevel.Minor && 
                impactAnalysis.ComplianceImpact == ComplianceImpact.None)
            {
                approvalPhase.AutoApproved = true;
                approvalPhase.Results["AutoApprovalReason"] = "Minor change with no compliance impact";
            }
            else
            {
                // Route to appropriate approvers based on impact
                var approvers = DetermineApprovers(impactAnalysis);
                approvalPhase.Results["RequiredApprovers"] = approvers;
                
                // Create approval tasks
                foreach (var approver in approvers)
                {
                    await CreateApprovalTaskAsync(request, approver, impactAnalysis);
                }
            }
            
            orchestration.Phases.Add(approvalPhase);
            
            // Phase 3: Implementation Planning
            var planningPhase = new WorkflowPhase { Name = "Implementation Planning" };
            
            if (impactAnalysis.RequiresTesting)
            {
                planningPhase.Results["TestPlan"] = await GenerateTestPlanAsync(request);
            }
            
            if (impactAnalysis.RequiresTraining)
            {
                planningPhase.Results["TrainingPlan"] = await GenerateTrainingPlanAsync(request);
            }
            
            orchestration.Phases.Add(planningPhase);
            
            // Phase 4: Change Execution
            var executionPhase = new WorkflowPhase { Name = "Change Execution" };
            
            // Schedule implementation
            var schedule = await ScheduleImplementationAsync(request, impactAnalysis);
            executionPhase.Results["ScheduledDate"] = schedule.ImplementationDate;
            executionPhase.Results["EstimatedDuration"] = schedule.EstimatedHours;
            
            orchestration.Phases.Add(executionPhase);
            
            // Start the workflow
            var workflowId = await StartWorkflowAsync(orchestration);
            orchestration.WorkflowId = workflowId;
            
            return orchestration;
        }
        
        // Supporting classes
        public class LoaderSpecification
        {
            public string ItemId { get; set; }
            public string Name { get; set; }
            public string Description { get; set; }
            public string Model { get; set; }
            public int BatteryVoltage { get; set; }
            public int BatteryCapacity { get; set; }
            public int ChargingTime { get; set; }
            public int OperatingHours { get; set; }
            public bool HasRegenerativeBraking { get; set; }
            public bool SupportsFastCharging { get; set; }
            public string ThermalManagement { get; set; }
            public List<string> SafetyFeatures { get; set; }
            public BatteryConfiguration BatteryConfiguration { get; set; }
            public List<string> ComplianceDocuments { get; set; }
        }
        
        public class BatteryConfiguration
        {
            public int ModuleCount { get; set; }
            public string ModuleType { get; set; }
            public int ModuleVoltage { get; set; }
            public int ModuleCapacity { get; set; }
            public string ConnectionType { get; set; }
            public string CoolingType { get; set; }
        }
        
        public class ComplianceReport
        {
            public string ItemId { get; set; }
            public DateTime CheckDate { get; set; }
            public ComplianceStatus ComplianceStatus { get; set; }
            public List<ComplianceCheck> Checks { get; set; } = new List<ComplianceCheck>();
            public List<string> CriticalIssues { get; set; } = new List<string>();
            public List<string> Warnings { get; set; } = new List<string>();
            public List<string> Recommendations { get; set; } = new List<string>();
        }
        
        public class ComplianceCheck
        {
            public string RequirementName { get; set; }
            public string RequiredType { get; set; }
            public bool IsCritical { get; set; }
            public string RegulatoryBody { get; set; }
            public DocumentStatus Status { get; set; }
            public string Message { get; set; }
            public string DocumentId { get; set; }
            public DateTime? ExpiryDate { get; set; }
            public DateTime? ValidUntil { get; set; }
            public DateTime? LastUpdated { get; set; }
        }
        
        public enum ComplianceStatus
        {
            Compliant,
            Warning,
            NonCompliant
        }
        
        public enum DocumentStatus
        {
            Valid,
            ExpiringSoon,
            Expired,
            Missing
        }
    }
}
```

## Python with SOAP

### Using Zeep for SOA Integration
```python
from zeep import Client, Settings, Transport
from zeep.wsse.username import UsernameToken
from zeep.plugins import HistoryPlugin
from requests import Session
from requests.auth import HTTPBasicAuth
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TeamcenterSOAClient:
    """
    Python SOA client for Teamcenter using Zeep
    Optimized for mining equipment operations
    """
    
    def __init__(self, wsdl_url: str, username: str, password: str):
        """
        Initialize SOA client with authentication
        """
        # Setup session with authentication
        session = Session()
        session.auth = HTTPBasicAuth(username, password)
        
        # Configure transport with session
        transport = Transport(session=session, timeout=30, operation_timeout=60)
        
        # Setup SOAP settings
        settings = Settings(
            strict=False,
            xml_huge_tree=True,
            raw_response=False
        )
        
        # History plugin for debugging
        self.history = HistoryPlugin()
        
        # Create client
        self.client = Client(
            wsdl=wsdl_url,
            transport=transport,
            settings=settings,
            plugins=[self.history]
        )
        
        # Get services
        self.service = self.client.service
        self.factory = self.client.type_factory('ns0')
        
        # Authenticate
        self._authenticate(username, password)
        
    def _authenticate(self, username: str, password: str):
        """
        Perform SOA authentication
        """
        try:
            response = self.service.login(
                username=username,
                password=password,
                group="",
                role="",
                locale=""
            )
            
            if response.serviceData.partialErrors:
                raise Exception(f"Login failed: {response.serviceData.partialErrors[0].message}")
                
            self.session_id = response.sessionId
            logger.info(f"Successfully authenticated as {username}")
            
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            raise
    
    def create_mining_equipment(self, equipment_data: Dict[str, Any]) -> str:
        """
        Create mining equipment with full specifications
        """
        try:
            # Create item properties
            item_props = self.factory.ItemProperties(
                clientId=f"create_{datetime.now().timestamp()}",
                itemId=equipment_data['item_id'],
                revId="A",
                name=equipment_data['name'],
                description=equipment_data.get('description', ''),
                type="EPR_MiningEquipment"
            )
            
            # Add extended attributes
            extended_data = {}
            
            # Equipment properties
            equipment_props = equipment_data.get('properties', {})
            for key, value in equipment_props.items():
                extended_data[f"epr_{key}"] = self.factory.VecStruct(
                    stringVec=[str(value)]
                )
            
            # Add facility
            extended_data['epr_facility'] = self.factory.VecStruct(
                stringVec=['Pitt Meadows']
            )
            
            # Add manufacture date
            extended_data['epr_manufacture_date'] = self.factory.VecStruct(
                stringVec=[datetime.now().isoformat()]
            )
            
            item_props.extendedData = extended_data
            
            # Create the item
            response = self.service.createItems(
                properties=[item_props],
                baseline=None,
                relationType=""
            )
            
            if response.serviceData.partialErrors:
                raise Exception(f"Failed to create equipment: {response.serviceData.partialErrors[0].message}")
            
            created_item = response.output[0].item
            logger.info(f"Created equipment: {created_item.itemId}")
            
            return created_item.uid
            
        except Exception as e:
            logger.error(f"Failed to create equipment: {e}")
            raise
    
    def build_equipment_bom(self, parent_item_id: str, components: List[Dict]) -> bool:
        """
        Build BOM structure for equipment
        """
        try:
            # Get parent item
            parent_item = self.get_item(parent_item_id)
            parent_rev = self.get_latest_revision(parent_item)
            
            # Create BOM window
            bom_window_info = self.factory.CreateBOMWindowsInfo(
                itemRev=parent_rev
            )
            
            window_response = self.service.createBOMWindows([bom_window_info])
            
            if window_response.serviceData.partialErrors:
                raise Exception(f"Failed to create BOM window: {window_response.serviceData.partialErrors[0].message}")
            
            bom_window = window_response.output[0].bomWindow
            top_line = window_response.output[0].bomLine
            
            # Add components
            for component in components:
                self._add_component_to_bom(bom_window, top_line, component)
            
            # Save and close
            self.service.saveBOMWindow(bom_window)
            self.service.closeBOMWindows([bom_window])
            
            logger.info(f"Successfully built BOM for {parent_item_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to build BOM: {e}")
            raise
    
    def _add_component_to_bom(self, window, parent_line, component: Dict):
        """
        Add single component to BOM
        """
        # Find or create component
        comp_item = self.find_or_create_item(
            component['item_id'],
            component['name']
        )
        comp_rev = self.get_latest_revision(comp_item)
        
        # Create line info
        line_info = self.factory.ItemLineInfo(
            itemRev=comp_rev
        )
        
        # Set line properties
        line_props = {
            'bl_quantity': str(component.get('quantity', 1)),
            'bl_sequence_no': component.get('find_number', ''),
            'bl_uom': component.get('uom', 'each')
        }
        
        # Add custom properties
        if component.get('is_critical'):
            line_props['epr_critical_component'] = 'true'
        
        line_info.lineProperties = line_props
        
        # Add to parent
        add_info = self.factory.AddOrUpdateChildrenToParentLineInfo(
            parentLine=parent_line,
            itemsToAdd=[line_info]
        )
        
        response = self.service.addOrUpdateChildrenToParentLine([add_info])
        
        if response.serviceData.partialErrors:
            raise Exception(f"Failed to add component {component['item_id']}: {response.serviceData.partialErrors[0].message}")
        
        # Recursively add children
        if 'children' in component:
            new_line = response.output[0].newBOMLines[0]
            for child in component['children']:
                self._add_component_to_bom(window, new_line, child)
    
    def execute_saved_query(self, query_name: str, parameters: Dict[str, str]) -> List[Dict]:
        """
        Execute a saved query with parameters
        """
        try:
            # Get the query
            query = self.get_query(query_name)
            
            # Build query input
            query_input = self.factory.QueryInput(
                query=query,
                maxNumToReturn=100,
                limitList=[],
                entries=list(parameters.keys()),
                values=list(parameters.values())
            )
            
            # Execute query
            response = self.service.executeSavedQueries([query_input])
            
            if response.serviceData.partialErrors:
                raise Exception(f"Query failed: {response.serviceData.partialErrors[0].message}")
            
            # Process results
            results = []
            for obj in response.arrayOfResults[0]:
                results.append({
                    'uid': obj.uid,
                    'type': obj.type,
                    'properties': self._get_object_properties(obj)
                })
            
            logger.info(f"Query '{query_name}' returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def start_ecn_workflow(self, target_item_id: str, change_data: Dict) -> str:
        """
        Start Engineering Change Notice workflow
        """
        try:
            # Get target item
            target_item = self.get_item(target_item_id)
            
            # Create ECN
            ecn_props = self.factory.ECNProperties(
                clientId=f"ecn_{datetime.now().timestamp()}",
                name=change_data['title'],
                description=change_data['description'],
                priority=change_data.get('priority', 'Normal'),
                targetItems=[target_item]
            )
            
            # Add change details
            ecn_props.changeType = change_data.get('change_type', 'Design Change')
            ecn_props.justification = change_data.get('justification', '')
            ecn_props.impactAnalysis = change_data.get('impact_analysis', '')
            
            # Create ECN
            ecn_response = self.service.createECN(ecn_props)
            
            if ecn_response.serviceData.partialErrors:
                raise Exception(f"Failed to create ECN: {ecn_response.serviceData.partialErrors[0].message}")
            
            ecn = ecn_response.ecn
            
            # Start workflow
            workflow_props = self.factory.WorkflowProperties(
                processTemplate="EPR_ECN_Process",
                name=f"ECN Workflow - {change_data['title']}",
                targets=[ecn],
                attachments=[target_item]
            )
            
            # Add participants
            if 'reviewers' in change_data:
                workflow_props.reviewers = change_data['reviewers']
            
            if 'approvers' in change_data:
                workflow_props.approvers = change_data['approvers']
            
            # Start the workflow
            workflow_response = self.service.startWorkflow(workflow_props)
            
            if workflow_response.serviceData.partialErrors:
                raise Exception(f"Failed to start workflow: {workflow_response.serviceData.partialErrors[0].message}")
            
            workflow_id = workflow_response.workflowId
            logger.info(f"Started ECN workflow: {workflow_id}")
            
            return workflow_id
            
        except Exception as e:
            logger.error(f"Failed to start ECN workflow: {e}")
            raise
    
    def check_compliance(self, item_id: str) -> Dict:
        """
        Check equipment compliance status
        """
        try:
            # Get item and its documents
            item = self.get_item(item_id)
            documents = self.get_item_documents(item)
            
            # Define required documents
            required_docs = {
                'MSHA_Certification': {'validity_days': 365, 'critical': True},
                'CE_Declaration': {'validity_days': 730, 'critical': True},
                'Battery_Safety_Report': {'validity_days': 90, 'critical': True},
                'Electrical_Safety_Test': {'validity_days': 180, 'critical': False}
            }
            
            compliance_status = {
                'item_id': item_id,
                'compliant': True,
                'issues': [],
                'warnings': [],
                'documents': {}
            }
            
            # Check each required document
            for doc_type, requirements in required_docs.items():
                found = False
                
                for doc in documents:
                    if doc.type == doc_type:
                        found = True
                        # Check validity
                        age_days = (datetime.now() - doc.created_date).days
                        
                        if age_days > requirements['validity_days']:
                            issue = f"{doc_type} expired"
                            if requirements['critical']:
                                compliance_status['compliant'] = False
                                compliance_status['issues'].append(issue)
                            else:
                                compliance_status['warnings'].append(issue)
                        elif age_days > requirements['validity_days'] - 30:
                            compliance_status['warnings'].append(
                                f"{doc_type} expires soon"
                            )
                        
                        compliance_status['documents'][doc_type] = {
                            'status': 'valid' if age_days <= requirements['validity_days'] else 'expired',
                            'age_days': age_days,
                            'document_id': doc.uid
                        }
                        break
                
                if not found:
                    issue = f"{doc_type} missing"
                    if requirements['critical']:
                        compliance_status['compliant'] = False
                        compliance_status['issues'].append(issue)
                    else:
                        compliance_status['warnings'].append(issue)
                    
                    compliance_status['documents'][doc_type] = {
                        'status': 'missing'
                    }
            
            return compliance_status
            
        except Exception as e:
            logger.error(f"Compliance check failed: {e}")
            raise
    
    def get_last_soap_request(self) -> str:
        """
        Get the last SOAP request for debugging
        """
        if self.history.last_sent:
            from lxml import etree
            return etree.tostring(
                self.history.last_sent['envelope'],
                encoding='unicode',
                pretty_print=True
            )
        return None
    
    def get_last_soap_response(self) -> str:
        """
        Get the last SOAP response for debugging
        """
        if self.history.last_received:
            from lxml import etree
            return etree.tostring(
                self.history.last_received['envelope'],
                encoding='unicode',
                pretty_print=True
            )
        return None


# Example usage
if __name__ == "__main__":
    # Initialize client
    client = TeamcenterSOAClient(
        wsdl_url="https://teamcenter.epiroc.com/tc/services/Core-2011-06-Session?wsdl",
        username="user@epiroc.com",
        password="password"
    )
    
    # Create equipment
    equipment_data = {
        'item_id': 'LOADER-001',
        'name': 'Scooptram ST1030 Battery',
        'description': '10-tonne battery-electric loader',
        'properties': {
            'equipment_type': 'Underground Loader',
            'model': 'ST1030',
            'power_type': 'Battery Electric',
            'voltage': '650V',
            'capacity': '10 tonnes'
        }
    }
    
    equipment_uid = client.create_mining_equipment(equipment_data)
    
    # Build BOM
    components = [
        {
            'item_id': 'BATTERY-PACK-650V',
            'name': 'Battery Pack System',
            'quantity': 1,
            'is_critical': True,
            'children': [
                {
                    'item_id': 'BATTERY-MODULE-001',
                    'name': 'Battery Module',
                    'quantity': 8
                }
            ]
        },
        {
            'item_id': 'BMS-V3',
            'name': 'Battery Management System',
            'quantity': 1,
            'is_critical': True
        }
    ]
    
    client.build_equipment_bom(equipment_uid, components)
    
    # Check compliance
    compliance = client.check_compliance(equipment_uid)
    print(f"Compliance status: {compliance}")
```

## Advanced Scenarios

### Multi-Site Synchronization
```java
public class MultiSiteSync {
    
    public void synchronizeEquipmentAcrossSites(List<String> sites) {
        // Implementation for synchronizing equipment data across
        // multiple Teamcenter sites (Sweden, Canada, etc.)
    }
}
```

### Predictive Maintenance Integration
```csharp
public class PredictiveMaintenanceService {
    
    public async Task IntegrateIoTDataAsync(string equipmentId, IoTSensorData data) {
        // Integration with IoT sensors on mining equipment
        // for predictive maintenance
    }
}
```

## Best Practices

### 1. Connection Pooling
```java
public class ConnectionPool {
    private static final int MAX_CONNECTIONS = 10;
    private final Queue<Connection> pool = new LinkedList<>();
    
    public synchronized Connection getConnection() {
        if (pool.isEmpty()) {
            return createNewConnection();
        }
        return pool.poll();
    }
    
    public synchronized void returnConnection(Connection conn) {
        if (pool.size() < MAX_CONNECTIONS) {
            pool.offer(conn);
        }
    }
}
```

### 2. Transaction Management
```java
public void performTransactionalOperation() {
    TransactionService txService = TransactionService.getService(connection);
    
    try {
        txService.beginTransaction();
        // Perform operations
        txService.commitTransaction();
    } catch (Exception e) {
        txService.rollbackTransaction();
        throw e;
    }
}
```

### 3. Error Handling
```csharp
public class ServiceExceptionHandler {
    
    public static void HandleServiceErrors(ServiceData serviceData) {
        if (serviceData.PartialErrors.Length > 0) {
            var errors = serviceData.PartialErrors
                .Select(e => $"{e.ErrorCode}: {e.Message}")
                .ToList();
            
            throw new AggregateException(
                "Service operation failed",
                errors.Select(e => new Exception(e))
            );
        }
    }
}
```

## Troubleshooting

### Common Issues

#### 1. Connection Timeout
```java
// Increase timeout
connection.setOption(Connection.OPT_REQUEST_TIMEOUT, 120000); // 2 minutes
```

#### 2. Large Dataset Handling
```java
// Use pagination
QueryOptions options = new QueryOptions();
options.setMaxResults(100);
options.setStartIndex(0);
```

#### 3. Memory Issues
```java
// Clear cache periodically
connection.getModelManager().clearCache();
```

## Support

For additional SOA examples and support:
- Siemens GTAC: https://support.sw.siemens.com
- API Documentation: Available in Teamcenter installation
- Community Forum: https://community.sw.siemens.com

---

© 2025 Murray Kopit. All Rights Reserved.