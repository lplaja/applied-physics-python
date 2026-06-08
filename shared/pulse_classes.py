
import numpy as np

class GaussianPulse:
    """Transform-limited Gaussian pulse with validated attributes."""

    c = 3e8

    def __init__(self, tau: float, wavelength: float, energy: float) -> None:
        # Use setters for validation from the start
        self.tau        = tau         # → calls self.tau.setter
        self.wavelength = wavelength
        self.energy     = energy

    # --- tau ---
    @property
    def tau(self) -> float:
        """1/e field half-width (s)."""
        return self._tau

    @tau.setter
    def tau(self, value: float) -> None:
        if value <= 0:
            raise ValueError(f"tau must be positive, got {value}")
        self._tau = float(value)

    # --- wavelength ---
    @property
    def wavelength(self) -> float:
        """Central wavelength (m)."""
        return self._wavelength

    @wavelength.setter
    def wavelength(self, value: float) -> None:
        if value <= 0:
            raise ValueError(f"wavelength must be positive, got {value}")
        self._wavelength = float(value)

    # --- energy ---
    @property
    def energy(self) -> float:
        """Pulse energy (J)."""
        return self._energy

    @energy.setter
    def energy(self, value: float) -> None:
        if value < 0:
            raise ValueError(f"energy must be non-negative, got {value}")
        self._energy = float(value)

    # --- computed properties (read-only) ---
    @property
    def frequency(self) -> float:
        """Central frequency ν₀ = c/λ₀ (Hz)."""
        return self.c / self.wavelength

    @property
    def fwhm(self) -> float:
        """Intensity FWHM (s)."""
        return 2 * np.sqrt(np.log(2)) * self.tau

    def __repr__(self) -> str:
        return (f"GaussianPulse(tau={self.tau*1e15:.1f} fs, "
                f"wavelength={self.wavelength*1e9:.0f} nm, "
                f"energy={self.energy*1e6:.1f} µJ)")

    def intensity(self, t: np.ndarray) -> np.ndarray:
        return np.exp(-t**2 / self.tau**2)

    def peak_power(self) -> float:
        return self.energy / (self.tau * np.sqrt(np.pi))

    def spectrum(self, t: np.ndarray):
        N  = len(t); dt = t[1] - t[0]
        E_f  = np.fft.fftshift(np.fft.fft(np.sqrt(self.intensity(t))))
        freq = np.fft.fftshift(np.fft.fftfreq(N, d=dt))
        return freq, np.abs(E_f)**2
    
class ChirpedPulse(GaussianPulse):
    """
    A Gaussian pulse with group delay dispersion (GDD).

    The chirped field in frequency domain:
        E_chirped(ω) = E_TL(ω) · exp(i · GDD/2 · ω²)
    """

    def __init__(
        self,
        tau: float,
        wavelength: float,
        energy: float,
        gdd: float,
    ) -> None:
        super().__init__(tau, wavelength, energy)   # delegate to parent
        self.gdd = gdd   # group delay dispersion (s²)

    @property
    def gdd(self) -> float:
        return self._gdd

    @gdd.setter
    def gdd(self, value: float) -> None:
        self._gdd = float(value)   # GDD can be negative

    @property
    def tau_chirped(self) -> float:
        """Chirped pulse duration: τ_c = τ √(1 + (GDD/τ²)²)."""
        return self.tau * np.sqrt(1 + (self.gdd / self.tau**2)**2)

    def __repr__(self) -> str:
        return (
            f"ChirpedPulse(tau={self.tau*1e15:.1f} fs, "
            f"wavelength={self.wavelength*1e9:.0f} nm, "
            f"energy={self.energy*1e6:.1f} µJ, "
            f"gdd={self.gdd*1e30:.0f} fs²)"
        )

    def intensity(self, t: np.ndarray) -> np.ndarray:
        """Override: chirped intensity has broader envelope."""
        return np.exp(-t**2 / self.tau_chirped**2)

    def spectrum(self, t: np.ndarray):
        """Override: apply GDD phase in frequency domain."""
        N  = len(t); dt = t[1] - t[0]
        E_TL = np.sqrt(np.exp(-t**2 / self.tau**2))
        freq  = np.fft.fftshift(np.fft.fftfreq(N, d=dt))
        ω     = 2 * np.pi * freq
        E_f   = np.fft.fftshift(np.fft.fft(E_TL))
        E_f  *= np.exp(0.5j * self.gdd * ω**2)
        return freq, np.abs(E_f)**2