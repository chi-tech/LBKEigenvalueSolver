#include "lbkes_k_eigenvalue_solver.h"

#include <chi_log.h>
extern ChiLog& chi_log;

#include <iomanip>

using namespace LinearBoltzmann;

//###################################################################
/**Execute a k-eigenvalue linear boltzmann solver.*/
void KEigenvalueSolver::Execute()
{
  PowerIteration();
  chi_log.Log(LOG_0)
      << "LinearBoltzmann::KEigenvalueSolver execution completed\n\n";
}