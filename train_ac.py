import numpy as np
import torch
import torch.optim as optim
import torch.nn.functional as F

from actorcritic import ActorCriticPlayer
from actorcritic import ActorCriticModel
from board import Board
from randomplayer import RandomPlayer
from greedyplayer import GreedyPlayer
from minimaxplayer import MMPlayer
from player import Player
from collections import namedtuple

results_path = './results/'
#
#if ((os.path.isdir(results_path) or os.path.isfile(results_path)) and not args.force):
#    print(results_path + " already exists. Exiting...")
#    exit(1)
#elif (args.force == True):
#    shutil.rmtree(results_path)
#
#from torch.utils.tensorboard import SummaryWriter
#writer = SummaryWriter(results_path)

bins = 6
neurons = 256
learning_rate = .001
gamma = 0.95
eps = np.finfo(np.float32).eps.item()


SavedAction = namedtuple('SavedAction', ['log_prob', 'value'])
board = Board()

#model = ActorCriticModel(bins*2+2, bins, neurons)
model = torch.load('./results/final_model.pt')

optimizer = optim.Adam(model.parameters(), lr=learning_rate)
p1 = ActorCriticPlayer('P1', model)

def select_action(state):
    state = torch.from_numpy(state).float()
    probs, state_value = model(state)

    # create a categorical distribution over the list of probabilities of actions
    m = Categorical(probs)

    # and sample an action using the distribution
    action = m.sample()

    # save to action buffer
    model.saved_actions.append(SavedAction(m.log_prob(action), state_value))
    reward = self.calcreward(pit-1, board)
    model.reward.append(reward)

    # the action to take
    return action.item()

def finish_episode(epoch):
    """Training code. Calculates actor and critic loss and performs backprop."""
    R = 0
    saved_actions = model.saved_actions
    policy_losses = [] # list to save actor (policy) loss
    value_losses = [] # list to save critic (value) loss
    returns = [] # list to save the true values

    # calculate the true value using rewards returned from the environment
    for r in model.rewards[::-1]:
        # calculate the discounted value
        R = r + gamma * R
        returns.insert(0, R)

    returns_unnormalized = torch.tensor(returns)
    returns = (returns_unnormalized - returns_unnormalized.mean()) / (returns_unnormalized.std() + eps)

    for [log_prob, value], R in zip(saved_actions, returns):
        advantage = R - value.item()

        # calculate actor (policy) loss
        policy_losses.append(-log_prob * advantage)
        
        #print("value:", value)
        #print("R:", torch.tensor([R]))

        # calculate critic (value) loss using L1 smooth loss
        value_losses.append(F.smooth_l1_loss(value, torch.tensor([[R]])))

    # reset gradients
    optimizer.zero_grad()

    # sum up all the values of policy_losses and value_losses
    loss = torch.stack(policy_losses).sum() + torch.stack(value_losses).sum()
    if (epoch+1) % 1000 == 0:
        print(f'Loss, {loss.item():4f}, {epoch}')

    # perform backprop
    loss.backward()
    optimizer.step()

    # reset rewards and action buffer
    del model.rewards[:]
    #print('actions:', len(model.saved_actions))
    del model.saved_actions[:]

def train():
#    results_draws = []
#    results_wins_agent1 = []
    p2 = RandomPlayer('P2')

    solved = False
    last_win_percentage = 0
    for trial in range(50000):
        model.train()

        board.resetBoard()
        #board.train = False
        state = board.get_pits()
        ep_reward = 0
        if (trial % 2) == 1: # P2 goes first every other trial
            board.set_player(1)
        done = board.check_done()
        
        while not done:
            player = board.get_player()
            if player == 0:
                pit = p1.get_move(board)
            else:
                pit = p2.get_move(board)
            legal_move = board.move(pit)
            #print("legal:", legal_move)
            done = board.check_done() or not legal_move
        if not legal_move:
            model.rewards[-1] += -5
        else:
            if (board.pits[7] < board.pits[0]):
                model.rewards[-1] += 25
            elif (board.pits[7] == board.pits[0]):
                model.rewards[-1] += 10
            model.rewards[-1] += (board.pits[0] - board.pits[7]) # reward for win/tie/loss
        finish_episode(trial)

        if trial == 10000:
            p2 = GreedyPlayer('P2')
        if trial == 30000:
            p2 = MMPlayer('P2')
            
        if (trial+1) % 1000 == 0:
            wins = 0
            illegal = 0
            for i in range(100):
                model.eval()
                board.resetBoard()
                #board.train = False
                state = board.get_pits()
                if (i % 2) == 1: # P2 goes first every other trial
                    board.set_player(1)
                done = board.check_done()
                while not done:
                    player = board.get_player()
                    if player == 0:
                        pit = p1.get_move(board)
                    else:
                        pit = p2.get_move(board)
                    legal_move = board.move(pit)
                    #print("legal:", legal_move)
                    done = board.check_done() or not legal_move
                if not legal_move:
                    illegal += 1
                else:
                    if (board.pits[7] < board.pits[0]):
                        wins += 1
                del model.rewards[:]
                del model.saved_actions[:]

            print('wins/100:', wins)
            print('illegal/100:', illegal)

            #ep_reward += reward

#        for _ in range(1, 10000):
#            action = select_action(state)
#
#            state, reward, done, _ = env.step(action)
#
#            if args.render:
#                env.render()
#
#            model.rewards.append(reward)
#            ep_reward += reward
#            if done:
#                break


def main():
    #writeSettings()


    train()
    torch.save(model, results_path + '/final_model.pt')

if __name__ == '__main__':
    main()


