"""Team data generator"""

import uuid
from datetime import datetime, timedelta
import random
from typing import Optional


class TeamGenerator:
    """Generate realistic team data"""
    
    # Realistic B2B SaaS team names
    TEAM_TEMPLATES = [
        {"name": "Platform Engineering", "dept": "Engineering"},
        {"name": "Frontend Team", "dept": "Engineering"},
        {"name": "Backend Services", "dept": "Engineering"},
        {"name": "Mobile Team", "dept": "Engineering"},
        {"name": "DevOps & Infrastructure", "dept": "Engineering"},
        {"name": "Product Management", "dept": "Product"},
        {"name": "UX/UI Design", "dept": "Design"},
        {"name": "Growth Marketing", "dept": "Marketing"},
        {"name": "Content & Brand", "dept": "Marketing"},
        {"name": "Enterprise Sales", "dept": "Sales"},
        {"name": "Customer Success", "dept": "Customer Success"},
        {"name": "Revenue Operations", "dept": "Operations"},
    ]
    
    def generate_teams(
        self,
        org_id: str,
        count: int = 5,
        start_date: Optional[datetime] = None
    ) -> list[dict]:
        """Generate team records"""
        
        start_date = start_date or (datetime.now() - timedelta(days=365))
        
        # Select teams (don't exceed available templates)
        selected = random.sample(
            self.TEAM_TEMPLATES, 
            min(count, len(self.TEAM_TEMPLATES))
        )
        
        teams = []
        for i, template in enumerate(selected):
            created_at = start_date + timedelta(days=random.randint(0, 30))
            
            teams.append({
                'team_id': str(uuid.uuid4()),
                'org_id': org_id,
                'name': template['name'],
                'description': f"The {template['name']} team at our company.",
                'created_at': created_at.isoformat()
            })
            
        return teams
    
    def generate_memberships(
        self,
        teams: list[dict],
        users: list[dict]
    ) -> list[dict]:
        """Generate team membership records"""
        
        memberships = []
        
        # Group users by department
        dept_users = {}
        for user in users:
            dept = user.get('department', 'Operations')
            if dept not in dept_users:
                dept_users[dept] = []
            dept_users[dept].append(user)
        
        for team in teams:
            team_id = team['team_id']
            team_created = datetime.fromisoformat(team['created_at'])
            
            # Assign 3-10 members per team
            team_size = random.randint(3, 10)
            
            # Prefer users from matching departments
            available_users = users.copy()
            random.shuffle(available_users)
            
            selected_users = available_users[:team_size]
            
            for i, user in enumerate(selected_users):
                role = 'admin' if i == 0 else 'member'
                joined = team_created + timedelta(days=random.randint(0, 14))
                
                memberships.append({
                    'membership_id': str(uuid.uuid4()),
                    'team_id': team_id,
                    'user_id': user['user_id'],
                    'role': role,
                    'joined_at': joined.isoformat()
                })
                
        return memberships
