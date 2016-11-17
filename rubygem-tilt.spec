%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Fallback to rh-nodejs4 rh-nodejs4-scldevel is probably not available in
# the buildroot.
%{!?scl_nodejs:%global scl_nodejs rh-nodejs4}
%{!?scl_prefix_nodejs:%global scl_prefix_nodejs %{scl_nodejs}-}

%global gem_name tilt

# When we are bootstrapping, we drop some dependencies, and/or build time tests.
# Set this to 0 after we've bootstrapped.
%{!?_with_bootstrap: %global bootstrap 0}

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 2.0.1
Release: 3%{?dist}
Summary: Generic interface to multiple Ruby template engines
Group: Development/Languages
License: MIT
URL: http://github.com/rtomayko/%{gem_name}
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildRequires: %{?scl_prefix}rubygem(nokogiri)
BuildRequires: %{?scl_prefix}rubygem(erubis)
BuildRequires: %{?scl_prefix}rubygem(builder)
BuildRequires: %{?scl_prefix}rubygem(coffee-script)
BuildRequires: %{?scl_prefix}rubygem(sass)

# Optional (template engines)
#BuildRequires: %{?scl_prefix}rubygem(creole)
#BuildRequires: %{?scl_prefix}rubygem(maruku)
#BuildRequires: %{?scl_prefix}rubygem(RedCloth)
#BuildRequires: %{?scl_prefix}rubygem(redcarpet)
#BuildRequires: %{?scl_prefix}rubygem(wikicloth)
#BuildRequires: %{?scl_prefix}rubygem(kramdown)
#BuildRequires: %{?scl_prefix}rubygem(rdiscount)
#BuildRequires: %{?scl_prefix}rubygem(liquid)

# Asciidoctor fails: AsciidoctorTemplateTest#test_preparing_and_evaluating_docbook_templates_on_render
# BuildRequires: %{?scl_prefix}rubygem(asciidoctor)

# Markaby test fails. It is probably due to rather old version found in Fedora.
# https://github.com/rtomayko/tilt/issues/96
# BuildRequires: %{?scl_prefix}rubygem(markaby)

%if ! 0%{?bootstrap}
#BuildRequires: %{?scl_prefix}rubygem(haml)
%endif

BuildRequires: %{?scl_prefix_nodejs}nodejs

BuildArch:     noarch
Requires:      %{?scl_prefix}%{pkg_name} = %{version}-%{release}
Provides:      %{?scl_prefix}rubygem(%{gem_name}) = %{version}

# Explicitly require runtime subpackage, as long as older scl-utils do not generate it
Requires: %{?scl_prefix}runtime

%description
Generic interface to multiple Ruby template engines.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
%{?scl:scl enable %{scl} - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
%if 0%{bootstrap} < 1
pushd .%{gem_instdir}
# Get rid of Bundler.
sed -i '/[Bb]undler/ s/^/#/' test/test_helper.rb

%{?scl:scl enable %{scl} %{scl_nodejs} - << \EOF}
LANG=en_US.utf8 ruby -Ilib:test -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
%{?scl:EOF}
popd
%endif

%files
%dir %{gem_instdir}
%{_bindir}/%{gem_name}
%{gem_instdir}/COPYING
%exclude %{gem_instdir}/%{gem_name}.gemspec
%exclude %{gem_instdir}/.*
%exclude %{gem_instdir}/Gemfile
%{gem_instdir}/bin
%{gem_libdir}
%doc %{gem_instdir}/README.md
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/HACKING
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/docs
%{gem_instdir}/test

%changelog
* Thu Feb 25 2016 Pavel Valena <pvalena@redhat.com> - 2.0.1-3
- Update to 2.0.1

* Fri Jan 16 2015 Josef Stribny <jstribny@redhat.com> - 1.4.1-1
- Update to 1.4.1

* Fri Mar 21 2014 Vít Ondruch <vondruch@redhat.com> - 1.3.3-13
- Rebuid against new scl-utils to depend on -runtime package.
  Resolves: rhbz#1069109

* Thu Nov 28 2013 Josef Stribny <jstribny@redhat.com> - 1.3.3-12
- Get rid of patch leftovers

* Thu Jun 13 2013 Josef Stribny <jstribny@redhat.com> - 1.3.3-11
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Patch for RDoc 4.0

* Wed Jun 12 2013 Josef Stribny <jstribny@redhat.com> - 1.3.3-10
- Remove RDoc patch
  - Resolves: rhbz#969099

* Thu Apr 25 2013 Vít Ondruch <vondruch@redhat.com> - 1.3.3-9
- Fix unowned directory (rhbz#912046, rhbz#956236).

* Tue Jul 31 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.3-8
- Exclude the cached gem.

* Thu Jul 26 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.3-7
- Specfile cleanup

* Thu May 31 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.3-6
- Fix the rdoc test patch to apply cleanly.

* Thu Apr 26 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.3-5
- Fix the rdoc template tests.

* Mon Apr 02 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.3-4
- Rebuilt for scl.

* Fri Feb 03 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.3-3
- Allowed running the tests.

* Tue Jan 24 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.3-2
- Rebuilt for Ruby 1.9.3.
- Introduced %%bootstrap macro to deal with dependency loop for BuildRequires.

* Mon Jan 16 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.3-1
- Updated to tilt 1.3.3.
- Removed patch that fixed BZ #715713, as it is a part of this version.
- Excluded unnecessary files.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Vít Ondruch <vondruch@redhat.com> - 1.3.2-1
- Updated to the tilt 1.3.2.
- Test suite for erubis, haml, builder and RedCloth template engines enabled.

* Fri Jun 24 2011 Vít Ondruch <vondruch@redhat.com> - 1.2.2-3
- Fixes FTBFS (rhbz#715713).

* Thu Feb 10 2011 Vít Ondruch <vondruch@redhat.com> - 1.2.2-2
- Test moved to doc subpackage
- %{gem_name} macro used whenever possible.

* Mon Feb 07 2011 Vít Ondruch <vondruch@redhat.com> - 1.2.2-1
- Initial package

