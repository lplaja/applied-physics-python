# Pre-Session Setup Guide — Python for Applied Physics

**Complete these steps BEFORE Session 1.** Budget 20–30 minutes. If anything fails, bring your laptop to class and we'll troubleshoot together.

---

## Step 1: Install Python (via Miniforge)

We recommend **Miniforge** — a lightweight conda distribution that gives you both `conda` (environment manager) and `pip` (package installer).

### Windows

1. Download Miniforge3 from: https://github.com/conda-forge/miniforge/releases/latest
   - Choose: `Miniforge3-Windows-x86_64.exe`
2. Run the installer. Accept defaults, **but check "Add to PATH"** if offered.
3. Open a new terminal (PowerShell or Command Prompt) and verify:
   ```
   conda --version
   python --version
   ```

### macOS

```bash
# Option A: Homebrew (if you have it)
brew install miniforge

# Option B: Direct download
curl -L -O https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-$(uname -m).sh
bash Miniforge3-MacOSX-$(uname -m).sh
```

Restart your terminal, then verify: `conda --version`

### Linux

```bash
curl -L -O https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh
```

Restart your terminal, then verify: `conda --version`

---

## Step 2: Create the Course Environment

Open a terminal and run:

```bash
conda create -n physics-python python=3.11 numpy scipy matplotlib pandas jupyter h5py -y
```

Activate it:

```bash
conda activate physics-python
```

Verify the scientific stack:

```bash
python -c "import numpy; import scipy; import matplotlib; print('All good!')"
```

You should see `All good!` with no errors.

> **Tip:** Every time you open a new terminal to work on this course, remember to activate the environment: `conda activate physics-python`

---

## Step 3: Install VS Code

1. Download from: https://code.visualstudio.com/
2. Install with default settings.
3. Launch VS Code.

---

## Step 4: Install VS Code Extensions

Open VS Code, then press `Ctrl+Shift+X` (Windows/Linux) or `⌘+Shift+X` (macOS) to open the Extensions sidebar. Search for and install:

| Extension | Publisher | Search for |
|-----------|-----------|------------|
| **Python** | Microsoft | `ms-python.python` |
| **Pylance** | Microsoft | `ms-python.vscode-pylance` |
| **Jupyter** | Microsoft | `ms-toolsai.jupyter` |

> These three are sufficient for Session 1. We'll add more extensions in later sessions.

---

## Step 5: Connect VS Code to Your Environment

1. Open VS Code.
2. Press `Shift+⌘+P` → type `Python: Select Interpreter`.
3. Choose the one that says `physics-python` (or the path containing `physics-python`).
4. Open a terminal in VS Code (`` Ctrl+` ``) and confirm:
   ```
   python --version
   ```
   It should show Python 3.11.x and the prompt should show `(physics-python)`.

---

## Step 6: Test Everything

1. In VS Code, create a new file: `File → New File`, save as `test_setup.py`.
2. Paste this code:

```python
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
```

3. Run it: right-click in the editor → `Run Python File in Terminal`, or press the ▶ button.
4. If a sine wave plot appears and you see `Setup complete ✓`, you're good to go.

---

## Step 7: Test Jupyter in VS Code

1. Press `Ctrl+Shift+P` → type `Jupyter: Create New Notebook`.
2. In the first cell, type:

```python
import numpy as np
print(f"NumPy version: {np.__version__}")
2 + 2
```

3. Press `Shift+Enter` to run the cell.
4. If you see output including `4`, Jupyter is working.

> Make sure the kernel (shown top-right) says `physics-python`.

---

## Troubleshooting

| Problem | Solution |
|---------|---------|
| `conda: command not found` | Restart your terminal. If still failing, the PATH wasn't set — reinstall Miniforge and check "Add to PATH". |
| VS Code doesn't find `physics-python` | Open a terminal in VS Code, run `conda activate physics-python`, then try `Python: Select Interpreter` again. |
| `ModuleNotFoundError: No module named 'numpy'` | Wrong environment. Check your kernel/interpreter — it should point to `physics-python`. |
| Jupyter cells don't run | Make sure the Jupyter extension is installed. Restart VS Code. |
| Plot doesn't show | Some systems need `%matplotlib inline` at the top of the notebook. Try it. |

---

**That's it!** Bring your laptop to Session 1 with everything working. See you there.
