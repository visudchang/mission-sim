extern "C" double compute_orbital_energy(double r, double v) {
        // Earth's gravitational parameter G * M
        const double mu = 3.986004418e14;
        return 0.5 * v * v - mu / r;
    }