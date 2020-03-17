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
