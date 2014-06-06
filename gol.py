import copy,sys,getopt,os,time

class newgame:
	def __init__(self,size,livecell,deadcell):
		self.size = size
		self.livecell = livecell
		self.deadcell = deadcell
		self.board = [copy.deepcopy([self.deadcell for y in range(self.size)]) for x in range(self.size)]
		
	def flip(self,cell):
		if cell == self.deadcell:
			cell = self.livecell
		else:
			cell = self.deadcell
		return cell
		
	def printboard(self):
		if os.name == 'nt':
			os.system('cls')
		else:
			os.system('clear')
		for x in self.board:
			print ''.join(x)

	def scanboard(self):
		cellstoflip = []
		for x in range(len(self.board)):
			for y in range(len(self.board)):
				neighbours = {
				'topleft':False,
				'top':False,
				'topright':False,
				'left':False,
				'right':False,
				'botleft':False,
				'bot':False,
				'botright':False
				}

				if x - 1 >= 0 and y - 1 >= 0:
					neighbours['topleft'] = self.board[x - 1][y - 1]
					
				if x - 1 >= 0:
					neighbours['top'] = self.board[x - 1][y]
					
				if x - 1 >= 0 and y  < len(self.board) - 1:
					neighbours['topright'] = self.board[x - 1][y + 1]
					
				if y - 1 >= 0:
					neighbours['left'] = self.board[x][y - 1]
					
				if y < len(self.board) - 1:
					neighbours['right'] = self.board[x][y + 1]
					
				if x < len(self.board) - 1 and y > 0:
					neighbours['botleft'] = self.board[x + 1][y - 1]
					
				if x < len(self.board) - 1:
					neighbours['bot'] = self.board[x + 1][y]
					
				if x < len(self.board) - 1 and y < len(self.board) - 1:
					neighbours['botright'] = self.board[x + 1][y + 1]
					
				livecount = 0
				for neighbour in neighbours:
					if neighbours[neighbour]:
						if neighbours[neighbour] == self.livecell:
							livecount += 1

				if livecount < 2 and self.board[x][y] == self.livecell:
					cellstoflip.insert(0,(x,y))
					
				if livecount > 3 and self.board[x][y] == self.livecell:
					cellstoflip.insert(0,(x,y))
					
				if livecount == 3 and self.board[x][y] == self.deadcell:
					cellstoflip.insert(0,(x,y))
		
		for i in cellstoflip:
			self.board[i[0]][i[1]] = self.flip(self.board[i[0]][i[1]])
			
def main(): #-b -c -s -d -a
	try:
		args = ' '.join(sys.argv[1:]).split()
		optlist, args = getopt.getopt(args, 'b:g:s:d:a:')
		
		for flags in optlist:
			if flags[0] == '-b':
				boardsize = int(flags[1])
			if flags[0] == '-g':
				generations = int(flags[1])
			if flags[0] == '-s':
				speed = float(flags[1])
			if flags[0]== '-d':
				deadcell = flags[1]
			if flags[0] == '-a':
				alivecell = flags[1]
				
		game = newgame(boardsize,alivecell,deadcell)
		print optlist
		for arg in args:
			alive = arg.split(',')
			game.board[int(alive[0])][int(alive[1])] = alivecell
			
		for i in range(generations):
			game.printboard()
			print 'Generation: ' + str(i + 1)
			time.sleep(speed)
			game.scanboard()
			
	except (ValueError, UnboundLocalError) as e:
		print ''
		print 'Options are: '
		print ''
		print '-b the board will be this size squared'
		print '-g the amount of generations'
		print '-s the amount of time to wait between generations'
		print '-d the character which represents dead cells'
		print '-a the character which represents alive cells'
		print ''
		print 'Example: gol.py -b 10 -g 60 -s 0.2 -d . -a @ 0,1 1,2 2,0 2,1 2,2'
		
		
if __name__ == '__main__':
	main()
