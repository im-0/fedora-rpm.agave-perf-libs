%global agave_suffix testnet

# Check `--device` in `ispc --help` for available options.
%global validator_target_cpu core-avx2

Name:       agave-perf-libs-%{agave_suffix}
Version:    0.19.3
Release:    1%{?dist}
Summary:    C and CUDA libraries to enhance Agave/Solana (no CUDA, only SIMD)

License:    Apache-2.0
URL:        https://github.com/solana-labs/solana-perf-libs/
Source0:    https://github.com/solana-labs/solana-perf-libs/archive/v%{version}/solana-perf-libs-%{version}.tar.gz

Patch0: override-device-for-avx512skx.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ispc


%description
C and CUDA libraries to enhance Agave/Solana (no CUDA, only SIMD).


%prep
%autosetup -N -b0 -n solana-perf-libs-%{version}
%patch -P 0 -p1


%build
cd src/poh-simd
%make_build ISPC_FLAGS="-g -O3 --device=%{validator_target_cpu} --opt=fast-masked-vload --opt=force-aligned-memory --pic -I."


%install
mkdir -p %{buildroot}/opt/agave/%{agave_suffix}/bin/perf-libs
cp -p \
        src/poh-simd/libs/libpoh-simd.so \
        %{buildroot}/opt/agave/%{agave_suffix}/bin/perf-libs/


%files
%dir /opt/agave
%dir /opt/agave/%{agave_suffix}
%dir /opt/agave/%{agave_suffix}/bin
%dir /opt/agave/%{agave_suffix}/bin/perf-libs
/opt/agave/%{agave_suffix}/bin/perf-libs/libpoh-simd.so


%changelog
* Wed Aug 7 2024 Ivan Mironov <mironov.ivan@gmail.com> - 0.19.3-1
- Initial packaging
