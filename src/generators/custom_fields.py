"""Custom field data generator"""

import uuid
import random
import json


class CustomFieldGenerator:
    """Generate custom field definitions and values"""
    
    FIELD_DEFINITIONS = [
        {
            'name': 'Priority Level',
            'field_type': 'enum',
            'enum_options': ['P0 - Critical', 'P1 - High', 'P2 - Medium', 'P3 - Low']
        },
        {
            'name': 'Story Points',
            'field_type': 'number',
            'enum_options': None
        },
        {
            'name': 'Sprint',
            'field_type': 'enum',
            'enum_options': ['Sprint 1', 'Sprint 2', 'Sprint 3', 'Sprint 4', 'Backlog']
        },
        {
            'name': 'Effort Estimate',
            'field_type': 'enum',
            'enum_options': ['XS', 'S', 'M', 'L', 'XL']
        },
        {
            'name': 'Due Quarter',
            'field_type': 'enum',
            'enum_options': ['Q1', 'Q2', 'Q3', 'Q4']
        },
        {
            'name': 'External Link',
            'field_type': 'text',
            'enum_options': None
        }
    ]
    
    def generate_field_definitions(self, org_id: str) -> list[dict]:
        """Generate custom field definitions for organization"""
        fields = []
        
        for field_def in self.FIELD_DEFINITIONS:
            fields.append({
                'field_id': str(uuid.uuid4()),
                'org_id': org_id,
                'name': field_def['name'],
                'field_type': field_def['field_type'],
                'enum_options': json.dumps(field_def['enum_options']) if field_def['enum_options'] else None
            })
        
        return fields
    
    def generate_field_values(
        self,
        tasks: list[dict],
        field_definitions: list[dict],
        fill_ratio: float = 0.6  # 60% of tasks have custom field values
    ) -> list[dict]:
        """Generate custom field values for tasks"""
        
        values = []
        
        for task in tasks:
            if random.random() > fill_ratio:
                continue
            
            # Each task gets 1-3 custom field values
            num_fields = random.randint(1, 3)
            selected_fields = random.sample(
                field_definitions,
                min(num_fields, len(field_definitions))
            )
            
            for field in selected_fields:
                value = self._generate_value(field)
                
                values.append({
                    'value_id': str(uuid.uuid4()),
                    'field_id': field['field_id'],
                    'task_id': task['task_id'],
                    'value': value
                })
        
        return values
    
    def _generate_value(self, field: dict) -> str:
        """Generate appropriate value for field type"""
        field_type = field['field_type']
        
        if field_type == 'enum':
            options = json.loads(field['enum_options'])
            return random.choice(options)
        elif field_type == 'number':
            if 'Points' in field['name']:
                return str(random.choice([1, 2, 3, 5, 8, 13]))
            return str(random.randint(1, 100))
        elif field_type == 'text':
            return f"https://example.com/{uuid.uuid4().hex[:8]}"
        else:
            return ""
