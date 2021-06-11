# Who was deplatformed where?

This project was carried on as a Master's semester project, under the supervision of Manoel Horta Ribiero and Professor West from the DLAB at EPFL. The goal of this project is to create a precise and large-scale dataset of deplatforming on various social media platforms. This dataset will then allow to conduct an analysis on the effect of deplatforming on the popularity or attention the banned entity receives.

## Requirements
The following libraries were used for this project: 

| library    | version|
|------------|--------|
| matplotlib | 3.3.4  |
| numpy      | 1.19.2 |
| pandas     | 1.2.3  |
| python     | 3.8.8  |
| scipy      | 1.6.2  |
| spacy      | 3.0.5  |
| statsmodel | 0.12.2 |
| swifter    | 1.0.7  |

## Structure

The project is structured as follows:
    .
    ├── scripts                 # python scripts for recreating the dataset and analysis
    |	├ scrape_reddit.py      # To scrape reddit posts using pushshift API. Otherwise, posts (up to 2019) can be found in 
	|	|						# `dlabdata1/reddit\_rad/{year}-{month}.jsonl.gz`
	|	|
	|	├ read\_reddit\_files.py  # To read the gz reddit files from the dlab cluster directly
    |	├ extract_pairs.py		# Extract entities/platform pairs from a given pattern and post + filter them
    |	├ extract_patterns.py   # Extracts patterns from a post and an entity/platform pair
    |	├ interrupted\_time\_series.py # Create interrupted time series models
    |	├ link\_google\_id.py   # Queries google knowledge graph to retrieve the google ids of given entities
    ├── data                    # Contains the intermediary data used 
    |	├ raw_patterns.csv      # The unfiltered list of patterns found extracted at the end of the first iteration
    |	├ filtered_patterns.csv # Filtred list of 17 patterns used in the second iteration
    |	├ platforms_list.txt    # List of predifined social media platforms 
    ├── results                 # Results at the end of the first iteration and of the second
    |	├ first\_pairs\_extracted.csv # Automatically filtered pairs after initial iteration 
    |	├ base_pairs.csv		# first pairs extracted manually filtered
    | 	├ bans.csv				# Final dataset
    ├── recreate_date.ipynb     # Jupyter notebook using the scripts for recreating step by step the final dataset
    ├── result_analysis.ipynb   # Jupyter notebook running the Interrupted Time Series analysis
    ├── report.pdf              # Report detailing various aspects of the project
    ├── algorithm\_diagram.pdf  # Diagram summarizing the algorithm for creating the dataset
    └── README.md

