%define linphone_major 4
%define mediastreamer_major 1
%define liblinphone %mklibname %{name} %{linphone_major}
%define libmediastreamer %mklibname mediastreamer %{mediastreamer_major}
%define libname_devel %mklibname -d %{name}

Name:		linphone
Version:	3.5.2
Release:	2
Summary:	Voice over IP Application
License:	GPLv2+
Group:		Communications
URL:		http://www.linphone.org/
Source0:	http://download.savannah.gnu.org/releases/linphone/stable/sources/linphone-%{version}.tar.gz
Source1:	http://download.savannah.gnu.org/releases/linphone/stable/sources/linphone-%{version}.tar.gz.sig
Source2:	%{name}48.png
Source3:	%{name}32.png
Source4:	%{name}16.png
Patch0:		linphone-3.2.0-imagedir.patch
Patch1:		linphone-3.5.0-link.patch
Patch2:		linphone-3.5.2-ffmpeg-0.11.patch
BuildRequires:	desktop-file-utils
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	gettext
BuildRequires:	exosip-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	gettext-devel
BuildRequires:	gsm-devel
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libosip2)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libv4l1)
BuildRequires:	pkgconfig(libv4l2)
BuildRequires:	pkgconfig(ortp) >= 0.17.0
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xv)

%description
Linphone is web-phone with a GNOME2 interface. It uses open protocols
such as SIP and RTP to make the communications.

#--------------------------------------------------------------------
%package -n %{liblinphone}
Summary:	Primary library for %{name}
Group:		System/Libraries

%description -n %{liblinphone}
Primary library for %{name}.

#--------------------------------------------------------------------
%package -n %{libmediastreamer}
Summary:	Media Streaming library for %{name}
Group:		System/Libraries

%description -n %{libmediastreamer}
Media Streaming library for %{name}.

#--------------------------------------------------------------------
%package -n %{libname_devel}
Summary:	Header files and static libraries from %{name}
Group:		Development/C
Requires:	%{liblinphone} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{libname_devel}
Libraries and includes files for developing programs based on %{name}.

#--------------------------------------------------------------------
%prep
%setup -q
%patch0 -p0 -b .image-dir
%patch1 -p0 -b .link
%patch2 -p1 -b .ffmpeg11~

%build
./autogen.sh

( pushd mediastreamer2
./autogen.sh
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
%__rm -rf %{buildroot}

%makeinstall_std

%find_lang %{name} --all-name --with-man

%__perl -pi -e "s|linphone/linphone2\.png|linphone2|g" %{buildroot}%{_datadir}/applications/linphone.desktop
desktop-file-install \
	--vendor="" \
	--add-category="VideoConference" \
	--remove-category='Application' \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/linphone.desktop

#icons
%__mkdir_p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
%__install -m 644 %{SOURCE4} \
	%{buildroot}%{_iconsdir}/hicolor/16x16/apps/linphone2.png
%__install -m 644 %{SOURCE3} \
	%{buildroot}%{_iconsdir}/hicolor/32x32/apps/linphone2.png
%__install -m 644 %{SOURCE2} \
	%{buildroot}%{_iconsdir}/hicolor/48x48/apps/linphone2.png
%__mkdir_p %{buildroot}/%{_miconsdir}
%__ln_s ../hicolor/16x16/apps/linphone2.png \
      %{buildroot}/%{_miconsdir}/
%__mkdir_p %{buildroot}/%{_iconsdir}
%__ln_s hicolor/32x32/apps/linphone2.png \
      %{buildroot}/%{_iconsdir}/
%__mkdir_p %{buildroot}/%{_liconsdir}
%__ln_s ../hicolor/48x48/apps/linphone2.png \
      %{buildroot}/%{_liconsdir}/

%multiarch_includes %{buildroot}%{_includedir}/linphone/config.h

# remove unwanted docs, generated if doxygen is installed
%__rm -rf %{buildroot}%{_docdir}/ortp %{buildroot}%{_docdir}/mediastreamer

%files -f %{name}.lang
%doc COPYING README AUTHORS BUGS INSTALL ChangeLog
%doc %{_datadir}/gnome/help/%{name}
%{_bindir}/linphone*
%{_bindir}/mediastream
%{_mandir}/man1/*
%{_datadir}/pixmaps/%{name}/
%{_datadir}/sounds/%{name}/
%{_datadir}/images/linphone/nowebcamCIF.jpg
%{_datadir}/applications/*
%{_iconsdir}/hicolor/*/apps/linphone2.png
%{_liconsdir}/linphone2.png
%{_iconsdir}/linphone2.png
%{_miconsdir}/linphone2.png
%{_datadir}/linphone/

%files -n %{liblinphone}
%{_libdir}/liblinphone.so.%{linphone_major}*

%files -n %{libmediastreamer}
%{_libdir}/libmediastreamer.so.%{mediastreamer_major}*

%files -n %{libname_devel}
%{multiarch_includedir}/linphone/config.h
%{_includedir}/linphone/
%{_includedir}/mediastreamer2/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

