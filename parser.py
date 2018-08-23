#!/usr/bin/python
#coding:utf-8
"""
LL(1) prediction analysis table
5151111910078 yangjunchen 
"""
#1.for an input grammar, tell the vt and vn
#2.intialize the table
#3.for each production A->α,calculate first(α), then scan the output, if vt, add to the table, if kong, calculate Follow(A)，add the table
#4.elimate the direct left recursion
import numpy as np
import re
#scan_grammar : input a file and distiguish the terminals,nterminals,productions
def scan_grammar(filename):
	file = open(filename,'r')
	production = []
	nterminals = []
	terminals = []
	rightparts = []
	for line in file.readlines():
		line = line.strip()
		production.append(line)
		nterminals.append(line.split('->')[0])
		rightparts.append(line.split('->')[1])
	nterminals = list(set(nterminals))
	for rightpart in rightparts:
		for i in rightpart:
			if i not in nterminals:
				terminals.append(i)
	terminals = list(set(terminals))
	terminals.append('$')
	if 'n' in terminals:
		terminals.remove('n')
	file.close()
	return terminals,nterminals,production

#table_allocate: add the production to the table
def table_allocate(terminals,nterminals,production):
	
	table = np.array([-1]*(len(terminals)*len(nterminals))).reshape(len(nterminals),len(terminals))
	for counter,prod in enumerate(production):
		output = First(prod.split('->')[0],terminals[:-1],nterminals, production)
		
		if 'n' not in output:
			for t_sig in output:
				if t_sig in terminals:
					table[nterminals.index(prod.split('->')[0])][terminals.index(t_sig)] = production.index(prod)
		else:
			follow_out = Follow(prod.split('->')[0],terminals[:-1],nterminals, production)
			
			for b in follow_out:
				table[nterminals.index(prod.split('->')[0])][terminals.index(b)] = production.index(prod)

	return table
#First: calculate the first(a)
def First(a,terminals,nterminals, production): 
	first = []
	if len(a) == 1:
		
		if a in terminals:
			first.append(a)
			return first
		else:
			for prod in production:
				if a+'->n' == prod:
					first.append('n')

				if a == prod.split('->')[0]:
					flag = 0
					for Y in prod.split('->')[1]:
						tmp = First(Y,terminals,nterminals,production)

						if 'n' not in tmp:
							for i in tmp:
								first.append(i)

							
							flag = 1
							break
						else:
							if len(tmp) != 1:
								
								tmp.remove('n')
								#print "ASfas"
								for i in tmp:
									first.append(i)
					if flag == 0:
						first.append('n')
			
			return list(set(first))
	else:
		new_production = []
		for i in production:
			new_production.append(i)
		new_production.append('Y->'+a)
		#print new_production
		temp = First('Y',terminals,nterminals,new_production)
		for i in temp:
			first.append(i)
		return first

#calculate the follow(B)
def Follow(B,terminals,nterminals, production):
	follow = []
	if B == production[0][0]:
		follow.append('$')
		
	for prod in production:
		leftpart = prod.split('->')[0]
		rightpart = prod.split('->')[1]
		if B in rightpart:


			if rightpart.index(B) == len(rightpart) -1:
				if leftpart == B:
					continue
				tmp_follow = Follow(leftpart,terminals,nterminals, production)
				#print tmp_follow
				for i in tmp_follow:
					follow.append(i)
			else:
				beta = rightpart[(rightpart.index(B)+1):]
				#print beta
				tmp_first = First(beta,terminals,nterminals, production)
				#print "asfsffags"
				if 'n' in tmp_first:
					tmp_first.remove('n')
					for j in tmp_first:
						follow.append(j)
					if leftpart == B:
						continue
					for i in Follow(leftpart,terminals,nterminals, production):
						follow.append(i)
				else:
					
					for j in tmp_first:
						follow.append(j)
	return list(set(follow))
#eliLeftRecur: eliminate the direct left recursion of an input file
def eliLeftRecur(filename):
	file = open(filename,'r')
	file1 = open('noleft.txt','w')
	for line in file.readlines():
		line = line.replace('->','|')
		tmp = line.split('|')
		flag = 0
		for item in tmp[1:]:
			if item[0] != tmp[0]:
				file1.write(tmp[0]+'->'+item+'Z'+'\n')
			else:
				file1.write('Z->'+item[1:]+'Z')
				flag = 1
		if flag == 1:
			file1.write('Z->n')

	file.close()
	file1.close()

def main():
	
	#mission1:read in a grammar(without direct left recursion),construct a table and output
	file = input("please input the grammar file (without direct left recursion):\n")
	terminals,nterminals,production = scan_grammar(file)
	table = table_allocate(terminals,nterminals,production)
	
	np.savetxt("mission1_out.txt",table,fmt='%d')
	file2 = open("mission1_out.txt",'a')
	for i in range(len(nterminals)):
		for j in range(len(terminals)):
			file2.write("----------------------------------------\n")
			file2.write("matrix details:\n")
			file2.write("position x\t")
			file2.write(str(i)+'\n')
			file2.write("position y\t")
			file2.write(str(j)+'\n')
			file2.write("--------\n")
			file2.write("non terminals\n")
			file2.write(nterminals[i]+'\n')
			file2.write("--------\n")			
			file2.write("terminals\n")
			file2.write(terminals[j]+'\n')
			file2.write("--------\n")
			file2.write("production\n")
			if table[i][j] != -1:
				file2.write(production[table[i][j]]+'\n')
			else:
				file2.write("NULL\n")
	file2.close()
	
	#mission2:read in a grammar(with direct left recursion),construct a table and output
	file1 = input("please input the grammar file (direct left recursion):\n")
	eliLeftRecur(file1)
	terminals1,nterminals1,production1 = scan_grammar("noleft.txt")
	table1 = table_allocate(terminals1,nterminals1,production1)
	np.savetxt("mission2_out.txt",table1,fmt='%d')
	file3 = open("mission2_out.txt",'a')
	for i in range(len(nterminals1)):
		for j in range(len(terminals1)):
			file3.write("----------------------------------------\n")
			file3.write("matrix details:\n")
			file3.write("position x\t")
			file3.write(str(i)+'\n')
			file3.write("position y\n")
			file3.write(str(j)+'\n')
			file3.write("--------\n")
			file3.write("non terminals\n")
			file3.write(nterminals1[i]+'\n')
			file3.write("--------\n")			
			file3.write("terminals\n")
			file3.write(terminals1[j]+'\n')
			file3.write("--------\n")
			file3.write("production\n")
			if table1[i][j] != -1:
				file3.write(production1[table1[i][j]]+'\n')
			else:
				file3.write("NULL\n")
	file3.close()
main()