# An MDP solver - author Sam Radhakrishnan(@samrk_09)
class MarkovDecisionProcess:
	"""
	States are numbered from 0 to n-1 where n is the number of states
	Actions are also numbered from o to m-1 where m is the number of states
	transition is a 3D array 
		transition[s][a][sprime] returns the probability of ending at a state sprime on taking action a at state s
	reward is a 1D array
		reward[s] stores the reward on reaching state s
	utility stores the utility of every state under a policy p
	"""
	def __init__(self, states, actions, transition, reward, utility, terminal_states, gamma):
		self.states = states
		self.transition = transition
		self.actions = actions
		self.reward = reward
		self.utility = utility
		self.terminal_states = terminal_states
		self.gamma = gamma

	def value_iteration(self):
		max_delta = 10**(-6)
		flag = True
		while flag:
			flag = False
			prev_utility = [x for x in utility]
			for u in range(0, len(utility)):
				if u in terminal_states:
					continue
				utility[u]= (-10**6)
				for a in actions:
					c = 0
					for s in states:
						c += transition[u][a][s] * (reward[u] + self.gamma * prev_utility[s])
					utility[u] = max(utility[u], c)
				if abs(utility[u] - prev_utility[u]) > max_delta:
					flag = True
			#self.print_utility()

	def print_utility(self):
		for u in states:
			print "Utitlty of state " + str(u) + " is :" + str(utility[u])
	
	def print_policy(self, policy):
		for u in states:
			print "Optimal Policy at state " + str(u) + "is :" + str(policy[u])
			
	
	def policy_evaluate(self, policy):
		"""Policy Evaluation
   		"""
   		gamma = self.gamma
		delta = 0
   		while delta < 10**(-6):
   			delta = 0
   			for s in states:
   				if s in terminal_states:
   					continue
   				a = policy[s]
   				v = utility[s]
   				utility[s] = 0
   				for sprime in states:
   					utility[s] += transition[s][a][sprime] * (reward[s] + gamma*utility[sprime])

 				delta = max(delta, abs(v - utility[s]))
 		



	def policy_iteration(self):
		"""
		Start from an arbitary policy
		"""
		policy = [0] * len(states)
		for j in terminal_states:
			policy[j] = -1
		gamma = self.gamma
		flag = True
		while flag:
			self.policy_evaluate(policy)
			flag = False
			prev_policy = [x for x in policy]

			for s in states:
				if s in terminal_states:
					continue
				max_util = 0
				for a in actions:
					curr_util = 0
					for sprime in states:
						curr_util += transition[s][a][sprime] * (reward[s] + gamma * utility[sprime])
					
					if max_util < curr_util:
						max_util = curr_util
						policy[s] = a

				if prev_policy[s] != policy[s]:
					flag = True

		self.print_policy(policy)


"""
Define a simple GridWorld

_____________________
|____|____|____|_+1_|
|____|BBBB|____|_-1_|
|____|____|____|____|

A simple GridWorld where posssible actions are Up(0), Left(1), Right(2), Down(4)

Probability that is an action is taken and that is executed correctly is 0.8. A right angle action is taken is 0.1 each

States start from bottom left and go upto top right

Reward for Goal state is +1 (state 11), for state 7 is -1 and every other state is -0.04.
State 5 is not accessible
"""

states = [x for x in range(0, 12)]
actions = [0,1,2,3]

n = len(states)
m = len(actions)

transition = [0]*n

for i in states:
	#action up
	transition[i] = [0]*m
	for j in range(0, m):
		transition[i][j] = [0]*n

	if i < 8 and i!=1:
		transition[i][0][i+4] = 0.8
	else:
		transition[i][0][i] = 0.8

	if i!=4 and i!=3 and i!=7 and i!=11:
		transition[i][0][i+1] += 0.1
	else:
		transition[i][0][i] += 0.1

	if i!=0 and i!=4 and i!=8 and i!=6:
		transition[i][0][i-1] += 0.1
	else:
		transition[i][0][i] += 0.1

	
	#action left
	if i < 8 and i!=1:
		transition[i][1][i+4] = 0.1
	else:
		transition[i][1][i] = 0.1

	if i!=0 and i!=4 and i!=8 and i!=6:
		transition[i][1][i-1] += 0.8
	else:
		transition[i][1][i] += 0.8
	
	if i > 3 and i!=9:
		transition[i][1][i-4] += 0.1
	else:
		transition[i][1][i] += 0.1

	#action right
	
	if i < 8 and i!=1:
		transition[i][2][i+4] = 0.1
	else:
		transition[i][2][i] = 0.1

	if i!=4 and i!=3 and i!=7 and i!=11:
		transition[i][2][i+1] += 0.8
	else:
		transition[i][2][i] += 0.8
	
	if i > 3 and i!=9:
		transition[i][2][i-4] += 0.1
	else:
		transition[i][2][i] += 0.1

	#action down
	
	if i > 3 and i!=9:
		transition[i][3][i-4] = 0.8
	else:
		transition[i][3][i] = 0.8

	if i!=4 and i!=3 and i!=7 and i!=11:
		transition[i][3][i+1] += 0.1
	else:
		transition[i][3][i] += 0.1

	if i!=0 and i!=4 and i!=8 and i!=6:
		transition[i][3][i-1] += 0.1
	else:
		transition[i][3][i] += 0.1

	#print transition[i]
	#raw_input()

reward = [0] * 12
reward[11] = 1
reward[7] = -1
terminal_states = [11, 7]

utility = [x for x in reward]

mdp = MarkovDecisionProcess(states, actions, transition, reward, utility, terminal_states, 0.9)

mdp.policy_iteration()
#mdp.value_iteration()
#mdp.print_utility()