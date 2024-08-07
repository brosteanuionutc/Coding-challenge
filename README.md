# LSEG_codingchallenge

## Overview
This application processes stock price data from various exchanges, predicts future stock prices based on historical data, and saves the predictions in new CSV files.

## Features
- Extracts 10 consecutive data points from a random timestamp for each file.
- Predicts the next 3 stock prices using a predefined algorithm.
- Handles errors gracefully, including missing or empty files.
- Supports processing multiple files per exchange.

## Setup
- add the .zip file in the same directory with the 'main.py' file
- update the 'zip_file_path' and 'unzip_dir' variables in the main function from the 'main.py' file
- run the 'main.py' file without any other extra parameters using '_python main.py_'

### Prerequisites
- Python 3.7 or higher
- libraries os, pandas, random and zipfile

### Future enhacements
- **Logging**: Use a logging library to handle different levels of logging (info, debug, error) instead of print statements.
- **Unit Tests**: Add unit tests to verify each function behavior independently.
- **Configuration File**: Use a configuration file (i.e. JSON or YAML) to manage parameters like paths and number of files to process.
- **Command-line Arguments**: Allow passing parameters via command-line arguments for more flexibility.
