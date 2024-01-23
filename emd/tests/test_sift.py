"""Tests for single-cycle analyses in emd.cycles."""

import unittest

import numpy as np
import pytest

from ..imftools import is_imf
from ..sift import (complete_ensemble_sift, ensemble_sift, get_config,
                    iterated_mask_sift, mask_sift, sift)
from ..simulate import abreu2010


class TestSiftDefaults(unittest.TestCase):
    """Ensure that all sift variants actually run with default options."""

    def setUp(self):
        """Set up data for testing."""
        # Create core signal
        seconds = 5.1
        sample_rate = 2000
        f1 = 2
        f2 = 18
        time_vect = np.linspace(0, seconds, int(seconds * sample_rate))

        x = abreu2010(f1, .2, 0, sample_rate, seconds)
        self.x = x + np.cos(2.3 * np.pi * f2 * time_vect) + np.linspace(-.5, 1, len(time_vect))

    def test_sift_default(self):
        """Check basic sift runs with some simple settings."""
        imf = sift(self.x)
        assert(imf.shape[0] == self.x.shape[0])  # just checking that it ran

    def test_ensemble_sift_default(self):
        """Check ensemble sift runs with some simple settings."""
        imf = ensemble_sift(self.x[:500], max_imfs=3)
        assert(imf.shape[0] == self.x[:500].shape[0])  # just checking that it ran

        imf = ensemble_sift(self.x[:500], max_imfs=3, noise_mode='flip')
        assert(imf.shape[0] == self.x[:500].shape[0])  # just checking that it ran

    def test_complete_ensemble_sift_default(self):
        """Check complete ensemble sift runs with some simple settings."""
        imf = complete_ensemble_sift(self.x[:200])
        assert(imf[0].shape[0] == self.x[:200].shape[0])  # just checking that it ran

    def test_mask_sift_default(self):
        """Check mask sift runs with some simple settings."""
        imf = mask_sift(self.x[:200], max_imfs=5, mask_freqs='zc')
        assert(imf.shape[0] == self.x[:200].shape[0])  # just checking that it ran

        imf = mask_sift(self.x[:200], max_imfs=5, mask_freqs='if')
        assert(imf.shape[0] == self.x[:200].shape[0])  # just checking that it ran

        imf = mask_sift(self.x[:200], max_imfs=5, mask_freqs=0.4)
        assert(imf.shape[0] == self.x[:200].shape[0])  # just checking that it ran

    def test_iterated_mask_sift_default(self):
        """Check mask sift runs with some simple settings."""
        imf = iterated_mask_sift(self.x[:200], max_imfs=5)
        assert(imf.shape[0] == self.x[:200].shape[0])  # just checking that it ran


class TestSiftEnsurance(unittest.TestCase):
    """Check that different inputs to sift work ok."""

    def setUp(self):
        """Set up signal for testing."""
        # Create core signal
        seconds = 5.1
        sample_rate = 2000
        f1 = 2
        f2 = 18
        time_vect = np.linspace(0, seconds, int(seconds * sample_rate))

        x = abreu2010(f1, .2, 0, sample_rate, seconds)
        self.x = x + np.cos(2.3 * np.pi * f2 * time_vect) + np.linspace(-.5, 1, len(time_vect))

    def test_get_next_imf_ensurance(self):
        """Ensure that get_next_imf works with expected inputs and errors."""
        from ..sift import get_next_imf

        # Check that various inputs to get_next_imf work or don't work
        # check 1d input ok
        imf, _ = get_next_imf(self.x)
        assert(imf.shape == (self.x.shape[0], 1))

        # check 1d+singleton is ok
        imf, _ = get_next_imf(self.x[:, np.newaxis])
        assert(imf.shape == (self.x.shape[0], 1))

        # check nd trailing singletons is ok
        imf, _ = get_next_imf(self.x[:, np.newaxis, np.newaxis])
        assert(imf.shape == (self.x.shape[0], 1))

        # check 2d raises error
        with pytest.raises(ValueError):
            xx = np.tile(self.x[:, np.newaxis], (1, 2))
            imf, _ = get_next_imf(xx)

        # check 3d raises error
        with pytest.raises(ValueError):
            xx = np.tile(self.x[:, np.newaxis, np.newaxis], (1, 2, 3))
            imf, _ = get_next_imf(xx)


