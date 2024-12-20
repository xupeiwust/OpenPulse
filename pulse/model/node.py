import numpy as np

DOF_PER_NODE_STRUCTURAL = 6
DOF_PER_NODE_ACOUSTIC = 1

def distance(a, b):
    return np.linalg.norm(a.coordinates - b.coordinates)

class Node:
    """A node class.
    This class creates a node object from input data.

    Parameters
    ----------
    x : float
        Node x coordinate.

    y : float
        node y coordinate.

    z : float
        Node z coordinate.

    global_index : int, optional
        Internal node index used for computing.
        Default is None.

    external_index : int
        Node index displayed to the user.
        Default is None.
    """
    def __init__(self, x, y, z, **kwargs):
        
        self.x = x
        self.y = y
        self.z = z

        self.global_index = kwargs.get('global_index', None)
        self.external_index = kwargs.get('external_index', None)

        self.reset()

    def reset(self):
        
        # Structural boundary conditions and external lumped elements

        self.deformed_coordinates = None
        self.deformed_rotations_xyz_gcs = None
        self.deformed_displacements_xyz_gcs = None
        self.nodal_solution_gcs = None
        self.static_nodal_solution_gcs = None
        self.acoustic_solution = None
        self.cross_section = None

    @property
    def coordinates(self):
        """
        This method returns the node's coordinates as a array.

        Returns
        -------
        array
            Node coordinates
        """
        return np.array([self.x, self.y, self.z], dtype=float)

    @property
    def local_dof(self):
        """
        This method returns the node's structural degrees of freedom in the local coordinate system. The 3D Timoshenko beam theory implemented takes into account the three node's translations and the three node's rotations.

        Returns
        -------
        list
            Node's structural degrees of freedom in the local coordinate system.

        See also
        --------
        global_dof : Structural degrees of freedom in the global coordinate system.
        """
        return np.arange(DOF_PER_NODE_STRUCTURAL)

    @property
    def global_dof(self):
        """
        This method returns the node's structural degrees of freedom in the global coordinate system. The 3D Timoshenko beam theory implemented takes into account the three node's translations and the three node's rotations.

        Returns
        -------
        list
            Node's structural degrees of freedom in the global coordinate system

        See also
        --------
        local_dof : Structural degrees of freedom in the local coordinate system.
        """
        return self.local_dof + self.global_index * DOF_PER_NODE_STRUCTURAL

    def distance_to(self, other: "Node"):
        """
        This method returns the distance between the actual node and other one.

        Parameters
        ----------
        other : Node object
            The node to calculate the distance to.

        Returns
        -------
        float
            Distance between the nodes.
        """
        return np.linalg.norm(self.coordinates - other.coordinates)
    
    # def admittance(self, area_fluid, frequencies):
    #     """
    #     This method returns the node's lumped acoustic admittance according to either prescribed specific impedance or prescribed radiation impedance. The admittance array has the same length as the frequencies array. In terms of analysis, if admittance is constant in the frequency domain, the method returns an array filled with the constant value with the same length as the frequencies array.

    #     Parameters
    #     ----------
    #     area_fluid : float
    #         Acoustic fluid cross section area.

    #     frequencies : list
    #         Frequencies of analysis.

    #     Returns
    #     ----------
    #     complex array
    #         Lumped acoustic admittance
        
    #     Raises
    #     ------
    #     TypeError
    #         The Specific Impedance array and frequencies array must have
    #         the same length.

    #     TypeError
    #         The Radiation Impedance array and frequencies array must have
    #         the same length.
    #     """
    #     admittance_specific = np.zeros(len(frequencies), dtype=complex)
    #     admittance_rad = np.zeros(len(frequencies), dtype=complex)

    #     if self.specific_impedance is not None:
    #         Z_specific = self.specific_impedance / area_fluid
            
    #         if isinstance(self.specific_impedance, complex):
    #             admittance_specific = 1/Z_specific * np.ones_like(frequencies)

    #         elif isinstance(self.specific_impedance, np.ndarray):
    #             if len(self.specific_impedance) != len(frequencies):
    #                 raise TypeError("The Specific Impedance array and frequencies array must have \nthe same length.")
    #             admittance_specific = np.divide(1, Z_specific)
              
    #     if self.radiation_impedance is not None:
    #         Z_rad = self.radiation_impedance / area_fluid

    #         if isinstance(self.radiation_impedance, complex):
    #             admittance_rad = np.divide(1, Z_rad) 

    #         elif isinstance(self.radiation_impedance, np.ndarray):
    #             if len(self.radiation_impedance) != len(frequencies):
    #                 raise TypeError("The Radiation Impedance array and frequencies array must have \nthe same length.")
    #             admittance_rad = np.divide(1, Z_rad)
        
    #     admittance = admittance_specific + admittance_rad
        
    #     return admittance.reshape(-1, 1)#([len(frequencies),1])