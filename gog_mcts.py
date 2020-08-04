# !/usr/bin/env python

from utils import *
from logic import *
import random
import math
import hashlib
import logging
import argparse
import time
import pycosat
from mcts import *
from games import *
import pycosat

# ------------------------------------------------------

NUM_TURNS = 2
RULES_DICT = {'rule_1': 'P implies effect_2',
              'rule_2': 'Q implies effect_3',
              'rule_3': 'R implies effect_4',
              'rule_4': 'S implies effect_5',
              'rule_5': 'T implies effect_6',
              'rule_6': 'U implies effect_7',
              'rule_7': 'V implies effect_8',
              'rule_8': 'W implies effect_9',
              'rule_9': 'X implies effect_10',
              'rule_10': 'Y implies effect_11',
              'rule_11': 'P11 implies effect_12',
              'rule_12': 'Q11 implies effect_13',
              'rule_13': 'R11 implies effect_14',
              'rule_14': 'S11 implies effect_15',
              'rule_15': 'T11 implies effect_16',
              'rule_16': 'U11 implies effect_17',
              'rule_17': 'V11 implies effect_18',
              'rule_18': 'W11 implies effect_19',
              'rule_19': 'X11 implies effect_20',
              'rule_20': 'Y11 implies effect_21',
              'rule_21': 'Z11 implies effect_22',
              'rule_22': 'A1 implies effect_23',
              'rule_23': 'A2 implies effect_24',
              'rule_24': 'A3 implies effect_25',
              'rule_25': 'A4 implies effect_26',
              'rule_26': 'A5 implies effect_27',
              'rule_27': 'A6 implies effect_28',
              'rule_28': 'A7 implies effect_29',
              'rule_29': 'A8 implies effect_30',
              'rule_30': 'A9 implies effect_31',
              'rule_31': 'A10 implies effect_32',
              'rule_32': 'A11 implies effect_33',
              'rule_33': 'A12 implies effect_34',
              'rule_34': 'A13 implies effect_35',
              'rule_35': 'A14 implies effect_36',
              'rule_36': 'A15 implies effect_37',
              'rule_37': 'A16 implies effect_38',
              'rule_38': 'A17 implies effect_39',
              'rule_39': 'A18 implies effect_40'}

ACTION_EFFECT_HASHTABLE = {'effect_1': 1, 'effect_2': 2, 'effect_3': -2, 'effect_4': 4, 'effect_5': -4, 'effect_6': 6,
                           'effect_7': -6, 'effect_8': 8, 'effect_9': -8, 'effect_10': 10,
                           'effect_11': -10, 'effect_12': 12, 'effect_13': -12, 'effect_14': 14, 'effect_15': -14,
                           'effect_16': 16, 'effect_17': -16, 'effect_18': 18, 'effect_19': -18, 'effect_20': 20,
                           'effect_21': -20, 'effect_22': 22,
                           'effect_23': -22, 'effect_24': 24, 'effect_25': -24, 'effect_26': 26, 'effect_27': -26,
                           'effect_28': 28, 'effect_29': -28, 'effect_30': 30, 'effect_31': -30, 'effect_32': 32,
                           'effect_33': -32, 'effect_34': 34, 'effect_35': -34,
                           'effect_36': 36, 'effect_37': -36, 'effect_38': 38, 'effect_39': -38, 'effect_40': 40,
                           'effect_41': -40, 'effect_42': 42, 'effect_43': -42, 'effect_44': 44, 'effect_45': -44,
                           'effect_46': 46, 'effect_47': -46, 'effect_48': 48,
                           'effect_49': -48, 'effect_50': 50, 'effect_51': -50, 'effect_52': 52, 'effect_53': -52,
                           'effect_54': 54, 'effect_55': -54, 'effect_56': 56, 'effect_57': -56, 'effect_58': 58,
                           'effect_59': -58, 'effect_60': 60, 'effect_61': -60}


# ------------------------------------------------------

