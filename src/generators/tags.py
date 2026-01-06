"""Tag data generator"""

import uuid
import random


class TagGenerator:
    """Generate tags and task-tag associations"""
    
    TAG_DEFINITIONS = [
        {'name': 'bug', 'color': 'red'},
        {'name': 'feature', 'color': 'blue'},
        {'name': 'urgent', 'color': 'red'},
        {'name': 'documentation', 'color': 'purple'},
        {'name': 'tech-debt', 'color': 'orange'},
        {'name': 'needs-review', 'color': 'yellow'},
        {'name': 'blocked', 'color': 'red'},
        {'name': 'quick-win', 'color': 'green'},
        {'name': 'customer-request', 'color': 'blue'},
        {'name': 'internal', 'color': 'gray'},
        {'name': 'improvement', 'color': 'teal'},
        {'name': 'security', 'color': 'red'},
    ]
    
    def generate_tags(self, org_id: str) -> list[dict]:
        """Generate tag definitions for organization"""
        tags = []
        
        for tag_def in self.TAG_DEFINITIONS:
            tags.append({
                'tag_id': str(uuid.uuid4()),
                'org_id': org_id,
                'name': tag_def['name'],
                'color': tag_def['color']
            })
        
        return tags
    
    def generate_task_tags(
        self,
        tasks: list[dict],
        tags: list[dict],
        tag_ratio: float = 0.5  # 50% of tasks get tags
    ) -> list[dict]:
        """Generate task-tag associations"""
        
        task_tags = []
        
        for task in tasks:
            if random.random() > tag_ratio:
                continue
            
            # 1-3 tags per task
            num_tags = random.randint(1, 3)
            selected_tags = random.sample(tags, min(num_tags, len(tags)))
            
            for tag in selected_tags:
                task_tags.append({
                    'task_id': task['task_id'],
                    'tag_id': tag['tag_id']
                })
        
        return task_tags
