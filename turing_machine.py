import numpy as np
import pickle


class TuringMachine:

    def __init__(self, other, num_states, alphabet_size, mutation_rate):
        """
        TuringMachine Constructor
        Filling the delta function with random values, choosing end states randomly

        tm = a TM for copying. Set to None if you want to create a random TM
        num_states = the number of states of the finite automaton
        alphabet_size = the number of additional symbols (in addition to the number of unique colours in the matrix)
        mutation_rate = how many entries of the delta function to change in each mutation
        """

        if other is None:
            # setting up read/write head
            self.head = 0

            # setting up delta function
            self.alphabet = alphabet_size
            self.delta = np.random.rand(
                num_states, self.alphabet, 3
            )  # delta : states x alphabet -> states x alphabet x {L,N,R}
            self.delta[:, :, 0] = np.floor(
                self.delta[:, :, 0] * num_states
            )  # generating outputs in range of states, for new state
            self.delta[:, :, 1] = np.floor(
                self.delta[:, :, 1] * self.alphabet
            )  # outputs in range of new symbol
            self.delta[:, :, 2] = np.floor(
                self.delta[:, :, 2] * 3
            ) - 1  # outputs in range [-1,0,1]

            self.delta = self.delta.astype(np.int32)

            # setting up end states, choosing 3 end states randomly
            self.end_states = np.unique(
                np.random.choice(np.arange(1, num_states), 3)
            )

            # setting current state to start state
            self.state = 0
            self.num_states = num_states
            self.mutation_rate = mutation_rate

        # end of random creation, beginning of copy constructor
        else:
            self.delta = other.delta
            self.mutation_rate = other.mutation_rate
            self.num_states = other.num_states
            self.end_states = other.end_states
            self.alphabet = other.alphabet

            # init stuff
            self.state = 0
            self.head = 0

    def reset(self):
        """
        Resets this Turing Machine to a blank state
        """
        self.head = 0
        self.state = 0
        self.band = None

    def read_from_array(self):
        pass

    def write_to_file(self, filename):
        pickle.dump(self, open(filename, "wb"))

    def read_from_file(self, filename):
        self = pickle.load(open(filename, "rb"))

    def write_to_array(self):
        pass

    def _step(self):
        """
        Performing one step of the TM: reading band, calling delta function, updating band and state
        """

        # read current symbol
        current_symbol = int(self.band[self.head])

        # call delta function
        self.state, new_symbol, new_move = self.delta[self.state,
                                                      current_symbol, :]

        # update band
        self.band[self.head] = new_symbol
        self.head = (self.head + new_move) % len(self.band)

    def run(self, matrix):
        """
        Running the TM: while no end state is reached, perform a step. Return band in the end.
        """
        # set limit parameters
        limit = 100
        step = 0

        # setup band
        self.band = matrix.flatten().astype(np.int32)

        # stop if end state is reached, keep going otherwise
        while step < limit and not self.state in self.end_states:
            self._step()
            step += 1

        return self.band

    def procreate(self):
        """
        Creates a child of this TM: a mutated version of itself
        """
        alan = TuringMachine(self, 0, 0, 0)
        alan._mutate()
        return alan

    def _mutate(self):
        """
        Mutates this TM itself
        """
        # change mutation_rate many indices of the delta matrix
        for _ in range(self.mutation_rate):

            rval = np.random.rand()
            x = int(np.floor(np.random.rand() * self.num_states))
            y = int(np.floor(np.random.rand() * self.alphabet))

            if rval > 0.66:
                # change one state-transition
                self.delta[x, y, 0] = int(
                    np.floor(np.random.rand() * self.num_states)
                )

            if rval < 0.66 and rval > 0.33:
                # change one write operation
                self.delta[x, y, 1] = int(
                    np.floor(np.random.rand() * self.alphabet)
                )

            if rval < 0.33:
                # change one move-command
                # (since it is so probable that this will be the same, I explicitly forbid the old value here)
                self.delta[x, y, 2] = int(
                    np.random.choice(
                        np.setdiff1d(
                            np.array([-1, 0, 1]),
                            np.array(self.delta[x, y, 2])
                        )
                    )
                )

    def breed(self, other):
        rands = np.random.rand(*self.delta.shape)
        breeding_inds = rands > 0.5
        self.delta[breeding_inds] = other.delta[breeding_inds]

    ### utility functions ###

    def __str__(self):
        return "Delta: " + str(self.delta)

    @staticmethod
    def _count_unique_colours(matrix):
        """
        Count the colours in the input matrix
        """
        return len(np.unique(matrix))
