import random
import math
import re

class Grid(object):

    def __init__(self, options=[], size=None, card_title=''):
        self.size = size
        if self.size is None:
            self.size = int(math.floor(math.sqrt(2*len(options))))
        if self.size % 2: 
            raise ValueError('Grid size must be even!')

        self.options = options
        if len(self.options) < (self.size*self.size)/2: 
            raise ValueError('Not enough options to fill grid!')

        self.showing = {}
        self.card_title = card_title
        self.largest_item = max(map(len,self.options + [self.card_title]))
        self.clear_grid()
        self.repopulate_grid()

    def clear_grid(self):
        self.grid = {}
        return self

    def repopulate_grid(self):
        num_options = int((self.size*self.size)/2)
        self.unpopulated = self.options[:num_options]*2
        choice_index = lambda: random.randint(0,len(self.unpopulated)-1)
        for i in range(self.size):
            for j in range(self.size):
                self.grid[(i,j)] = self.unpopulated.pop(choice_index())
        return self

    def __getitem__(self, coord):
        if len(coord) != 2:
            raise IndexError('Coordinates must be 2d')

        if coord[0] not in range(0,self.size) or \
           coord[1] not in range(0,self.size):
            raise ValueError('Position {0},{1} is off grid'.format(*coord))

        return self.grid[coord]

    def _format_cell(self, *coords):
        padding_tpl = '{{0: <{0}}}'.format(self.largest_item)
        if self.showing.get(coords):
            return padding_tpl.format(self.grid[coords])
        else:
            return padding_tpl.format(self.card_title)


    def __str__(self):
        cell_horiz_space = '+-' + '-'*self.largest_item
        row_hr = '-'.join([cell_horiz_space]*self.size) + '-+'

        rep = []

        for i in range(2*self.size+1):
            if i % 2 == 0:
                rep.append(row_hr)
                continue

            data = [
                self._format_cell((i-1)/2, j)
                for j in range(self.size)
            ]

            rep.append('| ' + ' | '.join(data) + ' |')

        return '\n'.join(rep)

    def __repr__(self):
        return str(self)

    def show(self, *coords):
        if len(coords) == 0:
            self.showing = {
                (i,j):1 
                for i in range(self.size)
                for j in range(self.size)
            }
            return self

        try:
            self.showing[coords] = 1
        except ValueError:
            pass

        return self

    def unshow(self, *coords):
        if len(coords) == 0:
            self.showing = {}
            return self


        try:
            self.showing[coords] = 0
        except ValueError:
            pass

        return self

def main():
    g = Grid('LION TIGER BEAR OCTOPUS BAT FOOT YETI PELICAN'.split())
    queued = []
    visible = []
    tries = 0

    while 1:
        try:
            if len(queued) < 2: 
                parsed = [int(x) for x in re.split(r'[^0-9]',input('> ').strip())]
                queued.append(tuple(parsed))
                g[queued[-1]]
            elif len(queued) == 2:
                if g[queued[0]] == g[queued[1]] and \
                   queued[0] != queued[1]:
                    visible += queued
                if sorted(visible) == sorted(list(g.grid.keys())): break
                queued = []
                continue

            [g.show(*a) for a in queued + visible]
            print('\n'*100)
            print(g)
            g.unshow()

        except SyntaxError as e:
            print('(syntax error: %s)' % (e.args[0],))
            queued = []
        except IndexError as e:
            print('(index error: %s)' % (e.args[0],))
            queued = []
        except ValueError as e:
            print('(value error: %s)' % (e.args[0],))
            queued = []

        tries += 1

    print("Finished in %d tries" % (tries,))

if __name__ == '__main__':
    main()

