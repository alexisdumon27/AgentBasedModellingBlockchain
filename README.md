# AgentBasedModellingBlockchain

## Project Explanation
This project aims to analyse the behavior of investors in a cryptocurrency exchange market. It does so by implementing an executable agent-based model that can be run from one's terminal and through a web-based user interface.

There are three different folders in the project repository which separate different aspects of the project.
The Data folder contains the scripts to clean the raw data files which need to be downloaded.
The Model folder contains the files containing the design of the simulation.
The Visualisation folder has the files which deal with visualising the model's state throughout the simulation.

The files were ran using Python 3.8.10 on an Apple MacBook air (M1 chip).

## Necessary Imports

The following libraries need to be installed in order for the code to run:

- numpy
- pandas
- matplotlib
- mesa

These can be installed on one's local machine or through any virtual environmen such as Conda.

## How to run

### Downloading the Data
There are two sources for the data: [www.cryptoarchive.com.au](https://www.cryptoarchive.com.au) and [finance.yahoo.com](finance.yahoo.com)

After the data has been downloaded it then needs to be cleaned and merged appropriately. This is all put into one script file called *dataCleaning.py*.
This will output a *.csv* file called *exchange_rates.csv* which should remain in the Data folder.

Once this is done the simulation is ready to be run. There are two ways by which it can be run:
* On the web interface --> *run.py*; this will show the model's running state through an HTML and Javascript web server.
* On the terminal --> *batchRunModel.py*; this will run the model 10 times and output *.csv* files of the data collected throughout the simulation


