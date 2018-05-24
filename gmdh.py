import numpy as np
import random

def mnko(a,b):
	
	x = np.matrix(a[:,0])
	H = 1/float(np.dot(x.T, x))
	g = np.dot(x.T,b)
	teta = np.dot(H,g)
	X = np.matrix(x)
	for i in range(1, a.shape[1]):
		x = np.matrix(a[:,i])
		X = np.concatenate((X,x),axis = 1)
		H = np.linalg.inv(np.dot(X.T, X))
		tmp = np.dot(x.T,b)
		g = np.concatenate((g,tmp),axis = 1)
		teta = np.dot(H,g.T)
	return teta

def Krit_regul(A,teta, real):
	FC = np.dot(A,teta)
	real = np.matrix(real)
	real = real.T
	s =0
	for i in range(FC.size):
		s += (real[i] - FC[i])**2
	return s/float(real.size)
	
def Krit_stop(error,iter):
	if iter ==0:
		return False
	elif (error[iter]>error[iter - 1]) or (iter == 10) or (error[iter]<= 0.000001):
		return True
	else:
		return False
			
def MSE(A, real, poriadok,net):
	Layer = net[-2]
	k = len(net)- 2
	res = Result_of_layer(net,A,k,poriadok)
	i = Index_of_best(Layer)
	fc = res[:,i]
	errors = fc - real
	tmp = np.multiply(errors,errors)
	tmp = float(sum(tmp))/len(real)
	return tmp

def trivial_MSE(fc,real):
	errors = fc - real
	tmp = np.multiply(errors,errors)
	tmp = float(sum(tmp))/len(real)
	return tmp

def MAPE(fc, real):
	er =  (real- fc)/real
	er = sum(np.fabs(er))/len(real)
	
	return 100*er
def Krit_nezm(FC, real):
		s = 0
		for i in range(FC.size):
			s += (real[i] - FC[i])**2
		return s/float(real.size)
	
def Create_matr(X, Y,k):
	I = np.ones((X.size,1))
	I = I
	I = np.matrix(I)
	if k:
		return np.concatenate((I,X,Y), axis = 1)
	else:
		Z = np.ones(X.size)
		Z = np.matrix(Z)
		Z = np.multiply(X,Y)
		return np.concatenate((I,X,Y,Z), axis = 1)
	
def Sequence_for_Learn(X,percent_learn):
	n = int(X.shape[0]*percent_learn/100)
	
	seq = np.ones(n)
	tmp = [] 
	for i in range(int(X.shape[0])):
		tmp.append(i)
	for i in range(n):
		r = int(len(tmp)*random.random())
		seq[i] = int(tmp[r])
		del tmp[r]
	return seq
	
def Sequence_for_Check(X, seq_for_learn):
    s = int(X.shape[0]) -  len(seq_for_learn)
    seq = np.ones(s)
    for j in range(s):
        for i in range(int(X.shape[0])):
            if not (i in seq_for_learn or i in seq):
                seq[j] = int(i)
                break
    return seq
				
def make_mat(FileName):
	File_one = open(FileName)
	Name = []
	for i in File_one:
		Name.append(float(i))
	Name = np.matrix(Name)
	Name = Name.T
	File_one.close
	return Name
	
	
def Matr_from_seq(A, seq):
	s = (len(seq), int(A.shape[1]))
	A_new = np.ones(s)
	A_new = np.matrix(A_new)
	for i in range(seq.size):
		A_new[i] = A[int(seq[i])]
	return A_new


def define_real(real, seq):
		s= len(seq)
		result = np.ones(s)
		for i in range(s):
				k = int(seq[i])
				result[i] = real[k]
		return result
	
