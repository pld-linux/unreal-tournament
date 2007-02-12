# TODO
# - all
# - use datadir
# - use system libs
Summary:	Futuristic FPS
Summary(pl.UTF-8):   Futurystyczna gra FPS
Name:		unreal-tournament
Version:	451
Release:	0.1
License:	as-is
Group:		Applications/Games
Source0:	ftp://ftp.lokigames.com/pub/patches/ut/ut-install-436.run
# Source0-md5:	b2fb7006ba2420665916739b7d9f7885
Source1:	http://utpg.org/patches/UTPGPatch%{version}.tar.bz2
# Source1-md5:	77a735a78b1eb819042338859900b83b
URL:		http://www.unrealtournament.com/
#URL:		http://utpg.org/
Requires:	OpenGL
Requires:	SDL
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		_noautoreq		Core.so Editor.so Engine.so Render.so
%define		__syslibs		libSDL-1.1.so.0 libmikmod.so.2 libopenal-0.0.so
%define		_noautoprov		%{__syslibs} %{_noautoreq} ALAudio.so Audio.so Fire.so GlideDrv.so IpDrv.so NullNetDriver.so NullRender.so OpenGLDrv.so SDLDrv.so SDLGLDrv.so SDLSoftDrv.so UWeb.so
%define		_gamelibdir		%{_libdir}/games/%{name}
%define		_gamedatadir	%{_datadir}/games/%{name}

%description
Unreal Tournament - futuristic FPS game.

%description -l pl.UTF-8
Unreal Tournament - futurystyczna gra FPS.

%prep
%setup -qcT
skip=$(grep -a ^skip= %{SOURCE0} | cut -d= -f2)
tail -n +${skip} %{SOURCE0} | tar -zx
mkdir UTPG
tar -C UTPG -xf %{SOURCE1}
rm -f UTPG/{checkfiles.sh,patch.md5}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_gamedatadir},%{_gamelibdir}} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir},%{_bindir}}

tar -zxf Credits.tar.gz -C $RPM_BUILD_ROOT%{_gamelibdir}
# NetGamesUSA.com
tar -zxf NetGamesUSA.com.tar.gz -C $RPM_BUILD_ROOT%{_gamelibdir}

# System
%if %{with 3dfx}
	tar -zxf Glide.ini.tar.gz -C $RPM_BUILD_ROOT%{_gamelibdir}
%else
	tar -zxf OpenGL.ini.tar.gz -C $RPM_BUILD_ROOT%{_gamelibdir}
%endif
tar -zxf data.tar.gz -C $RPM_BUILD_ROOT%{_gamelibdir}

# the most important things, ucc & ut :)
install bin/x86/{ucc,ut} $RPM_BUILD_ROOT%{_gamelibdir}

# install a few random files
install README icon.{bmp,xpm} $RPM_BUILD_ROOT%{_gamelibdir}

# install a menu item (closes bug #27542)
install icon.xpm $RPM_BUILD_ROOT%{_pixmapsdir}/ut.xpm

# finally, unleash the UTPG patch
cp -rf UTPG/* $RPM_BUILD_ROOT%{_gamelibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_pixmapsdir}/ut.xpm

%dir %{_gamelibdir}
%{_gamelibdir}/Web
%{_gamelibdir}/Textures
%{_gamelibdir}/NetGamesUSA.com
%{_gamelibdir}/Help
%{_gamelibdir}/System
%{_gamelibdir}/README
%{_gamelibdir}/checkfiles.sh
%{_gamelibdir}/icon.bmp
%{_gamelibdir}/icon.xpm
%{_gamelibdir}/patch.md5
%{_gamelibdir}/ucc
%{_gamelibdir}/ut

%dir %{_gamedatadir}
