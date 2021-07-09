-- 1D KEigen solver test with Vacuum BC.
-- SDM: PWLD
-- Test: Final k-eigenvalue: 0.999539
num_procs = 4





--############################################### Check num_procs
if (check_num_procs == nil and chi_number_of_processes ~= num_procs) then
    chiLog(LOG_0ERROR,"Incorrect amount of processors. " ..
                      "Expected "..tostring(num_procs)..
                      ". Pass check_num_procs=false to override if possible.")
    os.exit(0, false)
end

chiMPIBarrier()

-- ##################################################
-- ##### Parameters #####
-- ##################################################

-- Mesh variables
if (L == nil) then L = 100.0 end
if (n_cells == nil) then n_cells = 50 end

-- Transport angle information
if (n_angles == nil) then n_angles = 16 end 
if (scattering_order == nil) then scattering_order = 0 end

-- k-eigenvalue iteration parameters
if (max_iterations == nil) then max_iterations = 5000 end
if (tolerance == nil) then tolerance = 1e-8 end

-- Source iteration parameters
if (max_source_iterations == nil) then max_source_iterations = 500 end
if (source_iteration_tolerance == nil) then source_iteration_tolerance = 1e-4 end

-- Delayed neutrons
if (use_precursors == nil) then use_precursors = true end

-- NOTE: For command line inputs, specify as:
--       variable=[[argument]]

-- Cross section file
if (xsfile == nil) then
    xsfile = "Test/simple_fissile.csx"
end

-- ##################################################
-- ##### Run problem #####
-- ##################################################

--############################################### Setup mesh
-- Define nodes
nodes = {}
dx = L/n_cells
for i=0,n_cells do
  nodes[i+1] = i*dx
end

-- Create the mesh
chiMeshHandlerCreate()
_, region = chiMeshCreateUnpartitioned1DOrthoMesh(nodes)
chiVolumeMesherSetProperty(PARTITION_TYPE, PARMETIS)
chiVolumeMesherExecute()

--############################################### Set Material IDs
vol0 = chiLogicalVolumeCreate(RPP,-1000,1000,-1000,1000,-1000,1000)
chiVolumeMesherSetProperty(MATID_FROMLOGICAL,vol0,0)

--############################################### Add materials
materials = {}

-- Define cross sections
xs = chiPhysicsTransportXSCreate()
chiPhysicsTransportXSSet(xs,CHI_XSFILE,xsfile)
combo = {{xs, 1.0}}
xs_macro = chiPhysicsTransportXSMakeCombined(combo)

-- Add material1
materials[1] = chiPhysicsAddMaterial("Fissile Material")
chiPhysicsMaterialAddProperty(materials[1], TRANSPORT_XSECTIONS)
chiPhysicsMaterialSetProperty(materials[1], TRANSPORT_XSECTIONS,EXISTING, xs_macro)
G = chiPhysicsMaterialGetProperty(materials[1], TRANSPORT_XSECTIONS)["num_groups"]

--############################################### Setup Physics
-- Define solver
phys = chiKEigenvalueLBSCreateSolver()

-- Add region and discretization
chiSolverAddRegion(phys, region)
chiLBSSetProperty(phys, DISCRETIZATION_METHOD, PWLD)

-- Create quadrature and define scattering order
pquad = chiCreateProductQuadrature(GAUSS_LEGENDRE, n_angles)
chiLBSSetProperty(phys,SCATTERING_ORDER, scattering_order)

-- Create groups
for _ = 0, G-1 do
    chiLBSCreateGroup(phys)
end

-- Create groupset
gs = chiLBSCreateGroupset(phys)
chiLBSGroupsetAddGroups(phys,gs, 0, G-1)
chiLBSGroupsetSetQuadrature(phys, gs, pquad)
chiLBSGroupsetSetMaxIterations(phys, gs, max_source_iterations)
chiLBSGroupsetSetResidualTolerance(phys, gs, source_iteration_tolerance )
chiLBSGroupsetSetIterativeMethod(phys, gs, NPT_GMRES_CYCLES)
chiLBSGroupsetSetAngleAggregationType(phys, gs, LBSGroupset.ANGLE_AGG_SINGLE)

-- Additional parameters
chiLBSSetMaxKIterations(phys, max_iterations)
chiLBSSetKTolerance(phys, tolerance)
chiLBSSetUsePrecursors(phys, use_precursors)
chiLBSSetProperty(phys, VERBOSE_INNER_ITERATIONS, false)
chiLBSSetProperty(phys, VERBOSE_OUTER_ITERATIONS, false)

--############################################### Initialize and Execute Solver
chiKEigenvalueLBSInitialize(phys)
chiKEigenvalueLBSExecute(phys)

--############################################### Get field functions
--############################################### Line plot
--############################################### Volume integrations
--############################################### Exports
--############################################### Plots