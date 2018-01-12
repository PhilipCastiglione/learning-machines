import settings


class Rules:
    @classmethod
    def calculate_next_state(cls, state):
        w = settings.COLUMNS
        h = settings.ROWS
        
        # pass 1: count neighbours
        neighbours0 = [0] * (w * h)
        neighbours1 = [0] * (w * h)
        col = 0
        row = 0
        for cell in state:
            if cell == 48: # '0'
                if col > 0:
                    neighbours0[h*(row)+(col-1)] += 1
                    if row > 0:
                        neighbours0[h*(row-1)+(col-1)] += 1
                    if row < h-1:
                        neighbours0[h*(row+1)+(col-1)] += 1
                if col < w-1:
                    neighbours0[h*(row)+(col+1)] += 1
                    if row > 0:
                        neighbours0[h*(row-1)+(col+1)] += 1
                    if row < h-1:
                        neighbours0[h*(row+1)+(col+1)] += 1
                if row > 0:
                    neighbours0[h*(row-1)+(col)] += 1
                if row < h-1:
                    neighbours0[h*(row+1)+(col)] += 1
                
            elif cell == 49: # '1'
                if col > 0:
                    neighbours1[h*(row)+(col-1)] += 1
                    if row > 0:
                        neighbours1[h*(row-1)+(col-1)] += 1
                    if row < h-1:
                        neighbours1[h*(row+1)+(col-1)] += 1
                if col < w-1:
                    neighbours1[h*(row)+(col+1)] += 1
                    if row > 0:
                        neighbours1[h*(row-1)+(col+1)] += 1
                    if row < h-1:
                        neighbours1[h*(row+1)+(col+1)] += 1
                if row > 0:
                    neighbours1[h*(row-1)+(col)] += 1
                if row < h-1:
                    neighbours1[h*(row+1)+(col)] += 1

            col += 1
            if col == w:
                row += 1
                col = 0
        
        # pass 2: build new state from old + neighbours
        idx = 0
        for cell in state:
            neighbours = neighbours0[idx] + neighbours1[idx]
            if cell == '.' and neighbours == 3: # birth
                state[idx] = 48 if neighbours0[idx] > neighbours1[idx] else 49
            elif cell != '.' and (neighbours < 2 or neighbours > 3): # death
                state[idx] = 46
            idx += 1

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
