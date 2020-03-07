import numpy as np 
import turing_machine as tm 

input = np.array([[0,1,0],
                  [1,0,1],
                  [0,1,0]])

output = np.array([[0,2,0],
                   [2,0,2],
                   [0,2,0]]) 

if __name__ == "__main__" :

    # number of TMs
    n = 50

    # create n TMs
    alans = [tm.TuringMachine(None, 5, 5, 2) for _ in range(n)]

    # try to solve this for 10000 steps max
    step = 0
    while step < 100000 :

        # run all TMs on the IO pair
        res = [alan.run(input) for alan in alans]

        # calculate all differences between output and prediction
        diffs = [np.sum(np.abs(output.flatten() - r)) for r in res]

        # find index of best TM
        best_idx = np.argmin(diffs)
        alan = alans[best_idx]

        print("Best TM had diff ", diffs[best_idx])

        # if we found a working TM, stop
        if diffs[best_idx] == 0 :
            print("Found working TM: ")
            print(alan)
            alan.write_to_file("workingTM.p")
            break

        alans = [alan.procreate() for _ in range(n)]

        step += 1
        if step % 500 == 0 :
            print("Step ", step)

if diffs[best_idx] != 0 :
    print("No working TM could be found")




