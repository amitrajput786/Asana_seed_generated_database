"""Statistical distributions for realistic data generation"""

import random
from datetime import datetime, timedelta
from typing import Optional
import math


class Distributions:
    """Realistic probability distributions based on research"""
    
    # Task completion rates by project type (based on Asana Anatomy of Work)
    COMPLETION_RATES = {
        'sprint': (0.70, 0.85),
        'kanban': (0.50, 0.65),
        'campaign': (0.60, 0.75),
        'operations': (0.40, 0.55)
    }
    
    # Priority distribution (based on typical project management patterns)
    PRIORITY_WEIGHTS = {
        'low': 0.25,
        'medium': 0.45,
        'high': 0.22,
        'urgent': 0.08
    }
    
    # Due date distribution
    DUE_DATE_DISTRIBUTION = {
        'within_week': 0.25,
        'within_month': 0.40,
        'one_to_three_months': 0.20,
        'no_due_date': 0.10,
        'overdue': 0.05
    }
    
    @staticmethod
    def weighted_choice(options: dict) -> str:
        """Choose from weighted options"""
        items = list(options.keys())
        weights = list(options.values())
        return random.choices(items, weights=weights, k=1)[0]
    
    @staticmethod
    def get_completion_rate(project_type: str) -> float:
        """Get completion rate for project type"""
        min_rate, max_rate = Distributions.COMPLETION_RATES.get(
            project_type, (0.50, 0.70)
        )
        return random.uniform(min_rate, max_rate)
    
    @staticmethod
    def generate_due_date(
        created_at: datetime,
        now: Optional[datetime] = None
    ) -> Optional[datetime]:
        """Generate realistic due date based on creation date"""
        now = now or datetime.now()
        
        category = Distributions.weighted_choice(Distributions.DUE_DATE_DISTRIBUTION)
        
        if category == 'no_due_date':
            return None
        elif category == 'overdue':
            # 1-14 days before now
            days_overdue = random.randint(1, 14)
            due = now - timedelta(days=days_overdue)
        elif category == 'within_week':
            days_ahead = random.randint(1, 7)
            due = now + timedelta(days=days_ahead)
        elif category == 'within_month':
            days_ahead = random.randint(8, 30)
            due = now + timedelta(days=days_ahead)
        else:  # one_to_three_months
            days_ahead = random.randint(31, 90)
            due = now + timedelta(days=days_ahead)
        
        # Avoid weekends for 85% of tasks
        if random.random() < 0.85:
            while due.weekday() >= 5:  # Saturday = 5, Sunday = 6
                due += timedelta(days=1)
                
        return due
    
    @staticmethod
    def generate_completion_time(created_at: datetime) -> datetime:
        """Generate completion time using log-normal distribution"""
        # Log-normal with mean ~5 days, realistic for task completion
        days = random.lognormvariate(mu=1.5, sigma=0.8)
        days = min(max(days, 0.5), 30)  # Clamp between 0.5 and 30 days
        
        completed_at = created_at + timedelta(days=days)
        
        # Ensure not in future
        now = datetime.now()
        if completed_at > now:
            completed_at = now - timedelta(hours=random.randint(1, 48))
            
        return completed_at
    
    @staticmethod
    def generate_workday_timestamp(
        start_date: datetime,
        end_date: datetime
    ) -> datetime:
        """Generate timestamp during work hours (Mon-Fri, 9-18)"""
        # Random date in range
        delta = (end_date - start_date).days
        random_days = random.randint(0, max(0, delta))
        date = start_date + timedelta(days=random_days)
        
        # Skip to Monday if weekend
        while date.weekday() >= 5:
            date += timedelta(days=1)
        
        # Work hours (9 AM - 6 PM)
        hour = random.randint(9, 17)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        
        return date.replace(hour=hour, minute=minute, second=second)
    
    @staticmethod
    def should_be_assigned() -> bool:
        """85% of tasks should be assigned (15% unassigned per Asana benchmarks)"""
        return random.random() > 0.15
    
    @staticmethod
    def description_length() -> str:
        """Return description length category"""
        # 20% empty, 50% short, 30% detailed
        r = random.random()
        if r < 0.20:
            return 'empty'
        elif r < 0.70:
            return 'short'
        else:
            return 'detailed'
