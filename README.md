# Habit Tracker

An app to track your daily habits and create a schedule for consistent days created to maintain a healthy and monitored daily lifestyle and get a feedback on your daily activities.

## Features

-Includes a authentication system to create a user account and login to the app
-Allows users to create a daily schedule with specific start and end times for their habits
-Allows users to check off tasks as they complete them each day
-Provides a summary of the user's consistency
-Can see the history of the habits and the progress made over time

## Technologies Used

- Python
- Flask
- SQLite
- Qwen 0.5B (Local AI model)

## Why I built this
I built this because I needed a simple habit tracker that tracks my daily activities. I wanted a basic tool where I can schedule tasks, check them off, and see a simple summary of my consistency. I added a local AI summarizer because I wanted to see if a small local model could give me short, actionable feedback without needing an internet connection.

## Known Issue
I used "Qwen/Qwen2.5-0.5B-Instruct" model for the summary of the activities, but the model was not capable of interpreting the data perfectly, so there might appear the problem of imperfect summary.

## how to run
use the demo link and download the zip file and run the .exe file . and the internal folder should be in the same folder as the .exe file.