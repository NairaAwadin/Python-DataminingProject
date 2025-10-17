python --version : python 3.13

libs (imports) :
-numpy
-pandas
-matplotlib
-scikit-learn
-nltk
-fastparquet
-re
-math
-unicodedata
-numbers
-tkinter

files :
3 notebooks :
	+ "k-algorithms.ipynb" -> k-means algo.
	+ "vectorize_dataset_seloger.ipynb" -> clean,vectorize seloger.com dataset + fill some missing values with linear regression models.
	+ "k-means-applied.ipynb" -> apply k-means algo to predict resdential properties prices from scraped seloger.com vectorized dataset.

4 executable files :
	+ 3 files provide functions from 3 notebooks mentioned (model.py,k_means.py,sl_vectorization.py)
	+ 1 file "app.py" execute a terminal interface allow user to get predicted price of a property.
		+ [video display how to use this app.py]
		+ #1) to execute, you first need to create and activate virtual env, in bash terminal type : "source .venv/Scripts/activate"
		+ #2) make sure all imports are satisfied. (look above at libs section)
		+ #3) to run app file, in bash terminal type : "python app.py"
		+ #4) you will be asked to enter model path, models are in folder "models", i provided 2 models (model_sl_[seriesnb].parquet , series number indicate how model is trained, for example K16R10L1500 -> K16 , R10, L1500, K16 is number of centroids (16), R10 is number of runs (10), L1500 is number of training data (1500)), so in terminal, type "models/model_sl_K32R10L4800"
		+ #5) the terminal will the show you list of available types of residential property to predict (i limit the number of type due to small size dataset)
		+ #6) after picking a type, the program will display list of locations (in codepostals) to select.
		+ #7) after selecting a location, you will be asked to enter numerical values in a format [area-terrain-dispo-neuf-chambre-piece-floor-floors], please enter exactly in this format, example : "21.5-0-0-1-2-3-5-6" -> area = 21.5 , surface (terrain) = 0, O not immediately available (dispo mtn), 1 is new (neuf), 2 chambre (bedrooms), 3 pieces, location floor =5, building has 6 floors.

dataset files :
	+ (v_[digits].csv) vectorized datasets (cleaned, vectorized, fillna)
	+ (data_sample_[digits].csv)raw dataset scraped from seloger.com
		+ digits indicate size.

model files : 
	+ .parquet to preserve some datatypes when saving from pandas.DataFrame
