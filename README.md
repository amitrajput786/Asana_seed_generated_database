# Asana Seed Data Generator

A comprehensive tool for generating realistic seed data to simulate Asana workspaces for B2B SaaS companies. This project creates synthetic data including organizations, users, teams, projects, tasks, comments, custom fields, tags, and attachments using a combination of LLM-powered generation and template-based approaches.

## Features

- **Complete Asana Simulation**: Generates full workspace data including organizations, users, teams, projects, and tasks
- **LLM-Enhanced Content**: Uses Groq's LLM API to create realistic task names, descriptions, and comments
- **Modular Architecture**: Separate generators for each data type (users, tasks, comments, etc.)
- **Configurable Generation**: Environment variables control the scale of generated data
- **SQLite Database**: Stores generated data in a structured database for easy querying and export
- **Realistic Distributions**: Uses statistical distributions for user activity, task completion rates, etc.
- **Template Fallback**: Gracefully degrades to template-based generation if LLM is unavailable

## Project Structure

```
asana-seed-generator2/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── schema.sql               # SQLite database schema
├── data/                    # Input data directory
├── output/                  # Generated data output (SQLite DB, notebooks)
├── prompts/                 # LLM prompt templates
│   ├── comments.txt
│   ├── descriptions.txt
│   └── task_names.txt
└── src/
    ├── main.py             # Main entry point
    ├── test_llm.py         # LLM testing utilities
    ├── generators/         # Data generation modules
    │   ├── attachments.py
    │   ├── comments.py
    │   ├── custom_fields.py
    │   ├── projects.py
    │   ├── tags.py
    │   ├── tasks.py
    │   ├── teams.py
    │   └── users.py
    ├── models/             # Data models (if any)
    ├── scrapers/           # Data scraping utilities
    │   └── names.py
    └── utils/              # Utility modules
        ├── database.py
        ├── distributions.py
        └── llm.py
```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd asana-seed-generator2
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables (optional):
   ```bash
   cp .env.example .env  # If provided
   # Edit .env with your Groq API key and configuration
   ```

## Configuration

The generator can be configured via environment variables:

- `DB_PATH`: Path to SQLite database (default: `output/asana_simulation.sqlite`)
- `NUM_USERS`: Number of users to generate (default: 50)
- `NUM_TEAMS`: Number of teams to generate (default: 5)
- `NUM_PROJECTS`: Number of projects to generate (default: 10)
- `NUM_TASKS_PER_PROJECT`: Tasks per project (default: 15)
- `GROQ_API_KEY`: Your Groq API key for LLM features

## Usage

Run the main generator:

```bash
python src/main.py
```

This will generate a complete Asana workspace simulation and save it to `output/asana_simulation.sqlite`.

### Testing LLM Integration

Test the LLM functionality separately:

```bash
python src/test_llm.py
```

### Jupyter Notebook Analysis

Use the provided notebook in `output/Untitled.ipynb` to analyze the generated data.

## Database Schema

### Data Model Hierarchy

```
Organization (Root)
├── Users
├── Teams
│   └── Team Memberships ←→ Users (M:N)
│   └── Projects
│       └── Sections
│           └── Tasks
│               ├── Subtasks
│               ├── Comments
│               ├── Attachments
│               ├── Custom Field Values → Custom Field Definitions
│               └── Task-Tags → Tags (M:N)
├── Tags
└── Custom Field Definitions

```
### Data Model Hierarchy

The following diagram illustrates the relational structure of the generated Asana-like workspace, including entity dependencies and many-to-many relationships:


::contentReference[oaicite:0]{index=0}


> **Diagram source:**  
> https://github.com/amitrajput786/Asana_seed_generated_database/blob/main/prompts/Untitled.png

#### Textual Representation (for quick reference)



### Tables Summary

| Table | Records | Description |
|-------|---------|-------------|
| organizations | 1 | Root entity - company workspace |
| users | 50 | Workspace members with profiles |
| teams | 5 | Collaboration groups |
| team_memberships | ~35 | User-team associations (M:N) |
| projects | 10 | Work containers with sections |
| sections | ~40 | Workflow stages within projects |
| tasks | ~150 | Primary work items |
| subtasks | ~45 | Nested tasks within parent tasks |
| comments | ~60 | Task discussions and updates |
| tags | 12 | Cross-project labels |
| task_tags | ~75 | Task-tag associations (M:N) |
| custom_field_definitions | 6 | Custom field schemas |
| custom_field_values | ~90 | Custom field data per task |
| attachments | ~30 | File metadata |

