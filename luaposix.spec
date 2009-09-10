%define name          luaposix
%define soname        posix
%define version       1.0
%define major         1
%define release       %mkrel 5
%define libname       %mklibname %{soname} %{major}
%define libname_major %mklibname %{name} %{major}
%define libname_orig  %mklibname %{name}
%define develname     %mklibname %{name} -d
%define lua_version   5.1

Summary:        A POSIX library for the Lua programming language
Name:           %name
Version:        %version
Release:        %release
License:        Public Domain
Group:          Development/Other
URL:            http://www.tecgraf.puc-rio.br/~lhf/ftp/lua/
Source0:        lposix.tar.bz2
Patch0:         %{name}.patch
Patch1:		lposix-build-5.1.patch
BuildRoot:      %_tmppath/%{name}-buildroot
Obsoletes:      %{libname} = %{version}
Obsoletes:      %{libname_orig}
Provides:       %{libname} = %{version}
Provides:       %{libname_orig}

%description
A POSIX library for the Lua programming language.

%package -n     %{libname_major}
Summary:        A POSIX library for the Lua programming language
Group:          Development/Other
Obsoletes:      %{libname_orig}
Provides:       %{libname_orig}
Requires:       liblua%{lua_version}
BuildRequires:  liblua-devel

%description -n %{libname_major}
A POSIX library for the Lua programming language.

%package -n     %{develname}
Summary:        Static library and header files for the luaposix library
Group:          Development/Other
License:        Public Domain
Requires:       %{libname_major} = %{version}
Obsoletes:	%{libname_major}-devel

%description -n %{develname}
A POSIX library for the Lua programming language.

This package contains the static libluaposix library and its header files
needed to compile applications that use luaposix.

%prep
%setup -q -n %{soname}
%patch0 -p1
%patch1 -p0

%build
export CFLAGS="%{optflags} -fPIC"
%make

%install
strip %{soname}.so
%__rm -rf %{buildroot}
install -d %{buildroot}/%{_libdir}/lua/%{lua_version}
install -d %{buildroot}/%{_datadir}/lua/%{lua_version}
install -d %{buildroot}/%{_defaultdocdir}/lua/%{lua_version}/%{name}
install -m0755 %{soname}.so %{buildroot}%{_libdir}/lua/%{lua_version}
install -m0644 %{soname}.a %{buildroot}/%{_libdir}/lua/%{lua_version}
install -m0644 README %{buildroot}%{_defaultdocdir}/lua/%{lua_version}

%post -n %{libname_major}
cd %{_datadir}/lua/%{lua_version} && rm -f %{soname}.lua && ln default.lua %{soname}.lua

%postun -n %{libname_major}
if [ "$1" = "0" ]; then
  rm -f %{_datadir}/lua/%{lua_version}/%{soname}.lua
fi

%clean
%__rm -rf %{buildroot}

%files -n %{libname_major}
%defattr(-,root,root)
%{_libdir}/lua/%{lua_version}/*.so
%{_defaultdocdir}/lua/%{lua_version}/*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/lua/%{lua_version}/*.so
%{_libdir}/lua/%{lua_version}/*.a
