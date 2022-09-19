from IPython.display import Image, display
import copy
import numpy as np

def add_dist_col(df,dog_name):

    # this function will return 5 dogs that are similar with input_dog
    # also return the longest distance from the input dog data point
    df = copy.deepcopy(df)
    dist_list = []
    base = df.loc[dog_name].values
    
    for i in range(df.shape[0]):
        dist_list.append(np.linalg.norm(base - df.iloc[i].values))
    
    df['dist'] = dist_list
    df = df.sort_values(by = 'dist')
    # similarity rate will range from 0 to 1
    df['simliarity_rate'] = 1 - (df['dist'] / df['dist'].values[-1])
    
    return df.head(5)

def euclidean_by_name(df_similiar_dogs):
    name_list = list(df_similiar_dogs.index)
    similarity_list = list(df_similiar_dogs.simliarity_rate)
    for name,s_rate in zip(name_list,similarity_list):
        print(format(s_rate,'.2%'), "simliar to", name)
        display(Image(filename=f'img/{name}.jpg'))