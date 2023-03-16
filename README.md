# CongressionalDeceptionAndEvasion

This repository contains codes wfritten for labeling the Congressional Sessions Dataset.

The CongressionalDeception folder contains the dev work for the Deception Survey.

Prerequisites: we need to have Python3, Flask, Flask-WTF and WTForms installed.

```
$ brew install python3
$ pip3 install flask
$ pip3 install flask-wtf
$ pip3 install WTForms
$ pip3 install pymongo
$ pip3 install flask-recaptcha
```

To run it: Open Terminal and navigate to the CongressionalDeception folder and type:

```
python3 app.py
```

This starts the application server. Next open your favourite web-browser and enter the address of the server: `http://127.0.0.1:5000/index`. It should navigate to the Web-page of the survey.
