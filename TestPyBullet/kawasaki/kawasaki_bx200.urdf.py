from jinja2 import Template

base_data = { 
    'link_name'     : 'base',
    'link_origin'   : 'rpy="0 0 0" xyz="0 0 0"',
    'mesh_filepath' : 'meshes/base.dae',   
}
link_1_data = { 
    'link_name'     : 'link_1',
    'link_origin'   : 'rpy="0 0 0" xyz="0 0 0"',
    'mesh_filepath' : 'meshes/link_1.dae',   
}
link_2_data = { 
    'link_name'     : 'link_2',
    'link_origin'   : 'rpy="0 0 0" xyz="0 0.2 0.53"',
    'mesh_filepath' : 'meshes/link_2.dae',   
}
link_3_data = { 
    'link_name'     : 'link_3',
    'link_origin'   : 'rpy="0 0 0" xyz="0 0.2 1.69"',
    'mesh_filepath' : 'meshes/link_3.dae',   
}
link_4_data = { 
    'link_name'     : 'link_4',
    'link_origin'   : 'rpy="0 0 0" xyz="0 0.2 1.92"',
    'mesh_filepath' : 'meshes/link_4.dae',   
}
link_5_data = { 
    'link_name'     : 'link_5',
    'link_origin'   : 'rpy="0 0 0" xyz="0 1.45 1.92"',
    'mesh_filepath' : 'meshes/link_5.dae',   
}
link_6_data = { 
    'link_name'     : 'link_6',
    'link_origin'   : 'rpy="0 0 0" xyz="0 1.675 1.92"',
    'mesh_filepath' : 'meshes/link_6.dae',   
}
joint_1_data = {
    'joint_name' : 'joint_1',
    'parent_link' : 'base',
    'child_link' : 'link_1',
    'x' : 0,
    'y' : 0,
    'z' : 0,
    'eulerX' : 0,
    'eulerY' : 0,
    'eulerZ' : 0,    
    'joint_axis' : '0 0 1',    
    'limit_effort' : 300,
    'lower_limit' : -2.96705972839,
    'upper_limnit' : 2.96705972839,
    'velocity_limit' : 10
}


linkTemplate = '''
    <link name="{{ link_name }}">
        <origin {{ link_origin }} />
        <visual>
            <origin {{ link_origin }} />
            <geometry>
                <mesh filename="{{ mesh_filepath }}"/>
            </geometry>
        </visual>
        <collision>
            <origin {{ link_origin }} />
            <geometry>
                <mesh filename="{{ mesh_filepath }}"/>
            </geometry>
        </collision>
    </link>  
'''

jointTemplate = '''
    <joint name="{{ joint_name }}" type="revolute">
        <parent link="{{ parent_link }}"/>
        <child link="{{ child_link }}"/>
        <origin {{ joint_origin }}/>
        <axis xyz="{{ joint_axis }}"/>
        <limit effort="{{ limit_effort }}" lower="{{ lower_limit }}" upper="{{ upper_limit }}", velocity = "{{ velocity_limit }}"/>
        <dynamics damping="0.5"/>
    </joint>
'''

fileTemplate = '''
<?xml version="1.0" ?>

<robot name="kawasaki">
    
    <!-- Import Rviz colors -->
    <material name="Grey">
        <color rgba="0.2 0.2 0.2 1.0"/>
    </material>
    <material name="Orange">
        <color rgba="1.0 0.423529411765 0.0392156862745 1.0"/>
    </material>
    <material name="Blue">
        <color rgba="0.5 0.7 1.0 1.0"/>      
    </material>
    
    {{ base }}
    {{ link_1 }}
    {{ link_2 }}
    {{ link_3 }}
    {{ link_4 }}
    {{ link_5 }}
    {{ link_6 }}   
    
    {{ joint_1 }} 
	{{ joint_2 }} 
	{{ joint_3 }} 
	{{ joint_4 }} 
	{{ joint_5 }} 
	{{ joint_6 }} 
	
</robot>
'''

file_template_data = {
    'base' : Template(linkTemplate).render(base_data),
    'link_1' : Template(linkTemplate).render(link_1_data),
    'link_2' : Template(linkTemplate).render(link_2_data),
    'link_3' : Template(linkTemplate).render(link_3_data),
    'link_4' : Template(linkTemplate).render(link_4_data),
    'link_5' : Template(linkTemplate).render(link_5_data),
    'link_6' : Template(linkTemplate).render(link_6_data),
    'joint_1' : Template(jointTemplate).render(joint_1_data),
    'joint_2' : Template(jointTemplate).render(joint_1_data),
    'joint_3' : Template(jointTemplate).render(joint_1_data),
    'joint_4' : Template(jointTemplate).render(joint_1_data),
    'joint_5' : Template(jointTemplate).render(joint_1_data),
    'joint_6' : Template(jointTemplate).render(joint_1_data)
    
}

fileString = Template(fileTemplate).render(file_template_data)

# Write to file
f = open("kawasaki/test.urdf", "w")
f.write(fileString)
f.close()