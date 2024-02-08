# ESR Trend Analysis

**ESR Trend Analysis** is used to extract the trend analysis from the weekly SARS-CoV-2 concentrations obtained from The Institute of Environmental Science & Research (ESR) wastewater surveillance programme.

## Metrics and functions:
The following metrics can be obtained from **ESR Trend Analysis**:

 - Basic statistics metrics:
    - Moving average
    - Moving median
    - Moving variance
    - Moving standard deviation
    - Autocorrelation
    - Resampling/confidence interval

  - Advanced metrics:
    - Power spectral density
    - Seasonal trend decomposition
    - Relative strength index
    - Fast Fourier transform
    - Principal component analysis
    - Correlation (e.g., normalized gradient between Covid-19 cases and wasterwater measurements)

Note that this system is not intended to be used to produce predictions.

## Installation:
All the dependancies are included in ``env.yml``, the package can be installed following:
```
conda env create -f env.yml
```
This will create an conda environment called ``trend_analysis``.

## Run:
The trend analysis should be run under the environment ``trend_analysis``
```
conda activate trend_analysis
```

After the environment being loaded, the job can be run:
```
run --workdir /tmp/trend_analysis
    --cfg cfg/cfg.yml
```
where ``--workdir`` is the working directory where holds all the intermediate and final outputs, and ``--cfg`` represents the configuration path.

## Configuration:
An example of the configuration can be found at ``cfg/cfg.yml``, it controls all the task to be run in the system

  ```
  start_datetime: "2022-01-01"
  end_datetime: null

  metrics:
    regions:
      # - nation
      - Auckland
    methods:
      raw: false
      basic:
        enable: false
        window: 24
      psd:
        enable: false
        sampling_frequency: 100
      stl:
        enable: false
        window: 3
      rsi:
        enable: false
        window: 24
      fft:
        enable: false
        fft_cutoff: 0.05
      confidence_interval:
        enable: true
        n_samples: 100
        window: 4

  run_pca: true
  ```









