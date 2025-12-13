---
name: resume-matrix-mapper
description: Automatically map candidate resumes to qualification matrix tables. TRIGGER PHRASES - Use this skill when you see these phrases: "map resume to matrix", "fill in the matrix", "process resume against matrix", "populate matrix with resume", or when user uploads both a qualification matrix (.docx with requirements table) and a candidate resume (.docx) together. This skill extracts qualifications from resumes and populates "Applicant Qualifications", "Applicant Years of Experience", and "PROFESSIONAL EXPERIENCE" columns by matching against "Required Qualifications" and "Labor Category Capabilities". Never modifies human-filled requirement columns.
---

# Resume to Matrix Mapper Skill

## 🎯 QUICK START - Read This First

### When to Activate This Skill

**AUTOMATIC ACTIVATION when you see:**
- User uploads 2 documents: one matrix template + one resume
- User says: "map this resume", "fill the matrix", "process the resume", "populate matrix columns"
- User asks to extract qualifications from a resume into a table
- User needs candidate evaluation matrix filled out

**DO NOT activate for:**
- Creating new matrices from scratch
- General resume review or formatting
- Job description writing
- Skills assessment without a matrix template

### Pre-Flight Checklist

Before starting, verify:
1. ✅ You have a matrix document (Word .docx) with a requirements table
2. ✅ You have a candidate resume (Word .docx or PDF convertible to .docx)
3. ✅ The matrix has columns for: Required Qualifications, Applicant Qualifications, Applicant Years
4. ✅ The matrix has empty applicant columns waiting to be filled

If any item fails, **ask the user for clarification** before proceeding.

### The 30-Second Process

```
1. Read matrix → Find requirement rows
2. Read resume → Extract work history
3. For each requirement → Find matching resume content
4. Fill in: Qualifications + Years + Professional Experience
5. Save completed matrix
```

That's it. Everything below is detail for complex edge cases.

---

## Core Workflow - Step by Step

### STEP 1: Document Validation (30 seconds)

```python
# First, validate both documents exist and are readable
from docx import Document

# Load matrix
matrix_doc = Document('/mnt/user-data/uploads/matrix_template.docx')

# Verify it has tables
if not matrix_doc.tables:
    raise ValueError("Matrix document has no tables")

# Load resume  
resume_doc = Document('/mnt/user-data/uploads/candidate_resume.docx')

# Verify resume has content
resume_text = '\n'.join([para.text for para in resume_doc.paragraphs])
if len(resume_text) < 100:
    raise ValueError("Resume appears to be empty or too short")
```

### STEP 2: Understand Matrix Structure (30 seconds)

```python
# Find the main requirements table
main_table = matrix_doc.tables[0]  # Usually the first/largest table

# Identify column positions by scanning header row
headers = [cell.text.strip() for cell in main_table.rows[0].cells]

# Map column names to indices
col_map = {}
for idx, header in enumerate(headers):
    header_lower = header.lower()
    if 'required' in header_lower and 'qualification' in header_lower:
        col_map['required_quals'] = idx
    elif 'labor' in header_lower and 'capabilit' in header_lower:
        col_map['capabilities'] = idx
    elif 'applicant' in header_lower and 'qualification' in header_lower:
        col_map['applicant_quals'] = idx
    elif 'applicant' in header_lower and 'year' in header_lower:
        col_map['applicant_years'] = idx
    elif 'professional' in header_lower and 'experience' in header_lower:
        col_map['prof_experience'] = idx

# Verify we found the key columns
required_columns = ['required_quals', 'applicant_quals', 'applicant_years']
if not all(col in col_map for col in required_columns):
    # Ask user to clarify column names
    print("⚠️ Could not identify all required columns. Please verify matrix structure.")
```

### STEP 3: Extract Resume Content (1 minute)

```python
def extract_resume_data(resume_doc):
    """Extract structured data from resume"""
    
    resume_text = '\n'.join([para.text for para in resume_doc.paragraphs])
    
    # Parse work history with dates
    work_history = parse_work_experience(resume_text)
    # Returns: [{'company': str, 'title': str, 'start': date, 'end': date, 'duties': [str]}]
    
    # Extract skills and technologies
    skills = extract_skills_list(resume_text)
    # Returns: ['Python', 'AWS', 'Docker', ...]
    
    # Parse education
    education = parse_education(resume_text)
    # Returns: [{'degree': str, 'institution': str, 'year': int}]
    
    return {
        'work_history': work_history,
        'skills': skills,
        'education': education,
        'full_text': resume_text
    }
```

### STEP 4: Match Requirements to Resume (2-3 minutes per row)

