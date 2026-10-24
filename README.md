# OpenSSL 3.5.9 RPMs for EL7 (x86_64)

> **Emergency use:** Test/deploy private OpenSSL 3.5 as a temporary bridge to a supported OS.<br>
> **Target:** EL7 x86_64, private `/opt/openssl35` prefix; build/test environment: Oracle Linux 7.9.<br>
> **No warranty:** EL7 is EOL; no security or compatibility guarantee. System OpenSSL is not upgraded.

[Installation](INSTALL.md) | **[Rollback / recovery plan](INSTALL.md#rollback)**

[English](README.md) | [日本語 / Japanese](README.ja.md)

## What this repository does

Install OpenSSL 3.5.9 on EL7 using signed RPMs.<br>
Add it under `/opt/openssl35` without replacing system OpenSSL.<br>
Rebuild from the complete corresponding source RPM and SPEC.

## Target environment

- OS: EL7-family Linux (CentOS 7 / RHEL 7 / Oracle Linux 7).
- Architecture: **x86_64 only**. Build/test environment: Oracle Linux 7.9.
- Not certified on every derivative/configuration. Not for EL8/9 or aarch64.

## Quickstart: signature verification through installation

**Use a fresh/test EL7 host.** Take a recovery snapshot and install `curl`,
`gnupg2`, `tar`, `yum` and `sudo` from trusted OS repositories first.
The commands install both runtime and development RPMs. Dependencies must be
available from signature-verified OS repositories or installed beforehand.
Do not ignore GPG/dependency errors; review yum's proposed changes.

Confirm the public-key fingerprint through an independent trusted channel.
Downloading a key and software from the same site is not independent identity
verification. Run the command block below in an interactive terminal:
yum reads its confirmation from `/dev/tty`.

```sh
bash <<'BASH'
set -euo pipefail
work=$(mktemp -d "$HOME/openssl35-el7.XXXXXX")
cd "$work"
base=https://github.com/mocchii2/openssl35-el7/releases/download/openssl-3.5.9-3.el7
for file in openssl35-el7-binary-rpms.tar.gz openssl35-el7-source-rpms.tar.gz \
  PACKAGES.tsv source-inputs.sha256 RPM-GPG-KEY-muhoho-php84 SHA256SUMS SHA256SUMS.asc; do
  curl --fail --show-error --location --connect-timeout 20 --max-time 600 \
    --output "$file" "$base/$file"
done
mkdir -m 700 verify-keyring
gpg2 --homedir "$PWD/verify-keyring" --batch --import RPM-GPG-KEY-muhoho-php84
gpg2 --homedir "$PWD/verify-keyring" --batch --with-colons --fingerprint |
  grep -q '^fpr:::::::::F31EC32487D78F95819D941C6831939648F01B4C:'
gpg2 --homedir "$PWD/verify-keyring" --batch --verify SHA256SUMS.asc SHA256SUMS
sha256sum -c SHA256SUMS
tar -xzf openssl35-el7-binary-rpms.tar.gz
sudo rpm --import RPM-GPG-KEY-muhoho-php84
rpm -Kv RPMS/*.rpm
sudo yum --setopt=gpgcheck=1 --setopt=localpkg_gpgcheck=1 \
  --setopt=tsflags=test localinstall RPMS/*.rpm </dev/tty
# Review the test transaction, then approve the real transaction at yum's prompt.
sudo yum --setopt=gpgcheck=1 --setopt=localpkg_gpgcheck=1 localinstall RPMS/*.rpm </dev/tty
/opt/openssl35/bin/openssl version
printf 'Downloaded files retained in: %s\n' "$work"
BASH
```

## Known limitations

- **EL7 is end-of-life.** Migrate to a supported OS.
- Does not update `/usr/bin/openssl` or TLS used by nginx, SSH or yum.
- No FIPS certification or guarantee that every vulnerability is fixed.
- Review CA configuration before making connections; review dependencies
  before removing these packages.
- See [INSTALL.md](INSTALL.md) and Limitations below for details.

## Observed version output (2026-10-24)

Captured on the EL7 x86_64 test VM.

```console
$ /opt/openssl35/bin/openssl version
OpenSSL 3.5.9 29 Sep 2026 (Library: OpenSSL 3.5.9 29 Sep 2026)
```

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
