
#@title Run this to Import Data and Packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
#%matplotlib inline

def reduce_upper_outliers(df, reduce=0.01, half_width=4):
    length = len(df.iloc[0,:])
    remove = int(length*reduce)
    for i in df.index.values:
        values = df.loc[i,:]
        sorted_values = values.sort_values(ascending = False)
        for j in range(remove):
            idx = sorted_values.index[j]
            new_val = 0
            count = 0
            idx_num = int(idx[5:])
            for k in range(2*half_width+1):
                idx2 = idx_num + k - half_width
                if idx2 < 1 or idx2 >= length or idx_num == idx2:
                    continue
                new_val += values['FLUX-'+str(idx2)]

                count += 1
            new_val /= count # count will always be positive here
            if new_val < values[idx]: # just in case there's a few persistently high adjacent values
                df.set_value(i, idx, new_val)


    return df

def plot_light_curve(dataset, index):
  plt.figure()
  plt.plot(np.array(dataset[index:index+1])[0])
  plt.show()


# original source: https://www.kaggle.com/keplersmachines/kepler-labelled-time-series-data
#!wget -q --show-progress 'https://storage.googleapis.com/inspirit-ai-data-bucket-1/Data/AI%20Scholars/Sessions%206%20-%2010%20(Projects)/Project%20-%20Planet%20Hunters/exoTrain.csv'
#!wget -q --show-progress 'https://storage.googleapis.com/inspirit-ai-data-bucket-1/Data/AI%20Scholars/Sessions%206%20-%2010%20(Projects)/Project%20-%20Planet%20Hunters/exoTest.csv'
trainFile = 'D:\\git\\python\\PlanetFinder\\PlanetFinder\\exoTrain.csv'
testFile = 'D:\\git\\python\\PlanetFinder\\PlanetFinder\\exoTest.csv'
raw_data = np.loadtxt(trainFile, skiprows=1, delimiter=',')
x_train = raw_data[:, 1:]
y_train = raw_data[:, 0, np.newaxis] - 1.
raw_data = np.loadtxt(testFile, skiprows=1, delimiter=',')
x_test = raw_data[:, 1:]
y_test = raw_data[:, 0, np.newaxis] - 1.
del raw_data

# flux_data = pd.read_csv(trainFile, index_col=0)
# print(flux_data)
# flux_data['LABEL'] = flux_data['LABEL'] - 1 # Change the labels to be 1 for exoplanet and 0 for non-exoplanet

# Print the first five rows of the data frame
### YOUR CODE HERE
# flux_data.head()

flux_data = pd.read_csv(trainFile, index_col=False) # Read in the exoplanet training data using Pandas
flux_data['LABEL'] = flux_data['LABEL'] - 1 # Change the labels to be 1 for exoplanet and 0 for non-exoplanet

labels = flux_data['LABEL']
flux_data = flux_data.drop('LABEL', axis=1) # Drop the labels from the data frame, leaving only the flux data

non_exo_data = flux_data.loc[labels==0] # Select only rows with label 0
exo_data = flux_data.loc[labels==1] ### YOUR CODE HERE
print(str(exo_data))
print ("Number of exoplanets:", len(exo_data))
print ("Number of non-exoplanets:", len(non_exo_data))

# To get a sense for what these real light curves look like, use the following function in a loop to plot 5 light curves from the exoplanet category.
for i in range(5):

  print('Exoplanet Light Curve '+ str(i))

  plot_light_curve(exo_data, i)
### END CODE HERE

# do the same thing for the non-exoplanet category!
for i in range(5):

  print('Non-Exoplanet Light Curve '+ str(i))

  plot_light_curve(non_exo_data, i)

# To recognize exoplanets, we need to get comfortable finding the period from a graph!
# Here, we want to try to visualize one period of the exoplanet transit (starting at a dip and ending at a dip). 
# Let's see if we can find the time t_0, the time at which the first transit (dip in plot) starts. Then, we will see if we can find the period length (time from dip to dip), so we can plot one period from start to finish.
# Hint: to begin, set the period to 3197 to first figure out t_0. Then, reset the period.

index = 3 #@param {type:"slider", min:0, max:37, step:1}
t_0 = 230 #@param {type:"slider", min:0, max:3197, step:1}
period = 610 #@param {type:"slider", min:0, max:3197, step:1}

light_curve=np.array(exo_data.loc[index])
plt.plot(light_curve)
plt.title('Box Covering One Period of Exoplanet Transit')
plt.gca().add_patch(Rectangle((t_0, -510), period, 700, linewidth=1,edgecolor='r',facecolor='none'))
plt.show()

plt.plot(light_curve[t_0: t_0+period])
plt.title('Plot of Just One Period')
plt.show()

# Try this for a Non-Exoplanet
# So what happens if we use folding to find a period when there isn't one?
# Below, plot non-exoplanet light curve #25.

index = 25 #@param {type:"slider", min:0, max:5050, step:1}
t_0 = 0 #@param {type:"slider", min:0, max:3197, step:1}
period = 0 #@param {type:"slider", min:0, max:3197, step:1}

light_curve=np.array(non_exo_data.iloc[index])
plt.plot(light_curve)
plt.title('Box Covering One Period of non-Exoplanet')
plt.gca().add_patch(Rectangle((t_0, -510), period, 2050, linewidth=1,edgecolor='r',facecolor='none'))
plt.show()

plt.plot(light_curve[t_0: t_0+period])
plt.title('Plot of Just One Period non-exoplanet')
plt.show()























