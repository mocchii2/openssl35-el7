# Building

Use a disposable EL7 x86_64 build VM, not a production server. Do not build as
root. Provision GCC from Software Collections `devtoolset-12`, including
`devtoolset-12-gcc`, binutils, `rpm-build`, `rpm-sign` (only for signing),
`rpmdevtools`, `yum-utils`, `perl-core`, `make`, `zlib-devel`, `gnupg2`.
Archived OS/SCL repositories may be required: verify their vendor keys and
availability rather than disabling signature checks.

1. Download the matching source archive from this repository's GitHub release.
2. Verify its signed checksum manifest as described in INSTALL.md.
3. Extract the source archive. It contains the original complete `.src.rpm`.
4. Set up the conventional RPM tree as an unprivileged user:

   ```sh
   rpmdev-setuptree
   rpm -ivh SRPMS/openssl35-muhoho-3.5.9-3.el7.src.rpm
   source /opt/rh/devtoolset-12/enable
   rpmbuild -ba "$HOME/rpmbuild/SPECS/openssl35-muhoho.spec"
   ```

The compiler is sourced explicitly by the SPEC. `devtoolset-12-gcc` is a
required build-environment prerequisite even though the original OpenSSL
SPEC does not list it in BuildRequires. Do not use `--nodeps` or `--nocheck`.
Tests run with `HARNESS_JOBS=6`; the optional Perl tsget client is omitted to
avoid an unavailable EL7 Perl dependency.

Rebuilt RPMs are not automatically signed. Never reuse the maintainer's
release identity; use your own protected signing key. Matching source inputs
do not imply bit-for-bit reproducible binaries.
