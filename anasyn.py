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
	
	
class CodeGenerator(object):
	grotablo=[]
	identifierTable=[]
	identifierTableTemp=[]
	piletra=[]
	piletze=[]
	compteurligne=0

	@staticmethod
	def add_identifierTable(bula):
		CodeGenerator.identifierTable.append(bula)
		
	@staticmethod
	def add_identifierTableTemp(bula):
		CodeGenerator.identifierTableTemp.append(bula)
		
	@staticmethod	
	def raz_identifierTableTemp():
		CodeGenerator.identifierTableTemp=[]
		
	@staticmethod	
	def set_type_identifierTableTemp(ty):
		for i in CodeGenerator.identifierTableTemp:
			i.append(ty)
			
	@staticmethod		
	def concat():
		CodeGenerator.identifierTable+=CodeGenerator.identifierTableTemp
		CodeGenerator.identifierTableTemp=[]

	@staticmethod
	def	getindex(ident):
		for i,[x,y] in enumerate(CodeGenerator.identifierTable):
			if x==ident:
				return i
				
	@staticmethod
	def ecriretra():
		i=CodeGenerator.piletra.pop()
		CodeGenerator.grotablo.append('tra('+str(i)+')')
		CodeGenerator.compteurligne+=1
		
	@staticmethod
	def reecriretra():
		i=CodeGenerator.piletra.pop()
		CodeGenerator.grotablo[i]='tra('+str(CodeGenerator.compteurligne)+')'
		
	@staticmethod
	def reecriretze():
		i=CodeGenerator.piletze.pop()
		CodeGenerator.grotablo[i]='tze('+str(CodeGenerator.compteurligne)+')'
		


########################################################################				 	
#### Syntactical Diagrams
########################################################################				 	

def program(lexical_analyser):

	CodeGenerator.grotablo.append('debutProg()')###################################################    'debutProg()'
	CodeGenerator.compteurligne+=1
	specifProgPrinc(lexical_analyser)
	lexical_analyser.acceptKeyword("is")
	corpsProgPrinc(lexical_analyser)
	
	CodeGenerator.grotablo.append('finProg()')###################################################    'finProg()'
	CodeGenerator.compteurligne+=1
	
def specifProgPrinc(lexical_analyser):
	lexical_analyser.acceptKeyword("procedure")
	ident = lexical_analyser.acceptIdentifier()
	logger.debug("Name of program : "+ident)
	
def  corpsProgPrinc(lexical_analyser):
	if not lexical_analyser.isKeyword("begin"):
		logger.debug("Parsing declarations")
		partieDecla(lexical_analyser)
		logger.debug("End of declarations")
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
                if not lexical_analyser.isKeyword("begin"):
                        listeDeclaVar(lexical_analyser)
        
        else:
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
	ident = lexical_analyser.acceptIdentifier()
	logger.debug("Name of procedure : "+ident)
	
	partieFormelle(lexical_analyser)

	lexical_analyser.acceptKeyword("is")
	corpsProc(lexical_analyser)
	

def fonction(lexical_analyser):
	lexical_analyser.acceptKeyword("function")
	ident = lexical_analyser.acceptIdentifier()
	logger.debug("Name of function : "+ident)
	
        partieFormelle(lexical_analyser)

	lexical_analyser.acceptKeyword("return")
	nnpType(lexical_analyser)
        
	lexical_analyser.acceptKeyword("is")
	corpsFonct(lexical_analyser)

def corpsProc(lexical_analyser):
	if not lexical_analyser.isKeyword("begin"):
		partieDeclaProc(lexical_analyser)
	lexical_analyser.acceptKeyword("begin")
	suiteInstr(lexical_analyser)
	lexical_analyser.acceptKeyword("end")

def corpsFonct(lexical_analyser):
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
		CodeGenerator.set_type_identifierTableTemp('integer')
		
	elif lexical_analyser.isKeyword("boolean"):
		lexical_analyser.acceptKeyword("boolean")
		logger.debug("boolean type")
		
		########################################
		CodeGenerator.set_type_identifierTableTemp('boolean')
		
	else:
		logger.error("Unknown type found <"+ lexical_analyser.get_value() +">!")
		raise AnaSynException("Unknown type found <"+ lexical_analyser.get_value() +">!")
	
	############################################		
	CodeGenerator.concat()

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
	
	CodeGenerator.grotablo.append('reserver('+str(len(CodeGenerator.identifierTable))+')')###################################################    'reserver(n)'
	CodeGenerator.compteurligne+=1

