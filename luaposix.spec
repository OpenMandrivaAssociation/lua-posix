%define name          luaposix
%define soname        posix
%define version       1.0
%define major         1
%define release       %mkrel 2
%define libname       %mklibname %{soname} %{major}
%define libname_major %mklibname %{name} %{major}
%define libname_orig  %mklibname %{name}
%define lua_version   5.0

Summary:        A POSIX library for the Lua programming language
Name:           %name
Version:        %version
Release:        %release
License:        Public Domain
Group:          Development/Other
URL:            http://www.tecgraf.puc-rio.br/~lhf/ftp/lua/
Source0:        lposix.tar.bz2
Patch0:         %{name}.patch.bz2
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
Requires:       liblua5
BuildRequires:  liblua-devel

%description -n %{libname_major}
A POSIX library for the Lua programming language.

%package -n     %{libname_major}-devel
Summary:        Static library and header files for the luaposix library
Group:          Development/Other
License:        Public Domain
Obsoletes:      %{libname_orig}-devel
Provides:       %{libname_orig}-devel
Requires:       %{libname_major} = %{version}

%description -n %{libname_major}-devel
A POSIX library for the Lua programming language.

This package contains the static libluaposix library and its header files
needed to compile applications that use luaposix.

%prep
%setup -q -n %{soname}
%patch -p1

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

%files -n %{libname_major}-devel
%defattr(-,root,root)
%{_libdir}/lua/%{lua_version}/*.so
%{_libdir}/lua/%{lua_version}/*.a
