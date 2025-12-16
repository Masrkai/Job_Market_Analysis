### **Task: Collect and Categorize "Meme Jobs" from LinkedIn**

#### **Objective**
1. **Identify and collect** job titles or roles in the tech/CS space that are widely regarded as "meme jobs" (e.g., overly vague, buzzword-laden, or lacking clear responsibilities).
2. **Create a new category** in the dataset called `meme_jobs` to house these titles.
3. **Draft a `Rules/meme_jobs.md`** file to define what qualifies as a "meme job" and the classification process (for future reference).

---

### **Step 1: Define "Meme Jobs" (for `Rules/meme_jobs.md`)**

- **Purpose**: Explain why "meme jobs" are tracked and how they differ from standard roles.

> For Example

1 -
 **Classification Rules**:
 
  - A job title is classified as a "meme job" if it meets **at least 2 of the following**:
    1. Contains **3+ buzzwords** (e.g., "AI," "Blockchain," "Disrupt," "Innovate").
    2. Lacks a **clear, industry-recognized definition** (e.g., "Growth Hacker" vs. "Marketing Specialist").
    3. Is **rarely used in formal job postings** (e.g., found mostly on personal profiles).
    4. Includes **self-aggrandizing language** (e.g., "Guru," "Ninja," "Rockstar").

> Another example

- A "meme job" is a role that:
  - Uses **excessive buzzwords** (e.g., "Blockchain Guru," "AI Whisperer").
  - Has a **vague or overly broad** title (e.g., "Digital Transformation Evangelist").
  - Lacks **clear, actionable responsibilities** (e.g., "Innovation Catalyst").
  - Is often **self-proclaimed** or **unverified** (e.g., titles with "Ninja," "Rockstar," or "Guru").
  - Appears **frequently on LinkedIn** but rarely in formal job postings or industry standards.

#### but keep in mind
- This is not FINAL
- **Exceptions**: Titles that are satire or clearly humorous (e.g., "Chief Meme Officer") may be excluded unless they appear frequently on LinkedIn.
- **Maintenance**: Encourage community contributions to keep the list updated.

---

### **Step 2: Collect "Meme Jobs" from LinkedIn**
#### **Sources:**
- **LinkedIn Profiles**: Search for unusual or exaggerated job titles in the tech/CS space.
- **LinkedIn Job Postings**: Look for roles with vague descriptions or buzzword-heavy language.
- **Tech Satire Communities**: Check platforms like Reddit (e.g., r/ProgrammerHumor) or Twitter for crowdsourced examples.

#### **Examples of "Meme Jobs":**
- **Buzzword Titles**:
  - "Blockchain Evangelist"
  - "AI/ML Ninja"
  - "Cloud Disruptor"
  - "Digital Alchemist"
  - "Metaverse Architect"
  - "Web3 Visionary"
  - "Growth Hacker"
  - "Innovation Sherpa"

- **Vague or Overly Broad Titles**:
  - "Tech Thought Leader"
  - "Future of Work Strategist"
  - "Disruption Consultant"
  - "Synergy Coordinator"
  - "Paradigm Shift Engineer"
  - "Holistic Digital Experience Curator"

- **Self-Proclaimed "Expert" Titles**:
  - "Self-Taught AI Genius"
  - "10x Developer"
  - "Full-Stack Unicorn"
  - "Code Sorcerer"
  - "Data Science Rockstar"

---

### **Step 3: Add `meme_jobs` Category to the Dataset**
Update the JSON dataset to include a new category:
```json
{
  "domains": [
    {
      "name": "Meme Jobs",
      "description": "Job titles or roles in tech/CS that are vague, buzzword-heavy, or lack clear substance. Sourced from LinkedIn and tech satire communities.",
      "jobs": [
        {"name": "Blockchain Evangelist"},
        {"name": "AI/ML Ninja"},
        {"name": "Cloud Disruptor"},
        {"name": "Digital Alchemist"},
        {"name": "Metaverse Architect"},
        {"name": "Web3 Visionary"},
        {"name": "Growth Hacker"},
        {"name": "Tech Thought Leader"},
        {"name": "Future of Work Strategist"},
        {"name": "Disruption Consultant"},
        {"name": "Synergy Coordinator"},
        {"name": "Paradigm Shift Engineer"},
        {"name": "Holistic Digital Experience Curator"},
        {"name": "Self-Taught AI Genius"},
        {"name": "10x Developer"},
        {"name": "Full-Stack Unicorn"},
        {"name": "Code Sorcerer"},
        {"name": "Data Science Rockstar"}
      ]
    }
  ]
}
```

---

### **Step 4: Validate and Iterate**
- **Review with Peers**: Share the list with others to ensure it captures the spirit of "meme jobs."
- **Remove False Positives**: Exclude titles that might seem unusual but are legitimate in niche industries.
- **Document Edge Cases**: Note titles that are controversial or borderline (e.g., "Prompt Engineer" during the rise of LLMs).

---