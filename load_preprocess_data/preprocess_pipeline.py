import pandas as pd
import numpy as np

from typing import List
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


#preprocessing price feature
def preprocess_target_feature(x): 
        value = ''.join(char for char in x if char.isdigit() or char=='.')
        if (value.count('0') >= 3) and ('.' not in value): 
            return 100000 - float(value)
        else: 
            if '.' in value: #for values like 7.62, 53.3
                return (float(value.split('.')[0])*100000) + (float(value.split('.')[1])*1000)
            else: 
                return float(value) * 100000
            

class RemoveUnwantedColsAndRows(BaseEstimator,TransformerMixin):
    def __init__(self, unwanted_columns: List[str], non_nan_row_threshold:int = 90):
        self.unwanted_columns = unwanted_columns
        self.non_nan_row_threshold = non_nan_row_threshold
        return None

    def fit(self,X):
        self.column = X.columns
        return self

    def transform(self,X):
        x_transformed = X.copy()
        x_transformed.drop(self.unwanted_columns,axis=1,inplace = True)
        #removing rows which has Nan more than given threshold
        x_transformed.dropna(thresh = self.non_nan_row_threshold, axis = 0, inplace = True)
        print("The dropped columns are ")
        print(' '.join([col for col in self.column if col not in x_transformed.columns]))
        return x_transformed.reset_index(drop=True)
    

class StandardizeColumnName(BaseEstimator, TransformerMixin):
    def __init__(self,rename_columns):
        self.rename_columns = rename_columns

    def fit(self, X):
        return self
    
    def transform(self, X):
        transformed_df = X.copy()
        transformed_df.rename(columns = self.rename_columns, inplace= True)
        transformed_df.columns = [col.lower().replace(' ','_') for col in transformed_df.columns]
        return transformed_df

    
class CustomStandardScaler(BaseEstimator, TransformerMixin): 
    def __init__(self,is_train): 
        self.is_train = is_train
        self.column_names = ['kerb_weight', 'height', 'wheel_base','length','width','kilo_meter',
                'model_year','engine_displacement']
        
    def fit(self, X): 
        self.x_ss = StandardScaler()
        self.x_ss.fit(X[(X[self.column_names]!=-1).any(axis=1)][self.column_names])
        self.y_ss = StandardScaler()
        self.y_ss.fit(X[['price']])
        return self
    
    def transform(self, X): 
        transformed_df = X.copy()
        output_df = pd.DataFrame(self.x_ss.transform(transformed_df[self.column_names]),
                                columns = self.x_ss.get_feature_names_out())
        if self.is_train:
            price_col = pd.DataFrame(self.y_ss.transform(transformed_df[['price']]),columns=['price'])
            transformed_df = transformed_df.drop('price',axis = 1)
            output_df = pd.concat([output_df,price_col],axis= 1)
        transformed_df = transformed_df.drop(self.column_names, axis= 1)
        transformed_df = pd.concat([transformed_df,output_df],axis=1)
        return transformed_df
    

