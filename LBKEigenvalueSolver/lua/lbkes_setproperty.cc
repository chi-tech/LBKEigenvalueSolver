#include "../lbkes_k_eigenvalue_solver.h"

#include <chi_lua.h>

#include "ChiPhysics/chi_physics.h"
extern ChiPhysics& chi_physics_handler;

#include <chi_log.h>
extern ChiLog& chi_log;

#define MAX_ITERATIONS  1
#define TOLERANCE       2

using namespace LinearBoltzmann;

//############################################################
/**Set properties for the solver.*/
int chiLBKESSetProperty(lua_State *L)
{
  int num_args = lua_gettop(L);
  if (num_args < 2)
    LuaPostArgAmountError(__FUNCTION__, 2, num_args);

  LuaCheckNilValue(__FUNCTION__, L, 1);
  int solver_index = lua_tonumber(L, 1);

  //============================================= Get pointer to solver
  chi_physics::Solver* psolver;
  KEigenvalueSolver* solver;
  try
  {
    psolver = chi_physics_handler.solver_stack.at(solver_index);
    solver = dynamic_cast<KEigenvalueSolver*>(psolver);
    if (not solver)
    {
      chi_log.Log(LOG_ALLERROR)
          << __FUNCTION__ << ": Incorrect solver type. "
          << "Cannot cast to LinearBoltzmann::KEigenvalueSolver.";
      exit(EXIT_FAILURE);
    }
  }
  catch (const std::out_of_range& o)
  {
    chi_log.Log(LOG_ALLERROR)
        << __FUNCTION__ << ": Invalid handle to solver.";
    exit(EXIT_FAILURE);
  }

  //============================================= Get property index
  LuaCheckNilValue(__FUNCTION__, L, 2);
  int property = lua_tonumber(L,2);

  //============================================= Handle properties
  if (property == MAX_ITERATIONS)
  {
    LuaCheckNilValue(__FUNCTION__, L, 3);
    int max_iters = lua_tointeger(L, 3);

    if (max_iters <= 0)
    {
      chi_log.Log(LOG_ALLERROR)
          << __FUNCTION__ << ": Invalid max_iterations value. "
          << "Must be greater than 0.";
      exit(EXIT_FAILURE);
    }
    solver->max_iterations = static_cast<size_t>(max_iters);

    chi_log.Log(LOG_0)
        << "LinearBoltzmann::KEigenvalueSolver: "
        << "max_iterations set to " << solver->max_iterations << ".";
  }

  else if (property == TOLERANCE)
  {
    LuaCheckNilValue(__FUNCTION__, L, 3);
    double tol = lua_tonumber(L, 3);

    if (tol < 0.0 or tol > 1.0)
    {
      chi_log.Log(LOG_ALLERROR)
          << __FUNCTION__ << ": Invalid value for tolerance. "
          << "Must be in the range (0.0, 1.0].";
      exit(EXIT_FAILURE);
    }
    solver->tolerance = tol;

    char buff[100];
    sprintf(buff, "%.4e", tol);

    chi_log.Log(LOG_0)
        << "LinearBoltzmann::KEigenvalueSolver: "
        << "tolerance set to " << buff << ".";
  }
  else
  {
    chi_log.Log(LOG_ALLERROR)
        << __FUNCTION__ << ": Invalid property index.";
    exit(EXIT_FAILURE);
  }
  return 0;
}
