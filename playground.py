import numpy as np
import turing_machine as tm

input = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])

output = np.array([[0, 2, 0], [2, 0, 2], [0, 2, 0]])

if __name__ == "__main__":

    # number of TMs
<<<<<<< HEAD
    n = 50

    # create n TMs
    alans = [tm.TuringMachine(None, 5, 5, 2) for _ in range(n)]

    # try to solve this for 10000 steps max
    step = 0
    while step < 100000 :
=======
    n = 15

    # number to retain from each population
    n_parents = 5
    add_random = 5

    # parameter
    max_steps = 10000

    step_found = []

    for i in range(20):
>>>>>>> bd38da061d11bf6e8e49c8914846f6952b80d1ce

        # create n TMs
        alans = [tm.TuringMachine(None, 5, 5, 2) for _ in range(n)]

<<<<<<< HEAD
        # run all TMs on the IO pair
        res = [alan.run(input) for alan in alans]

        # calculate all differences between output and prediction
        diffs = [np.sum(np.abs(output.flatten() - r)) for r in res]

        # find index of best TM
        best_idx = np.argmin(diffs)
        alan = alans[best_idx]

        #print("Step {}: Best TM had diff ".format(step), diffs[best_idx])

        # if we found a working TM, stop
        if diffs[best_idx] == 0 :
            print("Found working TM: ")
            print(alan)
            alan.write_to_file("workingTM.p")
            break

        #alans = [alan.procreate() for _ in range(n)]

        step += 1
        if step % 500 == 0 :
            print("Step ", step)

if diffs[best_idx] != 0 :
    print("No working TM could be found")




=======
        # try to solve this for 10000 steps max
        losses = []
        step = 0
        while step < max_steps:
            # print(alans)
            # run all TMs on the IO pair
            res = [alan.run(input) for alan in alans]

            # calculate all differences between output and prediction
            diffs = [np.sum(np.abs(output.flatten() - r)) for r in res]

            # find the x best ones
            best_tm_inds = np.argsort(diffs)[:n_parents]
            best_tms = [
                alans[i] for i in range(len(alans)) if i in best_tm_inds
            ]
            # add completely new members to population to explore
            random_tms = [
                tm.TuringMachine(None, 5, 5, 2) for _ in range(add_random)
            ]
            # mutate the machines
            mutated = [alan.procreate() for alan in best_tms]

            # population are some new members, and the mutated best ones
            population = random_tms + mutated

            # fill population with children
            for i in range(n - n_parents - add_random):
                mom = np.random.randint(n_parents)
                dad = np.random.choice(np.delete(np.arange(n_parents), mom))
                print(mom, dad)
                best_tms[mom].breed(best_tms[dad])
                population.append(best_tms[mom])

            # find index of best TM
            best_idx = np.argmin(diffs)
            alan = alans[best_idx]

            # Loss = mean of population, bc we want the population to improve
            # print("Best TM had diff ", diffs[best_idx])
            # losses.append(diffs[best_idx])
            losses.append(np.mean(diffs))

            # if we found a working TM, stop
            if diffs[best_idx] == 0:
                print("Found working TM: ")
                print(alan)
                alan.write_to_file("workingTM.p")
                # save the step number where it was found
                step_found.append(step)
                break

            # 3 VERSIONS FOR TESTS: mutate, random, population
            # alans = [alan.procreate() for _ in range(n)]
            # alans = [tm.TuringMachine(None, 5, 5, 2) for _ in range(n)]
            alans = population

            step += 1
            if step % 50 == 0:
                print("Step ", step)
                print("Average loss in last 500 steps:", np.mean(losses[-50:]))

print("average step where found: ", np.mean(step_found))
if diffs[best_idx] != 0:
    print("No working TM could be found")
>>>>>>> bd38da061d11bf6e8e49c8914846f6952b80d1ce