class preprocess_numerical_column(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.column_names = ['length','width','height','wheel_base','kerb_weight','kilo_meter'] 
        pass

    def convert_numerical(self, x):
        #works for Length and Width features only
        if pd.notna(x):
            val  = str(x)
            if ','  in val:
                val = val.replace(',','')
            if '-' in val:
                val = val.split('-')[0]
            val = val.strip() 
            val = ''.join([char for char in val if char.isdigit()])
            if len(str(val))>1 :
                return int(val)
            else: 
                return None
        else:
            return None
    
    def convert_numerical_engine_cc(self, x):
        if pd.notna(x):
            val  = str(x).strip()
            val = ''.join([char for char in val if char.isdigit()])
            if int(val)>600:
                return int(val)
            else: 
                
                return None
        else:
            return None
    
    def fit(self, X):
        return self
    

    def transform(self, X):
        transformed_df = X.copy()
        #preprocess values
        for col in self.column_names:
            transformed_df[col] = transformed_df[col].apply(self.convert_numerical)
        transformed_df['engine_displacement'] = transformed_df['engine_displacement'].apply(self.convert_numerical_engine_cc)

        return transformed_df
    


class impute_numerical_missing_values(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        self.col_names = ['length','width','wheel_base','height','kerb_weight','engine_displacement','kilo_meter']
        

    def impute_null_with_lookup(self,model_name, model_year, look_up_table):
        if (model_name,model_year) in look_up_table.index:
            return look_up_table.loc[(model_name,model_year)]
        elif model_name in [model_name for model_name,_ in look_up_table.index]: 
            return look_up_table.loc[(model_name)].iloc[-1]
        else:
            return -1 

    def fit(self, X):
        X_copy = X.copy()
        self.lookup_tables = {}
        for col in self.col_names: 
            self.lookup_tables[col] = X_copy[pd.notna(X_copy[col])].groupby(['model','model_year'])[col].mean()
        return self
    
    def transform(self, X):
        transformed_df = X.copy()        

        for row in X[X.isna().any(axis=1)].iterrows():
            model_name = row[1]['model']
            model_year = row[1]['model_year']
            for col in self.col_names:
                val = row[1][col]
                if pd.isna(val):
                    impute_value = self.impute_null_with_lookup(model_name, model_year, self.lookup_tables[col])
                    transformed_df.iloc[row[0],list(X.columns).index(col)] = impute_value
    
        return transformed_df

    


class preprocess_categorical_features(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass 
    

    def turbo_charger_encode(self,x): 
        if pd.isna(x): 
            return None
        else:
            lower_x = x.lower().strip()
            if ('yes' in lower_x) or ('twin' in lower_x) or ('turbo' in lower_x):
                return 1
            else: 
                return 0
            

    def brake_encode(self,x): 
        if pd.isna(x):
            return None
        else :
            lower_x = x.lower().strip()
            if ('disc' in lower_x) or ('abs' in lower_x) or ('disk' in lower_x):
                return 1
            elif ('drum' in lower_x):
                return 0
            else:
                return None
                
    def tyre_preprocessing(self,x): 
        if pd.isna(x):
            return 'None/other'
        else:
            lower_x = x.lower().strip()
            
            if ('radial' in lower_x ) and ('runflat' in lower_x):
                return 'radial_runflat'
            elif ('runflat' in lower_x) and ('tubeless' in lower_x):
                return 'runflat_tubeless'
            elif ('tubeless' in lower_x) and ('radial' in lower_x):
                return 'tubeless_radial'
            elif 'runflat' in lower_x:
                return 'runflat'
            elif 'radial' in lower_x: 
                return 'radial'
            elif 'tubeles' in lower_x: 
                return 'tubeless'
            else: 
                return 'None/other'
            
    def transmission_encode(self,x): 
        x = x.lower().strip()
        if 'automatic' == x:
            return 1
        else: 
            return 0
        
    def cylinder_encode(self,x):
        if pd.notna(x):
            if x > 8:
                return None
            else: 
                return x
        else:
            return x


    def fit(self, X): 
        return self
    
    def transform(self, X):
        transformed_x = X.copy()
        transformed_x['front_brake_type'] = transformed_x['front_brake_type'].apply(self.brake_encode)
        transformed_x['rear_brake_type'] = transformed_x['rear_brake_type'].apply(self.brake_encode)
        transformed_x['turbo_charger']  = transformed_x['turbo_charger'].apply(self.turbo_charger_encode)
        transformed_x['transmission'] = transformed_x['transmission'].apply(self.transmission_encode)
        transformed_x['no_of_cylinder'] = transformed_x['no_of_cylinder'].apply(self.cylinder_encode)
        transformed_x['tyre_type'] = transformed_x['tyre_type'].apply(self.tyre_preprocessing)
        return transformed_x                    

        
class impute_categorical_feature(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.column_names = ['front_brake_type','rear_brake_type','turbo_charger','transmission','no_of_cylinder','tyre_type']
        
    def impute_null_with_lookup(self,model_name, model_year, col_name):
        look_up_table = self.lookup_table[col_name]
        if (model_name,model_year) in look_up_table.index:
            val = look_up_table.loc[(model_name,model_year)]
            return val
        elif model_name in [model_name for model_name,_ in look_up_table.index]: 
            val = look_up_table.loc[(model_name)].iloc[-1]
            return val
        else:
            return -1 

    def fit(self, X):
        self.type = []
        def get_mode(val): 
            mode = pd.Series.mode(val)
            self.type.append(type(mode))
            if len(mode)>1:
                return mode[0]
            else: 
                return mode
            
        X_copy = X.copy()
        self.lookup_table = {
            col: X_copy[pd.notna(X_copy[col])].groupby(['model','model_year'])[col].agg(get_mode) for col in self.column_names}
        return self
        
    def transform(self,X):
        transformed_df = X.copy()
        for row in X[X.isna().any(axis=1)].iterrows():
            model_name = row[1]['model']
            model_year = row[1]['model_year']
            
            for col in self.column_names:
                val = row[1][col]

                if pd.isna(val):
                    impute_value = self.impute_null_with_lookup(model_name, model_year,col)
                    transformed_df.iloc[row[0],list(X.columns).index(col)] = impute_value
    
        return transformed_df
    

    
class OneHotEncoding(BaseEstimator, TransformerMixin):
    def __init__(self,column_names): 
        self.column_names = column_names

    def fit(self, X):
            self.ohe = OneHotEncoder(sparse_output=False,dtype = int)
            self.ohe.fit(X[self.column_names])
            return self
    
    def transform(self,X): 
            ohe_value = self.ohe.transform(X[self.column_names])
            tranformed_df = pd.DataFrame(ohe_value, columns=self.ohe.get_feature_names_out())
            tranformed_df = pd.concat([X,tranformed_df], axis= 1)
            return tranformed_df.drop(self.column_names,axis = 1)
    

class TargetEncoding(BaseEstimator, TransformerMixin): 
    def __init__(self): 
        self.column_names = ['original_equipment_manufacturer', 'model', 'color']
        pass
        
    def fit(self, X):
        #target encoding
        self.mean_encoding = {}
        for col in self.column_names: 
            groupby_results = X[[col,'price']].groupby([col]).agg(mean_price = ('price','mean'),
                                                                          count = ('price','size'))
            
            self.mean_encoding[col] = groupby_results[groupby_results['count']>5]['mean_price']
        return self

    def transform(self, X):
        transformed_df = X.copy()
        col_idxes = [(list(X.columns).index(col),col) for col in self.column_names]
        for idx in range(X.shape[0]):
            for col_idx,col in col_idxes:
                val = transformed_df.iloc[idx,col_idx] 
                if pd.notna(val) and (val in self.mean_encoding[col]):
                    transformed_df.iloc[idx,col_idx] = self.mean_encoding[col][val]
                else:
                    transformed_df.iloc[idx,col_idx] = -1

        return transformed_df

def initialize_pipeline():
    numerical_pipeline = Pipeline([
        ('remove_unwanted_col_row', RemoveUnwantedColsAndRows(
            unwanted_columns = ["it","owner","centralVariantId","variantName","priceActual","priceSaving","priceFixedText",
                                "trendingText","Fuel Type","Ownership","Transmission","Year of Manufacture","Values per Cylinder",
                                "Value Configuration","BoreX Stroke","Compression Ratio","Max Power","Max Torque","Super Charger","Cargo Volumn","Top Speed",
                                "Acceleration","Turning Radius","Alloy Wheel Size","Rear Tread","Gross Weight","Front Tread","Engine Type","Ground Clearance Unladen",
                                "Seating Capacity","Gear Box","Steering Type", "Drive Type","No Door Numbers",'Displacement','RTO','Seats','Kms Driven','Registration Year',
                                'Insurance Validity','Fuel Suppy System','No Of Airbags','Number Of Speaker'],
            non_nan_row_threshold = 90)),

        ('standardize_column_names', StandardizeColumnName(
            
            rename_columns={'ft':'fuel_type','bt': 'body_type','km': 'kilo_meter', 'oem': 'original_equipment_manufacturer','modelYear': 'model_year',
                            'Wheel Base': 'wheel_base','Kerb Weight': 'kerb_weight','Rear Brake Type': 'rear_brake_type','Front Brake Type': 'front_brake_type',
                            'No of Cylinder': 'no_of_cylinder','Tyre Type' : 'tyre_type','Turbo Charger': 'turbo_charger'})),

        ('formatting_column', preprocess_numerical_column()),
        ('impute_missing_values',impute_numerical_missing_values()),
        ('standardization', CustomStandardScaler(is_train=True))
        
    ])



    categorical_pipeline = Pipeline([
        ('formatting_columns',preprocess_categorical_features()),
        ('impute_missing_values',impute_categorical_feature()),
        ('ohe', OneHotEncoding(column_names = ['fuel_type', 'body_type','location','no_of_cylinder','tyre_type'])),
        ('target_encoding', TargetEncoding())
    ])

    final_pipeline = Pipeline([
    ('numerical_pipeline', numerical_pipeline),
    ('categorical_pipeline',categorical_pipeline),
    ])

    return final_pipeline
            



