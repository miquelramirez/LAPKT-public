import sys
import os

def create_planner_dir( base_dir, planner_id ) : 
	print >> sys.stdout, "Deploying planner:", planner_id
	planner_folder = os.path.join( base_dir, planner_id )

	if os.path.exists( planner_folder ) :
		print >> sys.stdout, "Folder", planner_folder, "already exists, deleting..."
		rv = os.system( 'rm -rf %s'%planner_folder )
		if rv != 0 :
			print >> sys.stderr, "\tFolder", planner_folder, "could not be deleted, aborting!"
			sys.exit(1)

	print >> sys.stdout, "Creating folder", planner_folder
	rv = os.system( 'mkdir -p %s'%planner_folder )
	if rv != 0 :
		print >> sys.stderr, "\tCould not create folder", planner_folder, "aborting..."
		sys.exit(1)

	return os.path.join( base_dir, planner_id )

def copy_files( planner_dir, planner_name ) :
	
	dirs = [ 'include', 'interfaces', 'external', 'src', 'planners/python', 'planners/%s'%planner_name ]

	cmd_template = 'cp -ra %s %s'
	print >> sys.stdout, "Creating folder %s/planners"%planner_dir
	build_base_dir = os.path.join( planner_dir, 'planners' )
	rv = os.system( 'mkdir -p %s'%build_base_dir )

	if rv != 0 :
		print >> sys.stderr, "Could not create %s, aborting..."%build_base_dir
		sys.exit(1)

	for directory in dirs :
	
		if 'planners' in directory :
			dest_dir = build_base_dir	
		else :
			dest_dir = planner_dir

		print >> sys.stdout, "Copying %s to %s"%(directory, dest_dir)
		rv = os.system( cmd_template%(directory, dest_dir) )

		if rv != 0 :
			print >> sys.stderr, "Could not copy", directory, ", aborting..."
			sys.exit(1)

def create_build_script( home_dir, planner, files ) :

	script_filename = os.path.join( home_dir, 'build' )
	
	with open( script_filename, 'w' ) as out :
		
		print >> out, "#!/bin/bash"
		build_dir = os.path.join( 'planners', planner )
		print >> out, "cd %s"%build_dir
		print >> out, "scons -c"
		print >> out, "python2.7 build.py"
		print >> out, "cd ../.."
		for filename in files :
			print >> out, 'echo "Copying %s..."'%filename
			print >> out, "cp %s ."%(os.path.join( build_dir, filename ) )
			print >> out, "cp -ra external/fd ."

	os.system( 'chmod u+x %s'%script_filename )

def create_run_script( home_dir, executable ) :

	script_filename = os.path.join( home_dir, 'plan' )

	with open( script_filename, 'w' ) as out :
		print >> out, "#!/bin/bash"
		print >> out, "python2.7 %s $1 $2 $3"%executable
	
	os.system( 'chmod u+x %s'%script_filename )

def deploy_seq_agl_siw( base_dir ) :

	planner_id = 'seq-agl-siw'
	
	planner_dir = create_planner_dir( base_dir, planner_id )
	
	copy_files( planner_dir, 'siw' )	

	planner_files = [ 'siw.py', 'libsiw.so' ]

	create_build_script( planner_dir, 'siw', planner_files )
	
	create_run_script( planner_dir, 'siw.py' )

def deploy_seq_agl_siw_unit_cost( base_dir ) :
	planner_id = 'seq-agl-siw-unit-cost'
	
	planner_dir = create_planner_dir( base_dir, planner_id )
	
	copy_files( planner_dir, 'siw' )	

	planner_files = [ 'siw-unit-cost.py', 'libsiw.so' ]

	create_build_script( planner_dir, 'siw', planner_files )
	
	create_run_script( planner_dir, 'siw-unit-cost.py' )

def deploy_seq_agl_bfs_f_unit_cost( base_dir ) :
	planner_id = 'seq-agl-bfs-f-unit-cost'
	
	planner_dir = create_planner_dir( base_dir, planner_id )
	
	copy_files( planner_dir, 'bfs_f' )	

	planner_files = [ 'bfs_f-unit-cost.py', 'libbfsf.so' ]

	create_build_script( planner_dir, 'bfs_f', planner_files )
	
	create_run_script( planner_dir, 'bfs_f-unit-cost.py' )

def deploy_seq_agl_bfs_f( base_dir ) :
	planner_id = 'seq-agl-bfs-f'
	
	planner_dir = create_planner_dir( base_dir, planner_id )
	
	copy_files( planner_dir, 'bfs_f' )	

	planner_files = [ 'bfs_f.py', 'libbfsf.so' ]

	create_build_script( planner_dir, 'bfs_f', planner_files )
	
	create_run_script( planner_dir, 'bfs_f.py' )

def deploy_sat_bfs_f( base_dir ) :
	planner_id = 'seq-sat-bfs-f'
	
	planner_dir = create_planner_dir( base_dir, planner_id )
	
	copy_files( planner_dir, 'at_bfs_f' )	

	planner_files = [ 'at_bfs_f.py', 'libatbfsf.so' ]

	create_build_script( planner_dir, 'at_bfs_f', planner_files )
	
	create_run_script( planner_dir, 'at_bfs_f.py' )


def main() :
	base_dir = '~'
	if len(sys.argv) == 2 :
		base_dir = sys.argv[1]
		if not os.path.exists( base_dir ) :
			print >> sys.stderr, "Base folder", base_dir, "does not exist!"
			sys.exit(1)
	
	deploy_seq_agl_siw( base_dir )
	deploy_seq_agl_siw_unit_cost( base_dir )
	deploy_seq_agl_bfs_f( base_dir )
	deploy_seq_agl_bfs_f_unit_cost( base_dir )
	deploy_sat_bfs_f( base_dir )

if __name__ == "__main__" :
	main()
