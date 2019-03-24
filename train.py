import pandas as pd
features = pd.read_csv('features.csv', index_col='reviewID')
from sklearn.model_selection import train_test_split
len(features[features['label'] == 'Y'])
genuine = features[features['label'] == 'N']
fake = features[features['label'] == 'Y']
genuine = train_test_split(genuine, train_size=0.2, test_size=0.0)[0]
sample = genuine.append(fake)
data = sample.loc[:, 'length':'max_rating']
labels = sample['label']
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.1)
from sklearn.linear_model import LogisticRegression
logisticRegr = LogisticRegression()
logisticRegr.fit(x_train, y_train)
score = logisticRegr.score(x_test, y_test)
print(score)
from sklearn import svm
clf = svm.SVC(kernel='rbf')
clf.fit(x_train,y_train)
y_pred = clf.predict(x_test)
from sklearn import metrics
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))