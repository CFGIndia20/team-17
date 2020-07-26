# Team Ninjas in Pajamas 💫 
#### (Team-17; Code for good 2020)

This project aims to ease the process of filing complaints 
to the Janagraaha portal, to help them keep the city clean,
bypassing their existing web and mobile application at least 
from the user's side.

<hr>

## What is the solution?

A facebook messenger chatbot, totally user friendly interface letting users lodge complaints without going through the tedious task of selecting the "category". 
Let us automate that task using our amazing ML model for you :D


<hr>

## How to run the application?

- Create a new vitrual env, either using pipenv or anaconda. (Highly recommended)
- ```sh 
    # activate the environment
    # example: conda activate env_name

    cd apis
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    # server should be up and running
    ``` 
- Create firebase credentials 


<hr>

## How do I test the ML models?

- You can find `ml.py` in `apis/complaint/` directory
- Model is loaded and prediction is made from there
- Trained model file is saved in the `saved_models` directory
- You can find the jupyter notebooks in the `notebook` directory
- The data used for training lies in the `data` directory

<hr>

## How to test the Speech to text and Video Sound Extraction ?

- You can find `utils.py` in `apis/complaint/` directory
- Feel free to experiments with the flags but make sure `ffmpeg` is installed on your computer and its location is available in the path variable of the system.



    


