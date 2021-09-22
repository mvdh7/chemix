import teos10


class Solution:
    def __init__(self, solvent_mass=1.0, solvent_volume=None):
        """Mass in kg, volume in litres, density in kg/litre."""
        tempK = 298.15  # add as kwarg later
        presPa = 101325  # add as kwarg later
        self.solvent_density = 1e-3 * teos10.properties.density(
            float(tempK), float(presPa), gibbsfunc=teos10.gibbs.purewater
        )
        if solvent_volume is not None:
            solvent_mass = solvent_volume * self.solvent_density
        else:
            solvent_volume = solvent_mass / self.solvent_density
        self.solvent_mass = solvent_mass
        self.solution_mass = solvent_mass
        self.solvent_volume = solvent_volume
        self.amount = {}  # mol
        self.concentration = {}  # mol/litre
        self.content = {}  # mol/kg-solution
        self.mass = {}  # kg
        self.molality = {}  # mol/kg-solvent

    def _add_empty_solute(self, salt):
        for d in [
            self.amount,
            self.concentration,
            self.content,
            self.mass,
            self.molality,
        ]:
            if salt not in d:
                d[salt] = 0.0

    def add_salt(self, salt, salt_mass):
        """Mass in kg."""
        salt_splitter = {"NaCl": dict(Na=1, Cl=1)}
        salt_ram = {"NaCl": 58.44}
        solute_ram = {"Na": 22.989769, "Cl": 35.453}
        salt_amount = 1e3 * salt_mass / salt_ram[salt]  # mol
        for solute, solute_factor in salt_splitter[salt].items():
            self._add_empty_solute(solute)
            self.amount[solute] += salt_amount * solute_factor
            solute_mass = salt_amount * solute_factor * solute_ram[solute] * 1e-3
            self.mass[solute] += solute_mass
            self.solution_mass += solute_mass
            self._update_ratios_after_add_salt()

    def _update_ratios_after_add_salt(self):
        for solute, amount in self.amount.items():
            self.concentration[solute] = amount / self.solvent_volume
            self.content[solute] = amount / self.solution_mass
            self.molality[solute] = amount / self.solvent_mass
