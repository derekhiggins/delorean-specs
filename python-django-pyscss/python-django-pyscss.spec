%{!?__python2:%global __python2 %{__python}}
%{!?python2_sitelib:   %global python2_sitelib         %{python_sitelib}}

%global pypi_name django-pyscss

Name:           python-%{pypi_name}
Version:        1.0.1
Release:        2%{?dist}
Summary:        Makes it easier to use PySCSS in Django

License:        BSD
URL:            https://github.com/fusionbox/django-pyscss
Source0:        https://github.com/fusionbox/django-pyscss/archive/v1.0.1.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pillow
BuildRequires:  python-django-compressor >= 1.3
BuildRequires:  python-django-discover-runner
BuildRequires:  python-scss >= 1.2.0
BuildRequires:  python-django
 
Requires:       python-django >= 1.4
Requires:       python-scss >= 1.2.0

%description
A collection of tools for making it easier to use
pyScss within Django.

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{__python2} setup.py build


%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%check
%{__python2} setup.py test


%files
%doc README.rst LICENSE
%{python2_sitelib}/django_pyscss
%{python2_sitelib}/django_pyscss-%{version}-py?.?.egg-info

%changelog
* Tue Jul 08 2014 Matthias Runge <mrunge@redhat.com> - 1.0.1-2
- add br python-setuptools

* Tue Jul 08 2014 Matthias Runge <mrunge@redhat.com> - 1.0.1-1
- Initial package.
