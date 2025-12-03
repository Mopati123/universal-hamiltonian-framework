# Complete Beginner's Guide to Running Examples
## Never Coded Before? Start Here! 👋

**Welcome!** This guide assumes you've **never written code** or used a terminal before.

By the end (15 minutes), you'll have **real physics simulations running on your computer**!

---

## 🎯 What We're Going to Do

**Think of it like cooking**:
1. **Get a kitchen** = Install Python
2. **Get ingredients** = Download code
3. **Follow recipe** = Run example
4. **Enjoy meal** = See results!

**You literally can't mess this up** - just follow step-by-step.

---

## Step 1: Install Python (Your "Kitchen")

### What is Python?

A **programming language** - a way to give instructions to your computer.

Think: **English for humans, Python for computers**.

### 🪟 Windows Users

1. **Visit**: [python.org/downloads](https://python.org/downloads)
2. **Click**: Big yellow button "Download Python 3.x"
3. **Run** the installer file (in your Downloads folder)
4. **⚠️ IMPORTANT**: Check the box "Add Python to PATH"
   - This is at the BOTTOM of installer
   - Makes Python work from anywhere
5. Click "Install Now"
6. Wait 2 minutes
7. Click "Close"

**Done!** Python is installed ✓

### 🍎 Mac Users

**Option A**: Use Terminal (5 minutes)

1. **Open Terminal**:
   - Press `Cmd + Space`
   - Type "Terminal"
   - Press Enter
   
2. **Copy and paste this**:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
   
3. **Press Enter**, wait 5 minutes

4. **Then paste this**:
   ```bash
   brew install python3
   ```

**Option B**: Download installer (easier!)

1. Visit [python.org/downloads](https://python.org/downloads)
2. Download Mac installer
3. Run it
4. Follow prompts

### 🐧 Linux Users

You probably already have Python! Open terminal and type:
```bash
python3 --version
```

If not installed:
```bash
sudo apt install python3 python3-pip  # Ubuntu/Debian
sudo dnf install python3 python3-pip  # Fedora
```

---

### ✅ Verify Python Works

**All platforms**:

1. **Open** command prompt (Windows) or Terminal (Mac/Linux)
   - Windows: Press `Win + R`, type `cmd`, press Enter
   - Mac: `Cmd + Space`, type "Terminal"
   - Linux: `Ctrl + Alt + T`

2. **Type**:
   ```bash
   python --version
   ```
   
3. **Should see**: `Python 3.10.x` (or similar)

**If you see numbers, SUCCESS!** ✓

**If error "python not found"**:
- Windows: Try `python3 --version` or reinstall (check PATH box!)
- Mac/Linux: Use `python3` instead of `python`

---

## Step 2: Get the Code (Download the "Recipe Book")

### Method A: Download ZIP (Easiest!)

1. **Visit**: [github.com/Mopati123/universal-hamiltonian-framework](https://github.com/Mopati123/universal-hamiltonian-framework)

2. **Click**: Green button that says "Code"

3. **Select**: "Download ZIP"

4. **Save to Desktop**

5. **Extract**:
   - Windows: Right-click ZIP → "Extract All" → Choose Desktop
   - Mac: Double-click ZIP (auto-extracts)
   - Linux: Right-click → "Extract Here"

6. **You now have** a folder on your Desktop called `universal-hamiltonian-framework`!

### Method B: Git Clone (If You Know Git)

```bash
cd Desktop
git clone https://github.com/Mopati123/universal-hamiltonian-framework
```

---

## Step 3: Navigate to Examples Folder

### 🪟 Windows

1. **Open Command Prompt**:
   - Press `Win + R`
   - Type `cmd`
   - Press Enter

2. **Navigate to folder**:
   ```bash
   cd Desktop\universal-hamiltonian-framework\examples
   ```
   
3. **Press Enter**

**You're now "inside" the examples folder!**

### 🍎 Mac / 🐧 Linux

1. **Open Terminal**

2. **Navigate**:
   ```bash
   cd ~/Desktop/universal-hamiltonian-framework/examples
   ```

3. **Press Enter**

---

## Step 4: Install "Ingredients" (Python Packages)

**What are packages?**  
Pre-written code that does math for us. Like buying pre-made sauce instead of making from scratch!

**Type this**:
```bash
pip install -r requirements.txt
```

**Press Enter**

**What you'll see**:
```
Collecting numpy...
Downloading numpy-1.24.0...
Installing...
Successfully installed numpy scipy matplotlib
```

**This takes 30-60 seconds**. Be patient!

**If error "pip not found"**:
- Try: `pip3 install -r requirements.txt`
- Or: `python -m pip install -r requirements.txt`

---

## Step 5: Run Your First Example! 🎉

**Type**:
```bash
python minimal_example.py
```

**Press Enter**

**You should see**:
```
=====================================================
HAMILTONIAN LANGUAGE (HL) - Minimal Demo
=====================================================

Creating a qubit register...
Created: q with dimension 2

Creating H_state (energy levels [0, 1])...
H_state matrix:
[[0. 0.]
 [0. 1.]]

Verifying Hermiticity (H = H†)...
Hermitian: True

✓ Hamiltonian created successfully!
```

### 🎉 **CONGRATULATIONS!**

**You just ran a quantum mechanics simulation!**

You created a **qubit** (quantum bit) and calculated its **Hamiltonian** (energy operator).

This is the **same math** that:
- Powers quantum computers
- Describes atoms
- Explains chemistry
- Models consciousness

**And you did it!** ✓

---

## Step 6: What Next?

### Try Another Example

**Markets** (shows stock prices follow physics):
```bash
python domain_markets.py
```

**Consciousness** (shows attention is like momentum):
```bash
python domain_consciousness.py
```

**Blockchain** (shows consensus minimizes energy):
```bash
python domain_blockchain.py
```

### Understand Deeper

For each example, read the tutorial:
- `minimal_example_TUTORIAL.md`
- `domain_markets_TUTORIAL.md`
- `domain_consciousness_TUTORIAL.md`
- `domain_blockchain_TUTORIAL.md`

These explain **what's happening** and **why it matters**.

---

## 🔍 Understanding What You Just Did

### The Code You Ran

```python
from hl import Register, RegisterType

# Create a 2-level quantum system
q = Register("qubit", RegisterType.QUBIT, 2)

# Define its energy levels
H = np.array([[0, 0],
              [0, 1]])
```

**In plain English**:
1. Created a "quantum bit" (can be 0 or 1, or both!)
2. Gave it energy levels: state |0⟩ has energy 0, state |1⟩ has energy 1
3. This is the **Hamiltonian** - the "DNA" of the quantum system

### Why This Matters

**This same structure describes**:
- Electrons in atoms
- Stock prices changing
- Your attention shifting
- Bitcoin mining
- Everything!

---

## ❓ Common Questions

### "What's a terminal/command prompt?"

The **pure text interface** to your computer.  
Before graphical interfaces (windows, icons), this was the ONLY way to use computers!  
Still the best way to run code.

### "What does 'cd' mean?"

**"Change Directory"** = Move to different folder.

Think: Walking into a different room in your house.

### "Why do I need to install packages?"

Code reuse! **numpy** does math, **scipy** solves equations, **matplotlib** makes graphs.

We don't rewrite these - we use them!

### "Is this safe?"

**Yes!** 
- Python is trusted by millions
- Our code is open-source (you can read it!)
- Packages are from official Python repository
- No viruses, no tricks

### "I got an error!"

**No worries!** Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

Common errors:
- `'python' is not recognized` → Use `python3` instead
- `pip not found` → Use `pip3` or `python -m pip`
- `Permission denied` → Add `sudo` on Mac/Linux, run as Admin on Windows

---

## 🎓 You've Learned

✅ How to open terminal/command prompt  
✅ How to navigate folders (`cd`)  
✅ How to run Python code  
✅ How to install packages (`pip`)  
✅ What a Hamiltonian is (energy operator!)  
✅ That quantum mechanics runs on your computer

**From knowing NOTHING to running physics simulations in 15 minutes!**

That's incredible! 🎉

---

## 🚀 Next Steps

### Learn More

1. **Read tutorials** for each example (deep explanations)
2. **Modify code** (change numbers, see what happens!)
3. **Read Chapter 0** ([here](../docs/book-of-mopati-chapter0.md)) for theory
4. **Ask questions** in [Discussions](https://github.com/Mopati123/universal-hamiltonian-framework/discussions)

### Challenge Yourself

Can you:
- Change the energy levels in `minimal_example.py`?
- Run all three domain examples?
- Understand one line of code?

**Every programmer started exactly where you are!**

---

## 💬 Get Help

**Stuck?**
- [Troubleshooting Guide](TROUBLESHOOTING.md)
- [FAQ](FAQ.md)
- [GitHub Discussions](https://github.com/Mopati123/universal-hamiltonian-framework/discussions)

**Want to learn Python?**
- [python.org/tutorial](https://docs.python.org/3/tutorial/)
- [codecademy.com/learn/learn-python-3](https://www.codecademy.com/learn/learn-python-3)

---

## 🎉 You Did It!

**You're now a** (beginning) **computational physicist!**

Welcome to the world where mathematics describes reality. 🌌✨

---

_Remember: Every expert was once a beginner who didn't give up._  
_You've got this!_ 💪
