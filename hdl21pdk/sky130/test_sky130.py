import hdl21 as h
from . import sky130


def gethasmos():
    # Create a simple Module with each of the default-param Mos types
    hasmos = h.Module(name="hasmos")
    z = hasmos.z = h.Signal()
    hasmos.n = h.Nmos(h.MosParams())(d=z, g=z, s=z, b=z)
    hasmos.p = h.Pmos(h.MosParams())(d=z, g=z, s=z, b=z)

    # Checks on the initial Module
    assert isinstance(hasmos.n, h.Instance)
    assert isinstance(hasmos.p, h.Instance)
    assert isinstance(hasmos.n.of, h.PrimitiveCall)
    assert isinstance(hasmos.p.of, h.PrimitiveCall)

    return hasmos


def test_compile():
    hasmos = gethasmos()

    # Compile it for the PDK
    pkg = h.to_proto(hasmos)
    pdk_pkg = sky130.compile(pkg)

    # Import it back into Modules & Namespaces
    ns = h.from_proto(pdk_pkg)
    rt = ns.hdl21pdk.sky130.test_sky130.hasmos

    # And check what came back
    assert isinstance(rt.n, h.Instance)
    assert isinstance(rt.p, h.Instance)
    assert isinstance(rt.n.of, h.ExternalModuleCall)
    assert isinstance(rt.p.of, h.ExternalModuleCall)
    assert isinstance(rt.n.of.params, dict)
    assert isinstance(rt.p.of.params, dict)


def test_netlist():
    hasmos = gethasmos()

    # Netlist it for the PDK
    pkg = h.to_proto(hasmos)
    sky130.netlist(pkg, open("scratch/whatever.scs", "w"), "spectre")

