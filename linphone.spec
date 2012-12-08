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


%changelog
* Fri Jun 08 2012 Bernhard Rosenkraenzer <bero@bero.eu> 3.5.2-1
+ Revision: 803507
- Port to ffmpeg 0.11
- Update to 3.5.2

* Fri Feb 24 2012 Oden Eriksson <oeriksson@mandriva.com> 3.5.0-2
+ Revision: 780090
- rebuilt against libvpx.so.1

* Wed Feb 01 2012 Andrey Bondrov <abondrov@mandriva.org> 3.5.0-1
+ Revision: 770444
- New version 3.5.0. Update BuildRequires, find_lang usage, file list

* Sun Oct 23 2011 ZÃ© <ze@mandriva.org> 3.4.3-3
+ Revision: 705737
- clean defattr
- remove clean section
- remove buildroot
- small arrangements
- rebuild due to new osip2

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 3.4.3-2
+ Revision: 661687
- multiarch fixes

* Sun Apr 03 2011 Funda Wang <fwang@mandriva.org> 3.4.3-1
+ Revision: 649994
- new version 3.4.3

* Fri Apr 01 2011 Funda Wang <fwang@mandriva.org> 3.3.2-3
+ Revision: 649733
- only build libv4l2 interface

* Fri Dec 17 2010 Funda Wang <fwang@mandriva.org> 3.3.2-2mdv2011.0
+ Revision: 622478
- rebuild for new directfb

* Fri Aug 06 2010 Ahmad Samir <ahmadsamir@mandriva.org> 3.3.2-1mdv2011.0
+ Revision: 566544
- update to 3.3.2
- drop patch1,2 not needed any more (Fedora)
- drop patch5, package compiles without it
- bump some BR versions
- add BR libv4l-devel
- improve configure options
- delete .la files
- update file list
- remove 'mdkversion < 200900' bits, too old

* Wed Apr 07 2010 Ahmad Samir <ahmadsamir@mandriva.org> 3.2.1-3mdv2010.1
+ Revision: 532827
- rebuild for openssl-1.0.0

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 3.2.1-2mdv2010.1
+ Revision: 511590
- rebuilt against openssl-0.9.8m

* Mon Nov 09 2009 Funda Wang <fwang@mandriva.org> 3.2.1-1mdv2010.1
+ Revision: 463377
- New version 3.2.1

* Sun Nov 08 2009 Funda Wang <fwang@mandriva.org> 3.2.0-2mdv2010.1
+ Revision: 463085
- rebuild for new dfb

* Sun Sep 20 2009 Funda Wang <fwang@mandriva.org> 3.2.0-1mdv2010.0
+ Revision: 444882
- New version 3.2.0

* Tue May 05 2009 Funda Wang <fwang@mandriva.org> 3.1.2-1mdv2010.0
+ Revision: 372141
- New version 3.1.2

* Thu Mar 12 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.0.0-4mdv2009.1
+ Revision: 354275
- drop previous hack, invalid syntax
- fix build dependencies to use ortp from external package, instead of the one from previous linphone release
- rebuild for latest realine

  + Emmanuel Andry <eandry@mandriva.org>
    - diff P4 and P6 from upstream svn to fix build
    - diff P5 to fix str fmt
    - diff P7 to fix ortp linking
    - rediff P0
    - use external ortp
    - enable ipv6

* Sun Nov 09 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0.0-2mdv2009.1
+ Revision: 301476
- rebuilt against new libxcb

* Mon Oct 20 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0.0-1mdv2009.1
+ Revision: 295692
- 3.0.0
- drop P3, better ffmpeg header fix upstream
- fix weird intltoolize error (P3)
- fix deps

* Sat Jun 28 2008 Oden Eriksson <oeriksson@mandriva.com> 2.1.1-2mdv2009.0
+ Revision: 229665
- fix deps

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed May 28 2008 Funda Wang <fwang@mandriva.org> 2.1.1-1mdv2009.0
+ Revision: 212680
- BR intltool
- New version 2.1.1
- add patch from fedora
- add patch for new ffmpeg header locations

* Fri Feb 22 2008 Colin Guthrie <cguthrie@mandriva.org> 2.1.0-2mdv2008.1
+ Revision: 173794
- Fix libification

