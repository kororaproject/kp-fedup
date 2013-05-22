Name:           fedup
Version:        0.7.3
Release:        0%{?dist}
Summary:        The Fedora Upgrade tool

License:        GPLv2+
URL:            https://github.com/wgwoods/fedup
Source0:        https://github.com/downloads/wgwoods/fedup/%{name}-%{version}.tar.xz

# Require updates to various packages where necessary to fix bugs.
# Bug #910326
Requires:       systemd >= systemd-44-23.fc17
Requires:       grubby

BuildRequires:  python2-devel
BuildRequires:  systemd-devel
BuildRequires:  asciidoc
BuildArch:      noarch


# TODO: uncomment this once we figure out why PackageKit requires preupgrade..
#Obsoletes:      preupgrade
#Provides:       preupgrade

%description
fedup is the Fedora Upgrade tool.


%prep
%setup -q

%build
make PYTHON=%{__python}

%install
rm -rf $RPM_BUILD_ROOT
make install PYTHON=%{__python} DESTDIR=$RPM_BUILD_ROOT MANDIR=%{_mandir}
# backwards compatibility symlinks, wheee
ln -sf fedup $RPM_BUILD_ROOT/%{_bindir}/fedup-cli
ln -sf fedup.8 $RPM_BUILD_ROOT/%{_mandir}/man8/fedup-cli.8
# updates dir
mkdir -p $RPM_BUILD_ROOT/etc/fedup/update.img.d



%files
%doc README.asciidoc TODO.asciidoc COPYING
# systemd stuff
%{_unitdir}/system-upgrade.target
%{_unitdir}/upgrade-prep.service
%{_unitdir}/upgrade-switch-root.service
%{_unitdir}/upgrade-switch-root.target
%{_unitdir}/../upgrade-prep.sh
# python library
%{python_sitelib}/fedup*
# binaries
%{_bindir}/fedup
%{_bindir}/fedup-cli
# man pages
%{_mandir}/man*/*
# empty config dir
%dir /etc/fedup
# empty updates dir
%dir /etc/fedup/update.img.d

#TODO - finish and package gtk-based GUI
#files gtk
#{_bindir}/fedup-gtk
#{_datadir}/fedup/ui

%changelog
* Fri Mar 15 2013 Will Woods <wwoods@redhat.com> 0.7.3-0
- Write debuglog by default (/var/log/fedup.log)
- Add support for applying updates to upgrade.img
- Use proxy settings from yum.conf (#892994)
- Fix "NameError: global name 'po' is not defined" (#895576)
- Clearer error on already-upgraded systems (#895967)
- Fix upgrade hang with multiple encrypted partitions (#896010)
- Fix "OSError: [Errno 2]..." when `selinuxenabled` is not in PATH (#896721)
- Fix tracebacks on bad arguments to --iso (#896440, #895665)
- Fix traceback if grubby is missing (#896194)
- Require newer systemd to fix hang on not-updated systems (#910326)
- Fix hang starting upgrade on systems with /dev/md* (#895805)
- Better error messages if you're out of disk space (#896144)

* Thu Dec 06 2012 Will Woods <wwoods@redhat.com> 0.7.2-1
- Fix grubby traceback on EFI systems (#884696)
- Fix traceback if /var/tmp is a different filesystem from /var/lib (#883107)
- Disable SELinux during upgrade if system has SELinux disabled (#882549)
- Use new-kernel-pkg to set up bootloader (#872088, #879290, #881338)
- Remove boot option after upgrade (#873065)
- Fix running on minimal systems (#885990)
- Work around wrong/missing plymouth theme (#879295)
- Get instrepo automatically if available (#872899, #882141)
- Rename 'fedup-cli' to 'fedup'
- Rename '--repourl' to '--addrepo'
- Add mirrorlist support for --addrepo/--instrepo
- Clearer messages for most errors
- Fix --iso

* Mon Nov 19 2012 Will Woods <wwoods@redhat.com> 0.7.1-1
- Add --clean commandline argument
- Fix grubby traceback (#872088)
- Fetch kernel/initrd and set up bootloader
- Work around data-corrupting umount bug (#873459)
- Add support for upgrades from media (--device)

* Wed Oct 24 2012 Will Woods <wwoods@redhat.com> 0.7-1
- Initial packaging
