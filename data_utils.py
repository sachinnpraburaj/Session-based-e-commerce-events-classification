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

        df_copy = df_copy.loc[df_copy.price > 0, :] # positive price filter
        df_copy = df_copy.drop_duplicates() # drop duplicate records
        self.df = df_copy
        print('After pre-processing:')
        self.explore_data(self.df)

    def filter_products(self,start,end):
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

        if self.df[self.df.price<=0].shape[0] == 0:
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

class classifierInputData():
        datapath = 'preprocessed_data/'

        def read_data(self):
            self.df = pd.read_csv(self.datapath+'filtered_data.csv',header=0,parse_dates=['event_time'],infer_datetime_format=True)
            self.df['event_type'] = self.df['event_type'].astype('category')


        def get_demand(self, window_size):
            demand_df = self.df.copy()
            demand_df['year'] = demand_df.event_time.dt.year
            demand_df['month'] = demand_df.event_time.dt.month
            demand_df['day'] = demand_df.event_time.dt.day
            demand_df = demand_df.groupby(['product_id','year','month','day']) \
                .agg({'user_session':'nunique'}).reset_index()
            demand_df['date'] = pd.to_datetime(demand_df[['year','month','day']])

            for w in range(1,window_size+1):
                demand_df['shift_'+str(w)] = demand_df.user_session.shift(periods=w)
            demand_df = demand_df.dropna()

            for w1 in range(1,window_size+1):
                demand_df['prev_'+str(w1)] = 0
                for w2 in range(1, w1+1):
                    demand_df['prev_'+str(w1)] += demand_df['shift_'+str(w2)]
                demand_df['prev_'+str(w1)] = (demand_df['prev_'+str(w1)] / w1).astype('float')

            demand_df = demand_df[['product_id','date']+['prev_'+str(w1) for w1 in range(1,window_size+1)]]
            self.demand_df = demand_df
            del demand_df

        def get_input_data(self, window):
            df_copy = self.df.copy()
            # retain user-product combinations with cart event_type
            df_copy = df_copy.merge(df_copy.loc[df_copy.event_type=='cart',['product_id','user_id']].drop_duplicates() \
                        ,on=['product_id','user_id'],how='inner')

            # identifying latest cart event time
            last_cart_df = df_copy.loc[df_copy.event_type =='cart',['user_id','product_id','event_time']] \
                    .groupby(['user_id','product_id']).event_time.last().reset_index() \
                    .rename(columns={'event_time':'last_cart_time'})
            df_copy = df_copy.merge(last_cart_df,on=['user_id','product_id'],how='inner')
            del last_cart_df

            # time division based feature and label dataframes
            feature_df = df_copy.loc[df_copy.event_time <= df_copy.last_cart_time, ['user_id','product_id','price','event_type','user_session','event_time']]
            label_df = df_copy.loc[df_copy.event_time > df_copy.last_cart_time, ['user_id','product_id','event_type']]

            self.df = df_copy
            del df_copy

            # feature engineering
            for event in list(feature_df.event_type.unique()):
                feature_df[event] = (feature_df.event_type == event)

            feature_df = feature_df.sort_values(['user_id','product_id','event_time'])

            agg_func = dict()
            agg_func['price'] = ['first','mean','last']
            agg_func['event_type'] = 'count'
            agg_func['user_session'] = 'nunique'
            agg_func['event_time'] = ['first','last']
            agg_func['cart'] = 'sum'
            agg_func['view'] = 'sum'
            agg_func['remove_from_cart'] = 'sum'
            agg_func['purchase'] = 'sum'

            feature_df = feature_df.groupby(['user_id','product_id']).agg(agg_func).reset_index()
            feature_df.columns = ['_'.join(col) if col[1] != '' else ' '.join(col).strip() for col in feature_df.columns.values]


            # get average product demand for previous n days
            feature_df['date'] = pd.to_datetime(feature_df.event_time_last.dt.date)
            self.get_demand(window)
            feature_df = feature_df.merge(self.demand_df,on=['product_id','date'],how='inner')

            feature_df['price_change_percent'] = (100 * (feature_df['price_last'] - feature_df['price_first']) / feature_df['price_first'])
            feature_df['tenure'] = feature_df['event_time_last'].dt.dayofyear - feature_df['event_time_first'].dt.dayofyear
            feature_df['day_of_week'] = feature_df['date'].dt.dayofweek

            feature_df['lifetime_value'] = feature_df['price_mean']*feature_df['tenure']*feature_df['purchase_sum']
            feature_df = feature_df[['user_id','product_id','event_type_count','user_session_nunique','view_sum','cart_sum','remove_from_cart_sum','purchase_sum','price_mean','price_last','price_change_percent','tenure','day_of_week','lifetime_value']+['prev_'+str(w) for w in range(1,window+1)]]

            # creating labels
            label_df = label_df[label_df.event_type != 'view']
            label_df['event_type'] = label_df.event_type.apply(lambda x: 1 if x == 'purchase' else -1)
            label_df = label_df.groupby(['user_id','product_id']).agg({'event_type':'max'}).reset_index()

            # creating input dataframe
            final_df = feature_df.merge(label_df,on=['user_id','product_id'],how='outer').fillna(0)

            final_df.columns = ['user_id','product_id','interactions','sessions','no_view','no_cart','no_remove_from_cart','no_purchase','avg_price','latest_price','price_change','tenure','day_of_week','lifetime_value']+['prev_'+str(w) for w in range(1,window+1)]+['event_type']
            self.df = final_df
            del final_df
