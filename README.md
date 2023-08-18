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

 - Power spectral density
 - Seasonal trend decomposition
 - Relative strength index
 - Fast Fourier transform
 - Principal component analysis

Note that this system is not intended to be used to produce predictions.

## Installation:
```
conda env create -f env.yml
```

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
    - nation
    - Auckland
  methods:
    basic:
      enable: true
      window: 20
    psd:
      enable: true
      sampling_frequency: 100
    stl:
      enable: true
      window: 21
    rsi:
      enable: true
      window: 8
    fft:
      enable: true
      fft_cutoff: 0.5

run_pca: true
```



