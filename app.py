from flask import Flask, render_template, request, jsonify
import json
import csv

app = Flask(__name__)

# CSV reading function
def read_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        data = {row['Job Title']: [row[f'Skill {i+1}'] for i in range(13)] for row in reader}
    return data

# Function to find matching job titles
def find_matching_job_titles(user_skills, data):
    matching_job_titles = set()

    for job_title, skills in data.items():
        matching_count = sum(skill in user_skills for skill in skills)
        if matching_count > 0 and job_title not in matching_job_titles:
            matching_job_titles.add(job_title)

    return matching_job_titles

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Load existing data from the JSON file
        with open('data.json', 'r') as file:
            existing_data = json.load(file)

        # Get user input from the form
        skills = request.form.get('skills').split(',')
        job_titles = request.form.get('jobtitles').split(',')

        # Generate unique keys for new entries
        new_entries = {}
        for skill, title in zip(skills, job_titles):
            skill_key = f'Skill_{len(existing_data["Skills"]) + 1}'
            title_key = f'JobTitle_{len(existing_data["JobTitles"]) + 1}'

            new_entries[skill_key] = skill.strip()
            new_entries[title_key] = title.strip()

        # Update existing data with new entries
        existing_data.update(new_entries)

        # Save updated data back to the JSON file
        with open('data.json', 'w') as file:
            json.dump(existing_data, file, indent=2)

        # Render the template with the confirmation message
        return render_template('index.html', confirmation_message='Data submitted successfully.')

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input_skills = request.form.get('skills')
        user_input_skills = user_input_skills.strip().split(',')[:7]
        file_path = 'jobdetails.csv'  # Replace with the actual file path
        data = read_csv(file_path)
        matching_job_titles = find_matching_job_titles(user_input_skills, data)
        return render_template('index.html', matching_job_titles=matching_job_titles)

    return render_template('index.html', matching_job_titles=None)

if __name__ == '__main__':
    app.run(debug=True)
