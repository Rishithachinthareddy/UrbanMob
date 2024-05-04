from collections import defaultdict
from configuration import Configuration
from coordinates import Coordinates
from distance import Distance


class Correlation:
    """
    A class for computing correlation-based transition and emission probabilities.
    """

    def __init__(self, prior_knowledge):
        """
        Initializes the Correlation class with prior knowledge.

        Args:
            prior_knowledge (list): Prior knowledge of cell trajectories.
        """
        self.emission, self.transition = self.generate_correlation_model(prior_knowledge)

    def generate_correlation_model(self, prior):
        """
        Generate correlation model from prior knowledge.

        Args:
            prior (list): Prior knowledge of cell trajectories.

        Returns:
            tuple: Emission and transition dictionaries.
        """
        emission = defaultdict(int)
        transition = defaultdict(lambda: defaultdict(int))

        for cell_trajectory in prior:
            for prev_point, curr_point in zip(cell_trajectory, cell_trajectory[1:]):
                prev_cell = Coordinates.get_cell(prev_point)
                curr_cell = Coordinates.get_cell(curr_point)
                transition[prev_cell][curr_cell] += 1
                emission[curr_cell] += 1

        return emission, transition

    def get_transition(self, prior):
        """
        Compute the transition probabilities from the prior cell.

        Args:
            prior (tuple): The prior cell as a tuple (x, y).

        Returns:
            dict: The transition probabilities to neighboring cells.
        """
        x, y = prior
        local_transition = {}
        total_transition = sum(self.transition[(x, y)].values())

        if total_transition <= 0:
            local_transition = {
                (x_cell, y_cell): 1
                for x_cell in range(x - Configuration.NEIGHBOR_RANGE, x + Configuration.NEIGHBOR_RANGE + 1)
                for y_cell in range(y - Configuration.NEIGHBOR_RANGE, y + Configuration.NEIGHBOR_RANGE + 1)
                if Coordinates.in_range_cell((x_cell, y_cell))
            }
        else:
            local_transition = {
                key: value / total_transition
                for key, value in self.transition[(x, y)].items()
            }

        return {key: 1 / len(local_transition) for key in local_transition}

    def get_vanilla_transition(self, prior):
        """
        Retrieve the original (non-normalized) transition probabilities from the prior cell.

        Args:
            prior (tuple): The prior cell as a tuple (x, y).

        Returns:
            dict: The original transition probabilities to neighboring cells.
        """
        return self.transition.get(prior, {})

    def get_emission(self, prior):
        """
        Compute the emission probabilities from the prior cell.

        Args:
            prior (tuple): The prior cell as a tuple (x, y).

        Returns:
            dict: The emission probabilities to neighboring cells.
        """
        x, y = prior
        local_emission = {
            (x_cell, y_cell): self.emission[(x_cell, y_cell)]
            for x_cell in range(x - Configuration.NEIGHBOR_RANGE, x + Configuration.NEIGHBOR_RANGE + 1)
            for y_cell in range(y - Configuration.NEIGHBOR_RANGE, y + Configuration.NEIGHBOR_RANGE + 1)
            if Coordinates.in_range_cell((x_cell, y_cell))
        }
        total_emission = sum(local_emission.values())

        return {key: value / total_emission for key, value in local_emission.items()}

    def get_all_transition(self, prev_point, true_point, tau, consider_distance=True):
        """
        Compute all possible transitions from the previous point.

        Args:
            prev_point (tuple): The previous point as a tuple (x, y).
            true_point (tuple): The true point as a tuple (x, y).
            tau (float): The correlation threshold.
            consider_distance (bool): Whether to consider the distance threshold (default: True).

        Returns:
            tuple: The transition dictionaries (candidates, tau_candidates, tau_dist_candidates).
        """
        candidates = self.get_transition(prev_point)
        tau_candidates = {k: v for k, v in candidates.items() if v >= tau}

        if consider_distance:
            dist = Distance.sq_euclidean(prev_point, true_point)
            tau_dist_candidates = {
                k: v for k, v in tau_candidates.items() if Distance.sq_euclidean(k, true_point) <= dist
            }
            return candidates, tau_candidates, tau_dist_candidates
        else:
            return candidates, tau_candidates
