"""
Interactive Phase-Space Visualizer - Browser-based version

Opens in your web browser for easy interaction.
"""

import numpy as np
import webbrowser
import http.server
import socketserver
import threading
import json
from urllib.parse import parse_qs

# Generate HTML with embedded visualization
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Universal Hamiltonian Framework - Interactive Demo</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            background: #0a0a0a;
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        h1 {
            text-align: center;
            color: #00d4ff;
            text-shadow: 0 0 10px #00d4ff;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .controls {
            background: #1e1e1e;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
        }
        
        .slider-group {
            margin: 15px 0;
        }
        
        label {
            display: inline-block;
            width: 200px;
            color: #00d4ff;
            font-weight: bold;
        }
        
        input[type="range"] {
            width: 300px;
            margin: 0 10px;
        }
        
        .value-display {
            display: inline-block;
            width: 80px;
            text-align: right;
            color: #ffd93d;
            font-family: monospace;
        }
        
        button {
            background: #00d4ff;
            color: #000;
            border: none;
            padding: 10px 30px;
            margin: 5px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        button:hover {
            background: #00ffff;
            box-shadow: 0 0 15px #00d4ff;
        }
        
        #canvas-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-gap: 20px;
            margin-top: 20px;
        }
        
        canvas {
            background: #1e1e1e;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
        }
        
        .info {
            text-align: center;
            color: #888;
            margin-top: 20px;
            font-size: 14px;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-top: 20px;
        }
        
        .stat-box {
            background: #1e1e1e;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 24px;
            color: #00d4ff;
            font-weight: bold;
        }
        
        .stat-label {
            font-size: 12px;
            color: #888;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌌 Universal Hamiltonian Framework</h1>
        <h2 style="text-align: center; color: #888;">Interactive Phase-Space Explorer</h2>
        
        <div class="controls">
            <h3>System Parameters</h3>
            
            <div class="slider-group">
                <label>Mass (m):</label>
                <input type="range" id="mass" min="0.1" max="5" step="0.1" value="1.0">
                <span class="value-display" id="mass-val">1.00</span>
            </div>
            
            <div class="slider-group">
                <label>Spring Constant (k):</label>
                <input type="range" id="spring" min="0.1" max="5" step="0.1" value="1.0">
                <span class="value-display" id="spring-val">1.00</span>
            </div>
            
            <div class="slider-group">
                <label>Initial Position (q0):</label>
                <input type="range" id="q0" min="-5" max="5" step="0.1" value="1.0">
                <span class="value-display" id="q0-val">1.00</span>
            </div>
            
            <div class="slider-group">
                <label>Initial Momentum (p0):</label>
                <input type="range" id="p0" min="-5" max="5" step="0.1" value="0.0">
                <span class="value-display" id="p0-val">0.00</span>
            </div>
            
            <div style="margin-top: 20px; text-align: center;">
                <button onclick="resetSimulation()">Reset</button>
                <button onclick="togglePause()" id="pauseBtn">Pause</button>
            </div>
        </div>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-value" id="stat-time">0.00</div>
                <div class="stat-label">Time (t)</div>
            </div>
            <div class="stat-box">
                <div class="stat-value" id="stat-energy">0.50</div>
                <div class="stat-label">Energy (H)</div>
            </div>
            <div class="stat-box">
                <div class="stat-value" id="stat-steps">0</div>
                <div class="stat-label">Steps</div>
            </div>
            <div class="stat-box">
                <div class="stat-value" id="stat-drift">0.00%</div>
                <div class="stat-label">Energy Drift</div>
            </div>
        </div>
        
        <div id="canvas-container">
            <canvas id="phase-canvas" width="600" height="600"></canvas>
            <canvas id="time-canvas" width="600" height="600"></canvas>
        </div>
        
        <div class="info">
            <p>Adjust sliders to change parameters in real-time - Phase portrait shows (q,p) trajectory - Time plot shows evolution</p>
            <p style="color: #00d4ff;">Powered by Hamiltonian Mechanics - Energy preserved by symplectic integration</p>
        </div>
    </div>
    
    <script>
        // System state
        let system = {
            mass: 1.0,
            k: 1.0,
            q0: 1.0,
            p0: 0.0,
            q: 1.0,
            p: 0.0,
            t: 0.0,
            dt: 0.01,
            trajectory: [],
            maxPoints: 500,
            isPaused: false,
            steps: 0,
            E0: 0.5
        };
        
        // Canvases
        const phaseCanvas = document.getElementById('phase-canvas');
        const timeCanvas = document.getElementById('time-canvas');
        const phaseCtx = phaseCanvas.getContext('2d');
        const timeCtx = timeCanvas.getContext('2d');
        
        // Hamiltonian physics
        function hamiltonian(q, p) {
            return p*p / (2*system.mass) + 0.5*system.k*q*q;
        }
        
        function force(q) {
            return -system.k * q;
        }
        
        function verletStep() {
            const pHalf = system.p + 0.5 * system.dt * force(system.q);
            system.q = system.q + system.dt * pHalf / system.mass;
            system.p = pHalf + 0.5 * system.dt * force(system.q);
            system.t += system.dt;
            system.steps++;
            
            const E = hamiltonian(system.q, system.p);
            system.trajectory.push({q: system.q, p: system.p, t: system.t, E: E});
            
            if (system.trajectory.length > system.maxPoints) {
                system.trajectory.shift();
            }
        }
        
        function drawPhasePortrait() {
            phaseCtx.fillStyle = '#1e1e1e';
            phaseCtx.fillRect(0, 0, 600, 600);
            
            // Grid
            phaseCtx.strokeStyle = '#333';
            phaseCtx.lineWidth = 1;
            for (let i = -5; i <= 5; i++) {
                const x = 300 + i * 50;
                phaseCtx.beginPath();
                phaseCtx.moveTo(x, 0);
                phaseCtx.lineTo(x, 600);
                phaseCtx.stroke();
                
                const y = 300 - i * 50;
                phaseCtx.beginPath();
                phaseCtx.moveTo(0, y);
                phaseCtx.lineTo(600, y);
                phaseCtx.stroke();
            }
            
            // Axes
            phaseCtx.strokeStyle = '#666';
            phaseCtx.lineWidth = 2;
            phaseCtx.beginPath();
            phaseCtx.moveTo(300, 0);
            phaseCtx.lineTo(300, 600);
            phaseCtx.moveTo(0, 300);
            phaseCtx.lineTo(600, 300);
            phaseCtx.stroke();
            
            // Labels
            phaseCtx.fillStyle = '#888';
            phaseCtx.font = '14px monospace';
            phaseCtx.fillText('q', 580, 320);
            phaseCtx.fillText('p', 310, 20);
            
            // Trajectory
            if (system.trajectory.length > 1) {
                phaseCtx.strokeStyle = '#00d4ff';
                phaseCtx.lineWidth = 2;
                phaseCtx.beginPath();
                
                const first = system.trajectory[0];
                phaseCtx.moveTo(300 + first.q * 50, 300 - first.p * 50);
                
                for (let i = 1; i < system.trajectory.length; i++) {
                    const point = system.trajectory[i];
                    phaseCtx.lineTo(300 + point.q * 50, 300 - point.p * 50);
                }
                phaseCtx.stroke();
                
                // Current point
                phaseCtx.fillStyle = '#ff0000';
                phaseCtx.beginPath();
                phaseCtx.arc(300 + system.q * 50, 300 - system.p * 50, 8, 0, 2*Math.PI);
                phaseCtx.fill();
            }
            
            // Title
            phaseCtx.fillStyle = '#00d4ff';
            phaseCtx.font = 'bold 16px sans-serif';
            phaseCtx.fillText('Phase Portrait (q, p)', 10, 25);
        }
        
        function drawTimeEvolution() {
            timeCtx.fillStyle = '#1e1e1e';
            timeCtx.fillRect(0, 0, 600, 600);
            
            if (system.trajectory.length < 2) return;
            
            const tMin = system.trajectory[0].t;
            const tMax = system.trajectory[system.trajectory.length - 1].t;
            const tRange = Math.max(0.1, tMax - tMin);
            
            // Grid
            timeCtx.strokeStyle = '#333';
            timeCtx.lineWidth = 1;
            for (let i = 0; i <= 10; i++) {
                const x = i * 60;
                timeCtx.beginPath();
                timeCtx.moveTo(x, 0);
                timeCtx.lineTo(x, 600);
                timeCtx.stroke();
            }
            
            // Plot q(t)
            timeCtx.strokeStyle = '#ff6b6b';
            timeCtx.lineWidth = 2;
            timeCtx.beginPath();
            
            for (let i = 0; i < system.trajectory.length; i++) {
                const point = system.trajectory[i];
                const x = ((point.t - tMin) / tRange) * 550 + 25;
                const y = 200 - point.q * 30;
                
                if (i === 0) timeCtx.moveTo(x, y);
                else timeCtx.lineTo(x, y);
            }
            timeCtx.stroke();
            
            // Plot p(t)
            timeCtx.strokeStyle = '#4ecdc4';
            timeCtx.lineWidth = 2;
            timeCtx.beginPath();
            
            for (let i = 0; i < system.trajectory.length; i++) {
                const point = system.trajectory[i];
                const x = ((point.t - tMin) / tRange) * 550 + 25;
                const y = 450 - point.p * 30;
                
                if (i === 0) timeCtx.moveTo(x, y);
                else timeCtx.lineTo(x, y);
            }
            timeCtx.stroke();
            
            // Labels
            timeCtx.fillStyle = '#ff6b6b';
            timeCtx.font = 'bold 14px sans-serif';
            timeCtx.fillText('q(t)', 10, 50);
            
            timeCtx.fillStyle = '#4ecdc4';
            timeCtx.fillText('p(t)', 10, 300);
            
            timeCtx.fillStyle = '#888';
            timeCtx.font = '12px monospace';
            timeCtx.fillText('time →', 530, 590);
            
            // Title
            timeCtx.fillStyle = '#00d4ff';
            timeCtx.font = 'bold 16px sans-serif';
            timeCtx.fillText('Time Evolution', 10, 25);
        }
        
        function updateStats() {
            document.getElementById('stat-time').textContent = system.t.toFixed(2);
            
            const E = hamiltonian(system.q, system.p);
            document.getElementById('stat-energy').textContent = E.toFixed(4);
            document.getElementById('stat-steps').textContent = system.steps;
            
            const drift = Math.abs((E - system.E0) / system.E0) * 100;
            document.getElementById('stat-drift').textContent = drift.toFixed(4) + '%';
        }
        
        function resetSimulation() {
            system.q = system.q0;
            system.p = system.p0;
            system.t = 0;
            system.steps = 0;
            system.trajectory = [];
            system.E0 = hamiltonian(system.q, system.p);
        }
        
        function togglePause() {
            system.isPaused = !system.isPaused;
            document.getElementById('pauseBtn').textContent = system.isPaused ? 'Play' : 'Pause';
        }
        
        // Update slider values
        function updateSliders() {
            system.mass = parseFloat(document.getElementById('mass').value);
            system.k = parseFloat(document.getElementById('spring').value);
            system.q0 = parseFloat(document.getElementById('q0').value);
            system.p0 = parseFloat(document.getElementById('p0').value);
            
            document.getElementById('mass-val').textContent = system.mass.toFixed(2);
            document.getElementById('spring-val').textContent = system.k.toFixed(2);
            document.getElementById('q0-val').textContent = system.q0.toFixed(2);
            document.getElementById('p0-val').textContent = system.p0.toFixed(2);
        }
        
        document.getElementById('mass').oninput = updateSliders;
        document.getElementById('spring').oninput = updateSliders;
        document.getElementById('q0').oninput = updateSliders;
        document.getElementById('p0').oninput = updateSliders;
        
        // Animation loop
        function animate() {
            if (!system.isPaused) {
                for (let i = 0; i < 3; i++) {
                    verletStep();
                }
            }
            
            drawPhasePortrait();
            drawTimeEvolution();
            updateStats();
            
            requestAnimationFrame(animate);
        }
        
        // Start
        resetSimulation();
        animate();
    </script>
</body>
</html>
"""

# Save HTML file
with open('interactive_visualization.html', 'w') as f:
    f.write(html_content)

print("\n" + "="*70)
print("UNIVERSAL HAMILTONIAN FRAMEWORK - BROWSER VISUALIZATION")
print("="*70)
print("\nOpening interactive visualization in your browser...")
print("\nControls:")
print("  • Use sliders to adjust mass, spring constant, and initial conditions")
print("  • Click 'Reset' to restart with new parameters")
print("  • Click 'Pause/Play' to control evolution")
print("\nThe visualization shows:")
print("  • Phase Portrait: Real-time (q,p) trajectory")
print("  • Time Evolution: q(t) and p(t) plots")
print("  • Live statistics: Time, Energy, Steps, Energy Drift")
print("="*70)
print()

# Open in browser
import os
file_path = os.path.abspath('interactive_visualization.html')
webbrowser.open('file://' + file_path)

print(f"✓ Saved to: {file_path}")
print("✓ Opening in your default web browser...")
print("\nThe browser window should open automatically.")
print("If it doesn't, manually open: interactive_visualization.html")
print()
