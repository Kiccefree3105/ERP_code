import pandas as pd
import pickle

with open('lhs_exps_dict.pkl', 'rb') as f:
    lhs_exps_dict = pickle.load(f)

df = pd.DataFrame(lhs_exps_dict)
df.to_csv('lhs_exps.csv')

#import pandas as pd
#df=pd.read_csv('features_Manchester.csv').dropna(axis=0, how='all').reset_index(drop=True)
#df.to_csv('features_Manchester_JJ.csv', index=False)
#with open('features_Manchester.pkl', 'wb') as f:
#    pickle.dump(df.to_dict(orient='records'), f)