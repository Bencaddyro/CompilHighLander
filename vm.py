def openTab(file):
    f=open(file,'r')
    lines=f.readlines()
    f.close
    for i in range(len(lines)):
        lines[i]=lines[i].rstrip('\n')
    return lines

def test():
	maPile=Pile()
	maPile.empiler(2)
	maPile.empiler(0)
	maPile.affiche()
	print("premiere pile")
	maPile.empiler(0)
	maPile.empiler(5)
	print("avant affectation")
	maPile.affiche()
	print("apres affection")
	maPile.affectation()
	maPile.affiche()
	maPile.valeurPile()
	print("apres valeurPile")
	maPile.affiche()


def executer(file):
	i=0
	pile=Pile()
	lines=openTab(file)
	while pile.CO<len(lines):
		execline(lines[pile.CO],pile,pile.CO)
		pile.affiche()
		i+=1
		##pile.affiche()
		##i=temp

##__________________LE__SWITCH__DE__L'EXTREME________________________________________________________


def execline(instr,pile,i):
	print instr
	if len(instr)>=11 and instr[0:9]=='debutProg':
		pile.debutProg()
		
	elif len(instr)>=9 and instr[0:7]=='finProg':
		pile.finProg()
		
	elif len(instr)>=11 and instr[0:8]=='reserver' and instr[8]!='B':
		nb=instr.rstrip(')')
		nb=nb.lstrip('reserver(')
		pile.reserver(int(nb))
		##return i+1
	
	elif len(instr)>=10 and instr[0:7]=='empiler' and instr[7]!= 'A' and instr[7]!= 'P':
		nb=instr.rstrip(')')
		nb=nb.lstrip('empiler(')
		pile.empiler(int(nb))
		##return i+1
	
	elif len(instr)>=12 and instr[0:9]=='empilerAd':
		nb=instr.rstrip(')')
		nb=nb.lstrip('empilerAd(')
		pile.empilerAd(int(nb))
		##return i+1
		
		
	elif len(instr)>=13 and instr[0:11]=='affectation':
		pile.affectation()
		##return i+1
	
	elif len(instr)==12 and instr[0:10]=='valeurPile':
		pile.valeurPile()
		##return i+1
		
	elif len(instr)==5 and instr[0:3]=='get':
		pile.get()
		##return i+1	
		
	elif len(instr)>=5 and instr[0:3]=='put':
		pile.put()
		##return i+1
		
	elif len(instr)==7 and instr[0:5]=='moins':
		pile.moins()
		##return i+1

	elif len(instr)==6 and instr[0:4]=='sous':
		pile.sous()
		##return i+1
	
	elif len(instr)==5 and instr[0:3]=='add':
		pile.add()
		##return i+1
		
	elif len(instr)==6 and instr[0:4]=='mult':
		pile.mult()
		##return i+1
		
	elif len(instr)==5 and instr[0:3]=='div':
		pile.div()
		##return i+1
	
	elif len(instr)==6 and instr[0:4]=='egal':
		pile.egal()
		##return i+1
		
	elif len(instr)==6 and instr[0:4]=='diff':
		pile.diff()
		##return i+1
		
	elif len(instr)==5 and instr[0:3]=='inf':
		pile.inf()
		##return i+1
	
	elif len(instr)==7 and instr[0:5]=='infeg':
		pile.infeg()
		##return i+1
	
	elif len(instr)==5 and instr[0:3]=='sup':
		pile.sup()
		##return i+1
	
	elif len(instr)==7 and instr[0:5]=='supeg':
		pile.supeg()
		##return i+1

	elif len(instr)==4 and instr[0:2]=='et':
		pile.et()
		##return i+1
	
	elif len(instr)==4 and instr[0:2]=='ou':
		pile.ou()
		##return i+1
		
	elif len(instr)==5 and instr[0:3]=='non':
		pile.non()
		##return i+1

	elif len(instr)>=6 and instr[0:3]=='tra' and instr[3]!='S':
		nb=instr.rstrip(')')
		nb=nb.lstrip('tra(')
		pile.tra(int(nb))
		##return (int(nb)-1)

	elif len(instr)>=6 and instr[0:3]=='tze':
		nb=instr.rstrip(')')
		nb=nb.lstrip('tze(')
		test=pile.tze()
		if not test :
			pile.tra(int(nb))
			##return (int(nb)-1)
		else:
			pass
			##return i+1
		
		
	elif len(instr)==14 and instr[0:12]=='reserverBloc':
		pile.reserverBloc()
		##return i+1
		
	elif len(instr)==13 and instr[0:11]=='retourFonct':
		pile.retourFonct()
		##return i+1
	elif len(instr)==12 and instr[0:10]=='retourProc':
		pile.retourProc()
		##return i+1
		
	elif len(instr)>=15 and instr[0:12]=='empilerParam':
		nb=instr.rstrip(')')
		nb=nb.lstrip('empilerParam(')
		pile.empilerParam(int(nb))
		##return (int(nb)-1)
		
	elif len(instr)>=10 and instr[0:7]=='traStat':
		nb=instr.rstrip(')')
		nb=nb.lstrip('traStat(')
		pile.traStat(int(nb))
		##return (int(nb)-1)

		
		
