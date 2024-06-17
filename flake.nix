{
  description = "Development shell for webserver";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-24.05";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };
  outputs = { self, nixpkgs, poetry2nix, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system}; 
      inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication;
      wwwrequef = mkPoetryApplication { 
        projectDir = ./.;
        python = pkgs.python311;
        pyproject = ./pyproject.toml;
        poetryLock = ./poetry.lock; 
        # TODO: Plugin installation doesn't work for now.
        plugins = [ pkgs.poetryPlugins.poetry-plugin-export ];
      };
    in {
      devShells.${system}.default = pkgs.mkShell {
        LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";
        buildInputs = with pkgs; [
          wwwrequef
        ];    
      };
  };
}
