%define pkgname	libgnomedb
%define api 4.0
%define name	%{pkgname}%{api}
%define	major	4
%define oname gnomedb
%define libname	%mklibname %{oname}%{api}_ %major 
%define libnamedev %mklibname -d %{oname}%{api}
%define gdaver 3.99.7
%define git 20090503

Summary:	GNOME DB
Name:		%{pkgname}%{api}
Version:	3.99.8
Release:	0.%git.8
License:	GPLv2+ and LGPLv2+
Group: 		Databases
URL:		http://www.gnome-db.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{pkgname}/%{pkgname}-%git.tar.bz2
Patch1:		libgnomedb-fix-str-fmt.patch
Patch2:		libgnomedb-remove-duplicated-header.patch
BuildRequires:	pkgconfig(libgnomeui-2.0)
BuildRequires:	pkgconfig(libgda-4.0)
BuildRequires:	scrollkeeper
BuildRequires:	gtk-doc
BuildRequires:	docbook-dtd412-xml
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(gtksourceview-1.0)
BuildRequires:  pkgconfig(evolution-data-server-1.2)
BuildRequires:	pkgconfig(gladeui-1.0)
BuildRequires:	pkgconfig(goocanvas)
BuildRequires:	graphviz-devel
BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  gnome-common

%description
Gnome DB is a frontend to the GDA architecture, being developed as part
of the GNOME project. It adds, to the already powerful GDA architecture,
a nice GUI front end for users, as well as a whole set of software
components intended to be reused in other unrelated applications.

This package contains the core components of GNOME-DB.

%package -n %{libname}
Summary:	GNOME DB libraries
Group:		System/Libraries
Requires:	%{name} >= %{version}
#gw /usr/lib/glade3/modules/libgladegnomedb.so
Conflicts:	gnome-db2.0 < 3.1.2-10

%description -n %{libname}
Gnome DB is a frontend to the GDA architecture, being developed as part
of the GNOME project. It adds, to the already powerful GDA architecture,
a nice GUI front end for users, as well as a whole set of software
components intended to be reused in other unrelated applications.

%package -n %{libnamedev}
Summary:	GNOME DB Development
Group: 		Development/Databases
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires(post):		scrollkeeper
Requires(postun):		scrollkeeper

%description -n %{libnamedev}
Gnome DB is a frontend to the GDA architecture, being developed as part
of the GNOME project. It adds, to the already powerful GDA architecture,
a nice GUI front end for users, as well as a whole set of software
components intended to be reused in other unrelated applications.

This package contains libraries, header files and tools to let
you develop GNOME-DB applications.


%prep
%setup -q -n %{pkgname}
%patch1 -p1 -b .str
%patch2 -p1
./autogen.sh

%build
%configure2_5x --disable-static
%make LIBS="-lgmodule-2.0"

%install
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

desktop-file-install --vendor="" \
  --add-category="GNOME" \
  --add-category="GTK" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%{find_lang} %{pkgname}-%api --with-gnome

# remove unpackaged files
rm -rf %{buildroot}%{_libdir}/libglade/2.0/*.{la,a} \
       %{buildroot}%{_libdir}/glade3/modules/*a \
       %{buildroot}%{_libdir}/libgnomedb/plugins/*a

%preun
%preun_uninstall_gconf_schemas libgnomedb-%{api}

%files -f %{pkgname}-%{api}.lang
%doc AUTHORS COPYING NEWS
%{_sysconfdir}/gconf/schemas/libgnomedb-%{api}.schemas
%{_bindir}/*
%{_datadir}/pixmaps/*
%{_libdir}/glade3/modules/libgladegnomedb.so
%{_datadir}/glade3/
%dir %{_datadir}/gnome-db-%{api}/
%{_datadir}/gnome-db-%{api}/dtd
%{_datadir}/gnome-db-%{api}/*.xml
%{_datadir}/gnome-db-%{api}/*.glade
%{_datadir}/applications/database-properties-%{api}.desktop
%{_libdir}/libglade/2.0/*
%dir %{_libdir}/gnome-db-%{api}/
%{_libdir}/gnome-db-%{api}/plugins/

%files -n %{libname}
%{_libdir}/libgnomedb*-%{api}.so.%{major}*

%files -n %{libnamedev}
%doc %{_datadir}/gtk-doc/html/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%dir %{_datadir}/omf/*
%{_datadir}/omf/*/*-C.omf
%{_datadir}/gnome-db-%{api}/demo


