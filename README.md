# Submission-Analisis-Data
Tugas Submission Data analisis, dengan menggunakan dataset Bike Sharing 2011-2012

#  Setup Environment - Anaconda
conda create --name submission python=3.9
conda activate submission
pip install -r requirements.txt

# Setup Environment - Shell/Terminal
mkdir submission
cd submission
pipenv install
pipenv shell
pip install -r requirements.txt

# Run steamlit app
streamlit run dashboard.py
