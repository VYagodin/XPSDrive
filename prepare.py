import os.path
import pandas as pd


def getdir():
    try:
        rootdir = input('Project folder path: ')
        print()
        os.listdir(rootdir)
        return rootdir
    except:
        print('Invalid path')


def get_samples(path: str):
    try:
        samples = []
        listdir = os.listdir(path)
        for d in listdir:
            if os.path.isdir(path + '\\' + d):
                samples.append(d)
        if len(samples) != 0:
            print('Samples: ', ', '.join(samples))
            return samples
        else:
            print('No samples')
            return []
    except:
        print('Something went wrong when obtaining samples')
        return []


def get_files(sample: str):
    try:
        filelist = []
        for d in os.listdir(root + '\\' + sample):
            if os.path.isfile(root + '\\' + sample + '\\' + d) and d[-4:] == '.dat':
                filelist.append(d)
        if len(filelist) != 0:
            print('\n', 'Sample:', sample)
            print('Files: ', ', '.join(filelist) + '\n')
            return filelist
        else:
            print('\n', 'Sample:', sample)
            print('No files')
            return []
    except:
        print('Something went wrong when obtaining files')


def prepare_file(sample, file: str):
    try:
        f = open(root + '\\' + sample + '\\' + file, 'r')
        if f.read(1) == '/':
            f.seek(0, 0)
            x = f.read()
            f.close()
            f = open(root + '\\' + sample + '\\' + file, 'w')
            f.write(x[16:])
            f.close()
            dataframe = pd.read_csv(root + '\\' + sample + '\\' + file, sep='\t', header=None)
            dataframe.drop(columns=[dataframe.columns[2], dataframe.columns[3]], inplace=True)
            if file == 'review_r0.dat':  # prepare review to plot directly
                if not reverse:
                    dataframe = dataframe[::-1]
                dataframe.columns = ['B.E.(eV)', 'Raw Intensity']
                dataframe.to_csv(root + '\\' + sample + '\\' + sample + '_' + 'review' + '.csv',
                                 sep=';', decimal='.', index=False)
            else:
                dataframe.to_csv(root + '\\' + sample + '\\' + file, sep='\t',
                                 decimal='.', index=False, header=False)
            print('File: ', file, ': OK')
    except:
        print('File: ', file, ': FAIL')


setup = open('Settings.dat').readlines()  # setup check
if setup[0][-5:-1] == 'True':
    reverse = True
else:
    reverse = False
decimalsep = setup[1][-2:-1]
if setup[2][-4:] == 'True':
    transpose = True
else:
    transpose = False
postfix = setup[3][23:]

root = getdir()
samples = get_samples(root)
for sample in samples:
    filelist = get_files(sample)
    for file in filelist:
        prepare_file(sample, file)
