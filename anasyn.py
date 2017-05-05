#!/usr/bin/python

## 	@package anasyn
# 	Syntactical Analyser package. 
#

import sys, argparse, re
import logging
import pprint

import analex

logger = logging.getLogger('anasyn')

DEBUG = False
LOGGING_LEVEL = logging.DEBUG


class AnaSynException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
                return repr(self.value)

class ArrayCodeGenerator(object):
	petitablo=[]
	indicecourant=-1
	courant=None
	compteurligne=0
	
	
	@staticmethod
	def ajoutNNA():	
		ArrayCodeGenerator.petitablo.append(CodeGenerator(ArrayCodeGenerator.indicecourant))
		ArrayCodeGenerator.indicecourant+=1
		ArrayCodeGenerator.courant=ArrayCodeGenerator.petitablo[ArrayCodeGenerator.indicecourant]



class CodeGenerator:
	grotablo=None
	identifierTable=None
	identifierTableTemp=None
	piletra=None
	piletze=None
	pileType=None
	scope=None
	ident=None

	def __init__(self,lolu):
		self.scope=lolu
		self.grotablo=[]
		self.identifierTable=[]
		self.identifierTableTemp=[]
		self.piletra=[]
		self.piletze=[]
		self.pileType=[]
	

	def ecrire(self,mot):
	       	self.grotablo.append(mot)
		ArrayCodeGenerator.compteurligne+=1
		
		

	def add_identifierTable(self,bula):
		self.identifierTable.append(bula)
		

	def add_identifierTableTemp(self,bula):
		self.identifierTableTemp.append(bula)
		
	
	def raz_identifierTableTemp(self):
		self.identifierTableTemp=[]
		

	def set_type_identifierTableTemp(self,ty):
		for i in self.identifierTableTemp:
			i.append(ty)
			
	
	def concat(self):
		self.identifierTable+=self.identifierTableTemp

	
	def getindex(self,ident):
		for i,[x,y] in enumerate(self.identifierTable):
			if x==ident:
				return i

		for i in ArrayCodeGenerator.petitablo:
			print "------ IDENTIFIER TABLE ------"
			print str(i.identifierTable)
			print "------ END OF IDENTIFIER TABLE ------"


		assert False,"verboten identifiant \""+ident+"\" non declare at ligne 50 !"
		

	def gettype(self,ident):
		for [x,y] in self.identifierTable:
			if x==ident:
				return y
			

	def ecriretra(self):
		i=self.piletra.pop()
		self.ecrire('tra('+str(i)+')')
		
	
	def reecriretra(self):
		i=self.piletra.pop()
		self.grotablo[i]='tra('+str(ArrayCodeGenerator.compteurligne)+')'
		

	def reecriretze(self):
		i=self.piletze.pop()
		self.grotablo[i]='tze('+str(ArrayCodeGenerator.compteurligne)+')'
		

	def verifegalType(self):
		print "verifeagltype"+str(self.pileType)
		b=self.pileType.pop()
		a=self.pileType.pop()
		if(a!=b):
			assert False,"verboten type "+b+" found but type "+a+" expected ! at ligne 3"
	

	def verifopBin(self,var):
		print "verifopBin"+str(self.pileType)
		b=self.pileType.pop()
		a=self.pileType.pop()
		if(a!= var or b!=var):
			assert False,"verboten type "+var+" expected ! at ligne 3"

	def verifopUn(self,var):
		print "verifopUn"+str(self.pileType)
		a=self.pileType.pop()
		if(a!= var):
			assert False,"verboten type "+var+" expected ! at ligne 3"
	
		


########################################################################				 	
#### Syntactical Diagrams
########################################################################				 	

def program(lexical_analyser):

	ArrayCodeGenerator.courant.ecrire('debutProg()')###################################################    'debutProg()'
	
	specifProgPrinc(lexical_analyser)
	lexical_analyser.acceptKeyword("is")
	corpsProgPrinc(lexical_analyser)
	
	ArrayCodeGenerator.courant.ecrire('finProg()')###################################################    'finProg()'
	
	
