# File Synchronization Service


## Description
An application for file synchronization between a local directory and a directory on a remote disk. At the moment, synchronization with yandex.disk is implemented. The application downloads (with replacement) files from the local directory to the disk, and deletes files on the disk that are not on the local computer. Synchronization occurs with a frequency set via environment variables.


## Installation
To install the application, just copy the src folder and the file requirements.txt (or just dump the repository) to the local machine, install libraries from requirements.txt with the command ```pip install -r requirements.txt``` (preferably in a virtual environment). After that, you need to add environment variables using the example from the .end.example file (you can add the .env file). To work correctly, you need to get an authorization token for your disk (for example, for [Yandex disk](https://yandex.ru/dev/disk-api/doc/ru/concepts/quickstart#quickstart__oauth)). The frequency is adjusted using the environment variables DAYS, HOURS, MINUTES. The log file is called **logfile.log** and will be generated in the directory from which the script is run.
