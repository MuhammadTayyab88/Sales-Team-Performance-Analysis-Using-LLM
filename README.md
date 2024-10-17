# Sales Team Performance Analysis Using LLM

This Django project analyzes sales team performance using data from CSV files and provides insights with the help of a Large Language Model (LLM), specifically OpenAI's GPT. The application supports data ingestion, API endpoints for individual and team performance analysis, and trends over specified time periods.

## Table of Contents
- [Features](#features)
- [Technologies](#technologies)
- [Setup Instructions](#setup-instructions)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [License](#license)

## Features
- **Data Ingestion**: Import sales data from CSV files.
- **LLM Integration**: Generate insights using OpenAI's GPT for individual and team performance.
- **REST API**: Provides endpoints for querying sales performance, team trends, and individual representative insights.
- **Scalable**: Uses Django and Django REST Framework for robust and scalable API development.

## Technologies
- **Django**: Backend framework for server-side operations.
- **Django REST Framework**: For building the API endpoints.
- **OpenAI API**: For generating insights using GPT models.
- **Python-dotenv**: For environment variable management.
  
## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/sales_project.git

**Create and Activate a Virtual Environment**:
```bash
python -m venv env
```
```bash
source env/bin/activate  # On macOS/Linux
```
```bash
.\env\Scripts\activate   # On Windows
```
 **Install Dependencies**:
```bash
pip install -r requirements.txt
```
**Set Up Environment Variables**:
Create a .env file in the project root directory and add your OpenAI API key:
```bash
OPENAI_API_KEY ="sk-G8B-zacyp1S9JaYaXtdqe5Yd7yM7yqIg_hS7oXDVGyT3BlbkFJ-PX3RRG2RxHKIl14Tg5D_CeGmGM_4OV57E_K9SzCgA"
```
**Run Migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```
**Load Sales Data**:
To import sales data from a CSV file, run:
```bash
python manage.py import_sales_data "path/to/your/filename.csv"
```
**Start the Development Server**:
```bash
python manage.py runserver
```

**Individual Sales Representative Performance**:
URL: /api/rep_performance/<employee_id>/
```bash
http://127.0.0.1:8000/api/rep_performance/183/ 
```

**Team Performance**:
URL: /api/team_performance/
```bash
http://127.0.0.1:8000/api/team_performance/ 
```

**Performance Trends**:
URL: /api/performance_trends/?time_period=<time_period>
```bash
http://127.0.0.1:8000/api/performance_trends/?time_period=monthly
```