class BaseTestSiftBehaviour(object):
    """Base class for testing basic sift behaviour.

    Base class doesn't inherit from unittest so tests within it aren't run -
    use multiple inheritance in child classes to add unittest

    This class implements 5 tests (four from: https://doi.org/10.1016/j.ymssp.2007.11.028)
    1) The sift should be a complete decomposition
    2) The sift of a signal multiplied by a constant should just scale the IMFs by that constant
    3) The sift of a signal with a constant added should only affect the final
        IMF, and should only increase it by the scalar
    4) The sift of an IMF should just return the IMF
    5) The sift of a time-reversed signal should return time-reversed but otherwise identical IMFs

    """

    def setUpClass(self):
        """Create signals for testing.

        This should create at least:

        self.x
        self.imf1
        self.imf_kwargs
        self.envelope_kwargs
        self.extrema_kwargs
        """
        raise NotImplementedError

    def test_complete_decomposition(self):
        """Ensure complete decomposition."""
        assert(np.allclose(self.imf1.sum(axis=1), self.x))

    def test_sift_multiplied_by_constant(self):
        """Ensure constant scaling only scales IMFs."""
        const = 3
        imf2 = sift(self.x*const, imf_opts=self.imf_kwargs,
                    envelope_opts=self.envelope_kwargs,
                    extrema_opts=self.extrema_kwargs)
        assert(np.allclose(self.imf1, imf2/const))
        assert(np.allclose(imf2.sum(axis=1)/const, self.x))

    def test_sift_plus_constant(self):
        """Ensure adding constant only affects final IMF."""
        const = 3
        imf2 = sift(self.x+const, imf_opts=self.imf_kwargs,
                    envelope_opts=self.envelope_kwargs,
                    extrema_opts=self.extrema_kwargs)
        assert(np.allclose(self.imf1[:, :2], imf2[:, :2]))
        assert(np.allclose(self.imf1[:, 2]+const, imf2[:, 2]))

    def test_sift_of_imf(self):
        """Ensure sift of an IMF is that same IMF."""
        # Test sift of an IMF - Need to relax criteria as edges effects can be
        # amplified by repeated sifting
        imf2 = sift(self.imf1[:, 0], imf_opts=self.imf_kwargs,
                    envelope_opts=self.envelope_kwargs,
                    extrema_opts=self.extrema_kwargs)
        assert(np.allclose(imf2[:, 0], self.imf1[:, 0], atol=0.02))

        imf2 = sift(self.imf1[:, 1], imf_opts=self.imf_kwargs,
                    envelope_opts=self.envelope_kwargs,
                    extrema_opts=self.extrema_kwargs)
        assert(np.allclose(imf2[:, 0], self.imf1[:, 1], atol=0.02))

    def test_sift_of_reversed_signal(self):
        """Ensure sift of time-reversed signal returns reversed-but-identical IMFs."""
        # Test sift of reversed signal - very much increased criteria
        extrema_kwargs = self.extrema_kwargs.copy()
        extrema_kwargs['method'] = 'numpypad'  # Rilling not working here for some reason
        imf2 = sift(self.x[::-1], imf_opts=self.imf_kwargs,
                    envelope_opts=self.envelope_kwargs,
                    extrema_opts=extrema_kwargs)
        assert(np.allclose(self.imf1, imf2[::-1, :], atol=0.1))

        # Should be fine in the middle though...
        assert(np.allclose(self.imf1[3000:7000, :],
                           imf2[::-1, :][3000:7000, :],
                           atol=0.02))


class TestSiftBehaviour(unittest.TestCase, BaseTestSiftBehaviour):
    """Test sift behaviour on simple signal."""

    @classmethod
    def setUpClass(cls):
        """Set up data and IMFs for testing."""
        # Create core signal
        seconds = 5.1
        sample_rate = 2000
        f1 = 2
        f2 = 18
        time_vect = np.linspace(0, seconds, int(seconds * sample_rate))

        x = abreu2010(f1, .2, 0, sample_rate, seconds)
        cls.x = x + np.cos(2.3 * np.pi * f2 * time_vect) + np.linspace(-.5, 1, len(time_vect))

        cls.imf_kwargs = {}
        cls.envelope_kwargs = {'interp_method': 'splrep'}
        cls.extrema_kwargs = {}
        cls.imf1 = sift(cls.x, imf_opts=cls.imf_kwargs,
                        envelope_opts=cls.envelope_kwargs,
                        extrema_opts=cls.extrema_kwargs)


