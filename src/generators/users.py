"""User data generator"""

import uuid
from datetime import datetime, timedelta
import random
from typing import Optional

from scrapers.names import NameGenerator
from utils.distributions import Distributions


class UserGenerator:
    """Generate realistic user data"""
    
    def __init__(self, name_gen: Optional[NameGenerator] = None):
        self.name_gen = name_gen or NameGenerator()
        
    def generate_users(
        self,
        org_id: str,
        domain: str,
        count: int = 50,
        start_date: Optional[datetime] = None
    ) -> list[dict]:
        """Generate user records for an organization"""
        
        start_date = start_date or (datetime.now() - timedelta(days=365))
        users = []
        used_emails = set()
        
        for i in range(count):
            first_name, last_name = self.name_gen.generate_full_name()
            
            # Generate unique email
            email = self.name_gen.generate_email(first_name, last_name, domain)
            counter = 1
            base_email = email
            while email in used_emails:
                email = base_email.replace(f"@{domain}", f"{counter}@{domain}")
                counter += 1
            used_emails.add(email)
            
            department = self.name_gen.generate_department()
            job_title = self.name_gen.generate_job_title(department)
            
            # Created date with realistic growth pattern
            days_since_start = random.randint(0, 365)
            created_at = start_date + timedelta(days=days_since_start)
            
            # Last active (recent for most users)
            if random.random() < 0.9:  # 90% active recently
                last_active = datetime.now() - timedelta(
                    hours=random.randint(1, 72)
                )
            else:
                last_active = created_at + timedelta(
                    days=random.randint(1, 30)
                )
            
            users.append({
                'user_id': str(uuid.uuid4()),
                'org_id': org_id,
                'email': email,
                'full_name': f"{first_name} {last_name}",
                'job_title': job_title,
                'department': department,
                'is_active': random.random() < 0.95,  # 95% active
                'created_at': created_at.isoformat(),
                'last_active_at': last_active.isoformat()
            })
            
        return users
