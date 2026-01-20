import streamlit as st
import pandas as pd

def render():
    """Render the Help & User Guide page."""

    # Page header
    st.markdown("""
    <div style="
        background-color: #1e3a5f;
        color: white;
        padding: 2rem;
        border-radius: 8px;
        margin-bottom: 2rem;
    ">
        <h1 style="margin: 0; font-size: 1.75rem; font-weight: 700; color: white;">Help & User Guide</h1>
        <p style="margin: 0.25rem 0 0 0; opacity: 0.9; font-size: 0.95rem; color: white;">Complete guide to using Grader</p>
    </div>
    """, unsafe_allow_html=True)

    # Create sub-tabs for different help sections
    help_tabs = st.tabs([
        "🚀 Quick Start",
        "📚 Features Guide",
        "🎯 Workflows",
        "❓ FAQ",
        "💡 Tips & Tricks"
    ])

    with help_tabs[0]:
        render_quick_start()

    with help_tabs[1]:
        render_features_guide()

    with help_tabs[2]:
        render_workflows()

    with help_tabs[3]:
        render_faq()

    with help_tabs[4]:
        render_tips()


def render_quick_start():
    """Render the Quick Start guide."""

    st.markdown("""
    ### 🎯 Getting Started with Grader

    Follow these simple steps to start grading efficiently:
    """)

    # Step-by-step guide with cards
    steps = [
        {
            "num": "1",
            "title": "Create a Class",
            "content": "Go to the **Classes** tab and create your first class (e.g., 'Math 101', 'History 2024')",
            "color": "#1e3a5f"
        },
        {
            "num": "2",
            "title": "Add Students",
            "content": "Navigate to **Students** tab, select your class, and add students individually or bulk import via CSV",
            "color": "#3182ce"
        },
        {
            "num": "3",
            "title": "Create Assignments",
            "content": "In the **Assignments** tab, create assignments with points and weights (e.g., 'Quiz 1' - 20 points, weight 1.0)",
            "color": "#38a169"
        },
        {
            "num": "4",
            "title": "Enter Grades",
            "content": "Use **Grade Entry** for manual grading or **Auto-Grade** for automatic grading with answer keys",
            "color": "#d69e2e"
        },
        {
            "num": "5",
            "title": "View & Export",
            "content": "Check the **Gradebook** to view all grades and export reports in Excel, CSV, or text format",
            "color": "#e53e3e"
        }
    ]

    cols = st.columns(5)
    for i, step in enumerate(steps):
        with cols[i]:
            st.markdown(f"""
            <div style="
                background: {step['color']};
                color: white;
                padding: 1.5rem;
                border-radius: 8px;
                text-align: center;
                height: 200px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <div style="font-size: 2rem; font-weight: 700; color: white; margin-bottom: 0.5rem;">
                    {step['num']}
                </div>
                <div style="font-size: 0.9rem; font-weight: 600; color: white; margin-bottom: 0.5rem;">
                    {step['title']}
                </div>
                <div style="font-size: 0.8rem; opacity: 0.9; color: white;">
                    {step['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Video placeholder
    st.markdown("""
    ### 📺 Video Tutorial

    > **Coming Soon**: Step-by-step video walkthrough of Grader

    ---

    ### 📊 Sample Data

    Want to try Grader with sample data? Here's a quick setup:

    1. **Sample Class**: "Demo Class 2024"
    2. **Sample Students**: Download our [sample student CSV](#)
    3. **Sample Assignments**: Homework (20%), Quizzes (30%), Midterm (20%), Final (30%)
    """)


def render_features_guide():
    """Render detailed features guide."""

    st.markdown("### 📋 Feature Overview")

    # Features in expandable sections
    with st.expander("🎓 Classes Management", expanded=True):
        st.markdown("""
        **What you can do:**
        - Create unlimited classes
        - Edit class names
        - Delete classes (⚠️ deletes all associated data)
        - View student count per class

        **How to use:**
        1. Navigate to the **Classes** tab
        2. Enter a class name and click "Create Class"
        3. View all classes in the table below
        4. Edit names inline by clicking on them
        5. Delete classes using the delete section

        **Tips:**
        - Use descriptive names like "Math 101 - Fall 2024"
        - Classes are the foundation - create them first!
        """)

    with st.expander("👥 Student Roster"):
        st.markdown("""
        **What you can do:**
        - Add individual students with name, ID, and email
        - Bulk import students from CSV files
        - Edit student information inline
        - Remove students from classes

        **Student ID Feature (New!):**
        - Each student can have a unique identifier
        - Helps prevent duplicate entries
        - Used for auto-grading matching

        **CSV Format for Bulk Import:**
        ```
        name,student_id,email
        John Smith,12345678,john@school.edu
        Jane Doe,87654321,jane@school.edu
        ```

        **Tips:**
        - Student IDs are optional but recommended
        - Use consistent ID format (e.g., 8-digit numbers)
        """)

    with st.expander("📝 Assignments"):
        st.markdown("""
        **What you can do:**
        - Create assignments with custom point values
        - Set weights for weighted grade calculation
        - Add due dates for organization
        - Edit or delete assignments

        **Understanding Weights:**
        - Weight determines how much an assignment counts toward final grade
        - Example: If Quiz has weight 1 and Final has weight 3, the Final counts 3x more
        - All weights are relative to each other

        **Example Setup:**
        | Assignment | Points | Weight | Impact |
        |-----------|--------|--------|---------|
        | Homework  | 10     | 1.0    | 10%     |
        | Quiz      | 20     | 2.0    | 20%     |
        | Midterm   | 100    | 3.0    | 30%     |
        | Final     | 100    | 4.0    | 40%     |
        """)

    with st.expander("✏️ Grade Entry"):
        st.markdown("""
        **Manual Grade Entry:**
        1. Select class and assignment
        2. Enter points for each student
        3. Add optional comments
        4. Click "Save All Grades"

        **Features:**
        - See live statistics (graded count, average, highest, lowest)
        - Points are validated against max points
        - Comments for individual feedback
        - Bulk save all changes at once

        **Tips:**
        - Use Tab key to move between cells quickly
        - Leave blank for ungraded
        - Comments are optional but helpful for student feedback
        """)

    with st.expander("🤖 Auto-Grade"):
        st.markdown("""
        **Two-Step Process:**

        **Step 1: Create Answer Key**
        - Select class and assignment
        - Enter correct answers for each question
        - Set points per question
        - Choose question type (multiple choice, short text, numeric)

        **Step 2: Grade Responses**
        - Upload CSV/Excel with student responses
        - System automatically matches answers
        - Review results before saving
        - Save grades to database

        **Response File Format:**
        ```
        student_name,q1,q2,q3,q4,q5
        John Smith,A,B,C,A,D
        Jane Doe,B,B,C,D,D
        ```

        Or use student IDs:
        ```
        student_id,q1,q2,q3,q4,q5
        12345678,A,B,C,A,D
        87654321,B,B,C,D,D
        ```

        **Question Types:**
        - **Multiple Choice**: Exact match (A, B, C, D)
        - **Short Text**: Case-insensitive match
        - **Numeric**: Within 0.01 tolerance
        """)

    with st.expander("📊 Gradebook"):
        st.markdown("""
        **Features:**
        - View all grades in one place
        - Weighted average calculation
        - Letter grade assignment
        - Color-coded grade distribution
        - Export capabilities

        **Export Options:**
        1. **Excel (.xlsx)**: Full formatting, ready for records
        2. **CSV**: For data analysis or import elsewhere
        3. **Text Summary**: Human-readable report

        **Grade Statistics:**
        - Class average
        - Highest/lowest scores
        - Passing rate (60%+)
        - Grade distribution (A-F)

        **Visual Indicators:**
        - Red background for missing assignments
        - Color-coded grade cards
        - Distribution charts
        """)

    with st.expander("⚙️ Settings"):
        st.markdown("""
        **Grade Scale Configuration:**
        - Customize letter grade thresholds
        - Default: A=90%, B=80%, C=70%, D=60%, F=below 60%
        - Changes apply to all classes

        **Database Management:**
        - View database statistics
        - Location: `data/grader.db`
        - Reset option available (⚠️ deletes all data)

        **Tips:**
        - Backup your database file regularly
        - Export gradebooks before resetting
        """)


def render_workflows():
    """Render common workflows."""

    st.markdown("### 🎯 Common Grading Workflows")

    workflow_choice = st.selectbox(
        "Select a workflow to learn about:",
        [
            "End-to-End Grading Process",
            "Setting Up a New Semester",
            "Grading a Quiz/Exam",
            "Mid-Semester Grade Reports",
            "Final Grade Calculation",
            "Handling Make-up Work"
        ]
    )

    if workflow_choice == "End-to-End Grading Process":
        st.markdown("""
        #### Complete Grading Workflow

        **1️⃣ Initial Setup (Beginning of Term)**
        - Create class(es)
        - Import student roster
        - Plan and create all assignments with weights

        **2️⃣ Regular Grading**
        - After each assignment, enter or auto-grade
        - Review gradebook periodically
        - Export reports for records

        **3️⃣ Final Grades**
        - Ensure all assignments are graded
        - Review weighted averages
        - Export final gradebook
        - Archive or reset for next term
        """)

    elif workflow_choice == "Setting Up a New Semester":
        st.markdown("""
        #### New Semester Setup

        **Week 1: Foundation**
        ```
        1. Classes Tab → Create all classes
        2. Students Tab → Import rosters (CSV recommended)
        3. Verify student IDs are unique
        ```

        **Week 2: Assignment Planning**
        ```
        1. Assignments Tab → Create all planned assignments
        2. Set appropriate weights (total = 100%)
        3. Add due dates for organization
        ```

        **Ongoing: Maintenance**
        ```
        - Add/drop students as needed
        - Adjust assignment weights if syllabus changes
        - Regular backups of database
        ```
        """)

    elif workflow_choice == "Grading a Quiz/Exam":
        st.markdown("""
        #### Efficient Quiz/Exam Grading

        **Option A: Auto-Grade (Multiple Choice)**
        1. Create assignment in Assignments tab
        2. Go to Auto-Grade → Create Answer Key
        3. Enter correct answers and points
        4. Collect responses in spreadsheet
        5. Upload to Grade Responses
        6. Review and save to database

        **Option B: Manual Entry (Essay/Mixed)**
        1. Create assignment
        2. Grade papers offline
        3. Go to Grade Entry
        4. Enter scores for each student
        5. Add comments if needed
        6. Save all grades

        **Time-Saving Tip**: Use Auto-Grade for objective questions, manual for subjective
        """)

    elif workflow_choice == "Mid-Semester Grade Reports":
        st.markdown("""
        #### Generating Progress Reports

        **Steps:**
        1. Ensure all grades to-date are entered
        2. Go to Gradebook tab
        3. Select the class
        4. Review statistics (average, distribution)
        5. Export to Excel for formatting
        6. Add comments in Excel if needed
        7. Share with students/parents

        **What to Include:**
        - Current weighted average
        - Letter grade
        - Missing assignments (shown in red)
        - Class rank (calculate in Excel)
        """)

    elif workflow_choice == "Final Grade Calculation":
        st.markdown("""
        #### End-of-Term Grade Calculation

        **Checklist:**
        - [ ] All assignments graded
        - [ ] Weights sum to intended total
        - [ ] Review grade scale in Settings
        - [ ] Check for missing assignments
        - [ ] Export final gradebook

        **Final Steps:**
        1. Gradebook → Select class
        2. Verify all grades are complete
        3. Review weighted averages
        4. Export to Excel
        5. Submit grades to registrar
        6. Save backup of database
        """)

    elif workflow_choice == "Handling Make-up Work":
        st.markdown("""
        #### Managing Late/Make-up Assignments

        **Scenario 1: Same Assignment, Late Submission**
        - Grade Entry → Select original assignment
        - Enter grade with comment "Late submission"
        - Apply penalty manually if needed

        **Scenario 2: Alternative Assignment**
        - Create new assignment (e.g., "Quiz 1 - Makeup")
        - Set same weight as original
        - Grade only for applicable students

        **Tip**: Use comments field to track special circumstances
        """)


def render_faq():
    """Render FAQ section."""

    st.markdown("### ❓ Frequently Asked Questions")

    faqs = [
        {
            "q": "Can I import grades from other systems?",
            "a": "Yes! Use the Auto-Grade feature with a CSV file containing student names/IDs and their responses. You can also manually enter grades in the Grade Entry tab."
        },
        {
            "q": "What happens if I delete a class?",
            "a": "Deleting a class removes ALL associated data including students, assignments, and grades. Always export your gradebook before deleting."
        },
        {
            "q": "How are weighted grades calculated?",
            "a": "Each assignment's percentage score is multiplied by its weight, then all weighted scores are summed and divided by total weights. Example: (Quiz: 80% × weight 1) + (Final: 90% × weight 2) = weighted average."
        },
        {
            "q": "Can multiple teachers use the same gradebook?",
            "a": "Grader is designed for single-user access. Each teacher should run their own instance. You can share the database file, but not simultaneously."
        },
        {
            "q": "How do I backup my grades?",
            "a": "1) Export gradebooks regularly (Excel/CSV), 2) Copy the database file at `data/grader.db`, 3) Use Settings → Export for full backups."
        },
        {
            "q": "Can I change grades after saving?",
            "a": "Yes! Simply go back to Grade Entry, select the assignment, modify the grades, and save again. Changes overwrite previous values."
        },
        {
            "q": "What's the difference between points and weights?",
            "a": "Points = the maximum score for an assignment. Weight = how much that assignment counts toward the final grade. A 10-point quiz can have the same weight as a 100-point exam."
        },
        {
            "q": "How do I handle extra credit?",
            "a": "Create an assignment called 'Extra Credit' with appropriate points and a small weight. Students who don't complete it will have it count as 0."
        },
        {
            "q": "Can I customize the letter grade scale?",
            "a": "Yes! Go to Settings tab and adjust the percentage thresholds for each letter grade. Changes apply to all classes."
        },
        {
            "q": "What file formats are supported for import/export?",
            "a": "Import: CSV, Excel (.xlsx) for student rosters and grade uploads. Export: Excel, CSV, and text summary formats."
        }
    ]

    for faq in faqs:
        with st.expander(f"**{faq['q']}**"):
            st.write(faq['a'])


def render_tips():
    """Render tips and tricks section."""

    st.markdown("### 💡 Pro Tips & Best Practices")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        #### ⚡ Efficiency Tips

        **Keyboard Shortcuts:**
        - Tab: Move between input fields
        - Enter: Submit forms
        - Ctrl+A: Select all in data editor

        **Bulk Operations:**
        - Import students via CSV instead of one-by-one
        - Use Auto-Grade for objective assessments
        - Export all grades at once

        **Organization:**
        - Use consistent naming (e.g., "Quiz 1", "Quiz 2")
        - Add due dates to track timeline
        - Include year in class names
        """)

        st.markdown("""
        #### 🎯 Grading Strategies

        **Weight Distribution:**
        - Homework: 20-30%
        - Quizzes: 20-30%
        - Midterm: 20-25%
        - Final: 25-30%
        - Participation: 5-10%

        **Missing Work:**
        - Leave blank (not 0) until deadline
        - Use comments to note "Excused"
        - Create makeup assignments separately
        """)

    with col2:
        st.markdown("""
        #### 🛡️ Data Safety

        **Regular Backups:**
        1. Weekly: Export gradebooks to Excel
        2. Monthly: Copy database file
        3. End of term: Full export + database

        **Before Major Changes:**
        - Export current gradebook
        - Copy database file
        - Test with one item first

        **Database Location:**
        ```
        Windows: C:\\Users\\[you]\\Documents\\...\\Grader\\data\\grader.db
        Mac/Linux: ~/Documents/.../Grader/data/grader.db
        ```
        """)

        st.markdown("""
        #### 🚀 Advanced Usage

        **Custom Workflows:**
        - Create "Participation" assignments for daily grades
        - Use weight 0 for practice assignments
        - Negative points for deductions

        **Integration Ideas:**
        - Export to Excel → Mail merge for reports
        - Import from Google Forms responses
        - Use student IDs to match school systems

        **Performance:**
        - Works smoothly with 500+ students
        - No internet required (local database)
        - Auto-saves on every action
        """)

    # Additional resources
    st.markdown("---")
    st.markdown("""
    ### 📚 Additional Resources

    - **GitHub Repository**: [Grader on GitHub](https://github.com/YourRepo/Grader)
    - **Report Issues**: Use GitHub Issues for bug reports
    - **Video Tutorials**: Coming soon
    - **Sample Data Sets**: Available in `/samples` folder

    ### 📧 Need More Help?

    If you can't find what you're looking for:
    1. Check the FAQ section above
    2. Try the search feature (Ctrl+F)
    3. Submit an issue on GitHub
    4. Contact support

    ---

    <div style="text-align: center; padding: 2rem; background: #f7fafc; border-radius: 8px;">
        <p style="color: #718096; margin: 0;">
            Grader v1.0 • Built with ❤️ for educators
        </p>
    </div>
    """, unsafe_allow_html=True)