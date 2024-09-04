# Cardio-Guard
An AI-driven Cardiovascular Monitoring and Arrhythmia Detection System

A proposed project on heart monitoring for my thesis at the ECE department at the Technical University of Crete.

TODO: Update it


Install the dependencies listed in requirments.txt using ```pip install -r requirements.txt```

To connect to a movesense device, capture raw ECG data and process them, use ```python manage.py``` 

To display the processed data use ```python analytics.py```

If movesense device is not available, and for some reason need to run the manage.py, uncomment the hl.* methods and comment the reffering mv_blk.* ones.

For now the manage app can connect to only one movesense device, and proccess only ECG data.

Its a bit buggy sometimes. 