def pl_resolution(KB, alpha):
    """Propositional-logic resolution: say if alpha follows from KB. [Figure 7.12]"""
    clauses = KB.clauses + conjuncts(to_cnf(~alpha))
    #print(clauses)
    new = set()
    while True:
        n = len(clauses)
        pairs = [(clauses[i], clauses[j])
                 for i in range(n) for j in range(i + 1, n)]
        for (ci, cj) in pairs:
            resolvents = pl_resolve(ci, cj)
            if False in resolvents:
                return True
            new = new.union(set(resolvents))
        if new.issubset(set(clauses)):
            return False
        for c in new:
            if c not in clauses:
                clauses.append(c)


# ------------------------------------------------------

class AntasState():

    def __init__(self, value=0, current=[0] * 2 * NUM_TURNS,current_state={'P': True, 'Q': False, 'R': True, 'S': False,'T': True, 'U': False, 'V': True, 'W': False,'X': True,'Y': False}, turn=0):
                                                                          #'P11': True, 'Q11': False, 'R11': True, 'S11': False,'T11': True, 'U11': False, 'V11': True, 'W11': False,'X11': True,'Y11': False,'Z11': True}, turn=0):
                                                                           # 'A11': False, 'A12': True,'A13': False, 'A14': True

                                                                           #'A15': True, 'A16': False, 'A17': True, 'A18': False,'A19': True, 'A20': False, 'A21': True, 'A22': False,'A23': True, 'A24': False, 'A25': True, 'A26': False,'A27': True, 'A28': False, 'A29': True, 'A30': False
        self.value = value
        self.current = current
        self.turn = turn
        self.num_moves = (9 - self.turn) * (9 - self.turn - 1)
        self.current_state = current_state

    def adverary_actions(self, current_state):
        result = random.randint(1, 10)
        if result < 3:
            selection = random.choice(list(current_state.keys()))
            current_state[selection] = False

        return None

    def available_actions(self, current_state):
        '''determines which actions are available or fire able in a given state
                returns a a list of available moves in a given state'''
        current_state_KB = PropKB()

        expr_list = []

        #--------------------populate KB using state vars---------------------

        for item, value in current_state.items():
            #print(current_state)

            result = Expr(item)

            if value == True:
                expr_list.append(result)
            else:
                expr_list.append(~result)

        for item in expr_list:
            current_state_KB.tell(item)

        # --------------------------------------------------------------------

        effect_list = []
        actions_list = []

        for effect, value in RULES_DICT.items():
            tempval = value.split(' implies ')

            condition_tobe_tested = tempval[0]

            condition_tobe_tested_exp = Expr(condition_tobe_tested)

            result = pl_resolution(current_state_KB, condition_tobe_tested_exp)  # SAT SOLVER to see if the current state entails the KB

            if result == True:
                effect_list.append(tempval[1])

        # print(effect_list)

        for item in effect_list:
            actions_list.append(ACTION_EFFECT_HASHTABLE[item])

        # return list(self.succs.get(state, {}).keys()) #given a state X, get the available actions(keys of the dict)
        #print(actions_list)

        '''the decision which actions are avialable depends on condition action rules and the state. 
        So both P and Q are already true there are no actions available (which we are checking below'''
        i = 0

        while i < len(actions_list):
            item = actions_list[i]
            if -item in actions_list:
                actions_list.remove(item)
                actions_list.remove(-item)
                i = 0
            else:
                i = i + 1
        print("fireable actions:")
        print(actions_list)

        return actions_list

    def state_update_operator(self, last_action, current_state):

        count = 1
        last_action_str = ''
        for item, value in current_state.items():
            if count == last_action:
                last_action_str = item

            count = count + 1

        expr_str = ''

        # --------------------populate KB using state vars---------------------

        for item, value in current_state.items():

            if value == True:
                expr_str = expr_str + item + ','
            else:
                expr_str = expr_str + '~' + item + ','

        expr_str = expr_str[:-1]

        expr_str = '[' + expr_str + ']'

        # randomly popular the knowledge base, generate using function

        #myKB = self.knowledgebase.clauses

        #effect = '[' + last_action_str + ']'

        #message2 = {"effect": str([effect]),
        #            "KB": str(myKB),
        #            "current_state": expr_str
        #            }
        '''#HERE IF THE CURRENT STATE IS P,Q AND RULE SAYS R--> ~P|~Q THEN 
        #WE GET [R,Q] AND [R,P] AS NEW STATE WHICH ARE MAX SAT SETS'''

        #result_API = (maxSat_APICALL([message2]))
        '''

        if result_API['message'] == 'OK':
            try:
                result = result_API['newStates'][0]
            except:
                print(result_API)

            #convert into desired format   #{'P': True, 'Q': True}

            result = result[:-1]
            result = result[1:]
            result = result.split(',')

            result_dict = {}

            for item in result:
                if item is None:
                    continue
                if item[0] =='~':
                    result_dict[item[1]] = False
                else:
                    result_dict[item] = True
        '''

        result_dict = current_state

        if last_action_str != '':
            result_dict[last_action_str] = True

        print("new state:" + str(result_dict))

        return result_dict


    def next_state(self):
        availableActions = self.available_actions(self.current_state)
        # availableActions = [x for x in range(1, 9)]  # generate some available actions by calling available_actions function

        for c in self.current:
            if c in availableActions:
                availableActions.remove(c)

        #-------- bussines make moves-----------

        if len(availableActions) > 0:
            player1action = random.choice(availableActions)  # step 3 of those available actions select an action based on the evaluation function
            print(player1action)
            availableActions.remove(player1action)


            self.current_state = self.state_update_operator(player1action, self.current_state)

        nextcurrent = self.current[:]

        #--------  adverary action----------------
        self.adverary_actions(self.current_state)

        '''legacy code'''

        '''nextcurrent[self.turn] = player1action
        player2action = random.choice(
            availableActions)  # step 3 of those available actions select an action based on the evaluation function
        availableActions.remove(player2action)

        nextcurrent[self.turn + NUM_TURNS] = -player2action'''


        next = AntasState(current=nextcurrent, current_state=self.current_state,
                          turn=self.turn + 1)  

        return next

    def terminal(self):
        from decimal import Decimal, ROUND_HALF_EVEN
        from decimal import Decimal

        #if len(self.available_actions(self.current_state))<1:
        #    return True
        #print("------------------")
        #print(NUM_TURNS)
        #print(self.turn)
        #print(self.turn == NUM_TURNS)
        if self.turn == NUM_TURNS:
            #print(self.current_state)
            return True
        return False

    def reward(self):

        reward = 0
        for item, value in self.current_state.items():
            if value == True:
                reward = reward + 1

        reward = reward / len(self.current_state)

        return reward

    def __hash__(self):
        return int(hashlib.md5(str(self.current).encode('utf-8')).hexdigest(), 16)

    def __eq__(self, other):
        if hash(self) == hash(other):
            return True
        return False

    def __repr__(self):
        s = "CurrentState: %s; turn %d" % (self.current, self.turn)
        return s


if __name__ == "__main__":
    #parser = argparse.ArgumentParser(description='MCTS research code')
    #parser.add_argument('--num_sims', action="store", required=True, type=int,
    #                    help="Number of simulations to run, should be more than 114*113")
    #args = parser.parse_args()

    num_sims = 4

    start_time = time.time()

    current_node = Node(AntasState())
    for l in range(NUM_TURNS):
        current_node = UCTSEARCH(num_sims / (l + 1), current_node)

        print("level %d" % l)
        print("Num Children: %d" % len(current_node.children))
        for i, c in enumerate(current_node.children):
            print(i, c)
        print("Best Child: %s" % current_node.state)
        #print("--------------------------------")


    print("--- %s seconds ---" % (time.time() - start_time))
