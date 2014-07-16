%if 0%{?fedora} > 12 || 0%{?rhel} >= 8
%global with_python3 1
%endif

%{!?__python2:%global __python2 %{__python}}
%{!?python2_sitelib:   %global python2_sitelib         %{python_sitelib}}
%{!?python2_sitearch:  %global python2_sitearch        %{python_sitearch}}
%{!?python2_version:   %global python2_version         %{python_version}}


%global pypi_name XStatic

Name:           python-%{pypi_name}
Version:        1.0.1
Release:        1%{?dist}
Summary:        XStatic base package with minimal support code

License:        MIT
URL:            http://bitbucket.org/thomaswaldmann/xstatic
Source0:        https://pypi.python.org/packages/source/X/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-setuptools


%description
The goal of XStatic family of packages is to provide static
file packages with minimal overhead - without selling you some 
dependencies you don't want.

XStatic has some minimal support code for working with the
XStatic-* packages.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:       XStatic base package with minimal support code
BuildRequires: python3-devel
BuildRequires: python3-setuptools
%description -n python3-%{pypi_name}

The goal of XStatic family of packages is to provide static
file packages with minimal overhead - without selling you some 
dependencies you don't want.

XStatic has some minimal support code for working with the
XStatic-* packages.


%endif

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%{__python2} setup.py build


%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3

%{__python2} setup.py install --skip-build --root %{buildroot}


%files
%doc README.txt
%{python2_sitelib}/xstatic
%{python2_sitelib}/XStatic-%{version}-py%{python2_version}.egg-info
%{python2_sitelib}/XStatic-%{version}-py%{python2_version}-nspkg.pth

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.txt
%{python3_sitelib}/xstatic
%{python3_sitelib}/XStatic-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/XStatic-%{version}-py%{python3_version}-nspkg.pth

%endif


%changelog
* Tue Jul 08 2014 Matthias Runge <mrunge@redhat.com> - 1.0.1-1
- Initial package.