def listeIdent(lexical_analyser):
	ident = lexical_analyser.acceptIdentifier()
	logger.debug("identifier found: "+str(ident))

	##############################################on ajoute l'identifiant a la table des identifiants
	CodeGenerator.add_identifierTableTemp([ident])
	

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
		CodeGenerator.grotablo.append('get()')###################################################    'get()'
		CodeGenerator.compteurligne+=1
	
	elif lexical_analyser.isKeyword("put"):
		es(lexical_analyser)
		CodeGenerator.grotablo.append('put()')###################################################    'put()'
		CodeGenerator.compteurligne+=1
		
	elif lexical_analyser.isKeyword("return"):
		retour(lexical_analyser)
	elif lexical_analyser.isIdentifier():
		ident = lexical_analyser.acceptIdentifier()
		
		
		
		if lexical_analyser.isSymbol(":="):				
			# affectation
			CodeGenerator.grotablo.append('empiler('+str(CodeGenerator.getindex(ident))+')')###################################################    'empiler(ad(ident))'
			CodeGenerator.compteurligne+=1
			lexical_analyser.acceptSymbol(":=")
                        expression(lexical_analyser)
			logger.debug("parsed affectation")
			CodeGenerator.grotablo.append('affectation()')###################################################    'affectation()'
			CodeGenerator.compteurligne+=1
			
			
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
		exp1(lexical_analyser)
		CodeGenerator.grotablo.append('ou()')###################################################    'ou()'
		CodeGenerator.compteurligne+=1
        
def exp1(lexical_analyser):
	logger.debug("parsing exp1")
	
        exp2(lexical_analyser)
	if lexical_analyser.isKeyword("and"):
		lexical_analyser.acceptKeyword("and")
		exp2(lexical_analyser)
		CodeGenerator.grotablo.append('et()')###################################################    'et()'
		CodeGenerator.compteurligne+=1
        
def exp2(lexical_analyser):#### a recheck la grammaire si exp2:=exp3 < exp3 | exp3 et pas ex2 < exp3|exp3 -> faux prog modif en copnsequence
	logger.debug("parsing exp2")
        
	exp3(lexical_analyser)
	if	lexical_analyser.isSymbol("<"):
		opRel(lexical_analyser)
		exp2(lexical_analyser)
		CodeGenerator.grotablo.append('inf()')###################################################    'inf()'
		CodeGenerator.compteurligne+=1
		
	elif lexical_analyser.isSymbol("<="):
		opRel(lexical_analyser)
		exp2(lexical_analyser)
		CodeGenerator.grotablo.append('infeg()')###################################################    'infeg()'
		CodeGenerator.compteurligne+=1
		
	elif lexical_analyser.isSymbol(">"):
		opRel(lexical_analyser)
		exp2(lexical_analyser)
		CodeGenerator.grotablo.append('sup()')###################################################    'sup()'
		CodeGenerator.compteurligne+=1
		
	elif lexical_analyser.isSymbol(">="):
		opRel(lexical_analyser)
		exp2(lexical_analyser)
		CodeGenerator.grotablo.append('supeg()')###################################################    'supeg()'
		CodeGenerator.compteurligne+=1
		
	elif lexical_analyser.isSymbol("="):
		opRel(lexical_analyser)
		exp2(lexical_analyser)
		CodeGenerator.grotablo.append('egal()')###################################################    'egal()'
		CodeGenerator.compteurligne+=1
		
	elif lexical_analyser.isSymbol("/="): 
		opRel(lexical_analyser)
		exp2(lexical_analyser)
		CodeGenerator.grotablo.append('diff()')###################################################    'diff()'
		CodeGenerator.compteurligne+=1
	
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
		CodeGenerator.grotablo.append('add()')###################################################    'add()'
		CodeGenerator.compteurligne+=1
		
	elif lexical_analyser.isCharacter("-"):
		opAdd(lexical_analyser)
		exp3(lexical_analyser)###########################################################################originelement exp4 mais pas de sens ! cf grammaire
		CodeGenerator.grotablo.append('sous()')###################################################    'sous()'
		CodeGenerator.compteurligne+=1
		
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
		CodeGenerator.grotablo.append('mult()')###################################################    'mult()'
		CodeGenerator.compteurligne+=1
		
	elif lexical_analyser.isCharacter("/"):
		opMult(lexical_analyser)
		exp4(lexical_analyser)###########################################################################originelement prim mais pas de sens ! cf grammaire
		CodeGenerator.grotablo.append('div()')###################################################    'div()'
		CodeGenerator.compteurligne+=1
		
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
	elif lexical_analyser.isCharacter("-"):
		opUnaire(lexical_analyser)
		elemPrim(lexical_analyser)
		CodeGenerator.grotablo.append('moins()')###################################################    'moins()'
		CodeGenerator.compteurligne+=1
		
	elif lexical_analyser.isKeyword("not"):
		opUnaire(lexical_analyser)
		elemPrim(lexical_analyser)
		CodeGenerator.grotablo.append('non()')###################################################    'non()'
		CodeGenerator.compteurligne+=1
		
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
			CodeGenerator.grotablo.append('empiler('+str(CodeGenerator.getindex(ident))+')')###################################################    'empiler(ad(ident))'
			CodeGenerator.compteurligne+=1
			CodeGenerator.grotablo.append('valeurPile()')###################################################    'valeurPile()'
			CodeGenerator.compteurligne+=1
			
	else:
		logger.error("Unknown Value!")
		raise AnaSynException("Unknown Value!")

