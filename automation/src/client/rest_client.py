"""
Teamcenter REST API Client Implementation
"""

import requests
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from urllib.parse import urljoin
import time

logger = logging.getLogger(__name__)


class TeamcenterRESTClient:
    """
    REST API Client for Teamcenter PLM System
    Optimized for mining equipment operations at Epiroc
    """
    
    def __init__(self, base_url: str, username: str = None, password: str = None):
        """
        Initialize Teamcenter REST client
        
        Args:
            base_url: Base URL for Teamcenter instance
            username: Username for authentication
            password: Password for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.token = None
        self.token_expiry = None
        
        # Configure session
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        if username and password:
            self.authenticate(username, password)
    
    def authenticate(self, username: str, password: str) -> Dict:
        """
        Authenticate with Teamcenter and obtain session token
        
        Args:
            username: Teamcenter username
            password: Teamcenter password
            
        Returns:
            Authentication response with token
        """
        auth_url = urljoin(self.base_url, '/restful/auth/login')
        
        try:
            response = self.session.post(
                auth_url,
                json={
                    'username': username,
                    'password': password
                },
                timeout=30
            )
            response.raise_for_status()
            
            auth_data = response.json()
            self.token = auth_data.get('token')
            
            # Calculate token expiry (usually 1 hour)
            self.token_expiry = datetime.now() + timedelta(hours=1)
            
            # Update session headers with token
            self.session.headers.update({
                'Authorization': f'Bearer {self.token}'
            })
            
            logger.info(f"Successfully authenticated as {username}")
            return auth_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Authentication failed: {str(e)}")
            raise
    
    def ensure_authenticated(self):
        """Ensure the client is authenticated and token is valid"""
        if not self.token:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        # Check token expiry and refresh if needed
        if self.token_expiry and datetime.now() >= self.token_expiry:
            logger.info("Token expired, refreshing...")
            # In real implementation, would refresh token
            raise Exception("Token expired. Re-authenticate required.")
    
    # ==================== Item Operations ====================
    
    def create_item(self, item_data: Dict) -> Dict:
        """
        Create a new item in Teamcenter
        
        Args:
            item_data: Dictionary containing item properties
            
        Returns:
            Created item data
        """
        self.ensure_authenticated()
        
        url = urljoin(self.base_url, '/restful/items')
        
        # Add default properties if not provided
        item_data.setdefault('type', 'Item')
        item_data.setdefault('revisionId', 'A')
        
        try:
            response = self.session.post(url, json=item_data)
            response.raise_for_status()
            
            created_item = response.json()
            logger.info(f"Created item: {created_item.get('itemId')}")
            return created_item
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create item: {str(e)}")
            raise
    
    def get_item(self, item_id: str) -> Dict:
        """
        Get item details by ID
        
        Args:
            item_id: Item identifier
            
        Returns:
            Item data
        """
        self.ensure_authenticated()
        
        url = urljoin(self.base_url, f'/restful/items/{item_id}')
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get item {item_id}: {str(e)}")
            raise
    
    def update_item(self, item_id: str, updates: Dict) -> Dict:
        """
        Update item properties
        
        Args:
            item_id: Item identifier
            updates: Dictionary of properties to update
            
        Returns:
            Updated item data
        """
        self.ensure_authenticated()
        
        url = urljoin(self.base_url, f'/restful/items/{item_id}')
        
        try:
            response = self.session.put(url, json=updates)
            response.raise_for_status()
            
            logger.info(f"Updated item: {item_id}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update item {item_id}: {str(e)}")
            raise
    
    def delete_item(self, item_id: str) -> bool:
        """
        Delete an item
        
        Args:
            item_id: Item identifier
            
        Returns:
            True if successful
        """
        self.ensure_authenticated()
        
        url = urljoin(self.base_url, f'/restful/items/{item_id}')
        
        try:
            response = self.session.delete(url)
            response.raise_for_status()
            
            logger.info(f"Deleted item: {item_id}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to delete item {item_id}: {str(e)}")
            raise
    
    def search_items(self, query: Dict) -> List[Dict]:
        """
        Search for items using query criteria
        
        Args:
            query: Search query parameters
            
        Returns:
            List of matching items
        """
        self.ensure_authenticated()
        
        url = urljoin(self.base_url, '/restful/items/search')
        
        try:
            response = self.session.post(url, json=query)
            response.raise_for_status()
            
            results = response.json().get('results', [])
            logger.info(f"Search returned {len(results)} items")
            return results
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Search failed: {str(e)}")
            raise
    
    # ==================== BOM Operations ====================
    
    def get_bom_structure(self, item_id: str, revision_id: str = None, 
                         levels: int = -1) -> Dict:
        """
        Get BOM structure for an item
        
        Args:
            item_id: Parent item ID
            revision_id: Specific revision (optional)
            levels: Number of levels to expand (-1 for all)
            
        Returns:
            BOM structure data
        """
        self.ensure_authenticated()
        
        url = urljoin(self.base_url, f'/restful/bom/{item_id}/structure')
        
        params = {
            'levels': levels,
            'includeProperties': True
        }
        
        if revision_id:
            params['revisionId'] = revision_id
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            bom_data = response.json()
            logger.info(f"Retrieved BOM structure for {item_id}")
            return bom_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get BOM structure: {str(e)}")
            raise
    
    def add_bom_line(self, parent_id: str, child_id: str, 
                     quantity: float = 1.0, properties: Dict = None) -> Dict:
        """
        Add a component to BOM
        
        Args:
            parent_id: Parent item ID
            child_id: Child item ID
            quantity: Quantity of child item
            properties: Additional BOM line properties
            
        Returns:
            Created BOM line data
        """
        self.ensure_authenticated()
        
        url = urljoin(self.base_url, f'/restful/bom/{parent_id}/lines')
        
        bom_line_data = {
            'childId': child_id,
            'quantity': quantity,
            'properties': properties or {}
        }
        
        try:
            response = self.session.post(url, json=bom_line_data)
            response.raise_for_status()
            
            logger.info(f"Added {child_id} to BOM of {parent_id}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to add BOM line: {str(e)}")
            raise
    
    def update_bom_line(self, parent_id: str, line_id: str, 
                       updates: Dict) -> Dict:
        """
        Update BOM line properties
        
        Args:
            parent_id: Parent item ID
            line_id: BOM line ID
            updates: Properties to update
            
        Returns:
            Updated BOM line data
        """
        self.ensure_authenticated()
        
        url = urljoin(self.base_url, f'/restful/bom/{parent_id}/lines/{line_id}')
        
        try:
            response = self.session.put(url, json=updates)
            response.raise_for_status()
            
            logger.info(f"Updated BOM line {line_id}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update BOM line: {str(e)}")
            raise
    
    def remove_bom_line(self, parent_id: str, line_id: str) -> bool:
        """
        Remove a BOM line
        
        Args:
            parent_id: Parent item ID
            line_id: BOM line ID
            
        Returns:
            True if successful
        """
        self.ensure_authenticated()
        
        url = urljoin(self.base_url, f'/restful/bom/{parent_id}/lines/{line_id}')
        
        try:
            response = self.session.delete(url)
            response.raise_for_status()
            
            logger.info(f"Removed BOM line {line_id}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to remove BOM line: {str(e)}")
            raise
    
    def get_where_used(self, item_id: str) -> List[Dict]:
        """
        Get where-used information for an item
        
        Args:
            item_id: Item ID to check
            
        Returns:
            List of parent items using this component
        """
        self.ensure_authenticated()
        
        url = urljoin(self.base_url, f'/restful/bom/{item_id}/where-used')
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            where_used = response.json().get('parents', [])
            logger.info(f"Found {len(where_used)} parents for {item_id}")
            return where_used
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get where-used: {str(e)}")
            raise
    
    # ==================== Workflow Operations ====================
    
    def start_workflow(self, process_name: str, targets: List[str], 
                      properties: Dict = None) -> Dict:
        """
        Start a workflow process
        
        Args:
            process_name: Name of the workflow process
            targets: List of target item IDs
            properties: Workflow properties
            
        Returns:
            Started workflow data
        """
        self.ensure_authenticated()
        
        url = urljoin(self.base_url, '/restful/workflows/start')
        
        workflow_data = {
            'processName': process_name,
            'targets': targets,
            'properties': properties or {}
        }
        
        try:
            response = self.session.post(url, json=workflow_data)
            response.raise_for_status()
            
            workflow = response.json()
            logger.info(f"Started workflow: {workflow.get('workflowId')}")
            return workflow
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to start workflow: {str(e)}")
            raise
    
    def get_my_tasks(self) -> List[Dict]:
        """
        Get current user's workflow tasks
        
        Returns:
            List of pending tasks
        """
        self.ensure_authenticated()
        
        url = urljoin(self.base_url, '/restful/workflows/my-tasks')
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            tasks = response.json().get('tasks', [])
            logger.info(f"Found {len(tasks)} pending tasks")
            return tasks
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get tasks: {str(e)}")
            raise
    
    def complete_task(self, task_id: str, decision: str, 
                     comments: str = "") -> Dict:
        """
        Complete a workflow task
        
        Args:
            task_id: Task identifier
            decision: Task decision (approve/reject/etc)
            comments: Optional comments
            
        Returns:
            Task completion result
        """
        self.ensure_authenticated()
        
        url = urljoin(self.base_url, f'/restful/workflows/tasks/{task_id}/complete')
        
        completion_data = {
            'decision': decision,
            'comments': comments
        }
        
        try:
            response = self.session.post(url, json=completion_data)
            response.raise_for_status()
            
            logger.info(f"Completed task {task_id} with decision: {decision}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to complete task: {str(e)}")
            raise
    
    # ==================== Document Operations ====================
    
    def upload_file(self, item_id: str, file_path: str, 
                   dataset_type: str = "Text", relation_type: str = "IMAN_specification") -> Dict:
        """
        Upload a file and attach to item
        
        Args:
            item_id: Item to attach file to
            file_path: Path to file
            dataset_type: Type of dataset
            relation_type: Relation type for attachment
            
        Returns:
            Created dataset information
        """
        self.ensure_authenticated()
        
        url = urljoin(self.base_url, '/restful/documents/upload')
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {
                'itemId': item_id,
                'datasetType': dataset_type,
                'relationType': relation_type
            }
            
            # Remove Content-Type for multipart
            headers = self.session.headers.copy()
            del headers['Content-Type']
            
            try:
                response = self.session.post(
                    url, 
                    files=files, 
                    data=data,
                    headers=headers
                )
                response.raise_for_status()
                
                dataset = response.json()
                logger.info(f"Uploaded file to dataset: {dataset.get('datasetId')}")
                return dataset
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to upload file: {str(e)}")
                raise
    
    def download_file(self, dataset_id: str, output_path: str) -> str:
        """
        Download a file from dataset
        
        Args:
            dataset_id: Dataset identifier
            output_path: Path to save file
            
        Returns:
            Path to downloaded file
        """
        self.ensure_authenticated()
        
        url = urljoin(self.base_url, f'/restful/documents/{dataset_id}/download')
        
        try:
            response = self.session.get(url, stream=True)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Downloaded file to: {output_path}")
            return output_path
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download file: {str(e)}")
            raise
    
    # ==================== Query Operations ====================
    
    def execute_saved_query(self, query_name: str, 
                           parameters: Dict = None) -> List[Dict]:
        """
        Execute a saved query
        
        Args:
            query_name: Name of saved query
            parameters: Query parameters
            
        Returns:
            Query results
        """
        self.ensure_authenticated()
        
        url = urljoin(self.base_url, '/restful/query/execute')
        
        query_data = {
            'queryName': query_name,
            'parameters': parameters or {},
            'maxResults': 1000
        }
        
        try:
            response = self.session.post(url, json=query_data)
            response.raise_for_status()
            
            results = response.json().get('results', [])
            logger.info(f"Query '{query_name}' returned {len(results)} results")
            return results
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Query execution failed: {str(e)}")
            raise
    
    # ==================== Utility Methods ====================
    
    def get_server_info(self) -> Dict:
        """
        Get Teamcenter server information
        
        Returns:
            Server information
        """
        url = urljoin(self.base_url, '/restful/info')
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get server info: {str(e)}")
            raise
    
    def logout(self):
        """Logout and clean up session"""
        if self.token:
            url = urljoin(self.base_url, '/restful/auth/logout')
            
            try:
                self.session.post(url)
                logger.info("Successfully logged out")
            except:
                pass
            
            self.token = None
            self.token_expiry = None
            self.session.close()