# Grader User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation & Setup](#installation--setup)
3. [Quick Start Guide](#quick-start-guide)
4. [Features Overview](#features-overview)
5. [Detailed Feature Guide](#detailed-feature-guide)
6. [Common Workflows](#common-workflows)
7. [Tips & Best Practices](#tips--best-practices)
8. [Troubleshooting](#troubleshooting)
9. [FAQ](#faq)

---

## Introduction

Grader is a professional grading application designed for educators to efficiently manage classes, students, assignments, and grades. Built with simplicity and functionality in mind, it provides both manual and automatic grading capabilities.

### Key Features
- 📚 Multi-class management
- 👥 Student roster with unique IDs
- 📝 Flexible assignment creation with weights
- ✏️ Manual grade entry
- 🤖 Automatic grading with answer keys
- 📊 Comprehensive gradebook with statistics
- 📥 Multiple export formats (Excel, CSV, Text)
- ⚙️ Customizable grade scales

---

## Installation & Setup

### Requirements
- Python 3.8 or higher
- Windows, macOS, or Linux

### Installation Steps

1. **Clone or download the repository**
```bash
git clone https://github.com/YourRepo/Grader.git
cd Grader
```

2. **Create a virtual environment**
```bash
python -m venv venv
```

3. **Activate the virtual environment**
- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Run the application**
```bash
streamlit run app_tabbed.py
```

The application will open in your browser at `http://localhost:8501`

---

## Quick Start Guide

### 5-Step Setup Process

#### Step 1: Create a Class
1. Navigate to the **Classes** tab
2. Enter a class name (e.g., "Math 101 - Fall 2024")
3. Click "Create Class"

#### Step 2: Add Students
1. Go to the **Students** tab
2. Select your class
3. Either:
   - Add students individually with name, ID, and email
   - Bulk import from CSV file

#### Step 3: Create Assignments
1. Open the **Assignments** tab
2. Select your class
3. Add assignments with:
   - Name (e.g., "Quiz 1")
   - Max points
   - Weight (relative importance)
   - Due date (optional)

#### Step 4: Enter Grades
Choose one of two methods:

**Manual Entry:**
- Go to **Grade Entry** tab
- Select class and assignment
- Enter points for each student

**Auto-Grade:**
- Go to **Auto-Grade** tab
- Create an answer key
- Upload student responses

#### Step 5: View & Export Gradebook
1. Navigate to **Gradebook** tab
2. View calculated grades and statistics
3. Export in your preferred format

---

## Features Overview

### Navigation Structure
The application uses a tab-based navigation system with nine main sections:

| Tab | Purpose |
|-----|---------|
| 🏠 Home | Dashboard with statistics and quick access |
| 🎓 Classes | Create and manage classes |
| 👥 Students | Manage student rosters |
| 📝 Assignments | Create and configure assignments |
| ✏️ Grade Entry | Manually enter grades |
| 🤖 Auto-Grade | Automatic grading with answer keys |
| 📊 Gradebook | View all grades and statistics |
| ⚙️ Settings | Configure grade scales and manage database |
| ❓ Help | In-app documentation and guides |

---

## Detailed Feature Guide

### Classes Management

**Creating a Class:**
- Enter a descriptive name
- Recommended format: "Subject Code - Term Year"
- Examples: "MATH 101 - Fall 2024", "History AP - Spring 2025"

**Managing Classes:**
- Edit class names inline by clicking on them
- View student count for each class
- Delete classes (⚠️ Warning: Deletes all associated data)

### Student Roster

**Adding Students Individually:**
- **Name** (Required): Full student name
- **Student ID** (Optional): Unique identifier (e.g., school ID number)
- **Email** (Optional): Student email for records

**Bulk Import via CSV:**
CSV file format:
```csv
name,student_id,email
John Smith,12345678,john@school.edu
Jane Doe,87654321,jane@school.edu
Sarah Johnson,11223344,sarah@school.edu
```

**Student ID Feature:**
- Helps prevent duplicate entries
- Used for matching in auto-grading
- Optional but recommended for larger classes

### Assignments

**Creating Assignments:**
- **Name**: Clear, descriptive name
- **Max Points**: Maximum possible score
- **Weight**: Relative importance in final grade
- **Due Date**: Optional, for organization

**Understanding Weights:**
Weights determine how much each assignment counts toward the final grade.

Example weight distribution:
| Assignment Type | Weight | Percentage of Final Grade |
|----------------|--------|--------------------------|
| Homework | 1.0 | 10% |
| Quizzes | 2.0 | 20% |
| Midterm | 3.0 | 30% |
| Final Exam | 4.0 | 40% |
| **Total** | **10.0** | **100%** |

### Grade Entry

**Manual Grade Entry Process:**
1. Select class and assignment
2. View all students with current grades
3. Enter points (validated against max points)
4. Add optional comments for feedback
5. Click "Save All Grades" to commit changes

**Features:**
- Real-time statistics (average, highest, lowest)
- Missing assignments shown as dashes
- Bulk save functionality
- Student IDs displayed for verification

### Auto-Grade

**Two-Step Process:**

#### Step 1: Create Answer Key
1. Select class and assignment
2. Set number of questions
3. For each question, specify:
   - Correct answer
   - Points value
   - Question type (multiple choice, short text, numeric)
4. Save answer key

#### Step 2: Grade Responses
1. Prepare response file (CSV or Excel)
2. Upload file
3. System automatically:
   - Detects student identifiers
   - Matches answers to key
   - Calculates scores
4. Review results
5. Save to database

**Response File Formats:**

Using student names:
```csv
student_name,q1,q2,q3,q4,q5
John Smith,A,B,C,A,D
Jane Doe,B,B,C,D,D
```

Using student IDs:
```csv
student_id,q1,q2,q3,q4,q5
12345678,A,B,C,A,D
87654321,B,B,C,D,D
```

**Question Types:**
- **Multiple Choice**: Exact match (case-insensitive)
- **Short Text**: Case-insensitive string match
- **Numeric**: Number within 0.01 tolerance

### Gradebook

**Features:**
- Complete grade matrix for all students and assignments
- Weighted average calculation
- Letter grade assignment based on scale
- Color coding:
  - Red background: Missing assignments
  - Colored cards: Grade distribution

**Statistics Displayed:**
- Class average
- Highest/lowest scores
- Passing rate (60%+)
- Grade distribution (A through F)

**Export Options:**
1. **Excel (.xlsx)**: Formatted spreadsheet with all data
2. **CSV (.csv)**: Raw data for analysis
3. **Text Summary (.txt)**: Human-readable report

### Settings

**Grade Scale Configuration:**
Customize letter grade thresholds:
- Default: A ≥ 90%, B ≥ 80%, C ≥ 70%, D ≥ 60%, F < 60%
- Modify to match your institution's standards

**Database Management:**
- View statistics (classes, students, assignments)
- Database location: `data/grader.db`
- Reset option (⚠️ Deletes all data)

---

## Common Workflows

### Setting Up a New Semester

1. **Week 1: Foundation**
   - Create all classes
   - Import student rosters
   - Verify student information

2. **Week 2: Assignment Planning**
   - Create all planned assignments
   - Set appropriate weights
   - Add due dates

3. **Ongoing: Grading**
   - Enter grades after each assignment
   - Monitor class performance
   - Export reports as needed

### Grading a Multiple Choice Test

1. Create the assignment (Assignments tab)
2. Create answer key (Auto-Grade → Create Answer Key)
3. Collect student responses in spreadsheet
4. Upload responses (Auto-Grade → Grade Responses)
5. Review and save grades

### Generating Progress Reports

1. Ensure all current grades are entered
2. Go to Gradebook tab
3. Review statistics and distribution
4. Export to Excel
5. Add additional comments if needed
6. Share with students/parents

### End-of-Term Grade Calculation

1. Verify all assignments are graded
2. Check weight distribution totals correctly
3. Review grade scale in Settings
4. Export final gradebook
5. Submit grades to registrar
6. Backup database file

---

## Tips & Best Practices

### Efficiency Tips

**Keyboard Shortcuts:**
- Tab: Navigate between fields
- Enter: Submit forms
- Ctrl+A: Select all in data editor

**Naming Conventions:**
- Classes: Include year and term
- Assignments: Use consistent numbering
- Students: Last name, First name format

### Grade Management

**Weight Strategies:**
- Start with simple weights (1, 2, 3, 4)
- Adjust based on syllabus percentages
- Total weights don't need to equal 100

**Handling Missing Work:**
- Leave blank until deadline
- Use comments for "Excused" absences
- Enter 0 only after deadline passes

### Data Safety

**Regular Backups:**
1. Weekly: Export gradebooks
2. Monthly: Copy database file
3. End of term: Complete export

**Database Location:**
- Windows: `C:\Users\[username]\...\Grader\data\grader.db`
- macOS/Linux: `~/Grader/data/grader.db`

### Performance Optimization

- Works efficiently with 500+ students
- No internet required (local database)
- Auto-saves after each action
- Use bulk operations when possible

---

## Troubleshooting

### Common Issues

**Application won't start:**
- Verify Python 3.8+ is installed
- Check all dependencies are installed
- Ensure port 8501 is available

**Can't see file uploader in Auto-Grade:**
- Ensure you've created an answer key first
- Check that the assignment exists
- Verify class has students

**Grades not calculating correctly:**
- Check assignment weights
- Verify all grades are entered
- Review grade scale settings

**Database errors:**
- Check file permissions on data folder
- Ensure sufficient disk space
- Try restarting the application

### Getting Help

1. Check the in-app Help tab
2. Review this documentation
3. Check FAQ section
4. Report issues on GitHub

---

## FAQ

**Q: Can I use Grader for multiple subjects?**
A: Yes! Create separate classes for each subject. The application handles unlimited classes.

**Q: Is my data secure?**
A: Data is stored locally on your computer. No internet connection required for operation.

**Q: Can I share the gradebook with students?**
A: Export to Excel or PDF and share. The application itself is single-user.

**Q: How do I handle curved grades?**
A: Export to Excel, apply curve formula, then import back using Grade Entry.

**Q: Can I customize beyond the provided options?**
A: The application is open-source. Modify the code to suit your needs.

**Q: What's the maximum number of students/assignments?**
A: No hard limit. Tested successfully with 500+ students and 50+ assignments.

**Q: Can I use decimal points for grades?**
A: Yes! The system supports decimal values (e.g., 87.5 points).

**Q: How do I handle group projects?**
A: Create one assignment and enter the same grade for all group members.

**Q: Can I import from other grading systems?**
A: Yes, if you can export to CSV. Format the data to match Grader's structure.

**Q: Is there a mobile version?**
A: The web interface is mobile-responsive but optimized for desktop use.

---

## Conclusion

Grader streamlines the grading process while maintaining flexibility for various teaching styles and requirements. Regular backups and exports ensure your data is always safe and accessible.

For additional support or feature requests, please visit the GitHub repository.

---

**Version:** 1.0
**Last Updated:** January 2024
**License:** MIT
**Author:** Grader Development Team