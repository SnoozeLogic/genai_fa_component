# Analytics Feature Guide

## Overview
The Analytics feature provides comprehensive insights into student assignment submissions, including aggregate statistics, performance metrics, and downloadable reports.

## Features

### 📊 Key Statistics Dashboard
- **Total Students**: Count of all student repositories
- **Total Commits**: Aggregate commit count across all students
- **Average Commits**: Mean commits per student
- **Languages Used**: Total unique programming languages detected

### 📈 Analysis Progress
- Visual progress bars showing analyzed vs. pending repositories
- Percentage-based tracking of completion status

### 💻 Programming Language Distribution
- Language usage statistics with byte counts
- Percentage breakdown of codebase composition
- Automatic aggregation across all student repositories
- Visual bars showing relative language usage

### 🏆 Performance Metrics
- **Average Score**: Mean performance score across all analyzed repositories
- **Highest/Lowest Scores**: Range of performance
- **Score Distribution**:
  - Excellent (90+)
  - Good (75-89)
  - Average (60-74)
  - Needs Work (<60)

### ⭐ Top Performers
- Top 5 students ranked by performance score
- Displays commit count for each top performer
- Color-coded badges for quick identification

### 🔥 Most Active Students
- Top 5 students ranked by commit count
- Shows number of languages used
- Green badges indicating activity level

### 📋 Complete Student Overview
Comprehensive table with:
- Student name
- Commit count
- Languages used
- Performance score (with color-coded badges)
- Analysis status (Analyzed/Pending)
- Quick link to individual repository details

### 📥 Downloadable Reports
Generate Markdown format reports containing:
- Assignment overview statistics
- Language breakdown
- Individual student details
- AI summaries for analyzed repositories
- Performance scores

## How to Use

### Accessing Analytics

1. Navigate to an assignment from your dashboard
2. Click the **"View Analytics"** button (green button with bar chart icon)
3. Analytics page will display all available metrics

### Understanding the Dashboard

#### Top Section - Key Metrics
Four gradient-styled cards showing:
- Total students enrolled
- Total commits made
- Average commits per student
- Number of programming languages

#### Progress Section
Two progress bars:
- **Green bar**: Percentage of analyzed repositories
- **Yellow bar**: Percentage of pending repositories

#### Language Section (Left Column)
- Horizontal bars representing each language
- Percentage and byte size displayed
- Bars proportional to language usage
- Hover effect for better visibility

#### Performance Section (Right Column)
- Large average score display
- Min/Max score indicators
- Distribution breakdown with color-coded badges:
  - 🟢 Green: Excellent (90+)
  - 🔵 Blue: Good (75-89)
  - 🟠 Orange: Average (60-74)
  - 🔴 Red: Needs Work (<60)

#### Top Performers & Most Active (Two Cards)
- **Top Performers**: Ranked by AI performance score
- **Most Active**: Ranked by commit count
- Each shows top 5 students

#### Student Table (Bottom)
- Complete list of all students
- Sortable columns
- Color-coded status badges
- View button for detailed repository analysis

### Downloading Reports

1. Click **"Download Report"** button (top right, green with download icon)
2. JavaScript will fetch the report data
3. Markdown file will be automatically downloaded
4. Filename format: `Assignment_Title_report.md`

### Report Contents

The downloaded Markdown report includes:

```markdown
# Assignment Analysis Report: [Title]

## 📊 Overview Statistics
- Total Students
- Repositories Analyzed
- Total Commits
- Average Commits per Student
- Average Performance Score

## 💻 Programming Languages Used
- Language breakdown with percentages

## 👥 Student Details
For each student:
- Repository URL
- Commit count
- Languages used
- Performance score
- AI summary (truncated)
```

## Technical Details

### Backend (analytics.py)

#### `assignment_analytics(request, assignment_id)`
**Purpose**: Renders the analytics dashboard

**Calculations**:
1. **Basic Counts**:
   - `total_students = repos.count()`
   - `analyzed_repos = repos.filter(is_analyzed=True).count()`
   - `pending_repos = total_students - analyzed_repos`

2. **Commit Statistics**:
   - `total_commits = sum(repo.commit_count for repo in repos)`
   - `avg_commits = round(total_commits / total_students, 1)`

3. **Language Aggregation**:
   ```python
   all_languages = Counter()
   for repo in repos:
       if repo.languages:
           for lang, bytes_count in repo.languages.items():
               all_languages[lang] += bytes_count
   ```

4. **Performance Scores**:
   - Filters: `repos.filter(is_analyzed=True, performance_score__isnull=False)`
   - Avg: `sum(scores) / len(scores)`
   - Distribution: Counted based on score ranges

5. **Top Lists**:
   - Top Performers: `order_by('-performance_score')[:5]`
   - Most Active: `order_by('-commit_count')[:5]`

**Returns**: Renders `assignment_analytics.html` with context dictionary

#### `generate_assignment_report(request, assignment_id)`
**Purpose**: Generates downloadable Markdown report

**Returns**: JSON response with:
```json
{
    "success": true,
    "report": "...markdown content...",
    "filename": "Assignment_Title_report.md"
}
```

