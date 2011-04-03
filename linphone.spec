%define name 	linphone
%define version 3.4.3
%define release %mkrel 1

%define linphone_major 4
%define mediastreamer_major 1
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
Patch8:		linphone-3.3.2-libv4l.patch
BuildRequires:	alsa-lib-devel
BuildRequires:	desktop-file-utils
BuildRequires:	exosip-devel >= 3.1.0
BuildRequires:	ffmpeg-devel
BuildRequires:	gettext
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel
BuildRequires:	gsm-devel
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	gtk+2-devel
BuildRequires:	libxv-devel
BuildRequires:	libxext-devel
BuildRequires:	libx11-devel
BuildRequires:	libosip2-devel >= 3.1.0
BuildRequires:	readline-devel
BuildRequires:	speex-devel
BuildRequires:	ortp-devel >= 0.16.3
BuildRequires:	libv4l-devel
BuildRequires:	libtheora-devel
BuildRequires:	pulseaudio-devel
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
%patch0 -p0 -b .image-dir
%patch8 -p0 -b .libv4l

%build
autoreconf -fi

( pushd mediastreamer2
autoreconf -fi
%before_configure
popd )

%configure2_5x \
    --disable-static \
    --disable-rpath \
    --enable-alsa \
    --disable-strict \
    --enable-external-ortp \
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
rm -rf %{buildroot}%{_docdir}/ortp %{buildroot}%{_docdir}/mediastreamer

# don't ship .la:
rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%files -f %name.lang
%defattr(-,root,root)
%doc COPYING README AUTHORS BUGS INSTALL ChangeLog
%doc %_datadir/gnome/help/%name
%_bindir/linphone*
#%_bindir/sipomatic
%_libdir/mediastream
%_mandir/man1/*
%lang(cs) %_mandir/cs/man1/*
%_datadir/pixmaps/%name
%_datadir/sounds/%name
%_datadir/tutorials/%name
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
#%doc %{_datadir}/doc/mediastreamer/
%{_includedir}/linphone
%multiarch %{multiarch_includedir}/linphone/config.h
%{_includedir}/mediastreamer2
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
