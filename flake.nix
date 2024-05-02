{
  description = "Dev shell";

  inputs =
    {
      nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    };

  outputs = { self, nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShells.x86_64-linux.default =
        pkgs.mkShell
          {
            LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";
            shellHook = ''
              source .venv/bin/activate
            '';
          };
    };
}