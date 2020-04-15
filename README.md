# Session-based-e-commerce-analysis

- This project explores eCommerce events data to identify potential Business Intelligence use-cases and to develop data-driven solutions using machine learning and deep learning techniques
- The Kaggle eCommerce Events History in Cosmetics Shop was used for this project.
  Link to dataset: https://www.kaggle.com/mkechinov/ecommerce-events-history-in-cosmetics-shop

# Key aspects of the project
- Optimized memory usage of source dataframe by ~50% by efficiently reading the data.

# Instructions
- Download the dataset and extract the files into 'cosmetics dataset' folder

### pre-processing:
- Pre-processing the source dataset for further use.
```
python3 preprocess.py [-f] [--min MIN] [--max MAX]
```
- *filter_flag '-f'* enables filtering to produce filtered dataset along with the preprocessed dataset. Without filter flag, only the preprocessed dataset is generated.
- Filtering parameters can be set using *min* and *max* arguments and works only when filter flag is enabled. min and max are the minimum and maximum number of user_sessions a product must have to be included in the data. Any of the arguments can be left out. By default, min = 100; max = 1100.

### generating input for classification use-case:
- Generating labeled data with input features from the filtered dataset for classification use-case
```
python3 generate_input.py [-w DEMAND_WINDOW]
```
- *demand_window* determines the number of days to include for calculating average demand. By default, demand_window = 1.

# Project steps with Logic

### initial EDA and key observations:
- Performed initial EDA (Exploratory Data Analysis) on the dataset to observe errors in the dataset.
- Event time is an object -> must be converted to datetime
- Negative and zero price value in distribution shows error in data -> can be removed
- Category code and brand columns have a lot of null values -> columns can be ignored to avoid missing data
- Negligible amount of null user-sessions present -> must be removed along with users interaction with the product
- Number of user-sessions per product is heavily skewed -> products with significant number of user sessions can be chosen for further work
- Price distributions are not different for event types
- Duplicate records exist -> must be removed

### data pre-processing:
- Optimized memory usage by efficiently reading the data
