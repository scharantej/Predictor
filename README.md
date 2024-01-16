 ## **Flask Application Design**

### **HTML Files**

**1. index.html**
- This is the main HTML file that will serve as the user interface for the web application.
- It will contain a form that allows the user to input their predictions for the next round of results in the English Premier League.
- The form should include fields for the following:
  - Home Team
  - Away Team
  - Predicted Home Team Score
  - Predicted Away Team Score
- The form should also include a submit button that will send the user's predictions to the server.

**2. results.html**
- This HTML file will display the results of the user's predictions.
- It will be rendered after the user clicks the submit button on the index.html page.
- The results.html file should include the following information:
  - The user's predicted scores for each match
  - The actual scores for each match
  - The number of correct predictions the user made

### **Routes**

**1. @app.route('/')**
- This route will handle the GET request for the index.html page.
- It will render the index.html file, displaying the form for the user to input their predictions.

**2. @app.route('/results', methods=['POST'])**
- This route will handle the POST request sent from the index.html page when the user clicks the submit button.
- It will receive the user's predictions from the form data and process them to determine the number of correct predictions.
- It will then render the results.html file, displaying the results of the user's predictions.

### **Additional Notes**

- The Flask application will need to be configured to use a database to store the actual scores for each match.
- The application will also need to be configured to send emails to the user with the results of their predictions.