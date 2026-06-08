import numpy as np
def freq_axis(t: np.ndarray) -> np.ndarray:
    """
    Compute the FFT frequency axis for a uniformly sampled time array.

    Parameters
    ----------
    t : np.ndarray
        1D time array (s), uniformly spaced.

    Returns
    -------
    np.ndarray
        Frequency axis (Hz), centred (DC at index N//2).
    """
    N  = len(t)
    dt = t[1] - t[0]
    return np.fft.fftshift(np.fft.fftfreq(N, d=dt))


def pulse_spectrum(
    t: np.ndarray,
    E_t: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute the power spectrum of a pulse field via FFT.

    Parameters
    ----------
    t : np.ndarray
        Time array (s).
    E_t : np.ndarray
        Complex or real electric field envelope.

    Returns
    -------
    freq : np.ndarray
        Frequency axis (Hz), centred.
    S : np.ndarray
        Power spectral density (a.u.), centred.
    """
    freq = freq_axis(t)
    E_f  = np.fft.fftshift(np.fft.fft(E_t))
    S    = np.abs(E_f)**2
    return freq, S


# Quick self-test
t_test  = np.linspace(-1e-12, 1e-12, 512)
E_test  = np.exp(-t_test**2 / (2 * (100e-15)**2))
freq_t, S_t = pulse_spectrum(t_test, E_test)
assert S_t.shape == t_test.shape
assert freq_t[len(freq_t)//2] == 0.0 or abs(freq_t[len(freq_t)//2]) < 1e9
print("freq_axis     ✓")
print("pulse_spectrum ✓")