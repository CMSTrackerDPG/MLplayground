#!/bin/bash

cd ..

echo "Start filling DB"
echo "----------------"
echo ""

# To create superuser (if deleting the DB as a first step)
# https://docs.djangoproject.com/en/4.0/ref/django-admin/#django-admin-createsuperuser

# DJANGO_SUPERUSER_USERNAME
# DJANGO_SUPERUSER_EMAIL
# DJANGO_SUPERUSER_PASSWORD
# python manage.py createsuperuser --noinput

# ...
echo "Adding some histograms and corresponding runs"
./manage.py extract_run_histograms /eos/project/c/cmsml4dc/ML_2020/PerRun_UL2018_Data/ZeroBias_315257_UL2018.csv
echo "Histograms added successfully"
echo ""

# ...
echo "Adding some histograms and corresponding lumisections"
echo "Histograms added succesfully"
echo ""

# ...
echo "Adding run certification from Run Registry file"
FILE="/eos/user/x/xcoubez/dqm_playground_shared/data/derived/runs_flags.pkl"
./manage.py extract_run_certifications $FILE
echo "Certification added succesfully"
echo ""

# ...
echo "Adding lumisection certification from Run Registry files"
FILE="/eos/user/x/xcoubez/dqm_playground_shared/data/derived/lumisections_flags.pkl"
./manage.py extract_lumisections_certifications $FILE
echo "Certification added succesfully"
echo ""

# ...
echo "Adding run information from Run Registry"
echo ""

# ...
echo "Adding lumisection information from Run Registry?"
echo ""

# ...
echo "Adding lumisection information from OMS file"
FILE="/eos/user/x/xcoubez/dqm_playground_shared/data/secondary/ZeroBias_rate_perLS_from_OMS_2018.pkl"
./manage.py extract_oms_lumisection_information_from_file $FILE
echo "OMS information added succesfully"
echo ""
