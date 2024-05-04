import math


class Distance:
    """
    A class for distance calculation.
    """

    @staticmethod
    def sq_euclidean(point_1, point_2):
        """
        Calculates the squared Euclidean distance between two points.

        Args:
            point_1 (tuple): The first point as a tuple (x, y).
            point_2 (tuple): The second point as a tuple (x, y).

        Returns:
            float: The squared Euclidean distance.
        """
        x_1, y_1 = point_1
        x_2, y_2 = point_2
        return (x_1 - x_2) ** 2 + (y_1 - y_2) ** 2

    @staticmethod
    def euclidean(point_1, point_2):
        """
        Calculates the Euclidean distance between two points.

        Args:
            point_1 (tuple): The first point as a tuple (x, y).
            point_2 (tuple): The second point as a tuple (x, y).

        Returns:
            float: The Euclidean distance.
        """
        return math.sqrt(Distance.sq_euclidean(point_1, point_2))

    @staticmethod
    def haversine(coord1, coord2):
        """
        Calculates the Haversine distance between two coordinates.

        Args:
            coord1 (tuple): The first coordinate as a tuple (lat, lng).
            coord2 (tuple): The second coordinate as a tuple (lat, lng).

        Returns:
            float: The Haversine distance.
        """
        radius = 6372800  # Earth radius in meters
        lat1, lng1 = coord1
        lat2, lng2 = coord2

        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lng2 - lng1)

        a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return radius * c

    @staticmethod
    def jsd(hist1, hist2):
        """
        Calculates the Jensen-Shannon divergence between two probability distributions.

        Args:
            hist1 (array-like): The first probability distribution.
            hist2 (array-like): The second probability distribution.

        Returns:
            float: The Jensen-Shannon divergence.
        """
        # Add your implementation here
        pass