def specifProgPrinc(lexical_analyser):

	ArrayCodeGenerator.courant.piletra.append(ArrayCodeGenerator.compteurligne)
	ArrayCodeGenerator.courant.ecrire('tra(vide)')###################################################    'tra(fin de declaration des blocs NNA)'


	lexical_analyser.acceptKeyword("procedure")
	ident = lexical_analyser.acceptIdentifier()
	logger.debug("Name of program : "+ident)
	
def  corpsProgPrinc(lexical_analyser):##########################################################################################################################################################
	if not lexical_analyser.isKeyword("begin"):
		logger.debug("Parsing declarations")
		partieDecla(lexical_analyser)
		logger.debug("End of declarations")

	else:
		i=ArrayCodeGenerator.petitablo[0].piletra.pop()
		ArrayCodeGenerator.petitablo[0].grotablo[i]='tra('+str(ArrayCodeGenerator.compteurligne)+')'
		ArrayCodeGenerator.ajoutNNA()
		#################attention re-ecrire le tra, si pas de partie declarative

	lexical_analyser.acceptKeyword("begin")

	if not lexical_analyser.isKeyword("end"):
		logger.debug("Parsing instructions")
		suiteInstr(lexical_analyser)
		logger.debug("End of instructions")
		
	lexical_analyser.acceptKeyword("end")
	lexical_analyser.acceptFel()
	logger.debug("End of program")
	
def partieDecla(lexical_analyser):
        if lexical_analyser.isKeyword("procedure") or lexical_analyser.isKeyword("function") :
                listeDeclaOp(lexical_analyser)
		
		i=ArrayCodeGenerator.petitablo[0].piletra.pop()
		ArrayCodeGenerator.petitablo[0].grotablo[i]='tra('+str(ArrayCodeGenerator.compteurligne)+')'
		ArrayCodeGenerator.ajoutNNA()
		#######################re-ecriture du 1er tra !
		if not lexical_analyser.isKeyword("begin"):
			listeDeclaVar(lexical_analyser)
        
        else:
		i=ArrayCodeGenerator.petitablo[0].piletra.pop()
		ArrayCodeGenerator.petitablo[0].grotablo[i]='tra('+str(ArrayCodeGenerator.compteurligne)+')'
		###########################################################################re-ecriture du premier tra !
		ArrayCodeGenerator.ajoutNNA()
                listeDeclaVar(lexical_analyser)                

def listeDeclaOp(lexical_analyser):
	declaOp(lexical_analyser)
	lexical_analyser.acceptCharacter(";")
	if lexical_analyser.isKeyword("procedure") or lexical_analyser.isKeyword("function") :
		listeDeclaOp(lexical_analyser)

def declaOp(lexical_analyser):
	if lexical_analyser.isKeyword("procedure"):
		procedure(lexical_analyser)
	if lexical_analyser.isKeyword("function"):
		fonction(lexical_analyser)

def procedure(lexical_analyser):
	lexical_analyser.acceptKeyword("procedure")
	#############################################creation bloc NNA pour procedure !
	
	ArrayCodeGenerator.ajoutNNA()
	
	ident = lexical_analyser.acceptIdentifier()
	logger.debug("Name of procedure : "+ident)
	
	#############################################ajout ident a la table des identifiants global 
	
	partieFormelle(lexical_analyser)

	lexical_analyser.acceptKeyword("is")
	corpsProc(lexical_analyser)
	

def fonction(lexical_analyser):
	lexical_analyser.acceptKeyword("function")
	#############################################creation bloc NNA pour fonction !
	
	ArrayCodeGenerator.ajoutNNA()
	
	ident = lexical_analyser.acceptIdentifier()
	logger.debug("Name of function : "+ident)
	
	partieFormelle(lexical_analyser)

	lexical_analyser.acceptKeyword("return")
	nnpType(lexical_analyser)
        
	lexical_analyser.acceptKeyword("is")
	corpsFonct(lexical_analyser)

def corpsProc(lexical_analyser):##########################################################################################################################################################
	if not lexical_analyser.isKeyword("begin"):
		partieDeclaProc(lexical_analyser)
	lexical_analyser.acceptKeyword("begin")
	suiteInstr(lexical_analyser)
	lexical_analyser.acceptKeyword("end")

