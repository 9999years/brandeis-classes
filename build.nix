{ lib, python38, ctags, pipenv, doCheck ? true, init_coc_python ? null }:
let
  inherit (lib) inNixShell optionalString;
  pypkgs = python38.pkgs;

in pypkgs.buildPythonApplication {
  pname = "brandeis-classes";
  version = "1.0.0";
  srcs = if inNixShell then
    [ ]
  else [
    ./brandeis_classes
    ./pyproject.toml
    ./README.md
    ./LICENSE.txt
  ];
  unpackCmd = ''
    cp --recursive "$curSrc" "$(stripHash "$curSrc")"
  '';
  sourceRoot = ".";

  format = "flit";

  checkInputs = [ ctags pipenv ] ++ (with pypkgs; [
    black
    autopep8
    yapf
    jedi
    flake8
    bandit
    mypy
    pep8
    pydocstyle
    pylama
    pylint
    isort
    python-ctags3
    pytest
    hypothesis
    rope
    ptpython
    poetry
    conda
  ]);

  inherit doCheck;

  propagatedBuildInputs = with pypkgs; [ termcolor beautifulsoup4 requests ];

  shellHook = optionalString (init_coc_python != null)
    "${init_coc_python}/bin/init_coc_python.py";
}
