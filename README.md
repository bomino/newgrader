# Grader

A professional grading application for educators built with Streamlit and SQLite.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Features

- **Class Management** - Create and organize multiple classes
- **Student Roster** - Add students individually or bulk import from CSV with unique student IDs
- **Assignment Tracking** - Create assignments with points and weights
- **Grade Entry** - Manual grade entry with inline editing
- **Auto-Grading** - Create answer keys and automatically grade student responses
- **Gradebook** - View comprehensive gradebook with weighted averages and letter grades
- **Export Reports** - Download grades as Excel, CSV, or text summary
- **Configurable Grade Scale** - Customize A/B/C/D/F thresholds
- **In-App Help Guide** - Comprehensive documentation and tutorials built-in
- **Tab Navigation** - Clean, intuitive tab-based interface

## What's New

- ✨ **Rebranded to "Grader"** - Simplified, professional name
- 📑 **Tab-Based Navigation** - Modern, accessible interface without sidebar
- 🆔 **Student ID Support** - Track students with unique identifiers
- 📖 **Comprehensive Help System** - Built-in user guide with tutorials
- 🦶 **Professional Footer** - Version info and branding

## Screenshots

The application features a clean, professional Navy Blue & White theme with tab-based navigation:

| Home Dashboard | Gradebook | Help Guide |
|----------------|-----------|------------|
| Statistics overview and quick start guide | Full gradebook with grade distribution | In-app tutorials and documentation |

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/bomino/grader.git
   cd grader
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv

   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1

   # Windows (cmd)
   venv\Scripts\activate.bat

   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**

   Navigate to `http://localhost:8501`

## Usage Guide

### Getting Started

1. **Create a Class** - Navigate to "🎓 Classes" tab and add your first class (e.g., "Math 101")
2. **Add Students** - Go to "👥 Students" tab, select your class, and add students with optional IDs
3. **Create Assignments** - Use "📝 Assignments" tab to create quizzes, tests, or homework
4. **Enter Grades** - Use "✏️ Grade Entry" for manual grading or "🤖 Auto-Grade" for automatic grading
5. **View Gradebook** - Check "📊 Gradebook" tab to see all grades and export reports
6. **Get Help** - Visit "❓ Help" tab for comprehensive guides and tutorials

### Student Management

Add students with unique identifiers:
- **Name** (Required): Student's full name
- **Student ID** (Optional): Unique identifier (e.g., university ID)
- **Email** (Optional): Student's email address

### Auto-Grading

1. Create an answer key in the "Auto-Grade" tab
2. Prepare a CSV/Excel file with student responses
3. Upload the file and click "Grade Responses"
4. Review results and save to database

Supports matching by both student names and IDs for flexible grading.

### CSV Import Formats

For bulk student import:
```csv
name,student_id,email
John Smith,12345678,john@school.edu
Jane Doe,87654321,jane@school.edu
```

For auto-grading responses (using names):
```csv
student_name,q1,q2,q3,q4,q5
John Smith,A,B,C,A,D
Jane Doe,A,B,C,A,B
```

For auto-grading responses (using student IDs):
```csv
student_id,q1,q2,q3,q4,q5
12345678,A,B,C,A,D
87654321,A,B,C,A,B
```

## Project Structure

```
grader/
├── app.py                 # Main application with tab navigation
├── requirements.txt       # Python dependencies
├── pytest.ini            # Test configuration
├── docs/
│   └── USER_GUIDE.md     # Comprehensive user documentation
├── modules/
│   ├── database.py       # Database operations with migrations
│   ├── styles_tabbed.py  # UI theming for tab navigation
│   └── pages/            # Page modules
│       ├── classes.py
│       ├── students.py
│       ├── assignments.py
│       ├── grade_entry.py
│       ├── auto_grade.py
│       ├── gradebook.py
│       ├── settings.py
│       └── help_guide.py # In-app help system
├── tests/                # Playwright tests
│   └── screenshots/
└── data/
    └── grader.db         # SQLite database (auto-created)
```

## Testing

The project includes Playwright tests for UI verification.

```bash
# Install test dependencies
pip install pytest pytest-playwright playwright
playwright install chromium

# Start the app in one terminal
streamlit run app.py --server.port 8502

# Run tests in another terminal
pytest tests/ -v
```

## Configuration

### Grade Scale

Default grade scale (customizable in Settings):
- **A**: 90-100%
- **B**: 80-89%
- **C**: 70-79%
- **D**: 60-69%
- **F**: Below 60%

### Theming

The application uses a professional Navy Blue & White color scheme with enhanced accessibility:
- Primary: `#1e3a5f` (Navy Blue)
- Accent: `#3182ce` (Blue)
- Success: `#38a169` (Green)
- Warning: `#d69e2e` (Gold)
- Danger: `#e53e3e` (Red)

All text on colored backgrounds uses white for WCAG compliance.

## Tech Stack

- **[Streamlit](https://streamlit.io/)** - Web application framework
- **[SQLite](https://www.sqlite.org/)** - Embedded database with migrations
- **[Pandas](https://pandas.pydata.org/)** - Data manipulation
- **[openpyxl](https://openpyxl.readthedocs.io/)** - Excel export
- **[Playwright](https://playwright.dev/)** - UI testing

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for educators who need a simple, effective grading solution
- Designed with a focus on usability, accessibility, and clean aesthetics
- Tab-based navigation for improved user experience

## Version History

### Version 1.0 (January 2024)
- Rebranded from NewGrader to Grader
- Implemented tab-based navigation
- Added student ID support with database migration
- Created comprehensive in-app help system
- Added professional footer
- Enhanced accessibility with proper text contrast
- Consolidated application structure