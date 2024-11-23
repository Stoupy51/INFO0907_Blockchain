
# Imports
from print import *
import hashlib
import random
import numpy as np
from scipy.stats import chisquare

# Constants
BYTE_SIZE: int = 256				# Number of possible values for a byte

# Functions
@handle_error(exceptions=(ValueError,), error_log=3)
def frequency_test(data: bytes, p: float = 0.5, alpha: float = 0.05) -> tuple[float, bool]:
	""" Frequency test (monobit test) for randomness (f=p±√n)\n
	Args:
		data	(bytes):	Data to test for randomness
		p		(float):	Expected frequency of 1s (default: 0.5)
		alpha	(float):	Significance level for hypothesis test (default: 0.05)
	Returns:
		tuple[float, bool]: (p-value, whether test passed at significance level alpha)
	Raises:
		ValueError: If p is not between 0 and 1, or if alpha is not between 0 and 1
	"""
	# Input validation
	assert 0 <= p <= 1, "Expected frequency p must be between 0 and 1"
	assert 0 <= alpha <= 1, "Significance level alpha must be between 0 and 1"
	assert len(data) > 0, "Input data cannot be empty"

	# Convert bytes to bits and count 1s
	bits: str = "".join([f"{byte:08b}" for byte in data])
	ones: int = bits.count("1")
	n: int = len(bits)

	# Calculate observed and expected frequencies
	observed_freq: float = ones / n
	expected_freq: float = p

	# Calculate chi-square test statistic and p-value
	f_obs: np.ndarray = np.array([observed_freq, 1 - observed_freq])
	f_exp: np.ndarray = np.array([expected_freq, 1 - expected_freq])
	p_value: float = chisquare(f_obs, f_exp).pvalue

	# Test passes if we fail to reject null hypothesis
	passed: bool = p_value >= alpha
	return p_value, passed


# Test everything
if __name__ == "__main__":
	fake_data: bytes = bytes(random.randint(0, 255) for _ in range(1000))
	debug(f"Fake data: {''.join(f'{b:02X}' for b in fake_data)[:25]}...")
	info(f"Frequency test (p=0.5, alpha=0.05): {frequency_test(fake_data, p=0.5, alpha=0.05)}")
	pass

