################################################################
# Fem script to compute plane truss displacements and stresses #
# written by asvera                                            #
################################################################

import numpy as np

# constants
E=10e06
A=1.5

# structure geometry 
node_coord=np.array([[0,0],[0,40],[40,40]]) # nodes coordinates
elem_con=np.array([[0,2],[1,2]]) # elements connectivity

x=node_coord[:,0] # sliced array with only x node coordinates
y=node_coord[:,1] # sliced array with only y node coordinates
node_count=len(node_coord)
elem_count=len(elem_con)
struct_dof=2*node_count # (entire) structure degrees of freedom

# matrices initialization
displacement=np.zeros((struct_dof,1))
force=np.zeros((struct_dof,1))
sigma=np.zeros((elem_count,1))
stiffness=np.zeros((struct_dof,struct_dof))

# load assignments
force[4]=500
force[5]=300
 
# computations
for e in range(elem_count):
	index=elem_con[e]
	elem_dof=np.array([index[0]*2, index[0]*2+1, index[1]*2, index[1]*2+1])
	xl=x[index[1]]-x[index[0]]
	yl=y[index[1]]-y[index[0]]
	elem_length=np.sqrt(xl*xl+yl*yl)
	c=xl/elem_length
	s=yl/elem_length
	rot=np.array([[c*c, c*s, -c*c, -c*s],
                  [c*s, s*s, -c*s, -s*s],
                  [-c*c, -c*s, c*c, c*s],
                  [-c*s, -s*s, c*s, s*s]])
	k=(E*A/elem_length)*rot
	stiffness[np.ix_(elem_dof, elem_dof)] +=k

suppress_dof=np.array([0,1,2,3]) # constrained degrees of freedom
active_dof=np.setdiff1d(np.arange(struct_dof), suppress_dof)
displacement_aux=np.linalg.solve(stiffness[np.ix_(active_dof,active_dof)], force[np.ix_(active_dof)])
displacement[np.ix_(active_dof)]=displacement_aux
react=np.dot(stiffness, displacement)

for e in range(elem_count):
	index=elem_con[e]
	elem_dof=np.array([index[0]*2, index[0]*2+1, index[1]*2, index[1]*2+1])
	xl=x[index[1]]-x[index[0]]
	yl=y[index[1]]-y[index[0]]
	elem_length=np.sqrt(xl*xl+yl*yl)
	c=xl/elem_length
	s=yl/elem_length
	sigma[e]=(E/elem_length)*np.dot(np.array([-c,-s,c,s]), displacement[np.ix_(elem_dof)])

# emitting results to screen
print(f'displacements:\n {displacement}')
print(f'stress:\n {sigma}')