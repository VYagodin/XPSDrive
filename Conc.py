import os.path
import logging as log
import datetime
import re
import pandas as pd


# target work folder
def getdir():
    try:
        rootdir = input('Project folder path: ')
        print()
        os.listdir(rootdir)
        return rootdir
    except:
        print('Invalid path')


# get folders for corresponding samples list
def get_samples(path: str):
    try:
        samples = []
        listdir = os.listdir(path)
        for d in listdir:
            if os.path.isdir(path + '\\' + d):
                samples.append(d)
        if len(samples) != 0:
            print('Samples: ', ', '.join(samples))
            print()
            log.info('Samples: ' + ', '.join(samples) + '\n')
            return samples
        else:
            print('No samples')
            log.info('No samples')
            return []
    except:
        print('Something went wrong when obtaining samples')
        return []


# get files with spectra for sample
def get_files(sample: str):
    try:
        files = []
        filedict = {}
        knownelements = list(csdataframe.index)
        for file in os.listdir(root + '\\' + sample):
            if os.path.isfile(root + '\\' + sample + '\\' + file) and file[-len(postfix)-4:-4] == postfix \
                    and knownelements.__contains__(get_element(file)):
                files.append(file)
        for file in files:
            if csdataframe.index.__contains__(get_element(file)):
                filedict.update({csdataframe.loc[get_element(file), 'Z']: file})
        filelist = list(filedict.keys())
        filelist.sort()
        files.clear()
        for i in filelist:
            files.append(filedict[i])
        if len(files) != 0:
            return files
        else:
            print('No files')
            log.info('No files')
            return []
    except:
        print('Something went wrong when obtaining files')


# get chemical elements list
def get_elements(files: list):
    elementslist = []
    try:
        for file in files:
            if file.find('_') <= 2:
                elementslist.append(get_element(file))
            else:
                pass
        if len(elementslist) != 0:
            print('Elements: ', ', '.join(elementslist))
            log.info('Elements: ' + ', '.join(elementslist))
        else:
            print('No elements')
            log.info('No elements')
        return elementslist
    except:
        print('Something went wrong when obtaining elements')
        return []


# get chemical element from filename
def get_element(file):
    return file[0:int(file.find('_'))]


# load cross-sections dataframe
def get_cross_sections():
    print('Select X-ray gun anode:')
    print('Mg, 1253.6 eV - 0 or any key')
    print('Al, 1486.6 eV - 1')
    sel = input('Anode: ')
    if sel == '1':
        anode = 'Al'
    else:
        anode = 'Mg'
    try:
        csdataframe = pd.read_csv('CS_' + anode + '.csv', delimiter=';')
        csdataframe.index = csdataframe['Element']
        del csdataframe['Element']
        print(anode + ' anode')
        log.info(anode + ' anode')
        print()
        print(csdataframe)
        print()
        return csdataframe
    except:
        print('No cross-section data')
        return pd.DataFrame([], [])


# get specific cross-section
def get_cs(element, state: str):
    try:
        cs = float(csdataframe.loc[element, state[0:5]])
        return cs
        print(cs)
    except:
        print('No cross-section')


# open spectrum file, parce and return prepared dataframe
def parce_spectrum(sample, file: str):
    try:
        cols = re.findall('\S{1,}\s{,1}\S{1,}\s{,20}', open(root + '\\' + sample + '\\' + file, 'r').readline()[:-1])
        widths = []  # take header and count widths to parse it properly
        for i in cols:  # I had to add ugly construction to let user don't deal with adding proper count of spaces
            widths.append(len(i))
        dataframe = pd.read_fwf(root + '\\' + sample + '\\' + file,  widths=widths)
        if 'difference' in dataframe.columns:
            del dataframe['difference']
        for r in range(dataframe.shape[0]):  # convert all to float and NaN to zero
            for c in range(dataframe.shape[1]):
                s1 = str(dataframe.iloc[r, c])
                if s1 != 'nan':
                    dataframe.iloc[r, c] = float(dataframe.iloc[r, c].replace(',', '.'))
        if len(list(dataframe.columns)) == 5 and \
                list(dataframe.columns)[4][0:4] == 'Peak':  # autofill state for 1 peak samples
            dataframe.columns = ['B.E.(eV)', 'Raw Intensity', 'Peak Sum', 'Background', '1s1/2']  # (expected 1s1/2)
        return dataframe
    except:
        return pd.DataFrame([], [])


# find C 1s1/2 peak maximum, calculate charge shift and recalculate binding energies
def get_charge_shift(sample: str):
    try:
        dataframe = parce_spectrum(sample, 'C_r0(xps).dat')
        dataframe.index = dataframe['B.E.(eV)']
        dataframe[dataframe.columns[4]] = pd.to_numeric(dataframe[dataframe.columns[4]])
        return round(float(dataframe[dataframe.columns[4]].idxmax(skipna=True)) - 284.6, 2)
    except:
        return 0


