import pandas as pd
import numpy as np
from io import StringIO
import config
from pandas_description import apply_fe
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler 

from sklearn import svm, tree, linear_model, neighbors
from sklearn import naive_bayes, ensemble, discriminant_analysis, gaussian_process
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from xgboost import XGBClassifier

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

#sklearn modules for Model Evaluation & Improvement---------------------------
    
from sklearn.metrics import confusion_matrix, accuracy_score 
from sklearn.metrics import f1_score, precision_score, recall_score, fbeta_score
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV

from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import KFold

from sklearn import feature_selection
from sklearn import model_selection
from sklearn import metrics

from sklearn.metrics import classification_report, precision_recall_curve
from sklearn.metrics import auc, roc_auc_score, roc_curve
from sklearn.metrics import make_scorer, recall_score, log_loss
from sklearn.metrics import average_precision_score
#connection for connection
import boto
import boto.s3.connection
import boto3
import io

access_key = "AKIASSBSP25TUI3GPT27"
secret_key = "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"
# conn = boto.connect_s3(aws_access_key_id = access_key,
#                         aws_secret_access_key = secret_key)
s3 = boto3.client("s3",aws_access_key_id = access_key,
                        aws_secret_access_key = secret_key)
data_obj = s3.get_object(Bucket="jasbir", Key="20-02-2022/customer_churn_data.csv")

data = pd.read_csv(io.BytesIO(data_obj['Body'].read()))
dataset,response,description = apply_fe(data).checking_func()

# spliting of data
# class apply_model:
    # def __init__(self,dataset,)
X_train, X_test, y_train, y_test = train_test_split(dataset, response,
                                                    stratify=response, 
                                                    test_size = 0.3,
                                                    random_state = 0)

def ml_algo():
    models = []
    models.append(('Logistic Regression', LogisticRegression(solver='liblinear', random_state = 0,
                                                            class_weight='balanced')))
    models.append(('SVC', SVC(kernel = 'linear', random_state = 0)))
    models.append(('Kernel SVM', SVC(kernel = 'rbf', random_state = 0)))
    models.append(('KNN', KNeighborsClassifier(n_neighbors = config.baseline_knn_neighbour,
                                                metric = config.baseline_knn_metrics, 
                                                p = config.baseline_knn_p)))
    models.append(('Gaussian NB', GaussianNB()))
    models.append(('Decision Tree Classifier',
                DecisionTreeClassifier(criterion = config.baseline_dt_criterion, random_state = 0)))
    models.append(('Random Forest', RandomForestClassifier(
        n_estimators=config.baseline_rf_n_estimators, criterion = config.baseline_rf_criterion, random_state = 0)))
    return models
models = ml_algo()
def model_selection_baseline(models):
    acc_results = []
    auc_results = []
    names = []
    # set table to table to populate with performance results
    col = ['Algorithm', 'ROC AUC Mean', 'ROC AUC STD', 
        'Accuracy Mean', 'Accuracy STD']

    model_results = pd.DataFrame(columns=col)

    acc_results = []
    auc_results = []
    names = []
    # set table to table to populate with performance results
    col = ['Algorithm', 'ROC AUC Mean', 'ROC AUC STD', 
        'Accuracy Mean', 'Accuracy STD']

    model_results = pd.DataFrame(columns=col)
    i = 0
    # evaluate each model using k-fold cross-validation
    for name, model in models:
        kfold = model_selection.KFold(
            n_splits=10)  # 10-fold cross-validation

        cv_acc_results = model_selection.cross_val_score(  # accuracy scoring
            model, X_train, y_train, cv=kfold, scoring='accuracy')

        cv_auc_results = model_selection.cross_val_score(  # roc_auc scoring
            model, X_train, y_train, cv=kfold, scoring='roc_auc')

        acc_results.append(cv_acc_results)
        auc_results.append(cv_auc_results)
        names.append(name)
        model_results.loc[i] = [name,
                            round(cv_auc_results.mean()*100, 2),
                            round(cv_auc_results.std()*100, 2),
                            round(cv_acc_results.mean()*100, 2),
                            round(cv_acc_results.std()*100, 2)
                            ]
        i += 1
        
    model_results.sort_values(by=['ROC AUC Mean'], ascending=False)
    return(model_results)

def set_for_knn():
    score_array = []
    score = 0
    for each in range(1,config.set_limit_for_knn):
        knn_loop = KNeighborsClassifier(n_neighbors = each) #set K neighbor as 3
        knn_loop.fit(X_train,y_train)
        score_knn=knn_loop.score(X_test,y_test)
        score_array.append(score_knn)
        if(score_knn>score):
            score = score_knn
            best_each = each
    return(score_array,best_each)
def set_for_rf():
    score_array = []
    score = 0 
    for each in range(1,100):
        rf_loop = RandomForestClassifier(n_estimators = each, random_state = 1) 
        rf_loop.fit(X_train,y_train)
        score_rf = rf_loop.score(X_test,y_test)
        score_array.append(score_rf)
        if(score_rf>score):
            score = score_rf
            best_each = each
    return(score_array,best_each)

def lg_classifier():
    classifier = LogisticRegression(random_state = 0)
    classifier.fit(X_train, y_train)

    # Predicting the Test set results
    y_pred = classifier.predict(X_test)
    #print(y_pred)
    #Evaluate results

    acc = accuracy_score(y_test, y_pred )
    prec = precision_score(y_test, y_pred )
    rec = recall_score(y_test, y_pred )
    f1 = f1_score(y_test, y_pred )
    f2 = fbeta_score(y_test, y_pred, beta=2.0)

    results = pd.DataFrame([['Logistic Regression', acc, prec, rec, f1, f2]],
                columns = ['Model', 'Accuracy', 'Precision', 'Recall', 'F1 Score', 'F2 Score'])
    return(classifier,results)