def corpsFonct(lexical_analyser):##########################################################################################################################################################
	if not lexical_analyser.isKeyword("begin"):
		partieDeclaProc(lexical_analyser)
	lexical_analyser.acceptKeyword("begin")
	suiteInstrNonVide(lexical_analyser)
	lexical_analyser.acceptKeyword("end")

def partieFormelle(lexical_analyser):
	lexical_analyser.acceptCharacter("(")
	if not lexical_analyser.isCharacter(")"):
		listeSpecifFormelles(lexical_analyser)
	lexical_analyser.acceptCharacter(")")

def listeSpecifFormelles(lexical_analyser):
	specif(lexical_analyser)
	if not lexical_analyser.isCharacter(")"):
		lexical_analyser.acceptCharacter(";")
		listeSpecifFormelles(lexical_analyser)

def specif(lexical_analyser):
	listeIdent(lexical_analyser)
	lexical_analyser.acceptCharacter(":")
	if lexical_analyser.isKeyword("in"):
		mode(lexical_analyser)
                
	nnpType(lexical_analyser)

def mode(lexical_analyser):
	lexical_analyser.acceptKeyword("in")
	if lexical_analyser.isKeyword("out"):
		lexical_analyser.acceptKeyword("out")
		logger.debug("in out parameter")                
	else:
		logger.debug("in parameter")

def nnpType(lexical_analyser):

	if lexical_analyser.isKeyword("integer"):
		lexical_analyser.acceptKeyword("integer")
		logger.debug("integer type")
		
		#########################################
		ArrayCodeGenerator.courant.set_type_identifierTableTemp('integer')
		
	elif lexical_analyser.isKeyword("boolean"):
		lexical_analyser.acceptKeyword("boolean")
		logger.debug("boolean type")
		
		########################################
		ArrayCodeGenerator.courant.set_type_identifierTableTemp('boolean')
		
	else:
		logger.error("Unknown type found <"+ lexical_analyser.get_value() +">!")
		raise AnaSynException("Unknown type found <"+ lexical_analyser.get_value() +">!")
	
	############################################		
	ArrayCodeGenerator.courant.concat()

def partieDeclaProc(lexical_analyser):
	listeDeclaVar(lexical_analyser)

def listeDeclaVar(lexical_analyser):
	declaVar(lexical_analyser)
	if lexical_analyser.isIdentifier():
		listeDeclaVar(lexical_analyser)

def declaVar(lexical_analyser):
	listeIdent(lexical_analyser)
	lexical_analyser.acceptCharacter(":")
	logger.debug("now parsing type...")
	nnpType(lexical_analyser)
	lexical_analyser.acceptCharacter(";")
	
	ArrayCodeGenerator.courant.ecrire('reserver('+str(len(ArrayCodeGenerator.courant.identifierTableTemp))+')')###################################################    'reserver(n)'
	
	
	ArrayCodeGenerator.courant.raz_identifierTableTemp()
	

def listeIdent(lexical_analyser):
	ident = lexical_analyser.acceptIdentifier()
	logger.debug("identifier found: "+str(ident))

	##############################################on ajoute l'identifiant a la table des identifiants
	
	ArrayCodeGenerator.courant.add_identifierTableTemp([ident])
	

	if lexical_analyser.isCharacter(","):
		lexical_analyser.acceptCharacter(",")
		listeIdent(lexical_analyser)

def suiteInstrNonVide(lexical_analyser):
	instr(lexical_analyser)
	if lexical_analyser.isCharacter(";"):
		lexical_analyser.acceptCharacter(";")
		suiteInstrNonVide(lexical_analyser)

def suiteInstr(lexical_analyser):
	if not lexical_analyser.isKeyword("end"):
		suiteInstrNonVide(lexical_analyser)

