import pandas as pd


def combine_dfs(c_path, s_path, l_path):
    c = pd.read_csv(open(c_path))
    c.columns= ['0', 'a', 'c']
    s = pd.read_csv(open(s_path))
    s.columns = ['0', 'a', 's']
    l = pd.read_csv(open(l_path))
    l.columns = ['0', 'a', 'l']


    cs = pd.merge(c, s, on=['a'], how='inner')

    csl = pd.merge(cs, l, on=['a'], how='inner')

    print(csl.shape[0])
    print(csl.columns)
    print(csl[csl.l.isna()])
    print(csl.head())
    
    csl.to_csv('counts-starts-loc.csv')
    

    


if __name__=='__main__':
    c_path = 'contributor_count.csv'
    s_path = 'star_count.csv'
    l_path = 'loc_count.csv'

    combine_dfs(c_path, s_path, l_path)
    print('done')
