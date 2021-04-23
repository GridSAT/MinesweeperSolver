import math

import mines

class Game:
    def __init__(self, gridsize, n_mines):
        self.rounds = 0
        self.gridsize = gridsize
        self.n_mines = n_mines
        self.values = dict()
        self.clauses = dict()
        self.variables = list()
        self.assignments = list()
        self.sweeper = mines.Mines(gridsize, n_mines)
        self.sweeper.showcurrent()
        self.game_state = self.sweeper.checkcell((0, 0))


    def process_state(self):
        for row_index in range(gridsize):
            for col_index in range(gridsize):
                if self.game_state[row_index][col_index] != ' ':
                    neighbors = self.find_neighbors(row_index, col_index)
                    if len(neighbors) > 0:
                        position = (row_index, col_index)
                        self.values[position] = self.game_state[row_index][col_index]
                        self.clauses[position] = neighbors
                        for location in neighbors:
                            if location not in self.variables:
                                self.variables.append(location)

    def find_neighbors(self, row_index, col_index):
        potential_mines = list()
        for x in range(row_index-1, row_index+2):
            for y in range(col_index - 1, col_index + 2):
                if x != row_index or y != col_index: # fixme check the logic
                    if x >= 0 and y >= 0 and x < self.gridsize and y < self.gridsize:
                        thisrow = self.game_state[x]
                        print(thisrow)
                        thisthing = self.game_state[x][y] # fixme placeholder
                        if thisthing == '':
                            print("nothing")
                        elif thisthing == ' ':
                            print("spaces")
                        else:
                            print("fuck", ord(thisthing))
                        if self.game_state[x][y] == ' ': #fixme check that this test is valid
                            location = (x, y)
                            potential_mines.append(location)
        return potential_mines

    def solve_move(self):
        found_move = False
        self.assignments = list() # reset the assignments list
        possibilities = math.pow(2, len(self.variables))
        expressions = list(self.clauses.keys()) # [(x1, y1).....] these have values

        while possibilities > 0: #and found_move == False:
            possibilities -= 1
            assignment = self.update_assignment(possibilities, len(self.variables))
            exp_index = 0
            valid = True
            while exp_index < len(expressions) and valid: #iterate through clauses check if assignment is valid
                target = int(self.values[expressions[exp_index]])
                neighbors = self.clauses[expressions[exp_index]]
                score = self.sum(neighbors, assignment)
                if score != target:
                    valid = False
                else:
                    exp_index += 1
            if valid == True:
                self.assignments.append(assignment)#found_move = True




    def sum(self, neighbors, assigned_nums):
        score = 0
        for neighbor in neighbors:
            assignment_index = self.variables.index(neighbor)
            score += int(assigned_nums[assignment_index])
        return score

    def make_move(self):
        print("length of variables:", len(self.variables))
        chosen_assignment = self.determine_assignment()
        print("length of choice:", len(chosen_assignment))
        for i in range(len(self.variables)):
            if chosen_assignment[i] == "1":
                self.sweeper.flags.append(self.variables[i]) # fixme use a union here
            elif chosen_assignment[i] == "0":
                location = (self.variables[i][0], self.variables[i][1])
                self.game_state = self.sweeper.checkcell(location)
            # else if it's an 'U' do nothing TODO

    def determine_assignment(self):
        if len(self.assignments) > 0:
            choice = list(self.assignments[0])
            for option in self.assignments:
                for i in range(len(choice)):
                    if choice[i] != "?":
                        if choice[i] != option[i]:
                            choice[i] = "?"
        return ''.join(choice)

    def update_assignment(self, choice, length):
        new_assignment = "{0:b}".format(int(choice)).zfill(length)
        return new_assignment #self.assignments = new_assignment

    def play_game(self):
        while not self.sweeper.isfail() and not self.game_finished():# while we haven't failed and haven't finished
            self.rounds += 1
            print("Round #", self.rounds)
            self.sweeper.showcurrent()
            self.process_state() # assess
            self.solve_move() #calculate next move
            self.make_move() # make next move

        if self.game_finished() and not self.sweeper.isfail():
            self.sweeper.showcurrent()
            print("Rounds needed", self.rounds)
        if self.sweeper.isfail():
            print("We have failed")

    def game_finished(self):  #TODO check this works
        if self.sweeper.checkmines():
            print("success")
            return True
        elif self.sweeper.isfail():
            print("fail")
            return True
        return False
     


if __name__ == '__main__':
    gridsize = 6 #16
    n_mines = 10 #40
    current_game = Game(gridsize, n_mines)
    current_game.play_game()
  
