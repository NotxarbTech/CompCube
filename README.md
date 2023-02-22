# CompCube
#### Video Demo:  <https://youtu.be/aHNiZZEbIcA>
#### Description:
CompCube is a Flask website that allows users to create/compete in Rubik's Cube speed-solving competitions.

I have a background in Rubik's Cube speedsolving, and during the pandemic I was always searching for online competitions so I could use my skills and compare myself to other cubers, but I couldn't find one.

When thinking of a final project idea, this one came back to me, as I had always wanted to implement it, but did not have the technological know-how required.

This project integrates a library called PyTwistyScrambler, which creates WCA scrambles for Rubik's Cubes.

This project uses Bootstrap, which has useful features such as css styling and responsive features, such as the navigation bar.

The website has a login page, a register page, a home page, a "create competition" page, and a custom page for each competition.

The website uses a Sqlite3 database with 3 tables, a users table, a competitions table, and a solves table.

All skills that I used to create this website were from cs50, as I had never made a flask application before the course and had zero experience in sql.

When creating a competition, the user has the option to use their own custom scramble, or leave blank for a WCA (World Cubing Association) random scramble.

Each competition has its own page, complete with a leaderboard that shows each user's attempt in order of solve time.

The creator of the competition can delete entries from their own competition.

Each user can delete their time from the leaderboard if they accidentally inputted the wrong time.

If the user wishes to share their competition with others, they can copy the url and post it to any social media or share it with their friends.

This was cs50.

#### Tech Stack
##### Flask
Flask is a web framework that allows developers to create web apps with python. This is the framework that I built the backend with.

##### Bootstrap
Bootstrap is a frontend framework that I used to help create responsive styling for my web application.

##### PyTwistyScrambler
PyTwistyScrambler is a python library that generates WCA-compliant scrambles for the competitions

##### Sqlite3
Sqlite3 is a database engine that I used to store information about the users, the competitions, and the solves.

#### Future Features
##### More puzzles
In the future I plan to add support for more puzzles so that users can compete in other sizes, such as 2x2, 4x4 or 5x5.

##### Timer Integration
I plan to allow users to use a timer on the website instead of using a StackMat or mobile timer.

##### ~~ Personal best times ~~ (Now Avaliable)
I plan to allow users to see their's or other's PB solves.

###### User Profiles/Friends
I plan to add user profiles so users can view other cuber's info and send friend requests.

