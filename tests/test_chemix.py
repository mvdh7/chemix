import chemix as cx


def test_Solution():
    sol = cx.Solution()
    assert isinstance(sol, cx.Solution)
    assert isinstance(sol.solvent_density, float)
    assert isinstance(sol.solvent_mass, float)
    assert isinstance(sol.solvent_volume, float)


def test_add_salt():
    sol = cx.Solution()
    sol.add_salt("NaCl", 0.05)
    assert isinstance(sol.molality, dict)
    assert "Na" in sol.molality
    assert "Cl" in sol.molality


# test_Solution()
# test_add_salt()
