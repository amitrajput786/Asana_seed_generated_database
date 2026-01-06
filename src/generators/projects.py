"""Project data generator"""

import uuid
from datetime import datetime, timedelta
import random
from typing import Optional


class ProjectGenerator:
    """Generate realistic project data"""
    
    # Project templates by type
    PROJECT_TEMPLATES = {
        'Engineering': [
            {'name': 'Q{q} Sprint {n}', 'type': 'sprint', 'sections': ['Backlog', 'In Progress', 'Review', 'Done']},
            {'name': 'Platform Reliability', 'type': 'kanban', 'sections': ['To Do', 'Doing', 'Done']},
            {'name': 'API v{n} Development', 'type': 'sprint', 'sections': ['Planning', 'Development', 'Testing', 'Deployed']},
            {'name': 'Tech Debt Tracker', 'type': 'kanban', 'sections': ['Identified', 'Prioritized', 'In Progress', 'Resolved']},
            {'name': 'Security Improvements', 'type': 'kanban', 'sections': ['Audit Items', 'In Progress', 'Verified', 'Complete']},
        ],
        'Product': [
            {'name': 'Product Roadmap {year}', 'type': 'kanban', 'sections': ['Ideas', 'Researching', 'Planned', 'Building', 'Launched']},
            {'name': 'Feature: {feature}', 'type': 'sprint', 'sections': ['Discovery', 'Design', 'Development', 'Launch']},
            {'name': 'User Feedback Tracker', 'type': 'kanban', 'sections': ['New', 'Reviewing', 'Planned', 'Shipped']},
        ],
        'Marketing': [
            {'name': 'Q{q} Marketing Campaigns', 'type': 'campaign', 'sections': ['Planning', 'In Progress', 'Live', 'Completed']},
            {'name': 'Content Calendar', 'type': 'operations', 'sections': ['Ideas', 'Writing', 'Review', 'Published']},
            {'name': 'Website Redesign', 'type': 'sprint', 'sections': ['Research', 'Design', 'Development', 'Launch']},
            {'name': 'Brand Refresh {year}', 'type': 'campaign', 'sections': ['Strategy', 'Creative', 'Production', 'Rollout']},
        ],
        'Sales': [
            {'name': 'Enterprise Deals Q{q}', 'type': 'operations', 'sections': ['Prospecting', 'Qualifying', 'Proposal', 'Negotiation', 'Closed']},
            {'name': 'Sales Enablement', 'type': 'kanban', 'sections': ['Requested', 'Creating', 'Review', 'Published']},
        ],
        'Operations': [
            {'name': 'Company OKRs {year}', 'type': 'operations', 'sections': ['Draft', 'Active', 'Completed']},
            {'name': 'Process Improvements', 'type': 'kanban', 'sections': ['Ideas', 'Evaluating', 'Implementing', 'Done']},
            {'name': 'Vendor Management', 'type': 'operations', 'sections': ['To Review', 'In Negotiation', 'Active', 'Archived']},
        ]
    }
    
    FEATURES = [
        'Dashboard Analytics', 'User Permissions', 'API Integrations',
        'Mobile App', 'Reporting Module', 'SSO Support', 'Bulk Actions',
        'Export Functionality', 'Notifications', 'Search Enhancement'
    ]
    
    COLORS = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink']
    
    def generate_projects(
        self,
        teams: list[dict],
        users: list[dict],
        count: int = 10,
        start_date: Optional[datetime] = None
    ) -> tuple[list[dict], list[dict]]:
        """Generate projects and their sections"""
        
        start_date = start_date or (datetime.now() - timedelta(days=180))
        now = datetime.now()
        
        projects = []
        sections = []
        
        for i in range(count):
            team = random.choice(teams)
            team_id = team['team_id']
            team_name = team['name']
            
            # Determine department from team name
            dept = 'Operations'
            for d in self.PROJECT_TEMPLATES.keys():
                if d.lower() in team_name.lower():
                    dept = d
                    break
            
            # Get random template
            templates = self.PROJECT_TEMPLATES.get(dept, self.PROJECT_TEMPLATES['Operations'])
            template = random.choice(templates)
            
            # Format project name
            quarter = ((now.month - 1) // 3) + 1
            project_name = template['name'].format(
                q=quarter,
                n=random.randint(1, 5),
                year=now.year,
                feature=random.choice(self.FEATURES)
            )
            
            created_at = start_date + timedelta(days=random.randint(0, 150))
            
            # Due date for some projects
            due_date = None
            if random.random() < 0.6:
                due_date = (created_at + timedelta(days=random.randint(30, 120))).date()
            
            project_id = str(uuid.uuid4())
            owner = random.choice(users)
            
            project = {
                'project_id': project_id,
                'team_id': team_id,
                'name': project_name,
                'description': f"Project for tracking {template['type']} work in {team_name}.",
                'color': random.choice(self.COLORS),
                'status': random.choices(
                    ['active', 'active', 'active', 'completed', 'archived'],
                    weights=[0.7, 0.1, 0.1, 0.05, 0.05]
                )[0],
                'project_type': template['type'],
                'created_at': created_at.isoformat(),
                'due_date': str(due_date) if due_date else None,
                'owner_id': owner['user_id']
            }
            projects.append(project)
            
            # Create sections for this project
            for pos, section_name in enumerate(template['sections']):
                sections.append({
                    'section_id': str(uuid.uuid4()),
                    'project_id': project_id,
                    'name': section_name,
                    'position': pos,
                    'created_at': created_at.isoformat()
                })
        
        return projects, sections
