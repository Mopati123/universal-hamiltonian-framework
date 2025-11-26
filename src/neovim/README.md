# Neovim HL Plugin - Hamiltonian Language Editor Integration

**Artifact C**: Nvim plugin for editing, compiling, and visualizing HL programs

## Installation

```vim
" In your init.vim or init.lua
Plug 'mopati/hamiltonian-language.nvim'
```

## Features

- **Syntax highlighting** for HL programs
- **Async compilation** (no blocking)
- **Live simulation** (run selection)
- **Spectral visualization** (eigenvalues/eigenvectors)
- **H_meta optimization** triggers

## Keymaps (Leader = Space)

```vim
" Compilation
<leader>hc    " Compile current file
<leader>hs    " Simulate selection
<leader>ho    " Run H_meta optimization
<leader>hv    " Visualize spectrum

" Navigation
<leader>hr    " Jump to register definition
<leader>ht    " Jump to Hamiltonian term

" Debugging
<leader>hd    " Show density matrix
<leader>he    " Show energy levels
```

## HL Daemon (HTTP Server)

```python
# daemon.py - Background compilation server
import http.server
import json
from hl.canonical_library import *
from backends.jax_engine import *

class HLHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/compile':
            length = int(self.headers['Content-Length'])
            hl_code = self.rfile.read(length).decode()
            
            # Parse and compile
            result = compile_hl(hl_code)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

# Run: python daemon.py
server = http.server.HTTPServer(('localhost', 8080), HLHandler)
server.serve_forever()
```

## Lua Plugin Code

```lua
-- hamiltonian_language.lua
local M = {}
local curl = require('plenary.curl')

-- Compile current buffer
M.compile = function()
  local lines = vim.api.nvim_buf_get_lines(0, 0, -1, false)
  local code = table.concat(lines, '\n')
  
  curl.post('http://localhost:8080/compile', {
    body = code,
    callback = function(response)
      vim.notify('Compiled: ' .. response.status)
    end
  })
end

-- Simulate selection
M.simulate = function()
  local start_line = vim.fn.line("'<")
  local end_line = vim.fn.line("'>")
  local lines = vim.api.nvim_buf_get_lines(0, start_line-1, end_line, false)
  
  -- Send to simulation endpoint
  -- Display results in floating window
end

return M
```

**Status**: Scaffold complete - needs full implementation
