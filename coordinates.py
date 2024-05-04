from configuration import Configuration


class Coordinates:
    """
    A utility class for working with geographical coordinates and grid cells.
    """

    @staticmethod
    def in_range(point):
        """
        Checks if a given point is within the defined GPS limits.

        Args:
            point (tuple): The geographical point represented as a tuple (latitude, longitude).

        Returns:
            bool: True if the point is within the GPS limits, False otherwise.
        """
        lat, lng = point
        gps_limits = Configuration.GPS_LIMIT
        return (gps_limits["lat"][0] <= lat < gps_limits["lat"][1]) and \
               (gps_limits["lng"][0] <= lng < gps_limits["lng"][1])

    @staticmethod
    def in_range_cell(cell):
        """
        Checks if a given grid cell is within the defined grid size.

        Args:
            cell (tuple): The grid cell represented as a tuple (x, y).

        Returns:
            bool: True if the cell is within the grid size, False otherwise.
        """
        x, y = cell
        grid_size = Configuration.GRID_SIZE
        return 0 <= x < grid_size and 0 <= y < grid_size

    @staticmethod
    def get_cell(point, grid_size=None):
        """
        Converts a geographical point to its corresponding grid cell.

        Args:
            point (tuple): The geographical point represented as a tuple (latitude, longitude).
            grid_size (int): The size of the grid (optional).

        Returns:
            tuple: The grid cell corresponding to the given point as a tuple (x, y).
        """
        assert Coordinates.in_range(point), "Point outside GPS limits"
        
        gps_limits = Configuration.GPS_LIMIT
        if grid_size is None:
            grid_size = Configuration.GRID_SIZE
        
        lat_step = (gps_limits["lat"][1] - gps_limits["lat"][0]) / grid_size
        lng_step = (gps_limits["lng"][1] - gps_limits["lng"][0]) / grid_size
        
        x = int((point[0] - gps_limits["lat"][0]) / lat_step)
        y = int((point[1] - gps_limits["lng"][0]) / lng_step)
        
        return x, y

    @staticmethod
    def get_coordinate(cell):
        """
        Converts a grid cell to its corresponding geographical coordinate.

        Args:
            cell (tuple): The grid cell represented as a tuple (x, y).

        Returns:
            tuple: The geographical coordinate corresponding to the given cell as a tuple (latitude, longitude).
        """
        assert Coordinates.in_range_cell(cell), "Cell outside grid size"

        gps_limits = Configuration.GPS_LIMIT
        lat_step = (gps_limits["lat"][1] - gps_limits["lat"][0]) / Configuration.GRID_SIZE
        lng_step = (gps_limits["lng"][1] - gps_limits["lng"][0]) / Configuration.GRID_SIZE

        lat = gps_limits["lat"][0] + lat_step * cell[0]
        lng = gps_limits["lng"][0] + lng_step * cell[1]

        return lat, lng
