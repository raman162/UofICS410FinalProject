import sklearn
import classifier

result = classifier.optimize_score(
  min_features=500,
  feature_step=250,
  max_features=500,
  min_estimators=500,
  max_estimators=1000,
  estimator_step=250)
print(result)

