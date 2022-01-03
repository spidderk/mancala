import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Categorical
from mancala import Player

class ActorCriticModel(nn.Module):
    """
    implements both actor and critic in one model
    """
    def __init__(self, inputs, outputs, neurons):
        super(ActorCriticModel, self).__init__()
        self.affine1 = nn.Linear(inputs, neurons)

        # actor's layer
        self.action_head = nn.Linear(neurons, outputs)

        # critic's layer
        self.value_head = nn.Linear(neurons, 1)

        # action & reward buffer
        self.saved_actions = []
        self.rewards = []

    def forward(self, x):
        """
        forward of both actor and critic
        """
        x = F.relu(self.affine1(x))

        # actor: choses action to take from state s_t
        # by returning probability of each action
        action_prob = F.softmax(self.action_head(x), dim=-1)

        # critic: evaluates being in the state s_t
        state_values = self.value_head(x)

        # return values for both actor and critic as a tuple of 2 values:
        # 1. a list with the probability of each action over the action space
        # 2. the value from state s_t
        return action_prob, state_values
        
class ActorCriticPlayer(Player):
    """
    A wrapper around a PyTorch actor-critic model for Kalah
    """

    def __init__(self, pid, model, seed=543):
        Player.__init__(self, pid)
        self.model = model

    def _get_state(self, board):
        board_state = board.get_pits()
        state = np.array(board_state)/(2*board.numpits+2)
        return state

    def select_action(self, state, board):
        state = torch.from_numpy(state).float().unsqueeze(0)
        probs, state_value = self.model(state)
        #print('state_value:', state_value)
        m = Categorical(probs)
        action = m.sample()
        #print("action:", action.item())
#        self.model.saved_actions.append(SavedAction(m.log_prob(action), state_value))
        self.model.saved_actions.append([m.log_prob(action), state_value])
        reward = self.calcreward(action, board)
        #print("reward:", reward)
        self.model.rewards.append(reward)
        return action.item()

    def calcreward(self, a, board):
        pit = a+1
        seeds = board.pits[pit]
        dest = int((pit - seeds) % 14)
        reward = 0
        if seeds == 0: # illegal move pit empty
            reward -= 3
        if seeds == pit: # home, extra move
            reward += 3
        if seeds > pit: # one stone added
            reward += 1
        if (seeds > 0) and (board.pits[dest] == 0) and dest in self.valid_pits:
            reward += board.pits[(dest-7)%14] + 1
        #if self.state[a] & 4: # threatened
        if board.pits[pit] != 0 and board.pits[(14-pit)] == 0: # opposite pit empty
            for ipit in self.invalid_pits:
                if (ipit + pit) != 14: # check all but opposite for CAPTURE
                    iseeds = board.pits[ipit]
                    idest = int((ipit - iseeds) % 14)
                    if idest == (14-pit):
                        reward += board.pits[pit] + 1
                        break
        return reward

    def get_move(self, board):
        state = self._get_state(board)
        return self.select_action(state, board) + 1


