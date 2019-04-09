import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn import svm
from sklearn import tree
from sklearn import metrics
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
# from sklearn.metrics import precision_score
import matplotlib.pyplot as plt


features = pd.read_csv('features.csv', index_col='reviewID')
genuine = features[features['label'] == 'N']
fake = features[features['label'] == 'Y']
genuine = train_test_split(genuine, train_size=0.2, test_size=0.0)[0]
sample = genuine.append(fake)
feature_set = [
    'length',
    'avg_w_len',
    'c_words',
    'word_num_avg',
    'c_letters',
    'total_reviews'
]
data = sample.loc[:, feature_set]
labels = sample['label']
x_train, x_test, y_train, y_test = train_test_split(data,
                                                    labels,
                                                    test_size=0.1)
y_train = np.where(y_train == 'Y', 1, 0)
y_test = np.where(y_test == 'Y', 1, 0)

logisticRegr = LogisticRegression(max_iter=1000, solver='liblinear')
logisticRegr.fit(x_train, y_train)
probs = logisticRegr.predict_proba(x_test)
probs = probs[:, 1]
auc = roc_auc_score(y_test, probs)
print('AUC: %.3f' % auc)
fpr, tpr, thresh = roc_curve(y_test, probs)
score = logisticRegr.score(x_test, y_test)
print('Logistic Score: ', score)


sgd = SGDClassifier(max_iter=1000, tol=1e-3)
sgd.fit(x_train, y_train)
score = sgd.score(x_test, y_test)
print('SGD Score: ', score)


svc = svm.SVC(gamma='scale')
svc.fit(x_train, y_train)
y_pred = svc.predict(x_test)
print('SVM Score: ', metrics.accuracy_score(y_test, y_pred))


decision_tree = tree.DecisionTreeClassifier()
decision_tree.fit(x_train, y_train)
score = decision_tree.score(x_test, y_test)
print('Tree Score: ', score)

plt.plot([0, 1], [0, 1], linestyle='--')
plt.plot(fpr, tpr, marker='.')
plt.show()
