#include "../lbkes_k_eigenvalue_solver.h"

#include "ChiLua/chi_lua.h"

#include "ChiPhysics/chi_physics.h"
extern ChiPhysics& chi_physics_handler;

#include <chi_log.h>
extern ChiLog& chi_log;

using namespace LinearBoltzmann;

//###################################################################
/**Creates a k-eigenvalue solver.*/
int chiKEigenvalueLBSCreateSolver(lua_State* L)
{
  chi_log.Log(LOG_ALLVERBOSE_1)
      << "Creating k-Eigenvalue solver.";
  auto solver = new KEigenvalueSolver;

  chi_physics_handler.solver_stack.push_back(solver);

  lua_pushnumber(L, chi_physics_handler.solver_stack.size() - 1);
  return 1;
}




