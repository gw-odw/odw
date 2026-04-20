# Data Challenge

Challenge activity for the Open Data Workshop course.

Data files may be downloaded from [DCC G2300818](https://dcc.ligo.org/LIGO-G2300818/public) using these links:

* [challenge1.gwf](https://dcc.ligo.org/public/0187/G2300818/001/challenge1.gwf)
* [challenge2.gwf](https://dcc.ligo.org/public/0187/G2300818/001/challenge2.gwf)
* [challenge3.gwf](https://dcc.ligo.org/public/0187/G2300818/001/challenge3.gwf)
* [challenge3_2048hz.gwf](https://dcc.ligo.org/public/0187/G2300818/001/challenge3_2048hz.gwf)   <-- Downsampled version of Challenge 3 file

Workshop participants may [submit solutions via thinkific](https://learn.gwosc.org) as individuals or in teams of up to 3 people.
Check for the deadline date on the Thinkific website.

Challenges are ordered by difficulty. Entries will be rewarded a number of
points that scales with the difficulty of the challenge.

Good luck to all!

## Challenge 1 (1 point) -- Novice

Identify a loud binary black hole signal in white, Gaussian noise.

* Use the data file `challenge1.gwf`. The channel name is `H1:CHALLENGE1`.
* The data are white, Gaussian noise containing a simulated BBH signal.

Instructions:
1. Load the data into memory. What are the sampling rate and duration of the data?
2. Plot the data in the time-domain.
3. Plot a spectrogram (or q-transform) of the data, and try to identify the signal.

Question:
* What is the time of the merger (in seconds from the start of the segment)?

## Challenge 2 (2 points) -- Rookie

Signal in colored, Gaussian noise.

* Use the data file `challenge2.gwf`, with channel name `H1:CHALLENGE2`.
* The data contain a BBH signal with m1 = m2 = 30 solar masses, spin = 0.

Question A:

* What is the approximative time of the merger? (Hint: a plot of the q-transform could help)

Next steps:
1. Generate a time-domain template waveform using approximate `SEOBNRv4_opt`.
   with the same parameters as above. Plot this waveform.
2. Calculate a PSD of the data, and plot this on a log-log scale.
   Use axes ranging from 20 Hz up to the Nyquist frequency.
3. Use the template waveform and PSD to calculate the SNR time series. Plot the SNR time-series.

Question B:

* What is the matched filter SNR of the signal?


## Challenge 3 (4 points) -- Intermediate

* Use the data file `challenge3.gwf` with channel `H1:CHALLENGE3`.
* These are real LIGO data from O2, though we've adjusted the time labels and
  added some simulated signals.
* The data contain a loud simulated signal with m1 = m2 = 10 solar masses.

Questions:
A. What is the merger time of this signal?
B. What is the matched-filter SNR of this signal?

**Note:** it's not needed to use bilby for this challenge.

## Challenge 4 (8 points) -- Advanced

* Use the data file `challenge3.gwf` with channels `H1:CHALLENGE3` and `L1:CHALLENGE3`.
* These are real LIGO data from O2, though we've adjusted the time labels and
  added some simulated signals.
* Any simulated signals have been added to both the H1 and L1 data
* All simulated signals have spin = 0 and m1 = m2, with m1 somewhere in the range 10-50 solar masses

Questions:
A. Identify as many signals as you can. Watch out! These are real data, and so glitches may be
present. Any correct detection is +1 point but any false alarms will count -1 point
against your score. For each signal you find, list:

 * The merger time
 * The SNR
 * Your estimate of the component masses

B. Identify as many glitches as you can. Make a spectrogram of each one.

C. For the earliest event you found, use bilby to compute the posterior distribution for the mass.
   Fix the spin and mass ratio to make this run faster.

### Useful notes

Processing data from a local file with Bilby

```python
sampling_rate = 2048  # needs to be high enough for the signals found in steps above
duration = 8  # needs to be long enough for the signals found in steps above
start_time = 100  # needs to be set so that the segment defined by [start_time,start_time+duration] contains the signal

interferometers = bilby.gw.detector.InterferometerList([])
for ifo_name in ['H1', 'L1']:
    ifo = bilby.gw.detector.get_empty_interferometer(ifo_name)
    ifo.set_strain_data_from_frame_file('challenge3.gwf', sampling_rate, duration, start_time=start_time, channel=f'{ifo_name}:CHALLENGE3')
    interferometers.append(ifo)
```

To load data in google co-lab. Run this code, and then 'restart runtime', and run it again

```python
! pip install -q lalsuite
! pip install -q gwpy
! pip install -q pycbc
# -- Click "restart runtime" in the runtime menu

# -- download data
! wget https://dcc.ligo.org/public/0187/G2300818/001/challenge3.gwf

# -- for gwpy
from gwpy.timeseries import TimeSeries
gwpy_strain = TimeSeries.read('challenge3.gwf', channel="H1:CHALLENGE3")

# -- for pycbc
from pycbc import frame
pycbc_strain = frame.read_frame('challenge3.gwf', 'H1:CHALLENGE3')
```