class TestMaskSiftBehaviour(unittest.TestCase):
    """Ensure that sifted IMFs meet certain criteria."""

    def get_resid(self, x, x_bar):
        """Get residual from signal and IMF."""
        ss_orig = np.power(x, 2).sum()
        ss_resid = np.power(x - x_bar, 2).sum()
        return (ss_orig - ss_resid) / ss_orig

    def check_diff(self, val, target, eta=1e-3):
        """Assess difference between two signals."""
        return np.abs(val - target) < eta

    @classmethod
    def setUpClass(cls):
        """Set up data and IMFs for testing."""
        # Create core signal
        seconds = 5.1
        cls.sample_rate = 2000
        f1 = 2
        f2 = 17  # Has exact division into 5.1 seconds
        time_vect = np.linspace(0, seconds, int(seconds * cls.sample_rate))

        x = abreu2010(f1, .2, 0, cls.sample_rate, seconds)
        cls.x = x + np.cos(2 * np.pi * f2 * time_vect) + np.linspace(-.5, 1, len(time_vect))

        cls.imf_kwargs = {}
        cls.envelope_opts = {'interp_method': 'splrep'}
        cls.imf = sift(cls.x, imf_opts=cls.imf_kwargs, envelope_opts=cls.envelope_opts)

    # Test mask sifts
    def test_get_next_imf_mask(self):
        """Test that get_next_imf_mask works as expected."""
        from ..sift import get_next_imf_mask

        # sift with mask above signal should return zeros
        # mask has to be waaay above signal in a noiseless time-series
        next_imf, continue_flag = get_next_imf_mask(self.imf[:, 0, None], 0.25, 1)
        mask_power = np.sum(np.power(next_imf, 2))

        assert(mask_power < 1)

        # sift with mask below signal should return original signal
        next_imf, continue_flag = get_next_imf_mask(self.imf[:, 0, None], 0.0001, 1)
        power = np.sum(np.power(self.imf[:, 0], 2))
        mask_power = np.sum(np.power(next_imf, 2))

        assert(power - mask_power < 1)

    def test_get_mask_freqs(self):
        """Test API of get_mask_freqs."""
        from ..sift import get_mask_freqs

        # Values outside of 0 <= x < 0.5 raise an error
        self.assertRaises(ValueError, get_mask_freqs, self.x, 0.55)
        self.assertRaises(ValueError, get_mask_freqs, self.x, 5)
        self.assertRaises(ValueError, get_mask_freqs, self.x, -1)

        # Values within 0 <= x < 0.5 return themselves
        assert(get_mask_freqs(self.x, first_mask_mode=0.1) == 0.1)
        assert(get_mask_freqs(self.x, first_mask_mode=0.45894) == 0.45894)

        # ZC of sinusoid should return pretty much sinusoid freq
        target = 2 / self.sample_rate
        assert(np.allclose(get_mask_freqs(self.imf[:, 1], 'zc'), target, atol=1e-3))

        target = 17 / self.sample_rate
        assert(np.allclose(get_mask_freqs(self.imf[:, 0], 'zc'), target, atol=1e-3))

        # IF of sinusoid should return pretty much sinusoid freq
        target = 2 / self.sample_rate
        assert(np.allclose(get_mask_freqs(self.imf[:, 1], 'if'), target, atol=1e-3))

        target = 17 / self.sample_rate
        assert(np.allclose(get_mask_freqs(self.imf[:, 0], 'if'), target, atol=1e-3))


