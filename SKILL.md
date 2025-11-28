---
name: resume-matrix-mapper
description: Map resume content to qualification matrix tables for candidate evaluation. Use when managers need to populate matrix documents with candidate qualifications extracted from resumes. Fills "Applicant Qualifications" and "PROFESSIONAL EXPERIENCE" fields by matching resume content to "Required Qualifications" and "Labor Category Capabilities" rows. Leaves human-filled fields (Labor Category Description, Required Qualifications, Labor Category Capabilities, Program Domain Skills) untouched.
---

# Resume to Matrix Mapper

## Overview

This skill extracts relevant qualifications and experience from candidate resumes and maps them to pre-defined qualification matrix tables. Managers provide a matrix template with required qualifications and a candidate's resume, and this skill populates the applicant-specific columns with matching evidence and calculated years of experience.

## When to Use This Skill

Use this skill when:
- A manager uploads a qualification matrix template and a candidate resume
- The task involves filling in "Applicant Qualifications" or "PROFESSIONAL EXPERIENCE" columns
- Matching resume content to specific qualification requirements is needed
- Calculating years of relevant experience from work history is required

## Matrix Structure

The qualification matrix is a Word document table with these columns:

**Human-Filled Columns** (DO NOT MODIFY):
- Labor Category Description
- Required Qualifications
- Labor Category Capabilities
- Program Domain Skills

**AI-Populated Columns** (FILL FROM RESUME):
- Applicant Qualifications
- Applicant Years of Experience (calculated from resume dates)
- PROFESSIONAL EXPERIENCE section (detailed work history relevant to the row)

## Core Workflow

### Step 1: Load and Understand Documents

1. **Read the matrix template** using python-docx to understand:
   - Table structure and column positions
   - Required Qualifications for each row
   - Labor Category Capabilities for each row
   - Which fields are already filled by humans

2. **Extract resume content** using python-docx or pandoc:
   ```bash
   pandoc resume.docx -o resume.md
   ```
   Parse for:
   - Work experience with dates and responsibilities
   - Education and certifications
   - Skills and technical competencies
   - Projects and achievements

### Step 2: Match Resume to Requirements

For each matrix row with Required Qualifications or Labor Category Capabilities:

1. **Identify relevant resume content** that demonstrates the qualification:
   - Look for direct mentions of technologies, methodologies, or skills
   - Find work experience that used these capabilities
   - Locate certifications or education that meet requirements
   - Identify projects that demonstrate the skills

2. **Extract supporting evidence**:
   - Keep evidence concise and relevant (1-3 sentences)
   - Include specific technologies, tools, or methodologies
   - Reference job titles and companies when relevant
   - Cite certifications or degrees when applicable

3. **Calculate years of experience**:
   - Sum total time from all relevant job experiences
   - Parse date ranges (e.g., "Jan 2020 - Dec 2022" = 3 years)
   - Round to nearest year or use decimals for precision (e.g., 2.5 years)
   - If experience spans multiple roles, add them together
   - If dates are unclear, make reasonable estimates and note assumptions

### Step 3: Populate Matrix Fields

#### Applicant Qualifications Column

Write concise, evidence-based statements:

**Format**: Brief description of how the candidate meets this requirement

**Good Examples**:
- "5+ years Python development including Django, Flask, FastAPI for enterprise applications"
- "AWS Certified Solutions Architect with 3 years deploying cloud infrastructure using Terraform"
- "Led 3 Agile teams as Scrum Master; CSM certified 2019"
- "MS Computer Science, Stanford 2018; BS in Software Engineering, MIT 2015"

**Avoid**:
- Exact copying from resume (paraphrase and synthesize)
- Vague statements without specifics
- Listing every job where skill was used
- Information not relevant to this specific requirement

#### Applicant Years of Experience Column

Provide numeric calculation:

**Format**: Single number (e.g., "7", "3.5", "12")

**Calculation Rules**:
- Count only relevant experience for this specific requirement
- Sum across multiple jobs if the skill/capability was used
- Use decimals for partial years when appropriate
- If unclear, provide best estimate based on available information

#### PROFESSIONAL EXPERIENCE Section

Provide detailed work history relevant to this requirement:

**Format**: Chronological work history with dates, companies, roles, and relevant responsibilities

**Structure**:
```
Company Name, Job Title (Start Date - End Date)
- Relevant responsibility or achievement for this requirement
- Another relevant point
- Key technologies or methodologies used

Company Name, Job Title (Start Date - End Date)
- Relevant responsibility or achievement for this requirement
```

**Good Example**:
```
Google, Senior Software Engineer (Jan 2020 - Present)
- Architected microservices using Python and Docker, deployed on GCP Kubernetes
- Led migration of monolithic application to cloud-native architecture
- Technologies: Python, Docker, Kubernetes, GCP, Terraform

Amazon, Software Engineer (Jun 2017 - Dec 2019)
- Developed RESTful APIs using Python Flask for e-commerce platform
- Implemented CI/CD pipelines with Jenkins and AWS CodePipeline
- Technologies: Python, Flask, AWS, Jenkins, PostgreSQL
```

**Include Only**:
- Jobs where this specific qualification/capability was demonstrated
- Responsibilities directly related to the requirement
- Relevant technologies and tools
- Quantifiable achievements when available

**Exclude**:
- Jobs with no connection to this requirement
- Generic job duties not related to the capability
- Unrelated skills or technologies

### Step 4: Quality Checks

Before finalizing the matrix:

1. **Completeness Check**:
   - Every row with requirements should have applicant info filled
   - All three applicant columns should be populated for each relevant row
   - No placeholder text or TODOs remaining

2. **Accuracy Check**:
   - Years of experience calculations are mathematically correct
   - Evidence in Applicant Qualifications directly supports the requirement
   - Professional Experience only includes relevant jobs

