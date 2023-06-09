# -*- coding: utf-8 -*-
"""fifa_2018_world_cup_statistics_to_be_completed.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/gist/NancyBett/868a10a65a979440ccaa36363b98a711/fifa_2018_world_cup_statistics_to_be_completed.ipynb

This project is about an interpretable machine learning application for Global Explanations. The underpinning algorithmic approach is **Permutation Importance**. Please do complete the majority of the tasks below.
"""

import numpy as np
import pandas as pd

"""**Note:** Please make sure you have uploaded the Excel file with the data ("Files" icon on your right), if you are working within the Google's Colab environment, or into the folder being prompted when the Anaconda PowerShell Prompt has been launched. **For instance: (base) PS C:\Users\ek21aab>**"""

data = pd.read_csv('/FIFA 2018 Statistics.csv')
y = (data['Man of the Match'] == "Yes")  # Convert from string "Yes"/"No" to binary
feature_names = [i for i in data.columns if data[i].dtype in [np.int64]]
X = data[feature_names]

from google.colab import drive
drive.mount('/content/drive')

data.head()

print(feature_names)

from sklearn.model_selection import train_test_split

train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)

from sklearn.tree import DecisionTreeClassifier

tree_model = DecisionTreeClassifier(random_state=0, max_depth=5, 
                                    min_samples_split=5).fit(train_X, train_y)

y_pred = tree_model.predict(val_X)

from sklearn.metrics import confusion_matrix, accuracy_score

cm = confusion_matrix(val_y, y_pred)
print(cm)
accuracy_score(val_y, y_pred)

"""**Task 1:** In the following, try to use **Random Forest Classifier** as a prediction model to be also trained, tested and analysed in its performance in terms of accuracy."""

from sklearn.ensemble import RandomForestClassifier

forest_model=RandomForestClassifier(n_estimators=100,random_state=1)

forest_model.fit(train_X, train_y)

y_pred = forest_model.predict(val_X)
cm = confusion_matrix(val_y, y_pred)
print(cm)
accuracy_score(val_y, y_pred)

"""Random Forest classifier gives a better accuracy compared to the  decision tree classifier.

**Note:** In the following, you may need to run the pip installer, **without the exclamation mark in front**, within an Anaconda installation, if you are not using Google's Colab environment.
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install eli5

import eli5

from eli5.sklearn import PermutationImportance

perm = PermutationImportance(tree_model, random_state=1).fit(val_X, val_y)

eli5.show_weights(perm, feature_names = val_X.columns.tolist())

"""**Task 2:** In the following, try to run Permutation Importance for the **Random Forest Classifier** you trained and tested as of the task 1 above."""

perm = PermutationImportance(forest_model, random_state=1).fit(val_X, val_y)
eli5.show_weights(perm, feature_names = val_X.columns.tolist())

"""**Task 3:** Put forward as a text cell any interesting observations form the results of Permulation Importance in the context of both classifiers.

in the Random Forest classifier distance covered has a higher influence.
The yellow card has a positive influence .offsides,corners,goals in PSO,Attempts and passes have a negative influence compared to the Decision tree classifier that had only attempts and passes as a negative weight.

**Note:** In the following, you will need to run the pip installer, **without the exclamation mark in front**, within an Anaconda installation, if you are not using Google's Colab environment.
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install pdpbox

from matplotlib import pyplot as plt
from pdpbox import pdp, get_dataset, info_plots

feature_to_plot = 'Distance Covered (Kms)'

pdp_dist = pdp.pdp_isolate(model=tree_model, dataset=val_X, 
                           model_features=feature_names, 
                           feature=feature_to_plot)

pdp.pdp_plot(pdp_dist, feature_to_plot)
plt.show()

"""**Task 4:** In the following, try to get the partial dependence plot for the same feature "Distance Covered in Kms" and for the Random Forest Classifier. Subsequently, state any significant differences with the Decision Tree Classifier, the first prediction model."""

feature_to_plot = 'Distance Covered (Kms)'
pdp_dist = pdp.pdp_isolate(model=forest_model, dataset=val_X,
                           model_features=feature_names,
                           feature=feature_to_plot)

pdp.pdp_plot(pdp_dist, feature_to_plot)
plt.show()

"""from the random forest classifier one is said to be man of the match when they run between 98 and 112 kms.More than that becomes insignificant.

**Task 5:** In the following task, try to get the partial dependence plot for the feature "Yellow Cards" and for the second model, the Random Forest Classifier. Subsequently, state your intepretation of the plot.
"""

#partial dependence plot for yellow card using Random forest Classifier
feature_to_plot = 'Yellow Card'
pdp_dist = pdp.pdp_isolate(model=forest_model, dataset=val_X,
                           model_features=feature_names,
                           feature=feature_to_plot)

pdp.pdp_plot(pdp_dist, feature_to_plot)
plt.show()

"""From the partial dependence plot,the number of yellow cards has an influence in identifying the man of the match.Lower significance is seen in the first 3 yellow cards and has a higher significance from the 3rd yellow card.

END of the show....
"""

# Commented out IPython magic to ensure Python compatibility.
# %%shell
# jupyter nbconvert --to html / /content/FIFA_2018_World_Cup_Statistics_to_be_completed (4).ipynb
#