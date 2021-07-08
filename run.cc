#include "chi_runtime.h"
#include "ChiConsole/chi_console.h"


int main(int argc, char** argv)
{
  ChiTech::Initialize(argc,argv);
  ChiConsole& console = ChiConsole::GetInstance();

  auto L = console.consoleState;
  #include "ChiMacros/lua_register_macro.h"
  #include "lua/lua_register.h"
  #include "LBKEigenvalueSolver/lua/lua_register.h"

  ChiTech::RunBatch(argc, argv);

  ChiTech::Finalize();
  return 0;
}
