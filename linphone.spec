%define name 	linphone
%define version 1.6.0
%define release %mkrel 2

%define major	1
%define libname %mklibname %name %major

Name: 		%name
Version: 	%version
Release: 	%release
Summary: 	Voice over IP Application
License: 	GPL
Group: 		Communications
URL: 		http://www.linphone.org/
Source: 	http://download.savannah.nongnu.org/releases/linphone/stable/source/%{name}-%{version}.tar.bz2
Source1: 	%{name}48.png
Source2: 	%{name}32.png
Source3: 	%{name}16.png
Patch0:		linphone-1.5.0-ppc.patch
BuildRequires:	SDL-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	jackit-devel
BuildRequires:	libosip-devel >= 2.0.0
BuildRequires:	libpanel-applet-2-devel
BuildRequires:	libreadline-devel
BuildRequires:	libspeex-devel
BuildRequires:	ncurses-devel
#BuildRequires:	libalsa-devel
#BuildRequires:	libsamplerate-devel
BuildRequires:	gtk-doc docbook-dtd41-sgml docbook-dtd30-sgml
#if %mdkversion >= 1020
#BuildRequires:  multiarch-utils >= 1.0.3
#endif
BuildRoot: 	%{_tmppath}/%{name}-buildroot

%description
Linphone is web-phone with a GNOME2 interface. It uses open protocols
such as SIP and RTP to make the communications.

%package -n     %{libname}
Summary:        Dynamic libraries from %name
Group:          System/Libraries
Conflicts:	%{mklibname ortp 2}

%description -n %{libname}
Dynamic libraries from %name.

%package -n     %{libname}-devel
Summary:        Header files and static libraries from %name
Group:          Development/C
Requires:       %{libname} >= %{version}
Provides:       lib%{name}-devel = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}
Obsoletes:      %name-devel
Conflicts:	%{mklibname ortp 2}-devel

%description -n %{libname}-devel
Libraries and includes files for developing programs based on %name.

%prep

%setup -q
%patch0 -p1 -b .ppc

%build

%configure2_5x \
    --enable-static \
    --enable-shared \
    --enable-alsa

%make

%install
rm -rf %{buildroot}

%makeinstall

%find_lang %name

#mdk menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%name): command="%{name}" \
icon="%{name}.png" \
needs="x11" \
title="LinPhone" \
longtitle="Voice over IP" \
section="More Applications/Communications"
EOF

rm -rf %_datadir/applications/%{name}.desktop
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Linphone
Comment=Voice over IP Application
Exec=linphone
Icon=linphone2
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Internet-VideoConference;
EOF


#icons
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
cat %SOURCE1 > $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
cat %SOURCE2 > $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
cat %SOURCE3 > $RPM_BUILD_ROOT/%_miconsdir/%name.png

%if %mdkversion >= 1020
%multiarch_includes %{buildroot}%{_includedir}/linphone/config.h
%endif

%clean
rm -rf %{buildroot}

%post
%update_menus

%postun
%clean_menus

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files -f %name.lang
%defattr(-,root,root)
%doc COPYING README AUTHORS BUGS INSTALL ChangeLog
%doc %_datadir/gnome/help/%name
%_bindir/linphone*
%_bindir/sipomatic
%_libdir/linphone_applet
%_libdir/mediastream
%_libdir/bonobo/servers/*.server
%_mandir/man1/*
%_datadir/pixmaps/%name
%_datadir/sounds/%name
%_datadir/gnome/apps/Internet/%name.desktop
%_datadir/gnome-2.0/ui/*
#%_datadir/linphonec/linphonec
%_datadir/applications/*
%_menudir/%name
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_datadir}/gtk-doc/html/*
%dir %{_includedir}/linphone
%dir %{_includedir}/ortp
%if %mdkversion >= 1020
%multiarch %{multiarch_includedir}/linphone/config.h
%endif
%{_includedir}/linphone/*
%{_includedir}/mediastreamer2/*
%{_includedir}/ortp/*
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc


