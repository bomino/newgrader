# NewGrader User Guide

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Features Guide](#features-guide)
   - [Classes](#classes)
   - [Students](#students)
   - [Assignments](#assignments)
   - [Grade Entry](#grade-entry)
   - [Auto-Grade](#auto-grade)
   - [Gradebook](#gradebook)
   - [Settings](#settings)
5. [Auto-Grading Workflow](#auto-grading-workflow)
6. [File Formats](#file-formats)
7. [Tips & Best Practices](#tips--best-practices)

---

## Overview

NewGrader is a comprehensive grading application designed for teachers to:

- Manage classes and student rosters
- Create and track assignments with weighted grades
- Enter grades manually or use automated grading with answer keys
- View a complete gradebook with calculated averages and letter grades
- Export reports to Excel, CSV, or text summaries

### Key Features

| Feature | Description |
|---------|-------------|
| Class Management | Create and organize multiple classes |
| Student Roster | Add students individually or bulk import from CSV |
| Assignment Tracking | Create assignments with points, weights, and due dates |
| Manual Grading | Enter grades with an easy-to-use editable grid |
| Auto-Grading | Upload answer keys and grade student responses automatically |
| Gradebook | View all grades with weighted averages and letter grades |
| Configurable Scale | Customize grade thresholds (A/B/C/D/F) |
| Export Reports | Download grades as Excel, CSV, or summary reports |

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Navigate to the project directory:**
   ```powershell
   cd "C:\Users\lawry\Documents\Perso\Dr.G\NewGrader"
   ```

2. **Create and activate a virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```powershell
   streamlit run app.py
   ```

5. **Open in browser:**
   The app will automatically open at `http://localhost:8501`

---

## Getting Started

### Quick Start Workflow

1. **Create a Class** → Go to "Classes" and add your first class (e.g., "Math 101")
2. **Add Students** → Go to "Students", select your class, and add students
3. **Create Assignments** → Go to "Assignments" and create your first assignment
4. **Enter Grades** → Use "Grade Entry" for manual grading or "Auto-Grade" for automatic grading
5. **View Results** → Check the "Gradebook" to see all grades and statistics

---

## Features Guide

### Classes

The Classes page allows you to create and manage your teaching classes.

**Creating a Class:**
1. Click the "Add New Class" expander
2. Enter a class name (e.g., "English 9A", "Physics 101")
3. Click "Add Class"

**Viewing Classes:**
- All classes are displayed in a table showing:
  - Class ID
  - Class Name
  - Number of Students
  - Creation Date

**Deleting a Class:**
1. Select the class from the dropdown in the "Delete a Class" section
2. Click "Delete"
3. Confirm the deletion

> ⚠️ **Warning:** Deleting a class will also delete all students, assignments, and grades associated with that class.

---

### Students

The Students page manages student rosters for each class.

**Adding a Single Student:**
1. Select a class from the dropdown
2. Fill in the student name (required) and email (optional)
3. Click "Add Student"

**Bulk Import from CSV:**
1. Prepare a CSV file with columns: `name` (required), `email` (optional)
2. Select your class
3. Upload the CSV file
4. Preview the data and click "Import All Students"

**Example CSV format:**
```csv
name,email
John Smith,john@school.edu
Jane Doe,jane@school.edu
Bob Wilson,
```

**Editing Students:**
- The student table is editable - modify names or emails directly
- Click "Save Changes" to persist your edits

**Removing Students:**
1. Select the student from the dropdown
2. Click "Remove" and confirm

---

### Assignments

The Assignments page lets you create and manage assignments for each class.

**Creating an Assignment:**
1. Select a class
2. Click "Add New Assignment"
3. Fill in:
   - **Assignment Name** - e.g., "Chapter 1 Quiz"
   - **Max Points** - Maximum possible score (default: 100)
   - **Weight** - Grade weight multiplier (default: 1.0)
   - **Due Date** - Optional due date
4. Click "Add Assignment"

**Understanding Weight:**
- Weight determines how much an assignment counts toward the final grade
- Weight of 1.0 = normal importance
- Weight of 2.0 = counts double
- Weight of 0.5 = counts half

**Example:**
| Assignment | Max Points | Weight | Effective Weight |
|------------|------------|--------|------------------|
| Homework 1 | 50 | 1.0 | Normal |
| Midterm | 100 | 2.0 | Counts 2x |
| Participation | 20 | 0.5 | Counts 0.5x |

**Editing Assignments:**
1. Select the assignment from the dropdown
2. Modify any fields
3. Click "Save Changes"

---

### Grade Entry

The Grade Entry page provides manual grade input with an interactive grid.

**Entering Grades:**
1. Select a class
2. Select an assignment
3. The grade grid shows all students with columns:
   - Student Name (read-only)
   - Points (editable)
   - Comments (editable)
4. Enter scores directly in the grid
5. Click "Save All Grades"

**Features:**
- Existing grades are pre-loaded when editing
- Quick stats show: graded count, average, highest, lowest
- Points are validated against the assignment's max points

---

### Auto-Grade

The Auto-Grade page has two tabs: creating answer keys and grading responses.

#### Tab 1: Create Answer Key

**Setting Up an Answer Key:**
1. Select class and assignment
2. Set the number of questions
3. For each question, enter:
   - **Answer** - The correct response
   - **Points** - Points for this question
   - **Type** - Multiple choice, short text, or numeric
4. Click "Save Answer Key"

**Question Types:**

| Type | Description | Matching |
|------|-------------|----------|
| Multiple Choice | A, B, C, D answers | Exact match (case-insensitive) |
| Short Text | Text answers | Exact match (case-insensitive) |
| Numeric | Number answers | Within 0.01 tolerance |

#### Tab 2: Grade Responses

**Auto-Grading Workflow:**
1. Select class and assignment (must have an answer key)
2. Upload a CSV or Excel file with student responses
3. Click "Grade Responses"
4. Review results showing:
   - Score for each student
   - Percentage
   - Correct/incorrect count
5. Click "Save Grades to Database" to record the grades

---

### Gradebook

The Gradebook provides a comprehensive view of all grades for a class.

**Gradebook Matrix:**
- Rows: Students
- Columns: Each assignment + Average + Letter Grade
- Missing grades highlighted in red

**Calculated Fields:**
- **Average** - Weighted average across all assignments
- **Letter Grade** - Based on configured grade scale

**Statistics:**
- Class average
- Highest/lowest scores
- Passing rate (60%+)
- Grade distribution chart

**Export Options:**
1. **Excel** - Full gradebook with formatting
2. **CSV** - Simple comma-separated file
3. **Class Summary** - Text report with statistics

---

### Settings

The Settings page configures application-wide options.

**Grade Scale Configuration:**
Customize the percentage thresholds for letter grades:

| Grade | Default Minimum |
|-------|-----------------|
| A | 90% |
| B | 80% |
| C | 70% |
| D | 60% |
| F | Below 60% |

**Modifying the Scale:**
1. Enter new threshold values
2. Ensure they're in descending order (A > B > C > D)
3. Click "Save Grade Scale"

**Database Information:**
- View counts of classes, students, and assignments
- Database location: `data/grader.db`

---

## Auto-Grading Workflow

### Complete Auto-Grading Process

```
┌─────────────────┐
│ 1. Create Class │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 2. Add Students │
└────────┬────────┘
         ▼
┌─────────────────────┐
│ 3. Create Assignment│
└────────┬────────────┘
         ▼
┌─────────────────────┐
│ 4. Create Answer Key│
│   (Auto-Grade tab)  │
└────────┬────────────┘
         ▼
┌─────────────────────────┐
│ 5. Collect Student      │
│    Responses (CSV/Excel)│
└────────┬────────────────┘
         ▼
┌─────────────────────────┐
│ 6. Upload & Grade       │
│   (Auto-Grade tab)      │
└────────┬────────────────┘
         ▼
┌─────────────────────────┐
│ 7. Review & Save Grades │
└────────┬────────────────┘
         ▼
┌─────────────────────────┐
│ 8. View in Gradebook    │
└─────────────────────────┘
```

### Matching Students

When saving auto-graded results:
- Student names in the upload file are matched to database records
- Matching is case-insensitive
- Names must match exactly (consider standardizing names)
- Unmatched students are reported but not saved

---

## File Formats

### Student Import CSV

```csv
name,email
John Smith,john.smith@school.edu
Jane Doe,jane.doe@school.edu
Robert Johnson,
```

**Required columns:** `name`
**Optional columns:** `email`

### Student Response CSV (for Auto-Grading)

```csv
student_name,q1,q2,q3,q4,q5
John Smith,A,B,C,D,A
Jane Doe,A,C,C,D,B
Robert Johnson,B,B,C,D,A
```

**Required columns:** `student_name` (or `name` or `student`)
**Question columns:** `q1`, `q2`, `q3`, etc. (or `Q1`, `Question 1`, etc.)

### Alternative Column Naming

The auto-grader recognizes these column patterns:
- `q1`, `Q1`, `question1`, `Question 1`
- `student_name`, `name`, `student`, `Student Name`

---

## Tips & Best Practices

### Organization

1. **Naming Conventions**
   - Use consistent class names (e.g., "Math 101 - Fall 2024")
   - Use clear assignment names (e.g., "Ch1 Quiz", "Midterm Exam")

2. **Weights**
   - Plan your weights before creating assignments
   - Common scheme: Homework (1.0), Quizzes (1.5), Exams (2.0)

### Auto-Grading

1. **Answer Keys**
   - Double-check your answer key before grading
   - Use uppercase letters for multiple choice (A, B, C, D)
   - For short text, consider all acceptable variations

2. **Student Names**
   - Ensure student names in response files match database exactly
   - Use bulk import to standardize names from the start

### Data Management

1. **Regular Exports**
   - Export gradebook periodically as backup
   - Keep Excel exports for records

2. **Grade Entry**
   - Save frequently when entering many grades
   - Use comments for partial credit explanations

### Performance

1. **Large Classes**
   - Bulk import students rather than adding individually
   - Use auto-grading for objective assessments
   - Export to Excel for complex analysis

---

## Troubleshooting

### Common Issues

**"No classes found"**
- Create a class first before adding students or assignments

**"No students found"**
- Add students to the class before entering grades

**"Student not found" during auto-grade save**
- Student name in upload doesn't match database
- Check spelling and capitalization

**Grades not calculating**
- Ensure assignments have grades entered
- Check that weights are set correctly

### Getting Help

- Check the Settings page for database information
- The database is stored in `data/grader.db`
- All data persists between sessions

---

## Technical Reference

### Database Schema

```
classes
├── id (INTEGER PRIMARY KEY)
├── name (TEXT)
└── created_at (TIMESTAMP)

students
├── id (INTEGER PRIMARY KEY)
├── name (TEXT)
├── class_id (FK → classes)
├── email (TEXT)
└── created_at (TIMESTAMP)

assignments
├── id (INTEGER PRIMARY KEY)
├── name (TEXT)
├── class_id (FK → classes)
├── max_points (REAL)
├── weight (REAL)
├── due_date (TEXT)
└── created_at (TIMESTAMP)

grades
├── id (INTEGER PRIMARY KEY)
├── student_id (FK → students)
├── assignment_id (FK → assignments)
├── points (REAL)
├── comments (TEXT)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

answer_keys
├── id (INTEGER PRIMARY KEY)
├── assignment_id (FK → assignments)
├── question_num (INTEGER)
├── correct_answer (TEXT)
├── points (REAL)
└── question_type (TEXT)

settings
├── key (TEXT PRIMARY KEY)
└── value (TEXT)
```

### Grade Calculation Formula

```
Weighted Average = Σ(score_percentage × weight) / Σ(weight)

Where:
- score_percentage = (points_earned / max_points) × 100
- weight = assignment weight
```

---

*NewGrader - Built with Streamlit and SQLite*
