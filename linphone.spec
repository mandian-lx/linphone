%define linphone_major 6
%define mediastreamer_base_major 3
%define mediastreamer_voip_major 3
%define liblinphone %mklibname %{name} %{linphone_major}
%define libmediastreamer_base %mklibname mediastreamer_base %{mediastreamer_base_major}
%define libmediastreamer_voip %mklibname mediastreamer_voip %{mediastreamer_voip_major}
%define devname %mklibname -d %{name}

Summary:	Voice over IP Application
Name:		linphone
Version:	3.7.0
Release:	0.1
License:	GPLv2+
Group:		Communications
Url:		http://www.linphone.org/
Source0:	http://download.savannah.gnu.org/releases/linphone/stable/sources/linphone-%{version}.tar.gz
# Source1:	http://download.savannah.gnu.org/releases/linphone/stable/sources/linphone-%{version}.tar.gz.sig
Source2:	%{name}48.png
Source3:	%{name}32.png
Source4:	%{name}16.png
Patch0:		linphone-3.6.1-imagedir.patch
Patch1:		linphone-3.7.0-link.patch
BuildRequires:	desktop-file-utils
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	gettext
BuildRequires:	ffmpeg-devel
BuildRequires:	gettext-devel
BuildRequires:	gsm-devel
BuildRequires:	readline-devel
# http://lists.gnu.org/archive/html/linphone-developers/2013-04/msg00016.html
BuildRequires:	vim-common
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(belle-sip)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libosip2)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libv4l1)
BuildRequires:	pkgconfig(libv4l2)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(ortp) >= 0.23.0
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xv)

%description
Linphone is web-phone with a GNOME2 interface. It uses open protocols
such as SIP and RTP to make the communications.

%files -f %{name}.lang
%doc COPYING README AUTHORS BUGS INSTALL ChangeLog
%doc %{_datadir}/gnome/help/%{name}
%{_bindir}/linphone*
%{_bindir}/lp-gen-wrappers
%{_bindir}/mediastream
%{_bindir}/lpc2xml_test
%{_bindir}/xml2lpc_test
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

#--------------------------------------------------------------------

%package -n %{liblinphone}
Summary:	Primary library for %{name}
Group:		System/Libraries

%description -n %{liblinphone}
Primary library for %{name}.

%files -n %{liblinphone}
%{_libdir}/liblinphone.so.%{linphone_major}*

#--------------------------------------------------------------------

%package -n %{libmediastreamer_base}
Summary:	Media Streaming Base library for %{name}
Group:		System/Libraries

%description -n %{libmediastreamer_base}
Media Streaming library for %{name} - base part.

%files -n %{libmediastreamer_base}
%{_libdir}/libmediastreamer_base.so.%{mediastreamer_base_major}*

#--------------------------------------------------------------------

%package -n %{libmediastreamer_voip}
Summary:	Media Streaming VoIP library for %{name}
Group:		System/Libraries

%description -n %{libmediastreamer_voip}
Media Streaminglibrary for %{name} - VoIP part.

%files -n %{libmediastreamer_voip}
%{_libdir}/libmediastreamer_voip.so.%{mediastreamer_voip_major}*

#--------------------------------------------------------------------

%package -n %{devname}
Summary:	Header files and static libraries from %{name}
Group:		Development/C
Requires:	%{liblinphone} = %{version}-%{release}
Requires:	%{libmediastreamer_base} = %{version}-%{release}
Requires:	%{libmediastreamer_voip} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Libraries and includes files for developing programs based on %{name}.

%files -n %{devname}
%{_includedir}/linphone/
%{_includedir}/mediastreamer2/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/tutorials/%{name}

#--------------------------------------------------------------------

%prep
%setup -q
find '(' -name '*.c' -o -name '*.h' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'
%patch0 -p0 -b .image-dir
%patch1 -p1 -b .link

./autogen.sh

%build
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
%makeinstall_std

%find_lang %{name} --all-name --with-man

sed -i -e "s|linphone/linphone2\.png|linphone2|g" %{buildroot}%{_datadir}/applications/linphone.desktop
desktop-file-install \
	--vendor="" \
	--add-category="VideoConference" \
	--remove-category='Application' \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/linphone.desktop

#icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m 644 %{SOURCE4} \
	%{buildroot}%{_iconsdir}/hicolor/16x16/apps/linphone2.png
install -m 644 %{SOURCE3} \
	%{buildroot}%{_iconsdir}/hicolor/32x32/apps/linphone2.png
install -m 644 %{SOURCE2} \
	%{buildroot}%{_iconsdir}/hicolor/48x48/apps/linphone2.png
mkdir -p %{buildroot}/%{_miconsdir}
ln -s ../hicolor/16x16/apps/linphone2.png \
      %{buildroot}/%{_miconsdir}/
mkdir -p %{buildroot}/%{_iconsdir}
ln -s hicolor/32x32/apps/linphone2.png \
      %{buildroot}/%{_iconsdir}/
mkdir -p %{buildroot}/%{_liconsdir}
ln -s ../hicolor/48x48/apps/linphone2.png \
      %{buildroot}/%{_liconsdir}/

# remove unwanted docs, generated if doxygen is installed
rm -rf %{buildroot}%{_docdir}/ortp %{buildroot}%{_docdir}/mediastreamer* %{buildroot}%{_docdir}/%{name}*
