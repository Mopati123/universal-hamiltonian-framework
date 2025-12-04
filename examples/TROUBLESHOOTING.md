# Troubleshooting Guide
## Common Issues and Solutions

---

## 🔧 Installation Issues

### Problem 1: "python is not recognized"

**Symptoms**:
```
'python' is not recognized as an internal or external command
```

**Solution (Windows)**:
1. Reinstall Python from [python.org](https://python.org)
2. **IMPORTANT**: Check "Add Python to PATH" during install
3. Restart Command Prompt
4. Try `python3` instead of `python`

**Solution (Mac/Linux)**:
```bash
# Use python3 explicitly
python3 --version
python3 script.py
```

---

### Problem 2: "pip not found"

**Symptoms**:
```
'pip' is not recognized
pip: command not found
```

**Solutions**:

**Try pip3**:
```bash
pip3 install -r requirements.txt
```

**Use python -m pip**:
```bash
python -m pip install numpy scipy matplotlib
```

**Reinstall pip** (if all else fails):
```bash
# Windows
python -m ensurepip --upgrade

# Mac/Linux
sudo apt install python3-pip  # Ubuntu/Debian
brew install python3  # Mac
```

---

### Problem 3: Permission denied

**Symptoms**:
```
Permission denied
ERROR: Could not install packages
```

**Solution (Mac/Linux)**:
```bash
sudo pip install -r requirements.txt
```

**Solution (Windows)**:
- Right-click Command Prompt
- Select "Run as Administrator"
- Try install again

**Alternative (user install)**:
```bash
pip install --user -r requirements.txt
```

---

## 🐍 Python Issues

### Problem 4: Wrong Python version

**Symptoms**:
```
SyntaxError: invalid syntax
  File "script.py", line 10
    def function(param: str) -> int:
                      ^
SyntaxError: invalid syntax
```

**Check version**:
```bash
python --version
# Need: Python 3.8+
```

**Solution**:
- Download Python 3.8+ from [python.org](https://python.org)
- Install new version
- Use `python3` command

---

### Problem 5: Module not found errors

**Symptoms**:
```
ModuleNotFoundError: No module named 'numpy'
ModuleNotFoundError: No module named 'scipy'
```

**Solution**:
```bash
# Install all dependencies
pip install -r requirements.txt

# Or individually
pip install numpy
pip install scipy
pip install matplotlib
```

**If still fails**:
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Then try again
pip install numpy scipy matplotlib
```

---

## 📊 Graphics Issues

### Problem 6: No graphs appearing

**Symptoms**:
- Code runs without error
- No matplotlib window appears
- Or: "ImportError: No module named 'tkinter'"

**Solution 1** (Install matplotlib properly):
```bash
pip install matplotlib
```

**Solution 2** (Mac - install backend):
```bash
pip install pyqt5
```

**Solution 3** (Linux - install tkinter):
```bash
sudo apt-get install python3-tk  # Ubuntu/Debian
sudo dnf install python3-tkinter  # Fedora
```

**Workaround**: Graphs save as PNG files anyway!
```python
# Look for these files in your folder:
market_phase_space.png
consciousness_phase_space.png
```

---

### Problem 7: "Backend not available" error

**Symptoms**:
```
UserWarning: Matplotlib is currently using agg, which is a non-GUI backend
```

**Solution**:
```python
# Add these lines at top of script
import matplotlib
matplotlib.use('TkAgg')  # or 'Qt5Agg'
import matplotlib.pyplot as plt
```

**Or**: Just view the saved PNG files!

---

## 💻 Running Examples Issues

### Problem 8: Examples give different numbers than tutorial

**Is this a problem?** **NO!**

**Why it happens**:
- Floating-point precision varies
- Random number generators differ
- Operating system differences

**When to worry**:
- Difference > 10% → Check your Python version
- Error messages → See error-specific solutions
- NaN or Inf → Possible numerical instability

**If difference < 1%**: You're perfect! ✓

---

### Problem 9: "File not found" when running examples

**Symptoms**:
```
FileNotFoundError: [Errno 2] No such file or directory: 'domain_markets.py'
```

**Solution**: Navigate to examples folder!

**Windows**:
```bash
cd Desktop\universal-hamiltonian-framework\examples
python domain_markets.py
```

**Mac/Linux**:
```bash
cd ~/Desktop/universal-hamiltonian-framework/examples
python domain_markets.py
```

**Check you're in right place**:
```bash
# Should see .py files
dir   # Windows
ls    # Mac/Linux
```

---

### Problem 10: Script runs forever / hangs

**Symptoms**:
- Terminal shows nothing
- Waits indefinitely
- No error message

**Likely causes**:
1. Matplotlib waiting for window to close
2. Large computation (patience!)
3. Infinite loop (unlikely in our examples)

**Solutions**:
1. Close any matplotlib windows
2. Wait 30 seconds for consciousness example (longest)
3. Press Ctrl+C to cancel and restart

---

## 🔬 Understanding Issues

### Problem 11: "I don't understand what Hamiltonian means"

**Solution**: You're in the right place!

1. Read [minimal_example_TUTORIAL.md](minimal_example_TUTORIAL.md)
2. **TL;DR**: Hamiltonian = Total energy of the system
3. It's a function H(q, p) that determines how system evolves
4. Think: "Recipe for how things change over time"

**No advanced math required**!

---

### Problem 12: "Phase space" is confusing

**Solution**: Think simple!

**Without phase space**: "Ball is at position x=5"  
**With phase space**: "Ball is at x=5 AND moving at v=2"

**That's it!**

Position alone isn't enough - need velocity too.

Phase space = **(position, velocity)** or **(state, change rate)**

---

## 🌐 Network/Download Issues

### Problem 13: Git clone fails

**Symptoms**:
```
fatal: unable to access 'https://github.com/...'
Connection timeout
```

**Solution 1** (Check internet):
- Ensure you're online
- Try accessing GitHub.com in browser

**Solution 2** (Download ZIP instead):
1. Go to [GitHub page](https://github.com/Mopati123/universal-hamiltonian-framework)
2. Click green "Code" button
3. Select "Download ZIP"
4. Extract to Desktop

**Solution 3** (Proxy issues):
```bash
git config --global http.proxy http://proxy.example.com:8080
git clone ...
```

---

### Problem 14: pip install times out

**Symptoms**:
```
ReadTimeoutError: HTTPSConnectionPool...
```

**Solution**:
```bash
# Increase timeout
pip install --timeout 1000 numpy scipy matplotlib

# Or use different package index
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple numpy scipy matplotlib
```

---

## 🖥️ Platform-Specific Issues

### Windows: PowerShell execution policy

**Symptoms**:
```
cannot be loaded because running scripts is disabled on this system
```

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Mac: SSL certificate error

**Symptoms**:
```
ssl.SSLCertVerificationError
```

**Solution**:
```bash
/Applications/Python\ 3.x/Install\ Certificates.command
```

---

### Linux: Python points to Python 2

**Symptoms**:
```
python --version
Python 2.7.x
```

**Solution**: Always use `python3` and `pip3`
```bash
python3 domain_markets.py
pip3 install -r requirements.txt
```

**Or**: Create alias
```bash
alias python=python3
alias pip=pip3
```

---

## 📝 Still Stuck?

### Step 1: Check Basics

- [ ] Python 3.8+ installed?
- [ ] In correct directory (`examples/`)?
- [ ] Dependencies installed (`pip install -r requirements.txt`)?
- [ ] Tried both `python` and `python3`?

### Step 2: Search Existing Issues

- Check [GitHub Issues](https://github.com/Mopati123/universal-hamiltonian-framework/issues)
- Someone might have solved it!

### Step 3: Ask for Help

Create new issue with:
1. **What you tried**: Exact command
2. **Error message**: Copy-paste full error
3. **System**: Windows/Mac/Linux, Python version
4. **What you expected**: What should happen

We'll help! 🎯

---

## 🎓 Educational "Problems"

### "Problem" 15: I want to understand more deeply

**Not a problem - that's great!**

**Next steps**:
1. Read [Chapter 0](../docs/book-of-mopati-chapter0.md) - Mathematical foundations
2. Explore [Full Documentation](../docs/book-of-mopati.md)
3. Check tutorial "Additional Resources" sections
4. Try modifying example parameters!

### "Problem" 16: Examples are too easy, I want challenges

**Excellent!**

**Challenges**:
1. Modify parameters in examples
2. Combine multiple examples (coupled systems!)
3. Apply to your own domain
4. Read research papers referenced in tutorials
5. Contribute new examples to framework!

See [CONTRIBUTING.md](../CONTRIBUTING.md)

---

_Troubleshooting guide updated: December 2025_  
_Can't find your issue? Ask in [Discussions](https://github.com/Mopati123/universal-hamiltonian-framework/discussions)!_