class TestSecondLayerSift(unittest.TestCase):
    """Check second layer sifting is behaving itself."""

    @classmethod
    def setUpClass(cls):
        """Housekeeping and preparation."""
        cls.seconds = 10
        cls.sample_rate = 200
        cls.t = np.linspace(0, cls.seconds, cls.seconds*cls.sample_rate)

        cls.f_slow = 5  # Frequency of slow oscillation
        cls.f_slow_am = 0.5  # Frequency of slow amplitude modulation
        cls.a_slow_am = 0.5  # Amplitude of slow amplitude modulation

        cls.f_fast = 37  # Frequency of fast oscillation
        cls.a_fast = 0.5  # Amplitude of fast oscillation
        cls.f_fast_am = 5  # Frequency of fast amplitude modulation
        cls.a_fast_am = 0.5  # Amplitude of fast amplitude modulation

        # First we create a slow 4.25Hz oscillation with a 0.5Hz amplitude modulation
        cls.slow_am = (cls.a_slow_am+(np.cos(2*np.pi*cls.f_slow_am*cls.t)/2))
        cls.slow = cls.slow_am * np.sin(2*np.pi*cls.f_slow*cls.t)

        # Second, we create a faster 37Hz oscillation that is amplitude modulated by the first.
        cls.fast_am = (cls.a_fast_am+(np.cos(2*np.pi*cls.f_fast_am*cls.t)/2))
        cls.fast = cls.fast_am * np.sin(2*np.pi*cls.f_fast*cls.t)

        # We create our signal by summing the oscillation and adding some noise
        cls.x = cls.slow+cls.fast

    def test_second_layer_mask_sift_slow(self):
        """Check that carrier and am frequencies of slower component can be found."""
        from ..sift import mask_sift, mask_sift_second_layer
        from ..spectra import frequency_transform

        # Just checking slow component for now
        imf, masks = mask_sift(self.slow, max_imfs=4, ret_mask_freq=True)
        IP, IF, IA = frequency_transform(imf, self.sample_rate, 'hilbert')

        # Only checking for ballpark accuracy here
        assert(np.allclose(np.average(IF[:, 0], weights=IA[:, 0]), self.f_slow, atol=1))

        # Sift the first level IMFs
        self.imf2 = mask_sift_second_layer(IA, masks, sift_args={'max_imfs': 3})
        self.IP2, self.IF2, self.IA2 = frequency_transform(self.imf2, self.sample_rate, 'hilbert')

        assert(np.allclose(np.average(self.IF2[:, 0], weights=self.IA2[:, 0]), self.f_slow_am, atol=1))

    def test_second_layer_mask_sift_fast(self):
        """Check that carrier and am frequencies of faster component can be found."""
        from ..sift import mask_sift, mask_sift_second_layer
        from ..spectra import frequency_transform

        # Just checking fast component for now
        imf, masks = mask_sift(self.fast, max_imfs=4, ret_mask_freq=True, mask_amp_mode='ratio_imf')
        IP, IF, IA = frequency_transform(imf, self.sample_rate, 'hilbert')

        # Only checking for ballpark accuracy here
        assert(np.allclose(np.average(IF[:, 0], weights=IA[:, 0]), self.f_fast, atol=1))

        # Sift the first level IMFs
        self.imf2 = mask_sift_second_layer(IA, masks, sift_args={'max_imfs': 3, 'mask_amp_mode': 'ratio_imf'})
        self.IP2, self.IF2, self.IA2 = frequency_transform(self.imf2, self.sample_rate, 'hilbert')

        assert(np.allclose(np.average(self.IF2[:, 0], weights=self.IA2[:, 0]), self.f_fast_am, atol=1))


class TestSiftConfig(unittest.TestCase):
    """Ensure that sift configs work properly."""

    def test_config(self):
        """Check SiftConfig creation and editing."""
        # Get sift config
        conf = get_config('sift')
        # Check a couple of options
        assert(conf['max_imfs'] is None)
        assert(conf['extrema_opts/pad_width'] == 2)
        assert(conf['extrema_opts/loc_pad_opts/mode'] == 'reflect')

        # Get ensemble sift config
        conf = get_config('ensemble_sift')
        # Check a couple of options
        assert(conf['max_imfs'] is None)
        assert(conf['extrema_opts/pad_width'] == 2)
        assert(conf['extrema_opts/loc_pad_opts/mode'] == 'reflect')

        # Get mask sift config
        conf = get_config('ensemble_sift')
        # Check a couple of options
        assert(conf['nensembles'] == 4)
        assert(conf['max_imfs'] is None)
        assert(conf['extrema_opts/pad_width'] == 2)
        assert(conf['extrema_opts/loc_pad_opts/mode'] == 'reflect')

    def test_sift_config_saveload_yaml(self):
        """Check SiftConfig saving and loading."""
        import tempfile

        from ..sift import SiftConfig

        # Get sift config
        config = get_config('mask_sift')

        config_file = tempfile.NamedTemporaryFile(prefix="ExampleSiftConfig_").name

        # Save the config into yaml format
        config.to_yaml_file(config_file)

        # Load the config back into a SiftConfig object for use in a script
        new_config = SiftConfig.from_yaml_file(config_file)

        assert(new_config.sift_type == 'mask_sift')


class TestIsIMF(unittest.TestCase):
    """Ensure that we can validate IMFs."""

    def setUp(self):
        """Set up data for testing."""
        # Create core signal
        seconds = 5.1
        sample_rate = 2000
        f1 = 2
        f2 = 18
        time_vect = np.linspace(0, seconds, int(seconds * sample_rate))

        x = abreu2010(f1, .2, 0, sample_rate, seconds)
        self.x = x + np.cos(2.3 * np.pi * f2 * time_vect) + np.linspace(-.5, 1, len(time_vect))

        self.y = np.sin(2 * np.pi * 5 * time_vect)

    def test_is_imf_on_sinusoid(self):
        """Make sure a pure sinusoid is an IMF."""
        out = is_imf(self.y)

        # Should be true on both criteria
        assert(np.all(out))

    def test_is_imf_on_abreu(self):
        """Make sure the Abreu signal is an IMF."""
        imf = sift(self.x)
        out = is_imf(imf)

        # Should be true on both criteria
        assert(np.all(out[0, :]))

        # Should be true on both criteria
        assert(np.all(out[1, :]))

        # Trend is not an IMF, should be false on both criteria
        assert(np.all(out[2, :] == False))  # noqa: E712


