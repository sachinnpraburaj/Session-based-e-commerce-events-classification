# Session-based-e-commerce-analysis

- This project explores eCommerce events data to identify potential business intelligence use-cases and to develop data-driven solutions using machine learning
- The Kaggle eCommerce Events History in Cosmetics Shop was used for this project.
  Link to dataset: https://www.kaggle.com/mkechinov/ecommerce-events-history-in-cosmetics-shop

# Key aspects of the project
- Optimized memory usage of source dataframe by ~60% by efficiently reading the data.
- Performed initial EDA to identify errors in data and pre-processed accordingly
- Engineered key business-relevant features like customer lifetime value and aggregate product demand during window
- Used *Random Forest classifier* to predict user's activity - purchase, no change or remove from cart - after they add an item to the cart
- Performed hyperparameter optimization to improve model performance using Random Search and Grid Search

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

### initial EDA and key observations: [e-commerce EDA.ipynb](notebooks/e-commerce%20EDA.ipynb)
- Performed initial EDA (Exploratory Data Analysis) on the dataset to observe errors in the dataset.
- Event time is an object -> must be converted to datetime
- Negative and zero price value in distribution shows error in data -> can be removed
- Category code and brand columns have a lot of null values -> columns can be ignored to avoid missing data
- Negligible amount of null user-sessions present -> must be removed along with users interaction with the product
- Number of user-sessions per product is heavily skewed -> products with significant number of user sessions can be chosen for further work
- Price distributions are not different for event types
- Duplicate records exist -> must be removed

### data pre-processing: [preprocess.py](preprocess.py)
- Optimized memory usage by efficiently reading the data
- Handled observations from EDA to pre-process data
- Enabled filtering of data based on number of unique user-sessions
- Generated pre-processed and subset of pre-processed dataset for other use-cases

### feature engineering for classification: [generate_input.py](generate_input.py)
- Identified user's latest add to cart interaction time with a product
- Aggregated interactions before latest add to cart activity to generate input features for the classifier
- Used interactions after latest add to cart activity to generate labels for the dataset
```
1 - Purchased | 0 - No Activity | -1 - Removed from cart
```

### multi-class classification with hyperparameter optimization: [multi class classification.ipynb](notebooks/multi%20class%20classification.ipynb)
- One hot encoded categorical variables
- Predicted user's activity using random forest classifier with 71% accuracy
- Optimized hyperparameters using random search and grid search cross validation techniques
- Improved model accuracy to 00% accuracy
- Optimal hyperparameters:
```
n_estimators: | min_depth: |
```

# Future improvements
- More relevant features can be engineered to enhance the quality of the input data
- Explainable AI practices can be incorporated using SHAP or LIME for better explaining the results and feature importance 
- Recurrent Neural Network can be used to encode user's activity and predict next user activity
