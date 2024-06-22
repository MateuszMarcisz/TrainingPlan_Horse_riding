<h1 align="center"> Welcome to <strong>Patataj</strong>, a webapp for making custom training plans</h1>

## Description:

This app was made for my project during python programming course at [CodersLab](https://github.com/CodersLab). It was developed after approximately 2 months of learning.
The idea behind the app was to help my wife and her equestrian friends to manage training plans and save some events in calendar. Please note that the content of the app is in Polish.


## Technologies:

- **Framework**: Django
- **Backend**: Python
- **Frontend**: HTML, CSS and some JavaScript
- **Database**: PostgreSQL
- **Other**: Docker Desktop, Font Awesome, FullCalendar, pytest/pytest-django


### Setup:
<i>You will need Docker in order to make it work (or make some adjustments in settings and set up DB)</i>
1. Clone repository.
2. Install docker & docker-compose / docker desktop
3. Change .env.example name to .env and make adjustments
4. Run in the terminal: docker compose up --build
5. Go to: http://0.0.0.0:8000/



### Usage:
1. **Homepage**: Overview of the application with featured sections.
2. **Trainings**: Browse and filter through available trainings or add some new ones.
3. **Plans**: Create and manage custom training plans.
4. **Horses**: Manage your horses.
5. **Trainers**: Find and add new trainers.
6. **Calendar**: Schedule and view your training sessions.
<p>
Please have in mind that the content of the app is made in Polish language. All the comments to the code and descriptions are made in English.
</p>

### License:
You are free to use, modify, and distribute this application for your private, personal use.


### Tests:
I have made a total of 104 tests for 32 views. Sample of testing for main app views:
![tests](visualization/tests.png)
For more details about the tests go to the tests.py files in each of the apps (patataj, accounts, kalendarz).

### Visualization:
1. **Homepage:**
![Homepage](visualization/Homepage.png)
2. **Trainings:**
![Trainings](visualization/Trainings.png)
3. **Plan Details:**
![TrainingPlan](visualization/TrainingPlanDetails.png)
4. **Add Horse:**
![AddHorse](visualization/AddHorse.png)


## Author:
- **email**: mateusz.marciszm@gmail.com
- **github**: [MateuszMarcisz](https://github.com/MateuszMarcisz)
- **CodeWars**: [T0dl3r](https://www.codewars.com/users/T0dl3r)
- **GS**: [GoogleScholar](https://scholar.google.com/citations?user=QW3tlewAAAAJ&hl=en)

