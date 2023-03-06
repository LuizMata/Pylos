import math
import json
import copy

N = 3
COUNT = math.ceil(sum([ii * ii for ii in range(1, N + 1)]) /
                  2)  # total count of red (or blue) marbles
B, R, E = "B", "R", "E"  # aliases of colors
CP, CN, CR, CL = "CP", "CN", "CR", "CL"  # alias of outcome classes


class State(object):
    def __init__(self, board=None):
        """Create a new state and board.  If no board is supplied as argument, create an empty board"""

    def get_count(self, color):
    

    def print(self):
        

    def play_add(self, color, layer, row, col):


    def play_jump(self, color, from_layer, from_row, from_col, to_layer, to_row, to_col):
       

    def check_availability_to_add(self, layer, row, col):
        

    def check_availability_to_jump(self, from_layer, from_row, from_col):
        

    def check_availability_to_jump_here(self, from_layer, from_row, from_col, to_layer, to_row, to_col):
        

    def get_children_add(self, color):
       

    def get_children_jump(self, color):
        

    def get_all_children(self, color):
        """Return all children for a color"""
        jump_children = self.get_children_jump(color)
        add_children = self.get_children_add(color)
        return jump_children + add_children

    def get_equivalence(self):
        """Return 8 equivalent states from rotation/mirro that share the same outcome class"""

        # Rotate 0, 90, 180, 270 and their mirrors
        r0_board = copy.deepcopy(self.board)
        r0m_board = copy.deepcopy(self.board)
        r90_board = copy.deepcopy(self.board)
        r90m_board = copy.deepcopy(self.board)
        r180_board = copy.deepcopy(self.board)
        r180m_board = copy.deepcopy(self.board)
        r270_board = copy.deepcopy(self.board)
        r270m_board = copy.deepcopy(self.board)
        for layer in range(N):
            for row in range(layer + 1):
                for col in range(layer + 1):
                    val = self.board[layer][row][col]
                    r0_board[layer][row][col] = val
                    r0m_board[layer][col][row] = val
                    r90_board[layer][layer - row][col] = val
                    r90m_board[layer][col][layer - row] = val
                    r180_board[layer][layer - row][layer - col] = val
                    r180m_board[layer][layer - col][layer - row] = val
                    r270_board[layer][row][layer - col] = val
                    r270m_board[layer][layer - col][row] = val
        r0_state = State(r0_board)
        r0m_state = State(r0m_board)
        r90_state = State(r90_board)
        r90m_state = State(r90m_board)
        r180_state = State(r180_board)
        r180m_state = State(r180m_board)
        r270_state = State(r270_board)
        r270m_state = State(r270m_board)

        # Return non-duplicates
        states = [
            r0_state, r0m_state, r90_state, r90m_state, r180_state,
            r180m_state, r270_state, r270m_state
        ]
        out = {ss.uid: ss for ss in states}
        return list(out.values())

    def compute_oc(self):
        """Compute outcome class of this state"""
        global oc_dict
        global oc_counter

        if self.uid in oc_dict:
            #print(f'Read existing OC: {self.uid}')
            return oc_dict[self.uid]
        else:
            outcome = CP  # default

            if self.board[0][0][0] == E:
                if self.get_count(B) == 0:
                    outcome = CR
                elif self.get_count(R) == 0:
                    outcome = CL
                else:
                    left_oc = self.check_for_CL(B) or self.check_for_CP(B)
                    right_oc = self.check_for_CR(R) or self.check_for_CP(R)
                    if left_oc and right_oc:
                        outcome = CN
                    if left_oc and not (right_oc):
                        outcome = CL
                    if not (left_oc) and right_oc:
                        outcome = CR

            oc_counter += 1
            print(f'Computed new OC: {self.uid} (total: {oc_counter})')

            # Add equivalent and flip entries to OCT_DICT
            eq_states = self.get_equivalence()
            flip_map = {"CL": "CR", "CR": "CL", "CP": "CP", "CN": "CN"}
            for eq_state in eq_states:
                oc_dict[eq_state.uid] = outcome  # save equivalent cases
                flip_eq_state = eq_state.flip()
                oc_dict[flip_eq_state.uid] = flip_map[
                    outcome]  # save flip cases

            return outcome

    def check_for_CL(self, color):
        """Return whether any children of color are CL"""
        children = self.get_all_children(color)
        for child in children:
            if child.compute_oc() == CL:
                return True
        return False

    def check_for_CR(self, color):
        """Return whether any children of color are CR"""
        children = self.get_all_children(color)
        for child in children:
            if child.compute_oc() == CR:
                return True
        return False

    def check_for_CP(self, color):
        """Return whether any children of color are CP"""
        children = self.get_all_children(color)
        for child in children:
            if child.compute_oc() == CP:
                return True
        return False

    def flip(self):
        