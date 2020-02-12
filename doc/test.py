import pickle as pkl


# 0 = PairID -> ID de la famille 
# 1 = ID -> id propre à la personne 
# 2 = patID -> ID du père
# 3 = matID -> ID de la mère

def lecture(fichier):
	"""
	Convert a file.ped to a Dataframe
	"""
	tab = [i.strip().split() for i in open(fichier).readlines()]
	dfObj = pd.DataFrame(tab, columns = ['FamID' , 'ID', 'PatID', 'MatID'])
	return dfObj

#print(lecture("../data/fam9.ped"))

# DataFrame ou Array, à voir 

def dataframe_to_array(dataframe):
	"""
	return an dataframe convert into an array
	"""
	return dataframe.to_numpy()
tab = lecture("../data/fam9.ped")
tab_array = dataframe_to_array(tab)
#print(tab)
senegal = lecture("../data/senegal2013.ped")
#print(senegal.loc[senegal["FamID"]== 'D991313'])

def add_sexe(tab,famID=None):
	"""
	Return an array with a specific column to identify the individu's sex
	0 = unidentify
	1 = Male
	2 = Female
	"""
	if(famID != None):
		tab.insert(4,"sex",0)
		tab = tab.loc[tab["FamID"] == famID]
		father = tab["PatID"]
		mother = tab["MatID"]
		size = len(tab.index) # Number of columns
		sex = np.zeros(size,dtype=int)
		for i,j in zip(father,mother):
			f = tab.loc[tab["ID"] == i]
			m = tab.loc[tab["ID"] == j]
			print(f.index.values.tolist())
			#print(tab.at[int(f.index.values.),'sex'])
			# if (len(f)!=0 and f["FatID"].values != '0'):	
			# 	f["Sex"] = 1
			# if (len(m)!=0 and m["MatID"].values != '0'):
			# 	m["Sex"] = 2
		#tab.insert(4,"sex",sex)

	else:
		tab.insert(4,"sex",0)
		father = tab["PatID"]
		mother = tab["MatID"]
		size = len(tab.index) # Number of columns
		sex = np.zeros(size,dtype=int)
		for i,j in zip(father,mother):
			if int(i) != 0:
				sex[int(i)-1] = 1
			if int(j) != 0:
				sex[int(j)-1] = 2
		#tab.insert(4,"sex",sex)
	return tab


#print(add_sexe(tab))
print(add_sexe(senegal,'D1'))

def bro_sis(tab,id,famID=None):
	"""
	Return the brothers and sisters IDs of a specific individu
	"""
	return

def outsprings(tabs,id,famID=None):
	"""
	return the outsprings of an individu
	"""
	return

def holders(tabs,id,famID=None):
	"""
	return the holders of an individu
	"""
	return

def step_family(tab,id,famID=None):
	"""
	return the step family of an individu
	"""
	return

def cousins(tabs,id,famID=None):
	return