### Key Design Decisions

#### 1. Custom Fields (Entity-Attribute-Value Pattern)

```
custom_field_definitions (schema)
         ↓
custom_field_values (data per task)
```

- Allows unlimited custom fields without schema changes
- Mirrors Asana's actual flexible field system

#### 2. Task Hierarchy (Separate Tables)

```
tasks (parent)
  └── subtasks (children via parent_task_id FK)
```

- Simple queries without recursion
- Matches Asana's single-level subtask behavior

See `schema.sql` for the complete database structure.

## Data Generation Methodology

### Data Sources

| Data Type | Source | File |
|-----------|--------|------|
| User Names | US Census Bureau (top names) | `src/scrapers/names.py` |
| Company Names | YC/Crunchbase patterns | `src/scrapers/names.py` |
| Job Titles | LinkedIn/Glassdoor analysis | `src/scrapers/names.py` |
| Task Content | LLM (Groq) + Templates | `src/generators/tasks.py` |
| Distributions | Research benchmarks | `src/utils/distributions.py` |

### Key Distributions (Research-Based)

| Metric | Distribution | Source |
|--------|--------------|--------|
| Task Completion Rate | 40-85% (varies by project type) | Asana Anatomy of Work |
| Unassigned Tasks | 15% | Asana benchmarks |
| Due Date: Within 1 week | 25% | Sprint research |
| Due Date: Within 1 month | 40% | Sprint research |
| Due Date: 1-3 months | 20% | Planning horizons |
| Due Date: None | 10% | Backlog items |
| Due Date: Overdue | 5% | Realistic slippage |
| Priority: Low | 25% | Pareto principle |
| Priority: Medium | 45% | Pareto principle |
| Priority: High | 22% | Pareto principle |
| Priority: Urgent | 8% | Pareto principle |

### Consistency Rules

#### Temporal Consistency:

- `completed_at > created_at` (tasks can't complete before creation)
- `subtask.created_at > parent_task.created_at`
- `comment.created_at > task.created_at`
- `attachment.uploaded_at >= task.created_at`
- All timestamps ≤ current time

#### Relational Consistency:

- All foreign keys reference existing records
- Sections belong to their task's project
- Generation order follows dependency graph

### Generation Order (Dependency Graph)

```
1. Organization     →  2. Users           →  3. Teams
                                              ↓
4. Team Memberships ←─────────────────────────┘
        ↓
5. Projects + Sections  →  6. Tags  →  7. Custom Field Definitions
        ↓
8. Tasks + Subtasks
        ↓
9. Task-Tags  →  10. Custom Field Values  →  11. Comments  →  12. Attachments
```

## Sample Queries

### Task Completion Rate by Project

```sql
SELECT 
    p.name AS project_name,
    p.project_type,
    COUNT(*) AS total_tasks,
    SUM(CASE WHEN t.completed = 1 THEN 1 ELSE 0 END) AS completed,
    ROUND(100.0 * SUM(CASE WHEN t.completed = 1 THEN 1 ELSE 0 END) / COUNT(*), 1) || '%' AS rate
FROM projects p
LEFT JOIN tasks t ON p.project_id = t.project_id
GROUP BY p.project_id
ORDER BY rate DESC;
```

## Output Statistics

For default configuration (50 users, 5 teams, 10 projects, 15 tasks/project):

| Table | Expected Count |
|-------|-----------------|
| organizations | 1 |
| users | 50 |
| teams | 5 |
| team_memberships | ~35 |
| projects | 10 |
| sections | ~40 |
| tasks | ~150 |
| subtasks | ~45 |
| comments | ~60 |
| tags | 12 |
| task_tags | ~75 |
| custom_field_definitions | 6 |
| custom_field_values | ~90 |
| attachments | ~30 |
| **Total** | **~550-600** |

## Dependencies

- **groq**: For LLM-powered content generation
- **python-dotenv**: Environment variable management
- **Faker**: Realistic fake data generation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[MIT license]

## Notes

- The project uses Groq's API for enhanced realism in generated content
- If no API key is provided, it falls back to template-based generation
- Generated data is suitable for development, testing, and demonstration purposes
- The database schema is designed to be compatible with Asana's API structure
