import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn import svm
from sklearn import metrics


features = pd.read_csv('features.csv', index_col='reviewID')
genuine = features[features['label'] == 'N']
fake = features[features['label'] == 'Y']
genuine = train_test_split(genuine, train_size=0.2, test_size=0.0)[0]
sample = genuine.append(fake)
data = sample.loc[:, 'length':'max_rating']
labels = sample['label']
x_train, x_test, y_train, y_test = train_test_split(data,
                                                    labels,
                                                    test_size=0.1)
logisticRegr = LogisticRegression()
logisticRegr.fit(x_train, y_train)
score = logisticRegr.score(x_test, y_test)
print('Logistic Score: ', score)


sgd = SGDClassifier(max_iter=1000)
sgd.fit(x_train, y_train)
score = sgd.score(x_test, y_test)
print('SGD Score: ', score)


clf = svm.SVC()
clf.fit(x_train, y_train)
y_pred = clf.predict(x_test)
print('SVM Score: ', metrics.accuracy_score(y_test, y_pred))
