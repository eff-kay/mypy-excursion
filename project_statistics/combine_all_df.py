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
    

def print_markdown(file):
    df = pd.read_csv(open(file))
    df = df[['a' ,'c','s','l']]
    df.columns = ['projects', 'contributors', 'stars', 'loc']
    il = pd.read_csv(open('il_links.csv'))
    il = il[['owner', 'project name', 'clone_links']]
    il['projects'] = il['owner']+'-'+il['project name']

    c = pd.merge(df, il, on=['projects'], how='left')
    c = c.drop_duplicates(subset=['clone_links'])
    c = c.reset_index()
    c = c[['clone_links', 'contributors', 'stars', 'loc']]
    print(c.to_markdown())

if __name__=='__main__':
    c_path = 'contributor_count.csv'
    s_path = 'star_count.csv'
    l_path = 'loc_count.csv'

    file = 'counts-starts-loc.csv'
    #combine_dfs(c_path, s_path, l_path)
    print_markdown(file)
    print('done')
