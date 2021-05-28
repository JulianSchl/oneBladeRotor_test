from __future__ import division

import numpy as np
from matplotlib import pyplot as plt 
import precice

configuration_file_name = "../precice-config.xml"
participant_name = "Solid"
mesh_name = "Solid-Mesh"
write_data_name = 'Displacement'
read_data_name = 'Force'

num_vertices = 2  # Number of vertices

solver_process_index = 0
solver_process_size = 1

interface = precice.Interface(participant_name, configuration_file_name,
                              solver_process_index, solver_process_size)

mesh_id = interface.get_mesh_id(mesh_name)
dimensions = interface.get_dimensions()

vertices = np.zeros((num_vertices, dimensions))
read_data = np.zeros((num_vertices, dimensions))
write_data = np.zeros((num_vertices, dimensions))

vertices = np.array([[0.32, -0.105],[0.32, 0.016 ],[0.32, 0.097]])
read_data = vertices.copy()
write_data = vertices.copy()

vertex_ids = interface.set_mesh_vertices(mesh_id, vertices)
read_data_id = interface.get_data_id(read_data_name, mesh_id)
write_data_id = interface.get_data_id(write_data_name, mesh_id)
print(vertices)
dt = interface.initialize()
iteration = -1
next = 1
old_time_step = np.zeros((3,2))
new_time_step = np.zeros((3,2))
write_data = np.zeros((3,2))
while interface.is_coupling_ongoing():
    if interface.is_action_required(
            precice.action_write_iteration_checkpoint()):
        print("DUMMY: Writing iteration checkpoint")
        interface.mark_action_fulfilled(
            precice.action_write_iteration_checkpoint())

    iteration += 1
    if interface.is_read_data_available():
        read_data = interface.read_block_vector_data(read_data_id, vertex_ids)

    print(read_data)
    
    if iteration % 1 == 0:
    	next += 1
    	
    #Translation case
    write_data[:,1] = np.ones((3))*0.005*next
    #################
    
    #Rotation case
    length = 0.202
    zeit = 5*10**3
    omega = 2*np.pi/zeit
    
    print("Rotation")
    print(np.degrees(omega*iteration+np.pi/2))
    
    if iteration == 0:
    	old_time_step[0,:] = np.zeros((2))
    	radius = length*0.594
    	old_time_step[1,:] = np.array((np.cos(np.pi/2)*radius,np.sin(np.pi/2)*radius))
    	radius = length
    	old_time_step[2,:] = np.array((np.cos(np.pi/2)*radius,np.sin(np.pi/2)*radius))
    
    #unten
    new_time_step[0,:] = np.zeros((2))
    
    #mitte
    radius = length*0.594
    new_time_step[1,:] = np.array((np.cos(omega*iteration+np.pi/2)*radius,np.sin(omega*iteration+np.pi/2)*radius))
    
    #oben
    radius = length
    new_time_step[2,:] = np.array((np.cos(omega*iteration+np.pi/2)*radius,np.sin(omega*iteration+np.pi/2)*radius))
    
    print("Displacement:")
    displacement = new_time_step.copy() - old_time_step.copy()
    print(displacement)
    write_data = displacement
    
    #########
    

    if interface.is_write_data_required(dt):
        interface.write_block_vector_data(
            write_data_id, vertex_ids, write_data)

    print("DUMMY: Advancing in time")
    dt = interface.advance(dt)

    if interface.is_action_required(
            precice.action_read_iteration_checkpoint()):
        print("DUMMY: Reading iteration checkpoint")
        interface.mark_action_fulfilled(
            precice.action_read_iteration_checkpoint())

interface.finalize()
print("DUMMY: Closing python solver dummy...")
