import sys
import numpy as np
import matplotlib.pyplot as plt

print(f"Python {sys.version}")
print(f"NumPy  {np.__version__}")

x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x))
plt.title("If you see this plot, you're ready!")
plt.savefig("test_plot.png", dpi=100)
plt.show()
print("Setup complete ✓")