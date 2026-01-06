"""Name and company data generator using realistic sources"""

import random
from faker import Faker
from typing import Optional


class NameGenerator:
    """Generate realistic names based on census-like distributions"""
    
    # Common first names (US Census-inspired distribution)
    FIRST_NAMES_MALE = [
        "James", "Michael", "Robert", "John", "David", "William", "Richard",
        "Joseph", "Thomas", "Christopher", "Charles", "Daniel", "Matthew",
        "Anthony", "Mark", "Steven", "Paul", "Andrew", "Joshua", "Kevin",
        "Brian", "George", "Timothy", "Ronald", "Edward", "Jason", "Jeffrey",
        "Ryan", "Jacob", "Nicholas", "Gary", "Eric", "Jonathan", "Stephen",
        "Larry", "Justin", "Scott", "Brandon", "Benjamin", "Samuel"
    ]
    
    FIRST_NAMES_FEMALE = [
        "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth",
        "Susan", "Jessica", "Sarah", "Karen", "Lisa", "Nancy", "Betty",
        "Margaret", "Sandra", "Ashley", "Kimberly", "Emily", "Donna",
        "Michelle", "Dorothy", "Carol", "Amanda", "Melissa", "Deborah",
        "Stephanie", "Rebecca", "Sharon", "Laura", "Cynthia", "Kathleen",
        "Amy", "Angela", "Shirley", "Anna", "Brenda", "Pamela", "Emma"
    ]
    
    LAST_NAMES = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
        "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
        "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
        "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
        "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green",
        "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell"
    ]
    
    # B2B SaaS company name components (inspired by YC, Crunchbase patterns)
    COMPANY_PREFIXES = [
        "Cloud", "Data", "Tech", "Smart", "AI", "Next", "Pro", "Prime",
        "Swift", "Apex", "Nova", "Sync", "Flow", "Core", "Hub", "Wave"
    ]
    
    COMPANY_SUFFIXES = [
        "Labs", "Systems", "Works", "Logic", "Soft", "ware", "io", "ly",
        "Hub", "Base", "Stack", "Point", "Stream", "Grid", "Ops", "Forge"
    ]
    
    # Departments for B2B SaaS
    DEPARTMENTS = [
        "Engineering", "Product", "Design", "Marketing", "Sales",
        "Customer Success", "Operations", "Finance", "HR", "Legal"
    ]
    
    # Job titles by department
    JOB_TITLES = {
        "Engineering": [
            "Software Engineer", "Senior Software Engineer", "Staff Engineer",
            "Engineering Manager", "DevOps Engineer", "QA Engineer",
            "Frontend Developer", "Backend Developer", "Full Stack Developer"
        ],
        "Product": [
            "Product Manager", "Senior Product Manager", "Product Owner",
            "Associate Product Manager", "Director of Product"
        ],
        "Design": [
            "UX Designer", "UI Designer", "Product Designer", "Design Lead",
            "UX Researcher"
        ],
        "Marketing": [
            "Marketing Manager", "Content Marketer", "Growth Marketer",
            "Marketing Coordinator", "Brand Manager", "SEO Specialist"
        ],
        "Sales": [
            "Account Executive", "Sales Development Rep", "Sales Manager",
            "Enterprise Sales Rep", "Sales Director"
        ],
        "Customer Success": [
            "Customer Success Manager", "Support Engineer", "CSM Lead",
            "Technical Account Manager"
        ],
        "Operations": [
            "Operations Manager", "Business Analyst", "Project Manager",
            "Scrum Master"
        ],
        "Finance": [
            "Financial Analyst", "Accountant", "Controller", "FP&A Manager"
        ],
        "HR": [
            "HR Manager", "Recruiter", "People Operations", "HR Coordinator"
        ],
        "Legal": [
            "Legal Counsel", "Compliance Manager", "Paralegal"
        ]
    }
    
    def __init__(self, seed: Optional[int] = None):
        self.faker = Faker()
        if seed:
            Faker.seed(seed)
            random.seed(seed)
    
    def generate_full_name(self) -> tuple[str, str]:
        """Generate realistic full name, returns (first_name, last_name)"""
        if random.random() < 0.5:
            first = random.choice(self.FIRST_NAMES_MALE)
        else:
            first = random.choice(self.FIRST_NAMES_FEMALE)
        
        last = random.choice(self.LAST_NAMES)
        return first, last
    
    def generate_email(self, first_name: str, last_name: str, domain: str) -> str:
        """Generate corporate email address"""
        patterns = [
            f"{first_name.lower()}.{last_name.lower()}",
            f"{first_name.lower()}{last_name.lower()[0]}",
            f"{first_name.lower()[0]}{last_name.lower()}",
            f"{first_name.lower()}_{last_name.lower()}"
        ]
        return f"{random.choice(patterns)}@{domain}"
    
    def generate_company_name(self) -> str:
        """Generate B2B SaaS company name"""
        pattern = random.choice([
            lambda: f"{random.choice(self.COMPANY_PREFIXES)}{random.choice(self.COMPANY_SUFFIXES)}",
            lambda: f"{random.choice(self.COMPANY_PREFIXES)} {random.choice(['AI', 'Tech', 'Cloud'])}",
            lambda: self.faker.company()
        ])
        return pattern()
    
    def generate_domain(self, company_name: str) -> str:
        """Generate company domain from name"""
        # Clean company name for domain
        domain = company_name.lower()
        domain = ''.join(c for c in domain if c.isalnum())
        return f"{domain}.com"
    
    def generate_department(self) -> str:
        """Get random department"""
        return random.choice(self.DEPARTMENTS)
    
    def generate_job_title(self, department: str) -> str:
        """Get job title for department"""
        titles = self.JOB_TITLES.get(department, ["Team Member"])
        return random.choice(titles)