##______________LA__TROP__BELLE__CLASSE__PILE______________________________________________	
	
class Pile:	

	stack = None
	IP = None
	base= None
	baseSuiv= None
	CO =None
	
	def __init__(self):
		self.stack = []
		self.IP=-1
		self.base=-1
		self.CO=0
		
		
	def affiche(self):
		print(self.stack)
		print self.base

	def debutProg(self):
		self.stack=[]
		self.IP=-1
		self.CO+=1
		
		
	def finProg(self):
		self.CO+=1	
		pass

	def reserver(self,n):
		for k in range(n):
			self.stack.append(0)
		self.IP=self.IP+n
		self.CO+=1
	
	def empiler(self,i):
		self.stack.append(i)
		self.IP=self.IP + 1
		self.CO+=1
	
	def empilerAd(self,i):
		self.empiler(i)
		self.valeurPile()
		self.CO-=1
		##IP=IP+1
		##stack[IP]=stack[stack[i]]
				
				
	def affectation(self):
		val=self.stack.pop()
		adr=self.stack.pop()
		self.stack[adr]=val
		self.IP=self.IP-2
		self.CO+=1
		
				
				
	def valeurPile(self):
		self.stack[self.IP]=self.stack[self.stack[self.IP]]
		self.CO+=1


	def get(self):
		arg=input("entrez l'argument   :  ")
		self.empiler(arg)

  
	def put(self):
		elt=self.stack.pop()
		print(elt)
		self.IP-=1
		self.CO+=1
		
	def moins(self):
		var = self.stack.pop()
		self.empiler(-(var))

		
	def sous(self):
		op1=self.stack.pop()
		op2=self.stack.pop()
		self.IP-=2
		self.empiler(op2-op1)

		
	def add(self):
		op1=self.stack.pop()
		op2=self.stack.pop()
		self.IP-=2
		self.empiler(op1+op2)

    
	def mult(self):
		op1=self.stack.pop()
		op2=self.stack.pop()
		self.IP-=2
		self.empiler(op1*op2)


	def div(self):
		op1=self.stack.pop()
		op2=self.stack.pop()
		self.IP-=2
		self.empiler(op2/op1)
   	
	
	def egal(self):
		op1=self.stack.pop()
		op2=self.stack.pop()
		self.IP-=2
		self.empiler(op1==op2)



	def diff(self):
		op1=self.stack.pop()
		op2=self.stack.pop()
		self.IP-=2
		self.empiler(op1!=op2)

		
	def inf(self):
		op1=self.stack.pop()
		op2=self.stack.pop()
		self.IP-=2
		self.empiler(op2<op1)
	
		
	def infeg(self):
		op1=self.stack.pop()
		op2=self.stack.pop()
		self.IP-=2
		self.empiler(op2<=op1)
	
		
	def sup(self):
		op1=self.stack.pop()
		op2=self.stack.pop()
		self.IP-=2
		self.empiler(op2>op1)

		
	def supeg(self):
		op1=self.stack.pop()
		op2=self.stack.pop()
		self.IP-=2
		self.empiler(op2>=op1)
	
		
	def et(self):
		op1=self.stack.pop()
		op2=self.stack.pop()
		self.IP-=2
		self.empiler(op1 and op2)



	def ou(self):
		op1=self.stack.pop()
		op2=self.stack.pop()
		self.IP-=2
		self.empiler(op1 or op2)

		
	def non(self):
		op1=self.stack.pop()
		self.IP-=1
		self.empiler( not op1)

		
	def tra(self,i):
		self.CO=i-1
		
	def tze(self):
		op=self.stack.pop()
		self.IP-=1
		self.CO+=1
		return(op)
	
	def reserverBloc(self):
		self.empiler(self.base)
		self.CO-=1
		self.baseSuiv=self.IP
		self.empiler(0)
		self.CO-=1
		self.CO+=1
		
		
	def retourFonct(self):
		res=self.stack.pop()
		self.IP-=1
		while self.IP>(self.base+1):
			self.stack.pop()
			self.IP-=1
		nouvCO=self.stack.pop()
		self.IP-=1
		self.CO=nouvCO-1
		self.base=self.stack.pop()
		self.IP-=1
		self.empiler(res)
			
			
	def retourProc(self):
		while self.IP>(self.base+1):
			self.stack.pop()
			self.IP-=1
		nouvCO=self.stack.pop()
		self.IP-=1
		self.CO=nouvCO-1
		self.base=self.stack.pop()
		self.IP-=1
	
	
	def empilerParam(self,i):
		##if self.base==-1:
		self.empiler(self.base+i+2)
		##else :			
			##self.empiler(self.stack[self.base]+i+2)
			
			
	def traStat(self,ad):
		self.base=self.baseSuiv
		self.stack[self.base+1]=self.CO+1
		self.tra(ad)
		
		
		
		
		
		
		
		
		
