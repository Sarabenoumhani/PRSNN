import pandas as pd
import numpy as np 
import os
import re
import requests
import gzip
import gzip

def parse_23andme(file):
    sep=','
    if(file.find('.tsv')!=-1):
        sep='\t'

    if(file.find('.gz')!=-1):
        lines=gzip.open(file, 'rb').readlines()
    else:
        lines=open(file, 'r').readlines()

    lines_ = list(filter(lambda l: l if not l.startswith('#') else False, lines))
    f=open(file, 'w')
    f.write(''.join(lines_))
    f.close()

    df=pd.read_csv(file, sep=sep)
    if(not 'position' in df.columns):
        df=pd.read_csv(file, sep='\t', header=None)
        df.columns=['rsid','chromosome','position','genotype']

   #return { 'rsids': list(df['rsid']), 'genotype': list(df['genotype']) }
    return df

def parse_ancestry(file):
    sep=','
    if(file.find('.tsv')!=-1):
        sep='\t'

    if(file.find('.gz')!=-1):
        lines=gzip.open(file, 'rb').readlines()
    else:
        lines=open(file, 'r').readlines()

    lines_ = list(filter(lambda l: l if not l.startswith('#') else False, lines))
    f=open(file, 'w')
    f.write(''.join(lines_))
    f.close()

    df=pd.read_csv(file, sep=sep)
    if('allele1' in df.columns):
        df['genotype']=df['allele1']+df['allele2']

    return { 'rsids': list(df['rsid']), 'genotype': list(df['genotype']) }


def crawl_opensnps():
    # create the folder to store the data later
    folder='./data_opensnps/'
    if(not os.path.isdir(folder)):
        os.system('mkdir '+folder)

    f=open('list_opensnp.tsv','w')
    f.write('file\ttype\n')
    try:
        current='1'
        while(current!=None):
            content = requests.get('https://opensnp.org/genotypes?direction=asc&page='+current+'&sort=filetype')
            lines=content.text.split('\n')
            for l in lines:
                if(l.find('../data')!=-1):
                    ref=l.split('../data/')[1].split('>')[0].replace('"','')
                    type_=ref.split('.')[1]
                    f.write('https://opensnp.org/data/'+ref+'\t'+type_+'\n')

                if(l.find('page=')!=-1):
                    links=re.findall(r'(page=\S+)', l)
                    ok=False
                    for l in links:
                        newpage=l.split('page=')[1].split('&')[0]
                        if( int(newpage) > int(current) ):
                            current=newpage
                            ok=True

                    if(not ok):
                        current=None
    except:
        pass
    f.close()

def _test_extension(lines):
    linetest=None
    for l in lines:
        if( not l.startswith('#') ):
            linetest=l
            break
    ext=None
    if(linetest!=None):
        if( len(linetest.split(',')) > 1):
            ext='csv'
        elif( len(linetest.split('\t')) > 1):
            ext='tsv'
        elif( lines[0].lower().find('vcf')!=-1):
            ext='vcf'

    return ext


def Data_quality(df):
    df = df.drop_duplicates()
    df = df.dropna()  #Remove rows with any missing values
    df = df.reset_index(drop=True) # Reset index
    Data = pd.DataFrame(columns=['rsid','genotype','effect weight','P','Case of disease']) # before this step open the file to know the features

    Data['rsid']=df["SNPID"]
    Data['genotype']=df['Allele1']+df['Allele2']
    Data['P']=df['P.value']
    Data['effect weight'] = df['Effect'] 
    Data['Case of disease'] = np.where(df['P.value']<0.005, 1, 0)
    #Data.to_csv('Trainingpanicdisorderbeforeshapvalues.csv', index=False) save the data as csv file
    return Data 
