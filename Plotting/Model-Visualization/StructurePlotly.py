#########################################################################################
## This script plots the Nodes and Elements in order to render the OpenSees model.		
## Make sure you have installed Plotly successfully.								 		
## As of now, this procedure does not work for 2D/3D shell and solid elements.		  	
##																					 	
## Created By - Anurag Upadhyay, Ph.D. Candidate, University of Utah
## 																					  	
## You can download more examples from https://github.com/u-anurag					  	
#########################################################################################

import plotly.graph_objs as go
import chart_studio.plotly as py
import plotly.io as pio
import numpy as np

show_node_tags = 'no'		# Check if you want to display the node numbers     :: 'yes'  or   'no'
show_element_tags = 'no'	# Check if you want to display the element numbers  :: 'yes'  or   'no'
offset = 0.05				#offset for text
 

N,x,y,z = np.loadtxt('RecordNodes.out', dtype=str, delimiter=None, converters=None, unpack=True)

fig = go.Figure()

def nodecoordsOriginal(nodetag):
	i, = np.where(N == str(nodetag))
	return float(x[int(i)]),  float(y[int(i)]),  float(z[int(i)])

with open ('RecordElements.out', 'r') as elements:
	for line in elements:
		
		iNodeO = nodecoordsOriginal(line.split()[1])
		jNodeO = nodecoordsOriginal(line.split()[2])
		
		Xdata = np.array([iNodeO[0], jNodeO[0]])
		Ydata = np.array([iNodeO[1], jNodeO[1]])
		Zdata = np.array([iNodeO[2], jNodeO[2]])
		
		fig.add_trace(go.Scatter3d(x = Xdata, y=Ydata, z=Zdata,
								marker=dict(
									size=0.5,
									color='black',
								),
									line=dict(
									color='darkblue',
									width=2)))
									
		if show_node_tags == 'yes':
			fig.add_trace(go.Scatter3d(x = [iNodeO[0]+offset], y=[iNodeO[1]+offset], z=[iNodeO[2]+offset],
								mode="text",
								text=[str(line.split()[1])],
								textposition="top center"))
							
		if show_element_tags == 'yes':
			fig.add_trace(go.Scatter3d(x = [0.5*(iNodeO[0]+jNodeO[0])], y=[0.5*(iNodeO[1]+jNodeO[1])], z=[0.5*(iNodeO[2]+jNodeO[2])],
								mode="text",
								text=[str(line.split()[0])],
								textposition="top center"))
#
fig.update_layout(
	#width=800,
	#height=700,
	autosize=True,
	showlegend=False,
	scene=dict(
		aspectratio = dict( x=1, y=1, z=1),
		aspectmode = 'data',
	),
)

fig.update_layout(
	scene=dict(
		camera=dict(
			projection=dict(
				type= 'orthographic'
			)
		),
	),
)

pio.write_html(fig, file='StructurePlotly_Render.html', auto_open=True)

## Use py.plot to send the plot to your Plotly account. See Plotly python documentation to setup an account.
# py.plot(fig, file='StructurePlotly_Render', auto_open=True)
