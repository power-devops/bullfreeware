# Sensible Perl-specific RPM build macros.
#
# Chris Weyl <cweyl@alumni.drew.edu> 2009
# Marcela Mašláňová <mmaslano@redhat.com> 2011

%__perl %{_bindir}/perl
%perl_version  %(eval "`%{__perl} -V:version`" ; echo $version | sed "s|\.[0-9]*$||")
%perl_compat perl(:MODULE_COMPAT_%{perl_version})

%__perl_full_version %(eval "`%{__perl} -V:version`" ; echo $version)

%__perl32  %{_bindir}/perl%{__perl_full_version}_32
%__perl64  %{_bindir}/perl%{__perl_full_version}_64

#############################################################################
# Perl specific macros, no longer part of rpm >= 4.15
%perl_vendorarch32 %(eval "`%{__perl32} -V:installvendorarch`"; echo $installvendorarch)
%perl_vendorarch64 %(eval "`%{__perl64} -V:installvendorarch`"; echo $installvendorarch)
%perl_vendorlib  %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%perl_archlib    %(eval "`%{__perl} -V:installarchlib`"; echo $installarchlib)
%perl_privlib    %(eval "`%{__perl} -V:installprivlib`"; echo $installprivlib)

#############################################################################
# AIX Provides / Requires macros for modules
# These macros add automatically Requires and Provides from a list definied in
# sepcfile. 
# There is three kind of macros,
# - parameter checker, use them in specfile to automatically add provides / requires
# - printer, prefixed by __, do not use it directly
#
# Printers use lua to split a provides / requires list (input as string).
# They used the splitted list to wrap provides / requires with right version
# and "perl(" "perl<VER>("... strings.

# Add "Provides: perl(<provides>) = %{version}
# Parameter checker
%perl_meta_provides %{?provide_list:%__perl_meta_provides}

# Printer
%__perl_meta_provides %{lua: \
print("Provides: ") \
for elmt in string.gmatch(rpm.expand('%{provide_list}'), "[^^%s]+") do \
  print(string.format("perl(%s) = %s ", elmt, rpm.expand("%{version}"))) \
end \
}

# Add "Requires: perl(<requires>)"
#     "Requires: perl<VER>(<provides>)
#     "Requires: perl(perl)"
# Parameter checker
%perl_meta_requires %{?require_list:%__perl_meta_requires_list} \
%{?provide_list:%__perl_meta_provides_list} \
%__perl_meta_requires

# Printer -- prints perl(perl), even if there is no require list.
%__perl_meta_requires Requires: perl(perl) = %{perl_version}

# Printer
%__perl_meta_requires_list %{lua: \
print("Requires: ") \
for elmt in string.gmatch(rpm.expand('%{require_list}'), "[^^%s]+") do \
  print(string.format("perl(%s) ", elmt)) \
end \
}

%__perl_meta_provides_list %{lua: \
print("Requires: ") \
for elmt in string.gmatch(rpm.expand('%{provide_list}'), "[^^%s]+") do \
  print(string.format("perl%s(%s) = %s ", rpm.expand("%{perl_version}"), elmt, rpm.expand("%{version}"))) \
end \
}

# Add "Provides: perl<VER>(<provides>) = %{version}"
# Parameter checker
%perl_module_provides %{?provide_list:%__perl_module_provides}

# Printer
%__perl_module_provides %{lua: \
print("Provides: ") \
for elmt in string.gmatch(rpm.expand('%{provide_list}'), "[^^%s]+") do \
  print(string.format("perl%s(%s) = %s ", rpm.expand("%{perl_version}"), elmt, rpm.expand("%{version}"))) \
end \
}

# Add "Requires: perl<VER>(<requires>)"
#     "Requires: %perl_compat
# Parameter checker
%perl_module_requires %{?require_list:%__perl_module_requires_list} \
%__perl_module_requires

# Printer -- prints perm MODULE_COMPAT, even if there is no require list.
%__perl_module_requires Requires: %perl_compat

# Printer
%__perl_module_requires_list %{lua: \
print("Requires: ") \
for elmt in string.gmatch(rpm.expand('%{require_list}'), "[^^%s]+") do \
  print(string.format("perl%s(%s) ", rpm.expand("%{perl_version}"), elmt)) \
end \
}

###############################################################################
# Create module package from %meta_name with requirements and provides.

# Package + initilisation of %module_name
# Inlcude check for %meta_name
%perl_module %{expand:
%global module_name perl%{perl_version}-%{meta_name}
%package -n %module_name
%{?!meta_name:ERROR %%{meta_name} is missing}
Summary: %summary
%perl_module_provides
%perl_module_requires
}

# Create module package description
%perl_module_desc %{expand:
%{?!desc:ERROR %%{desc} is missing}
%description -n %module_name
%desc
}

#############################################################################
# Filtering macro incantations

# By default, for perl packages we want to filter all files in _docdir from 
# req/prov scanning.
# Filtering out any provides caused by private libs in vendorarch/archlib
# (vendor/core) is done by rpmbuild since Fedora 20
# <https://fedorahosted.org/fpc/ticket/353>.
#
# Note that this must be invoked in the spec file, preferably as 
# "%{?perl_default_filter}", before any %description block.

%perl_default_filter %{expand: \
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_docdir}
%global __requires_exclude_from %{?__requires_exclude_from:%__requires_exclude_from|}^%{_docdir}
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\\\(VMS|^perl\\\\(Win32|^perl\\\\(DB\\\\)|^perl\\\\(UNIVERSAL\\\\)
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\\\(VMS|^perl\\\\(Win32
}

# fixup (and create if needed) the shbang lines in tests, so they work and
# rpmlint doesn't (correctly) have a fit
%fix_shbang_line() \
TMPHEAD=`mktemp`\
TMPBODY=`mktemp`\
for file in %* ; do \
    head -1 $file > $TMPHEAD\
    tail -n +2 $file > $TMPBODY\
    %{__perl} -pi -e '$f = /^#!/ ? "" : "#!%{__perl}$/"; $_="$f$_"' $TMPHEAD\
    cat $TMPHEAD $TMPBODY > $file\
done\
%{__perl} -MExtUtils::MakeMaker -e "ExtUtils::MM_Unix->fixin(qw{%*})"\
%{__rm} $TMPHEAD $TMPBODY\
%{nil}

