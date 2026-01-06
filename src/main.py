"""
Asana Simulation Seed Data Generator
Main entry point for generating realistic Asana workspace data
"""

import os
import uuid
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

from utils.database import Database
from utils.llm import LLMClient
from scrapers.names import NameGenerator
from generators.users import UserGenerator
from generators.teams import TeamGenerator
from generators.projects import ProjectGenerator
from generators.tasks import TaskGenerator
from generators.comments import CommentGenerator
from generators.tags import TagGenerator
from generators.custom_fields import CustomFieldGenerator
from generators.attachments import AttachmentGenerator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AsanaSimulator:
    """Main orchestrator for generating Asana simulation data"""
    
    def __init__(self):
        self.db = Database(os.getenv('DB_PATH', 'output/asana_simulation.sqlite'))
        
        # Initialize LLM client (optional)
        try:
            self.llm = LLMClient()
            logger.info("LLM client initialized successfully")
        except Exception as e:
            logger.warning(f"LLM client not available: {e}. Using template-based generation.")
            self.llm = None
        
        # Initialize generators
        self.name_gen = NameGenerator()
        self.user_gen = UserGenerator(self.name_gen)
        self.team_gen = TeamGenerator()
        self.project_gen = ProjectGenerator()
        self.task_gen = TaskGenerator(self.llm)
        self.comment_gen = CommentGenerator(self.llm)
        self.tag_gen = TagGenerator()
        self.custom_field_gen = CustomFieldGenerator()
        self.attachment_gen = AttachmentGenerator()
        
        # Configuration
        self.config = {
            'num_users': int(os.getenv('NUM_USERS', 50)),
            'num_teams': int(os.getenv('NUM_TEAMS', 5)),
            'num_projects': int(os.getenv('NUM_PROJECTS', 10)),
            'tasks_per_project': int(os.getenv('NUM_TASKS_PER_PROJECT', 15))
        }
        
    def run(self):
        """Execute full data generation pipeline"""
        logger.info("=" * 60)
        logger.info("Starting Asana Simulation Data Generation")
        logger.info("=" * 60)
        
        # Initialize database
        self.db.connect()
        self.db.initialize_schema()
        
        start_date = datetime.now() - timedelta(days=365)
        
        # 1. Generate Organization
        logger.info("Step 1: Generating organization...")
        org = self._generate_organization()
        self.db.insert_many('organizations', [org])
        
        # 2. Generate Users
        logger.info(f"Step 2: Generating {self.config['num_users']} users...")
        users = self.user_gen.generate_users(
            org['org_id'],
            org['domain'],
            count=self.config['num_users'],
            start_date=start_date
        )
        self.db.insert_many('users', users)
        
        # 3. Generate Teams
        logger.info(f"Step 3: Generating {self.config['num_teams']} teams...")
        teams = self.team_gen.generate_teams(
            org['org_id'],
            count=self.config['num_teams'],
            start_date=start_date
        )
        self.db.insert_many('teams', teams)
        
        # 4. Generate Team Memberships
        logger.info("Step 4: Generating team memberships...")
        memberships = self.team_gen.generate_memberships(teams, users)
        self.db.insert_many('team_memberships', memberships)
        
        # 5. Generate Projects and Sections
        logger.info(f"Step 5: Generating {self.config['num_projects']} projects...")
        projects, sections = self.project_gen.generate_projects(
            teams,
            users,
            count=self.config['num_projects'],
            start_date=start_date
        )
        self.db.insert_many('projects', projects)
        self.db.insert_many('sections', sections)
        
        # 6. Generate Tags
        logger.info("Step 6: Generating tags...")
        tags = self.tag_gen.generate_tags(org['org_id'])
        self.db.insert_many('tags', tags)
        
        # 7. Generate Custom Fields
        logger.info("Step 7: Generating custom field definitions...")
        custom_fields = self.custom_field_gen.generate_field_definitions(org['org_id'])
        self.db.insert_many('custom_field_definitions', custom_fields)
        
        # 8. Generate Tasks and Subtasks
        logger.info(f"Step 8: Generating tasks ({self.config['tasks_per_project']} per project)...")
        tasks, subtasks = self.task_gen.generate_tasks(
            projects,
            sections,
            users,
            tasks_per_project=self.config['tasks_per_project']
        )
        self.db.insert_many('tasks', tasks)
        self.db.insert_many('subtasks', subtasks)
        
        # 9. Generate Task Tags
        logger.info("Step 9: Generating task-tag associations...")
        task_tags = self.tag_gen.generate_task_tags(tasks, tags)
        self.db.insert_many('task_tags', task_tags)
        
        # 10. Generate Custom Field Values
        logger.info("Step 10: Generating custom field values...")
        field_values = self.custom_field_gen.generate_field_values(tasks, custom_fields)
        self.db.insert_many('custom_field_values', field_values)
        
        # 11. Generate Comments
        logger.info("Step 11: Generating comments...")
        comments = self.comment_gen.generate_comments(tasks, users)
        self.db.insert_many('comments', comments)
        
        # 12. Generate Attachments
        logger.info("Step 12: Generating attachments...")
        attachments = self.attachment_gen.generate_attachments(tasks, users)
        self.db.insert_many('attachments', attachments)
        
        # Print summary
        self._print_summary()
        
        # Close database
        self.db.close()
        logger.info("Data generation complete!")
        
    def _generate_organization(self) -> dict:
        """Generate the main organization"""
        company_name = self.name_gen.generate_company_name()
        domain = self.name_gen.generate_domain(company_name)
        
        return {
            'org_id': str(uuid.uuid4()),
            'name': company_name,
            'domain': domain,
            'created_at': (datetime.now() - timedelta(days=730)).isoformat(),
            'industry': 'B2B SaaS',
            'employee_count': 7500  # Mid-range of 5000-10000
        }
    
    def _print_summary(self):
        """Print generation summary"""
        tables = [
            'organizations', 'users', 'teams', 'team_memberships',
            'projects', 'sections', 'tasks', 'subtasks', 'comments',
            'tags', 'task_tags', 'custom_field_definitions',
            'custom_field_values', 'attachments'
        ]
        
        logger.info("\n" + "=" * 60)
        logger.info("Generation Summary")
        logger.info("=" * 60)
        
        for table in tables:
            try:
                count = len(self.db.fetch_all(table))
                logger.info(f"  {table}: {count} records")
            except Exception:
                pass
        
        logger.info("=" * 60)


def main():
    """Main entry point"""
    simulator = AsanaSimulator()
    simulator.run()


if __name__ == "__main__":
    main()
