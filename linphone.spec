%define name 	linphone
%define version 3.2.1
%define release %mkrel 3

%define linphone_major 3
%define mediastreamer_major 0
%define libname_linphone %mklibname %name %linphone_major
%define libname_mediastreamer %mklibname mediastreamer %mediastreamer_major
%define libname_devel %mklibname -d %name

Name: 		%name
Version: 	%version
Release: 	%release
Summary: 	Voice over IP Application
License: 	GPLv2+
Group: 		Communications
URL: 		http://www.linphone.org/
Source0:	http://download.savannah.gnu.org/releases/linphone/stable/sources/linphone-%{version}.tar.gz
Source1:	http://download.savannah.gnu.org/releases/linphone/stable/sources/linphone-%{version}.tar.gz.sig
Source2:	%{name}48.png
Source3:	%{name}32.png
Source4:	%{name}16.png
Patch0:         linphone-3.2.0-imagedir.patch
Patch1:		linphone-3.1.1-ni_maxhost_hack.patch
Patch2:		linphone-2.1.0-no_werror.patch
Patch3:		linphone-3.2.0-intltoolize_fix.diff
Patch5:		linphone-3.1.1-fix-str-fmt.patch
Patch7:		linphone-3.2.0-ortp-linking-fix.patch
BuildRequires:	SDL-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	desktop-file-utils
BuildRequires:	exosip-devel >= 3.0.3
BuildRequires:	ffmpeg-devel
BuildRequires:	gettext
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel
BuildRequires:	gnome-panel-devel
BuildRequires:	gnomeui2-devel
BuildRequires:	gsm-devel
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	jackit-devel
BuildRequires:	libglade2.0-devel
BuildRequires:	libosip2-devel >= 3.0.3
BuildRequires:	libpanel-applet-2-devel
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	resample-devel
BuildRequires:	speex-devel
BuildRequires:	ortp-devel >= 0.16.1
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Linphone is web-phone with a GNOME2 interface. It uses open protocols
such as SIP and RTP to make the communications.

%package -n     %{libname_linphone}
Summary:        Primary library for %name
Group:          System/Libraries

%description -n %{libname_linphone}
Primary library for %name.

%package -n     %{libname_mediastreamer}
Summary:        Media Streaming library for %name
Group:          System/Libraries

%description -n %{libname_mediastreamer}
Media Streaming library for %name.

%package -n     %{libname_devel}
Summary:        Header files and static libraries from %name
Group:          Development/C
Requires:       %{libname_linphone} = %{version}-%{release}
Provides:       lib%{name}-devel = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}
Obsoletes:      %{name}-devel < %{version}-%{release}
Obsoletes:      %mklibname -d %{name} 1

%description -n %{libname_devel}
Libraries and includes files for developing programs based on %name.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p0
%patch5 -p0
%patch7 -p0

%build
autoreconf -fi

pushd mediastreamer2
autoreconf -fi
popd

%configure2_5x \
    --enable-alsa \
    --disable-strict \
    --enable-external-ortp=yes \
    --enable-ipv6
%make

%install
rm -rf %{buildroot}

%makeinstall_std

%find_lang %name

perl -pi -e "s|linphone/linphone2\.png|linphone2|g" %{buildroot}%{_datadir}/applications/linphone.desktop
desktop-file-install \
	--vendor="" \
	--add-category="VideoConference" \
	--remove-category='Application' \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/linphone.desktop

#icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m 644 %{_sourcedir}/linphone16.png \
	%{buildroot}%{_iconsdir}/hicolor/16x16/apps/linphone2.png
install -m 644 %{_sourcedir}/linphone32.png \
	%{buildroot}%{_iconsdir}/hicolor/32x32/apps/linphone2.png
install -m 644 %{_sourcedir}/linphone48.png \
	%{buildroot}%{_iconsdir}/hicolor/48x48/apps/linphone2.png
mkdir -p %{buildroot}/%_miconsdir
ln -s ../hicolor/16x16/apps/linphone2.png \
      %{buildroot}/%_miconsdir/
mkdir -p %{buildroot}/%_iconsdir
ln -s hicolor/32x32/apps/linphone2.png \
      %{buildroot}/%_iconsdir/
mkdir -p %{buildroot}/%_liconsdir
ln -s ../hicolor/48x48/apps/linphone2.png \
      %{buildroot}/%_liconsdir/

%multiarch_includes %{buildroot}%{_includedir}/linphone/config.h

# remove unwanted docs, generated if doxygen is installed
rm -rf %{buildroot}%{_docdir}/ortp

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%update_menus
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%post -n %{libname_linphone} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname_linphone} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libname_mediastreamer} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname_mediastreamer} -p /sbin/ldconfig
%endif

%files -f %name.lang
%defattr(-,root,root)
%doc COPYING README AUTHORS BUGS INSTALL ChangeLog
%doc %_datadir/gnome/help/%name
%_bindir/linphone*
%_bindir/sipomatic
%_libdir/mediastream
%_mandir/man1/*
%lang(cs) %_mandir/cs/man1/*
%_datadir/pixmaps/%name
%_datadir/sounds/%name
%{_datadir}/images/linphone/nowebcamCIF.jpg
%_datadir/applications/*
%{_iconsdir}/hicolor/*/apps/linphone2.png
%{_liconsdir}/linphone2.png
%{_iconsdir}/linphone2.png
%{_miconsdir}/linphone2.png
%{_datadir}/linphone

%files -n %{libname_linphone}
%defattr(-,root,root)
%{_libdir}/liblinphone.so.%{linphone_major}*

%files -n %{libname_mediastreamer}
%defattr(-,root,root)
%{_libdir}/libmediastreamer.so.%{mediastreamer_major}*

%files -n %{libname_devel}
%defattr(-,root,root)
%dir %{_includedir}/linphone
%multiarch %{multiarch_includedir}/linphone/config.h
%{_includedir}/linphone/*
%{_includedir}/mediastreamer2/*
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc
