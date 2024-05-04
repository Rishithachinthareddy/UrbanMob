import math
import random
import numpy as np
from collections import defaultdict
from joblib import Parallel, delayed
from scipy.stats import kendalltau
from fastdtw import dtw_ndim

class Evaluation:
    """
    A class for evaluating privacy-preserving techniques.
    """

    @staticmethod
    def generate_sample_dataset(selected_trajectories, fp_ratio, tau, theta, correlation, debug=False):
        """
        Generates sample datasets by applying a fingerprinting method to a selected trajectory.

        Args:
            selected_trajectories (list): Selected trajectory data.
            fp_ratio (float): False positive ratio.
            tau (float): Correlation threshold.
            theta (float): Balancing factor.
            correlation (object): Correlation model.
            debug (bool): Debug flag.

        Returns:
            list: Generated copies of the selected trajectories.
        """
        sample_dataset = []
        if debug:
            print("Generating fingerprinted copies.")
        for selected_trajectory in selected_trajectories:
            sample_dataset.append(Fingerprinting.probabilistic_fingerprint(selected_trajectory, tau, fp_ratio, theta, correlation, debug=False)[0])
        return sample_dataset

    @staticmethod
    def evaluate_utility(orig_dataset, dp_dataset, utility_metric, fp_ratio, tau, theta, correlation, grid_size=10, debug=False):
        """
        Evaluates the utility of the differential privacy (DP) dataset against the original dataset based on a specified utility metric.

        Args:
            orig_dataset (list): The original dataset.
            dp_dataset (list): The protected dataset.
            utility_metric (EvaluationMetric): The utility metric.
            fp_ratio (float): The fingerprinting ratio.
            tau (float): Correlation threshold.
            theta (float): Balancing factor.
            correlation (object): Correlation model.
            grid_size (int, optional): Size of the grid over which some evaluation metrics are calculated. Defaults to 10.
            debug (bool, optional): Debug flag.

        Returns:
            float: The result of the evaluation based on the specified utility metric.

        Raises:
            RuntimeError: If an invalid utility metric is provided.
        """
        fp_dataset = Evaluation.generate_sample_dataset(dp_dataset, fp_ratio, tau, theta, correlation, debug=debug)
        if utility_metric == EvaluationMetric.QA_POINTS:
            return Evaluation.eval_area_query_answering(orig_dataset, fp_dataset, grid_size=grid_size)
        elif utility_metric == EvaluationMetric.QA_PATTERNS:
            return Evaluation.eval_pattern_query_answering(orig_dataset, fp_dataset, grid_size=grid_size)
        elif utility_metric == EvaluationMetric.AREA_POPULARITY:
            return Evaluation.eval_popularity(orig_dataset, fp_dataset, grid_size=grid_size)
        elif utility_metric == EvaluationMetric.TRIP_ERROR:
            return Evaluation.eval_trip_error(orig_dataset, fp_dataset, grid_size=grid_size)
        elif utility_metric == EvaluationMetric.DIAMETER_ERROR:
            return Evaluation.eval_diameter_error(orig_dataset, fp_dataset, grid_size=grid_size)
        elif utility_metric == EvaluationMetric.TRIP_SIMILARITY:
            return Evaluation.evaluate_dtw_distance(orig_dataset, fp_dataset)
        else:
            raise RuntimeError("Invalid utility metric.")

    @staticmethod
    def evaluate_detection_accuracy(data, trial_rep_count, sub_trial_rep_count, trajectory_count, party_count, trajectory_length, fp_ratio, attack, correlation_model, tau=Configuration.TAU, theta=Configuration.THETA, attack_ratio=0.8, collusion_count=3, p_estimate=None, debug=False, parallel=False):
        """
        Evaluate the detection accuracy of a privacy-preserving technique.

        Args:
            data (list): The dataset.
            trial_rep_count (int): The number of trial repetitions.
            sub_trial_rep_count (int): The number of sub-trial repetitions.
            trajectory_count (int): The number of trajectories.
            party_count (int): The number of parties.
            trajectory_length (int): The length of trajectories.
            fp_ratio (float): The fingerprinting ratio.
            attack (Attack): The attack type.
            correlation_model (object): The correlation model.
            tau (float, optional): The threshold for similarity detection. Defaults to Configuration.TAU.
            theta (float, optional): The threshold for probabilistic fingerprinting. Defaults to Configuration.THETA.
            attack_ratio (float, optional): The attack ratio. Defaults to 0.8.
            collusion_count (int, optional): The number of colluding parties. Defaults to 3.
            p_estimate (float, optional): The probability estimate for probabilistic collusion attack. Defaults to None.
            debug (bool, optional): Enable debug mode. Defaults to False.
            parallel (bool, optional): Enable parallel execution. Defaults to False.

        Returns:
            float: The average detection accuracy.
        """
        def single_trial(trial_index, sub_trial_rep_count, data, trajectory_count, party_count, fp_ratio, attack, correlation_model, tau, theta, attack_ratio, collusion_count, p_estimate, debug):
            if debug:
                print("Trial # {}".format(trial_index))
            selected_trajectories = Sampling.sample_count(data, trajectory_count)

            copies = [[] for _ in range(party_count)]
            aux_info = []
            for trajectory_id, selected_trajectory in enumerate(selected_trajectories):
                selected_trajectory = selected_trajectory[:trajectory_length]

                if debug:
                    print("Generating fingerprinted copies.")

                for party_index in range(party_count):
                    copies[party_index].append(Fingerprinting.probabilistic_fingerprint(selected_trajectory, tau, fp_ratio, theta, correlation_model, debug=False))

            results = np.zeros(sub_trial_rep_count)
            if debug:
                print("Performing attack...")
            for sub_trial_index in range(sub_trial_rep_count):
                if attack == Attack.correlation_attack or attack == Attack.random_distortion_attack:
                    assert attack_ratio
                    leak_party_indexes = Sampling.sample_count(party_count, 1)
                else:
                    assert collusion_count > 1
                    leak_party_indexes = Sampling.sample_count(party_count, collusion_count)

                sus
