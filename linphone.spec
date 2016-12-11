%define oname Linphone
%define lname %(echo %oname | tr [:upper:] [:lower:])

%define major 9
%define devname %mklibname %{name} -d
%define libname %mklibname %{name} %{major}

%define majortester 0
%define nametester %{name}_tester
%define devnametester %mklibname %{name}tester -d
%define libnametester %mklibname %{name}tester %{majortester}

Summary:	Voice over IP Application
Name:		%{lname}
Version:	3.10.2
Release:	0
License:	GPLv2+
Group:		Communications
Url:		https://www.linphone.org/
#Source0:	https://github.com/BelledonneCommunications/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Source0:	http://download.savannah.gnu.org/releases/%{name}/stable/sources/%{name}-%{version}.tar.gz
Source1:	http://download.savannah.gnu.org/releases/%{name}/stable/sources/%{name}-%{version}.tar.gz.sig
Patch0:		%{name}-3.10.2-daemon_cmake.patch
Patch1:		%{name}-3.10.2-bctoolbox.patch

BuildRequires:	cmake
BuildRequires:	cmake(BcToolbox)
BuildRequires:	cmake(Belcard)
BuildRequires:	cmake(BelleSIP) >= 0.24.0
BuildRequires:	cmake(Mediastreamer2)
BuildRequires:	cmake(ORTP)
BuildRequires:  imagemagick
# http://lists.gnu.org/archive/html/linphone-developers/2013-04/msg00016.html
BuildRequires:	vim-common
BuildRequires:	pkgconfig(atk)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(gdk-x11-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(zlib)

Suggests:	%{_lib}x265_95

%description
Linphone is a free VoIP and video softphone based on the SIP protocol.

%files -f %{name}.lang
%doc COPYING README AUTHORS BUGS ChangeLog
#doc %{_datadir}/gnome/help/%{name}
%{_bindir}/%{name}*
%{_bindir}/lp-auto-answer
%{_bindir}/lp-gen-wrappers
%{_bindir}/lp-sendmsg
#{_bindir}/lpc2xml_test
#{_bindir}/xml2lpc_test
#{_mandir}/man1/*
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/pixmaps/%{name}/
%{_datadir}/sounds/%{name}/
%{_datadir}/applications/*
%{_iconsdir}/hicolor/*/*/linphone*.*
%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/%{name}/

#--------------------------------------------------------------------

%package -n %{libname}
Summary:	Primary library for %{name}
Group:		System/Libraries

%description -n %{libname}
Primary library for %{name}.

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

#--------------------------------------------------------------------

%package -n %{libnametester}
Summary: Tester library for %{name}
Group:   System/Libraries

%description -n %{libnametester}
Tester library for %{name}.

%files -n %{libnametester}
%{_bindir}/lib%{nametester}*
#{_libdir}/lib%{nametester}.so.%{majortester}*
%{_datadir}/lib%{nametester}/

#--------------------------------------------------------------------

%package -n %{devname}
Summary: Header files and static libraries from %{name}
Group:   Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libnametester} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Libraries and includes files for developing programs based on %{name}.

%files -n %{devname}
%{_includedir}/linphone/
%{_libdir}/lib%{name}.so
#%{_libdir}/lib%{nametester}.so
#%{_libdir}/pkgconfig/*.pc
%{_datadir}/%{oname}/cmake/
#%{_datadir}/tutorials/%{name}
%{_docdir}/%{_lib}%{name}-%{version}

#--------------------------------------------------------------------

%prep
%setup -q

# Apply all patches
%patch0 -p1 -b .orig
%patch1 -p1 -b .orig

# Remove embedded libs
rm -fr mediastreamer2
rm -fr oRTP

# Fix file-not-utf8 warning
for f in ChangeLog
do
  iconv -f iso8859-1 -t utf8 ${f} > ${f}.tmp
  touch -r ${f} ${f}.tmp
  mv -f ${f}.tmp ${f}
done

%build
%cmake \
	-DCMAKE_BUILD_TYPE:STRING=Debug \
	-DENABLE_SHARED:BOOL=ON \
	-DENABLE_STATIC:BOOL=OFF \
	-DENABLE_LDAP:BOOL=ON \
	-DENABLE_LIME:BOOL=ON \
	-DENABLE_TUNNEL:BOOL=OFF \
	-DENABLE_STRICT:BOOL=OFF \
	-DENABLE_TUTORIAL:BOOL=ON \
	-DENABLE_TESTS:BOOL=ON \
	%{nil}
%make

%install
%makeinstall_std -C build

desktop-file-edit \
	--add-category="VideoConference" \
	%{buildroot}%{_datadir}/applications/linphone.desktop

#icons
for d in 16 32 64 #48
do
install -dm 0755 %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps
convert -scale ${d}x${d} pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{name}.png
done

install -dm 0755 %{buildroot}/%{_miconsdir}/
ln -s ../hicolor/16x16/apps/%{name}.png %{buildroot}/%{_miconsdir}/
install -dm 0755 %{buildroot}/%{_iconsdir}/
ln -s ../hicolor/32x32/apps/%{name}.png %{buildroot}/%{_iconsdir}/
install -dm 0755 %{buildroot}/%{_liconsdir}/
ln -s ../hicolor/48x48/apps/%{name}.png %{buildroot}/%{_liconsdir}/

# appdata
install -dm 0755 %{buildroot}%{_datadir}/appdata/
install -pm 0644 share/appdata/%{name}.appdata.xml %{buildroot}%{_datadir}/appdata/

# move docs generated by doxygen
mv %{buildroot}%{_docdir}/%{name}-%{version} \
   %{buildroot}%{_docdir}/%{_lib}%{name}-%{version}

# localization
%find_lang %{name} --all-name --with-man