# process spectrum file, find summ of columns (integrate peaks)
def proc_spectrum(sample, file, fn: str):
    try:
        dataframe = parce_spectrum(sample, file)
        summ = 0
        knownstate = list(csdataframe.columns)[2:]
        for peak in list(dataframe)[4:]:  # get peaks with defined electronic states, calculate peak summ
            if knownstate.__contains__(peak[0:5]):
                print('State:', peak[0:5])
                log.info('State:' + peak[0:5])
                colsum = dataframe[peak].sum() - dataframe['Background'].sum()
                cs = get_cs(element, peak[0:5])
                print('Raw intensity:', round(colsum, 2))
                print('Recalculated intensity:', round(colsum / cs, 2), ' cross-section:', str(round(cs, 5)))
                log.info('Raw intensity: ' + str(round(colsum, 2)))
                log.info('Recalculated intensity: ' + str(round(colsum / cs, 2))
                         + ' cross-section: ' + str(round(cs, 5)))
                summ += round(colsum / cs, 2)

        for i in range(len(dataframe['B.E.(eV)'])):  # recalculate binding energy considering charge shift
            dataframe.iloc[i, 0] = dataframe.iloc[i, 0] - chargeshift
        if reverse:
            dataframe = dataframe[::-1]  # reverse and export to file
        dataframe.to_csv(root + '\\' + sample + '\\' + sample + '_' + fn + '.csv',
                         sep=';', index=False)
        return summ
    except:
        return 0


# review.csv need charge shift too
def proc_review(sample):
    if os.path.isfile(root + '\\' + sample + '\\' + sample + '_' + 'review' + '.csv'):
        dataframe = pd.read_csv(root + '\\' + sample + '\\' + sample + '_' + 'review' + '.csv', sep=';')
        for i in range(len(dataframe['B.E.(eV)'])):  # recalculate binding energy considering charge shift
            dataframe.iloc[i, 0] = dataframe.iloc[i, 0] - chargeshift
        dataframe.to_csv(root + '\\' + sample + '\\' + sample + '_' + 'review' + '.csv', sep=';', index=False)


# start obtaining
root = getdir()
log.basicConfig(filename=root+'\\'+'XPS_log.txt', format='%(message)s', filemode='w', level=log.INFO)
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

csdataframe = get_cross_sections()
log.info('Started processing ' + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
print('Started processing ' + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + '\n')
samples = get_samples(root)
pivot = pd.DataFrame(index=csdataframe.index, columns=samples)  # pivot table

for sample in samples:  # process all files in each sample folder
    print('//----------------------------------------------------------------------------')
    log.info('\n' + '//----------------------------------------------------------------------------')
    print('Sample: ', sample)
    log.info('Sample: ' + sample)
    files = get_files(sample)
    elements = get_elements(files)
    chargeshift = get_charge_shift(sample)
    print('Charge shift:', chargeshift, ' eV')
    print()
    log.info('Charge shift: ' + str(chargeshift) + ' eV' + '\n')
    try:
        sampletable = pd.DataFrame(index=elements, columns=[sample])
        for file in files:              # process all spectrum files and add results to table
            element = get_element(file)
            print('Element:', element)
            log.info('Element: ' + element)
            summ = proc_spectrum(sample, file, element)
            sampletable.at[element, sample] = round(summ, 2)
            print('Summ: ', round(summ, 2))
            print('')
            log.info('Summ: ' + str(round(summ, 2)) + '\n')
        proc_review(sample)

        sampletable = sampletable.loc[~(sampletable == 0).all(axis=1)]  # drop all elements with summ=0
        summ = sampletable[sample].sum()  # recalculate to percents and add to pivot table
        print('Relative concentrations in', sample + ':')
        log.info('Relative concentrations in ' + sample + ':')
        for i in range(len(sampletable.index)):
            a = sampletable.at[sampletable.index[i], sample] / summ * 100
            print(sampletable.index[i] + ': ' + (2-len(sampletable.index[i]))*' '
                  + '[' + int(a)*'█' + (100-int(a))*'░' + '] ' + str(round(a, 2)) + ' %')
            log.info(sampletable.index[i] + ': ' + str(round(a, 2)) + ' %')
            pivot.at[sampletable.index[i], sample] = round(a, 2)
        if sampletable.empty:
            print('No concentrations')
            log.info('No concentrations')
        print()
    except:
        pass

pivot.dropna(how='all', inplace=True)
pivot.dropna(axis=1, how='all', inplace=True)
pivot.fillna(0, inplace=True)
print()
if not pivot.empty:
    print('Pivot table:')
    if transpose:
        pivot = pivot.T
    print(pivot)
    pivot.to_csv(root + '\\' + 'Concentrations.csv', sep=';', decimal=decimalsep)
    log.info('\n' + 'Pivot table:')
    log.info(pivot)

log.info('\n' + 'Completed at ' + datetime.datetime.now().strftime("%H:%M:%S"))
print('\n' + 'Completed at ' + datetime.datetime.now().strftime("%H:%M:%S"))