def valeur(lexical_analyser):
	if lexical_analyser.isInteger():
		entier = lexical_analyser.acceptInteger()
		logger.debug("integer value: " + str(entier))
		
		CodeGenerator.grotablo.append('empiler('+str(entier)+')')###################################################    'empiler(entier)'
		CodeGenerator.compteurligne+=1
		
                return "integer"
	elif lexical_analyser.isKeyword("true"):
		
		CodeGenerator.grotablo.append('empiler(true)')###################################################    'empiler(true)'
		CodeGenerator.compteurligne+=1
		vtype = valBool(lexical_analyser)
                return vtype
	
	elif lexical_analyser.isKeyword("false"):
		
		CodeGenerator.grotablo.append('empiler(false)')###################################################    'empiler(false)'
		CodeGenerator.compteurligne+=1
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
	CodeGenerator.piletra.append(CodeGenerator.compteurligne)

	expression(lexical_analyser) #### {C}

	CodeGenerator.grotablo.append('tze(vide)')###################################################    'tze(ad2)' /!\attention
	CodeGenerator.piletze.append(CodeGenerator.compteurligne)
	CodeGenerator.compteurligne+=1

	lexical_analyser.acceptKeyword("loop")
	suiteInstr(lexical_analyser) ### {A}


	CodeGenerator.ecriretra()###################################################    'tra(ad1)'
	

	##reecriture de tze avec ad2
	CodeGenerator.reecriretze()
	
	lexical_analyser.acceptKeyword("end")
	logger.debug("end of while loop ")





def altern(lexical_analyser):
	logger.debug("parsing if: ")
	lexical_analyser.acceptKeyword("if")

	expression(lexical_analyser) ### {C}
	
	CodeGenerator.grotablo.append('tze(vide)')###################################################    'tze(ad1)'
	CodeGenerator.piletze.append(CodeGenerator.compteurligne)
	CodeGenerator.compteurligne+=1	
	
	lexical_analyser.acceptKeyword("then")
	suiteInstr(lexical_analyser) ## {A}
	

	if lexical_analyser.isKeyword("else"):
		
		CodeGenerator.grotablo.append('tra(vide)')###################################################    'tra(ad2)'
		CodeGenerator.piletra.append(CodeGenerator.compteurligne)
		CodeGenerator.compteurligne+=1
	
		##reecriture de tze avec ad1
		CodeGenerator.reecriretze()
		
		lexical_analyser.acceptKeyword("else")
		suiteInstr(lexical_analyser) ###{B}
		
		##ecrire ad2
		CodeGenerator.reecriretra()
	
	else:#ya pas de else (trop lol)
		
		##reecriture de tze avec ad1
		CodeGenerator.reecriretze()
		
		
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
	program(lexical_analyser)
	
	

        if args.show_ident_table:
                print "------ IDENTIFIER TABLE ------"
                print str(CodeGenerator.identifierTable)
                print "------ END OF IDENTIFIER TABLE ------"

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
        instrIndex = 0
        while instrIndex < len(CodeGenerator.grotablo):
        	output_file.write("%s\n" % str(CodeGenerator.grotablo[instrIndex]))
		instrIndex += 1
		
        if outputFilename != "":
                output_file.close() 

########################################################################				 

if __name__ == "__main__":
	main() 

