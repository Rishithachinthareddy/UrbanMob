from sampling import Sampling

class Fingerprinting:
    """
    A class for generating probabilistic fingerprints for trajectories.
    """

    @staticmethod
    def probabilistic_fingerprint(trajectory, tau, p, theta, correlation, debug=False):
        """
        Generate a probabilistic fingerprint for a trajectory.

        Args:
            trajectory (list): The trajectory to generate the fingerprint for.
            tau (float): The transition threshold for sampling candidates.
            p (float): The initial probability of fingerprinting a cell.
            theta (float): The adjustment parameter for the probability.
            correlation (Correlation): The correlation model for emission and transition probabilities.
            debug (bool, optional): Enable debug mode. Defaults to False.

        Returns:
            tuple: The fingerprinted trajectory and the corresponding fingerprint flags.
        """
        fp_trajectory = []
        fp_flag = []
        assert p >= 0

        if p == 0:
            if debug:
                print("p = 0, return origin")
            for x_cell, y_cell, time in trajectory:
                fp_trajectory.append((x_cell, y_cell, time))
                fp_flag.append(0)
            return fp_trajectory, fp_flag

        block_count = 0
        fp_count = 0
        p_current = p

        x_cell, y_cell, true_time = trajectory[0]
        if debug:
            print("First cell truth: %5d, %5d, %10.2f" % (x_cell, y_cell, true_time))

        distribution = correlation.get_emission((x_cell, y_cell))

        (
            sampled_lat,
            sampled_lng,
        ), fp_state = Sampling.sample_proportionally_with_truth(
            distribution, (x_cell, y_cell), p_current
        )
        if debug:
            print("Sampled: ", sampled_lat, sampled_lng, "FP:", fp_state)

        prev_lat, prev_lng, prev_time = sampled_lat, sampled_lng, true_time

        fp_trajectory.append((sampled_lat, sampled_lng, true_time))
        fp_flag.append(fp_state)
        if fp_state:
            fp_count += 1
            if debug:
                print("FP!")

        block_count += 1

        for true_lat, true_lng, true_time in trajectory[1:]:
            if debug:
                print("Prev:", prev_lat, prev_lng, "Truth: ", true_lat, true_lng)

            (
                sampled_lat,
                sampled_lng,
            ), fp_state = Sampling.sample_candidates(
                (prev_lat, prev_lng),
                (true_lat, true_lng),
                p_current,
                tau,
                correlation,
                replace=True,
                debug=False,
            )

            if debug:
                print(
                    "Sampled: ",
                    sampled_lat,
                    sampled_lng,
                    "FP:",
                    fp_state,
                    "(p =",
                    p_current,
                    ")",
                )

            prev_lat, prev_lng, prev_time = sampled_lat, sampled_lng, true_time

            fp_trajectory.append((sampled_lat, sampled_lng, true_time))
            fp_flag.append(fp_state)
            if fp_state:
                fp_count += 1
                if debug:
                    print("FP!")

            block_count += 1

            if block_count >= math.ceil(1 / p):
                length = len(fp_trajectory)
                if debug:
                    print("FP_COUNT: %d, Expected: %.2f" % (fp_count, p * length))
                if fp_count > p * length:
                    p_current = p * (1 - theta)
                elif fp_count < p * length:
                    p_current = p * (1 + theta)
                else:
                    p_current = p

                if p_current >= 1:
                    p_current = 1

                block_count = 0

        return fp_trajectory, fp_flag
