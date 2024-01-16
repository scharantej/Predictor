 
# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for

# Create a Flask app
app = Flask(__name__)

# Define the route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define the route for the results page
@app.route('/results', methods=['POST'])
def results():
    # Get the user's predictions from the form data
    predictions = request.form.to_dict()

    # Process the predictions to determine the number of correct predictions
    correct_predictions = 0
    for match, prediction in predictions.items():
        # Split the match string to get the home and away teams
        home_team, away_team = match.split(' vs. ')

        # Get the actual score for the match from the database
        actual_score = get_actual_score(home_team, away_team)

        # Check if the user's prediction is correct
        if prediction == actual_score:
            correct_predictions += 1

    # Render the results page with the number of correct predictions
    return render_template('results.html', correct_predictions=correct_predictions)

# Define a function to get the actual score for a match from the database
def get_actual_score(home_team, away_team):
    # Connect to the database and query for the actual score
    connection = sqlite3.connect('scores.db')
    cursor = connection.cursor()
    cursor.execute('SELECT home_team_score, away_team_score FROM matches WHERE home_team=? AND away_team=?', (home_team, away_team))
    result = cursor.fetchone()
    connection.close()

    # Return the actual score
    return result[0] + ' - ' + result[1]

# Run the app
if __name__ == '__main__':
    app.run()
