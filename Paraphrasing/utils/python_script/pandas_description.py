import pandas as pd
import numpy as np
import config
import feature_engineering
#from feature_engineering import fillna_mean, apply_label_encoding 
# from feature_engineering import fillna_bfill
# ["datatype","count of data","count of null value", "unique count", "mead","std","max","min"]
#data = pd.read_csv('customer_churn_data.csv')
import boto
import boto.s3.connection
import boto3
import io

access_key = "AKIASSBSP25TUI3GPT27"
secret_key = "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"
# conn = boto.connect_s3(aws_access_key_id = access_key,
#                         aws_secret_access_key = secret_key)
#s3 = boto3.client("s3",aws_access_key_id = access_key,
                        aws_secret_access_key = secret_key)
#data_obj = s3.get_object(Bucket="jasbir", Key="20-02-2022/customer_churn_data.csv")

#data = pd.read_csv(io.BytesIO(data_obj['Body'].read()))
class describe_data:
    def __init__(self,dataset):
        self.dataset = dataset
        self.data_entities = {}
        self.data_entities["total_rows"] = len(self.dataset)
        self.data_entities["total_column"] = len(self.dataset.columns)
        self.data_entities["column_data"] = []


    def get_attribute(self):
        for col in self.dataset.columns:
            buffer_data_entities = {}
            buffer_data_entities["name"] = col
            buffer_data_entities["datatype"]=str(self.dataset[col].dtypes)
            buffer_data_entities["null count"] = len(self.dataset[col]) - self.dataset[col].count()
            buffer_data_entities["unique"] = len(pd.unique(self.dataset[col]))
            if (buffer_data_entities["datatype"]=="float64" or buffer_data_entities["datatype"]=="int64"):
                buffer_data_entities["mean"] = self.dataset[col].mean()
                buffer_data_entities["std"] =self.dataset[col].std()
                buffer_data_entities["max"] =self.dataset[col].max()
                buffer_data_entities["min"] = self.dataset[col].min()
            else:
                buffer_data_entities["mean"] = None
                buffer_data_entities["std"] = None
                buffer_data_entities["max"] = None
                buffer_data_entities["min"] = None
            self.data_entities["column_data"].append(buffer_data_entities)
        return self.data_entities
class apply_fe:
    def __init__(self,dataset):
        obj = describe_data(dataset)
        self.dataset = dataset
        self.description = obj.get_attribute()
        self.response = feature_engineering.apply_label_encoding(self.dataset[self.description["column_data"][-1]["name"]])
        self.dataset.drop(columns =self.description["column_data"][-1]["name"], inplace = True)
        self.dataset.drop(columns =self.description["column_data"][0]["name"],inplace=True)
    #checking importance,removing null,onehot encoding
    def checking_func(self):
        dummy_data = pd.DataFrame()
        # for col in self.dataset.columns:
        # print(self.description)
        for i in self.description["column_data"][1:-1]:
            # if self.description[col]["unique"] < config.value_for_label_encoder:
            if i["unique"] < config.value_for_label_encoder:
                # used backward fill or forward fill to null value
                if i["null count"] > 0:
                    dummy_data[i["name"]]= feature_engineering.apply_label_encoding(feature_engineering.fillna_ffill(self.dataset[i["name"]]))
                else:
                    dummy_data[i["name"]]= feature_engineering.apply_label_encoding(self.dataset[i["name"]])
                # do label encoding and add to dummy data

            else:
                if (i["datatype"]=="float64" or i["datatype"]=="int64"):
                    # use mean to fill null val
                    if i["null count"] > 0:
                        dummy_data[i["name"]]= fillna_mean(self.dataset[i["name"]])
                    else:
                        dummy_data[i["name"]] = self.dataset[i["name"]]
                else:
                    pass
                    # used backward fill or forward fill to null value
                    # add data to dummy data

                    #  if self.description[col][2] > 0:
                    #     dummy_data[col]= fillna_ffill(self.dataset[col])
                    # else:
                    #     dummy_data[col] = self.dataset[col]
        return(dummy_data,self.response,self.description)
                    



if __name__ == "__main__":
    access_key = "AKIASSBSP25TUI3GPT27"
    secret_key = "vcVHY3F9v3IyUL+NG5X8Ehv4qkkawSSmtD3rvkIO"
    # conn = boto.connect_s3(aws_access_key_id = access_key,
    #                         aws_secret_access_key = secret_key)
    s3 = boto3.client("s3",aws_access_key_id = access_key,
                            aws_secret_access_key = secret_key)
    bucket = s3.Bucket('jasbir')
    for object_summary in bucket.objects.filter(Prefix="20-02-2022"):
        key_1 = object_summary.key
        if key_1.endswith(".csv"):
            data_obj = s3.get_object(Bucket="jasbir", Key="20-02-2022/" + key_1)
            data = pd.read_csv(io.BytesIO(data_obj['Body'].read()))
            obj = describe_data(data)
            # get description of data
            return obj.get_attribute()

            # dummy_data,response,description = apply_fe(data).checking_func()
            # print(dummy_data.shape)
            # print(response.shape)