def instr(lexical_analyser):		
	if lexical_analyser.isKeyword("while"):
		boucle(lexical_analyser)
		
	elif lexical_analyser.isKeyword("if"):
		altern(lexical_analyser)
		
	elif lexical_analyser.isKeyword("get"):
		es(lexical_analyser)
		##transformer l'identifiant en son adresse

		ArrayCodeGenerator.courant.verifopUn('integer')

		ArrayCodeGenerator.courant.ecrire('get()')###################################################    'get()'
		
	
	elif lexical_analyser.isKeyword("put"):
		es(lexical_analyser)

		ArrayCodeGenerator.courant.verifopUn('integer')

		ArrayCodeGenerator.courant.ecrire('put()')###################################################    'put()'
		
		
	elif lexical_analyser.isKeyword("return"):
		retour(lexical_analyser)
	elif lexical_analyser.isIdentifier():
		ident = lexical_analyser.acceptIdentifier()
		
		
		
		if lexical_analyser.isSymbol(":="):
			
			print "empile "+ArrayCodeGenerator.courant.gettype(ident)+" a cause "+ident
			ArrayCodeGenerator.courant.pileType.append(ArrayCodeGenerator.courant.gettype(ident))
			
			# affectation
			ArrayCodeGenerator.courant.ecrire('empiler('+str(ArrayCodeGenerator.courant.getindex(ident))+')')###################################################    'empiler(ad(ident))'
			
			lexical_analyser.acceptSymbol(":=")
                        expression(lexical_analyser)
			logger.debug("parsed affectation")

			ArrayCodeGenerator.courant.verifegalType()

			ArrayCodeGenerator.courant.ecrire('affectation()')###################################################    'affectation()'
			
			
			
		elif lexical_analyser.isCharacter("("):
			lexical_analyser.acceptCharacter("(")
			if not lexical_analyser.isCharacter(")"):
				listePe(lexical_analyser)

			lexical_analyser.acceptCharacter(")")
			logger.debug("parsed procedure call")
		else:
			logger.error("Expecting procedure call or affectation, verboten !")
			raise AnaSynException("Expecting procedure call or affectation!")
		
	else:
		logger.error("Unknown Instruction <"+ lexical_analyser.get_value() +">!")
		raise AnaSynException("Unknown Instruction <"+ lexical_analyser.get_value() +">!")

def listePe(lexical_analyser):
	expression(lexical_analyser)
	if lexical_analyser.isCharacter(","):
		lexical_analyser.acceptCharacter(",")
		listePe(lexical_analyser)

def expression(lexical_analyser):
	logger.debug("parsing expression: " + str(lexical_analyser.get_value()))

	exp1(lexical_analyser)
	if lexical_analyser.isKeyword("or"):
		lexical_analyser.acceptKeyword("or")
		expression(lexical_analyser)

		ArrayCodeGenerator.courant.verifopBin('boolean')
		print "empile boolean apres \"or\""
		ArrayCodeGenerator.courant.pileType.append('boolean')
		
		ArrayCodeGenerator.courant.ecrire('ou()')###################################################    'ou()'
		
        
def exp1(lexical_analyser):
	logger.debug("parsing exp1")
	
        exp2(lexical_analyser)
	if lexical_analyser.isKeyword("and"):
		lexical_analyser.acceptKeyword("and")
		exp1(lexical_analyser)

		ArrayCodeGenerator.courant.verifopBin('boolean')
		print "empile boolean apres \"and\""
		ArrayCodeGenerator.courant.pileType.append('boolean')

		ArrayCodeGenerator.courant.ecrire('et()')###################################################    'et()'
		
        