3. **Consistency Check**:
   - Date formats are consistent throughout
   - Writing style is professional and consistent
   - Numeric formats match (e.g., always "5" not "five")

4. **Formatting Check**:
   - Table structure is preserved
   - Human-filled columns remain unchanged
   - Line breaks and spacing are appropriate
   - No formatting errors introduced

## Advanced Techniques

### Handling Ambiguous Requirements

When a requirement is vague or could match multiple resume elements:

1. **Prioritize direct matches**: Look for exact terminology first
2. **Consider related experience**: Include adjacent or transferable skills
3. **Note assumptions**: If making interpretive leaps, briefly note this
4. **Ask for clarification**: If truly unclear, ask the manager

Example:
- Requirement: "Cloud experience"
- Resume mentions: AWS, Azure, "worked on cloud migration project"
- Applicant Qualifications: "3 years AWS and Azure experience including cloud migration of legacy applications"

### Calculating Complex Experience

For overlapping or part-time work:

**Concurrent Jobs**: Count each job's contribution
- If someone worked two jobs simultaneously for 2 years where both used Python: count as 2 years, not 4

**Part-Time Work**: Prorate if information is available
- 2 years part-time (50%) = 1 year full-time equivalent

**Contract/Project Work**: Count actual duration
- Multiple 3-month contracts over 5 years = total contract months, not 5 years

**Career Breaks**: Exclude from calculations
- If someone worked 2015-2017, took break 2018-2019, worked 2020-2023: calculate as 2+3=5 years, not 8

### Handling Missing Information

When resume lacks clear information:

1. **Education dates missing**: Use graduation year or estimate from work history
2. **Job dates incomplete**: Use "Present" for current job, estimate others from context
3. **Years at company but not role**: Distribute proportionally if multiple roles listed
4. **No dates at all**: Note "Experience duration unclear from resume" and provide best estimate

### Synthesizing Multiple Resume Sections

Requirements often span multiple resume sections:

**Education + Experience**: 
- Requirement: "Master's degree and 5 years experience in data science"
- Look at: Education section + relevant work history
- Synthesize: "MS Data Science, UC Berkeley 2015; 7 years experience in ML engineering roles at Facebook and Google"

**Certifications + Projects**:
- Requirement: "AWS certification and cloud deployment experience"
- Look at: Certifications + project descriptions + work history
- Synthesize: "AWS Solutions Architect Professional certified 2021; deployed 15+ production applications on AWS using ECS, Lambda, and RDS"

## Python Implementation Pattern

Use python-docx for reliable matrix manipulation:

```python
from docx import Document

def process_resume_to_matrix(resume_path, matrix_path, output_path):
    # Load documents
    resume_doc = Document(resume_path)
    matrix_doc = Document(matrix_path)
    
    # Extract resume content
    resume_text = extract_resume_content(resume_doc)
    work_history = parse_work_history(resume_text)
    skills = extract_skills(resume_text)
    education = extract_education(resume_text)
    
    # Process matrix table
    for table in matrix_doc.tables:
        for row in table.rows:
            # Identify columns
            requirement = get_cell_text(row, "Required Qualifications")
            capability = get_cell_text(row, "Labor Category Capabilities")
            
            if requirement or capability:
                # Find matching resume content
                matches = find_matching_content(
                    requirement, capability, 
                    work_history, skills, education
                )
                
                # Calculate years
                years = calculate_relevant_years(matches, work_history)
                
                # Populate applicant columns
                set_cell_text(row, "Applicant Qualifications", 
                            format_qualifications(matches))
                set_cell_text(row, "Applicant Years", str(years))
                set_cell_text(row, "PROFESSIONAL EXPERIENCE", 
                            format_work_history(matches))
    
    # Save result
    matrix_doc.save(output_path)
```

## Common Pitfalls

**Avoid These Mistakes**:

1. **Over-claiming**: Don't inflate experience or claim qualifications not supported by resume
2. **Verbatim copying**: Paraphrase and synthesize rather than copy-pasting resume text
3. **Irrelevant information**: Only include content directly related to each requirement
4. **Inconsistent dates**: Ensure all date calculations and formats are consistent
5. **Modifying human-filled fields**: Never change pre-filled requirement descriptions
6. **Missing context**: Include enough detail that evidence is clear without referencing resume
7. **Formatting breaks**: Preserve table structure and cell formatting

## Output Format

The completed matrix should:
- Preserve all original table structure and formatting
- Have all applicant columns filled for relevant rows
- Show consistent professional writing style
- Include no errors or placeholder text
- Be ready for manager review without additional editing

## Example Transformation

**Matrix Row (Before)**:
| Required Qualifications | Applicant Qualifications | Applicant Years | PROFESSIONAL EXPERIENCE |
|------------------------|-------------------------|-----------------|------------------------|
| Python programming with web frameworks | [TO FILL] | [TO FILL] | [TO FILL] |

**Matrix Row (After)**:
| Required Qualifications | Applicant Qualifications | Applicant Years | PROFESSIONAL EXPERIENCE |
|------------------------|-------------------------|-----------------|------------------------|
| Python programming with web frameworks | 6 years Python development using Django and Flask for enterprise web applications; built 10+ production APIs | 6 | **Google, Senior Software Engineer (Jan 2020 - Present)**<br>- Developed microservices using Python Django for internal tools<br>- Led API development for customer-facing web applications<br><br>**Startup Inc, Python Developer (Jun 2017 - Dec 2019)**<br>- Built Flask-based REST APIs for mobile app backend<br>- Maintained Django e-commerce platform with 100K+ users |

This example shows proper synthesis, calculation, and formatting for one matrix row.