For each requirement row in the matrix:

```python
for row_idx in range(1, len(main_table.rows)):  # Skip header
    row = main_table.rows[row_idx]
    
    # Get requirement text
    requirement = row.cells[col_map['required_quals']].text.strip()
    capability = row.cells[col_map.get('capabilities', -1)].text.strip() if 'capabilities' in col_map else ''
    
    if not requirement and not capability:
        continue  # Skip rows without requirements
    
    # Combine requirement texts for matching
    search_terms = f"{requirement} {capability}".lower()
    
    # Find matching resume content
    matches = find_matching_content(
        search_terms=search_terms,
        work_history=resume_data['work_history'],
        skills=resume_data['skills'],
        education=resume_data['education']
    )
    
    # Calculate years of relevant experience
    years = calculate_years(matches, requirement)
    
    # Format the outputs
    applicant_quals = format_qualifications(matches, requirement)
    prof_exp = format_professional_experience(matches)
    
    # Populate the cells
    row.cells[col_map['applicant_quals']].text = applicant_quals
    row.cells[col_map['applicant_years']].text = str(years)
    if 'prof_experience' in col_map:
        row.cells[col_map['prof_experience']].text = prof_exp
```

### STEP 5: Quality Check & Save (30 seconds)

```python
# Verify all requirement rows are filled
empty_rows = []
for row_idx in range(1, len(main_table.rows)):
    row = main_table.rows[row_idx]
    requirement = row.cells[col_map['required_quals']].text.strip()
    applicant_quals = row.cells[col_map['applicant_quals']].text.strip()
    
    if requirement and not applicant_quals:
        empty_rows.append(row_idx)

if empty_rows:
    print(f"⚠️ Warning: {len(empty_rows)} rows still empty")

# Save to outputs
output_path = '/mnt/user-data/outputs/completed_matrix.docx'
matrix_doc.save(output_path)

print(f"✅ Matrix completed and saved to {output_path}")
```

---

## Detailed Matching Logic

### Finding Relevant Resume Content

The matching algorithm uses multiple strategies:

#### 1. Direct Keyword Matching
```python
# Requirement: "Python programming experience"
# Look for: 'python', 'py', 'django', 'flask', 'fastapi'
```

#### 2. Semantic Similarity
```python
# Requirement: "Cloud infrastructure experience"
# Match: AWS, Azure, GCP, Kubernetes, Docker, Terraform, CloudFormation
```

#### 3. Date-Based Filtering
```python
# Requirement: "Recent Agile experience"
# Prioritize: Jobs from last 5 years with Scrum/Kanban/Agile
```

#### 4. Context-Aware Relevance
```python
# Requirement: "Senior software engineer"
# Look for: 'Senior', 'Lead', 'Principal' titles + years of experience
# Weight recent jobs higher than old jobs
```

### Calculating Years of Experience

**Rules for Year Calculation:**

1. **Single Job with Skill**
   ```python
   # Software Engineer, Jan 2020 - Dec 2023, used Python
   # Calculation: 4 years
   years = (end_date - start_date).days / 365.25
   ```

2. **Multiple Jobs with Skill**
   ```python
   # Job 1: Jan 2020 - Dec 2021, used Python (2 years)
   # Job 2: Jun 2022 - Present, used Python (2.5 years)
   # Calculation: 2 + 2.5 = 4.5 years
   years = sum(duration for job in matching_jobs)
   ```

3. **Overlapping Jobs** (count once)
   ```python
   # Full-time Job: Jan 2020 - Dec 2023 (4 years)
   # Part-time Contract: Jun 2020 - Jun 2021 (1 year) - OVERLAPS
   # Calculation: 4 years (not 5)
   ```

4. **Part-Time Work** (prorate if known)
   ```python
   # Part-time (50%), 2 years = 1 year equivalent
   # If percentage unknown, count full duration
   ```

5. **Career Gaps** (exclude)
   ```python
   # Job 1: 2015-2017 (2 years)
   # Gap: 2018-2019
   # Job 2: 2020-2023 (3 years)
   # Total: 5 years, not 8
   ```

### Formatting Applicant Qualifications

**Goal**: 1-3 sentence summary showing the candidate meets the requirement

**Template Structure:**
```
[X years] [skill/technology] experience including [specific tools/frameworks] at [notable context]; [additional evidence like certifications or achievements]
```

**Examples:**

✅ **Good:**
```
7 years Python development using Django, Flask, and FastAPI for enterprise web applications; built 15+ production APIs handling 1M+ requests/day at Google and Amazon
```