%changelog
* Wed May 11 2011 Funda Wang <fwang@mandriva.org> 3.99.8-0.20090503.5mdv2011.0
+ Revision: 673598
- rebuild for new graphviz

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 3.99.8-0.20090503.4
+ Revision: 661468
- mass rebuild

* Fri Dec 17 2010 Götz Waschk <waschk@mandriva.org> 3.99.8-0.20090503.3mdv2011.0
+ Revision: 622593
- rebuild for new libgladeui

* Fri Aug 06 2010 Götz Waschk <waschk@mandriva.org> 3.99.8-0.20090503.2mdv2011.0
+ Revision: 566638
- rebuild for new glade3

* Mon Sep 07 2009 Götz Waschk <waschk@mandriva.org> 3.99.8-0.20090503.1mdv2010.1
+ Revision: 432637
- fix conflict
- add conflict with gnome-dv2.0

* Thu Sep 03 2009 Götz Waschk <waschk@mandriva.org> 3.99.8-0.20090503.1mdv2010.0
+ Revision: 428369
- update build deps
- new snapshot
- update patch 1
- fix installation
- update file list

* Wed Dec 31 2008 Götz Waschk <waschk@mandriva.org> 3.99.7-1mdv2009.1
+ Revision: 321678
- new version
- bump gda dep

* Fri Dec 19 2008 Funda Wang <fwang@mandriva.org> 3.99.6-2mdv2009.1
+ Revision: 316062
- fix str fmt

* Wed Nov 26 2008 Götz Waschk <waschk@mandriva.org> 3.99.6-1mdv2009.1
+ Revision: 306984
- fix build deps
- new version
- new api
- cleanup spec
- import 3.0 branch

* Mon Nov 10 2008 Funda Wang <fwang@mandriva.org> 3.1.2-6mdv2009.1
+ Revision: 301673
- rebuild for new xcb

* Wed Aug 06 2008 Götz Waschk <waschk@mandriva.org> 3.1.2-5mdv2009.0
+ Revision: 264248
- update license

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed May 28 2008 Frederic Crozat <fcrozat@mandriva.com> 3.1.2-3mdv2009.0
+ Revision: 212605
- Patch0: fix underlinking

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 3.1.2-2mdv2008.1
+ Revision: 148505
- rebuild
- kill re-definition of %%buildroot on Pixel's request
- do not package big ChangeLog

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Oct 26 2007 Götz Waschk <waschk@mandriva.org> 3.1.2-1mdv2008.1
+ Revision: 102294
- bump deps
- new version

* Tue Sep 11 2007 Frederic Crozat <fcrozat@mandriva.com> 3.1.1-3mdv2008.0
+ Revision: 84391
- Fix categories in .desktop to only appear in Settings
- Fix missing icon for .desktop

* Fri Sep 07 2007 Götz Waschk <waschk@mandriva.org> 3.1.1-2mdv2008.0
+ Revision: 81440
- add dep on the main package to the library package

* Sun Sep 02 2007 Götz Waschk <waschk@mandriva.org> 3.1.1-1mdv2008.0
+ Revision: 78335
- new version
- bump gda dep
- depend on graphviz and goocanvas
- new devel name
- update file list

* Tue Jul 24 2007 Götz Waschk <waschk@mandriva.org> 3.0.0-3mdv2008.0
+ Revision: 54945
- fix buildrequires

* Fri Jun 08 2007 Götz Waschk <waschk@mandriva.org> 3.0.0-2mdv2008.0
+ Revision: 37254
- rebuild

* Tue Apr 24 2007 Götz Waschk <waschk@mandriva.org> 3.0.0-1mdv2008.0
+ Revision: 17771
- new version

* Wed Apr 18 2007 Götz Waschk <waschk@mandriva.org> 2.99.6-1mdv2008.0
+ Revision: 14654
- new version
- drop sharp binding
- bump deps
- new api version