* Fri Feb 01 2008 Austin Acton <austin@mandriva.org> 2.1.0-1mdv2008.1
+ Revision: 160987
- new version
- configure 2.5

  + Colin Guthrie <cguthrie@mandriva.org>
    - Add libeXosip2 to BuildRequires
    - Undo BuildRequire "fix" that was incorrect.
    - Fix build requires (libosip2-devel not libosip-devel)
    - Comply with new library policy
    - Remove old patches
    - Fix .desktop icon extension
    - Upgrade to 2.0.1 (for libosip2-3.x)

  + Thierry Vignaud <tv@mandriva.org>
    - fix libosip-devel BR, reverting bogus change
    - rebuild
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Thu Jul 26 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.7.1-4mdv2008.0
+ Revision: 56018
- Replaced docbook-utils buildrequire with gtk-doc.

* Wed Jul 25 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.7.1-3mdv2008.0
+ Revision: 55490
- Added missing BuildRequires for docbook-utils.

* Tue Jul 24 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.7.1-2mdv2008.0
+ Revision: 55044
- Fixes for ticket #27731:
  * help contents aren't shown when you click on help menu.
  * possibly missing icons, added compatibility symlinks for some icon
    directories.

* Wed Jun 13 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.7.1-1mdv2008.0
+ Revision: 38894
- Added BuildRequires for desktop-file-utils.
- Removed some now uneeded BuildRequires.
- Build fixes.
- Updated to version 1.7.1.
- Removed old menu, switch to freedesktop icon scheme.

* Mon May 07 2007 Lenny Cartier <lenny@mandriva.org> 1.6.0-3mdv2008.0
+ Revision: 24006
- Fix xdg
- Fix menu section (Bug #15268)


* Thu Jan 25 2007 Lenny Cartier <lenny@mandriva.com> 1.6.0-1mdv2007.0
+ Revision: 113350
- Update to 1.6.0

* Fri Dec 22 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 1.5.1-1mdv2007.1
+ Revision: 101492
- 1.5.1
- patch0: fix a compilation warning on ppc

* Tue Oct 31 2006 Stefan van der Eijk <stefan@mandriva.org> 1.5.0-1mdv2007.1
+ Revision: 74402
- 1.5.0
- Import linphone

* Thu Mar 09 2006 Austin Acton <austin@mandriva.org> 1.3.0-1mdk
- New release 1.3.0

* Tue Feb 14 2006 Oden Eriksson <oeriksson@mandriva.com> 1.2.0-2mdk
- mutliarch fixes

* Mon Feb 13 2006 Oden Eriksson <oeriksson@mandriva.com> 1.2.0-1mdk
- 1.2.0
- fix deps

* Tue Jan 31 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 1.1.0-5mdk
- add BuildRequires: docbook-dtd30-sgml

* Fri Jan 27 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 1.1.0-4mdk
- add BuildRequires: libspeex-devel docbook-dtd41-sgml

* Wed Nov 30 2005 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-3mdk
- rebuilt against openssl-0.9.8a
- added some lib64 fixes

* Thu Sep 01 2005 Austin Acton <austin@mandriva.org> 1.1.0-2mdk
- fix menu

* Fri Aug 26 2005 Austin Acton <austin@mandriva.org> 1.1.0-1mdk
- 1.1.0
- fix source URL

* Thu Jul 21 2005 Nicolas Lécureuil <neoclust@mandriva.org> 1.0.1-1mdk
- New release 1.0.1

* Tue Mar 22 2005 Frederic Lepied <flepied@mandrakesoft.com> 1.0.0-1mdk
- final 1.0.0

* Mon Feb 14 2005 Austin Acton <austin@mandrake.org> 1.0.0-0.pre8.2mdk
- fix botched upload

* Thu Feb 10 2005 Austin Acton <austin@mandrake.org> 1.0.0-0.pre8.1mdk
- 1.0.0pre8
- add libs
- configure 2.5

* Thu Jul 15 2004 Michael Reinsch <mr@uue.org> 0.12.2-3mdk
- rebuild again for fixed alsa which broke broken alsa

* Tue Jun 22 2004 Michael Reinsch <mr@uue.org> 0.12.2-2mdk
- rebuild for new alsa

* Sat Apr 24 2004 Stefan van der Eijk <stefan@eijk.nu> 0.12.2-1mdk
- 0.12.2
- BuildRequires perl-XML-Parser (temp)

* Fri Feb 20 2004 David Baudens <baudens@mandrakesoft.com> 0.12.1-2mdk
- Fix menu

* Mon Feb 16 2004 Austin Acton <austin@mandrake.org> 0.12.1-1mdk
- 0.12.1
- fix buildrequires

