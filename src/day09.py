import sys

class MarbleGame:
    def __init__(self, num_players, last_marble_worth):
        self.num_players = num_players
        self.last_marble_worth = last_marble_worth

        self.marbles = [0]
        self.current_marble_num = 1
        self.current_marble_idx = 0
        self.player_scores = [0 for _ in range(num_players)]

    def play(self):
        while self.current_marble_num < self.last_marble_worth:
            curr_marble, curr_player = self.next_play()

            if curr_marble % 23 == 0:
                # import ipdb; ipdb.set_trace()
                idx = self.get_index_n_counterclockwise(7)
                marble_to_remove = self.marbles.pop(idx)
                self.player_scores[curr_player] += curr_marble + marble_to_remove
                self.current_marble_idx = idx
            else:
                # Insert marble between 1 and 2 marbles clockwise
                idx = self.get_index_n_clockwise(1) + 1
                self.marbles.insert(idx, curr_marble)
                self.current_marble_idx = idx

            # print(self, end='\n\n')
            if self.current_marble_num % (10 ** 5) == 0:
                print('{} / {}'.format(self.current_marble_num, self.last_marble_worth))

    def next_play(self): # Returns next_marble, next_player
        next_m = self.current_marble_num
        self.current_marble_num += 1
        return next_m, next_m % self.num_players

    def get_index_n_clockwise(self, n):
        return (self.current_marble_idx + n) % len(self.marbles)

    def get_index_n_counterclockwise(self, n):
        return (self.current_marble_idx - n) % len(self.marbles)

    def __str__(self):
        return ''.join([' {:2} '.format(m) if i != self.current_marble_idx else '({:2})'.format(m) \
                        for i, m in enumerate(self.marbles)])


if __name__ == '__main__':
    import re
    # line = sys.stdin.readline().rstrip()
    line = open('../input/day09.in').readline().rstrip()
    # line = "30 players; last marble is worth 5807 points"

    match = re.match(r'([\d]+) players; last marble is worth ([\d]+) points', line)
    num_players = int(match.group(1))
    last_marble_worth = int(match.group(2))

    ## First part
    # game = MarbleGame(num_players, last_marble_worth)
    # game.play()
    # print(max(game.player_scores))

    ## Second part ## NOTE There's surely a more efficient way to do this
    game = MarbleGame(num_players, last_marble_worth * 100)
    game.play()
    print(max(game.player_scores))