"""Comment data generator"""

import uuid
from datetime import datetime, timedelta
import random
from typing import Optional

from utils.llm import LLMClient


class CommentGenerator:
    """Generate realistic task comments"""
    
    COMMENT_TEMPLATES = {
        'status_update': [
            "Started working on this today.",
            "Made good progress, should be done by EOD.",
            "This is now complete and ready for review.",
            "Moving this to next sprint due to dependencies.",
            "Blocked on {blocker}, will update when resolved.",
            "50% complete, on track for deadline."
        ],
        'question': [
            "Can someone clarify the requirements here?",
            "Should we prioritize this over {other_task}?",
            "Who should I loop in for the review?",
            "Is there a deadline for this?",
            "Do we have the design specs ready?"
        ],
        'answer': [
            "Yes, please go ahead with the current approach.",
            "I've added the specs to the shared folder.",
            "Let's discuss this in tomorrow's standup.",
            "The deadline is end of this week.",
            "I'll send you the details by EOD."
        ],
        'feedback': [
            "Looks good! Just a few minor comments.",
            "Great work on this!",
            "Can we add more details to the description?",
            "Approved! Ready for the next step.",
            "Please address the comments and re-submit."
        ],
        'blocker': [
            "Blocked: waiting for API access.",
            "Blocked on design review.",
            "Need input from the product team.",
            "Waiting for third-party integration.",
            "Dependency on {dependency} not resolved yet."
        ]
    }
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client
        
    def generate_comments(
        self,
        tasks: list[dict],
        users: list[dict],
        comments_ratio: float = 0.4  # 40% of tasks get comments
    ) -> list[dict]:
        """Generate comments for tasks"""
        
        comments = []
        
        for task in tasks:
            if random.random() > comments_ratio:
                continue
            
            task_id = task['task_id']
            task_created = datetime.fromisoformat(task['created_at'])
            
            # 1-4 comments per task
            num_comments = random.randint(1, 4)
            
            last_comment_time = task_created
            
            for i in range(num_comments):
                comment_type = random.choice(list(self.COMMENT_TEMPLATES.keys()))
                author = random.choice(users)
                
                # Comment time progression
                hours_later = random.randint(1, 72)
                comment_time = last_comment_time + timedelta(hours=hours_later)
                
                if comment_time > datetime.now():
                    comment_time = datetime.now() - timedelta(hours=random.randint(1, 24))
                
                last_comment_time = comment_time
                
                content = self._generate_comment_content(
                    task['name'],
                    comment_type,
                    author.get('job_title', 'Team Member')
                )
                
                comments.append({
                    'comment_id': str(uuid.uuid4()),
                    'task_id': task_id,
                    'author_id': author['user_id'],
                    'content': content,
                    'created_at': comment_time.isoformat()
                })
        
        return comments
    
    def _generate_comment_content(
        self,
        task_name: str,
        comment_type: str,
        author_role: str
    ) -> str:
        """Generate comment content"""
        
        if self.llm and random.random() < 0.3:  # Use LLM for 30%
            try:
                return self.llm.generate_comment(task_name, comment_type, author_role)
            except Exception:
                pass
        
        templates = self.COMMENT_TEMPLATES.get(comment_type, self.COMMENT_TEMPLATES['status_update'])
        template = random.choice(templates)
        
        return template.format(
            blocker=random.choice(['external API', 'design approval', 'data migration']),
            other_task='the urgent bug fix',
            dependency='the auth module'
        )
