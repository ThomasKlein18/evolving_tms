class TM2dim:

    def __init__(self, num_states, alphabet_size):

        # setting up read/write head
        self.head_x = 0
        self.head_y = 0

        # setting up delta function
        self.alphabet = alphabet_size
        self.delta = np.random.rand(
            num_states, self.alphabet, 4
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
        self.delta[:, :, 3] = np.floor(
            self.delta[:, :, 3] * 3
        ) - 1  # outputs in range [-1,0,1]
        print(self.delta.shape)

        self.delta = self.delta.astype(np.int32)

        # setting up end states, choosing 3 end states randomly
        self.end_states = np.unique(
            np.random.choice(np.arange(1, num_states), 1)
        )

        # setting current state to start state
        self.state = 0
        self.num_states = num_states

    def _step(self):
        """
        Performing one step of the TM: reading band, calling delta function, updating band and state
        """

        # read current symbol
        current_symbol = int(self.band[self.head_x, self.head_y])

        # call delta function
        self.state, new_symbol, move_x, move_y = self.delta[self.state,
                                                            current_symbol, :]

        # if new_symbol == int(self.groundtruth[self.head_x, self.head_y]):
        #  self.fix[self.state, current_symbol] = self.delta[self.state, current_symbol]

        # update band
        self.band[self.head_x, self.head_y] = new_symbol
        self.head_x = (self.head_x + move_x) % len(self.band)
        self.head_y = (self.head_y + move_y) % len(self.band[0])

    def run(self, matrix):
        """
        Running the TM: while no end state is reached, perform a step. Return band in the end.
        """
        # set limit parameters
        limit = 1000
        step = 0

        # setup band
        self.band = matrix.copy()  # .flatten().astype(np.int32)
        # self.groundtruth = outp
        # self.fix = np.zeros(self.delta.shape).astype(int)
        # alphabet_mapping = np.unique(outp)
        # actual_alphabet_size = len(alphabet_mapping)

        # stop if end state is reached, keep going otherwise
        while step < limit and not self.state in self.end_states:
            self._step()
            step += 1

        return self.band