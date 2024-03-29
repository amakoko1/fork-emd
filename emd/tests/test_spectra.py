"""Tests for instantaneous frequency and power spectra in emd.spectra."""

import unittest

import numpy as np


class TestSpectra(unittest.TestCase):
    """Ensure basic frequency transforms are working."""

    def setUp(self):
        """Set up data for testing."""
        # Create core signal
        seconds = 10
        self.sample_rate = 2000
        self.f1 = 5
        self.f2 = 18
        time_vect = np.linspace(0, seconds, int(seconds * self.sample_rate))

        self.x1 = np.cos(2 * np.pi * self.f1 * time_vect)[:, None]
        self.x2 = 2 * np.cos(2 * np.pi * self.f2 * time_vect)[:, None]

    def test_frequency_transform(self):
        """Ensure basic frequency transforms are working."""
        from ..spectra import frequency_transform

        tol = 1e-3  # Relatively generous tol due to edge effects

        # Check first signal
        IP, IF, IA = frequency_transform(self.x1, self.sample_rate, 'hilbert')
        assert(IP.max() - (2 * np.pi) < tol)
        assert(IP.min() < tol)
        assert(IA.mean() - 1 < tol)
        assert(IF.mean() - self.f1 < tol)

        # Check second signal
        IP, IF, IA = frequency_transform(self.x2, self.sample_rate, 'hilbert')
        assert(IP.max() - (2 * np.pi) < tol)
        assert(IP.min() < tol)
        assert(IA.mean() - 2 < tol)
        assert(IF.mean() - self.f2 < tol)

    def test_freq_from_phase(self):
        """Ensure we get correct instantaneous frequency from phase."""
        from ..spectra import freq_from_phase

        tst = freq_from_phase(np.linspace(0, 2 * np.pi, 48), 47)
        assert(np.allclose(tst, 1))

        tst = freq_from_phase(np.linspace(0, 2 * np.pi * .5, 48), 47)
        assert(np.allclose(tst, .5))

        tst = freq_from_phase(np.linspace(0, 2 * np.pi * 2, 48), 47)
        assert(np.allclose(tst, 2))

    def test_phase_from_freq(self):
        """Ensure we get correct instantaneous phase rom frequency."""
        from ..spectra import phase_from_freq

        tol = 1e-6

        phs = phase_from_freq(np.ones((100,)), sample_rate=100)
        assert(phs.max() - np.pi < tol)

    def test_hilberthunang_1d(self):
        """Ensure 1D Hilber-Huang Spectrum is working."""
        from ..spectra import hilberthuang

        IF = np.linspace(5, 15, 11)[:, None]
        IA = np.ones_like(IF)

        # We should 2 bins with 5 frequencies in each bin, top IF value is dropped.
        edges = np.linspace(5, 15, 3)
        f, spec = hilberthuang(IF, IA, edges, mode='amplitude', sum_imfs=False)
        assert(np.all(spec[:, 0] == [5, 5]))

        # We should 4 bins with 2 or 3 frequencies in each bin.
        edges = np.linspace(5, 15, 5)
        f, spec = hilberthuang(IF, IA, edges, mode='amplitude', sum_imfs=False)
        assert(np.all(spec[:, 0] == [3, 2, 3, 2]))

        IA = IA * 2
        # We should 2 bins with 5frequencies in each bin, energy should be 20
        # per bin (5*(2**2))
        edges = np.linspace(5, 15, 3)
        f, spec = hilberthuang(IF, IA, edges, mode='power', sum_imfs=False)
        assert(np.all(spec[:, 0] == [20, 20]))

    def test_hilberthuang(self):
        """Ensure 2D Hilber-Huang Spectrum is working."""
        from ..spectra import hilberthuang

        IF = np.linspace(0, 12, 13)[:, None]
        IA = np.ones_like(IF)
        edges = np.linspace(0, 13, 3)

        F, hht = hilberthuang(IF, IA, edges, sum_time=False)

        # Check total amplitude is equal in HHT and IA
        assert(hht.sum() == IA.sum())

        assert(np.all(hht[0, :7] == np.array([1., 1., 1., 1., 1., 1., 1.])))
        assert(np.all(hht[1, :7] == np.array([0., 0., 0., 0., 0., 0., 0.])))
        assert(np.all(hht[1, 7:] == np.array([1., 1., 1., 1., 1., 1.])))
        assert(np.all(hht[0, 7:] == np.array([0., 0., 0., 0., 0., 0.])))


class TestHistograms(unittest.TestCase):
    """Ensure histogram binning is working."""

    def test_hist_bins_from_data(self):
        """Check we get the right bins from data."""
        from ..spectra import define_hist_bins_from_data

        data = np.linspace(0, 1, 16)
        edges, bins = define_hist_bins_from_data(data, tol=0)

        assert(np.all(edges == np.array([0., .25, .5, .75, 1.])))
        assert(np.all(bins == np.array([0.125, 0.375, 0.625, 0.875])))

    def test_hist_bins(self):
        """Check we get the right bins from user definition."""
        from ..spectra import define_hist_bins

        edges, bins = define_hist_bins(0, 1, 5)

        edges = np.round(edges, 6)  # Sometimes returns float errors 0.30000000000000004
        bins = np.round(bins, 6)  # Sometimes returns float errors 0.30000000000000004

        assert(np.all(edges == np.array([0., 0.2, 0.4, 0.6, 0.8, 1.])))
        assert(np.all(bins == np.array([0.1, 0.3, 0.5, 0.7, 0.9])))


class TestHolospectrum(unittest.TestCase):
    """Ensure Holospectrum is working."""

    def test_holo(self):
        """Ensure Holospectrum is working."""
        from ..spectra import define_hist_bins, holospectrum

        f_edges1, f_bins1 = define_hist_bins(0, 10, 5)
        f_edges2, f_bins2 = define_hist_bins(0, 1, 5)

        if1 = np.array([2, 6])[:, None]
        if2 = np.array([.2, .3])[:, None, None]
        ia2 = np.array([1, 2])[:, None, None]

        fcarrier, fam, holo = holospectrum(if1, if2, ia2, f_edges1, f_edges2, sum_time=False)

        assert(np.all(holo.shape == (5, 5, 2)))