def svc_linear():
    classifier = SVC(kernel = 'linear', random_state = 0)
    classifier.fit(X_train, y_train)
    # Predicting the Test set results 
    y_pred = classifier.predict(X_test)
    #Evaluate results
    acc = accuracy_score(y_test, y_pred )
    prec = precision_score(y_test, y_pred )
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred )
    f2 = fbeta_score(y_test, y_pred, beta=2.0)

    results = pd.DataFrame([['SVM (Linear)', acc, prec, rec, f1, f2]],
                columns = ['Model', 'Accuracy', 'Precision', 'Recall', 'F1 Score', 'F2 Score'])
    return(classifier,results)
def svc_rbf():
    classifier = SVC(kernel = 'rbf', random_state = 0)
    classifier.fit(X_train, y_train)
    # Predicting the Test set results 
    y_pred = classifier.predict(X_test)
    #Evaluate results
    acc = accuracy_score(y_test, y_pred )
    prec = precision_score(y_test, y_pred )
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred )
    f2 = fbeta_score(y_test, y_pred, beta=2.0)

    results = pd.DataFrame([['SVM (Linear)', acc, prec, rec, f1, f2]],
                columns = ['Model', 'Accuracy', 'Precision', 'Recall', 'F1 Score', 'F2 Score'])
    return(classifier,results)
def knn():
    _,n_neighbour = set_for_knn()
    classifier = KNeighborsClassifier(n_neighbors = n_neighbour, 
                                        metric = config.baseline_knn_metrics, 
                                        p = config.baseline_knn_p)
    classifier.fit(X_train, y_train)
    # Predicting the Test set results 
    y_pred  = classifier.predict(X_test)
    #Evaluate results
    acc = accuracy_score(y_test, y_pred )
    prec = precision_score(y_test, y_pred )
    rec = recall_score(y_test, y_pred )
    f1 = f1_score(y_test, y_pred )
    f2 = fbeta_score(y_test, y_pred, beta=2.0)

    results = pd.DataFrame([['K-Nearest Neighbours', acc, prec, rec, f1, f2]],
                columns = ['Model', 'Accuracy', 'Precision', 'Recall', 'F1 Score', 'F2 Score'])
    return classifier,results
def gaussian_nb():
    classifier = GaussianNB()
    classifier.fit(X_train, y_train)

    # Predicting the Test set results 
    y_pred = classifier.predict(X_test)

    #Evaluate results
    acc = accuracy_score(y_test, y_pred )
    prec = precision_score(y_test, y_pred )
    rec = recall_score(y_test, y_pred )
    f1 = f1_score(y_test, y_pred )
    f2 = fbeta_score(y_test, y_pred, beta=2.0)

    results = pd.DataFrame([['Naive Byes', acc, prec, rec, f1, f2]],
                    columns = ['Model', 'Accuracy', 'Precision', 'Recall', 'F1 Score', 'F2 Score'])
    return classifier,results
def dt():
    classifier = DecisionTreeClassifier(criterion = config.baseline_dt_criterion, random_state = 0)
    classifier.fit(X_train, y_train)


    # Predicting the Test set results 
    y_pred = classifier.predict(X_test)

    #Evaluate results
    acc = accuracy_score(y_test, y_pred )
    prec = precision_score(y_test, y_pred )
    rec = recall_score(y_test, y_pred )
    f1 = f1_score(y_test, y_pred )
    f2 = fbeta_score(y_test, y_pred, beta=2.0)

    results = pd.DataFrame([['Decision Tree', acc, prec, rec, f1, f2]],
                columns = ['Model', 'Accuracy', 'Precision', 'Recall', 'F1 Score', 'F2 Score'])
    return classifier,results
def rf():
    _,estimator = set_for_rf()
    classifier = RandomForestClassifier(n_estimators = estimator, 
                                        criterion = config.baseline_rf_criterion, random_state = 0)
    classifier.fit(X_train, y_train)
    # Predicting the Test set results 
    y_pred = classifier.predict(X_test)
    #Evaluate results
    from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, precision_score, recall_score
    acc = accuracy_score(y_test, y_pred )
    prec = precision_score(y_test, y_pred )
    rec = recall_score(y_test, y_pred )
    f1 = f1_score(y_test, y_pred )
    f2 = fbeta_score(y_test, y_pred, beta=2.0)

    results = pd.DataFrame([['Random Forest', acc, prec, rec, f1, f2]],
                columns = ['Model', 'Accuracy', 'Precision', 'Recall', 'F1 Score', 'F2 Score'])
    return classifier,results
classifier_lg,result_lg = lg_classifier()
classifier_svc_linear,result_svc_linear =svc_linear()
#print(result_svc_linear)
classifier_svc_rbf,result_svc_rbf = svc_rbf()
classifier_knn,result_knn = knn()
classifier_gaussian_nb,result_gaussian_nb = gaussian_nb()
classifier_dt,result_dt=dt()
classifier_rf,result_rf=rf()

model_results = pd.DataFrame(result_lg)
model_results=model_results.append(result_svc_linear,ignore_index=True)
model_results=model_results.append(result_svc_rbf,ignore_index=True)
model_results=model_results.append(result_knn,ignore_index=True)
model_results=model_results.append(result_gaussian_nb,ignore_index=True)
model_results=model_results.append(result_dt,ignore_index=True)
model_results=model_results.append(result_rf,ignore_index=True)
#print(model_results)
csv_buffer = StringIO()
model_results.to_csv(csv_buffer,header=True,index=False)
csv_buffer.seek(0)
s3.put_object(Bucket="jasbir",Body=csv_buffer.getvalue(),Key="20-02-2022/model_result.csv")