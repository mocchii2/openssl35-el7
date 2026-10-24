# OpenSSL 3.5.9 RPMs for EL7 (x86_64)

> **緊急対応向け:** EL7環境で専用のOpenSSL 3.5系を迅速に検証・導入するための手順・ビルド設定集です。
> OS標準のOpenSSLは置き換えません。サポート対象OSへの移行までの暫定対応を想定しています。

## このリポジトリでできること（3行）

EL7向けのOpenSSL 3.5.9を、署名付きRPMでインストールできます。<br>
システムのOpenSSLを置き換えず、`/opt/openssl35` に追加できます。<br>
完全な対応ソースRPMとSPECを使って、自分でビルドできます。

## 対応環境

- OS: EL7系 Linux（CentOS 7 / RHEL 7 / Oracle Linux 7）。
- アーキテクチャ: **x86_64のみ**。検証用ビルド環境はOracle Linux 7.9。
- 全派生OSでの動作保証はありません。EL8/9、aarch64用ではありません。

## 最短手順（署名確認からインストールまで）

**新規・検証用EL7ホストで実行してください。** スナップショットを取得し、
信頼できるOSリポジトリから `curl`、`gnupg2`、`tar`、`yum`、`sudo` を用意します。
下記はランタイムと開発用RPMをインストールします。依存関係の取得には、
署名検証が有効なOSリポジトリ、または事前に導入した依存RPMが必要です。
GPGエラーや依存エラーを無視せず、yumの変更内容を確認してください。

公開鍵の指紋は、別の信頼できる経路でも確認してください。同じ配布元からの
鍵とファイルの取得だけでは、配布元の身元を独立に確認したことになりません。

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

## 注意点（既知の制約）

- **EL7はEOLです。** サポートされるOSへの移行を推奨します。
- OSの `/usr/bin/openssl` やnginx、SSH、yumのTLSは更新しません。
- FIPS認証や、すべての脆弱性への対応を保証するものではありません。
- 通信に使用する前にCA設定を確認してください。削除時も依存関係の確認が必要です。
- 詳細は [INSTALL.md](INSTALL.md) と下記のLimitationsを参照してください。

## 動作確認ログ（実測、2026-10-24）

EL7 x86_64の検証VMで取得した出力です。

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
