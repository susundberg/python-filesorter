import argparse
import os
import datetime
import shutil
import hashlib

def print_info( string ):
    print ("II: " + string)
    
def print_warning( string ):
    print ("WW: " + string)

    
def get_arguments():
   parser = argparse.ArgumentParser(description='Process files.')
   parser.add_argument("input_path", help="What files to move")
   parser.add_argument("target_path", help="where to move files")
   parser.add_argument("--dry_run", help="Print only what to do", dest='dry_run', action='store_true' )
   return parser.parse_args()


def find_new_free_name( path, fn ):
    for loop in range(2**10):
        fn_list = fn.split(".")
        fn_list[-2] += "_%d" % loop
        
        fn_new = ".".join( fn_list )
        new_name = os.path.join( path, fn_new )
        if not os.path.exists( new_name ):
            return new_name
    raise Exception("There are too many same named files, sanity check fail")    
    
def check_for_duplicate( fn1, fn2 ):
    def md5(fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(2**10), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()    
    return md5( fn1 ) == md5( fn2 )

def main( args ):
    
   for dirpath, dnames, fnames in os.walk( args.input_path ):
    for filename in fnames:
        full_source = os.path.join( dirpath, filename )
        stat = os.stat( full_source )
        time = datetime.date.fromtimestamp( stat.st_mtime ) 
        new_path = "%04d-%02d" % ( time.year ,time.month )
        
        
        full_target_path = os.path.join( args.target_path, new_path)
        full_target = os.path.join( full_target_path, filename )
                                        
        
        if not os.path.exists( full_target_path ):
           os.makedirs( full_target_path )
        else:
           if os.path.exists( full_target ):
               if check_for_duplicate( full_source, full_target ) == True:
                   print_info("Duplicate file '%s' - '%s': removing source" % (full_source, full_target ) )
                   if args.dry_run == False:
                       shutil.remove( full_source )
               else: # File exists, but not duplicate -> two same named files
                   
                   new_full_target = find_new_free_name( full_target_path, filename )
                   print_warning("Files '%s' - '%s' same name, different md5, renaming to %s" % 
                                  (full_source, full_target, new_full_target ))
                   full_target = new_full_target
                   
        if args.dry_run == True:
            print_info( "mv %s %s" % ( full_source, full_target ) )
    

if __name__ == "__main__":
    main( get_arguments() )
   
   