class TestSiftUtils(unittest.TestCase):
    """Ensure envelopes and extrema are behaving."""

    def setUp(self):
        """Set up data for testing."""
        sample_rate = 1280
        seconds = 10

        time_vect = np.linspace(0, seconds, seconds*sample_rate)
        f = 5

        self.X = np.zeros((len(time_vect), 5))
        self.X[:, 0] = np.sin(2*np.pi*f*time_vect)
        self.X[:, 1] = np.sin(2*np.pi*f*time_vect+np.pi/3)
        self.X[:, 2] = np.sin(2*np.pi*f*time_vect+np.pi*1.63)
        self.X[:, 3] = np.cos(2*np.pi*f*2*time_vect+np.pi/2)
        self.X[:, 4] = np.sin(2*np.pi*f*5*time_vect)

    def test_num_extrema(self):
        """Check that various methods find correct number of extrema."""
        from ..sift import get_padded_extrema

        # Check extrema without padding
        extr = [50, 50, 50, 100, 250]
        for ii in range(5):
            l, m = get_padded_extrema(self.X[:, ii], pad_width=0, mode='peaks', method='numpypad')
            assert(len(l) == extr[ii])
            assert(len(m) == extr[ii])

        for ii in range(5):
            l, m = get_padded_extrema(self.X[:, ii], pad_width=0, mode='troughs', method='numpypad')
            assert(len(l) == extr[ii])
            assert(len(m) == extr[ii])

        # Check extrema without padding - both at once
        extr = [50, 50, 50, 100, 250]
        for ii in range(5):
            l, m, l2, m2 = get_padded_extrema(self.X[:, ii], pad_width=0, mode='both', method='numpypad')
            assert(len(l) == extr[ii])
            assert(len(m) == extr[ii])
            assert(len(l2) == extr[ii])
            assert(len(m2) == extr[ii])

    def test_numpypad_padding(self):
        """Check that numpypad options are working."""
        from ..sift import get_padded_extrema

        pads = [0, 1, 5, 10]
        extr = 50
        for ii in range(len(pads)):
            l, m = get_padded_extrema(self.X[:, 0], pad_width=pads[ii], mode='peaks', method='numpypad')
            assert(len(l) == extr+2*pads[ii])
            assert(len(m) == extr+2*pads[ii])

    def test_rilling_padding(self):
        """Check that numpypad options are working."""
        from ..sift import get_padded_extrema

        # Rilling method returns peaks and troughs in both mode
        out = get_padded_extrema(self.X[:, 0], pad_width=3, mode='both', method='rilling')
        assert(len(out) == 4)

        # Rilling method returns only peaks when only peaks are requested
        out = get_padded_extrema(self.X[:, 0], pad_width=3, mode='peaks', method='rilling')
        assert(len(out) == 2)

        pads = [0, 1, 5, 10]
        extr = 50
        for ii in range(len(pads)):
            lp, mp, lt, mt = get_padded_extrema(self.X[:, 0], pad_width=pads[ii], mode='both', method='rilling')
            assert(len(lp) == extr+2*pads[ii])
            assert(len(mp) == extr+2*pads[ii])

    def test_envelope_interpolation(self):
        """Ensure envelope interpolation is sensible."""
        from ..sift import interp_envelope

        env = interp_envelope(self.X[:, 2])
        # Envelope shapes match input
        assert(env[0].shape[0] == self.X.shape[0])
        assert(env[1].shape[0] == self.X.shape[0])

        # Envelopes are sufficiently close to +/-1
        assert(np.sum((1-env[0])**2) < 1e-3)
        assert(np.sum((1+env[1])**2) < 1e-3)

    def test_zero_crossing_count(self):
        """Ensure we're finding right number of zero crossings."""
        # Use different sinusoids for this one
        from ..sift import zero_crossing_count
        seconds = 5.1
        sample_rate = 1000
        time_vect = np.linspace(0, seconds, int(seconds*sample_rate))

        x = np.sin(2*np.pi*2*time_vect)
        assert(zero_crossing_count(x) == 21)

        x = np.sin(2*np.pi*17*time_vect)
        assert(zero_crossing_count(x) == 174)
