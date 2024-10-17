%define name          luaposix
%define soname        posix
%define version       5.1.23
%define major         1
%define release       2
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
URL:            https://www.tecgraf.puc-rio.br/~lhf/ftp/lua/
Source0:        https://github.com/downloads/luaposix/luaposix/%{name}-%{version}.tar.gz
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
BuildRequires:  pkgconfig(lua)

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
%setup -q

%build
export CFLAGS="%{optflags} -fPIC"
%configure2_5x --libdir=%{_libdir}/lua/%{lua_version}/%{name} \
		--docdir=%{_datadir}/doc/lua/%{lua_version}/%{name} \
		--datadir=%{_datadir}/doc/lua/%{lua_version}/%{name}
%make

%install
%makeinstall_std

%post -n %{libname_major}
cd %{_datadir}/lua/%{lua_version} && rm -f %{soname}.lua && ln default.lua %{soname}.lua

%postun -n %{libname_major}
if [ "$1" = "0" ]; then
  rm -f %{_datadir}/lua/%{lua_version}/%{soname}.lua
fi

%files -n %{libname_major}
%{_libdir}/lua/%{lua_version}/%{name}/*.so
%{_defaultdocdir}/lua/%{lua_version}/*

%files -n %{develname}
#%{_libdir}/lua/%{lua_version}/*.so
#%{_libdir}/lua/%{lua_version}/*.a
