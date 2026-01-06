"""Attachment data generator"""

import uuid
from datetime import datetime, timedelta
import random


class AttachmentGenerator:
    """Generate realistic attachment data"""
    
    FILE_TYPES = {
        'document': {
            'extensions': ['.pdf', '.docx', '.doc', '.txt', '.md'],
            'names': ['requirements', 'specs', 'proposal', 'report', 'notes', 'summary', 'brief'],
            'size_range': (10000, 5000000)  # 10KB - 5MB
        },
        'spreadsheet': {
            'extensions': ['.xlsx', '.csv', '.xls'],
            'names': ['data', 'analysis', 'budget', 'timeline', 'metrics', 'tracking'],
            'size_range': (5000, 2000000)  # 5KB - 2MB
        },
        'image': {
            'extensions': ['.png', '.jpg', '.jpeg', '.gif', '.svg'],
            'names': ['screenshot', 'mockup', 'design', 'diagram', 'chart', 'logo'],
            'size_range': (50000, 10000000)  # 50KB - 10MB
        },
        'presentation': {
            'extensions': ['.pptx', '.ppt', '.key'],
            'names': ['presentation', 'deck', 'slides', 'pitch', 'overview'],
            'size_range': (100000, 20000000)  # 100KB - 20MB
        }
    }
    
    def generate_attachments(
        self,
        tasks: list[dict],
        users: list[dict],
        attachment_ratio: float = 0.2  # 20% of tasks have attachments
    ) -> list[dict]:
        """Generate attachments for tasks"""
        
        attachments = []
        
        for task in tasks:
            if random.random() > attachment_ratio:
                continue
            
            task_id = task['task_id']
            task_created = datetime.fromisoformat(task['created_at'])
            
            # 1-3 attachments per task
            num_attachments = random.randint(1, 3)
            
            for i in range(num_attachments):
                file_type = random.choice(list(self.FILE_TYPES.keys()))
                type_info = self.FILE_TYPES[file_type]
                
                extension = random.choice(type_info['extensions'])
                base_name = random.choice(type_info['names'])
                file_name = f"{base_name}_{uuid.uuid4().hex[:6]}{extension}"
                
                size_min, size_max = type_info['size_range']
                file_size = random.randint(size_min, size_max)
                
                uploader = random.choice(users)
                
                uploaded_at = task_created + timedelta(
                    hours=random.randint(0, 72)
                )
                if uploaded_at > datetime.now():
                    uploaded_at = datetime.now() - timedelta(hours=random.randint(1, 24))
                
                attachments.append({
                    'attachment_id': str(uuid.uuid4()),
                    'task_id': task_id,
                    'file_name': file_name,
                    'file_type': extension[1:],  # Remove leading dot
                    'file_size': file_size,
                    'uploaded_by': uploader['user_id'],
                    'uploaded_at': uploaded_at.isoformat()
                })
        
        return attachments
