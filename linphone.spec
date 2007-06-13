%define name 	linphone
%define version 1.7.1
%define release %mkrel 1

%define major	1
%define libname %mklibname %name %major

Name: 		%name
Version: 	%version
Release: 	%release
Summary: 	Voice over IP Application
License: 	GPL
Group: 		Communications
URL: 		http://www.linphone.org/
Source0:	http://download.savannah.gnu.org/releases/linphone/stable/sources/linphone-%{version}.tar.gz
Source1:	http://download.savannah.gnu.org/releases/linphone/stable/sources/linphone-%{version}.tar.gz.sig
Source2:	%{name}48.png
Source3:	%{name}32.png
Source4:	%{name}16.png
Patch0:		linphone-1.5.0-ppc.patch
BuildRequires:	SDL-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	jackit-devel
BuildRequires:	libosip-devel >= 2.0.0
BuildRequires:	libpanel-applet-2-devel
BuildRequires:	libreadline-devel
BuildRequires:	libspeex-devel
BuildRequires:	ncurses-devel
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
    --enable-alsa \
    --disable-strict

%make

%install
rm -rf %{buildroot}

%makeinstall

%find_lang %name

desktop-file-install \
	--vendor="" \
	--add-category="X-MandrivaLinux-Internet-VideoConference" \
	--dir %{buildroot}%{_datadir}/applications \
	$RPM_BUILD_ROOT%{_datadir}/applications/linphone.desktop

#icons
mkdir -p $RPM_BUILD_ROOT%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m 644 %{_sourcedir}/linphone16.png \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/16x16/apps/linphone2.png
install -m 644 %{_sourcedir}/linphone32.png \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/32x32/apps/linphone2.png
install -m 644 %{_sourcedir}/linphone48.png \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/48x48/apps/linphone2.png

%if %mdkversion >= 1020
%multiarch_includes %{buildroot}%{_includedir}/linphone/config.h
%endif

# remove unwanted docs, generated if doxygen is installed
rm -rf $RPM_BUILD_ROOT%{_docdir}/ortp

%clean
rm -rf %{buildroot}

%post
%update_menus
%update_icon_cache hicolor

%postun
%clean_menus
%update_icon_cache hicolor

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files -f %name.lang
%defattr(-,root,root)
%doc COPYING README AUTHORS BUGS INSTALL ChangeLog
%doc %_datadir/gnome/help/%name
%_bindir/linphone*
%_bindir/sipomatic
%_libdir/mediastream
%_mandir/man1/*
%_datadir/pixmaps/%name
%_datadir/sounds/%name
%_datadir/gnome/apps/Internet/%name.desktop
%{_datadir}/images/nowebcamCIF.jpg
%_datadir/applications/*
%{_iconsdir}/hicolor/*/apps/linphone2.png

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/liblinphone.so.%{major}*
%{_libdir}/libmediastreamer.so.*
%{_libdir}/libortp.so.*
%{_libdir}/libquickstream.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
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

