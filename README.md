# Session-based-e-commerce-analysis
- The Kaggle eCommerce Events History in Cosmetics Shop was used in this project.
  Link to dataset: https://www.kaggle.com/mkechinov/ecommerce-events-history-in-cosmetics-shop
- Performed EDA (Exploratory Data Analysis) on the dataset and observed few errors in the dataset.

# Key observations
- Event time is an object -> must be converted to datetime
- Negative price value in distribution shows error in data -> can be removed
- Category code and brand columns have a lot of null values -> columns can be ignored to avoid missing data
- Negligible amount of null user-sessions present -> must be removed along with users interaction with the product
- Number of user-sessions per product is heavily skewed -> products with significant number of user sessions can be chosen for further work
- Price distributions are not different for event types
- Duplicate records exist -> must be removed

# Instructions
- Download the dataset and extract the files into 'cosmetics dataset' folder
- To pre-process the data:
```
python3 preprocess.py <filter_flag> <min> <max>
```
- *filter_flag* must be 1 to get a filtered dataset along with the preprocessed dataset. Filtering parameters can be set using *min* and *max* arguments. min and max are the minimum and maximum number of user_sessions a product must have to be included in the data. Any of the arguments can be left out. By default, min = 100; max = 1100
- The output datatsets are stored in folder 'preprocessed_data'
