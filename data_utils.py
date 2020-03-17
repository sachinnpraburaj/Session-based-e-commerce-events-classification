import pandas as pd
import numpy as np
import random

class ProcessData():
    datapath = 'cosmetics dataset/'

    def mem_usage(self, df):
        usage_b = df.memory_usage(deep=True).sum()
        usage_mb = usage_b / 1024 ** 2 # convert bytes to megabytes
        return "{:03.2f} MB".format(usage_mb)

    def explore_data(self, df):
        print("Memory Usage: ", self.mem_usage(df))
        print("Number of records and columns: ",df.shape)
        df_columns = df.columns
        print(df.dtypes)
        print("Null %: ",100*(df.isnull().any(axis=1).sum()/df.shape[0]))

    def read_data(self):
        oct_df = pd.read_csv(self.datapath+'2019-Oct.csv')
        nov_df = pd.read_csv(self.datapath+'2019-Nov.csv')
        self.df = pd.concat([oct_df,nov_df])
        self.explore_data(self.df)

    def read_sample_data(self):
        sample_file = self.datapath+'2019-Oct.csv'
        n = sum(1 for line in open(sample_file)) - 1 #number of records in file (excludes header)
        s = 100000 #desired sample size
        skip = sorted(random.sample(range(1,n+1),n-s)) #the 0-indexed header will not be included in the skip list
        self.df = pd.read_csv(sample_file, skiprows=skip)
        self.explore_data(self.df)

    def optimized_read(self):
        column_types = dict()
        column_types['event_type'] = 'category'
        column_types['product_id'] = 'uint32'
        column_types['category_id'] = 'uint64'
        column_types['price'] = 'float32'
        column_types['user_id'] = 'uint32'
        column_types['user_session'] = 'object'

        oct_df = pd.read_csv(self.datapath+'2019-Oct.csv',dtype=column_types,parse_dates=['event_time'],infer_datetime_format=True)
        nov_df = pd.read_csv(self.datapath+'2019-Nov.csv',dtype=column_types,parse_dates=['event_time'],infer_datetime_format=True)
        self.df = pd.concat([oct_df,nov_df])
        self.explore_data(self.df)

    def pre_process(self):
        df_copy = self.df.copy()
        df_copy = df_copy.drop(['category_code','brand'], axis='columns')

        # handling missing user sessions
        user_product = df_copy[df_copy.user_session.isnull()][['user_id','product_id']].drop_duplicates()
        df_copy = df_copy.merge(user_product,on=['user_id','product_id'],how='outer', indicator=True)
        df_copy = df_copy.loc[df_copy._merge == 'left_only', :]
        df_copy = df_copy.drop(['_merge'], axis='columns')

        df_copy = df_copy.loc[df_copy.price >= 0, :] # non-negative price filter
        df_copy = df_copy.drop_duplicates() # drop duplicate records
        self.df = df_copy
        print('After pre-processing:')
        self.explore_data(self.df)

    def filter_products(self,start=100,end=1100):
        df_copy = self.df.copy()

        # products with significant user sessions
        sess_product = df_copy.groupby('product_id')[['user_session']].nunique() \
            .reset_index().sort_values(by=['user_session'],ascending=False) \
            [['product_id']][start:end]
        df_copy = df_copy.merge(sess_product,on=['product_id'],how='inner')

        self.filtered_df = df_copy
        print("After filtering products:")
        self.explore_data(self.filtered_df)

    def verify_preprocess(self):
        msg = dict()
        if 'event_time' in self.df.select_dtypes(include=[np.datetime64]).columns.tolist():
            msg['event_time'] = 'success'
        else:
            msg['event_time'] = 'fail'

        if self.df[self.df.price<0].shape[0] == 0:
            msg['price'] = 'success'
        else:
            msg['price'] = 'fail'

        if self.df[self.df.user_session.isnull()].shape[0] == 0:
            msg['user_session'] = 'success'
        else:
            msg['user_session'] = 'fail'

        if self.df[self.df.duplicated()].shape[0] == 0:
            msg['duplicates'] = 'success'
        else:
            msg['duplicates'] = 'fail'

        for key,value in msg.items():
            print(key,':',value)