def exp2(lexical_analyser):#### a recheck la grammaire si exp2:=exp3 < exp3 | exp3 et pas ex2 < exp3|exp3 -> faux prog modif en copnsequence
	logger.debug("parsing exp2")
        
	exp3(lexical_analyser)
	if	lexical_analyser.isSymbol("<"):
		opRel(lexical_analyser)
		exp2(lexical_analyser)

		ArrayCodeGenerator.courant.verifopBin('integer')
		print "empile boolean apres \"<\""
		ArrayCodeGenerator.courant.pileType.append('boolean')

		ArrayCodeGenerator.courant.ecrire('inf()')###################################################    'inf()'
		
		
	elif lexical_analyser.isSymbol("<="):
		opRel(lexical_analyser)
		exp2(lexical_analyser)

		ArrayCodeGenerator.courant.verifopBin('integer')
		print "empile boolean apres \"<=\""
		ArrayCodeGenerator.courant.pileType.append('boolean')

		ArrayCodeGenerator.courant.ecrire('infeg()')###################################################    'infeg()'
		
		
	elif lexical_analyser.isSymbol(">"):
		opRel(lexical_analyser)
		exp2(lexical_analyser)

		ArrayCodeGenerator.courant.verifopBin('integer')
		print "empile boolean apres \">\""
		ArrayCodeGenerator.courant.pileType.append('boolean')
		
		ArrayCodeGenerator.courant.ecrire('sup()')###################################################    'sup()'
		
		
	elif lexical_analyser.isSymbol(">="):
		opRel(lexical_analyser)
		exp2(lexical_analyser)

		ArrayCodeGenerator.courant.verifopBin('integer')
		print "empile boolean apres \">=\""
		ArrayCodeGenerator.courant.pileType.append('boolean')

		ArrayCodeGenerator.courant.ecrire('supeg()')###################################################    'supeg()'
		
		
	elif lexical_analyser.isSymbol("="):
		opRel(lexical_analyser)
		exp2(lexical_analyser)

		ArrayCodeGenerator.courant.verifegalType()
		print "empile boolean apres \"=\""
		ArrayCodeGenerator.courant.pileType.append('boolean')

		ArrayCodeGenerator.courant.ecrire('egal()')###################################################    'egal()'
		
		
	elif lexical_analyser.isSymbol("/="): 
		opRel(lexical_analyser)
		exp2(lexical_analyser)

		ArrayCodeGenerator.courant.verifegalType()
		print "empile boolean apres \"/=\""
		ArrayCodeGenerator.courant.pileType.append('boolean')

		ArrayCodeGenerator.courant.ecrire('diff()')###################################################    'diff()'
		
	
def opRel(lexical_analyser):
	logger.debug("parsing relationnal operator: " + lexical_analyser.get_value())
        
	if	lexical_analyser.isSymbol("<"):
		lexical_analyser.acceptSymbol("<")
        
	elif lexical_analyser.isSymbol("<="):
		lexical_analyser.acceptSymbol("<=")
        
	elif lexical_analyser.isSymbol(">"):
		lexical_analyser.acceptSymbol(">")
        
	elif lexical_analyser.isSymbol(">="):
		lexical_analyser.acceptSymbol(">=")
        
	elif lexical_analyser.isSymbol("="):
		lexical_analyser.acceptSymbol("=")
        
	elif lexical_analyser.isSymbol("/="):
		lexical_analyser.acceptSymbol("/=")
        
	else:
		msg = "Unknown relationnal operator <"+ lexical_analyser.get_value() +">!"
		logger.error(msg)
		raise AnaSynException(msg)

def exp3(lexical_analyser):
	logger.debug("parsing exp3")
	exp4(lexical_analyser)	
	if lexical_analyser.isCharacter("+"):
		opAdd(lexical_analyser)
		exp3(lexical_analyser)###########################################################################originelement exp4 mais pas de sens ! cf grammaire

		ArrayCodeGenerator.courant.verifopBin('integer')
		print "empile integer apres \"+\""
		ArrayCodeGenerator.courant.pileType.append('integer')

		ArrayCodeGenerator.courant.ecrire('add()')###################################################    'add()'
		
		
	elif lexical_analyser.isCharacter("-"):
		opAdd(lexical_analyser)
		exp3(lexical_analyser)###########################################################################originelement exp4 mais pas de sens ! cf grammaire

		ArrayCodeGenerator.courant.verifopBin('integer')
		print "empile integer apres \"-\""
		ArrayCodeGenerator.courant.pileType.append('integer')

		ArrayCodeGenerator.courant.ecrire('sous()')###################################################    'sous()'
		
		
def opAdd(lexical_analyser):
	logger.debug("parsing additive operator: " + lexical_analyser.get_value())
	if lexical_analyser.isCharacter("+"):
		lexical_analyser.acceptCharacter("+")
                
	elif lexical_analyser.isCharacter("-"):
		lexical_analyser.acceptCharacter("-")
                
	else:
		msg = "Unknown additive operator <"+ lexical_analyser.get_value() +">!"
		logger.error(msg)
		raise AnaSynException(msg)