def find_layer(A, seq_learn, seq_check, real, poriadok):
	F = 4 # I decided 4
	MLearn = Matr_from_seq(A, seq_learn)
	MCheck = Matr_from_seq(A, seq_check)
	real_learn = define_real(real, seq_learn)
	real_check = define_real(real, seq_check)
	n = int((int(A.shape[1])*(int(A.shape[1]) - 1))/float(2))
	
	Help_matr = Create_matr(A[:,0],A[:,0], poriadok)
	m = int(Help_matr.shape[1])+3
	tmp = np.ones((n,m))
	Layer = np.matrix(tmp)
	#a = np.ones(4)
	counter_for_def =0
	counter_for_def = int(counter_for_def)
	for i in range(int(A.shape[1]-1)):
		for j in range(i+1, int(A.shape[1])):
				
				MWork = Create_matr(MLearn[:,i],MLearn[:,j], poriadok)
				M_check_loc = Create_matr(MCheck[:,i],MCheck[:,j], poriadok)
				a = mnko(MWork,real_learn)
				error = Krit_regul(M_check_loc, a,real_check)
				Layer[counter_for_def,0] = error
				Layer[counter_for_def,1] = i
				Layer[counter_for_def,2] = j
				for k in range(3, m):
					Layer[counter_for_def, k] = a[k-3]
				counter_for_def += 1
	er_container = [] # container for defs which go further
	for i in range(n):
		er_container.append(i)	
	for j in range(n - F):
		max = 0
		index = 100
		for i in er_container:
			if Layer[ i, 0]> max:
				max = Layer[i, 0]
				index = i
		for k in er_container:
			if k == index:
				del er_container[er_container.index(k)]
		
	fin_layer = np.ones((F,m))	
	tmp = np.ones((F,m))
	Selected_Layer = np.matrix(tmp)
	for i in range(F):
		for j in range(m):
			Selected_Layer[i, j] = Layer[er_container[i], j]
	return Selected_Layer

def Proof_error(Layer):
 error = Layer[0,0]
 for i in Layer[:,0]:
	if i< error:
		error = i
 return error
 
def Matr_from_layer(Layer):
	n = int(Layer.shape[0])
	m = int(Layer.shape[1]) - 3
	new_matrix  = np.ones((n,m))
	new_matrix = np.matrix(new_matrix)
	for i in range(n):
		for j in range(m):
			new_matrix[i,j] = Layer[i, j+3]
	return new_matrix
def index_to_percent(k):
	if k ==1:
		res = 50
	elif k==2:
		res = 60
	elif k==3:
		res = 70
	elif k==4:
		res = 80
	else: res=90
	return res
	
def MGUA(A,real,percent,Name, poriadok):
	seq_learn = Sequence_for_Learn(A, percent)
	seq_check = Sequence_for_Check(A,seq_learn)
	net = []
	it = 0
	errors = []
	K  = A
	net.append(find_layer(K,seq_learn, seq_check, real, poriadok))
	errors.append(float(Proof_error(net[it])))
		
	while not Krit_stop(errors,it):
		Q = Result_of_layer(net,A,it, poriadok)
		net.append(find_layer(Q,seq_learn, seq_check, real, poriadok))
		it+=1	
		errors.append(float(Proof_error(net[it])))
	#	print(it)
#		print(errors)
	k = it-1	
#	print(net[k])	
	#print(Index_of_best(net[k]))
#	print(String_Result_of_Layer(Name, net,A,k,Index_of_best(net[k]), poriadok))
	return net

def Index_of_best(Layer):
	min  = Layer[0,0]
	index = 0
	for i in range(int(Layer.shape[0])):
		if min>Layer[i,0]:
			min = Layer[i,0]
			index = i
	return index
	
def calculate_result(vec, net,poriadok):
	seq = [0]
	n = len(net)- 2
	a = Result_of_layer(net,vec,n,poriadok)
	i = Index_of_best(net[n])

	return a[0,i]

def Result_of_layer(Layers_list, A, k,poriadok):
	y = []
	Layer = Layers_list[k]
	a = Matr_from_layer(Layer)
	a = a.T
	if k>0:
		A = Result_of_layer(Layers_list,A,k-1, poriadok)
	for l in range(int(Layer.shape[0])):
		i = Layer[l, 1]
		j = Layer[l, 2]
		H = Create_matr(A[:,i],A[:,j], poriadok)
		y.append(np.dot(H,a[:,l]))# !!!!!!!!!!!!!!!!!
	t = np.ones((int(A.shape[0]),int(Layer.shape[0])))
	for j in range(int(Layer.shape[0])):
		for i in range(int(A.shape[0])):
			t[i,j] = y[j][i]
	t= np.matrix(t)
	return t
	
