# NewGrader

A professional grading application for educators built with Streamlit and SQLite.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Features

- **Class Management** - Create and organize multiple classes
- **Student Roster** - Add students individually or bulk import from CSV
- **Assignment Tracking** - Create assignments with points and weights
- **Grade Entry** - Manual grade entry with inline editing
- **Auto-Grading** - Create answer keys and automatically grade student responses
- **Gradebook** - View comprehensive gradebook with weighted averages and letter grades
- **Export Reports** - Download grades as Excel, CSV, or text summary
- **Configurable Grade Scale** - Customize A/B/C/D/F thresholds

## Screenshots

The application features a clean, professional Navy Blue & White theme:

| Home Dashboard | Gradebook |
|----------------|-----------|
| Statistics overview and quick start guide | Full gradebook with grade distribution |

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/bomino/newgrader.git
   cd newgrader
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

1. **Create a Class** - Go to "Classes" and add your first class (e.g., "Math 101")
2. **Add Students** - Navigate to "Students", select your class, and add students individually or import from CSV
3. **Create Assignments** - Go to "Assignments" to create quizzes, tests, or homework with point values and weights
4. **Enter Grades** - Use "Grade Entry" for manual grading or "Auto-Grade" for automatic grading with answer keys
5. **View Gradebook** - Check "Gradebook" to see all grades, statistics, and export reports

### Auto-Grading

1. Create an answer key in the "Auto-Grade" tab
2. Prepare a CSV file with columns: `student_name, q1, q2, q3, ...`
3. Upload the file and click "Grade Responses"
4. Review results and save to database

### CSV Import Format

For bulk student import:
```csv
name,email
John Smith,john@school.edu
Jane Doe,jane@school.edu
```

For auto-grading responses:
```csv
student_name,q1,q2,q3,q4,q5
John Smith,A,B,C,A,D
Jane Doe,A,B,C,A,B
```

## Project Structure

```
newgrader/
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── pytest.ini            # Test configuration
├── modules/
│   ├── database.py       # Database operations
│   ├── styles.py         # UI theming (Navy Blue & White)
│   └── pages/            # Page modules
│       ├── classes.py
│       ├── students.py
│       ├── assignments.py
│       ├── grade_entry.py
│       ├── auto_grade.py
│       ├── gradebook.py
│       └── settings.py
├── tests/                # Playwright tests
│   ├── test_sidebar.py
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
pytest tests/test_sidebar.py -v
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

The application uses a professional Navy Blue & White color scheme:
- Primary: `#1e3a5f` (Navy Blue)
- Accent: `#3182ce` (Blue)
- Success: `#38a169` (Green)
- Warning: `#d69e2e` (Gold)
- Danger: `#e53e3e` (Red)

## Tech Stack

- **[Streamlit](https://streamlit.io/)** - Web application framework
- **[SQLite](https://www.sqlite.org/)** - Embedded database
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
- Designed with a focus on usability and clean aesthetics
