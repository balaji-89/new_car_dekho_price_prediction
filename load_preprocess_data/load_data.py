import pandas as pd
import os

#new_car_detail
def load_column_names(df:pd.DataFrame):
    #get car detail
    new_car_detail_column_names =  list(eval(df['new_car_detail'][0]).keys())

    #new_car_overview
    new_car_overview_column_names = list(map['key'] for map in eval(df['new_car_overview'][0])['top'])

    #new car feature
    feature_heading_value_dict = {}
    for idx in range(df.shape[0]):
        item = eval(df.new_car_feature[idx])['data']
        for element in item:
            heading_data = element['heading']
            if heading_data not in feature_heading_value_dict:
                feature_heading_value_dict[heading_data] = set()
            feature_heading_value_dict.get(heading_data).update([val['value'] for val in element['list']])


    new_car_feature_column_names = [col_name for ls in feature_heading_value_dict.values() for col_name in ls]

    #new_car_specs
    specs_heading_value_dict = {}
    for idx in range(df.shape[0]):
        item = eval(df.new_car_specs[idx])['data']
        for element in item:
            heading_data = element['heading']
            if heading_data not in specs_heading_value_dict:
                specs_heading_value_dict[heading_data] = set()
            specs_heading_value_dict.get(heading_data).update([val['key'] for val in element['list']])


    new_car_specs_column_names = [col_name for ls in specs_heading_value_dict.values() for col_name in ls]

    return new_car_detail_column_names,new_car_overview_column_names,new_car_feature_column_names,new_car_specs_column_names




def get_car_detail(df:pd.DataFrame,new_car_detail_column_names,location_info):
    new_car_detail_extracted_values = []
    for idx, val in df['new_car_detail'].items():
        val = eval(val)
        value = []
        if len(new_car_detail_column_names)-1 != len(val.keys()):
            raise Exception("Error")
            break
        for key in new_car_detail_column_names:
            if key == 'location':
                value.append(location_info)
            else:
                value.append(val[key])

        new_car_detail_extracted_values.append(value)

    return pd.DataFrame(new_car_detail_extracted_values,columns= new_car_detail_column_names)


def get_new_car_overview(df:pd.DataFrame, new_car_overview_column_names):
    new_car_overview_extracted_values = []
    for idx in range(df.shape[0]): 
        extracted_information = []
        value = {map['key']:map['value'] for map in eval(df['new_car_overview'][idx])['top']}
        for key in new_car_overview_column_names:
            extracted_information.append(value.get(key,None))
        new_car_overview_extracted_values.append(extracted_information)
    
    return  pd.DataFrame(new_car_overview_extracted_values,columns=new_car_overview_column_names)


def get_new_car_feature(df:pd.DataFrame,new_car_feature_column_names):
    extracted_values = []
    for idx in range(df.shape[0]):
        data = eval(df.new_car_feature[idx])['data']
        data_result = [False]*len(new_car_feature_column_names)
        features = []
        for item in data:
            features.extend([ls_item['value'] for ls_item in item['list']])

        for feature in features:
            feature_index = new_car_feature_column_names.index(feature)
            data_result[feature_index] = True
        
        extracted_values.append(data_result)

    return pd.DataFrame(extracted_values,columns=new_car_feature_column_names)


def get_new_car_specs(df:pd.DataFrame, new_car_specs_column_names):
    #extracting values
    new_specs_extracted_values = []
    for idx in range(df.shape[0]):
        data = eval(df.new_car_specs[idx])['data']
        specs = [None]*len(new_car_specs_column_names)
        for item in data:
            for ls_item in item['list']:
                key = ls_item['key']
                ele_idx = new_car_specs_column_names.index(key)
                specs[ele_idx] = ls_item['value']

        new_specs_extracted_values.append(specs)
    


    return pd.DataFrame(new_specs_extracted_values,columns=new_car_specs_column_names)


def load_data_structured_save():
        try:
            dataset_location = '../dataset/'
            column_names = load_column_names(pd.read_excel("../dataset/bangalore_cars.xlsx"))
            column_names[0].append('location')
            all_column_names = column_names[0]+column_names[1]+column_names[2]+column_names[3]

            final_data = pd.DataFrame(columns=all_column_names)

            for file in os.listdir(dataset_location):
                location = file.split('_')[0]
                df = pd.read_excel(dataset_location+file)
                new_car_detail_extracted_values = get_car_detail(df,column_names[0],location)
                new_car_overview_extracted_values = get_new_car_overview(df,column_names[1])
                new_car_features_extracted_values = get_new_car_feature(df,column_names[2])
                new_specs_extracted_values = get_new_car_specs(df, column_names[3])
                concatenated_data = pd.concat([new_car_detail_extracted_values,new_car_overview_extracted_values,
                                            new_car_features_extracted_values,new_specs_extracted_values],axis=1)
                final_data = pd.concat([final_data,concatenated_data],axis=0)
            
            final_data.to_csv('/home/laptop-kl-11/personal_project/car_dekho_project/dataset/extracted_dataset/extracted_data.csv',index=False)

            return "Done"

        except Exception:
            raise "Error in loading and preprocessing the data"
    





    
    


    