def String_Result_of_Layer(Names,Layers_list,A,k,i, poriadok):
	#k  - index of Layer
	# i = index of part definition which must be revealed
	i = int(i)
	s = ''
	if k == -1:
		s = s+Names[i]
		#s =str(Layer[i,n-2])+'+'+str(Layer[i,n-1])+'*    '+'+'+str(Layer[i,n])+'*    ')' 
	else:
		Layer= Layers_list[k]
		n = int(Layer.shape[1])
		num_for_round = 3
		if int(Layer.shape[1])==7:
			s = str(round(Layer[i,n-4],num_for_round))+'+(('+str( round(Layer[i,n-3],num_for_round))+')*('+String_Result_of_Layer(Names, Layers_list,A,k-1,Layer[i,1], poriadok)+'))'+'+(('+str(round(Layer[i,n-2],num_for_round))+')*('+String_Result_of_Layer(Names, Layers_list,A,k-1,Layer[i,2], poriadok)+'))+('+ str(round(Layer[i,n-1],num_for_round))+')*('+String_Result_of_Layer(Names, Layers_list,A,k-1,Layer[i,1], poriadok)+'*'+String_Result_of_Layer(Names, Layers_list,A,k-1,Layer[i,2], poriadok)+')'
		elif 	int(Layer.shape[1])==6:
			s = str(round(Layer[i,n-3],num_for_round))+'+('+str( round(Layer[i,n-2],num_for_round))+')*('+String_Result_of_Layer(Names, Layers_list,A,k-1,Layer[i,1], poriadok)+')'+'+('+str(round(Layer[i,n-1],num_for_round))+')*('+String_Result_of_Layer(Names, Layers_list,A,k-1,Layer[i,2], poriadok)+')'
	return s
def errors_of_layer(A, real, poriadok,net):
	Layer = net[-2]
	k = len(net)- 2
	res = Result_of_layer(net,A,k,poriadok)
	i = Index_of_best(Layer)
	fc = res[:,i]
	errors = fc - real
	return errors


def Darbin_Watson(errors):
	n = len(errors)
	s = 0
	for i in range(1,n):
		s+=(errors[i] - errors[i-1])**2
	s1 = 0
	for i in range(n):
		s1+= errors[i]**2
		
	return float(float(s)/s1)
	
def R_kv(real, fc):
	mean = sum(real)/float(real.size)
	TSS = sum(np.multiply((real - mean),(real - mean)))
	RSS = sum(np.multiply((fc - mean),(fc - mean)))
	return float(float(RSS)/TSS)
	
def Movav(real,m):
	a =[]
	for i in range(m-1,real.size):
		s = 0
		for k in range(m):
			s+=float(real[i-k])
			
		a.append(s/float(m))
	a = np.matrix(a)
	a = a.T
	return a
	
def Sum_of_S_errors(real, fc):
	error = real-fc
	error = np.multiply(error,error)
	return float(sum(error))
		
	
def Theil(real,fc):
	n = float(len(real))
	a = trivial_MSE(real, fc)
	real = np.multiply(real,real)
	real = sum(real)
	real = float(real/n)
	real  = real**(float(1)/2)
	
	fc = np.multiply(fc,fc)
	fc = sum(fc)
	fc = float(fc/n	)
	fc  = fc**(float(1)/2)
	return a/(real+fc)

def Vec_res_of_net(Layers_list, A, k,poriadok ):
	Layer = Result_of_layer(Layers_list, A, k,poriadok )
	i = Index_of_best(Layer)
	return Layer[:,i]

def  Akaike(SSE,n,p):
	return n*np.log(SSE)+2*p