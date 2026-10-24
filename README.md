# OpenSSL 3.5.9 RPMs for EL7 (x86_64)

Unofficial community packaging for legacy CentOS/RHEL/Oracle Linux 7 systems.
EL7 is end-of-life: these packages do **not** make the operating system supported
or resolve vulnerabilities in unrelated software. Migrate to a supported OS.

## What this provides

- OpenSSL **3.5.9**, RPM release `3.el7`.
- Runtime and development packages installed under `/opt/openssl35`.
- No replacement or `Provides: openssl` for the OS OpenSSL.
- Existing nginx, SSH, yum and OS consumers are not upgraded by installation.
- Private library RUNPATH; full upstream test suite enabled in the SPEC.

The matching [PHP 8.4 stack](https://github.com/mocchii2/php84-el7) uses these
libraries. OpenSSL is deliberately distributed in this separate repository.
Package names retain the `muhoho` suffix to match the tested build/ABI.

## Downloads and trust

See [Releases](https://github.com/mocchii2/openssl35-el7/releases).
Each release includes separate binary RPM and complete corresponding SRPM
archives, checksums and detached signatures. See [INSTALL.md](INSTALL.md)
before installing. No automated production migration script is provided.

Release-key fingerprint:

```text
F31E C324 87D7 8F95 819D 941C 6831 9396 48F0 1B4C
```

This is the maintainer's dedicated community release key, not a Red Hat,
Oracle, CentOS, OpenSSL or PHP upstream signature. Fetching a key and software
from the same site is not independent identity verification; confirm the
fingerprint through a trusted channel before trusting it.

## Source, build and license

The SPEC in this repository is the one embedded in the published source RPM.
The SRPM includes the complete upstream source and necessary build inputs,
not merely a download link. See [BUILD.md](BUILD.md).

OpenSSL is distributed under Apache-2.0; its license/notice files are preserved
in the sources and RPM. New repository helper scripts and documentation are
MIT licensed; this does not relicense OpenSSL. See [LICENSE](LICENSE).

## Limitations

- Tested on EL7 x86_64; not certified for every downstream EL7 configuration.
- Six build/test workers are hard-coded; provision sufficient RAM/disk.
- No FIPS certification claim.
- This is not a blanket security guarantee or ongoing enterprise support.
- Private trust defaults require deliberate configuration. For the PHP stack,
  see its opt-in CA-policy package and documented legacy OS limitations.
