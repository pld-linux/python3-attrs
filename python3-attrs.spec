# Conditional build:
%bcond_with	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	attrs
Summary:	Writing classes without having to implement object protocols
Name:		python3-%{module}
Version:	25.3.0
Release:	2
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.debian.net/attrs/%{module}-%{version}.tar.gz
# Source0-md5:	173fe452e1fe986051d9bc194ed59525
URL:		https://www.attrs.org/
BuildRequires:	python3-build
BuildRequires:	python3-hatch_fancy_pypi_readme
BuildRequires:	python3-hatch_vcs
BuildRequires:	python3-hatchling
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.2
%if %{with tests}
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
# replace with other requires if defined in setup.py
Requires:	python3-modules >= 1:3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
attrs is the Python package that will bring back the joy of writing
classes by relieving you from the drudgery of implementing object
protocols (aka dunder methods).

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
rm -rf docs/_build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md  README.md
%{py3_sitescriptdir}/attr
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