### Frontend (assignment_analytics.html)

#### Key Components:

1. **Breadcrumb Navigation**: Shows path from Dashboard → Assignment → Analytics

2. **Statistics Cards**: 
   - CSS gradient backgrounds
   - Responsive grid layout (4 columns on desktop)

3. **Progress Bars**:
   - Django template tag: `{% widthratio analyzed_repos total_students 100 %}`
   - Bootstrap progress component

4. **Language Bars**:
   - Custom CSS with gradient backgrounds
   - Hover transform effect
   - Dynamic width based on percentage

5. **Score Badges**:
   - Custom CSS classes with color coding
   - Inline badge generation based on score value

6. **Download Function** (JavaScript):
   ```javascript
   function downloadReport() {
       fetch("{% url 'generate_report' assignment.id %}")
           .then(response => response.json())
           .then(data => {
               const blob = new Blob([data.report], { type: 'text/markdown' });
               const url = window.URL.createObjectURL(blob);
               const a = document.createElement('a');
               a.href = url;
               a.download = data.filename;
               a.click();
           });
   }
   ```

### URL Configuration

```python
# edutrack/urls.py
path('assignments/<int:assignment_id>/analytics/', 
     analytics.assignment_analytics, 
     name='assignment_analytics'),
     
path('assignments/<int:assignment_id>/report/', 
     analytics.generate_assignment_report, 
     name='generate_report'),
```

## Use Cases

### For Teachers

1. **Quick Overview**: 
   - View all student submissions at a glance
   - Identify students who haven't submitted
   - See overall class performance

2. **Identify Struggling Students**:
   - Check "Needs Work (<60)" count
   - Review students with low commit counts
   - Provide targeted assistance

3. **Recognize Top Performers**:
   - Highlight excellent work
   - Use as examples for other students
   - Award extra credit

4. **Language Insights**:
   - Ensure students are using required languages
   - Identify unexpected language usage
   - Verify project requirements compliance

5. **Reporting**:
   - Download comprehensive reports for grading
   - Share statistics with administration
   - Track class progress over time

### For Students (Future Enhancement)
- View their own ranking (anonymously)
- Compare their commits to average
- See language distribution of their code

## Design Philosophy

### Visual Hierarchy
1. Most important metrics at top (gradient cards)
2. Progress indicators for quick status check
3. Detailed breakdowns in middle section
4. Complete data table at bottom

### Color Coding
- **Purple/Violet**: Total students (primary metric)
- **Pink/Red**: Commits (activity metric)
- **Blue/Cyan**: Averages (comparative metric)
- **Green/Teal**: Languages (technical metric)
- **Performance Badges**: Standard traffic light system

### Responsive Design
- Cards stack on mobile
- Table scrolls horizontally if needed
- Buttons wrap in flex container
- Charts remain readable on all screens

## Best Practices

### When to View Analytics

1. **After Initial Submissions**: Check how many students have submitted
2. **Mid-Assignment**: Identify students falling behind
3. **After Analysis**: Review AI-generated performance scores
4. **Before Grading**: Download report for comprehensive overview
5. **End of Semester**: Track improvement over multiple assignments

### Interpreting Data

- **Low Average Commits**: May indicate simple assignment or late starts
- **High Language Count**: Could show creativity or confusion about requirements
- **Wide Score Distribution**: Indicates varying skill levels
- **Many Pending**: Students haven't analyzed yet (reminder needed)

### Tips

1. Analyze at least a few repositories before viewing analytics for meaningful data
2. Download reports regularly for record-keeping
3. Use top performers list to identify potential TAs
4. Monitor most active students for potential burnout
5. Check pending count regularly to ensure all submissions are analyzed

## Future Enhancements

Potential additions:
- [ ] Time-series graphs showing commits over time
- [ ] Comparative analytics across multiple assignments
- [ ] Student-facing analytics (personal dashboard)
- [ ] Export to CSV/Excel for external analysis
- [ ] Interactive charts (Chart.js integration)
- [ ] Automated insights ("30% of students need help")
- [ ] Email notifications for low performers
- [ ] Plagiarism detection patterns
- [ ] Code quality trends
- [ ] Deadline vs. submission time analysis

## Troubleshooting

### No Data Showing
- Ensure repositories have been added to the assignment
- Check that GitHub API is accessible
- Verify student names were provided during repo addition

### Analytics Shows 0 Analyzed
- Repositories need to be analyzed first
- Click "Analyze with AI" on individual repositories
- Or use bulk analysis feature (if implemented)

### Download Button Not Working
- Check browser console for errors
- Ensure JavaScript is enabled
- Verify report generation endpoint is accessible
- Check network tab for failed requests

### Incorrect Statistics
- Re-analyze repositories if code has changed
- Check that languages JSON is being saved properly
- Verify performance scores are numeric

## Conclusion

The Analytics feature transforms raw repository data into actionable insights, helping teachers efficiently monitor class progress, identify students needing assistance, and recognize outstanding work. The visual design prioritizes clarity and ease of use, making complex data accessible at a glance.
