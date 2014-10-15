Summary:	Network monitoring tools including ping
Name:		iputils
Version:	20140620
Release:	%mkrel 3
License:	BSD
Group:		System/Base
URL:		http://www.linux-ipv6.org/gitweb/gitweb.cgi?p=gitroot/iputils.git
Source0:	http://www.skbuff.net/iputils/%{name}-%{version}.tar.xz
# ifenslave.c seems to come from linux-2.6.25/Documentation/networking/ifenslave.c
Source1:	ifenslave.c
# bonding.txt seems to come from linux-2.6.25/Documentation/networking/bonding.txt
Source2:	bonding.txt
Source3:	ifenslave.8
Source4:	bin.ping.apparmor
Patch0:		iputils-ifenslave.patch
Requires(pre):	filesystem >= 2.1.9-18
BuildRequires:	docbook-dtd31-sgml
BuildRequires:	libidn-devel
BuildRequires:	libsysfs-devel
BuildRequires:	perl-SGMLSpm
BuildRequires:	openssl-devel
BuildRequires:	libcap-devel
BuildRequires:	gnutls-devel
BuildRequires:	libgcrypt-devel

%description
The iputils package contains ping, a basic networking tool. The ping command
sends a series of ICMP protocol ECHO_REQUEST packets to a specified network
host and can tell you if that machine is alive and receiving network traffic.

%prep

%setup -q

cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .

%patch0 -p1 -b .addr

%build
%serverbuild
perl -pi -e 's!\$\(MAKE\) -C doc html!!g' Makefile
%make IDN="yes" OPTFLAGS="%{optflags} -fno-strict-aliasing"
%make ifenslave CFLAGS="%{optflags}"

make man

%install
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man8

install -c clockdiff		%{buildroot}%{_sbindir}/

install -c arping %{buildroot}%{_sbindir}/

install -c ping %{buildroot}%{_bindir}/
install -c ifenslave %{buildroot}%{_sbindir}/
install -c ping6 %{buildroot}%{_bindir}/
install -c rdisc %{buildroot}%{_sbindir}/
install -c tracepath %{buildroot}%{_sbindir}/
install -c tracepath6 %{buildroot}%{_sbindir}/
install -c traceroute6 %{buildroot}%{_sbindir}/

install -c doc/*.8 %{buildroot}%{_mandir}/man8/
install -c ifenslave.8 %{buildroot}%{_mandir}/man8/

# these manpages are provided by other packages
rm -f %{buildroot}%{_mandir}/man8/rarpd.8*
rm -f %{buildroot}%{_mandir}/man8/tftpd.8*

# apparmor profile
mkdir -p %{buildroot}%{_sysconfdir}/apparmor.d/
install -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/apparmor.d/bin.ping

%posttrans
# if we have apparmor installed, reload if it's being used
if [ -x /sbin/apparmor_parser ]; then
        /sbin/service apparmor condreload
fi

%files
%doc RELNOTES bonding.txt
%config(noreplace) %{_sysconfdir}/apparmor.d/bin.ping
%{_sbindir}/clockdiff
%attr(4755,root,root)	%{_bindir}/ping
%{_sbindir}/arping
%{_sbindir}/ifenslave
#%ifnarch ppc
%attr(4755,root,root) %{_bindir}/ping6
%{_sbindir}/tracepath6
#%endif
%{_sbindir}/tracepath
%attr(4755,root,root) %{_sbindir}/traceroute6
%{_sbindir}/rdisc
%{_mandir}/man8/*


