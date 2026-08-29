-- PR #4: Skill Mastery Dependency Graph & Adaptive Path
CREATE INDEX IF NOT EXISTS idx_skills_category ON skills (category, slug);
