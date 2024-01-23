"""Tests for imftools."""

import unittest

import numpy as np
import pandas as pd


class TestAssessHarmonicCriteria(unittest.TestCase):
    """Ensure that all sift variants actually run with default options."""

    @classmethod
    def setUpClass(cls):
        """Create some signals for testing."""
        cls.sample_rate = 512
        cls.seconds = 10
        cls.time = np.linspace(0, cls.seconds, cls.seconds*cls.sample_rate)

        cls.x = np.sin(2*np.pi*5*cls.time)
        cls.y = np.sin(2*np.pi*10*cls.time)
        cls.z = np.sin(2*np.pi*15*cls.time)

        cls.imfs = np.vstack((cls.x, cls.y, cls.z)).T

        from ..spectra import frequency_transform
        cls.IP, cls.IF, cls.IA = frequency_transform(cls.imfs, cls.sample_rate, 'hilbert')

    def test_input_length(self):
        """Smoke test to make sure that it runs without error."""
        from ..imftools import assess_harmonic_criteria

        # Equal segment lengths
        df = assess_harmonic_criteria(self.IP, self.IF, self.IA, num_segments=10)
        assert(isinstance(df, pd.DataFrame))

        # Unequal segment lengths
        df = assess_harmonic_criteria(self.IP, self.IF, self.IA, num_segments=7)
        assert(isinstance(df, pd.DataFrame))
