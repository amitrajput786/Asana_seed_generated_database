-- Asana Simulation Database Schema
-- Designed for B2B SaaS company simulation

-- Drop tables if they exist (for clean re-runs)
DROP TABLE IF EXISTS task_tags;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS custom_field_values;
DROP TABLE IF EXISTS custom_field_definitions;
DROP TABLE IF EXISTS attachments;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS subtasks;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS sections;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS team_memberships;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS organizations;

-- Organizations/Workspaces
CREATE TABLE organizations (
    org_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    domain TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    industry TEXT,
    employee_count INTEGER
);

-- Users
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    job_title TEXT,
    department TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL,
    last_active_at TIMESTAMP,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

-- Teams
CREATE TABLE teams (
    team_id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

-- Team Memberships (Many-to-Many: Users <-> Teams)
CREATE TABLE team_memberships (
    membership_id TEXT PRIMARY KEY,
    team_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    role TEXT DEFAULT 'member',  -- 'admin', 'member'
    joined_at TIMESTAMP NOT NULL,
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    UNIQUE(team_id, user_id)
);

-- Projects
CREATE TABLE projects (
    project_id TEXT PRIMARY KEY,
    team_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    color TEXT,
    status TEXT DEFAULT 'active',  -- 'active', 'archived', 'completed'
    project_type TEXT,  -- 'sprint', 'kanban', 'campaign', 'operations'
    created_at TIMESTAMP NOT NULL,
    due_date DATE,
    owner_id TEXT,
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (owner_id) REFERENCES users(user_id)
);

-- Sections (within Projects)
CREATE TABLE sections (
    section_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    position INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- Tasks
CREATE TABLE tasks (
    task_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    section_id TEXT,
    name TEXT NOT NULL,
    description TEXT,
    assignee_id TEXT,
    created_by TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    due_date DATE,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    priority TEXT,  -- 'low', 'medium', 'high', 'urgent'
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (section_id) REFERENCES sections(section_id),
    FOREIGN KEY (assignee_id) REFERENCES users(user_id),
    FOREIGN KEY (created_by) REFERENCES users(user_id)
);

-- Subtasks
CREATE TABLE subtasks (
    subtask_id TEXT PRIMARY KEY,
    parent_task_id TEXT NOT NULL,
    name TEXT NOT NULL,
    assignee_id TEXT,
    created_at TIMESTAMP NOT NULL,
    due_date DATE,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    FOREIGN KEY (parent_task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (assignee_id) REFERENCES users(user_id)
);

-- Comments/Stories
CREATE TABLE comments (
    comment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    author_id TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (author_id) REFERENCES users(user_id)
);

-- Custom Field Definitions
CREATE TABLE custom_field_definitions (
    field_id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    name TEXT NOT NULL,
    field_type TEXT NOT NULL,  -- 'text', 'number', 'enum', 'date'
    enum_options TEXT,  -- JSON array for enum types
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

-- Custom Field Values
CREATE TABLE custom_field_values (
    value_id TEXT PRIMARY KEY,
    field_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    value TEXT,
    FOREIGN KEY (field_id) REFERENCES custom_field_definitions(field_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    UNIQUE(field_id, task_id)
);

-- Tags
CREATE TABLE tags (
    tag_id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    name TEXT NOT NULL,
    color TEXT,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

-- Task-Tag Associations (Many-to-Many)
CREATE TABLE task_tags (
    task_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    PRIMARY KEY (task_id, tag_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);

-- Attachments
CREATE TABLE attachments (
    attachment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_type TEXT,
    file_size INTEGER,  -- in bytes
    uploaded_by TEXT NOT NULL,
    uploaded_at TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (uploaded_by) REFERENCES users(user_id)
);

-- Indexes for performance
CREATE INDEX idx_users_org ON users(org_id);
CREATE INDEX idx_teams_org ON teams(org_id);
CREATE INDEX idx_projects_team ON projects(team_id);
CREATE INDEX idx_tasks_project ON tasks(project_id);
CREATE INDEX idx_tasks_assignee ON tasks(assignee_id);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_subtasks_parent ON subtasks(parent_task_id);
CREATE INDEX idx_comments_task ON comments(task_id);
