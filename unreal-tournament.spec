#
# Conditional build:
%bcond_with	3dfx		# prefer Glide over OpenGL in config
# TODO
# - all
# - use datadir
# - use system libs
Summary:	Futuristic FPS
Summary(pl.UTF-8):	Futurystyczna gra FPS
Name:		unreal-tournament
Version:	451
Release:	0.2
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

%define		_noautoreq		Core.so Editor.so Engine.so Render.so libopenal-0.0.so libglide.so.2
%define		__syslibs		libSDL-1.1.so.0 libmikmod.so.2
%define		_noautoprov		%{__syslibs} %{_noautoreq} ALAudio.so Audio.so Fire.so GlideDrv.so IpDrv.so NullNetDriver.so NullRender.so OpenGLDrv.so SDLDrv.so SDLGLDrv.so SDLSoftDrv.so UWeb.so
%define		_enable_debug_packages	0
%define		skip_post_check_so	libSDL-1.1.so.0

%define		gamelibdir		%{_libdir}/games/%{name}
%define		gamedatadir		%{_datadir}/games/%{name}

%description
Unreal Tournament - futuristic FPS game.

%description -l pl.UTF-8
Unreal Tournament - futurystyczna gra FPS.

%prep
%setup -qcT
skip=$(grep -a ^skip= %{SOURCE0} | cut -d= -f2)
tail -n +$skip %{SOURCE0} | tar -zx
install -d UTPG lib
tar -C UTPG -xf %{SOURCE1}
rm -f UTPG/{checkfiles.sh,patch.md5}

tar -zxf Credits.tar.gz -C lib
# NetGamesUSA.com
tar -zxf NetGamesUSA.com.tar.gz -C lib

# System
%if %{with 3dfx}
tar -zxf Glide.ini.tar.gz -C lib
%else
tar -zxf OpenGL.ini.tar.gz -C lib
%endif
tar -zxf data.tar.gz -C lib

# not really needed to execute
chmod a-x lib/NetGamesUSA.com/ngStats/spawnBrowser.exe

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{gamedatadir},%{gamelibdir}} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir},%{_bindir}}

cp -a lib/* $RPM_BUILD_ROOT%{gamelibdir}

# the most important things, ucc & ut :)
install -p bin/x86/{ucc,ut} $RPM_BUILD_ROOT%{gamelibdir}

# install a few random files
cp -p README icon.{bmp,xpm} $RPM_BUILD_ROOT%{gamelibdir}

# install a menu item (closes bug #27542)
cp -p icon.xpm $RPM_BUILD_ROOT%{_pixmapsdir}/ut.xpm

# finally, unleash the UTPG patch
cp -a UTPG/* $RPM_BUILD_ROOT%{gamelibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_pixmapsdir}/ut.xpm

%dir %{gamelibdir}
%{gamelibdir}/Web
%{gamelibdir}/Textures
%{gamelibdir}/NetGamesUSA.com
%{gamelibdir}/Help
%{gamelibdir}/System
%{gamelibdir}/README
%{gamelibdir}/icon.bmp
%{gamelibdir}/icon.xpm
%{gamelibdir}/ucc
%{gamelibdir}/ut

%dir %{gamedatadir}
