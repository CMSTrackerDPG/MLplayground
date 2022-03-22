# DQM Playground

[![Build Status](https://app.travis-ci.com/XavierAtCERN/MLplayground.svg?branch=master)](https://app.travis-ci.com/XavierAtCERN/MLplayground)

The goal of the DQM Playground is to serve information from various sources (OMS, Run Registry, DQM GUI, static files from the ML4DQM effort) in order to ease model development and to provide a place to compare the predictions of the various models.

## Environmental variables
All must be stored in a file named `.env`:
```python3
DJANGO_DATABASE_ENGINE
DJANGO_DEBUG
DJANGO_DATABASE_NAME
DJANGO_DATABASE_PASSWORD
DJANGO_DATABASE_USER
DJANGO_DATABASE_HOST
DJANGO_DATABASE_PORT
DJANGO_SECRET_KEY
DIR_PATH_EOS_CMSML4DC
 ```

## Behavior
### Histogram File Manager
- Currently, the choices for available files provided are only refreshed once, on server start, meaning that to refresh the list of available DQM files, one has to restart the app

## Management Commands
### `histogram_file_manager`
- `discover_dqm_files`: Will scan `DIR_PATH_EOS_CMSML4DC` for files and check if a `HistogramDataFile` has been stored in the DB for each file.

### `lumisection_histos1D`
- `exctract_lumisections_histos1D_csv`: Given a CSV containing 1D Lumisection Histograms, this command will parse the file's contents and create appropriate entries in the `LumisectionHisto1D` table.

### `lumisection_histos2D`
- `exctract_lumisections_histos2D_csv`: Given a CSV containing 2D Lumisection Histograms, this command will parse the file's contents and create appropriate entries in the `LumisectionHisto2D` table.
