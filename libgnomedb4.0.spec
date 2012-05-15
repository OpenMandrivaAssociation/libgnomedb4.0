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
Name:		%name
Version: 3.99.8
Release: %mkrel 0.%git.6
License:	GPLv2+ and LGPLv2+
Group: 		Databases
URL:		http://www.gnome-db.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{pkgname}/%{pkgname}-%git.tar.bz2
Patch1:		libgnomedb-fix-str-fmt.patch
Patch2:		libgnomedb-remove-duplicated-header.patch
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	libgnomeui2-devel
BuildRequires:	libgda4.0-devel >= %gdaver
BuildRequires:	scrollkeeper
BuildRequires:	gtk-doc
BuildRequires:	docbook-dtd412-xml
BuildRequires:	libglade2.0-devel
BuildRequires:	gtksourceview1-devel
BuildRequires:  evolution-data-server-devel
BuildRequires:	glade3-devel >= 3.1.5
BuildRequires:	libgoocanvas-devel >= 0.9
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
Group: 		System/Libraries
Requires: %name >= %version
#gw /usr/lib/glade3/modules/libgladegnomedb.so
Conflicts: gnome-db2.0 < 3.1.2-10

%description -n %{libname}
Gnome DB is a frontend to the GDA architecture, being developed as part
of the GNOME project. It adds, to the already powerful GDA architecture,
a nice GUI front end for users, as well as a whole set of software
components intended to be reused in other unrelated applications.


%package -n %{libnamedev}
Summary:	GNOME DB Development
Group: 		Development/Databases
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}
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
%configure2_5x
%make

%install
rm -rf %{buildroot}

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

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%{update_menus}
%post_install_gconf_schemas libgnomedb-%{api}
%endif

%preun
%preun_uninstall_gconf_schemas libgnomedb-%{api}

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%if %mdkversion < 200900
%post -n %{libnamedev}
%update_scrollkeeper
%endif

%if %mdkversion < 200900
%postun -n %{libnamedev}
%clean_scrollkeeper
%endif

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
							  
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif
							  
%files -f %{pkgname}-%api.lang
%defattr(-, root, root)
%doc AUTHORS COPYING NEWS
%_sysconfdir/gconf/schemas/libgnomedb-%{api}.schemas
%{_bindir}/*
%{_datadir}/pixmaps/*
%_libdir/glade3/modules/libgladegnomedb.so
%_datadir/glade3/
%dir %_datadir/gnome-db-%{api}/
%_datadir/gnome-db-%{api}/dtd
%_datadir/gnome-db-%{api}/*.xml
%_datadir/gnome-db-%{api}/*.glade
%_datadir/applications/database-properties-%{api}.desktop
%{_libdir}/libglade/2.0/*
%dir %{_libdir}/gnome-db-%{api}/
%{_libdir}/gnome-db-%{api}/plugins/

%files -n %{libname}
%defattr(-, root, root)
%{_libdir}/libgnomedb*-%{api}.so.%{major}*

%files -n %{libnamedev}
%defattr(-, root, root)
%doc %{_datadir}/gtk-doc/html/*
%{_libdir}/*.so
%attr(644,root,root) %{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/pkgconfig/*
%{_includedir}/*
%dir %{_datadir}/omf/*
%{_datadir}/omf/*/*-C.omf
%_datadir/gnome-db-%{api}/demo
