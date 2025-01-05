from typedschema import FQTN


def test_fqtn():
    t = FQTN("data_warehouse1", "customers")

    assert f"{t}" == "data_warehouse1.customers"

    t2 = FQTN.of(t)
    assert f"{t2}" == "data_warehouse1.customers"
    t3 = FQTN.of("data_warehouse1.customers")
    assert t3.ns == "data_warehouse1"
    assert t3.name == "customers"
    assert t3 == "data_warehouse1.customers"
