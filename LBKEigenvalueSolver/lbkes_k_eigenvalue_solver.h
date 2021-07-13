#ifndef LBKES_K_EIGENVALUE_SOLVER_H
#define LBKES_K_EIGENVALUE_SOLVER_H

#include "LinearBoltzmannSolver/lbs_linear_boltzmann_solver.h"
#include "ChiMath/UnknownManager/unknown_manager.h"

#include <string>

namespace LinearBoltzmann
{

/**A k-eigenvalue linear boltzmann transport solver.*/
class KEigenvalueSolver : public LinearBoltzmann::Solver
{
public:
  /**The current k-eigenvalue estimate.*/
  double k_eff = 1.0;

  /**Iterative parameters.*/
  size_t max_iterations = 1000;
  double tolerance = 1.0e-8;

  /**Delayed neutron precursor information.*/
  size_t num_precursors;
  size_t max_num_precursors_per_material;

  chi_math::UnknownManager precursor_uk_man;

  std::vector<double> precursor_new_local;

public:

  void Initialize() override;
  void Execute() override;

  virtual void ComputePrecursors();

  // IterativeMethods
  void PowerIteration();

  // Iterative operations
  double ComputeFissionProduction();
};

}

#endif //LBKES_K_EIGENVALUE_SOLVER_H