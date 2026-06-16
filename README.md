# Task 1 - $1 Gesture Recognizer

## Setup

Install all required dependencies using the provided requirements.txt file:

```code
pip install -r requirements.txt 
```

## Running the Application

Navigate to the task_1 folder and start the application:

```code
python gesture_input.py 
```
A window will open where gestures can be drawn using the mouse.

## Usage

- Press and hold the left mouse button and draw a gesture.
- Release the mouse button to finish the gesture.
- The gesture will automatically be classified by the $1 Recognizer.
- The recognized gesture and its confidence score will be displayed in the application window.

To draw a new gesture, simply start drawing again. The previous gesture will be cleared automatically.

## Saving Gestures

After a gesture has been recognized, it can be saved as an XML file by pressing the S key.

The gesture will be stored in XML format and saved under the gesture class that was predicted by the recognizer.

The file path can be specified in the code for both, the classifier train data and the output file path.

```code 
XML_LOGS_DIR = 'xml_logs'
XML_LOGS_OWN = 'datasets'
```

# Task 2 - LSTM Gesture Recognition

The file unistroke_gestures.ipynb contains the complete implementation for Task 2.

The notebook includes training models and analysis of the results.

# Task 3 - Gesture Detection Game

Copied my own code from Task 1. Lacked time this week.
But hey, these points work :D
```code
(1P) Gesture input works
(2P) Three gestures are distinguished robustly
```

# Task 4 - Bonus: Study Participation
I've scheduled an appointment for next Tuesday 2pm