This is the script for X-ray photoelectron spectroscopy data processing
working together with the XPSPEAK41 program.
The script builds table of the relative concentration of chemical elements.

the procedure for working with the program is as follows:
1. At first, you have to prepare your data properly for successfull processing.
1.1 Please, create root directory for the experiment. Then, create subdirectories
for each experimental sample. Other files in root directory and directories in 
subdirectories will be ignored.
1.2 Every sample dir contains steaming raw data just from the spectrometer, 
the main ones is raw spectra ASCII files for each chemical element.
Please, name spectra files for each chemical element in standard form: 
(element)_(additional information).* (.dat or .txt or smth else) 
e.g. C_r0.dat, O_r0.dat, Au_r0.dat (This is an example for my spectrometer 
program, the minimal filename is C_.dat, O_.dat, Pt_.dat etc.). 
Review spectra file should have name "review.dat" (or review.txt).
1.3 In case of multiple element spectra files occurence (for example, different
spectrometer settings for the same element), create new sample folder put 
the new file there and copy the rest element files.
1.4 Prepare files for manual processing in XPSPEAK41 program, they should contain
only two columns, energy and intensity, no header, decimal separator is ".".
You can use "Prepare raw data files" option.

2. Now you process your spectra in XPSPEAK41, set background, approximate peaks, etc.
2.1 When you processed your spectrum in XPSPEAK41, export it to the same folder, where
source spectrum file is stored. Add postfix (xps) to the filename (you can set your 
own postfix in settings.dat). 
You should get filename "(element)_(additional information)(xps).dat" to specify 
unambiguously which file to process, e.g. C_r0(xps).dat
2.2 Now open this file and mark essential peaks in header with corresponding electronic state.
Replace standart markup "Peak 1, Peak 2...Peak N" with states e.g. "1s1/2", "2p3/2" etc.
If standart "Peak N" is not replaced with electronic state, the peak is considered as 
inessential - ghost peak, satellite peak, shake-up peak, auger peak, peak from another 
element, etc, and not used in calculations.
2.3 If there is only one peak and it left non marked-up "Peak 1" it will be concidered 
to be 1s1/2 state, so elements like C, O, B, Li, etc can be just left alone, 
except there are two or more chemical states with plenty of 1s1/2 peaks. 
In this case, mark-up is necessary.
2.4 Important! Please, when processing carbon spectra, use first peak (Peak 0 in XPSPEAK41) 
as main 1s peak in case of several chemical states to let the script find charge shift correctly.

3. When all files are processed and all states are marked, start the script and select 
"calculate relative concentrations" option. All you have to do is just specify root folder 
of experiment, where sample folders are stored.
3.1 The program will export log file and concentrations.csv file with pivot table 
in root folder, and prepare *.csv files with spectra, background, peaks, 
peak summ to plot them in Origin Pro, Grapher, and other programs. 
The files stored in sample folders and have standart form "(sample)_(element).csv". 
You can set decimal separator for numbers which you prefer, reverse binding energies 
(0...1000 or 1000...0) or not and transpose concentrations pivot table or not in settings.dat.

4. Also, you can use tiny, but powerful auger parameter calculator.
