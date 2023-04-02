import ktrain
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1" # use only CPU in prediction

#predictor_load = ktrain.load_predictor('/data/thinhlv/thiennn/deeplearning/TextClassification/bert')

def get_prediction(x):
	return None