import numpy as np
from dataclasses import dataclass

class OpticalElement:
    """Abstract base for ABCD optical elements."""

    def matrix(self) -> np.ndarray:
        """Return the 2×2 ABCD ray transfer matrix."""
        raise NotImplementedError("Subclasses must implement matrix()")

    def __matmul__(self, other):
        """Compose two elements: (self @ other).matrix() = self.matrix() @ other.matrix()."""
        if isinstance(other, OpticalElement):
            M = self.matrix() @ other.matrix()
            return _MatrixElement(M)
        return NotImplemented

    def propagate(self, ray: np.ndarray) -> np.ndarray:
        """Apply this element to a ray [y, θ]."""
        return self.matrix() @ ray

    def __repr__(self) -> str:        
        return f"{self.__class__.__name__}()"


class _MatrixElement(OpticalElement):
    """Internal: holds a precomputed matrix (result of composition)."""
    def __init__(self, M): self._M = M
    def matrix(self): return self._M


class FreeSpace(OpticalElement):
    """Free-space propagation over distance d."""

    def __init__(self, d: float) -> None:
        if d < 0:
            raise ValueError(f"Distance must be non-negative, got {d}")
        self.d = d

    def matrix(self) -> np.ndarray:
        return np.array([[1.0, self.d], [0.0, 1.0]])

    def __repr__(self) -> str:
        return f"FreeSpace(d={self.d*1e3:.1f} mm)"


class ThinLens(OpticalElement):
    """Thin lens with focal length f."""

    def __init__(self, f: float) -> None:
        if f == 0:
            raise ValueError("Focal length cannot be zero")
        self.f = f

    def matrix(self) -> np.ndarray:
        return np.array([[1.0, 0.0], [-1.0/self.f, 1.0]])

    def __repr__(self) -> str:
        return f"ThinLens(f={self.f*1e3:.1f} mm)"


class Mirror(OpticalElement):
    """Curved mirror with radius of curvature R (R>0: concave)."""

    def __init__(self, R: float) -> None:
        self.R = R

    def matrix(self) -> np.ndarray:
        return np.array([[1.0, 0.0], [-2.0/self.R, 1.0]])

    def __repr__(self) -> str:
        return f"Mirror(R={self.R*1e3:.1f} mm)"
    
@dataclass
class BeamParameters:
    """
    Spatial parameters of a Gaussian beam at a given plane.

    All lengths in metres.
    """
    wavelength : float           # m
    w0         : float           # beam waist radius (m)
    z          : float = 0.0    # position along optical axis (m)
    M2         : float = 1.0    # beam quality factor

    # Computed fields — not constructor arguments
    def __post_init__(self):
        if self.w0 <= 0:
            raise ValueError(f"w0 must be positive, got {self.w0}")
        if self.M2 < 1:
            raise ValueError(f"M² must be ≥ 1, got {self.M2}")

    @property
    def rayleigh_range(self) -> float:
        """z_R = π w₀² / (M² λ)."""
        return np.pi * self.w0**2 / (self.M2 * self.wavelength)

    @property
    def w_at_z(self) -> float:
        """Beam radius at current z."""
        return self.w0 * np.sqrt(1 + (self.z / self.rayleigh_range)**2)