# Simple Usage of Alpha Vantage Apis

## Project Structure

The project is written in python **3.8**, it is an *interactive command line interface*, which uses some of alpha
vantage apis (refer to [docs](https://www.alphavantage.co/documentation/)) to display some data.

The following tree structure shows the code organization.

```
alpha_vantage
├── alpha_vantage
│   └── __init__.py
│   └── alpha_vantage.py
├── helpers
│   └── decorators
│       └── __init__.py
│       └── validation_decorator.py
│   └── __init__.py
│   └── custom_exceptions_helper.py
├── tests
│   └── __init__.py
│   └── test_alpha_vantage.py
└── alpha_vantage_runner.py
└── constants.py
└── main.py
└── requirements.txt
└── README.md
```

## Usage
Execute the python script from the root folder (**alpha_vantage**): 
First, source python 3, then:  
`pip install requirements.txt` 

Now, you can enjoy using Aplha Vantage cli   
`python -m main`
```
usage: python -m  main.py [-h] -k API_KEY [-f {json,csv}] [-s {compact,full}] [-d OUTPUT_FOLDER] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -k API_KEY, --api-key API_KEY
                        apikey for alpha vantage api, if you don't have one, you can claim your apikey on: https://www.alphavantage.co/support/#api-key
  -f {json,csv}, --output-format {json,csv}
                        For Alpha Vantage timeseries apis only, specify `datatype`; `json`, returns the api result in JSON format `csv`, returns the api result as a CSV
                        file.
  -s {compact,full}, --output-size {compact,full}
                        Some Alpha Vantage apis specify `outputsize`; `compact`, returns only the latest 100 data points' `full`, returns the full-length of the data. The
                        `compact` option is recommended if you would like to reduce the data size of each API call.
  -d OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
                        Provide a full path directory to use as a base to store output results when available (either json or csv). If not provided, will use `./output as
                        a default.
  -v, --verbose         Print the output to the console of json apis in the console.
```

**<font color=maroon>Note:</font>** use `-v` or `--verbose` to see the output in command line while running the cli command.

## Features

1. Search specific symbols or companies.
2. From the search list, you can choose a company and display the following options:
    - Display additional details in grid.
    - Display historical prices on specific timeframes.
    - Display current quote.
    - Display exponential moving average
    
## Tests
To run the unit tests:
From the mail directory, run this command.
```
python -m unittest tests/test_alpha_vantage.py
```

```
Ran 7 tests in 650.163s

OK
```
Between each test, there is a delpy time period of (20 seconds), to prevent exceeding the usage limit (5 requests per minute). 

## Sample output

You can find some sample output saved in `output` folder. 