# Robust Fingerprint of Location Trajectories Under Differential Privacy #

## Project Overview

This study is a pioneer in the use of fingerprinting techniques in conjunction with differential privacy protections to improve the security of trajectory data in studies of public transportation. The paper shows the effectiveness of the technique against various attacks and maintains significant data utility within privacy limitations using the Urbanmob dataset, which is enhanced for more data points collected from cab trajectories. The methodology uses a methodical approach to apply data modifications to mask individual travel patterns. It begins with correlation corrections and ends with the deployment of differential privacy. In addition to strengthening protection against potential data breaches, our multi-stage processing pipeline maintains data usability for traffic management and urban planning applications. Based on the analysis, it can be concluded that a scalable solution to support data privacy in sensitive transportation datasets and establish a standard for future privacy-focused studies across various data-driven domains can be achieved by strategically integrating advanced privacy-preserving techniques and purposeful data augmentation, while maintaining the detailed insights essential for effective public infrastructure analysis.
## Directory Structure


all the required packages can be downloaded using the imports.py file such as below
pip install numpy
pip install matplotlib
pip install tqdm
pip install enum34
pip install jsonlib2
pip install shapely
pip install scipy
pip install pandas
pip install dtaidistance
pip install bresenham
The directory structure of the project is organized as follows:

- `fingerprinting.py`: Contains methods for generating probabilistic fingerprints.
- `attack.py`: Implements different attack methods on trajectories.
- `sampling.py`: Helper functions for sampling used in fingerprinting and attack methods.
- `imports.py`: Import statements.
- `configuration.py`: Configuration settings.
- `README.md`: This file providing an overview of the project.
  


## Configuration

The `configuration.py` file contains settings and parameters used throughout the project. These include probabilities, thresholds, and other variables that control the behavior of fingerprinting and attack methods.

## Training the Model

Training the model involves generating probabilistic fingerprints for location trajectories. This is done using the `Fingerprinting` class in the `fingerprinting.py` module. Detailed instructions for training the model can be found in the docstrings of the relevant methods.

## Evaluating the Model

The model can be evaluated using various attack methods implemented in the `attack.py` module. These methods simulate real-world scenarios where an adversary tries to infer sensitive information from location trajectories. Evaluation involves applying these attack methods to fingerprinted trajectories and analyzing their effectiveness.

## Utilities

The `sampling.py` module contains utility functions for sampling used in both fingerprinting and attack methods. These functions facilitate the generation of probabilistic fingerprints and the implementation of attack strategies.


