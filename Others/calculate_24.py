"""
 data structure designed for intermiddle result
 each calculation should have this format {value1-node, value2-node, operation}
 operation means that one of +-*/ calculation
 the reason for Operator having append method is that for same value-node can
 have multi calculation path. eg 2 2 -> 4 can have '+  *' paths.
"""

class Node():
	def __init__(self,value):
		self.value = value
		self.i_list = []

	def append(self,node):
		self.i_list.append(node)

class Operator():

	def __init__(self,op):
		self.op = op

	def append(self,op):
		self.op.append(op)

"""

"""
def cal(node1,node2):
	the_list =[]
	var_1 = node1.value
	var_2 = node2.value
	m_dict = {}
	m_dict[var_1 + var_2] = [1]
	temp_var = var_1 - var_2
	if temp_var > 0:
		m_dict[temp_var] = [2]
	else:
		m_dict[-temp_var] = [-2] # <= 0
	temp_var = var_1 * var_2
	if temp_var not in m_dict:
		m_dict[temp_var] = [3]
	else:
		m_dict[temp_var].append(3)
	if var_2 != 0:	
		temp_var = var_1 / var_2
		if temp_var not in m_dict:
			m_dict[temp_var] = [4]
		else:
			m_dict[temp_var].append(4)
	if var_1 != 0:	
		temp_var = var_2 / var_1
		if temp_var not in m_dict:
			m_dict[temp_var] = [-4]
		else:
			m_dict[temp_var].append(-4)
	for k,v in m_dict.items():
		t_node = Node(k)
		t_node.append(node1)
		t_node.append(node2)
		oper = Operator(v)
		t_node.append(oper)
		the_list.append(t_node)
	return the_list

 # should add a step for removing repeated results
def iterator(node):
	if len(node.i_list) != 0:
		print(node.value,node.i_list[0].value,
			node.i_list[1].value,node.i_list[2].op)
		iterator(node.i_list[0])
		iterator(node.i_list[1])

def A_and_B(var_list):
	var_1 = var_list[0]
	var_2 = var_list[1]
	var_3 = var_list[2]
	var_4 = var_list[3]
	t_res_1 = cal(var_1,var_2)
	t_res_2 = cal(var_3,var_4)
	res = []
	for item_1 in t_res_1:
		for item_2 in t_res_2:
			res += cal(item_1,item_2)
	return res

def ABB(var_list):
	var_1 = var_list[0]
	var_2 = var_list[1]
	res_1 = cal(var_1,var_2)

	var_3 = var_list[2]
	res_2 = []
	for item in res_1:
		res_2 += cal(item,var_3)

	var_4 = var_list[3]
	res = []
	for item in res_2:
		res += cal(item,var_4)
	return res

if __name__ == "__main__":
	var_1 = Node(8)
	var_2 = Node(3)
	var_3 = Node(8)
	var_4 = Node(3)
	list_1 = [var_1,var_2,var_3,var_4]
	list_2 = [var_1,var_3,var_2,var_4]
	list_3 = [var_1,var_4,var_2,var_3]
	list_4 = [var_3,var_4,var_1,var_2]
	list_5 = [var_2,var_4,var_1,var_3]
	list_6 = [var_2,var_3,var_1,var_4]
	m_list = [list_1,list_2,list_3,list_4,list_5,list_6]
	m_res = []
	for item in m_list:
		m_res += ABB(item)
	for item in m_list[:3]:
		m_res += A_and_B(item)

	for t in m_res:
		if t.value - 24 < 1e-3 and t.value -24 > -1e-3:
			iterator(t)
			print('===========')
			# for item in t.i_list:
			# 	if isinstance(item,Node):
			# 		iterator(item)
			# 	else:
			# 		print(item.op)
			

