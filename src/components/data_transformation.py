import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from src.exception import CustomException
from src.logger import logging
from sklearn.impute import SimpleImputer
import os
from src.utils import save_object

@dataclass
class DataTransformConfig:
    preprocessor_obj_file_path=os.path.join('artifact',"preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformConfig()

    def get_data_transform_object(self):
        '''
        This function is responsible for transfromation of data based on it types
        '''
        try:   
            categorial_column=[
                'buying',
                'maintenance',
                'doors',
                'person', 
                'lug_boot', 
                'safety', 
                
            ]
            cat_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("One_hot_encoder",OneHotEncoder())
                ]
            )
            logging.info(f"Categorical column :{categorial_column}")

            preprocessor=ColumnTransformer(
                [
                    ("cat_pipeline",cat_pipeline,categorial_column)
                ]
            )

            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read Train and Test data completed")

            logging.info("Obtaining preprocessing object")

            preprocessor_obj=self.get_data_transform_object()

            target_column_name="acceptability"
            

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]
            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]
            ##

            logging.info(
                f"Applyiing prepocessor object on training and testing dataframe"
            )
            input_feature_train_arr=preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessor_obj.transform(input_feature_test_df)

            import scipy.sparse  # Add this

            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)

            # Handle sparse matrices
            if scipy.sparse.issparse(input_feature_train_arr):
                input_feature_train_arr = input_feature_train_arr.toarray()# type: ignore 
            if scipy.sparse.issparse(input_feature_test_arr):
                input_feature_test_arr = input_feature_test_arr.toarray()#type: ignore

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df).reshape(-1, 1)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df).reshape(-1, 1)]




            


            logging.info("Saved Prepocessing Object.")


            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessor_obj
            )
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        except Exception as e:
            raise CustomException(e,sys)