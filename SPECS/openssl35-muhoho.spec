Name:           openssl35-muhoho
Version:        3.5.9
Release:        3%{?dist}
Summary:        Private OpenSSL 3.5 LTS runtime for the muhoho PHP stack
License:        Apache-2.0
URL:            https://www.openssl-library.org/
Source0:        https://github.com/openssl/openssl/releases/download/openssl-%{version}/openssl-%{version}.tar.gz

BuildRequires:  perl-core
BuildRequires:  make
BuildRequires:  zlib-devel
Requires:       zlib

# This package intentionally does not replace or provide the system openssl.
# Its private SONAMEs are resolved through an executable RUNPATH.

%description
OpenSSL 3.5 LTS installed below /opt/openssl35 for PHP 8.4. It is isolated
from the CentOS 7 system OpenSSL used by yum, SSH, nginx and system services.

%package devel
Summary:        Development files for the private OpenSSL 3.5 LTS runtime
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       zlib-devel

%description devel
Headers, pkg-config metadata and static development symlinks used to build
the private PHP 8.4 stack against /opt/openssl35.

%prep
%setup -q -n openssl-%{version}

%build
source /opt/rh/devtoolset-12/enable
export CFLAGS="%{optflags} -fPIC"
export LDFLAGS="-Wl,-z,relro -Wl,-z,now -Wl,--enable-new-dtags -Wl,-rpath,/opt/openssl35/lib64"
./Configure linux-x86_64 \
    --prefix=/opt/openssl35 \
    --openssldir=/opt/openssl35/ssl \
    --libdir=lib64 \
    shared zlib enable-pic
make -j6

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install_sw install_ssldirs
rm -f %{buildroot}/opt/openssl35/lib64/*.a
# tsget is not needed by PHP and would add an unavailable EL7 perl-WWW-Curl
# runtime dependency. Keep the CA helper, but omit this optional HTTP client.
rm -f %{buildroot}/opt/openssl35/ssl/misc/tsget \
      %{buildroot}/opt/openssl35/ssl/misc/tsget.pl

%check
HARNESS_JOBS=6 make test
readelf -d %{buildroot}/opt/openssl35/bin/openssl | grep -q 'RUNPATH.*\[/opt/openssl35/lib64\]'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE.txt
%doc README.md CHANGES.md
%dir /opt/openssl35
/opt/openssl35/bin/openssl
/opt/openssl35/bin/c_rehash
/opt/openssl35/lib64/libcrypto.so.3
/opt/openssl35/lib64/libssl.so.3
%dir /opt/openssl35/lib64/engines-3
/opt/openssl35/lib64/engines-3/*.so
%dir /opt/openssl35/lib64/ossl-modules
/opt/openssl35/lib64/ossl-modules/*.so
%dir /opt/openssl35/ssl
%config(noreplace) /opt/openssl35/ssl/openssl.cnf
%config(noreplace) /opt/openssl35/ssl/ct_log_list.cnf
/opt/openssl35/ssl/openssl.cnf.dist
/opt/openssl35/ssl/ct_log_list.cnf.dist
%dir /opt/openssl35/ssl/certs
%dir /opt/openssl35/ssl/private
%dir /opt/openssl35/ssl/misc
/opt/openssl35/ssl/misc/*

%files devel
/opt/openssl35/include
/opt/openssl35/lib64/libcrypto.so
/opt/openssl35/lib64/libssl.so
/opt/openssl35/lib64/pkgconfig
/opt/openssl35/lib64/cmake

%changelog
* Sat Oct 24 2026 Codex Build <root@localhost> - 3.5.9-3
- Drop the optional tsget helper to avoid an unavailable EL7 Perl dependency.

* Sat Oct 24 2026 Codex Build <root@localhost> - 3.5.9-2
- Use deterministic build/test parallelism and enforce the private library RUNPATH.

* Sat Oct 24 2026 Codex Build <root@localhost> - 3.5.9-1
- Initial isolated EL7 package for the PHP 8.4 migration.
