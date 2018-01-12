import settings
import next_cell_states


class Rules:
    @classmethod
    def calculate_next_state(cls, state):
        state = state.encode('ascii') # much faster to index than unicode is

        w = settings.COLUMNS
        h = settings.ROWS
        
        # pass 1: count neighbours
        neighbours0 = [0] * (w * h)
        neighbours1 = [0] * (w * h)
        col = 0
        row = 0
        for cell in state:
            if cell == b'0':
                if col > 0 and row > 0:
                    neighbours0[h*(row-1)+(col-1)] += 1
                if row > 0:
                    neighbours0[h*(row-1)+(col)] += 1
                if col < w-1 and row > 0:
                    neighbours0[h*(row-1)+(col+1)] += 1
                if col > 0:
                    neighbours0[h*(row)+(col-1)] += 1
                if col < w-1:
                    neighbours0[h*(row)+(col+1)] += 1
                if col > 0 and row < h-1:
                    neighbours0[h*(row+1)+(col-1)] += 1
                if row < h-1:
                    neighbours0[h*(row+1)+(col)] += 1
                if col < w-1 and row < h-1:
                    neighbours0[h*(row+1)+(col+1)] += 1
            elif cell == b'1':
                if col > 0 and row > 0:
                    neighbours1[h*(row-1)+(col-1)] += 1
                if row > 0:
                    neighbours1[h*(row-1)+(col)] += 1
                if col < w-1 and row > 0:
                    neighbours1[h*(row-1)+(col+1)] += 1
                if col > 0:
                    neighbours1[h*(row)+(col-1)] += 1
                if col < w-1:
                    neighbours1[h*(row)+(col+1)] += 1
                if col > 0 and row < h-1:
                    neighbours1[h*(row+1)+(col-1)] += 1
                if row < h-1:
                    neighbours1[h*(row+1)+(col)] += 1
                if col < w-1 and row < h-1:
                    neighbours1[h*(row+1)+(col+1)] += 1
            if col == w-1:
                row += 1
                col = 0
            else:
                col += 1

        # pass 2: build new state from old + neighbours
        next_cells = [''] * (w * h)
        idx = 0
        for cell in state:
            neighbours = neighbours0[idx] + neighbours1[idx]
            if cell == '.' and neighbours == 3: # birth
                next_cells[idx] = b'0' if neighbours0[idx] > neighbours1[idx] else b'1' 
            elif cell != '.' and (neighbours < 2 or neighbours > 3): # death
                next_cells[idx] = b'.' 
            else:
                next_cells[idx] = cell
            idx += 1

        return b''.join(next_cells).decode('ascii')

    def calculate_heuristic(state, my_turn):
        if my_turn:
            player_id = settings.PLAYER_ID
            opponent_id = settings.OPPONENT_ID
        else:
            opponent_id = settings.PLAYER_ID
            player_id = settings.OPPONENT_ID

        cell_count = state.count(player_id)
        opponent_cell_count = state.count(opponent_id)

        if opponent_cell_count == 0:
            # if the opponent has no cells left, this is a win, set to max
            value = 16 * settings.COLUMNS
        elif cell_count == 0:
            # if you have no cells left, this is a loss, set to min
            value = 0
        else:
            # otherwise use the difference between your and their live cells
            value = cell_count - opponent_cell_count

        return value
