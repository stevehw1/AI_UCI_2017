# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent

class MyAI ( Agent ):

	def __init__ ( self ):
	# ======================================================================
	# YOUR CODE BEGINS
	# ======================================================================
		self.imGAY = 0;
		self.first_turn = True
		self.have_gold = False;
		self.traverse = True
		self.path_back = None;
		self.have_arrow = True;
		self.wumpus_is_alive = True;
		self.wumpus_location = None;
		self.attack_wumpus = False;
		self.shoot_wumpus = False;
		self.current_location = (1,1); #(x, y)
		self.unvisited = dict(); #key=location value is val bw 0 and 100. Higher = more likely to die.
		self.visited = list();#list of visited places
		self.is_safe = dict();#key will be a location and val will be a tuple of bools (stench, breeze)
		self.known_safe = list();
		self.known_wumpus_or_pits = dict(); #key = location val = bools(wumpus, pit)
		self.facing = Direction.right;
		self.true_width = False;
		self.true_height = False;
		self.board_width = 900;
		self.board_height = 900;
		self.travel_to = None; #should only be an adjacent node. This will be used in "look_dat_way_boi" function to help the character turn and go forward
		self.travel_path = dict();
		self.edges = {(1,1): [(1,2), (2,1)]};

	def find_way_back(self)-> {"dict of moves to get back, key = current_location and val is move to go"}:
		# print("why god")
		# print("Current Location: ", self.current_location)
		# print("self.visited: ", self.visited)
		# print("Self.unvisited: ", self.unvisited)
		# print("Edge Graph: ")
		# for edge in self.edges:
		# 	print("\t", edge, ": ", self.edges[edge])
		if self.path_back != None:
			self.path_back.clear();
		explored = [];
		current_location = self.current_location
		queue = [current_location]
		the_path = list();
		path_dict = dict();
		adjacent_tiles = [(1+1, 1),
							(1-1, 1),
							(1, 1+1),
							(1, 1-1)];
		# if current_location == self.travel_to:
			# if current_location in self.unvisited:
			# 	del self.unvisited[current_location]
			# # self.travel_to = None;
			# self.leastRiskyNode()

		while len(queue) != 0:
			popped = queue.pop(0);
			for child in self.edges[popped]:
				if child not in explored:
					queue.append(child)
			explored.append(popped)
			if popped in adjacent_tiles:
				explored.append((1,1))
				break;
		# print("Explored: ", explored)
		from_index = len(explored) -1
		to_index = from_index - 1;
		from_n = explored[from_index]
		to_n = explored[to_index]

		while (to_n != (1,1)):
			if from_n == (1,1):
				path_dict[to_n] = (1,1)
				from_index = to_index;
				to_index -= 1;
				from_n = explored[from_index]
				to_n = explored[to_index]
			elif from_n in self.edges[to_n]:
				path_dict[to_n] = from_n
				from_index = to_index;
				to_index -= 1;
				from_n = explored[from_index]
				to_n = explored[to_index]
				# if to_n == self.current_location:
				# 	path_dict[to_n] = from_n
				# 	break
			else:
				to_index -= 1
				to_n = explored[to_index]

		self.path_back = path_dict

	def find_path(self):
		if self.travel_path != None:
			self.travel_path.clear();
		explored = [];
		current_location = self.current_location
		queue = [current_location]
		the_path = list();
		path_dict = dict();
		adjacent_tiles = [(self.travel_to[0]+1, self.travel_to[1]),
							(self.travel_to[0]-1, self.travel_to[1]),
							(self.travel_to[0], self.travel_to[1]+1),
							(self.travel_to[0], self.travel_to[1]-1)];
		if self.current_location in adjacent_tiles:
			path_dict[self.current_location] = self.travel_to

		while len(queue) != 0:
			for child in self.edges[queue[0]]:
				if child not in explored:
					queue.append(child)
			popped = queue.pop(0);
			explored.append(popped)
			if popped in adjacent_tiles:
				explored.append(self.travel_to)
				break;
		from_index = len(explored) -1
		to_index = from_index - 1;
		from_n = explored[from_index]
		to_n = explored[to_index]

		while (to_n != self.travel_to):
			if from_n == self.travel_to:
				path_dict[to_n] = self.travel_to
				from_index = to_index;
				to_index -= 1;
				from_n = explored[from_index]
				to_n = explored[to_index]
			elif from_n in self.edges[to_n]:
				path_dict[to_n] = from_n
				from_index = to_index;
				to_index -= 1;
				from_n = explored[from_index]
				to_n = explored[to_index]
				# if to_n == self.current_location:
				# 	path_dict[to_n] = from_n
				# 	break
			else:
				to_index -= 1
				to_n = explored[to_index]

		self.travel_path = path_dict

	def go_back_home_boi(self, stench, breeze):
		# print("============================IN Go back Home boi============================")
		# print("WorldWide current_location, ", self.current_location)
		# print("WorldWide travel to: ", self.travel_to)
		# print("WorldWide path: ", self.travel_path)
		# print("Visited: ", self.visited)
		# print("is_safe: ", self.is_safe)
		# print("known_safe: ", self.known_safe)
		# print("Unvisited and Risks: ", self.unvisited)
		# print("Known wumpus or pits: ", self.known_wumpus_or_pits)
		# print("==========================Not in Go back Home boi==========================")
		going_to = self.path_back[self.current_location];
		if self.facing == Direction.right: #FACING RIGHT
			if self.current_location[0] == going_to[0]: #IF X'S MATCH
				if (self.current_location[1] - going_to[1]) == -1:
					# print("TURN_LEFT                                         ")
					return Agent.Action.TURN_LEFT;
				elif (self.current_location[1] - going_to[1]) == 1:
					# print("TURN_RIGHT")
					return Agent.Action.TURN_RIGHT;
			elif self.current_location[1] == going_to[1]: #IF Y'S MATCH
				if (self.current_location[0] - going_to[0] == -1):
					# print("FORWARD")
					return Agent.Action.FORWARD;
				elif (self.current_location[0] - going_to[0] == 1):
					# print("TURN_RIGHT")
					return Agent.Action.TURN_RIGHT;

		elif self.facing == Direction.down: #FACING DOWN
			if self.current_location[0] == going_to[0]: #IF X'S MATCH
				if (self.current_location[1] - going_to[1]) == -1:
					# print("TURN_RIGHT")
					return Agent.Action.TURN_RIGHT;
				elif (self.current_location[1] - going_to[1]) == 1:
					# print("FORWARD")
					return Agent.Action.FORWARD;
			elif self.current_location[1] == going_to[1]: #IF Y'S MATCH
				if (self.current_location[0] - going_to[0] == -1):
					# print("TURN_LEFT")
					return Agent.Action.TURN_LEFT;
				elif (self.current_location[0] - going_to[0] == 1):
					# print("TURN_RIGHT")
					return Agent.Action.TURN_RIGHT;

		elif self.facing == Direction.left: #FACING LEFT
			if self.current_location[0] == going_to[0]: #IF X'S MATCH
				if (self.current_location[1] - going_to[1]) == -1:
					# print("TURN_RIGHT")
					return Agent.Action.TURN_RIGHT;
				elif (self.current_location[1] - going_to[1]) == 1:
					# print("TURN_LEFT")
					return Agent.Action.TURN_LEFT;
			elif self.current_location[1] == going_to[1]: #IF Y'S MATCH
				if (self.current_location[0] - going_to[0] == -1):
					# print("TURN_LEFT")
					return Agent.Action.TURN_RIGHT;
				elif (self.current_location[0] - going_to[0] == 1):
					# print("FORWARD")
					return Agent.Action.FORWARD;

		elif self.facing == Direction.up: #FACING UP
			if self.current_location[0] == going_to[0]: #IF X'S MATCH
				if (self.current_location[1] - going_to[1]) == -1:
					# print("FORWARD")
					return Agent.Action.FORWARD;
				elif (self.current_location[1] - going_to[1]) == 1:
					# print("TURN_LEFT")
					return Agent.Action.TURN_RIGHT;
			elif self.current_location[1] == going_to[1]: #IF Y'S MATCH
				if (self.current_location[0] - going_to[0] == -1):
					# print("TURN_RIGHT")
					return Agent.Action.TURN_RIGHT;
				elif (self.current_location[0] - going_to[0] == 1):
					# print("TURN_LEFT")
					return Agent.Action.TURN_LEFT;

	def MrWorldWide(self, stench, breeze):
		# print("============================IN MrWorldWide============================")
		# print("WorldWide current_location, ", self.current_location)
		# print("WorldWide travel to: ", self.travel_to)
		# print("WorldWide path: ", self.travel_path)
		# print("Visited: ", self.visited)
		# print("is_safe: ", self.is_safe)
		# print("known_safe: ", self.known_safe)
		# print("Unvisited and Risks: ", self.unvisited)
		# print("Known wumpus or pits: ", self.known_wumpus_or_pits)
		# print("==========================Not in MrWorldWide==========================")
		going_to = self.travel_path[self.current_location];
		if self.facing == Direction.right: #FACING RIGHT
			if self.current_location[0] == going_to[0]: #IF X'S MATCH
				if (self.current_location[1] - going_to[1]) == -1:
					# print("TURN_LEFT                                         ")
					return Agent.Action.TURN_LEFT;
				elif (self.current_location[1] - going_to[1]) == 1:
					# print("TURN_RIGHT")
					return Agent.Action.TURN_RIGHT;
			elif self.current_location[1] == going_to[1]: #IF Y'S MATCH
				if (self.current_location[0] - going_to[0] == -1):
					# print("FORWARD")
					return Agent.Action.FORWARD;
				elif (self.current_location[0] - going_to[0] == 1):
					# print("TURN_RIGHT")
					return Agent.Action.TURN_RIGHT;

		elif self.facing == Direction.down: #FACING DOWN
			if self.current_location[0] == going_to[0]: #IF X'S MATCH
				if (self.current_location[1] - going_to[1]) == -1:
					# print("TURN_RIGHT")
					return Agent.Action.TURN_RIGHT;
				elif (self.current_location[1] - going_to[1]) == 1:
					# print("FORWARD")
					return Agent.Action.FORWARD;
			elif self.current_location[1] == going_to[1]: #IF Y'S MATCH
				if (self.current_location[0] - going_to[0] == -1):
					# print("TURN_LEFT")
					return Agent.Action.TURN_LEFT;
				elif (self.current_location[0] - going_to[0] == 1):
					# print("TURN_RIGHT")
					return Agent.Action.TURN_RIGHT;

		elif self.facing == Direction.left: #FACING LEFT
			if self.current_location[0] == going_to[0]: #IF X'S MATCH
				if (self.current_location[1] - going_to[1]) == -1:
					# print("TURN_RIGHT")
					return Agent.Action.TURN_RIGHT;
				elif (self.current_location[1] - going_to[1]) == 1:
					# print("TURN_LEFT")
					return Agent.Action.TURN_LEFT;
			elif self.current_location[1] == going_to[1]: #IF Y'S MATCH
				if (self.current_location[0] - going_to[0] == -1):
					# print("TURN_LEFT")
					return Agent.Action.TURN_RIGHT;
				elif (self.current_location[0] - going_to[0] == 1):
					# print("FORWARD")
					return Agent.Action.FORWARD;

		elif self.facing == Direction.up: #FACING UP
			if self.current_location[0] == going_to[0]: #IF X'S MATCH
				if (self.current_location[1] - going_to[1]) == -1:
					# print("FORWARD")
					return Agent.Action.FORWARD;
				elif (self.current_location[1] - going_to[1]) == 1:
					# print("TURN_LEFT")
					return Agent.Action.TURN_RIGHT;
			elif self.current_location[1] == going_to[1]: #IF Y'S MATCH
				if (self.current_location[0] - going_to[0] == -1):
					# print("TURN_RIGHT")
					return Agent.Action.TURN_RIGHT;
				elif (self.current_location[0] - going_to[0] == 1):
					# print("TURN_LEFT")
					return Agent.Action.TURN_LEFT;

	def handle_1_1(self, stench, breeze, glitter, bump, scream):
		if self.first_turn:
			self.is_safe[(1,1)] = (stench, breeze)
			self.add_adjacent();
			if self.have_gold:
				return Agent.Action.CLIMB;
			# elif self.visit_1_1:
			# 	return Agent.Action.CLIMB;
			elif stench and breeze:
				return Agent.Action.CLIMB;
			# 	if self.have_arrow == False:
			# 		# print("stench and breeze and go forward");
			# 		self.wumpus_location = (1,2);
			# 		self.known_wumpus_or_pits[(1,2)] = (True, True); #if stench and breeze and no arrow then we will go forward. If we survive then forsure wumpus & pit in (1,1);
			# 		# print("wumpus_location found and no arrow. Go forward")
			# 		self.known_safe.append((2,1))
			# 		self.first_turn == False;
			# 		return self.handle_forward(stench, breeze);
			# 	if random.randrange(10) >1:
			# 		# print("stench and breeze and climb")
			# 		return Agent.Action.CLIMB;
			# 	else:
			# 		# print("stench and breeze and shoot");
			# 		self.have_arrow = False;
			# 		return Agent.Action.SHOOT;

			# elif scream and breeze:
			# 	# print("scream and breeze. Wumpus is dead and go forward");
			# 	self.wumpus_is_alive = False;
			# 	self.known_wumpus_or_pits[(1,2)] = (False, True); #if we go forward and survive then (1,2) forsure has breeze.
			# 	self.known_safe.append((2,1))
			# 	self.first_turn = False;
			# 	return self.handle_forward(stench, breeze)
			elif stench:
				# print("stench")
				if self.have_arrow == True:
					# print("stench, have arrow, and shoot");
					self.have_arrow = False;
					return Agent.Action.SHOOT;
				else:
					self.wumpus_location = (1,2);
					self.known_wumpus_or_pits[(1,2)] = (True, False); #if stench and no arrow then forsure wumpus in (1,2)
					self.known_safe.append((2,1))
					# print("stench, no arrow, and wumpus_location found. Go forward")
					self.first_turn = False;
					return self.handle_forward(stench, breeze);
			elif scream:
				# print("Scream and forward")
				self.unvisited[(1,2)] = 0; #if we shoot right then perceive scream then wumpus dead. (1,2) will forsure be safe bc no wumpus.
				self.known_safe.append((1,2))
				self.wumpus_is_alive = False;
				self.first_turn = False;
				return self.handle_forward(stench, breeze);
			elif breeze:
				if random.randrange(10) > 8:
					# print("breeze and forward")
					self.known_wumpus_or_pits[(1,2)] = (False, True); #if we go forward and survive then (1,2) forsure has breeze.
					self.first_turn = False;
					return self.handle_forward(stench, breeze);
				# print("breeze and climb out");
				return Agent.Action.CLIMB;
			else:
				# print("no percepts and go forward")
				self.unvisited[(1,2)] = 0; #if no percept then we go forward and the other adjacent forsure has no breeze.
				self.first_turn = False;
				self.known_safe.append((1,2))
				self.known_safe.append((2,1))
				return self.handle_forward(stench, breeze);

	def handle_bumps(self):
		if self.travel_to in self.unvisited:
			del self.unvisited[self.travel_to]
		self.travel_to = None;

		if self.board_width == True:
			for node in self.unvisited:
				if node[0] == self.board_width:
					del self.unvisited[node]
		if self.board_height == True:
			for node in self.unvisited:
				if node[1] == self.board_height:
					del self.unvisited[node]

		adj_list = [(self.current_location[0]+1, self.current_location[1]),
					(self.current_location[0]-1, self.current_location[1]),
					(self.current_location[0], self.current_location[1] + 1),
					(self.current_location[0], self.current_location[1] -1)]

		if (self.current_location in self.is_safe):
			del self.is_safe[self.current_location];
		if (self.current_location in self.visited):
			self.visited.remove(self.current_location);
		if (self.current_location in self.unvisited):
			# print("Deleting from unvisited: ", self.current_location)
			del self.unvisited[self.current_location];
		if (self.current_location in self.edges):
			del self.edges[self.current_location];
		if self.current_location in self.known_safe:
			self.known_safe.remove(self.current_location)

		for edge in self.edges:
			if self.current_location in self.edges[edge]:
				self.edges[edge].remove(self.current_location)

		if self.facing == Direction.right:
			self.board_width = self.current_location[0] - 1;
			self.true_width = True;
			self.current_location = (self.current_location[0] - 1, self.current_location[1])
			for adj in adj_list:
				if adj in self.unvisited and adj != self.current_location:
					del self.unvisited[adj]
			return self.handle_turning(Agent.Action.TURN_LEFT);
		elif self.facing == Direction.left:
			self.current_location = (self.current_location[0] + 1, self.current_location[1])
			for adj in adj_list:
				if adj in self.unvisited and adj != self.current_location:
					del self.unvisited[adj]
			return self.handle_turning(Agent.Action.TURN_LEFT);
		elif self.facing == Direction.up:
			self.board_height = self.current_location[1] - 1;
			self.true_height = True;
			self.current_location = (self.current_location[0], self.current_location[1] - 1)
			for adj in adj_list:
				if adj in self.unvisited and adj != self.current_location:
					del self.unvisited[adj]
			return self.handle_turning(Agent.Action.TURN_LEFT);
		elif self.facing == Direction.down:
			self.current_location = (self.current_location[0], self.current_location[1] + 1)
			for adj in adj_list:
				if adj in self.unvisited and adj != self.current_location:
					del self.unvisited[adj]
			return self.handle_turning(Agent.Action.TURN_LEFT);

	def handle_turning(self, action):
		if action == Agent.Action.TURN_LEFT:
			if self.facing == Direction.right:
				self.facing = Direction.up;
				# print("bump and turn left baybeee");
				return Agent.Action.TURN_LEFT;
			elif self.facing == Direction.left:
				self.facing = Direction.down;
				# print("bump and turn left baybeee");
				return Agent.Action.TURN_LEFT;
			elif self.facing == Direction.up:
				self.facing = Direction.left;
				# print("bump and turn left baybeee");
				return Agent.Action.TURN_LEFT;
			elif self.facing == Direction.down:
				self.facing = Direction.right;
				# print("bump and turn left baybeee");
				return Agent.Action.TURN_LEFT;
		elif action == Agent.Action.TURN_RIGHT:
			if self.facing == Direction.right:
				self.facing = Direction.down;
				# print("bump and turn left baybeee");
				return Agent.Action.TURN_RIGHT;
			elif self.facing == Direction.left:
				self.facing = Direction.up;
				# print("bump and turn left baybeee");
				return Agent.Action.TURN_RIGHT;
			elif self.facing == Direction.up:
				self.facing = Direction.right;
				# print("bump and turn left baybeee");
				return Agent.Action.TURN_RIGHT;
			elif self.facing == Direction.down:
				self.facing = Direction.left;
				# print("bump and turn left baybeee");
				return Agent.Action.TURN_RIGHT;

	def add_adjacent(self):
		plus_x = (self.current_location[0]+1, self.current_location[1]);
		minus_x = (self.current_location[0]-1, self.current_location[1]);
		plus_y = (self.current_location[0], self.current_location[1] + 1);
		minus_y = (self.current_location[0], self.current_location[1] -1);

		if self.current_location[0] > 1 and minus_x not in self.visited:
			self.unvisited[minus_x] = 0;
		if self.current_location[0] < self.board_width and plus_x not in self.visited:
			self.unvisited[plus_x] = 0;
		if self.current_location[1] > 1 and minus_y not in self.visited:
			self.unvisited[minus_y] = 0;
		if self.current_location[1] < self.board_height and plus_y not in self.visited:
			self.unvisited[plus_y] = 0;

		edges = list();
		if self.current_location[0] > 1 and minus_x in self.visited:
			edges.append(minus_x);
		if self.current_location[0] < self.board_width and plus_x in self.visited:
			edges.append(plus_x);
		if self.current_location[1] > 1 and minus_y in self.visited:
			edges.append(minus_y);
		if self.current_location[1] < self.board_height and plus_y in self.visited:
			edges.append(plus_y);
		self.edges[self.current_location] = edges;

		for edge in edges:
			if edge in self.edges:
				if self.current_location not in self.edges[edge]:
					self.edges[edge].append(self.current_location);

	def handle_forward(self, stench, breeze):
		if self.current_location not in self.visited: # add old location to visited
			self.visited.append(self.current_location);
		if self.current_location not in self.is_safe and self.current_location in self.visited:
			self.is_safe[self.current_location] = (stench, breeze);
		if self.current_location in self.unvisited:
			del self.unvisited[self.current_location]
		if self.current_location not in self.known_safe:
			self.known_safe.append(self.current_location)


		if self.facing == Direction.left and self.current_location[0] >= 1:
			self.current_location = (self.current_location[0] - 1, self.current_location[1]);
			if self.current_location not in self.visited: #add new location to visited
				self.visited.append(self.current_location);
			# if self.current_location not in self.is_safe and self.current_location in self.visited:
			# 	self.is_safe[self.current_location] = (stench, breeze);
			if self.current_location not in self.known_safe:
				self.known_safe.append(self.current_location)
			if self.current_location in self.unvisited:
				del self.unvisited[self.current_location]
			self.add_adjacent();
			return Agent.Action.FORWARD;
		elif self.facing == Direction.down and self.current_location[1] >= 1:
			self.current_location = (self.current_location[0], self.current_location[1] - 1);
			if self.current_location not in self.visited: #add new location to visited
				self.visited.append(self.current_location);
			# if self.current_location not in self.is_safe and self.current_location in self.visited:
			# 	self.is_safe[self.current_location] = (stench, breeze);
			if self.current_location not in self.known_safe:
				self.known_safe.append(self.current_location)
			if self.current_location in self.unvisited:
				del self.unvisited[self.current_location]
			self.add_adjacent();
			return Agent.Action.FORWARD;
		elif self.facing == Direction.right and self.current_location[0] <= self.board_width:
			self.current_location = (self.current_location[0] + 1, self.current_location[1]);
			if self.current_location not in self.visited: #add new location to visited
				self.visited.append(self.current_location);
			# if self.current_location not in self.is_safe and self.current_location in self.visited:
			# 	self.is_safe[self.current_location] = (stench, breeze);
			if self.current_location not in self.known_safe:
				self.known_safe.append(self.current_location)
			if self.current_location in self.unvisited:
				del self.unvisited[self.current_location]
			self.add_adjacent();
			return Agent.Action.FORWARD;
		elif self.facing == Direction.up and self.current_location[1] <= self.board_height:
			self.current_location = (self.current_location[0], self.current_location[1] + 1);
			if self.current_location not in self.visited: #add new location to visited
				self.visited.append(self.current_location);
			# if self.current_location not in self.is_safe and self.current_location in self.visited:
			# 	self.is_safe[self.current_location] = (stench, breeze);
			if self.current_location not in self.known_safe:
				self.known_safe.append(self.current_location)
			if self.current_location in self.unvisited:
				del self.unvisited[self.current_location]
			self.add_adjacent();
			return Agent.Action.FORWARD;

	def calculate_risks_current_location(self, node, stench, breeze):
			adj_list = list();

			if len(self.visited) != 0: #don't do calucations when backtracking
				if node in self.visited:
					return;

			plus_x = (node[0]+1, node[1]);
			minus_x = (node[0]-1, node[1]);
			plus_y = (node[0], node[1] + 1);
			minus_y = (node[0], node[1] -1);

			if node[0] > 1:
				adj_list.append(minus_x);
			if node[0] < self.board_width:
				adj_list.append(plus_x);
			if node[1] > 1:
				adj_list.append(minus_y);
			if node[1] < self.board_height:
				adj_list.append(plus_y);

			if stench or breeze:
				nKnown = 0;
				risk = 100;
				for check_node in adj_list:
					if check_node in self.known_safe:
						nKnown += 1;
					if check_node in self.known_wumpus_or_pits.keys():
						nKnown += 1;


				if len(adj_list) == 4:
					risk = 100 - (	nKnown * 25);
					if risk <= 25:
						risk = 100;
				elif len(adj_list) == 3:
					risk = 100 - ( (nKnown * 25) + 25);
					if risk <= 25:
						risk = 100;
				elif len(adj_list) == 2:
					risk = 100 - ( (nKnown * 25) + 50);
					if risk <= 25:
						risk = 100;
			else:
				risk = 0;

			return risk;
	def in_corner(self, node):
		if ((node[0] == 1 and node[1] == 1) or
			(node[0] == 1 and node[1] == self.board_height) or
			(node[0] == self.board_width and node[1] == 1) or
			(node[0] == self.board_width and node[1] == self.board_height)):
			return True
		return False


	def on_edge(self, node):
		if node[0] == 1 or node[0] == self.board_width or node[1] == 1 or node[1] == self.board_height:
			return True;
		return False;


	def calculate_risks(self, stench, breeze):
		# print("============================IN Calculate Risks============================")
		for known in self.known_wumpus_or_pits:
			if known in self.unvisited:
				# print("Removing ", known, "from unvisited: known wumpus or pits")
				del self.unvisited[known]
		for node in list(self.unvisited.keys()):
			riskCurrentNode = self.calculate_risks_current_location(node, stench, breeze);

			adj_list = list();

			plus_x = (node[0]+1, node[1]);
			minus_x = (node[0]-1, node[1]);
			plus_y = (node[0], node[1] + 1);
			minus_y = (node[0], node[1] -1);

			if node[0] > 1:
				adj_list.append(minus_x);
			if node[0] < self.board_width:
				adj_list.append(plus_x);
			if node[1] > 1:
				adj_list.append(minus_y);
			if node[1] < self.board_height:
				adj_list.append(plus_y);


			breeze = 0;
			stench = 0;
			nKnown = 0;

			# print("Adj list for node ", node, ": ", adj_list)
			for check_node in adj_list:
				if check_node in self.is_safe:
					nKnown += 1;
					if self.is_safe[check_node][0]:
						# print("Stench found in ", check_node)
						stench += 1;
					if self.is_safe[check_node][1]:
						breeze += 1
						# print("Stench found in ", check_node)
			# print("For Node: ", node, "\nNumber of breezes: ", breeze, "\nNumber of stenches: ", stench)


			#Corner case
			if self.in_corner(node):
				#General Check:
				if (nKnown > stench) and (nKnown > breeze):
					self.unvisited[node] = 0;
				elif (stench >= 2 and breeze >= 2):
					# print("Found Wumpus and pit at: ", node, "\n stench and breeze corner case")
					self.known_wumpus_or_pits[node] = (True, True)
					if node in self.unvisited:
						del self.unvisited[node];
					self.wumpus_location = node;
				else:
					if stench >= 2 :
						# print("Found Wumpus at: ", node, "\n stench corner case")
						self.known_wumpus_or_pits[node] = (True, False)
						if node in self.unvisited:
							del self.unvisited[node];
						self.wumpus_location = node;
					elif breeze >= 2 :
						# print("Found pit at: ", node, "\n breeze corner case")
						self.known_wumpus_or_pits[node] = (False, True)
						if node in self.unvisited:
							del self.unvisited[node];
					elif stench == 1 or breeze == 1:
						if nKnown >= 2:
							self.unvisited[node] = 0;
						else:
							self.unvisited[node] = 50;
					else:
						self.unvisited[node] = 0;

			#Edge case
			if self.on_edge(node):
				#General Check:
				if (nKnown > stench) and (nKnown > breeze):
					self.unvisited[node] = 0;
				elif (stench >= 2 and breeze >= 2):
					# print("Found Wumpus and pit at: ", node, "\n stench and breeze edge case")
					self.known_wumpus_or_pits[node] = (True, True)
					if node in self.unvisited:
						del self.unvisited[node];
					self.wumpus_location = node;
				else:
					if stench >= 2 :
						# print("Found Wumpus at: ", node, "\n stench edge case")
						self.known_wumpus_or_pits[node] = (True, False)
						if node in self.unvisited:
							del self.unvisited[node];
						self.wumpus_location = node;
					elif breeze >= 2 :
						# print("Found pit at: ", node, "\n breeze edge case")
						self.known_wumpus_or_pits[node] = (False, True)
						if node in self.unvisited:
							del self.unvisited[node];
					elif stench == 1 or breeze == 1:
						if nKnown >= 2:
							self.unvisited[node] = 0;
						else:
							self.unvisited[node] = 50;
					else:
						self.unvisited[node] = 0;

			#Open case
			else:
				#General Check:
				if (nKnown > stench) and (nKnown > breeze):
					self.unvisited[node] = 0;
				elif (stench >= 3 and breeze >= 3):
					# print("Found Wumpus and pit at: ", node, "\n stench and breeze open case")
					self.known_wumpus_or_pits[node] = (True, True)
					if node in self.unvisited:
						del self.unvisited[node];
					self.wumpus_location = node;
				else:
					if stench >= 3 :
						# print("Found Wumpus at: ", node, "\n stench open case")
						self.known_wumpus_or_pits[node] = (True, False)
						if node in self.unvisited:
							del self.unvisited[node];
						self.wumpus_location = node;
					elif breeze >= 3 :
						# print("Found pit at: ", node, "\n breeze open case")
						self.known_wumpus_or_pits[node] = (False, True)
						if node in self.unvisited:
							del self.unvisited[node];
					elif stench == 2 or breeze ==2 :
						self.unvisited[node] = 75;
					elif stench == 1 or breeze == 1:
						if nKnown >= 2:
							self.unvisited[node] = 0;
						else:
							self.unvisited[node] = 50;
					else:
						self.unvisited[node] = 0;

	def leastRiskyNode(self, stench, breeze):
		'''
		Gets the least risky node from the self.risks dictionary
		if there are multiple of the same risk, it chooses randomly
		'''
		if len(self.unvisited.values()) == 0:
			if self.wumpus_location != None:
				if self.wumpus_is_alive and self.have_arrow and self.known_wumpus_or_pits[self.wumpus_location][1] == False:
					if not self.attack_wumpus:
						self.travel_to = self.adjWumpus();
						self.travel_path.clear();
						self.attack_wumpus = True;
					else:
						self.shoot_wumpus = True;
				else:
					self.traverse = False;
					self.find_way_back();
			else:
				self.traverse = False;
				self.find_way_back();


		else:
			min_value = min(self.unvisited.values());
			if min_value > 25:
				# print("it's a little risky frisky in here")
				self.travel_to = None;
				self.travel_path.clear()
				self.traverse = False;
				self.find_way_back();

			else:
				min_keys = [k for k in self.unvisited if self.unvisited[k] == min_value];
				min_keys = sorted(min_keys, key=self.heuristic)
				# for key in min_keys:
				# 	print(key, ": " , self.heuristic(key))
				self.travel_to = min_keys[0];


	def heuristic(self, b):
		'''
		Heuristic used in A* search:
		'''
		return abs(self.current_location[0] - b[0]) + abs(self.current_location[1] - b[1]);

	def adjWumpus(self):
		node = self.wumpus_location;
		adj_list = list();
		visited_list = list();

		plus_x = (node[0]+1, node[1]);
		minus_x = (node[0]-1, node[1]);
		plus_y = (node[0], node[1] + 1);
		minus_y = (node[0], node[1] -1);

		if node[0] > 1:
			adj_list.append(minus_x);
		if node[0] < self.board_width:
			adj_list.append(plus_x);
		if node[1] > 1:
			adj_list.append(minus_y);
		if node[1] < self.board_height:
			adj_list.append(plus_y);

		for adj_node in adj_list:
			if adj_node in self.visited:
				visited_list.append(adj_node);

		min_keys = sorted(visited_list, key=self.heuristic)
		return min_keys[0];

	def make_move(self, stench, breeze, glitter, bump, scream):
		if self.travel_to == None or self.current_location == self.travel_to or self.traverse == False:
			# if self.current_location == self.travel_to:
			# 	del self.unvisited[self.current_location]
			self.calculate_risks(stench, breeze)
			self.leastRiskyNode(stench, breeze)
			if self.traverse == False:
				self.find_way_back()
				return self.go_back_home_boi(stench, breeze)
			elif self.attack_wumpus:
				if self.current_location != self.travel_to:
					self.find_path();
					return self.MrWorldWide(stench,breeze)
				else:
					facing = self.look_dat_way_boi(self.wumpus_location)
					if facing == True and self.have_arrow:
						return Agent.Action.SHOOT;
					elif facing == True and self.have_arrow == False:
						return Agent.Action.FORWARD;
					else:
						return facing;
			else:
				self.find_path();
		elif stench or breeze:
			self.calculate_risks(stench, breeze);
			self.leastRiskyNode(stench, breeze)
			unv_vals = self.unvisited.values()
			if len(unv_vals) != 0:
				min_value = min(unv_vals);
				if self.unvisited[self.travel_to] > min_value:
					self.leastRiskyNode(stench, breeze);
				# self.find_path();
		self.calculate_risks(stench, breeze);
		self.find_path();
		return self.MrWorldWide(stench, breeze);


	def getAction( self, stench, breeze, glitter, bump, scream ):
		# if self.wumpus_location != None:
		# 	print("wumpus_location: ", self.wumpus_location)
		self.add_adjacent();
		if self.current_location not in self.is_safe and self.current_location in self.visited:
			self.is_safe[self.current_location] = (stench, breeze);
		self.imGAY -=1;
		if self.imGAY <= -150:
			self.traverse = False;
			self.find_way_back();
		self.calculate_risks(stench, breeze);

		# print("============================IN Get Action============================")
		# print("WorldWide current_location, ", self.current_location)
		# print("WorldWide travel to: ", self.travel_to)
		# print("WorldWide path: ", self.travel_path)
		# print("Visited: ", self.visited)
		# print("is_safe: ", self.is_safe)
		# print("known_safe: ", self.known_safe)
		# print("Unvisited and Risks: ", self.unvisited)
		# print("Known wumpus or pits: ", self.known_wumpus_or_pits)
		# print("==========================NOT IN Get Action==========================")
		# print("Unvisited",self.unvisited)
		# print("visited", self.visited)
		# print("is Safe: ",self.is_safe)
		# print("Current Location: ", self.current_location)
		# print("Edges: ", self.edges)
		# print("Travel To: ", self.travel_to)
		# print("Travel Path: ", self.travel_path)
		if glitter:
			# print("picked up gold");
			self.have_gold = True;
			self.traverse = False;
			self.find_way_back();
			return Agent.Action.GRAB;
		elif self.current_location == (1,1) and self.have_gold:
			return Agent.Action.CLIMB
		elif self.current_location == (1,1) and self.first_turn == True:
			return self.handle_1_1(stench, breeze, glitter, bump, scream);
		elif self.traverse == False:
			# print("traverse == False")
			if self.current_location == (1,1):
				# print("CLIMB")
				return Agent.Action.CLIMB;
			# self.find_way_back();
			move = self.make_move(stench, breeze, glitter, bump, scream)
			# move = Agent.Action.FORWARD;
			if bump:
				# print("Handling Bumps")
				return self.handle_bumps();
			elif move == Agent.Action.FORWARD:
				# print("Handle Forward")
				return self.handle_forward(stench, breeze);
			elif move == Agent.Action.TURN_LEFT:
				# print("Handle Turning: Left")
				return self.handle_turning(Agent.Action.TURN_LEFT);
			elif move == Agent.Action.TURN_RIGHT:
				# print("Handle Turning: Right")
				return self.handle_turning(Agent.Action.TURN_RIGHT);
		else: #not (1,1) case
			move = self.make_move(stench, breeze, glitter, bump, scream)
			# move = Agent.Action.FORWARD;
			if bump:
				# print("Handling Bumps")
				return self.handle_bumps();
			elif move == Agent.Action.FORWARD:
				# print("Handle Forward")
				return self.handle_forward(stench, breeze);
			elif move == Agent.Action.TURN_LEFT:
				# print("Handle Turning: Left")
				return self.handle_turning(Agent.Action.TURN_LEFT);
			elif move == Agent.Action.TURN_RIGHT:
				# print("Handle Turning: Right")
				return self.handle_turning(Agent.Action.TURN_RIGHT);
			else:
				return move

	def look_dat_way_boi(self, node_to_face):
			"""
			Will return an action to turn if not facing the correct direction.
			Returns True if facing correct way.
			"""
			going_to = node_to_face;
			if self.facing == Direction.right: #FACING RIGHT
				if self.current_location[0] == going_to[0]: #IF X'S MATCH
					if (self.current_location[1] - going_to[1]) == -1:
						return Agent.Action.TURN_LEFT;
					elif (self.current_location[1] - going_to[1]) == 1:
						return Agent.Action.TURN_RIGHT;
				elif self.current_location[1] == going_to[1]: #IF Y'S MATCH
					if (self.current_location[0] - going_to[0] == -1):
						return True;
					elif (self.current_location[0] - going_to[0] == 1):
						return Agent.Action.TURN_RIGHT;

			elif self.facing == Direction.down: #FACING DOWN
				if self.current_location[0] == going_to[0]: #IF X'S MATCH
					if (self.current_location[1] - going_to[1]) == -1:
						return Agent.Action.TURN_RIGHT;
					elif (self.current_location[1] - going_to[1]) == 1:
						return True;
				elif self.current_location[1] == going_to[1]: #IF Y'S MATCH
					if (self.current_location[0] - going_to[0] == -1):
						return Agent.Action.TURN_LEFT;
					elif (self.current_location[0] - going_to[0] == 1):
						return Agent.Action.TURN_RIGHT;

			elif self.facing == Direction.left: #FACING LEFT
				if self.current_location[0] == going_to[0]: #IF X'S MATCH
					if (self.current_location[1] - going_to[1]) == -1:
						return Agent.Action.TURN_RIGHT;
					elif (self.current_location[1] - going_to[1]) == 1:
						return Agent.Action.TURN_LEFT;
				elif self.current_location[1] == going_to[1]: #IF Y'S MATCH
					if (self.current_location[0] - going_to[0] == -1):
						return Agent.Action.TURN_LEFT;
					elif (self.current_location[0] - going_to[0] == 1):
						return True;

			elif self.facing == Direction.up: #FACING UP
				if self.current_location[0] == going_to[0]: #IF X'S MATCH
					if (self.current_location[1] - going_to[1]) == -1:
						return True;
					elif (self.current_location[1] - going_to[1]) == 1:
						return Agent.Action.TURN_LEFT;
				elif self.current_location[1] == going_to[1]: #IF Y'S MATCH
					if (self.current_location[0] - going_to[0] == -1):
						return Agent.Action.TURN_RIGHT;
					elif (self.current_location[0] - going_to[0] == 1):
						return Agent.Action.TURN_LEFT;


from enum import Enum
from collections import namedtuple
import random
import operator

class Direction ( Enum ):
	left = 1;
	right = 2;
	up = 3;
	down = 4;


    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
