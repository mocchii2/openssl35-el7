# Verify and install

Take a tested recovery backup first. Unpack release assets into a dedicated
directory and retain the original files. Do not pipe downloaded scripts to root.

Verify the published key fingerprint against a trusted copy, then use a
dedicated GnuPG home (the imported key below is public, not a private key):

```sh
mkdir -m 700 verify-keyring
gpg2 --homedir ./verify-keyring --import RPM-GPG-KEY-muhoho-php84
gpg2 --homedir ./verify-keyring --fingerprint
gpg2 --homedir ./verify-keyring --verify SHA256SUMS.asc SHA256SUMS
sha256sum -c SHA256SUMS
```

All files named by SHA256SUMS must be downloaded before the checksum command.
Verify **before** unpacking the binary/source tar archives. The detached
manifest authenticates both the binaries and the corresponding sources.

After deliberately trusting the key, register it in RPM and check every RPM:

```sh
sudo rpm --import RPM-GPG-KEY-muhoho-php84
rpm -Kv RPMS/*.rpm
sudo yum --disablerepo='*' --setopt=localpkg_gpgcheck=1 \
  --setopt=tsflags=test localinstall RPMS/*.rpm
```

Inspect the complete transaction. Resolve dependencies using vendor-signed
packages; do not disable GPG checks or replace system OpenSSL.
Only after review, run the same command **without** `--setopt=tsflags=test`.

```sh
/opt/openssl35/bin/openssl version -a
```

This does not change `/usr/bin/openssl` or relink nginx/system services.
The matching PHP stack needs both runtime/devel packages for building; a
standalone runtime-only installation can select just `openssl35-muhoho`.
The default private CA path is `/opt/openssl35/ssl/cert.pem`; configure trust
deliberately before using the private CLI for peer verification.

## Rollback

Removal can break applications depending on these private libraries.
Use normal package transactions with dependency review and a tested snapshot
recovery procedure; never force-remove packages.
