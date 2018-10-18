Name: tmate
Version: 2.2.1
Release: 1
License: BSD
Summary: Instant Terminal Sharing
BuildArch: x86_64
Source: https://github.com/tmate-io/tmate/archive/%{version}.tar.gz

BuildRequires: openssl-devel zlib-devel ruby ncurses-devel libssh-devel msgpack-devel libevent-devel
Requires: openssl zlib ncurses libssh msgpack libevent

%description

Tmate is a fork of tmux. It provides an instant pairing solution.

%prep

%setup -n tmate-%{version}

%build

./autogen.sh
./configure --prefix=/usr
make

%install

make install DESTDIR=%buildroot

%clean

rm -rf %buildroot

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz

%changelog
* Thu Oct 18 2018 Bernd Helmle <bernd.helmle@credativ.de> 2.2.1-1
- Upstream release 2.2.1
