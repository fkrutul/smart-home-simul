# Installation/Usage Guide

## Installation
- Make sure you have Python3 and Node installed on your system. If not(look up specific installation guides for your OS).
- Use PIP to install pipenv
- Inside the root folder of the project, run *pipenv install* to install Python dependencies
- cd into 'frontend'
  - Run *npm install* to get the Node dependencies.
- You will also need an OpenWeatherMap API key to run the application
  - Go to <a>https://openweathermap.org/api</a> and register with an email for free tier access to their API.
  - Once your account is confirmed, you can access your API key from your account page.
  - Copy the API key to your clipboard.
  - Create a file in root_directory/public called *local_config.py*
  - Inside that file write ```API_key = "<your-copied-API-key>"```

## Usage
- Run *pipenv shell* or *python -m pipenv shell* to enter the virtual environment (if successful 'term-project' should be in parentheses before your shell input).
- Open 2 terminals and make sure the pipenv environment is active in both:
  - In terminal 1:
    - cd into 'public' from the root directory
    - Run *export FLASK_ENV=development* to set the app in development mode
    - Run *flask_run* to start the backend server
  - In terminal 2:
    - cd into 'frontend'
    - Run *npm run build* to build the project
    - Run *npm run start* to start the frontend service
- In your browser, go to *127.0.0.1:3000* to see the page