def exp4(lexical_analyser):
	logger.debug("parsing exp4")
        
	prim(lexical_analyser)	
	if lexical_analyser.isCharacter("*"):
		opMult(lexical_analyser)
		exp4(lexical_analyser)###########################################################################originelement prim mais pas de sens ! cf grammaire

		ArrayCodeGenerator.courant.verifopBin('integer')
		print "empile integer apres \"*\""
		ArrayCodeGenerator.courant.pileType.append('integer')

		ArrayCodeGenerator.courant.ecrire('mult()')###################################################    'mult()'
		
		
	elif lexical_analyser.isCharacter("/"):
		opMult(lexical_analyser)
		exp4(lexical_analyser)###########################################################################originelement prim mais pas de sens ! cf grammaire

		ArrayCodeGenerator.courant.verifopBin('integer')
		print "empile integer apres \"/\""
		ArrayCodeGenerator.courant.pileType.append('integer')

		ArrayCodeGenerator.courant.ecrire('div()')###################################################    'div()'
		
		
def opMult(lexical_analyser):
	logger.debug("parsing multiplicative operator: " + lexical_analyser.get_value())
	if lexical_analyser.isCharacter("*"):
		lexical_analyser.acceptCharacter("*")
                
	elif lexical_analyser.isCharacter("/"):
		lexical_analyser.acceptCharacter("/")
                
	else:
		msg = "Unknown multiplicative operator <"+ lexical_analyser.get_value() +">!"
		logger.error(msg)
		raise AnaSynException(msg)

def prim(lexical_analyser):
	logger.debug("parsing prim")
        
	if lexical_analyser.isCharacter("+"):
		opUnaire(lexical_analyser)
		elemPrim(lexical_analyser)

		ArrayCodeGenerator.courant.verifopUn('integer')
		print "empile integer apres \"+\" unaire"
		ArrayCodeGenerator.courant.pileType.append('integer')

	elif lexical_analyser.isCharacter("-"):
		opUnaire(lexical_analyser)
		elemPrim(lexical_analyser)

		ArrayCodeGenerator.courant.verifopUn('integer')
		print "empile integer apres \"-\" unaire"
		ArrayCodeGenerator.courant.pileType.append('integer')

		ArrayCodeGenerator.courant.ecrire('moins()')###################################################    'moins()'
		
		
	elif lexical_analyser.isKeyword("not"):
		opUnaire(lexical_analyser)
		elemPrim(lexical_analyser)

		ArrayCodeGenerator.courant.verifopUn('boolean')
		print "empile boolean apres \"non\" unaire"
		ArrayCodeGenerator.courant.pileType.append('boolean')

		ArrayCodeGenerator.courant.ecrire('non()')###################################################    'non()'
		
		
	else:
		elemPrim(lexical_analyser)

def opUnaire(lexical_analyser):
	logger.debug("parsing unary operator: " + lexical_analyser.get_value())
	if lexical_analyser.isCharacter("+"):
		lexical_analyser.acceptCharacter("+")
                
	elif lexical_analyser.isCharacter("-"):
		lexical_analyser.acceptCharacter("-")
                
	elif lexical_analyser.isKeyword("not"):
		lexical_analyser.acceptKeyword("not")
                
	else:
		msg = "Unknown additive operator <"+ lexical_analyser.get_value() +">!"
		logger.error(msg)
		raise AnaSynException(msg)

def elemPrim(lexical_analyser):
	logger.debug("parsing elemPrim: " + str(lexical_analyser.get_value()))
	if lexical_analyser.isCharacter("("):
		lexical_analyser.acceptCharacter("(")
		expression(lexical_analyser)
		lexical_analyser.acceptCharacter(")")
	elif lexical_analyser.isInteger() or lexical_analyser.isKeyword("true") or lexical_analyser.isKeyword("false"):
		valeur(lexical_analyser)
	elif lexical_analyser.isIdentifier():
		ident = lexical_analyser.acceptIdentifier()



		if lexical_analyser.isCharacter("("):			# Appel fonct
			lexical_analyser.acceptCharacter("(")
			if not lexical_analyser.isCharacter(")"):
				listePe(lexical_analyser)

			lexical_analyser.acceptCharacter(")")
			logger.debug("parsed procedure call")

			logger.debug("Call to function: " + ident)
		else:
			logger.debug("Use of an identifier as an expression: " + ident)     

			ArrayCodeGenerator.courant.pileType.append(ArrayCodeGenerator.courant.gettype(ident))

			ArrayCodeGenerator.courant.ecrire('empiler('+str(ArrayCodeGenerator.courant.getindex(ident))+')')###################################################    'empiler(ad(ident))'
			
			ArrayCodeGenerator.courant.ecrire('valeurPile()')###################################################    'valeurPile()'
			
			
	else:
		logger.error("Unknown Value!")
		raise AnaSynException("Unknown Value!")

