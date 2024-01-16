 
# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for
import requests
import sqlite3

# Create a Flask app
app = Flask(__name__)

# Database connection
conn = sqlite3.connect('fantasy_premier_league.db')
c = conn.cursor()

# Home page route
@app.route('/')
def index():
    # Get the latest fixtures from fantasy.premierleague.com
    response = requests.get('https://fantasy.premierleague.com/api/fixtures/')
    fixtures = response.json()['fixtures']

    # Render the home page with the fixtures
    return render_template('index.html', fixtures=fixtures)

# Route to handle predicted scores submission
@app.route('/predict_scores', methods=['POST'])
def predict_scores():
    # Get the predicted scores from the form
    predictions = request.form.to_dict()

    # Store the predicted scores in the database
    for fixture_id, predicted_score in predictions.items():
        c.execute('INSERT INTO predictions (fixture_id, predicted_score) VALUES (?, ?)', (fixture_id, predicted_score))
    conn.commit()

    # Redirect to the home page
    return redirect(url_for('index'))

# Leaderboard route
@app.route('/leaderboard')
def leaderboard():
    # Get the leaderboard data from the database
    c.execute('SELECT username, SUM(points) AS total_points FROM users JOIN predictions ON users.id = predictions.user_id GROUP BY username ORDER BY total_points DESC')
    leaderboard = c.fetchall()

    # Render the leaderboard
    return render_template('leaderboard.html', leaderboard=leaderboard)

# Results route
@app.route('/results')
def results():
    # Get the results from fantasy.premierleague.com
    response = requests.get('https://fantasy.premierleague.com/api/results/')
    results = response.json()['results']

    # Calculate the points for each prediction
    for result in results:
        fixture_id = result['fixture']['id']
        actual_score = result['goalsHomeTeam'] - result['goalsAwayTeam']

        # Get the predicted scores for the fixture
        c.execute('SELECT predicted_score, user_id FROM predictions WHERE fixture_id = ?', (fixture_id,))
        predictions = c.fetchall()

        # Calculate the points for each prediction
        for predicted_score, user_id in predictions:
            if predicted_score == actual_score:
                points = 10
            elif predicted_score > actual_score and actual_score > 0:
                points = 5
            elif predicted_score < actual_score and actual_score < 0:
                points = 5
            else:
                points = 0

            # Update the user's points in the database
            c.execute('UPDATE users SET points = points + ? WHERE id = ?', (points, user_id))
    conn.commit()

    # Render the results
    return render_template('results.html', results=results)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
