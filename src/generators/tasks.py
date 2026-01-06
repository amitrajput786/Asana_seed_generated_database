"""Task data generator"""

import uuid
from datetime import datetime, timedelta
import random
from typing import Optional

from utils.distributions import Distributions
from utils.llm import LLMClient


class TaskGenerator:
    """Generate realistic task data"""
    
    # Fallback task name templates if LLM unavailable
    TASK_TEMPLATES = {
        'sprint': [
            "Implement {component} {action}",
            "Fix bug in {component}",
            "Add unit tests for {component}",
            "Refactor {component} module",
            "Update {component} documentation",
            "Review PR for {feature}",
            "Deploy {component} to staging",
            "Performance optimization for {component}"
        ],
        'kanban': [
            "Research {topic}",
            "Update {document}",
            "Review {item}",
            "Improve {process}",
            "Investigate {issue}"
        ],
        'campaign': [
            "Create {asset} for {campaign}",
            "Review {asset} copy",
            "Design {asset}",
            "Schedule {channel} posts",
            "Analyze {campaign} performance",
            "Update {channel} content"
        ],
        'operations': [
            "Review {document}",
            "Update {process} workflow",
            "Prepare {report}",
            "Schedule {meeting}",
            "Follow up on {item}"
        ]
    }
    
    COMPONENTS = ['authentication', 'dashboard', 'API', 'database', 'UI', 'notifications', 'search', 'reports']
    ACTIONS = ['feature', 'endpoint', 'integration', 'handler', 'service', 'component']
    FEATURES = ['user settings', 'data export', 'bulk operations', 'filters', 'sorting']
    ASSETS = ['banner', 'email', 'landing page', 'blog post', 'video', 'infographic']
    CAMPAIGNS = ['Q1 launch', 'product update', 'holiday', 'webinar', 'conference']
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client
        self.use_llm = llm_client is not None
        
    def generate_tasks(
        self,
        projects: list[dict],
        sections: list[dict],
        users: list[dict],
        tasks_per_project: int = 15
    ) -> tuple[list[dict], list[dict]]:
        """Generate tasks and subtasks for projects"""
        
        tasks = []
        subtasks = []
        
        # Group sections by project
        project_sections = {}
        for section in sections:
            pid = section['project_id']
            if pid not in project_sections:
                project_sections[pid] = []
            project_sections[pid].append(section)
        
        for project in projects:
            project_id = project['project_id']
            project_type = project.get('project_type', 'kanban')
            project_name = project['name']
            project_created = datetime.fromisoformat(project['created_at'])
            proj_sections = project_sections.get(project_id, [])
            
            # Get team name for context
            team_name = "Team"  # Default
            
            # Generate task names
            task_names = self._generate_task_names(
                project_type, 
                project_name,
                team_name,
                tasks_per_project
            )
            
            completion_rate = Distributions.get_completion_rate(project_type)
            
            for i, task_name in enumerate(task_names):
                task_id = str(uuid.uuid4())
                
                # Assign to section based on completion
                section = random.choice(proj_sections) if proj_sections else None
                
                # Creator and assignee
                creator = random.choice(users)
                assignee = random.choice(users) if Distributions.should_be_assigned() else None
                
                # Timestamps
                created_at = Distributions.generate_workday_timestamp(
                    project_created,
                    datetime.now() - timedelta(days=7)
                )
                
                # Due date
                due_date = Distributions.generate_due_date(created_at)
                
                # Completion
                completed = random.random() < completion_rate
                completed_at = None
                if completed:
                    completed_at = Distributions.generate_completion_time(created_at)
                
                # Description
                desc_length = Distributions.description_length()
                description = self._generate_description(task_name, desc_length)
                
                # Priority
                priority = Distributions.weighted_choice(Distributions.PRIORITY_WEIGHTS)
                
                task = {
                    'task_id': task_id,
                    'project_id': project_id,
                    'section_id': section['section_id'] if section else None,
                    'name': task_name,
                    'description': description,
                    'assignee_id': assignee['user_id'] if assignee else None,
                    'created_by': creator['user_id'],
                    'created_at': created_at.isoformat(),
                    'due_date': due_date.date().isoformat() if due_date else None,
                    'completed': completed,
                    'completed_at': completed_at.isoformat() if completed_at else None,
                    'priority': priority
                }
                tasks.append(task)
                
                # Generate 0-3 subtasks for some tasks (30% chance)
                if random.random() < 0.3:
                    num_subtasks = random.randint(1, 3)
                    for j in range(num_subtasks):
                        subtask = self._generate_subtask(task, users)
                        subtasks.append(subtask)
        
        return tasks, subtasks
    
    def _generate_task_names(
        self,
        project_type: str,
        project_name: str,
        team_name: str,
        count: int
    ) -> list[str]:
        """Generate task names using LLM or templates"""
        
        if self.use_llm and self.llm:
            try:
                names = self.llm.generate_task_names(
                    project_type,
                    project_name,
                    team_name,
                    count
                )
                if names and len(names) >= count // 2:
                    return names[:count]
            except Exception:
                pass  # Fall back to templates
        
        # Template-based generation
        templates = self.TASK_TEMPLATES.get(project_type, self.TASK_TEMPLATES['kanban'])
        names = []
        
        for i in range(count):
            template = random.choice(templates)
            name = template.format(
                component=random.choice(self.COMPONENTS),
                action=random.choice(self.ACTIONS),
                feature=random.choice(self.FEATURES),
                topic=random.choice(['market trends', 'competitors', 'user needs']),
                document=random.choice(['specs', 'requirements', 'guidelines']),
                item=random.choice(['feedback', 'request', 'proposal']),
                process=random.choice(['onboarding', 'review', 'deployment']),
                issue=random.choice(['slowdown', 'error', 'bottleneck']),
                asset=random.choice(self.ASSETS),
                campaign=random.choice(self.CAMPAIGNS),
                channel=random.choice(['LinkedIn', 'Twitter', 'email']),
                report=random.choice(['weekly', 'monthly', 'quarterly']),
                meeting=random.choice(['standup', 'review', 'planning'])
            )
            names.append(name)
        
        return names
    
    def _generate_description(self, task_name: str, length: str) -> str:
        """Generate task description"""
        if length == 'empty':
            return ""
        
        if self.use_llm and self.llm and length == 'detailed':
            try:
                return self.llm.generate_description(task_name, 'general', 'team')
            except Exception:
                pass
        
        # Simple template-based description
        if length == 'short':
            return f"Work on: {task_name}"
        else:
            return f"This task involves completing the following work: {task_name}. Please update progress in comments."
    
    def _generate_subtask(self, parent_task: dict, users: list[dict]) -> dict:
        """Generate a subtask for a parent task"""
        parent_created = datetime.fromisoformat(parent_task['created_at'])
        
        subtask_prefixes = ['Review', 'Draft', 'Update', 'Test', 'Document', 'Verify']
        subtask_name = f"{random.choice(subtask_prefixes)} {parent_task['name'][:30]}"
        
        created_at = parent_created + timedelta(hours=random.randint(1, 48))
        
        assignee = random.choice(users) if random.random() < 0.7 else None
        
        completed = parent_task['completed'] and random.random() < 0.9
        completed_at = None
        if completed:
            completed_at = Distributions.generate_completion_time(created_at)
        
        return {
            'subtask_id': str(uuid.uuid4()),
            'parent_task_id': parent_task['task_id'],
            'name': subtask_name,
            'assignee_id': assignee['user_id'] if assignee else None,
            'created_at': created_at.isoformat(),
            'due_date': parent_task['due_date'],
            'completed': completed,
            'completed_at': completed_at.isoformat() if completed_at else None
        }
