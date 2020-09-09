from __future__ import absolute_import, division, print_function
import logging
logging.basicConfig()

"""
Structure of a ray-tracing module. For documentation and development purposes.
"""

solution_types = {1: 'direct',
                  2: 'refracted',
                  3: 'reflected'}


class ray_tracing:
    """
    base class of ray tracer. All ray tracing modules need to prodide the following functions
    """

    def __init__(self, medium, attenuation_model="SP1", log_level=logging.WARNING,
                 n_frequencies_integration=6):
        """
        class initilization

        Parameters
        ----------
        x1: 3dim np.array
            start point of the ray
        x2: 3dim np.array
            stop point of the ray
        medium: medium class
            class describing the index-of-refraction profile
        attenuation_model: string
            signal attenuation model (so far only "SP1" is implemented)
        log_level: logging object
            specify the log level of the ray tracing class
            * logging.ERROR
            * logging.WARNING
            * logging.INFO
            * logging.DEBUG
            default is WARNING
        n_frequencies_integration: int
            the number of frequencies for which the frequency dependent attenuation
            length is being calculated. The attenuation length for all other frequencies
            is obtained via linear interpolation.

        """
        pass

   
        
    
    def set_start_and_end_point(self, x1, x2):
        x1 = np.array(x1, dtype =np.float)
        x2 = np.array(x2, dtype = np.float)
        self._x1 = x1
        self._x2 = x2

    
    
    def RadioPropa(self, x1, x2 ):
        """
        uses RadioPropa to find the numerical ray tracing solutions for x1 x2 and returns the Candidates for all the possible solutions 
        """
        candidates = []
        
        airBoundary = radiopropa.Discontinuity(radiopropa.Plane(radiopropa.Vector3d(0,0,0), radiopropa.Vector3d(0,0,1)), 1.3, 1)
        sim = radiopropa.ModuleList()
        sim.add(airBoundary)
        sim.add(radiopropa.MaximumTrajectoryLength(1000*radiopropa.meter))

        phi_direct, theta = hp.cartesian_to_spherical(*(np.array(self._x2)-np.array(self._x1)))
        phi_direct = np.rad2deg(phi_direct)
        theta = np.rad2deg(theta)

        for phi in np.arange(0,phi_direct, 1):
            x = hp.spherical_to_cartesian(np.deg2rad(x1_dir[0]), np.deg2rad(x1_dir[1]))
            y = hp.spherical_to_cartesian(np.deg2rad(phi), np.rad2deg(theta))
            delta = np.arccos(np.dot(x, y))

            cherenkov_angle = 56
            if (abs(np.rad2deg(delta) - cherenkov_angle) < 20): #only include rays with angle wrt cherenkov angle smaller than 20 degrees

                source = radiopropa.Source()

                source.add(radiopropa.SourcePosition(radiopropa.Vector3d(x1[0], x1[1], x1[2])))
                x,y,z = hp.spherical_to_cartesian(phi * radiopropa.deg ,theta * radiopropa.deg)
                source.add(radiopropa.SourceDirection(radiopropa.Vector3d(x, 0 , z)))
                sim.setShowProgress(True)
                candidate = source.getCandidate()

                sim.run(candidate, True)
                trajectory_length = candidate.getTrajectoryLength()
                Candidate = candidate.get() #candidate is a pointer to the object Candidate
                detection = obs.checkDetection(Candidate)
                if detection == 0:
                    candidates.append(Candidate)
        return candidates
    
    

    def find_solutions(self):
        """
        find all solutions between x1 and x2
        """
        results = []

        candidates = RadioPropa(self._x1, self._x2)
        for candidate in candidates:
            
            solution_type = candidate.getSolutionType()
            reflection = candidate.getReflection()
            results.append('type':solution_type, 'reflection':reflection)
    
        return results

    def has_solution(self):
        """
        checks if ray tracing solution exists
        """
        return len(self.__results) > 0

    def get_number_of_solutions(self):
        """
        returns the number of solutions
        """
        return len(self.__results)

    def get_results(self):
        """

        """
        return self.__results

    def get_solution_type(self, iS):
        """ returns the type of the solution

        Parameters
        ----------
        iS: int
            choose for which solution to compute the launch vector, counting
            starts at zero

        Returns
        -------
        solution_type: int
            * 1: 'direct'
            * 2: 'refracted'
            * 3: 'reflected
        """
        solution_type = candidates[iS].getSolutiontype()
        return solution_type
        
    def get_path(self, iS, n_points=1000):
        """
        helper function that returns the 3D ray tracing path of solution iS

        Parameters
        ----------
        iS: int
            ray tracing solution
        n_points: int
            number of points of path
        """
        
        path = candidates[iS].getPath()
        return path
        

    def get_launch_vector(self, iS):
        """
        calculates the launch vector (in 3D) of solution iS

        Parameters
        ----------
        iS: int
            choose for which solution to compute the launch vector, counting
            starts at zero

        Returns
        -------
        launch_vector: 3dim np.array
            the launch vector
            
        """
        launch_vector = candidates[iS].get_launch_vector()
        return launch_vector

    def get_receive_vector(self, iS):
        """
        calculates the receive vector (in 3D) of solution iS

        Parameters
        ----------
        iS: int
            choose for which solution to compute the launch vector, counting
            starts at zero

        Returns
        -------
        receive_vector: 3dim np.array
            the receive vector
            
        """
        receive_vector = candidates[iS].get_receive_vector()
        return receive_vector

    def get_reflection_angle(self, iS):
        """
        calculates the angle of reflection at the surface (in case of a reflected ray)

        Parameters
        ----------
        iS: int
            choose for which solution to compute the launch vector, counting
            starts at zero

        Returns
        -------
        reflection_angle: float or None
            the reflection angle (for reflected rays) or None for direct and refracted rays
        """
        reflection_angle = candidates[iS].get_reflection_angle()
        return reflection_angle

    def get_path_length(self, iS, analytic=True):
        """
        calculates the path length of solution iS

        Parameters
        ----------
        iS: int
            choose for which solution to compute the launch vector, counting
            starts at zero

        analytic: bool
            If True the analytic solution is used. If False, a numerical integration is used. (default: True)

        Returns
        -------
        distance: float
            distance from x1 to x2 along the ray path
        """
        path_length = candidates[iS].get_trajectoryLength()
        return path_length

    def get_travel_time(self, iS, analytic=True):
        """
        calculates the travel time of solution iS

        Parameters
        ----------
        iS: int
            choose for which solution to compute the launch vector, counting
            starts at zero

        analytic: bool
            If True the analytic solution is used. If False, a numerical integration is used. (default: True)

        Returns
        -------
        time: float
            travel time
        """
        travel_time = candidates[iS].get_propagationTime()
        return travel_time
        
    def get_attenuation(self, iS, frequency, max_detector_freq=None):
        """
        calculates the signal attenuation due to attenuation in the medium (ice)

        Parameters
        ----------
        iS: int
            choose for which solution to compute the launch vector, counting
            starts at zero

        frequency: array of floats
            the frequencies for which the attenuation is calculated

        max_detector_freq: float or None
            the maximum frequency of the final detector sampling
            (the simulation is internally run with a higher sampling rate, but the relevant part of the attenuation length
            calculation is the frequency interval visible by the detector, hence a finer calculation is more important)

        Returns
        -------
        attenuation: array of floats
            the fraction of the signal that reaches the observer
            (only ice attenuation, the 1/R signal falloff not considered here)
        """
        pass

    def apply_propagation_effects(self, efield, iS):
        
        
        return efield

    def create_output_data_structure(self, dictionary, n_showers, n_antennas):
        nS = self.get_number_of_raytracing_solutions()
        dictionary['ray_tracing_solution_type'] = np.ones((n_showers, n_antennas, nS), dtype=np.int) * -1


    def write_raytracing_output(self, dictionary):
        pass

    def check_if_presimulated(self):
        pass

    def get_number_of_raytracing_solutions(self):
        pass