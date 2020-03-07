import numpy as np 
import pickle
import turing_machine as tm


if __name__ == "__main__" :

    turing = pickle.load(open("workingTM.p", "rb"))

    input = np.array([[0,1,0],[1,0,1],[0,1,0]]).flatten()
    turing.reset()
    res = turing.run(input)
    print(res)

    input = np.array([[0,3,0],[3,0,3],[0,3,0]]).flatten()
    turing.reset()
    res2 = turing.run(input)
    print(res2)
