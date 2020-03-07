import numpy as np 
import pickle
import turing_machine as tm


if __name__ == "__main__" :

    turing = pickle.load(open("workingTM.p", "rb"))
    res = turing.run()

    print(res)
