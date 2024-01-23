API
================

This page is the reference for the functions in the EMD package. Further
details can be found on the page for each individual function.

Sift Functions
*********************

Primary user-level functions for running the sift.

.. autosummary::
     :toctree: stubs

     emd.sift.sift
     emd.sift.ensemble_sift
     emd.sift.complete_ensemble_sift
     emd.sift.mask_sift
     emd.sift.iterated_mask_sift
     emd.sift.sift_second_layer
     emd.sift.mask_sift_second_layer


Sift Utilities
*********************

Low-level utility functions used by the sift routines.

.. autosummary::
     :toctree: stubs

     emd.sift.get_config
     emd.sift.get_next_imf
     emd.sift.get_next_imf_mask
     emd.sift.interp_envelope
     emd.sift.get_padded_extrema
     emd.sift.fixed_stop
     emd.sift.sd_stop
     emd.sift.rilling_stop
     emd.sift.energy_stop

Frequency Functions
*********************

Computing frequency transforms from narrow band oscillations (IMFs).

.. autosummary::
     :toctree: stubs

     emd.spectra.frequency_transform
     emd.spectra.phase_from_complex_signal
     emd.spectra.freq_from_phase
     emd.spectra.phase_from_freq

Spectrum Functions
*********************

Compute Hilbert-Huang and Holospectra from instantaneous frequency data.

.. autosummary::
     :toctree: stubs

     emd.spectra.hilberthuang
     emd.spectra.holospectrum
     emd.spectra.hilbertmarginal

Spectrum Utilities
*********************

Low-level helper functions for spectrum computations.

.. autosummary::
     :toctree: stubs

     emd.spectra.define_hist_bins
     emd.spectra.define_hist_bins_from_data

IMF-Tools
*********************

Assess and analyse IMFs and their derivatives.

.. autosummary::
   :toctree: stubs

    emd.imftools.amplitude_normalise
    emd.imftools.wrap_phase
    emd.imftools.zero_crossing_count
    emd.imftools.is_imf
    emd.imftools.est_orthogonality
    emd.imftools.check_decreasing_freq
    emd.imftools.pseudo_mode_mixing_index
    emd.imftools.assess_harmonic_criteria
    emd.imftools.assess_joint_if
    emd.imftools.apply_epochs
    emd.imftools.find_extrema_locked_epochs

Simulate
*********************

Create artificial oscillations.

.. autosummary::
   :toctree: stubs

    emd.simulate.ar_oscillator
    emd.simulate.abreu2010
    emd.simulate.compute_joint_if


Cycle Analysis
*********************

Identify and analyse single cycles of an oscillation.

.. autosummary::
     :toctree: stubs

     emd.cycles.Cycles
     emd.cycles.get_cycle_vector
     emd.cycles.get_cycle_stat
     emd.cycles.get_control_points
     emd.cycles.phase_align
     emd.cycles.normalised_waveform
     emd.cycles.bin_by_phase
     emd.cycles.mean_vector
     emd.cycles.kdt_match

Package Utilities
*********************

Routines related to python, logging and installation.

.. autosummary::
     :toctree: stubs

     emd.support.get_install_dir
     emd.support.get_installed_version
     emd.logger.set_up
