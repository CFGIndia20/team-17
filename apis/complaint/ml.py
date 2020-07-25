import pickle
from sklearn.linear_model import SGDClassifier

with open('../../saved_models/sdg.pkl', 'rb') as fid:
    sgd = pickle.load(fid)

def predict(x_test):
    """
    Array of strings : Description of the location / problem
    returns the list of predicted categories
    """
    global sgd
    return sgd.predict(x_test)

### Just for testing ####
# TODO: Delete before production
if __name__ == "__main__":
    print(
        predict(
            [
                "Jogeshwari east subhash road ,\
                there is no road as we can see only potholes\
                every where on subhash road"
            ]
        )
    )
