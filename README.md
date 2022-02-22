# Coinisky_Algo
Coinisky Algorithms
1. Data description :-

        1.Datatype
        2.Count 
        3.Null value count
        4.Distinct values
        5.Mean
        6.Std
        7.Max
        8.Min
        Run :- python pandas_description.py
        
2.Feature Engineering:-
 
        1.If a column is categorial(less than 8 distinct values) and having null values then apply forward_fill and backward fill to fill the values and apply label encoding on top of that.
        2.Otherwise if column is int or float then fill null values with mean
        3.Currently, Discard all other columns **(Need Disscusion on this)
        
3.Models:

        1.Logistic regression
        2.gaussianNb
        3.Svm kernel:linear
        4.Svm Kernel:rbf
        5.Knn
        6.Decision treee
        7.Random forest
4.Data :-
        “s3://jasbir/20-02-2022/customer_churn_data.csv”
5.Output :- 
        “s3://jasbir/20-02-2022/model_result.csv”
 
              
