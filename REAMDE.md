# DIALOGUE CITOYEN V0.0

## Prerequisite
- Python 3.X installed
- Google Cloud SDK (CLI)

## Production
 Idea is that for production everything will be inside the `app` folder
 Must:
 - authenticate
 - deploy

 **Must run deploy from dialogue_citoyen folder**

## Website
 At the moment `app.py` have a basic flask server that interact with stripe and allow downloading the contract after payment. Hardcoded to localhost

## Logic
 `main.py` offer basic logic to take the inpur strings, query gemini and return the response.

## Goal
 Goal is to offer basic legal advide and unbiased resolution between two person. Initial price would be 0$, eventually more!