def valeur(lexical_analyser):
	if lexical_analyser.isInteger():
		entier = lexical_analyser.acceptInteger()
		logger.debug("integer value: " + str(entier))
		
		print "empile integer apres "+str(entier)
		ArrayCodeGenerator.courant.pileType.append('integer')

		ArrayCodeGenerator.courant.ecrire('empiler('+str(entier)+')')###################################################    'empiler(entier)'
		
		
                return "integer"
	elif lexical_analyser.isKeyword("true"):

		print "empile boolean apres true"
		ArrayCodeGenerator.courant.pileType.append('boolean')

		ArrayCodeGenerator.courant.ecrire('empiler(true)')###################################################    'empiler(true)'
		
		vtype = valBool(lexical_analyser)
                return vtype
	
	elif lexical_analyser.isKeyword("false"):
		
		print "empile boolean apres fasle"
		ArrayCodeGenerator.courant.pileType.append('boolean')

		ArrayCodeGenerator.courant.ecrire('empiler(false)')###################################################    'empiler(false)'
		
		vtype = valBool(lexical_analyser)
                return vtype
	else:
		logger.error("Unknown Value! Expecting an integer or a boolean value!")
		raise AnaSynException("Unknown Value ! Expecting an integer or a boolean value!")

def valBool(lexical_analyser):
	if lexical_analyser.isKeyword("true"):
		lexical_analyser.acceptKeyword("true")	
		logger.debug("boolean true value")
                
	else:
		logger.debug("boolean false value")
		lexical_analyser.acceptKeyword("false")	
                
        return "boolean"

def es(lexical_analyser):
	logger.debug("parsing E/S instruction: " + lexical_analyser.get_value())
	if lexical_analyser.isKeyword("get"):
		lexical_analyser.acceptKeyword("get")
		lexical_analyser.acceptCharacter("(")
		ident = lexical_analyser.acceptIdentifier()
		ArrayCodeGenerator.courant.ecrire('empiler('+str(ArrayCodeGenerator.courant.getindex(ident))+')')#####################################empiler ad(ident)
		
		print "empile "+ArrayCodeGenerator.courant.gettype(ident)+" apres "+ident
		ArrayCodeGenerator.courant.pileType.append(ArrayCodeGenerator.courant.gettype(ident))
		
		
		lexical_analyser.acceptCharacter(")")
		logger.debug("Call to get "+ident)
	elif lexical_analyser.isKeyword("put"):
		lexical_analyser.acceptKeyword("put")
		lexical_analyser.acceptCharacter("(")
		expression(lexical_analyser)
		lexical_analyser.acceptCharacter(")")
		logger.debug("Call to put")
	else:
		logger.error("Unknown E/S instruction!")
		raise AnaSynException("Unknown E/S instruction!")

def boucle(lexical_analyser):
	logger.debug("parsing while loop: ")
	
	
	lexical_analyser.acceptKeyword("while")

	###ecrire ad1
	ArrayCodeGenerator.courant.piletra.append(ArrayCodeGenerator.compteurligne)

	expression(lexical_analyser) #### {C}

	ArrayCodeGenerator.courant.verifopUn("boolean")

	ArrayCodeGenerator.courant.ecrire('tze(vide)')###################################################    'tze(ad2)' /!\attention
	ArrayCodeGenerator.courant.piletze.append(ArrayCodeGenerator.compteurligne)
	

	lexical_analyser.acceptKeyword("loop")
	suiteInstr(lexical_analyser) ### {A}


	ArrayCodeGenerator.courant.ecriretra()###################################################    'tra(ad1)'
	

	##reecriture de tze avec ad2
	ArrayCodeGenerator.courant.reecriretze()
	
	lexical_analyser.acceptKeyword("end")
	logger.debug("end of while loop ")





