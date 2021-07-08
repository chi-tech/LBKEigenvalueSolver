#ifndef _K_EIGENVALUE_SOLVER_H
#define _K_EIGENVALUE_SOLVER_H

#include "LinearBoltzmannSolver/lbs_linear_boltzmann_solver.h"
#include "ChiMath/UnknownManager/unknown_manager.h"

#include <string>

namespace LinearBoltzmann
{

/**A k-eigenvalue linear boltzmann transport solver.*/
class KEigenvalueSolver : public LinearBoltzmann::Solver
{
public:
  double k_eff = 1.0;

  size_t num_precursors;
  size_t max_num_precursors_per_material;

  chi_math::UnknownManager precursor_uk_man;

  std::vector<double> precursor_new_local;

  void Initialize() override;
  void Execute() override;

  virtual void ComputePrecursors();

  // IterativeMethods
  void PowerIteration();

  // Iterative operations
  double ComputeFissionProduction();
};

}

#endif //_K_EIGENVALUE_SOLVER_H