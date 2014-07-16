%if 0%{?fedora} > 12 || 0%{?rhel} >= 8
%global with_python3 1
%endif

%{!?__python2:%global __python2 %{__python}}
%{!?python2_sitelib:   %global python2_sitelib         %{python_sitelib}}
%{!?python2_sitearch:  %global python2_sitearch        %{python_sitearch}}
%{!?python2_version:   %global python2_version         %{python_version}}


%global pypi_name XStatic-jQuery

Name:           python-%{pypi_name}
Version:        1.10.2.1
Release:        1%{?dist}
Summary:        jQuery 1.10.2 (XStatic packaging standard)

License:        MIT
URL:            http://jquery.com/
Source0:        https://pypi.python.org/packages/source/X/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-XStatic


%description
jQuery javascript library packaged for
setuptools (easy_install) / pip.

This package is intended to be used by
**any** project that needs these files.

It intentionally does **not** provide
any extra code except some metadata
**nor** has any extra requirements. You MAY
use some minimal support code from
the XStatic base package, if you like.

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info



%build
%{__python} setup.py build


%install
%{__python} setup.py install --skip-build --root %{buildroot}


%files
%doc README.txt
%{python_sitelib}/XStatic_jQuery-%{version}-py?.?.egg-info
%{python_sitelib}/XStatic_jQuery-%{version}-py?.?-nspkg.pth
%{python_sitelib}/xstatic/pkg/jquery

%changelog
* Wed Mar 12 2014 Matthias Runge <mrunge@redhat.com> - 1.10.2.1-1
- Initial package.