✅ **Good:**
```
AWS Solutions Architect Professional certified (2021); 5 years deploying cloud infrastructure using Terraform, EKS, and Lambda across 20+ production environments
```

✅ **Good:**
```
MS Computer Science, Stanford (2018); 6 years machine learning engineering including deep learning model deployment at Meta using PyTorch and TensorFlow
```

❌ **Bad (too vague):**
```
Experienced in Python and has worked on many projects
```

❌ **Bad (too long / copy-pasted):**
```
The candidate has extensive experience with Python programming language, having used it at multiple companies including ABC Corp where they were responsible for developing backend services, and XYZ Inc where they built data pipelines, and also freelance projects...
```

### Formatting Professional Experience

**Goal**: Chronological work history with only relevant jobs and duties

**Template:**
```
Company Name, Job Title (Month Year - Month Year)
• Relevant responsibility demonstrating this requirement
• Another relevant duty or achievement
• Key technologies: [list]

Company Name, Job Title (Month Year - Month Year)
• Relevant responsibility demonstrating this requirement
• Key technologies: [list]
```

**Example for "Python web development" requirement:**

```
Google, Senior Software Engineer (January 2020 - Present)
• Architect and develop microservices using Python Django and Flask
• Lead backend API development for Google Cloud Console using FastAPI
• Mentor team of 5 engineers on Python best practices and design patterns
• Technologies: Python, Django, Flask, FastAPI, PostgreSQL, Redis, Kubernetes

Amazon Web Services, Software Development Engineer (June 2017 - December 2019)
• Built and maintained Python-based REST APIs for AWS billing services
• Implemented automated testing framework using pytest and moto
• Optimized database queries reducing API latency by 40%
• Technologies: Python, Flask, DynamoDB, pytest, Docker
```

**What to EXCLUDE:**
- Jobs where the required skill was NOT used
- Duties unrelated to this specific requirement
- Generic responsibilities like "attended meetings"

---

## Edge Cases & Troubleshooting

### Issue: Matrix columns don't match expected names

**Solution:**
```python
# Show user what you found
print("Found these columns:", headers)
print("Looking for: Required Qualifications, Applicant Qualifications, Applicant Years")

# Ask for guidance
response = input("Please tell me which column numbers to use for applicant info")
```

### Issue: Resume has no clear dates

**Solution:**
```python
# Make reasonable estimates
if "current" in job_text.lower() or "present" in job_text.lower():
    end_date = datetime.now()
if not start_date:
    # Estimate based on typical role duration (2-3 years)
    start_date = end_date - timedelta(days=2.5*365)
    
# NOTE this in the output
note = " (estimated duration)"
```

### Issue: Requirement is very vague

**Example:** Requirement says "technical skills"

**Solution:**
```python
# Be broad in matching
matching_skills = all_technical_skills_from_resume
# In qualification, be specific about what was found
applicant_quals = f"Technical skills include: {', '.join(matching_skills[:10])}"
```

### Issue: Resume seems irrelevant to matrix

**Example:** Matrix is for software engineering, resume is for nursing

**Solution:**
```python
# Process what you can, note what's missing
if no_relevant_experience:
    applicant_quals = "No relevant experience found in resume for this requirement"
    years = "0"
    prof_exp = "N/A"
```

### Issue: Multiple tables in matrix document

**Solution:**
```python
# Find the largest table or the one with "Required Qualifications" column
tables_with_reqs = []
for table in matrix_doc.tables:
    headers = [cell.text for cell in table.rows[0].cells]
    if any('required' in h.lower() and 'qualification' in h.lower() for h in headers):
        tables_with_reqs.append(table)

if len(tables_with_reqs) > 1:
    # Ask user which table to process
    print(f"Found {len(tables_with_reqs)} requirements tables. Processing the first one.")
    main_table = tables_with_reqs[0]
```

---

## Human-in-the-Loop Validation

After processing, always show the user a summary:

```python
print("\n" + "="*60)
print("PROCESSING COMPLETE")
print("="*60)
print(f"✅ Processed {rows_filled} requirement rows")
print(f"✅ Calculated years of experience for {rows_filled} requirements")
print(f"✅ Extracted professional experience from {len(relevant_jobs)} jobs")
print(f"\n⚠️  Please review the following for accuracy:")
print(f"   • Years of experience calculations")
print(f"   • Relevance of matched content")
print(f"   • Completeness of professional experience")
print(f"\nOutput saved to: {output_path}")
print("="*60)
```

---

## Column Identification Reference

The skill should recognize these column name variations:

| Concept | Possible Column Names |
|---------|----------------------|
| Required Qualifications | "Required Qualifications", "Requirements", "Required Skills", "Job Requirements", "Position Requirements" |
| Labor Category Capabilities | "Labor Category Capabilities", "Capabilities", "Required Capabilities", "Core Competencies" |
| Applicant Qualifications | "Applicant Qualifications", "Candidate Qualifications", "How Met", "Evidence", "Applicant Evidence" |
| Applicant Years | "Applicant Years", "Years of Experience", "Years", "Experience (Years)", "Applicant Yrs" |
| Professional Experience | "Professional Experience", "PROFESSIONAL EXPERIENCE", "Work History", "Relevant Experience", "Career History" |

Use case-insensitive partial matching to identify columns.

---

## Testing Your Work

Before delivering the completed matrix, verify:

- [ ] Every row with requirements has applicant info filled
- [ ] Years calculations are mathematically correct (spot check 3-5 rows)
- [ ] Professional experience only includes jobs where skill was used
- [ ] No information was invented (all from resume)
- [ ] Formatting is clean and professional
- [ ] Human-filled columns are untouched
- [ ] No placeholder text remains ([TO FILL], TBD, etc.)

---

## Common Pitfalls to Avoid

❌ **Don't copy-paste resume verbatim** → Synthesize and paraphrase

❌ **Don't count overlapping time twice** → Concurrent jobs = count time once

❌ **Don't fill irrelevant experience** → Only include jobs where skill was actually used

❌ **Don't modify requirement columns** → Only fill applicant columns

❌ **Don't invent information** → If resume doesn't have it, note as missing

❌ **Don't use vague statements** → Be specific with tools, technologies, contexts

❌ **Don't make wild assumptions** → If truly unclear, ask user or note limitation

---

## Success Metrics

A well-executed matrix will have:

✅ **100% completion rate** - All requirement rows filled (or noted as N/A)

✅ **Accurate calculations** - Years match actual resume dates

✅ **Relevant evidence** - Each qualification directly supports its requirement

✅ **Professional formatting** - Consistent style, no errors

✅ **Ready for review** - Manager can review immediately without cleanup

---

## Final Checklist Before Saving

```python
# Run this mental checklist before saving output
validation_checklist = {
    'All requirement rows processed': True,
    'Years are numeric (not text)': True,
    'Professional experience in reverse chronological order': True,
    'No [TO FILL] or [TBD] placeholders remain': True,
    'Human-filled columns unchanged': True,
    'Output file in /mnt/user-data/outputs/': True,
    'File named descriptively (e.g., matrix_john_doe_completed.docx)': True
}

if not all(validation_checklist.values()):
    print("⚠️ VALIDATION FAILED - Review before delivering")
```

---

## When to Ask for Help

**Ask the user if:**
- Matrix structure is completely different from expected
- Multiple resumes provided and unclear which to use
- Resume format is unusual (pure images, tables only, etc.)
- Requirement is ambiguous and could match multiple interpretations
- Years calculation seems incorrect but you can't determine why

**Don't ask if:**
- Minor formatting differences (handle automatically)
- Slightly different column names (use fuzzy matching)
- Some requirements have no matches (fill with "No relevant experience")
- Resume is in standard format but poorly formatted (extract what you can)

---

## Summary: The Essential Flow

```
INPUT: Matrix template + Candidate resume

STEP 1: Validate documents (30 sec)
STEP 2: Map column positions (30 sec)  
STEP 3: Extract resume data (1 min)
STEP 4: Match & populate each row (2-3 min per row)
STEP 5: Validate & save (30 sec)

OUTPUT: Completed matrix in /mnt/user-data/outputs/
```

**Total time: 5-15 minutes depending on matrix complexity**

---

## Example: Complete Processing Run

**Input Files:**
- `software_engineer_matrix.docx` - 10 requirement rows
- `jane_smith_resume.docx` - 3 pages, 5 jobs

**Processing Log:**
```
✓ Loaded matrix: 10 requirement rows found
✓ Loaded resume: 5 jobs, 12 skills identified
✓ Row 1: "5 years Python" → Found 7 years → Filled
✓ Row 2: "AWS certification" → Found cert + 4 years → Filled
✓ Row 3: "Agile experience" → Found 6 years → Filled
...
✓ Row 10: "PhD required" → Not found → Noted as missing
✅ Completed 9/10 rows (1 requirement not met by candidate)
✅ Saved to: completed_matrix_jane_smith.docx
```

**Output Quality:**
- Qualifications: Concise, specific, evidence-based
- Years: Accurate calculations from resume dates
- Professional Experience: Only relevant jobs included
- Format: Professional, consistent, no errors

---

END OF SKILL DOCUMENTATION
