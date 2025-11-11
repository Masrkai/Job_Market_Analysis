{ pkgs ? import <nixpkgs> {} }:

(pkgs.buildFHSEnv {
  name = "python-env";
  targetPkgs = pkgs: (with pkgs; [
    python312
    pythonManylinuxPackages.manylinux2014Package

    gcc

    brave
  ]);
  runScript = pkgs.writeScript "init-venv" ''
    #!/bin/bash
    set -e
    echo "Setting up Python virtual environment..."
    test -d .venv || python3 -m venv .venv
    source .venv/bin/activate
    
    echo "Virtual environment activated at: $VIRTUAL_ENV"
    echo "Python path: $(which python)"
    echo "Pip path: $(which pip)"
    echo "UV will automatically detect the .venv directory"
    exec bash --rcfile <(echo "source .venv/bin/activate")
  '';
}).env