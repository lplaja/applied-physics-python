"""shared/optics.py

Reusable optics functions for the Applied Physics Python course.
Grow this module as the course progresses.
"""

import math


def rayleigh_range(w0, wavelength):
    """
    Rayleigh range of a Gaussian beam.

    Parameters
    ----------
    w0 : float
        Beam waist radius [m].
    wavelength : float
        Laser wavelength [m].

    Returns
    -------
    float
        Rayleigh range z_R [m].
    """
    return math.pi * w0**2 / wavelength


def gaussian_beam_waist(z, w0, wavelength):
    """
    Beam radius of a Gaussian beam at propagation distance z.

    Parameters
    ----------
    z : float
        Propagation distance from the waist [m].
    w0 : float
        Beam waist radius [m].
    wavelength : float
        Laser wavelength [m].

    Returns
    -------
    float
        Beam radius w(z) [m].
    """
    z_R = rayleigh_range(w0, wavelength)
    return w0 * math.sqrt(1 + (z / z_R)**2)


def fresnel_reflectance(n1, n2, theta_i_deg):
    """
    Fresnel reflectance for s- and p-polarizations.

    Parameters
    ----------
    n1, n2 : float
        Refractive indices of incident and transmitted media.
    theta_i_deg : float
        Angle of incidence [degrees].

    Returns
    -------
    R_s, R_p : float
        Reflectance for s- and p-polarizations (0–1).
    """
    theta_i = math.radians(theta_i_deg)
    sin_t = n1 * math.sin(theta_i) / n2
    if abs(sin_t) > 1.0:
        return 1.0, 1.0
    theta_t = math.asin(sin_t)
    cos_i = math.cos(theta_i)
    cos_t = math.cos(theta_t)
    r_s = (n1 * cos_i - n2 * cos_t) / (n1 * cos_i + n2 * cos_t)
    r_p = (n2 * cos_i - n1 * cos_t) / (n2 * cos_i + n1 * cos_t)
    return r_s**2, r_p**2

def peak_irradiance(E_J, tau_s, w0_m):
    """
    Peak irradiance at the beam waist of a Gaussian pulse.

    I_peak = 2 * E / (pi * w0^2 * tau)

    Parameters
    ----------
    E_J   : float  Pulse energy [J]
    tau_s : float  Pulse duration FWHM [s]
    w0_m  : float  Beam waist radius [m]

    Returns
    -------
    float
        Peak irradiance [W/m²]
    """
    import math
    I_peak = 2 * E_J / (math.pi * w0_m**2 * tau_s)
    return I_peak