def altern(lexical_analyser):
	logger.debug("parsing if: ")
	lexical_analyser.acceptKeyword("if")

	expression(lexical_analyser) ### {C}

	ArrayCodeGenerator.courant.verifopUn("boolean")
	
	ArrayCodeGenerator.courant.ecrire('tze(vide)')###################################################    'tze(ad1)'
	ArrayCodeGenerator.courant.piletze.append(ArrayCodeGenerator.compteurligne)
	
	
	lexical_analyser.acceptKeyword("then")
	suiteInstr(lexical_analyser) ## {A}
	

	if lexical_analyser.isKeyword("else"):
		
		ArrayCodeGenerator.courant.ecrire('tra(vide)')###################################################    'tra(ad2)'
		ArrayCodeGenerator.courant.piletra.append(ArrayCodeGenerator.compteurligne)
		
	
		##reecriture de tze avec ad1
		ArrayCodeGenerator.courant.reecriretze()
		
		lexical_analyser.acceptKeyword("else")
		suiteInstr(lexical_analyser) ###{B}
		
		##ecrire ad2
		ArrayCodeGenerator.courant.reecriretra()
	
	else:#ya pas de else (trop lol)
		
		##reecriture de tze avec ad1
		ArrayCodeGenerator.courant.reecriretze()
		
		
	lexical_analyser.acceptKeyword("end")
	logger.debug("end of if")
	

def retour(lexical_analyser):
	logger.debug("parsing return instruction")
	lexical_analyser.acceptKeyword("return")
	expression(lexical_analyser)

	

########################################################################				 	
def main():

 	
	parser = argparse.ArgumentParser(description='Do the syntactical analysis of a NNP program.')
	parser.add_argument('inputfile', type=str, nargs=1, help='name of the input source file')
	parser.add_argument('-o', '--outputfile', dest='outputfile', action='store', \
				    default="", help='name of the output file (default: stdout)')
	parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
	parser.add_argument('-d', '--debug', action='store_const', const=logging.DEBUG, \
				    default=logging.INFO, help='show debugging info on output')
        parser.add_argument('-p', '--pseudo-code', action='store_const', const=True, default=False, \
				    help='enables output of pseudo-code instead of assembly code')
        parser.add_argument('--show-ident-table', action='store_true', \
				    help='shows the final identifiers table')
	args = parser.parse_args()

	filename = args.inputfile[0]
	f = None
	try:
		f = open(filename, 'r')
	except:
		print "Error: can\'t open input file!"
		return
	
	outputFilename = args.outputfile
	
  	# create logger      
        LOGGING_LEVEL = args.debug
	logger.setLevel(LOGGING_LEVEL)
	ch = logging.StreamHandler()
	ch.setLevel(LOGGING_LEVEL)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	ch.setFormatter(formatter)
	logger.addHandler(ch)


	# Init
	identifierTable=[]
	identifierTableTemp=[]
	tabInstruction=[]


        if args.pseudo_code:
                True#?
        else:
                True#?

	lexical_analyser = analex.LexicalAnalyser()
	
	lineIndex = 0
	for line in f:
		line = line.rstrip('\r\n')
		lexical_analyser.analyse_line(lineIndex, line)
		lineIndex = lineIndex + 1
	f.close()
	

	# launch the analysis of the program
	lexical_analyser.init_analyser()

	ArrayCodeGenerator.ajoutNNA()
	program(lexical_analyser)
	
	

        if args.show_ident_table:
		for i in ArrayCodeGenerator.petitablo:
			print "------ IDENTIFIER TABLE ------"
			print str(i.identifierTable)
			print "------ END OF IDENTIFIER TABLE ------"

		print "------ TableType ------"
		print str(ArrayCodeGenerator.courant.pileType)
		print "------           ------"

	#pprint.pprint(args)
	

        if outputFilename != "":
                try:
                        output_file = open(outputFilename, 'w')
                except:
                        print "Error: can\'t open output file!"
                        return
        else:
                output_file = sys.stdout

	
	
	
	# Outputs the generated code to a file
       	for i in ArrayCodeGenerator.petitablo:
		instrIndex = 0
      		while instrIndex < len(i.grotablo):
		
			output_file.write("%s\n" % str(i.grotablo[instrIndex]))
			instrIndex += 1


        if outputFilename != "":
                output_file.close() 

########################################################################				 

if __name__ == "__main__":
	main() 

