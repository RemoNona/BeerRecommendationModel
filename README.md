## About the project
This project was persued as part of the Data Science Capstone of the MS Data Science program at University of Denver. 

## Steps
1. Please view requirements.txt - this is the envrionment needed for the Streamlit applicaiton to run. To use the notebooks described below please have Jupyter installed.
2. beerReviews_cleanPrep.ipynb - this notebook is for reference, as it can take about 2 hours to run. The dataframes that it creates are saved as pickle files and are  provided for easy loading into beerReviews_EDA_recModels.ipynb. 

    main.pickle - this file is too large to upload to Github, please follow google drive link for download.
    users.pickle - this file is available in this repository, and also accessible through the google drive link

    They can be downloaded here: https://drive.google.com/drive/folders/108rE14VN_5elSMdcuBXxJmccz8ktoWhl

3. beerReviews_EDA_recModels.ipynb – This notebook walks through the exploratory data analysis and model recommendation algorithms.

4. atts_distributions.html, top10styles.html – interactive graphical outputs
5. Beer_Recommendation_app_prep.ipynb - This notebook further cleans the beer dataset to remove most brewery and beer names that have non-english keyboard characters for use in the Streamlit application
6. BRapp.py - this file is the application. Once you have the requirements installed. Run this command in the terminal:
   ```streamlit run BRapp.py```
