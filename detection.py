import numpy as np
from configuration import Configuration


class Detection:
    """
    A class for detecting similarity between trajectories.
    """

    @staticmethod
    def similarity_detection(leak_trajectory, candidates):
        """
        Perform similarity detection between a leak trajectory and a list of candidate trajectories.

        Args:
            leak_trajectory (list): The leak trajectory as a list of tuples (lat, lng, _).
            candidates (list): The candidate trajectories as a list of tuples (trajectory, _).

        Returns:
            tuple: The index of the most similar candidate trajectory and the similarity scores.
        """
        num_candidates = len(candidates)
        scores = np.zeros(num_candidates)
        length = len(leak_trajectory)

        for i, (leak_lat, leak_lng, _) in enumerate(leak_trajectory):
            distances = np.zeros(num_candidates)

            for j, (cand_trajectory, _) in enumerate(candidates):
                cand_lat, cand_lng, _ = cand_trajectory[i]
                distances[j] = (leak_lat - cand_lat) ** 2 + (leak_lng - cand_lng) ** 2

            min_distance = np.min(distances)
            min_indices = np.where(distances == min_distance)[0]
            scores[min_indices] += 1 / length

        most_similar_index = np.argmax(scores)
        return most_similar_index, scores
